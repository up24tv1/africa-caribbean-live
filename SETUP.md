# Africa x Caribbean Live — Setup Guide

## Quick Deploy (3 steps)

### 1. Deploy to Vercel
Double-click `deploy.bat` or run:
```bash
cd africa-caribbean-live
npx vercel login     # Opens browser to authenticate
npx vercel --yes --prod
```

### 2. Create Stripe Payment Links
Go to https://dashboard.stripe.com/payment-links and create 4 links:
- **Supporter** — $1.00
- **Super Fan** — $3.00
- **Fam** — $5.00
- **Captain** — $10.00

For each link, set "After payment" → Redirect to: `https://YOUR-VERCEL-URL/success`

Then update `app/components/PaySection.tsx` — replace the `link: "#"` values with your Stripe Payment Link URLs.

OR run the script (needs STRIPE_SECRET_KEY in worldcup-x-agent/.env):
```bash
python -X utf8 scripts/create_stripe_links.py
```

### 3. Set Up Discord
1. Create server → Enable Community
2. Create Stage Channel: "The Stadium"
3. Voice rooms: Jamaica Room, DR Congo Room, Neutral Room
4. Text channels: #welcome, #matchday-live, #predictions, #prove-your-country, #memes-and-banter
5. Roles: Supporter, Super Fan, Fam, Captain + country roles
6. Create Scheduled Event for March 26 match
7. Generate invite link → Set as NEXT_PUBLIC_DISCORD_INVITE_URL in Vercel env vars

### 4. Redeploy
After updating Stripe links and env vars:
```bash
npx vercel --prod
```
