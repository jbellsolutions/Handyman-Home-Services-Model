# Home Services Lead Machine

**Get leads for your home service business in 24 hours.**

This is a complete lead generation system built for handymen, roofers, plumbers, electricians, pest control, property maintenance — any home service business. It sets up your ads, tracking number, business pages, and automation so you can focus on doing the work.

---

## What You Get

- **Craigslist ads** — 4-7 ads/day in your city, with templates proven to generate calls
- **Facebook Marketplace listings** — product-style workarounds that don't get flagged
- **Call tracking number** — records every call, tells you which ad generated it ($15/mo)
- **Business page setup** — Google Business Profile, Nextdoor, Porch, Yelp
- **Ad templates** — pre-written for wildlife removal, roof repair, handyman, property maintenance (customizable for any service)
- **Posting automation** — optional DIY agent that posts your CL ads automatically (saves $600+/mo vs posting services)
- **Daily playbook** — exactly what to do every morning, midday, and evening to keep leads flowing
- **Partnership agreement template** — ready-to-use LLC-to-LLC agreement for business partners

---

## How to Start (2 minutes)

### Step 1: Open this repo in Claude Code

```bash
git clone https://github.com/jbellsolutions/Handyman-Home-Services-Model.git
cd Handyman-Home-Services-Model
```

Open it in [Claude Code](https://claude.ai/code) (CLI, desktop app, or IDE extension).

### Step 2: Say "Set me up"

Claude will walk you through everything:

1. Your business info (name, city, services, pricing)
2. Tracking number setup (AvidTrak — $15/mo, records calls)
3. Craigslist ad creation (custom ads for your services)
4. Facebook Marketplace listings (free)
5. Business page setup (Google, Nextdoor, Porch — all free)
6. Your daily lead routine

**No technical knowledge required.** Claude asks simple questions, you answer, and it configures everything.

### Step 3: Answer the phone

Leads start coming in within hours of your first Craigslist ad going live. Respond fast — first to call back wins the job.

---

## What It Costs

### To Get Started (Week 1)

| Item | Cost |
|------|------|
| Call tracking (AvidTrak) | $0 (14-day free trial) |
| Craigslist ads (7 ads x $5 each x 3 days) | $105 |
| Facebook Marketplace | $0 |
| Business pages | $0 |
| **Total to launch** | **$105** |

### Monthly (Once Running)

| Item | Cost |
|------|------|
| Craigslist ads (7/day x 3 days/week) | $420-$840 |
| Call tracking | $15 |
| Everything else | $0 |
| **Total monthly** | **$435-$855** |

### What You Should Make

- **Week 1:** 5-15 leads, 1-3 jobs booked
- **Month 1:** 3-5 leads/day, $3,000-$8,000 revenue
- **Month 2-3:** 5-10 leads/day, $15,000-$30,000/month revenue

---

## Craigslist Posting Options

| Method | Cost Per Ad | Effort | Best For |
|--------|-------------|--------|----------|
| **Craigslist Dominator** | $10/live ad | Zero — they do everything | Getting started fast |
| **Fiverr freelancer** | $6-7/live ad | Send ad copy + photos | Budget-conscious |
| **DIY posting agent** | $5/ad (CL fee only) | Setup once, runs itself | Scaling past 7 ads/day |

Start with Dominator or Fiverr. Graduate to the DIY agent when you're ready to save $600+/month.

---

## Repo Structure

```
.
├── CLAUDE.md                    # Setup wizard brain (Claude reads this)
├── README.md                    # You're reading this
├── LAUNCH-CHECKLIST.md          # Step-by-step checklist (manual version)
├── PARTNERSHIP-AGREEMENT.md     # LLC-to-LLC partner agreement template
│
├── setup/
│   ├── wizard.py                # Interactive setup script
│   └── onboarding.md            # Setup question flow reference
│
├── automation/
│   ├── .env.example             # Config template (copy to .env)
│   ├── requirements.txt         # Python dependencies
│   ├── config/
│   │   └── settings.yaml        # Business config, posting schedule
│   ├── craigslist/
│   │   ├── poster.py            # CL posting agent (GoLogin + Playwright)
│   │   ├── ghost_check.py       # Verify ads are actually visible
│   │   └── ad_templates/
│   │       └── templates.yaml   # Ad copy templates (customized during setup)
│   ├── facebook/
│   │   └── inbox_monitor.py     # FB Marketplace message monitor
│   ├── shared/
│   │   ├── db.py                # SQLite lead tracking
│   │   └── logger.py            # Logging
│   └── scripts/
│       ├── setup.sh             # Dependency installer
│       └── test_proxy.py        # Proxy connection tester
│
├── lead-gen/                    # Platform playbooks
│   ├── HOW-TO-USE-CL-POSTING-SERVICES.md
│   ├── FB-MARKETPLACE-WORKAROUNDS.md
│   ├── CRAIGSLIST-PLAYBOOK.md
│   ├── FB-MARKETPLACE-PLAYBOOK.md
│   ├── NEXTDOOR-PLAYBOOK.md
│   ├── CHANNEL-STRATEGY.md
│   └── DAILY-POSTING-SCHEDULE.md
│
├── outreach/
│   └── FREE-PLATFORMS-AND-OUTREACH.md
│
├── business-model/
│   ├── PRICING-MODEL.md
│   ├── SERVICE-MENU.md
│   └── TARGET-MARKET.md
│
├── research/                    # Deep research on every platform
│   ├── CRAIGSLIST-PROXY-RESEARCH.md
│   ├── CRAIGSLIST-POSTING-SERVICES-RESEARCH.md
│   ├── FB-MARKETPLACE-AUTOMATION-RESEARCH.md
│   ├── BROWSER-AUTOMATION-RESEARCH.md
│   ├── FREE-LEAD-PLATFORMS-COMPLETE.md
│   └── MARKETPLACE-LEAD-GEN-RESEARCH-2025-2026.md
│
├── docs/
│   └── TROUBLESHOOTING.md
│
└── swipe-file/                  # Reference ads and examples
```

---

## For Partners: Partnership Agreement

If you're starting this business with a partner, the `PARTNERSHIP-AGREEMENT.md` is a ready-to-use LLC-to-LLC template that covers:

- Revenue split (customizable — default 35/65)
- Who does what (marketing vs. field work)
- Marketing budget management
- 30-day test period with clean exit terms
- IP ownership (who keeps what if you split)
- Decision-making framework
- Growth milestones (10 workers, $30-50K/month)

Edit it with your names, percentages, and terms. Both parties sign. Done.

---

## FAQ

**How fast will I get leads?**
First leads typically come within 24-48 hours of your first Craigslist ad going live. Craigslist is the fastest channel.

**Do I need to be technical?**
No. Claude Code walks you through everything in plain English. You answer questions, it does the setup.

**Can I use this for any home service?**
Yes. The ad templates are customizable for any service — plumbing, electrical, HVAC, landscaping, cleaning, painting, anything.

**What if my Craigslist ads get flagged?**
The system includes proxy research, anti-detection strategies, and multi-account rotation. See `research/CRAIGSLIST-PROXY-RESEARCH.md` for the full breakdown.

**Do I need a business license?**
Depends on your state and city. This system helps you get leads — licensing and insurance are your responsibility.

**Can I use this in any city?**
Yes. During setup, you tell Claude your city and it customizes everything for your market.

---

## Support

Open this repo in Claude Code and ask any question. The system has deep research docs on every platform and strategy. If Claude can't answer from the docs, it will research it for you.

---

Built by [JBell Solutions](https://github.com/jbellsolutions)
