#!/usr/bin/env python3
"""
Home Services Lead Machine — Setup Wizard

Run this to configure your business. It asks simple questions
and writes all config files so the automation is ready to go.

Usage:
    python setup/wizard.py              # Full interactive setup
    python setup/wizard.py --check      # Check if setup is complete
    python setup/wizard.py --reset      # Reset config to defaults
"""
import os
import sys
import yaml
import shutil
from pathlib import Path

ROOT = Path(__file__).parent.parent
AUTOMATION = ROOT / 'automation'
ENV_FILE = AUTOMATION / '.env'
ENV_EXAMPLE = AUTOMATION / '.env.example'
SETTINGS_FILE = AUTOMATION / 'config' / 'settings.yaml'
TEMPLATES_FILE = AUTOMATION / 'craigslist' / 'ad_templates' / 'templates.yaml'


def ask(question, default=None, required=True):
    """Ask a question and return the answer."""
    suffix = f" [{default}]" if default else ""
    while True:
        answer = input(f"\n{question}{suffix}\n> ").strip()
        if not answer and default:
            return default
        if answer or not required:
            return answer
        print("  Please provide an answer.")


def ask_list(question, example=None):
    """Ask for a comma-separated list."""
    hint = f" (example: {example})" if example else ""
    answer = ask(f"{question}{hint}")
    return [item.strip() for item in answer.split(',') if item.strip()]


def ask_yes_no(question, default='y'):
    """Ask a yes/no question."""
    answer = ask(f"{question} (y/n)", default=default, required=False)
    return answer.lower() in ('y', 'yes', '')


def banner(text):
    """Print a section banner."""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}")


def collect_business_info():
    """Phase 1: Collect business information."""
    banner("STEP 1: YOUR BUSINESS INFO")
    print("\nI'm going to ask a few questions about your business.")
    print("This takes about 2 minutes.\n")

    info = {}
    info['business_name'] = ask("What's your business name?",
                                 default="My Handyman Services")

    info['city'] = ask("What city are you in?",
                       default="Jacksonville")

    info['state'] = ask("What state?", default="FL")

    info['services'] = ask_list(
        "What services do you offer? (comma separated)",
        example="handyman work, roof repair, wildlife removal, property maintenance"
    )

    info['service_area'] = ask_list(
        "What cities/areas do you serve? (comma separated)",
        example="Jacksonville, Orange Park, Ponte Vedra, St. Augustine"
    )

    info['owner_name'] = ask("What's your name? (name customers will see)")

    info['personal_phone'] = ask("What's your cell phone number? (calls forward here)")

    print("\n--- Pricing ---")
    info['pricing'] = {}
    for service in info['services']:
        price_range = ask(f"Price range for {service}?",
                          default="$150-$500 per job")
        info['pricing'][service] = price_range

    info['has_photos'] = ask_yes_no("Do you have business photos ready?", default='n')

    return info


def collect_tracking_info():
    """Phase 2: Tracking number setup."""
    banner("STEP 2: CALL TRACKING NUMBER")
    print("""
You need a phone number for your ads that:
  - Forwards calls to your cell phone
  - Records every call
  - Tells you which ad generated each lead

RECOMMENDED: AvidTrak ($15/mo, 14-day free trial)
  - Sign up at: avidtrak.com
  - Get a local number in your area code
  - Set it to forward to your cell
  - Enable call recording

OTHER OPTIONS:
  - CallScaler ($29/mo) — cheap per-number pricing
  - CallRail ($45/mo) — industry standard
  - Google Voice (free) — no recording, no tracking (not recommended)
""")

    tracking = {}
    has_tracking = ask_yes_no("Do you already have a tracking number set up?", default='n')

    if has_tracking:
        tracking['number'] = ask("What's your tracking number?")
        tracking['provider'] = ask("Which provider? (avidtrak/callscaler/callrail/google-voice/other)",
                                   default="avidtrak")
    else:
        print("\nNo problem. Here's what to do:")
        print("  1. Go to avidtrak.com")
        print("  2. Start the 14-day free trial (no credit card needed)")
        print("  3. Get a local number in your area code")
        print("  4. Set it to forward to your cell phone")
        print("  5. Enable call recording")
        print("  6. Come back here and run this setup again with your number")
        print("")
        proceed = ask_yes_no("Want to continue setup without a tracking number for now?")
        if proceed:
            tracking['number'] = ask("Enter your personal phone number (we'll use this until you get tracking)",
                                     required=True)
            tracking['provider'] = 'pending'
        else:
            print("\nGo set up AvidTrak, then come back. Run: python setup/wizard.py")
            sys.exit(0)

    return tracking


def collect_craigslist_info():
    """Phase 3: Craigslist preferences."""
    banner("STEP 3: CRAIGSLIST ADS")
    print("""
Craigslist is your fastest path to leads.
Each ad costs $5. We'll set up 4-7 ads across your services.
""")

    cl = {}
    cl['posts_per_day'] = int(ask("How many CL ads per day? (4-7 recommended)", default="7"))
    cl['days_per_week'] = int(ask("How many days per week? (3 = $420/mo, 5 = $700/mo)", default="3"))

    print("""
How do you want to post?
  1. Craigslist Dominator ($10/ad — they handle everything)
  2. Fiverr freelancer ($6-7/ad — you send them the ad copy)
  3. DIY posting agent (just $5 CL fee — requires proxy + anti-detect browser setup)
""")
    cl['posting_method'] = ask("Pick 1, 2, or 3", default="1")

    if cl['posting_method'] == '3':
        cl['proxy_provider'] = ask(
            "Proxy provider? (brightdata/oxylabs/decodo/smartproxy/none-yet)",
            default="none-yet"
        )
        cl['antidetect_browser'] = ask(
            "Anti-detect browser? (gologin/adspower/multilogin/none-yet)",
            default="none-yet"
        )
        cl['num_accounts'] = int(ask("How many CL accounts do you have? (need 2-3 for 7 ads/day)",
                                      default="0"))

    return cl


def write_env(business, tracking, craigslist):
    """Write the .env file from collected info."""
    lines = [
        "# Home Services Lead Machine — Configuration",
        "# Generated by setup wizard",
        "",
        "# Business Info",
        f"BUSINESS_NAME={business['business_name']}",
        f"OWNER_NAME={business['owner_name']}",
        f"BUSINESS_CITY={business['city']}",
        f"BUSINESS_STATE={business['state']}",
        f"SERVICE_AREA={', '.join(business['service_area'])}",
        "",
        "# Phone Numbers",
        f"TRACKING_PHONE={tracking['number']}",
        f"TRACKING_PROVIDER={tracking.get('provider', 'pending')}",
        f"PERSONAL_PHONE={business['personal_phone']}",
        "",
    ]

    # CL accounts (if DIY method)
    if craigslist.get('posting_method') == '3':
        lines.extend([
            "# Craigslist Accounts",
            "CL_ACCOUNT_1_EMAIL=",
            "CL_ACCOUNT_1_PASSWORD=",
            "CL_ACCOUNT_1_PHONE=",
            "",
            "CL_ACCOUNT_2_EMAIL=",
            "CL_ACCOUNT_2_PASSWORD=",
            "CL_ACCOUNT_2_PHONE=",
            "",
            "CL_ACCOUNT_3_EMAIL=",
            "CL_ACCOUNT_3_PASSWORD=",
            "CL_ACCOUNT_3_PHONE=",
            "",
        ])

        # Proxy config
        provider = craigslist.get('proxy_provider', 'none-yet')
        lines.extend([
            f"# Proxy ({provider})",
            "PROXY_HOST=",
            "PROXY_PORT=",
            "PROXY_USER=",
            "PROXY_PASS=",
            "",
        ])

        # GoLogin
        lines.extend([
            f"# Anti-detect browser ({craigslist.get('antidetect_browser', 'none-yet')})",
            "GOLOGIN_API_TOKEN=",
            "",
        ])

    # Facebook
    lines.extend([
        "# Facebook (for inbox monitor — optional)",
        "FB_EMAIL=",
        "FB_PASSWORD=",
    ])

    ENV_FILE.parent.mkdir(parents=True, exist_ok=True)
    ENV_FILE.write_text('\n'.join(lines) + '\n')
    print(f"\n  Config written to: {ENV_FILE}")


def write_settings(business, tracking, craigslist):
    """Write settings.yaml from collected info."""
    metro_url = f"https://{business['city'].lower().replace(' ', '')}.craigslist.org"

    # Build posting schedule
    schedule = []
    times = ["07:00", "08:30", "10:00", "11:30", "13:00", "14:30", "16:00"]
    services = business['services']

    slot_idx = 0
    for service in services:
        service_key = service.lower().replace(' ', '_').replace('/', '_')
        # Two categories per service (except last service gets one if we'd exceed 7)
        for cat in ['skilled_trade_services', 'household_services']:
            if slot_idx >= min(craigslist['posts_per_day'], 7):
                break
            schedule.append({
                'time': times[slot_idx % len(times)],
                'template': service_key,
                'category': cat,
            })
            slot_idx += 1
        if slot_idx >= min(craigslist['posts_per_day'], 7):
            break

    settings = {
        'business': {
            'name': business['business_name'],
            'owner': business['owner_name'],
            'phone': tracking['number'],
            'personal_phone': business['personal_phone'],
            'city': business['city'],
            'state': business['state'],
            'email': '',
            'booking_url': '',
            'service_area': business['service_area'],
            'services': business['services'],
            'pricing': business['pricing'],
        },
        'craigslist': {
            'metro_url': metro_url,
            'posts_per_day': craigslist['posts_per_day'],
            'days_per_week': craigslist['days_per_week'],
            'posting_method': craigslist['posting_method'],
            'renewal_hours': 48,
            'posting_schedule': schedule,
            'max_post_age_days': 14,
            'require_unique_images': True,
        },
        'facebook': {
            'check_interval_minutes': 5,
            'auto_respond': True,
            'max_auto_responses': 3,
            'active_hours': {'start': '07:00', 'end': '21:00'},
            'posts_per_week': 14,
        },
        'tracking': {
            'provider': tracking.get('provider', 'pending'),
            'number': tracking['number'],
            'database': 'sqlite:///data/leads.db',
            'export_csv': True,
            'export_path': './data/leads_export.csv',
        },
        'safety': {
            'kill_switch': False,
            'max_daily_posts': 15,
            'max_daily_responses': 50,
            'min_action_delay': 30,
            'max_action_delay': 120,
        },
    }

    SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(SETTINGS_FILE, 'w') as f:
        yaml.dump(settings, f, default_flow_style=False, sort_keys=False)
    print(f"  Settings written to: {SETTINGS_FILE}")


def generate_ad_templates(business, tracking):
    """Generate customized CL ad templates from business info."""
    city = business['city']
    state = business['state']
    phone = tracking['number']
    area = ', '.join(business['service_area'][:5])
    biz_name = business['business_name']

    templates = {}

    for service in business['services']:
        key = service.lower().replace(' ', '_').replace('/', '_')
        templates[key] = {
            'categories': ['skilled_trade_services', 'household_services'],
            'titles': [
                f"{service.title()} -- Fast & Affordable -- {city} {state}",
                f"{service.title()} -- Licensed & Insured -- {city} Area",
                f"Need {service.title()}? Same Day Available -- {city} {state}",
            ],
            'bodies': [
                (
                    f"Looking for reliable {service.lower()}? {biz_name} is here to help.\n\n"
                    f"We offer professional {service.lower()} services across {area}.\n\n"
                    f"Licensed. Insured. Honest pricing.\n\n"
                    f"FREE estimates -- call or text today: {{phone}}\n\n"
                    f"Serving: {area}"
                ),
                (
                    f"Don't wait on {service.lower()} -- we respond fast and get it done right.\n\n"
                    f"WHAT WE OFFER:\n"
                    f"* Professional {service.lower()}\n"
                    f"* Same-day and next-day scheduling\n"
                    f"* Honest, upfront pricing\n"
                    f"* Licensed and insured\n\n"
                    f"Call or text for a FREE quote: {{phone}}\n\n"
                    f"We serve all of {city} and surrounding areas."
                ),
                (
                    f"Need {service.lower()}? We've been serving {city} for years.\n\n"
                    f"Fast response. Fair pricing. Quality work guaranteed.\n\n"
                    f"* Free estimates\n"
                    f"* Same-day service available\n"
                    f"* Licensed & insured\n\n"
                    f"{{phone}} -- Call or text anytime.\n\n"
                    f"Service area: {area}"
                ),
            ],
            'images_folder': key,
        }

    data = {
        'templates': templates,
    }

    TEMPLATES_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TEMPLATES_FILE, 'w') as f:
        f.write(f"# Ad Templates for {biz_name} — {city}, {state}\n")
        f.write(f"# Generated by setup wizard\n")
        f.write(f"# Phone placeholder {{phone}} is replaced with: {phone}\n\n")
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    print(f"  Ad templates written to: {TEMPLATES_FILE}")
    print(f"  Generated {len(templates)} service templates with 3 title + 3 body variants each")


def create_directories():
    """Create all needed directories."""
    dirs = [
        AUTOMATION / 'data',
        AUTOMATION / 'logs',
        AUTOMATION / 'profiles' / 'craigslist',
        AUTOMATION / 'profiles' / 'facebook',
        AUTOMATION / 'screenshots',
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
    # Create image dirs per service
    images_dir = AUTOMATION / 'craigslist' / 'ad_templates' / 'images'
    images_dir.mkdir(parents=True, exist_ok=True)


def check_setup():
    """Check if setup is complete."""
    banner("SETUP CHECK")
    checks = {
        '.env file exists': ENV_FILE.exists(),
        'settings.yaml exists': SETTINGS_FILE.exists(),
        'templates.yaml exists': TEMPLATES_FILE.exists(),
        'data directory exists': (AUTOMATION / 'data').exists(),
    }

    if ENV_FILE.exists():
        env_content = ENV_FILE.read_text()
        checks['Tracking number configured'] = 'TRACKING_PHONE=' in env_content and \
            not env_content.split('TRACKING_PHONE=')[1].split('\n')[0].strip() == ''
        checks['Business name configured'] = 'BUSINESS_NAME=' in env_content and \
            not env_content.split('BUSINESS_NAME=')[1].split('\n')[0].strip() == ''

    all_good = True
    for check, passed in checks.items():
        status = "PASS" if passed else "FAIL"
        print(f"  [{status}] {check}")
        if not passed:
            all_good = False

    if all_good:
        print("\n  All checks passed. You're ready to go.")
        print("  Next: Post your ads or run 'python automation/craigslist/poster.py --test'")
    else:
        print("\n  Some checks failed. Run 'python setup/wizard.py' to fix.")

    return all_good


def show_summary(business, tracking, craigslist):
    """Show setup summary."""
    banner("SETUP COMPLETE")
    print(f"""
  Business:        {business['business_name']}
  Owner:           {business['owner_name']}
  City:            {business['city']}, {business['state']}
  Services:        {', '.join(business['services'])}
  Service area:    {', '.join(business['service_area'][:3])}...
  Tracking phone:  {tracking['number']}
  CL ads/day:      {craigslist['posts_per_day']}
  CL days/week:    {craigslist['days_per_week']}
  Posting method:  {'Dominator' if craigslist['posting_method'] == '1' else 'Fiverr' if craigslist['posting_method'] == '2' else 'DIY Agent'}

  Estimated monthly CL cost: ${craigslist['posts_per_day'] * 5 * craigslist['days_per_week'] * 4}

  Files created:
    - automation/.env
    - automation/config/settings.yaml
    - automation/craigslist/ad_templates/templates.yaml

  NEXT STEPS:
  1. {'Set up AvidTrak tracking number (avidtrak.com)' if tracking.get('provider') == 'pending' else 'Tracking number is set up'}
  2. Post your Craigslist ads (see LAUNCH-CHECKLIST.md)
  3. Post Facebook Marketplace listings (see lead-gen/FB-MARKETPLACE-WORKAROUNDS.md)
  4. Set up Google Business Profile (business.google.com)
  5. Follow the daily routine in LAUNCH-CHECKLIST.md
""")


def main():
    if len(sys.argv) > 1:
        if '--check' in sys.argv:
            check_setup()
            return
        if '--reset' in sys.argv:
            if ENV_FILE.exists():
                ENV_FILE.unlink()
            print("Config reset. Run 'python setup/wizard.py' to set up again.")
            return

    banner("HOME SERVICES LEAD MACHINE — SETUP")
    print("""
  This wizard will set up your lead generation system.
  It takes about 5 minutes. I'll ask simple questions,
  you answer, and I'll configure everything.

  Let's go.
""")

    # Collect info
    business = collect_business_info()
    tracking = collect_tracking_info()
    craigslist = collect_craigslist_info()

    # Confirm
    banner("CONFIRM YOUR INFO")
    print(f"""
  Business:     {business['business_name']}
  City:         {business['city']}, {business['state']}
  Services:     {', '.join(business['services'])}
  Area:         {', '.join(business['service_area'][:3])}...
  Phone:        {tracking['number']}
  CL ads/day:   {craigslist['posts_per_day']}
""")

    if not ask_yes_no("Does this look right?"):
        print("\nRun the wizard again to start over.")
        sys.exit(0)

    # Write everything
    banner("WRITING CONFIG FILES")
    create_directories()
    write_env(business, tracking, craigslist)
    write_settings(business, tracking, craigslist)
    generate_ad_templates(business, tracking)

    # Show summary
    show_summary(business, tracking, craigslist)


if __name__ == '__main__':
    main()
