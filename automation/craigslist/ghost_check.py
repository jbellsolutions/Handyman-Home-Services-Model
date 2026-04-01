"""
Ghost Check — Verify Craigslist ads are actually visible.

CL sometimes "ghost-bans" ads: they appear to you but are invisible to everyone else.
This script checks your ads from a clean browser (no cookies, different fingerprint)
to confirm they are actually live and visible.

Usage:
    python craigslist/ghost_check.py                # Check all active ads
    python craigslist/ghost_check.py --url URL       # Check a specific ad URL
    python craigslist/ghost_check.py --search        # Search CL for your ads by title
"""
import asyncio
import argparse
import os
import sys
import yaml
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from playwright.async_api import async_playwright
from dotenv import load_dotenv
from shared.db import init_db, get_active_ads, update_ad_status
from shared.logger import get_logger

load_dotenv(Path(__file__).parent.parent / '.env')

logger = get_logger('ghost_check')

SCREENSHOTS_DIR = Path(__file__).parent.parent / 'screenshots'
SETTINGS_PATH = Path(__file__).parent.parent / 'config' / 'settings.yaml'


def load_settings():
    if SETTINGS_PATH.exists():
        with open(SETTINGS_PATH) as f:
            return yaml.safe_load(f)
    return {}


async def check_url(page, url):
    """Check if a specific CL ad URL is accessible."""
    try:
        response = await page.goto(url, wait_until='networkidle', timeout=15000)
        await asyncio.sleep(2)

        # Check for removed/expired/flagged indicators
        page_text = await page.inner_text('body')

        if response and response.status == 404:
            return 'REMOVED', 'Page returned 404'

        if 'this posting has been flagged' in page_text.lower():
            return 'FLAGGED', 'Ad was flagged by CL community'

        if 'this posting has been deleted' in page_text.lower():
            return 'DELETED', 'Ad was deleted'

        if 'this posting has expired' in page_text.lower():
            return 'EXPIRED', 'Ad has expired'

        if 'posting not found' in page_text.lower():
            return 'NOT_FOUND', 'Posting not found — likely ghosted or removed'

        # Check if the posting body is present (sign of a live ad)
        posting_body = page.locator('#postingbody')
        if await posting_body.count() > 0:
            title = await page.locator('.postingtitletext').inner_text() if await page.locator('.postingtitletext').count() > 0 else 'Unknown'
            return 'LIVE', f'Ad is visible: {title[:60]}'

        return 'UNKNOWN', 'Page loaded but could not confirm ad content'

    except Exception as e:
        return 'ERROR', f'Failed to check: {e}'


async def search_for_ads(page, metro_url, phone_number):
    """Search CL for ads matching our phone number to find ghosted ones."""
    results = []
    search_url = f'{metro_url}/search/bbb?query={phone_number}'

    try:
        await page.goto(search_url, wait_until='networkidle', timeout=15000)
        await asyncio.sleep(2)

        listings = page.locator('.cl-search-result, .result-row')
        count = await listings.count()

        for i in range(min(count, 20)):
            listing = listings.nth(i)
            try:
                title_el = listing.locator('.titlestring, .result-title')
                link_el = listing.locator('a').first
                title = await title_el.inner_text() if await title_el.count() > 0 else 'Unknown'
                href = await link_el.get_attribute('href') if await link_el.count() > 0 else ''
                results.append({'title': title, 'url': href})
            except Exception:
                continue

        return results
    except Exception as e:
        logger.error(f"Search failed: {e}")
        return []


async def run_ghost_check(url=None, search_mode=False):
    """Run ghost check against active ads or a specific URL."""
    settings = load_settings()
    metro_url = settings.get('craigslist', {}).get('metro_url', 'https://jacksonville.craigslist.org')
    phone = os.getenv('TRACKING_PHONE', os.getenv('BUSINESS_PHONE', ''))

    async with async_playwright() as p:
        # Launch a CLEAN browser — no cookies, no saved state, no proxy
        # This simulates a random person browsing CL
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080},
            locale='en-US',
        )
        page = await context.new_page()

        try:
            if url:
                # Check specific URL
                status, message = await check_url(page, url)
                print(f"\n  [{status}] {url}")
                print(f"  {message}\n")
                return

            if search_mode:
                # Search for our ads
                if not phone:
                    print("\n  No phone number configured. Set TRACKING_PHONE in .env\n")
                    return

                print(f"\n  Searching CL for ads with phone: {phone}...")
                results = await search_for_ads(page, metro_url, phone.replace('-', '').replace('+1', ''))

                if results:
                    print(f"\n  Found {len(results)} ads:\n")
                    for r in results:
                        print(f"  - {r['title'][:60]}")
                        print(f"    {r['url']}")
                else:
                    print("\n  No ads found. Your ads may be ghosted or not yet indexed.\n")
                return

            # Check all active ads from database
            await init_db()
            active_ads = await get_active_ads('craigslist')

            if not active_ads:
                print("\n  No active ads in database. Post some ads first.\n")
                return

            print(f"\n=== Ghost Check — {len(active_ads)} Active Ads ===\n")

            live_count = 0
            dead_count = 0

            for ad in active_ads:
                if not ad['post_url'] or ad['post_url'] == 'test':
                    continue

                status, message = await check_url(page, ad['post_url'])

                icon = {
                    'LIVE': 'PASS',
                    'FLAGGED': 'FAIL',
                    'DELETED': 'FAIL',
                    'EXPIRED': 'WARN',
                    'NOT_FOUND': 'FAIL',
                    'REMOVED': 'FAIL',
                    'ERROR': 'WARN',
                    'UNKNOWN': 'WARN',
                }.get(status, 'WARN')

                print(f"  [{icon}] {ad['title'][:50]}")
                print(f"         {message}")

                if status == 'LIVE':
                    live_count += 1
                else:
                    dead_count += 1
                    if status in ('FLAGGED', 'DELETED', 'REMOVED', 'NOT_FOUND'):
                        await update_ad_status(ad['id'], 'removed')

                await asyncio.sleep(2)  # Don't hammer CL

            print(f"\n  Results: {live_count} live, {dead_count} dead/removed")
            if dead_count > 0:
                print("  Dead ads need to be reposted with different content.\n")
            else:
                print("  All ads are live and visible.\n")

        finally:
            await browser.close()


def main():
    parser = argparse.ArgumentParser(description='Ghost Check — Verify CL ads are visible')
    parser.add_argument('--url', type=str, help='Check a specific ad URL')
    parser.add_argument('--search', action='store_true', help='Search CL for your ads')
    args = parser.parse_args()

    asyncio.run(run_ghost_check(url=args.url, search_mode=args.search))


if __name__ == '__main__':
    main()
