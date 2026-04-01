# Troubleshooting Guide

Common issues and how to fix them.

---

## Craigslist

### "My ad was ghosted" (posted but invisible to others)
**Symptoms:** Ad shows in your CL account but doesn't appear in search results.
**Cause:** CL detected something suspicious — shared IP, similar content, or bot behavior.
**Fix:**
1. Run the ghost checker: `python automation/craigslist/ghost_check.py --search`
2. If ghosted, rewrite the ad completely (new title, new body, different photos)
3. Post from a different account with a different ISP proxy
4. Wait 24 hours before reposting in the same category

### "My ad was flagged"
**Cause:** Other CL users flagged your ad, or CL's automated system detected a violation.
**Fix:**
1. Don't repost the exact same ad — change everything
2. Check if your ad sounds too spammy or has duplicate content from another ad
3. Vary your posting times and ad structure
4. Consider using a posting service (CL Dominator) instead of DIY

### "Login failed / captcha / phone verification"
**Cause:** CL detected automation or suspicious login.
**Fix:**
1. Log in manually from the same browser profile to clear the captcha
2. Complete any phone verification CL asks for
3. Use GoLogin/AdsPower browser profiles (not raw Playwright)
4. Make sure your proxy IP matches your account's registered location

### "I'm getting charged $5 but ads aren't going live"
**Cause:** CL charges the posting fee even if the ad gets immediately removed.
**Fix:**
1. Check your email — CL sends a confirmation link. Did you click it?
2. Run the ghost checker to verify ad visibility
3. If ads keep dying immediately, your account or IP may be burned
4. Switch to a posting service until you get fresh accounts/IPs

### "How many ads can I post per day?"
- **Per account:** Max 3 in services categories. Pushing past 3 risks flags.
- **Total with 3 accounts:** 7-9 ads/day safely
- **Rule of thumb:** 1 ad per category per city per 48 hours per account
- **Space them out:** 10-30 minutes between posts, randomized

---

## Call Tracking

### "Calls aren't being recorded"
1. Log into AvidTrak (or your provider) and check recording settings
2. Make sure recording is enabled for the tracking number
3. Some states require two-party consent for recording — check your state's laws
4. Test: Call your tracking number from a different phone

### "I don't know which ad generated a call"
1. If using one number on all ads: you can't tell which ad. This is why we recommend separate numbers per service (or at minimum, use UTM parameters in your ad URLs)
2. Upgrade: Get separate tracking numbers per service category ($2-3/number extra on AvidTrak)
3. Ask the caller: "How did you hear about us?" — simple but effective

### "Calls aren't forwarding to my phone"
1. Check forwarding settings in your tracking provider dashboard
2. Make sure the destination phone number is correct (no typos)
3. Check if your cell phone has Do Not Disturb enabled
4. Test: Call tracking number from another phone

---

## Facebook Marketplace

### "My listing was removed"
**Cause:** FB detected it as a service (not a product).
**Fix:**
1. Don't repost the same listing — change the title, photos, and description
2. Frame it as a product: "Gift Certificate," "Maintenance Package," "Repair Kit"
3. Post from your phone app (longer survival than desktop)
4. Don't use the word "service" in the title
5. Wait 24 hours before posting again

### "I'm not getting messages on my listings"
1. Check that Marketplace messaging is enabled in your FB settings
2. Make sure your listing price isn't too high (free and low-price listings get more engagement)
3. Post in Classifieds > Miscellaneous (less enforcement)
4. Include clear photos — listings with good photos get 3-5x more responses

### "My account got restricted from Marketplace"
**Cause:** Too many listings removed, or posting too fast on a new account.
**Fix:**
1. Wait. Restrictions usually lift in 1-7 days
2. Don't create a new FB account — it will get flagged faster
3. When restriction lifts, post slowly: max 1 listing/day for 2 weeks
4. Use the gift certificate method (safest approach)

---

## Posting Agent (DIY Automation)

### "Playwright install failed"
```bash
pip install playwright
playwright install chromium
```
If it fails on Mac: `xcode-select --install` first.

### "GoLogin API not connecting"
1. Check your API token: `GOLOGIN_API_TOKEN` in `.env`
2. Make sure your GoLogin subscription is active
3. Try starting a profile manually in the GoLogin desktop app first
4. Check if your GoLogin profile has a proxy assigned

### "Proxy connection failed"
1. Run the proxy tester: `python automation/scripts/test_proxy.py`
2. Check proxy credentials in `.env` (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)
3. ISP proxies sometimes go down — check your provider's dashboard
4. Try a different proxy IP if the current one is burned

### "The script crashes mid-post"
1. Check `automation/logs/` for error details
2. CL may have changed their page layout — selectors might need updating
3. Run with `--test` to see the browser and identify where it fails
4. Take a screenshot of the error state and share it

---

## Setup Issues

### "wizard.py won't run"
```bash
python3 setup/wizard.py
```
Make sure you're running Python 3.8+: `python3 --version`

### ".env file not found"
```bash
cp automation/.env.example automation/.env
```
Then edit `.env` with your info, or run `python setup/wizard.py` to generate it.

### "settings.yaml is wrong"
Run the setup wizard again: `python setup/wizard.py`
Or edit `automation/config/settings.yaml` directly.

---

## General

### "I'm not getting any leads"
1. Check that your ads are actually live (not ghosted): `python automation/craigslist/ghost_check.py`
2. Check that your tracking number is forwarding correctly
3. Check CL email — leads may be going to your CL email inbox
4. Check FB messages — Marketplace inquiries go there
5. Are you in a competitive market? You may need more ads (increase from 3 to 5-7 days/week)
6. Review your ad copy — is the phone number at the top AND bottom?

### "I'm spending money but not booking jobs"
1. Are you responding fast enough? First responder wins. Under 5 minutes.
2. Are you answering professionally? Practice your phone script.
3. Are your prices competitive for your market? Check competitors on CL.
4. Are you showing up reliably? No-shows kill your reputation fast.

### "How do I track my leads and revenue?"
1. Start simple: Google Sheets with columns: Date, Source, Name, Phone, Service, Status, Revenue
2. The automation tracks ads and leads in `automation/data/leads.db` (SQLite)
3. Upgrade later: ClickUp or similar project management tool
