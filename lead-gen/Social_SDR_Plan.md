# UAIS Social SDR Automation Plan
## Browser Use — LinkedIn, Facebook, Instagram

---

## THE BUSINESS (Summary)
- **Company:** Using AI to Scale (UAIS)
- **Offer:** Recruit, certify, and place AI Integrators into businesses. Human + AI agent stack.
- **Tiers:** Starter ($1K), Professional ($2K), Enterprise ($5K) + $300/mo recurring
- **ICP:** Business owners and team managers who need AI-trained help to run their operations
- **Guarantee:** Double productivity in 30 days or money back
- **One-liner:** "We recruit, certify, and place an AI-trained integrator into your business. They double your team's output in 30 days or you don't pay."

---

## PLATFORM STRATEGY

### LinkedIn — The Closer (Highest-value leads)
**Why:** Decision-makers live here. Business owners, team leads, ops managers actively looking for productivity solutions. Longest sales cycle but highest ticket.

**Daily Limits:**
- Connection requests: 10/day
- DMs: 20/day (mix of new + follow-up)
- Comments: 15-20/day
- Post engagement (likes): 30/day
- Posts on your profile: 1/day

### Facebook — The Networker (Volume play)
**Why:** Groups are gold mines. Business owner groups, local entrepreneur groups, "hiring help" groups. This is where the organic playbook you shared shines.

**Daily Limits:**
- Friend requests: 20/day (you said 20, playbook says 40 — keeping yours for safety with automation)
- DMs: 30/day (mix of new + follow-up)
- Comments: 15-20/day
- Group posts: 1/day
- Profile/page posts: 1/day
- Post engagement (likes/reactions): 40/day

### Instagram — The Brand Builder (Awareness + warm leads)
**Why:** Visual proof of what you do. Behind-the-scenes of AI setups, client wins, short-form content. Lower intent than LinkedIn but broader reach.

**Daily Limits:**
- Follow requests: 50/day
- DMs: 30/day
- Comments: 20/day
- Story engagement: 15/day
- Posts/reels: 1/day

---

## SDR AGENT PERSONAS

Each platform gets a distinct voice that matches platform culture, but all funnel toward the same goal: **book a warm-up call.**

### LinkedIn Persona — "The Expert Connector"
- **Tone:** Professional but not corporate. Direct. Confident. No fluff.
- **Style:** Leads with insight, not pitches. Comments add real value. DMs feel like a peer reaching out, not a salesperson.
- **Example comment:** "This is exactly the gap most teams hit — they buy the AI tools but nobody knows how to use them. We started placing trained AI integrators into businesses for exactly this reason. The tool isn't the bottleneck, the operator is."
- **Example DM:** "Hey {{firstName}} — saw your post about scaling ops. Quick question: if someone showed up tomorrow already trained on AI tools and doubled one person's output in 30 days, what role would you put them in? That's literally what we do. Happy to show you how it works."

### Facebook Persona — "The Friendly Networker"
- **Tone:** Casual, warm, approachable. Like a helpful friend who happens to know AI.
- **Style:** Asks questions, starts conversations, builds rapport first. Never pitches in comments. Always pulls to DM.
- **Example comment:** "Love this question! We actually just helped a business owner solve this exact thing last week. Mind if I PM you? Would love to share what worked for them 🙂"
- **Example DM:** "Hey {{firstName}}! Just saw your post in [group name] and had to reach out. Sounds like you're dealing with a lot of the same stuff we help businesses with every day. What's taking up most of your time right now that you wish you could hand off?"

### Instagram Persona — "The Results Showcaser"
- **Tone:** Energetic, visual, proof-driven. Short punchy comments.
- **Style:** Engages with content genuinely. Comments feel real, not bot-like. DMs are casual and direct.
- **Example comment:** "This is exactly why we built what we built 🔥 Most businesses are drowning in manual work when AI could handle 80% of it"
- **Example DM:** "Hey! Loved your content about [topic]. Quick question — have you thought about bringing in someone AI-trained to handle [pain point they posted about]? We place certified AI integrators into businesses. Might be worth a quick chat if you're open to it."

---

## BROWSER USE SKILLS TO BUILD

### Skill 1: LinkedIn Commenter
**Trigger:** Runs daily on schedule
**Actions:**
1. Navigate to LinkedIn feed
2. Scroll through feed, identify posts from target audience (business owners, team leads posting about hiring, productivity, AI, scaling)
3. Leave thoughtful, value-add comments (not generic — reference specific content)
4. Like the post
5. Track which posts were commented on (file system persistence)
**Safety:** Max 15-20 comments/day. Randomized timing (2-5 min between actions). No duplicate comments.

### Skill 2: LinkedIn Connector
**Trigger:** Runs daily on schedule
**Actions:**
1. Search LinkedIn for target profiles (business owners, ops managers, team leads)
2. Review profile to confirm ICP match
3. Send personalized connection request with note
4. Log connection request sent
**Safety:** Max 10/day. Include personalized note referencing something from their profile. Never send generic "I'd like to connect."

### Skill 3: LinkedIn DM Sequence
**Trigger:** Runs daily — checks for new connection accepts
**Actions:**
1. Check for newly accepted connections
2. Send Day 1 DM (the opener — asking what role they'd put an AI integrator in)
3. If no response after 3 days, send Day 2 follow-up (share a result/case study)
4. If no response after 5 more days, send Day 3 walk-away (no pressure, leave door open)
5. If they respond at any point, flag for human review (you take over the conversation)
**Safety:** Max 20 DMs/day total. Never double-message. If they say no or uninterested, stop immediately and log as "not interested."

### Skill 4: Facebook Group Engager
**Trigger:** Runs daily on schedule
**Actions:**
1. Navigate to prioritized Facebook groups (you'll provide the list)
2. Scroll recent posts, identify posts from potential ICP members
3. Like posts, leave genuine comments that start conversations
4. Identify commenters/likers on your own posts — add as friends
5. Track group engagement in persistent file
**Safety:** Max 20 comments/day. Vary comment style. Never pitch in comments. Always pull to DM.

### Skill 5: Facebook Friend + DM Engine
**Trigger:** Runs daily on schedule
**Actions:**
1. Send friend requests to people identified from group engagement
2. Check for accepted friend requests
3. Send opening DM to new friends (rapport-first, not pitch-first)
4. Follow up on open conversations
5. Flag warm leads for human takeover
**Safety:** Max 20 friend requests/day. Max 30 DMs/day. Randomize timing. If messenger gets paused, stop and retry next day.

### Skill 6: Facebook Group Poster
**Trigger:** Runs daily on schedule (different time per group)
**Actions:**
1. Create post for target group (rotating between Let's Get Connected, Ask/Engagement, and value posts)
2. Post to ONE group per day (never same post in multiple groups same day)
3. Monitor post for engagement over next 2-4 hours
4. Like + reply to every comment
5. Add engaged users to friend request queue
**Safety:** 1 group post/day max. Never duplicate exact post across groups.

### Skill 7: Instagram Engagement Engine
**Trigger:** Runs daily on schedule
**Actions:**
1. Navigate to target hashtags and profiles
2. Like and comment on posts from ICP-matching accounts
3. Follow relevant accounts
4. Engage with stories (reactions, replies)
5. DM new followers or engaged users
**Safety:** Max 50 follows/day. Max 20 comments/day. Max 30 DMs/day. Randomize everything.

### Skill 8: Cross-Platform Lead Tracker
**Trigger:** Runs after each platform skill completes
**Actions:**
1. Log all interactions (comments, DMs, connections, friend requests)
2. Track conversation stage (cold → warm → hot → booked)
3. Flag leads ready for human takeover
4. Generate daily summary report
**Safety:** Read-only analysis. No outbound actions.

### Skill 9: Comment Responder (All Platforms)
**Trigger:** Runs every 2-3 hours
**Actions:**
1. Check for new comments on your posts (LinkedIn, Facebook, Instagram)
2. Like each comment
3. Reply with a thoughtful response that opens a conversation loop
4. If commenter is new, add to connection/friend queue
**Safety:** Always reply genuinely. Never copy-paste responses. Vary language.

---

## DAILY SCHEDULE (Automated)

| Time | Platform | Skill | Action |
|------|----------|-------|--------|
| 7:00 AM | LinkedIn | Post | Publish daily content post |
| 7:30 AM | LinkedIn | Commenter | Engage with 15-20 posts |
| 8:00 AM | LinkedIn | Connector | Send 10 connection requests |
| 8:30 AM | LinkedIn | DM Sequence | Send/follow-up on DMs |
| 9:00 AM | Facebook | Group Poster | Post in 1 target group |
| 9:30 AM | Facebook | Group Engager | Comment on 15-20 posts |
| 10:00 AM | Facebook | Friend + DM | Send requests + DMs |
| 11:00 AM | Instagram | Engagement | Like, comment, follow |
| 11:30 AM | Instagram | DMs | Outreach to engaged users |
| 1:00 PM | All | Comment Responder | Reply to all new comments |
| 4:00 PM | All | Comment Responder | Reply to all new comments |
| 5:00 PM | All | Lead Tracker | Generate daily summary |
| 7:00 PM | All | Comment Responder | Final comment check |

**Total daily automated actions:** ~250-300 touches across 3 platforms
**Human time required:** ~30-60 min reviewing flagged leads and taking over warm conversations

---

## SAFETY & ANTI-DETECTION

### Platform-Specific Limits (Hard Caps)
| Platform | Friend/Connect | DMs | Comments | Likes | Posts |
|----------|---------------|-----|----------|-------|-------|
| LinkedIn | 10/day | 20/day | 20/day | 30/day | 1/day |
| Facebook | 20/day | 30/day | 20/day | 40/day | 1 group + 1 profile |
| Instagram | 50/day | 30/day | 20/day | 50/day | 1/day |

### Anti-Detection Measures
1. **Residential proxies** — Browser Use Cloud handles this. Each session routes through real residential IPs.
2. **Stealth browsers** — Anti-fingerprint browser profiles that look like real Chrome sessions.
3. **Randomized timing** — 1-5 minute random delays between actions. No robotic patterns.
4. **Session warmup** — Start slow (50% of limits for first week), ramp up gradually.
5. **Human-like scrolling** — Random scroll patterns, pauses, back-and-forth navigation.
6. **Persistent browser profiles** — Same profile per platform = consistent cookies, history, behavior.
7. **Activity variation** — Don't do the same sequence every day. Randomize order of actions.
8. **Emergency stop** — If any rate limit warning is detected, immediately stop all activity on that platform for 24 hours.

### Escalation Rules
- **If account gets warning:** Stop all automation on that platform for 48 hours. Resume at 50% volume.
- **If account gets restricted:** Stop all automation. Human reviews and adjusts strategy.
- **If account gets banned:** Do NOT try to work around it. Reassess approach entirely.

---

## CONTENT TEMPLATES

### LinkedIn Post Templates (Rotate Daily)
1. **Insight post:** "Most businesses buy AI tools and expect magic. The tool isn't the problem. The operator is. We started placing trained AI integrators into businesses because..."
2. **Question post:** "If you could hand off ONE task to someone who's already trained on AI — what would it be?"
3. **Result post:** "Last week we placed an AI integrator into a [industry] business. Within 14 days they cut admin time by 60%. Here's what we did..."
4. **Contrarian post:** "Hot take: You don't need more AI tools. You need someone who knows how to use the ones you already have."
5. **Story post:** "A business owner told me last month: 'I've spent $500/mo on AI subscriptions and nothing has changed.' The problem wasn't the AI..."

### Facebook Group Post Templates (Rotate)
1. **Let's Get Connected:** "Hey everyone! Let's get connected. What's your biggest time sink in your business right now? For us it's [relatable thing]. Drop yours below 👇"
2. **Ask/Engagement:** "Quick poll — how many hours a week do you spend on tasks that feel like they should be automated? Be honest 😅"
3. **Value post:** "3 things I wish every business owner knew about AI right now: 1) You don't need to learn to code. 2) The right person matters more than the right tool. 3) Start with ONE workflow, not everything."
4. **Soft CTA:** "We just put together something for business owners who want to bring AI into their operations but don't know where to start. If you're curious, drop a '🙋' below and I'll send you the details."

### DM Scripts

**LinkedIn — After Connection Accept:**
> "Hey {{firstName}}! Thanks for connecting. I checked out your profile — [specific observation]. Quick question: if someone showed up at {{companyName}} tomorrow, already trained on AI tools, and doubled one person's output in 30 days — what role would you put them in? That's what we do and I'm curious how it'd apply to your world."

**Facebook — After Friend Accept:**
> "Hey {{firstName}}! Thanks for the add. Saw you in [group name] — what do you do for work? Always looking to connect with other business-minded people in the community 🙂"

**Instagram — New Follower:**
> "Hey! Thanks for the follow 🙌 What caught your eye? Always curious what resonates with people."

**Follow-up (All Platforms) — 3 Days No Response:**
> "Hey {{firstName}} — no worries if you're slammed. Just wanted to share: we helped a [similar industry] business cut their admin workload in half last month using an AI integrator. If that's ever relevant for you, happy to chat."

**Walk-Away (All Platforms) — 8 Days No Response:**
> "Last ping from me! If you ever need help with AI in your business, I'm here. Good luck with everything at {{companyName}} 🤙"

---

## WHAT TO BUILD FIRST (Priority Order)

### Phase 1: Foundation (This Week)
1. ☐ Create Browser Use Cloud browser profiles for LinkedIn, Facebook, Instagram
2. ☐ Log into each account and save persistent sessions
3. ☐ Build Skill 1: LinkedIn Commenter (highest ROI, lowest risk)
4. ☐ Build Skill 9: Comment Responder (keeps conversations alive)
5. ☐ Test at 50% volume for 3 days

### Phase 2: Outreach (Week 2)
6. ☐ Build Skill 2: LinkedIn Connector
7. ☐ Build Skill 3: LinkedIn DM Sequence
8. ☐ Build Skill 5: Facebook Friend + DM Engine
9. ☐ Ramp to 75% volume

### Phase 3: Content + Groups (Week 3)
10. ☐ Build Skill 4: Facebook Group Engager
11. ☐ Build Skill 6: Facebook Group Poster
12. ☐ Build Skill 7: Instagram Engagement Engine
13. ☐ Ramp to 100% volume

### Phase 4: Intelligence (Week 4)
14. ☐ Build Skill 8: Cross-Platform Lead Tracker
15. ☐ Set up daily summary reports
16. ☐ Build scheduling for all skills
17. ☐ Full autopilot mode

---

## EXPECTED RESULTS (Conservative)

### Monthly Output at Full Volume
| Metric | LinkedIn | Facebook | Instagram | Total |
|--------|----------|----------|-----------|-------|
| Connections/Friends | 300 | 600 | 1,500 | 2,400 |
| DMs Sent | 600 | 900 | 900 | 2,400 |
| Comments | 600 | 600 | 600 | 1,800 |
| Posts | 30 | 60 | 30 | 120 |

### Conversion Funnel (Conservative)
- 2,400 DMs sent/month
- 10-15% response rate = 240-360 conversations
- 20% qualify as warm leads = 48-72 warm leads
- 30% book a call = 14-22 warm-up calls/month
- 33% close rate = 5-7 new clients/month
- At $1,000 average front-end = **$5,000-$7,000/month new revenue**
- Plus $300/mo recurring per client = **compounding MRR**

### By Month 3 (if consistent)
- Network: 5,000-7,000 new connections across platforms
- Pipeline: 40-60 warm leads/month
- Revenue: $5-10K/month front-end + $3-6K MRR
- **Your time:** 30-60 min/day reviewing leads and closing

---

## COST ESTIMATE

### Browser Use Cloud
- ~$0.02-0.05 per task action
- ~300 actions/day = $6-15/day = **$180-$450/month**
- Skills (once built) are cheaper — deterministic, no AI inference per run

### Browser Use Local (Alternative for some tasks)
- Free (runs on your Mac)
- Good for: content posting, comment responding, non-stealth tasks
- Not ideal for: LinkedIn/Facebook (no residential proxies, easier to detect)

### Recommended Mix
- **Cloud:** LinkedIn + Facebook (need stealth + proxies) — ~$300/month
- **Local:** Instagram engagement, lead tracking, report generation — $0
- **Total estimated cost: ~$300-400/month**

---

## WHAT I NEED FROM YOU TO START

1. **LinkedIn login credentials** (email + password)
2. **Facebook login credentials** (email + password)
3. **Instagram login credentials** (email + password)
4. **List of 5-10 Facebook groups** you're already in or want to join
5. **5-10 LinkedIn influencers/accounts** in your space to mine engagement from
6. **Your profile URLs** for all 3 platforms
7. **Any 2FA setup** — we'll need to handle this for browser profiles
8. **Approval on the DM scripts and comment templates above** (or your edits)
