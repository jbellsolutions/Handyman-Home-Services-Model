# Onboarding Question Flow

This is the reference for the setup wizard. Claude Code follows this when walking a new user through setup. The `setup/wizard.py` script also follows this flow.

---

## Phase 1: Business Info (2 min)

| # | Question | Why We Ask | What We Do With It |
|---|----------|------------|-------------------|
| 1 | Business name | Goes on all ads and business pages | `.env` → `BUSINESS_NAME`, `settings.yaml` → `business.name` |
| 2 | City and state | Targets CL metro, localizes ads | `settings.yaml` → `craigslist.metro_url`, ad templates |
| 3 | Services offered | Generates ad templates per service | `templates.yaml` → one template block per service |
| 4 | Service area | Listed in every ad body | `settings.yaml` → `business.service_area`, ad templates |
| 5 | Pricing per service | For reference when quoting jobs | `settings.yaml` → `business.pricing` |
| 6 | Personal phone | Calls forward here from tracking number | `.env` → `PERSONAL_PHONE` |
| 7 | Owner name | For business pages and customer-facing comms | `.env` → `OWNER_NAME` |
| 8 | Photos ready? | Determines if we use stock photos or skip image upload | Setup flow branching |

**After collecting:** Show summary, ask for confirmation, write to config files.

---

## Phase 2: Tracking Number (5 min)

| # | Question | Options |
|---|----------|---------|
| 1 | Do you already have a tracking number? | Yes → ask for number and provider. No → walk through AvidTrak signup |
| 2 | (If no) Want to set it up now or continue without? | Now → guide through avidtrak.com. Later → use personal phone temporarily |

**Recommended:** AvidTrak at $15/mo
- 14-day free trial, no credit card
- Call recording + AI transcription
- Source tracking (which ad generated the call)
- Local number in their area code
- Forwards to cell

**Alternatives:**
- CallScaler ($29/mo) — $0.50/number, good for multiple campaigns
- CallRail ($45/mo) — industry standard, most features
- Google Voice (free) — no recording, no tracking, not recommended

**After collecting:** Update `.env` with tracking number.

---

## Phase 3: Craigslist Setup (10 min)

| # | Question | Options |
|---|----------|---------|
| 1 | How many ads per day? | Default: 7. Range: 4-7 |
| 2 | How many days per week? | Default: 3. Options: 3 ($420/mo), 5 ($700/mo), 7 ($980/mo) |
| 3 | Posting method? | 1 = Dominator ($10/ad), 2 = Fiverr ($6-7/ad), 3 = DIY agent ($5/ad) |

**If DIY (option 3), also ask:**
| # | Question | Options |
|---|----------|---------|
| 4 | Proxy provider? | brightdata, oxylabs, decodo, smartproxy, none-yet |
| 5 | Anti-detect browser? | gologin ($49/mo), adspower ($5.40/mo), multilogin ($99/mo), none-yet |
| 6 | How many CL accounts? | Need 2-3 for 7 ads/day |

**After collecting:**
1. Generate customized ad templates (3 title variants + 3 body variants per service)
2. Show each ad to user for approval
3. Write to `templates.yaml`
4. Write posting schedule to `settings.yaml`

---

## Phase 4: Facebook Marketplace (5 min)

No config questions needed — we generate listings from their business info.

**What we do:**
1. Generate 7 product-style listings from their services
2. Show each listing for approval
3. Tell them to post from their phone
4. Give them the safety rules (max 1-2/day for first 2 weeks)

---

## Phase 5: Business Pages (5 min)

No config questions — just walk them through signup.

**Priority order:**
1. Google Business Profile — highest SEO impact
2. Nextdoor — neighborhood trust
3. Porch.com — may get free leads on signup
4. Yelp, Home Depot Pro, BuildZoom, Houzz — this week

---

## Phase 6: Daily Routine (2 min)

Show them the daily schedule. No questions — just tell them what to do.

---

## Config Files Written

| File | What's In It | When It's Written |
|------|-------------|-------------------|
| `automation/.env` | Credentials, phone numbers, proxy config | Phase 1-3 |
| `automation/config/settings.yaml` | Business info, posting schedule, safety limits | Phase 1-3 |
| `automation/craigslist/ad_templates/templates.yaml` | Customized ad copy | Phase 3 |

---

## Common Situations

**"I don't have a business name yet"**
→ Use their personal name + service: "Mike's Handyman Services" or "Jacksonville Roof Repair"

**"I only do one service"**
→ Generate templates for that one service. Use both CL categories (skilled trade + household) to get 2 ads from one service.

**"I don't have photos"**
→ Tell them to take photos on their next job. For now, skip image upload in CL ads (text-only ads still work).

**"I don't want to spend money on tracking"**
→ Use their personal phone number. Tell them they're missing data on which ads work. Recommend upgrading to AvidTrak when they can.

**"Craigslist is too expensive"**
→ Start with 3 days/week instead of 7. Or use Fiverr freelancers ($6-7/ad vs $10 for Dominator). Or start with Facebook Marketplace only (free).

**"I'm in a small town without a CL metro"**
→ Find the nearest CL metro that covers their area. Adjust service area in ads.
