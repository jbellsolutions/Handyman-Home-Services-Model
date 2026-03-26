# Handyman Business — Jacksonville FL
## Business Model, Lead Generation, Outreach & Automation

Everything needed to launch and run a handyman/home services business in Jacksonville, FL. Business model, lead gen across all platforms, local outreach system, and browser-based automation for posting and responding.

---

## Services Offered
1. **Wildlife Removal** — raccoons, squirrels, rats, exclusion work
2. **Roof Repair** — leak fixes, shingle replacement, storm damage, flashing
3. **Handyman Work** — drywall, fixtures, painting, doors, trim, general repairs
4. **On-Call Property Maintenance** — lawn care, pressure washing, gutter cleaning, turnover prep

---

## Repository Structure

```
├── business-model/                         # Core business model
│   ├── PRICING-MODEL.md                    # Service pricing & packages
│   ├── SERVICE-MENU.md                     # All services offered
│   └── TARGET-MARKET.md                    # ICP and market analysis
│
├── lead-gen/                               # Lead generation playbooks
│   ├── CHANNEL-STRATEGY.md                 # Which channels, what priority
│   ├── CRAIGSLIST-PLAYBOOK.md              # CL posting strategy & templates
│   ├── HOW-TO-USE-CL-POSTING-SERVICES.md   # ⭐ How to hire CL posting services
│   ├── FB-MARKETPLACE-PLAYBOOK.md          # Facebook Marketplace approach
│   ├── FB-MARKETPLACE-WORKAROUNDS.md       # Product-style service listings for FB
│   ├── NEXTDOOR-PLAYBOOK.md                # Nextdoor monitoring & response
│   └── DAILY-POSTING-SCHEDULE.md           # Daily actions across all channels
│
├── outreach/                               # Local outreach system
│   └── FREE-PLATFORMS-AND-OUTREACH.md      # 16 platforms + Jax contractor/PM/buyer outreach
│
├── automation/                             # Browser-based posting & monitoring code
│   ├── craigslist/
│   │   ├── poster.py                       # Automated CL poster (Playwright + anti-detect)
│   │   └── ad_templates/
│   │       ├── templates.yaml              # 7 ad templates (4 services, 3 variants each)
│   │       └── images/                     # Ad photos organized by service
│   ├── facebook/
│   │   └── inbox_monitor.py                # FB Marketplace inbox monitor (5-min checks)
│   ├── scripts/
│   │   ├── test_proxy.py                   # Proxy connection tester
│   │   └── setup.sh                        # Environment setup script
│   ├── shared/
│   │   ├── db.py                           # SQLite lead tracking
│   │   └── logger.py                       # Structured logging
│   ├── config/
│   │   └── settings.yaml                   # Proxy, account, and schedule config
│   └── requirements.txt                    # Python dependencies
│
└── research/                               # Market & platform research
    ├── MARKETPLACE-LEAD-GEN-RESEARCH-2025-2026.md   # 14-platform deep dive
    ├── FREE-LEAD-PLATFORMS-COMPLETE.md               # 45+ free/cheap platforms
    ├── BROWSER-AUTOMATION-RESEARCH.md                # Playwright, anti-detect, proxies
    ├── CRAIGSLIST-PROXY-RESEARCH.md                  # Jacksonville proxy setup guide
    ├── CRAIGSLIST-POSTING-SERVICES-RESEARCH.md       # Posting service cost comparison
    └── FB-MARKETPLACE-AUTOMATION-RESEARCH.md         # FB automation tools compared
```

---

## 3-Day Test Plan (This Week)

### 7 Ads Per Day:

| # | Service | CL Category 1 | CL Category 2 |
|---|---------|---------------|---------------|
| 1 | Wildlife Removal | Skilled Trade Services | — |
| 2 | Wildlife Removal | — | Household Services |
| 3 | Roof Repair | Skilled Trade Services | — |
| 4 | Roof Repair | — | Household Services |
| 5 | Property Maintenance | Skilled Trade Services | — |
| 6 | Property Maintenance | — | Household Services |
| 7 | Handyman Work | Skilled Trade Services | — |

**Same 7 ads also posted to Facebook Marketplace** using product-style workarounds (gift certificates, free estimate listings, maintenance packages).

### Test Budget: ~$210 for 3 days (CL Dominator) or ~$115 (Fiverr)

---

## Lead Gen Channels

### Tier 1 — Post Ads Here (Free / Near-Free)
| Channel | Cost | Action |
|---------|------|--------|
| **Craigslist** | $5/post (CL fee) | 7 ads/day, 3 days/week via posting service |
| **Facebook Marketplace** | Free | Product-style listings (see workarounds guide) |
| **Google Business Profile** | Free | Set up and optimize for all 4 services |
| **Nextdoor** | Free | Claim business page, monitor for job requests |

### Tier 2 — Sign Up & Receive Leads (Free Listings)
| Channel | Cost | Action |
|---------|------|--------|
| **Porch.com** | Free listing | Sign up, fill out profile completely |
| **Home Depot Pro Referral** | Points-based (free) | Register for the referral network |
| **Yelp** | Free listing | Claim business, start collecting reviews |
| **BuildZoom** | 2.5% only if hired | Zero upfront risk |
| **Houzz** | Free profile | Upload portfolio photos |
| **Alignable** | Free | Local business networking |

### Tier 3 — Free Classifieds (Post Everywhere)
| Channel | Cost | Action |
|---------|------|--------|
| **Locanto** | Free | Post all 4 services |
| **ClassifiedAds.com** | Free | Post all 4 services |
| **Geebo** | Free | Post all 4 services |

### Tier 4 — Local Outreach (Direct Contact)
| Target | How to Find Them | Action |
|--------|-----------------|--------|
| **Property Managers** | Google "Jacksonville property management" | Cold call/email for retainer deals |
| **Local Contractors** | DBPR license search, Google Maps | Partner for overflow/referral work |
| **Recent Home Buyers** | Duval County Property Appraiser records | Direct mail + cold call (past 90 days) |
| **Real Estate Investors** | Tax records, DBPR, BiggerPockets | Offer on-call maintenance packages |

---

## How to Get Started Tomorrow

1. **Read** `lead-gen/HOW-TO-USE-CL-POSTING-SERVICES.md` — pick your posting method
2. **Prep photos** — 4-8 per service, drop in `automation/craigslist/ad_templates/images/`
3. **Sign up** for Craigslist Dominator ($10 free credit) or find a Fiverr freelancer
4. **Post 7 ads** on Craigslist using our templates
5. **Post 7 product-style listings** on FB Marketplace (see `lead-gen/FB-MARKETPLACE-WORKAROUNDS.md`)
6. **Set up Google Business Profile** for all 4 services
7. **Claim Nextdoor business page**
8. **Start calling** Jacksonville property managers from the outreach list

---

## Proxy Setup (If Posting Yourself from Tampa)

See `research/CRAIGSLIST-PROXY-RESEARCH.md` for full details.

**Quick version:**
- Best: Use the Jacksonville MacBook (free, most authentic IP)
- Alternative: Bright Data ISP proxies — $2/IP/month for static Jacksonville IPs
- Required: Anti-detect browser (GoLogin $49/mo or AdsPower $5.4/mo)
- Each CL account needs: unique IP + unique browser profile + unique phone + unique email
