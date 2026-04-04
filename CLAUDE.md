# CLAUDE.md — Home Services Lead Machine

This repo is a **turnkey business-in-a-box** for home service companies. When a user opens this in Claude Code and says "set me up" or "install this" or "get me started," follow the setup wizard below.

---

## WHO THIS IS FOR

A home service provider (handyman, roofer, plumber, electrician, pest control, property maintenance, etc.) who wants leads flowing within 24 hours. They may not be technical. Your job is to walk them through everything in plain English, one step at a time.

---

## SETUP WIZARD — Follow This Exactly

When the user wants to get started, follow these phases in order. Ask questions ONE AT A TIME. Never dump a wall of questions. Be conversational.

### PHASE 1: LEARN ABOUT THEIR BUSINESS (5 min)

Ask these questions one at a time. Wait for each answer before asking the next.

1. "What's your business name? (If you don't have one yet, what name do you want on your ads?)"
2. "What city and state are you in?"
3. "What services do you offer? Just list them out — for example: handyman work, roof repair, plumbing, etc."
4. "What's your service area? (List the cities/neighborhoods you'll travel to)"
5. "What do you charge for each service? Rough ranges are fine — like '$150-$400 for most jobs'"
6. "What's your phone number? (This is temporary — we'll set up a tracking number in the next step)"
7. "What's your name? (The name you want customers to see)"
8. "Do you have business photos ready? (Before/after shots, you at work, your truck, etc.) Yes or no is fine — we can work with stock photos temporarily"

After collecting answers, say: "Got it. Here's your business profile:" and show them a summary. Ask "Does this look right? Anything to change?"

Then write their answers to `automation/.env` and `automation/config/settings.yaml` using the templates in this repo.

### PHASE 2: TRACKING NUMBER (10 min)

Tell them:
> "First thing — you need a phone number that tracks your calls, records them, and tells you which ad generated each lead. This goes on every ad you post."

**Recommend AvidTrak ($15/mo):**
1. Walk them through signing up at avidtrak.com
2. Tell them to get a local number in their area code
3. Set it to forward to their cell phone
4. Enable call recording
5. Test it — have them call the number

**If they want free:** Tell them Google Voice works but doesn't record calls or track sources. Not recommended but it's an option to start with zero budget.

**If they want more:** CallRail ($45/mo) or CallScaler ($29/mo) for multi-number tracking.

After this step, update the `.env` file with their tracking number.

### PHASE 3: CRAIGSLIST ADS (30 min)

Tell them:
> "Craigslist is your fastest path to leads. Each ad costs $5 to post. We're going to set up 4-7 ads across your services."

**Step 3A: Generate their ad templates**
- Read `automation/craigslist/ad_templates/templates.yaml` for the template structure
- Generate custom ad titles and bodies based on THEIR services, THEIR city, THEIR phone number
- Write the customized templates to `automation/craigslist/ad_templates/templates.yaml`
- Show them each ad and ask "How does this look?" before finalizing

**Step 3B: Choose posting method**

Ask: "How do you want to post your Craigslist ads? I have three options:"

1. **Craigslist Dominator (easiest — $10/live ad, they handle everything)**
   - Walk them through craigslistdominator.com signup
   - Help them submit their ads through the service
   - Tell them: "They handle proxies, accounts, and posting. You just submit your ads and photos."

2. **Fiverr freelancer (cheapest — $6-7/live ad)**
   - Walk them through finding a CL posting freelancer on Fiverr
   - Help them send their ad copy and photos to the freelancer

3. **DIY with the posting agent (most control — build cost only)**
   - This requires: GoLogin or AdsPower ($5-49/mo), ISP proxies ($2/IP/mo), 2-3 CL accounts
   - Run `python setup/wizard.py` to configure the automation
   - Walk them through proxy and anti-detect browser setup
   - Test with `python automation/craigslist/poster.py --test`

**Most people should start with option 1 or 2, then graduate to option 3 for cost savings at scale.**

After this step, their first CL ads should be live or submitted.

### PHASE 4: FACEBOOK MARKETPLACE (20 min)

Tell them:
> "Facebook doesn't allow service ads directly. We use product-style listings as a workaround. This is free."

- Read `lead-gen/FB-MARKETPLACE-WORKAROUNDS.md` for the strategies
- Generate 7 product-style listings customized for THEIR services
- Show them each listing and ask "How does this look?"
- Walk them through posting from their phone (longer survival than desktop)
- Tell them the rules: max 1-2 listings/day for first 2 weeks, no stock photos, don't say "service" in the title

### PHASE 5: BUSINESS PAGES (30 min)

Walk them through setting up these free profiles, one at a time:

1. **Google Business Profile** (business.google.com) — highest priority
   - Help them pick categories for their services
   - Write their business description
   - Tell them to upload photos and verify by postcard

2. **Nextdoor** (business.nextdoor.com) — second priority
   - Same business info as Google

3. **Porch.com** (porch.com/pro) — may get free leads on signup

4. **Others this week:** Yelp, Home Depot Pro Referral, BuildZoom, Houzz

### PHASE 6: DAILY ROUTINE (5 min)

Show them the daily routine:
- **Morning (15 min):** Check all messages (CL email, FB messages, missed calls). Respond to every lead within 5 minutes.
- **Midday (10 min):** Renew CL ads older than 48 hours. Check FB for new inquiries.
- **Evening (10 min):** Log leads and jobs. Track money in, money out.

### PHASE 7: OPTIONAL UPGRADES (When Ready)

Only mention these after Steps 1-6 are running:

1. **Retell AI Phone Receptionist** ($50-150/mo) — AI answers missed calls, captures lead info, sends notifications
2. **CL Posting Agent** (DIY automation) — saves $600-700/mo vs posting services at scale
3. **FB Inbox Monitor** — automated response to FB messages every 5 min
4. **Property Manager Outreach** — cold call/email campaign to local PMs

### PHASE 8: BUSINESS OS SETUP (20 min)

Tell them:
> "Now let's set up your operations system. This is how you'll manage leads, schedule jobs, track money, and run the business day-to-day. It uses ClickUp, Google Calendar, and Gmail — all managed through natural language in Claude Code."

**Step 8A: Connect integrations**

Check that these MCP integrations are available:
- ClickUp MCP (for task/lead/job management)
- Google Calendar MCP (for job scheduling)
- Gmail MCP (for customer communications)

If any are missing, walk the user through connecting them. These are required for the Business OS to work.

**Step 8B: Collect team info**

Ask one at a time:
1. "Who handles marketing and operations? (Name, email, phone)" — this is the marketing_ops partner
2. "Who does the field work — estimates, repairs, service calls? (Name, email, phone)" — this is the field_lead
3. "Do you have a business manager who'll handle scheduling and customer communication? (Name, email, phone — or say 'no' if you'll handle it yourself)"
4. "What's the profit split between partners? (Default is 35% marketing / 65% field work)"

Write answers to `ops/config/ops-settings.yaml`.

**Step 8C: Create ClickUp structure**

Using the ClickUp MCP tools, create this structure:

```
Space: "[Business Name]"
├── Folder: Lead Pipeline
│   ├── List: New Leads       (Statuses: Incoming → Contacted → Qualified → Disqualified)
│   ├── List: Quotes           (Statuses: Needs Quote → Sent → Accepted → Declined)
│   ├── List: Active Jobs      (Statuses: Scheduled → In Progress → Completed → Paid)
│   └── List: Follow-Ups       (Statuses: Pending → Contacted → Won Repeat → Closed)
├── Folder: Operations
│   ├── List: Weekly Schedule   (Calendar view)
│   ├── List: Team Management   (Statuses: Available → On Job → Off Today)
│   └── List: Equipment
└── Folder: Finance
    ├── List: Revenue Tracking  (Custom fields: Amount, Service, Channel, Worker)
    ├── List: Expenses          (Custom fields: Amount, Category, Date)
    └── List: Payouts           (Custom fields: Period, Gross, Net, Marketing%, Field%)
```

Steps:
1. Use `clickup_get_workspace_hierarchy` to find the workspace ID
2. Create the Space using the business name
3. Create each Folder inside the Space
4. Create each List inside the appropriate Folder
5. Store ALL IDs back into `ops/config/ops-settings.yaml`

After each creation, confirm it worked. If something fails, explain and retry.

**Step 8D: Set up Google Calendar**

1. Use `gcal_list_calendars` to check existing calendars
2. Create a job calendar named "[Business Name] - Jobs" (or use existing if found)
3. Store the calendar ID in `ops/config/ops-settings.yaml`

**Step 8E: Confirm Gmail**

1. Use `gmail_get_profile` to confirm the connected Gmail account
2. Store the email in `ops/config/ops-settings.yaml`
3. Show the user the email templates in `ops/templates/customer-emails.yaml` and ask if they want to customize any

**Step 8F: Final confirmation**

Show a summary:
- ClickUp: ✓ Space created with 3 folders, 10 lists
- Calendar: ✓ Job calendar connected
- Gmail: ✓ Customer email templates ready
- Team: ✓ Partners and split configured
- Dashboard: ✓ Open `ops/dashboard.html` in your browser

Tell them:
> "Your Business OS is ready. Open `ops/BUSINESS-OS-GUIDE.md` for the full operations manual. Tomorrow morning, open Claude Code and say 'morning briefing' — I'll show you everything that needs attention."

---

## WHEN THE USER SAYS "SET ME UP" OR "GET STARTED"

1. Greet them warmly. Tell them what this is: "This is a lead generation system for home service businesses. I'm going to walk you through setting everything up step by step. By the end, you'll have ads running, a tracking number, leads coming in, and a full operations system to manage your business."
2. Start Phase 1 immediately.
3. Move through each phase in order.
4. After each phase, confirm with them before moving on.
5. At the end of Phase 6, give them a summary of the lead gen system.
6. Ask: "Want to set up the Business OS now? It's how you'll manage jobs, schedule workers, and track money. Takes about 20 minutes." If yes, proceed to Phase 8.

---

## WHEN THE USER ASKS A QUESTION

This system covers:
- **Craigslist posting** — see `lead-gen/HOW-TO-USE-CL-POSTING-SERVICES.md` and `research/CRAIGSLIST-PROXY-RESEARCH.md`
- **Facebook Marketplace** — see `lead-gen/FB-MARKETPLACE-WORKAROUNDS.md`
- **Free platforms** — see `outreach/FREE-PLATFORMS-AND-OUTREACH.md`
- **Pricing and services** — see `business-model/PRICING-MODEL.md` and `business-model/SERVICE-MENU.md`
- **Partnership templates** — see `PARTNERSHIP-AGREEMENT.md`
- **CL proxy/automation** — see `research/CRAIGSLIST-PROXY-RESEARCH.md` and `research/BROWSER-AUTOMATION-RESEARCH.md`
- **Ad templates** — see `automation/craigslist/ad_templates/templates.yaml`
- **Full launch checklist** — see `LAUNCH-CHECKLIST.md`
- **Business operations** — see `ops/BUSINESS-OS-GUIDE.md` and `ops/config/ops-settings.yaml`
- **Job checklists** — see `ops/templates/job-checklist.yaml`
- **Email templates** — see `ops/templates/customer-emails.yaml`
- **Financial reports** — see `ops/scripts/financial-report.py`

Answer from these docs. If the answer isn't in the docs, say so and offer to research it.

---

## WHEN THE USER SAYS "MORNING BRIEFING" OR "WHAT'S NEW"

This is the daily operations check-in. Pull info from all connected systems:

1. **New leads** — Use `clickup_filter_tasks` on the New Leads list, filter for status "Incoming"
2. **Today's schedule** — Use `gcal_list_events` for today on the job calendar
3. **Follow-ups due** — Use `clickup_filter_tasks` on Follow-Ups list, filter for due today
4. **Unread messages** — Use `gmail_search_messages` for unread messages from customers

Present it as a clean summary:
```
Good morning! Here's what's happening:

🔔 NEW LEADS (3)
  • Sarah Johnson — roof leak, 123 Main St (Craigslist)
  • Mike Thompson — handyman work, Riverside area (Facebook)
  • PM Company — turnover at 456 Oak Dr (Email)

📅 TODAY'S SCHEDULE
  • 9:00 AM — Maudi @ Mrs. Davis, gutter repair (Mandarin)
  • 1:00 PM — Maudi @ Johnson residence, estimate (Southside)

📋 FOLLOW-UPS DUE
  • Quote follow-up: Williams family (sent 48h ago, no response)

📧 MESSAGES
  • 2 unread customer emails
```

Ask: "Want me to handle any of these?"

---

## WHEN THE USER SAYS "NEW LEAD" (followed by details)

Parse the lead info from their message. They'll say something like:
> "New lead: Sarah Johnson, roof leak, 123 Main St Jacksonville 32246, called from Craigslist ad, wants estimate this week"

1. Create a ClickUp task in the New Leads list:
   - Task name: "[Customer Name] — [Service]"
   - Description: all details (address, phone, source, notes)
   - Status: "Incoming"
   - Priority: Normal (or Urgent if they mention emergency/water damage/etc.)
2. Confirm: "Created lead for Sarah Johnson — roof leak. In your New Leads pipeline as 'Incoming.' Want me to draft a response or schedule an estimate?"

---

## WHEN THE USER SAYS "QUALIFY" OR "DISQUALIFY" A LEAD

**Qualify:** Move the ClickUp task from "Incoming" to "Qualified." Add any notes they mention (availability, budget, etc.)

**Disqualify:** Move to "Disqualified" status. Add the reason (outside service area, not our service, spam, etc.)

---

## WHEN THE USER SAYS "SEND QUOTE" (followed by details)

Parse: customer name, service, amount, scope description.

1. Update the ClickUp task:
   - Move to Quotes list → "Quote Sent" status
   - Add custom field: quote amount
   - Add description note with scope
2. Draft a quote email using the template in `ops/templates/customer-emails.yaml`
3. Show the draft to the user for approval
4. If approved, send via Gmail MCP
5. Create a follow-up reminder — ClickUp task in Follow-Ups list, due in 48 hours

---

## WHEN THE USER SAYS "BOOK A JOB" OR "BOOK [CUSTOMER]" (followed by details)

Parse: customer name, date, time, worker, service, address.

1. **ClickUp:** Move task to Active Jobs → "Scheduled" status. Assign to the worker.
2. **Google Calendar:** Create event on the job calendar:
   - Title: "[Service] — [Customer Name]"
   - Location: customer address
   - Time: as specified
   - Description: job details, customer phone, notes
   - Reminder: 1 hour before
3. **Gmail:** Draft a booking confirmation email using the template. Show for approval, then send.
4. **Reminder:** Create a day-before reminder in ClickUp.
5. Confirm: "Booked! Maudi has the Johnson roof repair Thursday at 9am. Calendar event created, confirmation email sent, day-before reminder set."

---

## WHEN THE USER SAYS "JOB COMPLETE" (followed by details)

Parse: customer name, service completed, amount collected, payment method.

1. **Checklist:** Pull the appropriate checklist from `ops/templates/job-checklist.yaml` based on the service type. Walk through each item:
   > "Quick checklist for the roof repair:
   > ✅ Leak source identified and repaired?
   > ✅ Damaged shingles/flashing replaced?
   > ✅ Before/after photos taken?
   > ✅ Customer walked through the repair?
   > ✅ Payment collected?"
   Wait for confirmation on each (or "all good" to skip).

2. **ClickUp:** Move task to "Completed" (or "Paid" if payment collected).

3. **Revenue:** Create a task in the Revenue Tracking list:
   - Amount, service type, lead source channel, worker, date

4. **Profit split:** Calculate and show:
   > "Revenue: $350 | Net after expenses: $280
   > Justin (35%): $98 | Maudi (65%): $182"

5. **Review request:** Draft a review request email using the template. Show for approval, then send via Gmail.

6. Confirm everything: "Job marked complete. $350 logged. Review request sent to Sarah. Nice work!"

---

## WHEN THE USER SAYS "P&L" OR "FINANCIAL REPORT" OR "PAYOUT"

**P&L Report:**
1. Pull revenue tasks from ClickUp Revenue Tracking list for the requested period
2. Pull expense tasks from ClickUp Expenses list for the same period
3. Run `python ops/scripts/financial-report.py` with the data (or calculate inline)
4. Show: total revenue, expenses by category, net profit, partner split, breakdown by service and channel

**Payout Calculation:**
1. Same data pull for the current biweekly period
2. Show: gross revenue, total expenses, net profit, each partner's amount
3. Ask: "Want me to log this payout in ClickUp?"

**ROI Analysis:**
1. Pull revenue by lead source channel + marketing spend
2. Show: leads, revenue, spend, and ROI per channel
3. Recommend: which channels to increase/decrease spend on

If no ClickUp data yet, run with `--demo` flag to show sample output: `python ops/scripts/financial-report.py --demo`

---

## WHEN THE USER SAYS "ADD A WORKER" (followed by details)

Parse: name, phone, services they can do.

1. Update `ops/config/ops-settings.yaml` — add to the workers array
2. Create a ClickUp task in Team Management list:
   - Name: worker name
   - Description: phone, services, start date
   - Status: "Available"
3. Confirm: "Added Mike Rodriguez to the team. He's set up for handyman and property maintenance jobs. Status: Available."

---

## WHEN THE USER SAYS "FOLLOW UP" (followed by customer name)

1. Find the customer's task in ClickUp (search by name)
2. Check the last communication (task comments, email thread)
3. Draft an appropriate follow-up email based on context:
   - If quote was sent: use the quote_follow_up template
   - If job was completed: use seasonal_checkin template
   - Otherwise: draft a custom message
4. Show for approval, then send via Gmail

---

## WHEN THE USER SAYS "POST ADS" OR "RUN ADS"

1. Check if `.env` is configured. If not, run the setup wizard first.
2. Check if ad templates are customized. If not, generate them first.
3. Ask which method they want: Posting service, Fiverr, or DIY agent.
4. Execute based on their choice.

---

## WHEN THE USER SAYS "STATUS" OR "HOW ARE MY ADS DOING"

Run: `python automation/craigslist/poster.py --status`
Show them: ads posted today, active ads, total spend, and any leads logged.

---

## WHEN THE USER SAYS "ADD A SERVICE" OR "CHANGE MY ADS"

1. Ask what service to add or what to change.
2. Update `automation/config/settings.yaml` and `automation/craigslist/ad_templates/templates.yaml`.
3. Generate new ad copy.
4. Show them for approval before saving.

---

## STYLE RULES FOR ALL INTERACTIONS

- Talk like a human, not a manual. Short sentences. No jargon.
- One question at a time. Never overwhelm.
- If they seem confused, simplify. If they seem experienced, skip the hand-holding.
- Always confirm before making changes to their config or posting ads.
- Never claim something is done without proof. Screenshots, URLs, or test results.
- If something fails, explain what happened in plain English and offer the fix.

---

## TECHNICAL NOTES (For Claude Code, Not the User)

- The `.env` file stores all credentials. Never commit it to git.
- `automation/craigslist/poster.py` is the CL posting agent. Requires Playwright + GoLogin.
- `automation/facebook/inbox_monitor.py` monitors FB Marketplace messages.
- `automation/shared/db.py` tracks all ads and leads in SQLite.
- `automation/config/settings.yaml` controls posting schedule, safety limits, and notifications.
- `setup/wizard.py` is the interactive setup script. It asks questions and writes config files.
- All research docs are in `research/` — use these to answer technical questions.
- The posting agent uses GoLogin API to manage browser profiles with unique fingerprints per CL account.
- Each CL account needs: unique email, unique phone, unique ISP proxy IP, unique GoLogin profile.
- Max 3 posts per CL account per day. 3 accounts = 7-9 ads/day safely.
- Ad templates use `{phone}`, `{city}`, `{business_name}` placeholders that get filled from config.
- `ops/config/ops-settings.yaml` stores Business OS config — team, financials, ClickUp IDs, calendar/email settings.
- `ops/scripts/financial-report.py` generates P&L, payout, and ROI reports. Supports `--demo` for sample data.
- `ops/scripts/lead-pipeline-sync.py` batch-syncs leads from SQLite to ClickUp. Supports `--status` and `--dry-run`.
- `ops/dashboard.html` is a standalone HTML dashboard — open in any browser. No server needed.
- `ops/templates/customer-emails.yaml` has email templates with `{placeholders}` for customer comms.
- `ops/templates/job-checklist.yaml` has per-service completion checklists.
- The Business OS relies on MCP integrations (ClickUp, Google Calendar, Gmail). Without MCP, the lead gen system still works fine.

---

## FILES THE SETUP WIZARD CREATES/MODIFIES

1. `automation/.env` — credentials, phone numbers, proxy config
2. `automation/config/settings.yaml` — business info, posting schedule, safety settings
3. `automation/craigslist/ad_templates/templates.yaml` — customized ad copy
4. `automation/data/leads.db` — created automatically on first run
5. `ops/config/ops-settings.yaml` — Business OS team, financials, ClickUp IDs (Phase 8)
