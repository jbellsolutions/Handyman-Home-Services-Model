# Business OS — Operations Guide

This is your daily operations manual. Open Claude Code and talk to it in plain English. It manages ClickUp, Gmail, and Google Calendar for you.

---

## Your Morning Routine (5 minutes)

Open Claude Code and say:

> "Morning briefing"

Claude will show you:
- New leads that came in overnight
- Today's job schedule (who's going where)
- Follow-ups due today
- Unread customer messages

Review and respond to anything urgent.

---

## How to Process a New Lead

When someone calls or messages about a job:

> "New lead: Sarah Johnson, roof leak, 123 Main St Jacksonville 32246, called from Craigslist ad, wants estimate this week"

Claude creates a ClickUp task in your Lead Pipeline with all the details.

To qualify the lead:

> "Qualify the Sarah Johnson lead — she's available Thursday morning, budget is around $500"

Claude moves it from "Incoming" to "Qualified" and adds the notes.

To disqualify:

> "Disqualify the Smith lead — they're outside our service area"

---

## How to Send a Quote

After visiting the job site or getting enough info:

> "Send quote to Sarah Johnson — roof leak repair, $350, includes shingle replacement and flashing around the vent"

Claude:
1. Updates the ClickUp task with the quote amount
2. Moves it to "Quote Sent" status
3. Drafts a quote email for your review
4. Schedules a follow-up reminder for 48 hours

---

## How to Book a Job

When a customer says yes:

> "Book Sarah Johnson for Thursday at 9am, assign to Maudi, roof leak repair at 123 Main St"

Claude:
1. Creates a Google Calendar event for Thursday 9am
2. Updates ClickUp task to "Scheduled" in Active Jobs
3. Assigns it to Maudi
4. Drafts a booking confirmation email to Sarah
5. Schedules a day-before reminder

---

## How to Mark a Job Complete

When the job is done:

> "Job complete: Sarah Johnson roof repair, collected $350 cash"

Claude:
1. Walks you through the completion checklist (see `ops/templates/job-checklist.yaml`)
2. Marks the ClickUp task as "Completed"
3. Logs $350 in Revenue Tracking
4. Calculates the profit split
5. Drafts a review request email to Sarah

---

## How to Run Financial Reports

At any time:

> "P&L this month"

Claude shows:
- Total revenue
- Total expenses (materials, labor, marketing, insurance)
- Net profit
- Justin's share (35%) and Maudi's share (65%)
- Breakdown by service type and lead source

For payout calculation:

> "Calculate this biweekly payout"

Claude pulls the last 2 weeks of revenue and expenses and shows each partner's amount.

---

## How to Add a New Worker

When you hire someone:

> "Add new worker: Mike Rodriguez, phone 904-555-1234, does handyman and property maintenance"

Claude:
1. Adds Mike to the team config
2. Creates a ClickUp entry in Team Management
3. Sets him as "Available"

To assign Mike to a job:

> "Book the Thompson handyman job for Mike, Tuesday at 2pm"

---

## How to Handle a Complaint

> "Customer complaint: Sarah Johnson says the roof is still leaking after our repair"

Claude:
1. Creates a high-priority ClickUp task
2. Pulls up the original job details
3. Suggests next steps (schedule a return visit, contact the worker who did the job)

---

## Common Commands

| What You Want | What to Say |
|---|---|
| See today's schedule | "What's on the schedule today?" |
| Check new leads | "Any new leads?" |
| Book a job | "Book [customer] for [date] at [time], assign to [worker]" |
| Complete a job | "Job complete: [customer], collected $[amount]" |
| Send a follow-up | "Follow up with [customer] about their quote" |
| Weekly summary | "Give me the weekly summary" |
| Monthly P&L | "P&L this month" |
| Payout calculation | "Calculate this biweekly payout" |
| Add a worker | "Add new worker: [name], [phone], does [services]" |
| Check worker schedule | "What's [worker name] doing this week?" |
| Send review request | "Send review request to [customer]" |
| Check which ads work | "Which lead source has the best ROI this month?" |

---

## For the Business Manager (Ashley's Role)

Your job is to be the bridge between leads coming in and jobs going out. Daily:

1. **Morning (10 min):** Run the morning briefing. Respond to new leads. Confirm today's schedule.
2. **During the day:** Book jobs as quotes get accepted. Update job statuses. Handle customer questions.
3. **End of day (5 min):** Mark completed jobs. Log payments. Send review requests.
4. **Weekly (15 min):** Run the P&L. Calculate payouts. Review which lead sources are working best.

You never need to touch a spreadsheet, open ClickUp, or write an email manually. Tell Claude what you need, and it handles the rest.

---

## If You Don't Have a Business Manager

If you're running ops yourself (marketing person or field lead doing double duty), the system works exactly the same. You'll just do the morning briefing and job booking between your other tasks. It takes about 15-20 minutes total per day.
