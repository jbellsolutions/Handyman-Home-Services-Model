# Facebook Marketplace Automation Research
## Browser Automation Tools for Home Services Ad Posting & Auto-Responding

**Research Date:** March 25, 2026
**Purpose:** Evaluate tools for automating Facebook Marketplace listing creation and inquiry responses for a handyman/home services business.

---

## Table of Contents

1. [Airtop (airtop.ai)](#1-airtop-airtopai)
2. [Browser Use (browser-use.com)](#2-browser-use-browser-usecom)
3. [Other Browser Automation Options](#3-other-browser-automation-options)
4. [Facebook Marketplace Specifics](#4-facebook-marketplace-specifics)
5. [The Auto-Response System](#5-the-auto-response-system)
6. [Existing FB Marketplace Bots (Turnkey Solutions)](#6-existing-fb-marketplace-bots-turnkey-solutions)
7. [Practical Recommendation](#7-practical-recommendation)
8. [Cost Comparison Table](#8-cost-comparison-table)
9. [Risk Assessment](#9-risk-assessment)

---

## 1. Airtop (airtop.ai)

### What It Is

Airtop is a cloud browser automation platform that runs secure, always-on cloud browsers with built-in proxies. It allows AI agents and developers to automate web tasks using either natural language commands or traditional automation scripts (Playwright, Puppeteer, Selenium). It compiles natural language instructions into deterministic workflows and provides video replay of every action for debugging.

### Key Capabilities

- **Cloud browsers** that run 24/7 without needing a local machine
- **Natural language control** -- describe what you want in plain English and it executes
- **Full Playwright/Puppeteer/Selenium support** for scripted automation
- **Built-in proxies** to rotate IP addresses
- **OAuth, 2FA, and CAPTCHA handling** built into the platform
- **SOC 2 Type II certified** and HIPAA compliant
- **Session persistence** -- can save and restore browser state (cookies, localStorage) across runs

### Can It Stay Logged Into Facebook Persistently?

Partially. Airtop supports session profiles that save browser state (cookies, cache, localStorage). You log in once manually, and subsequent sessions start already authenticated. However:

- Facebook cookies expire, so sessions need refreshing approximately every 7 days
- Facebook may invalidate sessions if it detects unusual patterns (new IP, new browser fingerprint)
- Airtop's built-in proxies help but are not specifically designed for Facebook anti-detection
- There is no guarantee of uninterrupted Facebook login persistence

### Pricing Model

Credit-based billing:

| Plan | Monthly Cost | Credits Included |
|------|-------------|-----------------|
| Free | $0 | 1,000 credits |
| Starter | $26/mo | Limited credits |
| Professional | $80/mo | More credits |
| Enterprise | $342/mo | 500,000+ credits |

**Problem:** Credit consumption rates are not transparently documented. Running a browser session every 5 minutes, 24/7 would consume a significant number of credits. The Professional plan ($80/mo) is likely the minimum for this use case, but cost predictability is poor.

### Facebook Anti-Bot Detection Handling

Airtop claims to handle CAPTCHAs and complex authentication. However, Facebook's detection goes beyond CAPTCHAs -- it analyzes behavioral patterns, mouse movements, typing speed, and session consistency. Airtop's cloud browsers may trigger Facebook's "unusual login" detection more frequently than anti-detect browsers specifically designed for social media.

### Running 24/7 Checks Every 5 Minutes

Airtop's cloud infrastructure supports this architecturally. You would:
1. Create a scheduled job (cron or external scheduler)
2. Each run: start a session, load saved profile, check messages, respond, save profile, end session
3. The session start/stop overhead adds latency (15-30 seconds per cycle)

Alternatively, keep a single session alive continuously, but this is more expensive and riskier for detection.

### SDK Integration

- **Python SDK:** `pip install airtop` -- both sync and async clients
- **Node.js/TypeScript SDK:** `npm install @airtop-ai/sdk`
- **REST API** available for any language
- **No-code:** Integrations with Make and n8n

### FB Marketplace Automation Examples

No publicly documented examples of FB Marketplace automation with Airtop. The platform is positioned more for sales/marketing workflows (LinkedIn scraping, lead enrichment) than social media marketplace automation.

---

## 2. Browser Use (browser-use.com)

### What It Is

Browser Use is an open-source Python library (21,000+ GitHub stars) that connects AI agents directly to web browsers. It enables autonomous navigation, interaction, and data extraction using LLM providers (OpenAI, Google, local models via Ollama). It also has a cloud offering (Browser Use Cloud) with stealth browsers and managed infrastructure.

### Key Capabilities

- **Open-source core** -- free self-hosted option
- **AI-driven automation** using natural language task descriptions
- **Stealth browsers** (cloud version) designed to avoid detection and CAPTCHA challenges
- **3-5x faster** task completion than competing models
- **State-of-the-art accuracy** on web automation benchmarks
- **Supports all major LLM providers** as the "brain"

### Can It Handle Facebook Login and Stay Authenticated?

Yes, with configuration:

- **Local profile reuse:** Use `user_data_dir` and `profile_directory` to point at your real Chrome profile, preserving existing cookies without re-authentication
- **Storage state files:** Pass a Playwright storage state file (cookies + localStorage) for a clean profile that retains login
- **`keep_alive=True`:** Keeps the browser open across multiple tasks without losing session state
- **Cloud profiles:** Browser Use Cloud supports persistent profiles that save state when sessions end

**Important caveats:**
- Must call `sessions.stop()` properly or state may not persist
- Refresh profiles older than 7 days to keep login state fresh
- Facebook may still invalidate sessions based on behavioral analysis

### Pricing

**Open-source (self-hosted):** Free, but you pay for LLM API calls and your own infrastructure.

**Browser Use Cloud:**

| Component | Cost |
|-----------|------|
| Task initialization | $0.01 per task |
| Browser sessions | Billed based on timeout duration with proportional refunds |
| LLM costs | 1.2x markup over raw provider costs |
| Max session length | 4 hours (240 minutes) |

- Browser Use 2.0 model is 15x cheaper and 6x faster than frontier models (~3s/step vs ~8s/step)
- Business/Scaleup subscribers get 50% off browser session costs

**For 5-minute checks, 24/7:** ~288 task initializations/day = $2.88/day in init fees alone, plus session and LLM costs. Estimated $100-200/month on cloud.

### Comparison to Airtop for Persistent Sessions

| Feature | Airtop | Browser Use |
|---------|--------|-------------|
| Session persistence | Profile-based, cloud-managed | Local profile or cloud profiles |
| Self-hosted option | No | Yes (open-source) |
| Stealth/anti-detection | Basic (proxies) | Dedicated stealth browsers (cloud) |
| Pricing transparency | Poor (credit-based) | Better (per-task + per-minute) |
| Facebook-specific features | None | None |
| Learning curve | Lower (natural language + scripts) | Higher (Python required) |

### Scheduled 5-Minute Checks

Self-hosted: Use a cron job or Python scheduler (APScheduler) to trigger Browser Use every 5 minutes. The browser can stay alive between checks using `keep_alive=True`.

Cloud: Each check is a separate task invocation. The 4-hour session limit means you cannot keep a single session running indefinitely.

### Python SDK

Fully Python-native. Install with `pip install browser-use`. Supports async/await patterns. Well-documented with examples on GitHub.

---

## 3. Other Browser Automation Options

### 3a. Playwright with Stealth Plugins + Anti-Detect Browser

**Playwright + Patchright (undetected Playwright fork):**
- Patchright is currently considered the most undetectable Playwright variant
- Adds `--disable-blink-features=AutomationControlled` and removes `--enable-automation`
- Free and open-source
- Requires Python or Node.js knowledge
- No built-in session management -- you handle cookies/profiles manually

**Anti-detect browsers (for fingerprint management):**

| Browser | Starting Price | Key Feature for FB |
|---------|---------------|-------------------|
| GoLogin | Free (3 profiles) | Simple, good for beginners. No built-in automation. |
| Dolphin Anty | Free (10 profiles) | Built-in "Scenarios" for automation sequences. Facebook-oriented tools. |
| AdsPower | Free (5 profiles) | Built-in RPA mode for automation. Dual-engine (Chromium + Firefox). |
| MultiLogin | EUR 29/mo (10 profiles) | Most mature. Full API access. Selenium/Playwright/Puppeteer support. |

**Best combo for FB Marketplace:** MultiLogin (EUR 51/mo Solo plan) + Playwright/Patchright scripts. MultiLogin handles fingerprinting and IP rotation; Patchright handles the automation logic.

### 3b. Selenium with Undetected-Chromedriver

- `undetected-chromedriver` patches Chrome to avoid detection
- Unofficial, often breaks with Chrome updates
- Less reliable than Patchright for modern detection systems
- Suitable for quick prototyping but not recommended for production Facebook automation

### 3c. AgentQL

- A query language and toolkit for making web content AI-readable
- More of a component than a full automation framework
- Useful for extracting structured data from pages but not a standalone FB automation solution
- Would need to be combined with Playwright or another browser driver

### 3d. Skyvern

- AI-powered browser automation using LLMs and computer vision
- No custom code needed per website -- works on sites never seen before
- 85.8% accuracy on WebVoyager benchmark (best for form-filling)
- Open-source with cloud offering

**Pricing:**
| Plan | Cost | Credits |
|------|------|---------|
| Free | $0 | 1,000 credits |
| Hobby | Paid | 30,000 credits/mo |
| Pro | Paid | 150,000 credits/mo |
| Enterprise | Custom | Unlimited |

Steps cost $0.05 each (reduced from $0.10 in Sept 2025).

**For FB Marketplace:** Overkill for a repetitive check-and-respond workflow. Better suited for one-off complex form filling across varied websites.

### 3e. MultiLogin Browser

See section 3a above. MultiLogin is specifically designed for managing multiple browser fingerprints and is widely used in the Facebook advertising and marketplace community. At EUR 51/mo (Solo plan), it provides:

- Advanced fingerprint spoofing
- Built-in premium proxies
- Full API access for Selenium/Playwright/Puppeteer
- Persistent profiles that maintain Facebook login across sessions

---

## 4. Facebook Marketplace Specifics

### Can You Post SERVICES on FB Marketplace?

**No. Facebook Marketplace officially does NOT support services.** It is designed exclusively for physical items, vehicles, and property rentals. Facebook's Commerce Policies explicitly prohibit:

- Home repairs
- Childcare
- Personal training
- Any service-based listing

**Enforcement:** Posts violating this are flagged and removed by a combination of automated tools and human reviewers. Repeated violations result in loss of Marketplace posting privileges, and potentially account restriction.

### Workarounds Contractors Actually Use

1. **Post as an "item" with service description:** List a "Handyman Service Package" for $1 with a description of services offered. This works temporarily but gets flagged quickly -- sometimes within minutes.

2. **Post tools/materials with service mention:** List "Professional Paint Job - Includes All Materials" as if selling materials. Slightly longer lifespan but still violates ToS.

3. **Facebook Groups instead of Marketplace:** Join local buy/sell/trade groups and community groups. Post service offers there. This is the LEGITIMATE approach and is far more sustainable.

4. **Facebook Business Page + Paid Ads:** Create a business page and run paid Marketplace ads. This is Facebook's intended path for services and costs money but does not risk account bans.

5. **Respond to "ISO" (In Search Of) posts:** Monitor Marketplace and groups for people seeking handyman help, then respond to those posts. Lower volume but zero ban risk.

### Handling FB's Automated Responses / Message Requests

Facebook Marketplace has a built-in "quick reply" system where buyers tap pre-made messages like "Is this still available?" These arrive as Messenger messages and can be answered through:

- **Meta Business Suite Inbox Automations:** Official feature for business pages. Supports auto-replies, away messages, and FAQ responses. Free but limited customization.
- **Third-party Chrome extensions:** FB Auto Reply AI, AutoResponder.ai, etc. (see Section 6)
- **Custom automation:** Using Browser Use, Playwright, etc. to monitor and respond

### Rate Limits on Responding to Messages

Facebook does not publicly disclose exact limits. Based on community reports:

- **New/young accounts:** May hit limits after 10-15 messages
- **Aged accounts (1+ year):** Higher limits but still throttled with rapid-fire messaging
- **Restrictions last:** 24 hours to 1 week
- **Triggers:** Sending many messages in a short period, repetitive/identical message content, messaging people you have no prior connection with
- **Safe threshold (estimated):** 20-30 unique responses per day for aged accounts, spaced out over time

### Risk of Account Ban

**Risk level: HIGH for automated posting. MODERATE for automated responding.**

- Meta has increased automation-related enforcement by ~25% recently
- Detection signals: unusual API call patterns, credential sharing, rapid repetitive actions, consistent timing intervals (e.g., exactly every 5 minutes)
- Auto-listing bots get accounts banned quickly
- Auto-responding carries less risk because you are replying to inbound messages (expected behavior)
- Using an anti-detect browser + residential proxies + randomized timing reduces risk significantly

### Best Practices to Avoid Detection

1. **Randomize timing:** Do not check exactly every 5 minutes. Use 4-7 minute random intervals.
2. **Vary response templates:** Use 5-10 template variations, not one identical message.
3. **Mimic human behavior:** Add random delays between actions (2-8 seconds), simulate mouse movements, vary scroll patterns.
4. **Use residential proxies:** Datacenter IPs are instantly flagged. Use residential IPs in your local area.
5. **Warm up accounts:** Do not start automating a new account. Use accounts with 6+ months of normal activity.
6. **Limit daily actions:** Stay under 30 responses/day and 5 listings/day.
7. **Use anti-detect browser profiles:** Unique fingerprints per account.
8. **Do not automate posting services directly:** Focus automation on responding to inquiries, not creating listings (which get flagged anyway).

---

## 5. The Auto-Response System

### Architecture for 5-Minute Message Checks

```
[Scheduler (cron/APScheduler)]
        |
        v
[Browser Automation Layer]
  - Load persistent browser profile (cookies/session)
  - Navigate to FB Messenger / Marketplace inbox
  - Scrape new unread messages
  - Compare against "already responded" database
        |
        v
[Response Logic Layer]
  - Classify inquiry type (pricing, availability, booking, complex)
  - Select appropriate template + personalize
  - If complex: flag for human handoff
        |
        v
[Action Layer]
  - Type and send response via browser automation
  - Log message in database (message ID, timestamp, response sent)
  - Update "already responded" database
        |
        v
[Notification Layer]
  - If human handoff needed: send alert (SMS/email/Slack)
  - Daily summary of inquiries handled
```

### Detecting New vs Already-Responded Inquiries

**Method 1 -- Unread indicator:** Facebook marks unread messages with a visual indicator. Scrape the inbox, identify conversations with unread badges.

**Method 2 -- Message timestamp tracking:** Store the timestamp of the last checked message per conversation. On each check, only process messages newer than the stored timestamp.

**Method 3 -- Database tracking:** Maintain a local SQLite or JSON database:
- Key: conversation ID (extracted from Messenger URL or DOM)
- Value: last message timestamp, last response timestamp, status (active/handed-off/closed)

**Recommended:** Combine Methods 1 and 2. Use unread indicators as the primary signal, with timestamp tracking as backup to prevent duplicate responses.

### Template Responses for Booking Quotes

**Initial inquiry response (rotate among 5+ variations):**

> Hi [Name]! Thanks for reaching out. I offer [service category] services in the [city] area. To give you an accurate quote, could you share:
> 1. What specifically needs to be done?
> 2. Your zip code
> 3. Any time preferences?
> I usually respond with a quote within a few hours.

**Follow-up with pricing:**

> Based on what you described, here is a rough estimate:
> [Service]: $[range]
> This includes [details]. I can come take a look for a more precise quote -- what days work best for you this week?

**Booking confirmation:**

> Great! I have you down for [day] at [time]. I will send a reminder the day before. My number is [phone] if you need to reach me directly. Looking forward to helping out!

### Integration with Calendar/Booking System

**Option A -- Google Calendar API:**
- When a booking is confirmed, create a calendar event via Google Calendar API
- Check calendar availability before suggesting times
- Send automated reminders via the calendar

**Option B -- Calendly/Cal.com link:**
- Include a booking link in the auto-response
- "You can pick a time that works for you here: [calendly link]"
- Eliminates back-and-forth scheduling
- Cal.com is free and open-source

**Option C -- Google Sheets as simple CRM:**
- Log every inquiry: name, service needed, date, status, quote amount
- Use Google Sheets API to write rows automatically
- Simple but effective for a small operation

### Human Handoff Triggers

Flag for human intervention when:
1. **Price negotiation:** Customer pushes back on quote
2. **Complex job description:** More than 3 services mentioned or ambiguous scope
3. **Urgency signals:** "emergency," "ASAP," "water leak," "broken pipe"
4. **Complaint or dissatisfaction:** Negative sentiment detected
5. **Repeated back-and-forth:** More than 3 exchanges without booking
6. **Out-of-scope request:** Services you do not offer

Handoff method: Send a push notification (via Pushover, Slack, or SMS via Twilio) with conversation summary and a direct link to the Messenger conversation.

---

## 6. Existing FB Marketplace Bots (Turnkey Solutions)

Before building a custom system, consider these existing tools:

### FB Auto Reply AI (Chrome Extension)

- **What:** Chrome extension that auto-replies to Marketplace messages using AI
- **Rating:** 4.7-4.8 stars on Chrome Web Store
- **Features:** Sub-minute reply times, per-listing message customization, CRM integration (HubSpot, GoHighLevel, Google Sheets), niche modes for real estate/auto/flippers
- **Limitation:** Requires Chrome to be running on your computer 24/7. Not truly cloud-based.
- **Pricing:** Subscription-based (exact pricing not publicly listed, appears to be $20-50/mo range)
- **Best for:** Sellers who keep a computer running and want plug-and-play auto-responses

### AutoResponder.ai (Mobile App)

- **What:** Android/iOS app that auto-responds to Messenger messages
- **Features:** Custom rules, multiple response templates, works with Marketplace messages
- **Limitation:** Runs on your phone. Battery and connectivity dependent.
- **Pricing:** Free tier available, premium ~$5-10/mo

### MarketWiz AI

- **What:** AI platform for cross-platform marketplace automation (FB Marketplace, OfferUp, Craigslist)
- **Features:** Auto-listing, auto-responding, AI replies tagged by urgency, real-time notifications, scheduling, cross-posting
- **Pricing:** 14-day free trial, then subscription (pricing not publicly listed)
- **Best for:** High-volume sellers managing multiple platforms

### FBVerse Bot / AKVerse Bot

- **What:** Desktop software for FB Marketplace auto-listing
- **Features:** C++ core, up to 10 concurrent browsers, proxy support, anti-detection, auto-renew/relist, vehicle and property data mapping
- **Risk level:** HIGH -- these are clearly ToS-violating tools. Account bans are common.
- **Best for:** High-volume product flippers willing to burn accounts. NOT recommended for a legitimate service business.

---

## 7. Practical Recommendation

### For a Handyman/Home Services Business

**The honest answer: Do NOT automate FB Marketplace posting for services.** Facebook Marketplace does not support service listings, and automated posting of fake "item" listings will get your account banned. The risk-reward ratio is terrible for a legitimate business.

### What TO Do Instead (Recommended Strategy)

**Tier 1 -- Legitimate Facebook Presence (Zero Ban Risk):**

1. **Create a Facebook Business Page** for your handyman service
2. **Run paid Marketplace ads** ($5-15/day) targeting your service area. This is Facebook's intended mechanism for services.
3. **Join 10-20 local Facebook Groups** (buy/sell/trade, community, neighborhood groups) and post service offers manually 2-3 times per week
4. **Set up Meta Business Suite auto-replies** for your business page (free, official feature)

**Tier 2 -- Automate Responses Only (Low-Moderate Risk):**

If you are getting enough inbound Marketplace messages (from paid ads or group posts) and want to automate responses:

1. **FB Auto Reply AI Chrome Extension** (~$30/mo) -- simplest option. Runs in Chrome on your computer. AI-powered responses. CRM integration.
2. **Keep a dedicated laptop running 24/7** with Chrome open to Facebook
3. Use the extension's per-listing customization to craft service-appropriate responses
4. Set up Google Sheets integration to log all leads

**Tier 3 -- Custom Automation (Moderate Risk, Higher Capability):**

If you need more control and are comfortable with Python:

1. **Browser Use (self-hosted)** + **Patchright** (undetected Playwright) + residential proxy
2. Run on a cheap VPS ($5-10/mo, e.g., Hetzner or DigitalOcean)
3. Use your real Chrome profile exported to the VPS
4. Check messages every 4-7 minutes (randomized)
5. AI-powered response generation using a local LLM or OpenAI API
6. Log everything to SQLite + Google Sheets
7. Pushover/Slack notifications for human handoff

**Estimated monthly cost for Tier 3:**
| Component | Cost |
|-----------|------|
| VPS (4GB RAM) | $5-10 |
| Residential proxy (5GB) | $20-40 |
| OpenAI API (GPT-4o-mini for responses) | $5-15 |
| Browser Use (self-hosted) | Free |
| Cal.com for booking | Free |
| **Total** | **$30-65/mo** |

### What I Would NOT Recommend

- **Airtop** for this specific use case: Too expensive for simple message checking, credit-based pricing is unpredictable, and it is not designed for social media anti-detection. Better suited for enterprise sales automation.
- **Skyvern** for this use case: Overkill. It is designed for navigating unfamiliar websites, not repeatedly checking the same inbox.
- **FBVerse/AKVerse bots:** High ban risk, designed for product flippers, not service providers.
- **Automated service listing posting:** On any tool. The listings will get removed and your account restricted.

---

## 8. Cost Comparison Table

| Solution | Monthly Cost | Setup Complexity | Ban Risk | 24/7 Capable | Best For |
|----------|-------------|-----------------|----------|-------------|----------|
| FB Auto Reply AI (Chrome ext) | ~$30 | Very Low | Low | Yes (needs PC on) | Quick start, non-technical users |
| AutoResponder.ai (mobile) | ~$5-10 | Very Low | Low | Partial (phone must be on) | Budget option |
| MarketWiz AI | ~$50-100 (est.) | Low | Moderate | Yes (cloud) | Multi-platform sellers |
| Browser Use (self-hosted) + VPS | $30-65 | High | Moderate | Yes | Technical users wanting full control |
| Browser Use Cloud | $100-200 | Medium | Moderate | Yes | Less infra management |
| Airtop Professional | $80+ | Medium | Moderate | Yes | Enterprise workflows |
| MultiLogin + Playwright | $60-100 | High | Low-Moderate | Yes (needs PC/VPS) | Multi-account management |
| Skyvern Pro | $50+ | Medium | Moderate | Yes | Complex multi-site automation |
| Meta Business Suite (official) | Free | Very Low | Zero | Yes | Business page auto-replies |
| Facebook Paid Ads | $150-450 | Low | Zero | Yes | Legitimate lead generation |

---

## 9. Risk Assessment

### Risk Matrix for FB Marketplace Automation

| Activity | Risk Level | Consequence | Mitigation |
|----------|-----------|-------------|------------|
| Posting services as "items" | VERY HIGH | Listing removed, posting privileges revoked | Do not do this. Use paid ads instead. |
| Auto-posting listings (any tool) | HIGH | Account ban, Marketplace access revoked | Use anti-detect browser + residential proxy + slow cadence |
| Auto-responding to inbound messages | LOW-MODERATE | Temporary message limits (24-48 hours) | Randomize timing, vary templates, limit to 20-30/day |
| Using Chrome extensions for auto-reply | LOW | Minimal detection (runs in your real browser) | Keep responses varied and human-sounding |
| Running paid Marketplace ads | ZERO | None -- this is the intended use | Follow Facebook ad policies |
| Posting in local FB Groups | VERY LOW | Group admin may remove post | Follow group rules, do not spam |
| Meta Business Suite auto-replies | ZERO | None -- official feature | Use appropriately |

### Bottom Line

For a legitimate handyman business, the highest-ROI approach is:

1. **Facebook Business Page + Paid Ads** ($5-15/day) for lead generation
2. **Meta Business Suite auto-replies** (free) for immediate response
3. **FB Auto Reply AI extension** (~$30/mo) if you need smarter auto-responses
4. **Local Facebook Groups** for organic reach
5. **Custom Browser Use automation** only if you are technical and volume justifies it

The browser automation tools (Airtop, Browser Use, Skyvern) are powerful but are better suited for scraping, data extraction, and enterprise workflows than for Facebook Marketplace service promotion, which is fundamentally not supported by the platform.

---

*Research compiled from public documentation, pricing pages, community forums, and tool comparison articles. All pricing is approximate and subject to change. Facebook's policies and detection mechanisms evolve continuously.*
