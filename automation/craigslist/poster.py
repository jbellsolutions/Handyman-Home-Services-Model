"""
Craigslist Posting Agent — Home Services Lead Machine

Posts ads to Craigslist using GoLogin anti-detect browser profiles
with per-account proxy isolation and multi-account rotation.

Usage:
    python craigslist/poster.py --test          # Test one ad (visible browser, no submit)
    python craigslist/poster.py --post          # Post next scheduled ad
    python craigslist/poster.py --post-all      # Post all scheduled ads for today
    python craigslist/poster.py --schedule      # Run on daily schedule (background)
    python craigslist/poster.py --status        # Show posting status
    python craigslist/poster.py --renew         # Renew ads older than 48 hours

Requirements:
    - GoLogin account + API token (gologin.com) OR AdsPower
    - ISP proxy per CL account (brightdata.com or similar)
    - 2-3 CL accounts (each with unique email + phone)
    - Photos in ad_templates/images/ folders

Without GoLogin (fallback):
    - Uses basic Playwright with anti-detection flags
    - Less safe but works for testing and low-volume posting
"""
import asyncio
import argparse
import json
import os
import random
import sys
import yaml
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from playwright.async_api import async_playwright
from dotenv import load_dotenv
from shared.db import init_db, log_ad, get_todays_ads, get_active_ads
from shared.logger import get_logger

load_dotenv(Path(__file__).parent.parent / '.env')

logger = get_logger('craigslist')

# --- Paths ---
TEMPLATES_PATH = Path(__file__).parent / 'ad_templates' / 'templates.yaml'
IMAGES_DIR = Path(__file__).parent / 'ad_templates' / 'images'
PROFILES_DIR = Path(__file__).parent.parent / 'profiles' / 'craigslist'
SCREENSHOTS_DIR = Path(__file__).parent.parent / 'screenshots'
SETTINGS_PATH = Path(__file__).parent.parent / 'config' / 'settings.yaml'

# --- Config from .env ---
GOLOGIN_TOKEN = os.getenv('GOLOGIN_API_TOKEN', '')
BUSINESS_PHONE = os.getenv('TRACKING_PHONE', os.getenv('BUSINESS_PHONE', ''))

# CL accounts loaded from .env
CL_ACCOUNTS = []
for i in range(1, 4):
    email = os.getenv(f'CL_ACCOUNT_{i}_EMAIL', '')
    password = os.getenv(f'CL_ACCOUNT_{i}_PASSWORD', '')
    phone = os.getenv(f'CL_ACCOUNT_{i}_PHONE', '')
    if email:
        CL_ACCOUNTS.append({
            'id': i,
            'email': email,
            'password': password,
            'phone': phone,
            'profile_dir': PROFILES_DIR / f'account_{i}',
            'gologin_profile_id': os.getenv(f'GOLOGIN_PROFILE_{i}', ''),
            'posts_today': 0,
            'max_posts_per_day': 3,
        })

# Proxy from .env
PROXY_HOST = os.getenv('PROXY_HOST', '')
PROXY_PORT = os.getenv('PROXY_PORT', '')
PROXY_USER = os.getenv('PROXY_USER', '')
PROXY_PASS = os.getenv('PROXY_PASS', '')

CL_CATEGORIES = {
    'skilled_trade_services': 'skilled trade services',
    'household_services': 'household services',
}


def load_settings():
    """Load settings from YAML."""
    if SETTINGS_PATH.exists():
        with open(SETTINGS_PATH) as f:
            return yaml.safe_load(f)
    return {}


def load_templates():
    """Load ad templates from YAML."""
    with open(TEMPLATES_PATH) as f:
        data = yaml.safe_load(f)
    return data.get('templates', {})


def get_metro_url():
    """Get the CL metro URL from settings."""
    settings = load_settings()
    return settings.get('craigslist', {}).get('metro_url', 'https://jacksonville.craigslist.org')


def pick_ad(templates, template_name, category, used_today=None):
    """Pick a random title/body variant, avoiding today's used combos."""
    used_today = used_today or []
    template = templates.get(template_name)
    if not template:
        logger.error(f"Template '{template_name}' not found")
        return None

    phone = BUSINESS_PHONE
    settings = load_settings()
    city = settings.get('business', {}).get('city', '')
    biz_name = settings.get('business', {}).get('name', '')

    for title in random.sample(template['titles'], len(template['titles'])):
        for body in random.sample(template['bodies'], len(template['bodies'])):
            combo_key = f"{template_name}:{category}:{title[:30]}"
            if combo_key not in used_today:
                filled_body = body.replace('{phone}', phone) \
                                  .replace('{city}', city) \
                                  .replace('{business_name}', biz_name)
                return {
                    'template_name': template_name,
                    'title': title,
                    'body': filled_body,
                    'images_folder': template.get('images_folder', ''),
                    'category': category,
                }

    # Fallback
    body = random.choice(template['bodies'])
    return {
        'template_name': template_name,
        'title': random.choice(template['titles']),
        'body': body.replace('{phone}', phone).replace('{city}', city).replace('{business_name}', biz_name),
        'images_folder': template.get('images_folder', ''),
        'category': category,
    }


def get_images(images_folder):
    """Get image paths for an ad template."""
    folder = IMAGES_DIR / images_folder
    if not folder.exists():
        logger.warning(f"Images folder not found: {folder}")
        return []
    images = sorted(folder.glob('*.jpg')) + sorted(folder.glob('*.png'))
    return [str(p) for p in images[:8]]


def pick_account(used_accounts_today=None):
    """Pick the CL account with the fewest posts today."""
    used_accounts_today = used_accounts_today or {}
    if not CL_ACCOUNTS:
        return None

    available = []
    for acct in CL_ACCOUNTS:
        posts_today = used_accounts_today.get(acct['id'], 0)
        if posts_today < acct['max_posts_per_day']:
            available.append((acct, posts_today))

    if not available:
        logger.warning("All accounts at daily post limit")
        return None

    # Pick account with fewest posts today
    available.sort(key=lambda x: x[1])
    return available[0][0]


def get_proxy_config():
    """Build Playwright proxy config."""
    if not PROXY_HOST:
        return None
    return {
        'server': f'http://{PROXY_HOST}:{PROXY_PORT}',
        'username': PROXY_USER,
        'password': PROXY_PASS,
    }


# --- Human-like behavior simulation ---

async def human_type(page, selector, text, min_delay=40, max_delay=120):
    """Type text with human-like speed variation."""
    element = page.locator(selector)
    await element.click()
    await asyncio.sleep(random.uniform(0.2, 0.5))
    for char in text:
        await element.type(char, delay=random.uniform(min_delay, max_delay))
        # Occasional pause (thinking)
        if random.random() < 0.05:
            await asyncio.sleep(random.uniform(0.3, 1.0))


async def human_delay(min_sec=1, max_sec=3):
    """Random delay simulating human reading/thinking."""
    await asyncio.sleep(random.uniform(min_sec, max_sec))


async def random_mouse_movement(page):
    """Simulate random mouse movement."""
    x = random.randint(100, 1200)
    y = random.randint(100, 600)
    await page.mouse.move(x, y)
    await asyncio.sleep(random.uniform(0.1, 0.3))


# --- GoLogin Integration ---

async def launch_gologin_profile(profile_id):
    """Launch a GoLogin browser profile via API and return CDP endpoint."""
    if not GOLOGIN_TOKEN or not profile_id:
        return None

    try:
        import aiohttp
        async with aiohttp.ClientSession() as session:
            # Start the profile
            async with session.post(
                f'https://api.gologin.com/browser/{profile_id}/start',
                headers={'Authorization': f'Bearer {GOLOGIN_TOKEN}'},
                json={'isHeadless': False}
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    ws_url = data.get('wsUrl') or data.get('ws', {}).get('puppeteer')
                    logger.info(f"GoLogin profile {profile_id} started, CDP: {ws_url}")
                    return ws_url
                else:
                    logger.error(f"GoLogin start failed: {resp.status} {await resp.text()}")
                    return None
    except ImportError:
        logger.error("aiohttp not installed — pip install aiohttp")
        return None
    except Exception as e:
        logger.error(f"GoLogin error: {e}")
        return None


async def stop_gologin_profile(profile_id):
    """Stop a GoLogin browser profile."""
    if not GOLOGIN_TOKEN or not profile_id:
        return
    try:
        import aiohttp
        async with aiohttp.ClientSession() as session:
            await session.put(
                f'https://api.gologin.com/browser/{profile_id}/stop',
                headers={'Authorization': f'Bearer {GOLOGIN_TOKEN}'}
            )
            logger.info(f"GoLogin profile {profile_id} stopped")
    except Exception as e:
        logger.warning(f"GoLogin stop error: {e}")


# --- Browser Creation ---

async def create_browser(playwright, account=None, headless=True):
    """Launch browser — GoLogin if available, fallback to basic Playwright."""
    # Try GoLogin first
    if account and account.get('gologin_profile_id') and GOLOGIN_TOKEN:
        ws_url = await launch_gologin_profile(account['gologin_profile_id'])
        if ws_url:
            browser = await playwright.chromium.connect_over_cdp(ws_url)
            context = browser.contexts[0] if browser.contexts else await browser.new_context()
            return browser, context, 'gologin'

    # Fallback: basic Playwright with anti-detection
    logger.info("Using basic Playwright (no GoLogin). Less safe for production posting.")

    os.makedirs(PROFILES_DIR, exist_ok=True)
    profile_dir = account['profile_dir'] if account else PROFILES_DIR / 'default'
    os.makedirs(profile_dir, exist_ok=True)

    proxy = get_proxy_config()
    launch_args = [
        '--disable-blink-features=AutomationControlled',
        '--disable-infobars',
        '--no-first-run',
    ]

    # Randomize fingerprint per account
    resolutions = [
        {'width': 1366, 'height': 768},
        {'width': 1440, 'height': 900},
        {'width': 1536, 'height': 864},
        {'width': 1920, 'height': 1080},
    ]
    user_agents = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.2 Safari/605.1.15',
    ]

    # Use account id as seed for consistent fingerprint per account
    seed = account['id'] if account else 0
    rng = random.Random(seed)
    viewport = rng.choice(resolutions)
    ua = rng.choice(user_agents)

    settings = load_settings()
    city = settings.get('business', {}).get('city', 'Jacksonville')

    # Approximate coordinates for major FL cities
    geo_coords = {
        'jacksonville': {'latitude': 30.3322, 'longitude': -81.6557},
        'miami': {'latitude': 25.7617, 'longitude': -80.1918},
        'tampa': {'latitude': 27.9506, 'longitude': -82.4572},
        'orlando': {'latitude': 28.5383, 'longitude': -81.3792},
    }
    coords = geo_coords.get(city.lower(), {'latitude': 30.3322, 'longitude': -81.6557})

    state_file = profile_dir / 'state.json'
    context_opts = {
        'user_agent': ua,
        'viewport': viewport,
        'locale': 'en-US',
        'timezone_id': 'America/New_York',
        'geolocation': coords,
        'permissions': ['geolocation'],
        'storage_state': str(state_file) if state_file.exists() else None,
    }

    if proxy:
        context_opts['proxy'] = proxy

    browser = await playwright.chromium.launch(headless=headless, args=launch_args)
    context = await browser.new_context(**context_opts)

    await context.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        window.chrome = { runtime: {} };
    """)

    return browser, context, 'playwright'


# --- CL Login ---

async def login_to_cl(page, account, metro_url):
    """Log into a Craigslist account."""
    logger.info(f"Logging in as account #{account['id']} ({account['email'][:5]}...)")
    await page.goto(f'{metro_url}/login')
    await page.wait_for_load_state('networkidle')
    await human_delay(1, 2)

    if 'account' in page.url:
        logger.info("Already logged in")
        return True

    await human_type(page, '#inputEmailHandle', account['email'])
    await human_delay(0.5, 1)
    await human_type(page, '#inputPassword', account['password'])
    await human_delay(0.5, 1)

    await random_mouse_movement(page)
    await page.click('#login')
    await page.wait_for_load_state('networkidle')
    await human_delay(2, 4)

    if 'account' in page.url or 'login' not in page.url:
        logger.info("Login successful")
        # Save state
        profile_dir = account.get('profile_dir', PROFILES_DIR / 'default')
        os.makedirs(profile_dir, exist_ok=True)
        storage = await page.context.storage_state()
        with open(profile_dir / 'state.json', 'w') as f:
            json.dump(storage, f)
        return True
    else:
        logger.error("Login failed — may need manual verification or captcha")
        os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
        await page.screenshot(path=str(SCREENSHOTS_DIR / f'login_fail_{account["id"]}_{datetime.now().strftime("%H%M%S")}.png'))
        return False


# --- Ad Posting ---

async def post_ad(page, ad, metro_url, test_mode=False):
    """Post a single ad to Craigslist."""
    category = ad.get('category', 'skilled_trade_services')
    category_text = CL_CATEGORIES.get(category, 'skilled trade services')
    logger.info(f"Posting: {ad['title']} -> {category_text}")

    await page.goto(f'{metro_url}/post')
    await page.wait_for_load_state('networkidle')
    await human_delay(1, 3)

    # Step 1: Choose "service offered"
    try:
        await page.click('input[value="so"]')
        await human_delay(0.5, 1.5)
        await random_mouse_movement(page)
        await page.click('button.pickbutton')
        await page.wait_for_load_state('networkidle')
        await human_delay(1, 2)
    except Exception as e:
        logger.error(f"Failed to select posting type: {e}")
        return None

    # Step 2: Choose category
    try:
        cat_label = page.locator(f'label:has-text("{category_text}")')
        if await cat_label.count() > 0:
            await cat_label.first.click()
        else:
            cat_option = page.locator(f'text={category_text}')
            if await cat_option.count() > 0:
                await cat_option.first.click()
            else:
                logger.warning(f"Category '{category_text}' not found, using first available")
                await page.locator('input[type="radio"]').first.click()

        await human_delay(0.5, 1)
        await page.click('button.pickbutton')
        await page.wait_for_load_state('networkidle')
        await human_delay(1, 2)
    except Exception as e:
        logger.warning(f"Category selection issue: {e}")
        try:
            await page.click('button.pickbutton')
            await page.wait_for_load_state('networkidle')
        except Exception:
            pass

    # Step 3: Fill the form
    try:
        await human_type(page, '#PostingTitle', ad['title'], min_delay=30, max_delay=80)
        await human_delay(0.5, 1)

        city_input = page.locator('#GeographicArea')
        if await city_input.count() > 0:
            settings = load_settings()
            city = settings.get('business', {}).get('city', '')
            await city_input.fill(city)

        postal = page.locator('#postal_code, input[name="postal"]')
        if await postal.count() > 0:
            await postal.fill('32202')

        await human_delay(0.3, 0.8)
        await human_type(page, '#PostingBody', ad['body'], min_delay=20, max_delay=60)
        await human_delay(0.5, 1)

        phone_input = page.locator('input[name="contact_phone"]')
        if await phone_input.count() > 0:
            clean_phone = BUSINESS_PHONE.replace('-', '').replace('+1', '').replace(' ', '')
            await phone_input.fill(clean_phone)

        await random_mouse_movement(page)
        logger.info("Form filled")
    except Exception as e:
        logger.error(f"Form fill failed: {e}")
        os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
        await page.screenshot(path=str(SCREENSHOTS_DIR / f'form_error_{datetime.now().strftime("%H%M%S")}.png'))
        return None

    if test_mode:
        logger.info("TEST MODE — not submitting")
        os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
        screenshot_path = SCREENSHOTS_DIR / f'test_{datetime.now().strftime("%H%M%S")}.png'
        await page.screenshot(path=str(screenshot_path))
        logger.info(f"Screenshot saved: {screenshot_path}")
        return 'test'

    # Step 4: Submit
    try:
        await page.click('button.go')
        await page.wait_for_load_state('networkidle')
        await human_delay(2, 4)

        # Upload images
        images = get_images(ad['images_folder'])
        if images:
            file_input = page.locator('input[type="file"]')
            if await file_input.count() > 0:
                for img_path in images:
                    await file_input.set_input_files(img_path)
                    await human_delay(1, 3)
                logger.info(f"Uploaded {len(images)} images")

        # Done with images
        done_btn = page.locator('button:has-text("done with images")')
        if await done_btn.count() > 0:
            await done_btn.click()
            await page.wait_for_load_state('networkidle')
            await human_delay(2, 3)

        # Final publish
        publish_btn = page.locator('button.go, button:has-text("publish")')
        if await publish_btn.count() > 0:
            await publish_btn.click()
            await page.wait_for_load_state('networkidle')
            await human_delay(3, 5)

        post_url = page.url
        logger.info(f"Ad posted: {post_url}")
        return post_url

    except Exception as e:
        logger.error(f"Submit failed: {e}")
        os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
        await page.screenshot(path=str(SCREENSHOTS_DIR / f'submit_error_{datetime.now().strftime("%H%M%S")}.png'))
        return None


# --- Main Operations ---

async def run_single_post(template_name=None, category=None, test_mode=False):
    """Post a single ad using the next available account."""
    await init_db()
    templates = load_templates()
    settings = load_settings()
    metro_url = get_metro_url()

    todays_ads = await get_todays_ads('craigslist')
    used_today = [f"{row['template_name']}:{row['category']}:{row['title'][:30]}"
                  for row in todays_ads] if todays_ads else []

    max_daily = settings.get('craigslist', {}).get('posts_per_day', 7)
    if len(used_today) >= max_daily and not test_mode:
        logger.info(f"Already posted {len(used_today)}/{max_daily} ads today")
        return

    # Pick template from schedule if not specified
    if not template_name:
        schedule = settings.get('craigslist', {}).get('posting_schedule', [])
        posted_count = len(used_today)
        if posted_count < len(schedule):
            slot = schedule[posted_count]
            template_name = slot['template']
            category = slot.get('category', 'skilled_trade_services')
        else:
            template_name = list(templates.keys())[0] if templates else None
            category = 'skilled_trade_services'

    if not template_name or template_name not in templates:
        logger.error(f"No valid template: {template_name}")
        return

    if not category:
        category = 'skilled_trade_services'

    ad = pick_ad(templates, template_name, category, used_today)
    if not ad:
        logger.error("Failed to generate ad")
        return

    # Pick account with capacity
    used_accounts = {}
    if todays_ads:
        for row in todays_ads:
            # Track posts per account (stored as category prefix in a real impl)
            pass

    account = pick_account(used_accounts) if CL_ACCOUNTS else None

    if not account and not test_mode:
        # No accounts configured — can still test
        logger.warning("No CL accounts configured. Using single-account mode.")
        account = {
            'id': 0,
            'email': os.getenv('CL_ACCOUNT_1_EMAIL', ''),
            'password': os.getenv('CL_ACCOUNT_1_PASSWORD', ''),
            'phone': '',
            'profile_dir': PROFILES_DIR / 'default',
            'gologin_profile_id': '',
            'max_posts_per_day': 7,
        }

    logger.info(f"Selected: {ad['template_name']} -> {CL_CATEGORIES.get(category, category)}")
    if account:
        logger.info(f"Using account #{account['id']}")

    async with async_playwright() as p:
        headless = not test_mode
        browser, context, mode = await create_browser(p, account, headless=headless)
        logger.info(f"Browser mode: {mode}")
        page = await context.new_page()

        try:
            if account and account['email']:
                logged_in = await login_to_cl(page, account, metro_url)
                if not logged_in:
                    logger.error("Login failed — cannot post")
                    return

            result = await post_ad(page, ad, metro_url, test_mode=test_mode)

            if result and result != 'test':
                await log_ad(
                    platform='craigslist',
                    city=settings.get('business', {}).get('city', 'Unknown'),
                    category=category,
                    template_name=ad['template_name'],
                    title=ad['title'],
                    post_url=result,
                    cost=5.0,
                )
                logger.info("Ad logged. Cost: $5.00")
            elif result == 'test':
                logger.info("Test complete. Check screenshots/ folder.")
        finally:
            if mode == 'gologin' and account:
                await stop_gologin_profile(account.get('gologin_profile_id', ''))
            await browser.close()


async def run_all_posts():
    """Post all scheduled ads for today, rotating accounts."""
    await init_db()
    settings = load_settings()
    schedule = settings.get('craigslist', {}).get('posting_schedule', [])

    todays_ads = await get_todays_ads('craigslist')
    posted_count = len(todays_ads) if todays_ads else 0

    remaining = schedule[posted_count:]
    if not remaining:
        logger.info("All scheduled ads for today have been posted.")
        return

    logger.info(f"Posting {len(remaining)} remaining ads for today...")

    for slot in remaining:
        template_name = slot['template']
        category = slot.get('category', 'skilled_trade_services')

        logger.info(f"--- Posting: {template_name} -> {category} ---")
        await run_single_post(template_name=template_name, category=category)

        # Wait between posts (human-like interval)
        wait_time = random.uniform(600, 1800)  # 10-30 minutes
        logger.info(f"Waiting {wait_time/60:.0f} minutes before next post...")
        await asyncio.sleep(wait_time)


async def run_scheduled():
    """Run the full daily posting schedule at configured times."""
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
    from apscheduler.triggers.cron import CronTrigger

    await init_db()
    settings = load_settings()
    schedule = settings.get('craigslist', {}).get('posting_schedule', [])

    logger.info(f"Starting scheduler with {len(schedule)} posting slots")

    scheduler = AsyncIOScheduler()

    for slot in schedule:
        time_str = slot['time']
        template = slot['template']
        category = slot.get('category', 'skilled_trade_services')
        hour, minute = time_str.split(':')

        # Add random offset (0-15 min) to avoid predictable timing
        offset_min = random.randint(0, 15)
        actual_minute = (int(minute) + offset_min) % 60

        scheduler.add_job(
            run_single_post,
            CronTrigger(hour=int(hour), minute=actual_minute),
            kwargs={'template_name': template, 'category': category},
            id=f'cl_{template}_{category}_{time_str}',
            name=f'{time_str}(+{offset_min}m) | {template} -> {category}',
        )
        logger.info(f"  {time_str} (+{offset_min}m) | {template} -> {CL_CATEGORIES.get(category, category)}")

    scheduler.start()
    posts_per_day = len(schedule)
    logger.info(f"Scheduler running. {posts_per_day} posts/day. Cost: ${posts_per_day * 5}/day. Ctrl+C to stop.")

    try:
        while True:
            await asyncio.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logger.info("Scheduler stopped.")


async def show_status():
    """Show posting status and account health."""
    await init_db()
    settings = load_settings()
    todays_ads = await get_todays_ads('craigslist')
    active_ads = await get_active_ads('craigslist')
    max_daily = settings.get('craigslist', {}).get('posts_per_day', 7)

    print("\n=== Craigslist Posting Status ===")
    print(f"Today's posts: {len(todays_ads) if todays_ads else 0}/{max_daily}")
    print(f"Active ads: {len(active_ads) if active_ads else 0}")
    print(f"CL accounts configured: {len(CL_ACCOUNTS)}")
    print(f"GoLogin: {'Connected' if GOLOGIN_TOKEN else 'Not configured'}")
    print(f"Proxy: {'Configured' if PROXY_HOST else 'Not configured'}")

    posting_method = settings.get('craigslist', {}).get('posting_method', '1')
    methods = {'1': 'Craigslist Dominator', '2': 'Fiverr', '3': 'DIY Agent'}
    print(f"Posting method: {methods.get(posting_method, 'Unknown')}")

    if todays_ads:
        print("\nToday's ads:")
        for ad in todays_ads:
            print(f"  [{ad['posted_at'][:16]}] {ad['template_name']}: {ad['title'][:60]}")

    total_cost = sum(ad['cost'] for ad in (todays_ads or []))
    print(f"\nToday's CL fees: ${total_cost:.2f}")

    # Monthly projection
    days_per_week = settings.get('craigslist', {}).get('days_per_week', 3)
    monthly_cost = max_daily * 5 * days_per_week * 4
    print(f"Monthly CL fee estimate: ${monthly_cost}")
    print()


def main():
    parser = argparse.ArgumentParser(description='Craigslist Posting Agent — Home Services Lead Machine')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--test', action='store_true', help='Test one ad (visible browser, no submit)')
    group.add_argument('--post', action='store_true', help='Post next scheduled ad')
    group.add_argument('--post-all', action='store_true', help='Post all remaining ads for today')
    group.add_argument('--schedule', action='store_true', help='Run daily posting schedule')
    group.add_argument('--status', action='store_true', help='Show posting status')
    group.add_argument('--renew', action='store_true', help='Renew ads older than 48 hours')
    args = parser.parse_args()

    if args.test:
        asyncio.run(run_single_post(test_mode=True))
    elif args.post:
        asyncio.run(run_single_post())
    elif args.post_all:
        asyncio.run(run_all_posts())
    elif args.schedule:
        asyncio.run(run_scheduled())
    elif args.status:
        asyncio.run(show_status())
    elif args.renew:
        print("Renewal: re-post ads that are 48+ hours old.")
        print("Coming soon — for now, renew manually on CL or through your posting service.")


if __name__ == '__main__':
    main()
