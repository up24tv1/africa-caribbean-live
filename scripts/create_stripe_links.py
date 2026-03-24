"""
Create Stripe Payment Links for Africa x Caribbean Live watch room tiers.
Reads STRIPE_SECRET_KEY from worldcup-x-agent/.env automatically.
Run: python -X utf8 scripts/create_stripe_links.py
"""
import os, sys, json
from pathlib import Path

# Load .env from worldcup-x-agent
env_path = Path(__file__).parent.parent.parent / "worldcup-x-agent" / ".env"
if env_path.exists():
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

import stripe

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
if not stripe.api_key:
    print("ERROR: STRIPE_SECRET_KEY not found in environment or .env")
    sys.exit(1)

# The Vercel deployment URL — update after first deploy
SUCCESS_URL = os.environ.get(
    "STRIPE_SUCCESS_URL", "https://africa-caribbean-live.vercel.app/success"
)

TIERS = [
    {
        "name": "Africa x Caribbean Live — Supporter",
        "price_cents": 100,
        "description": "Access the global watch room, text channels, and voice rooms.",
    },
    {
        "name": "Africa x Caribbean Live — Super Fan",
        "price_cents": 300,
        "description": "Full access + highlighted role and prediction game entry.",
    },
    {
        "name": "Africa x Caribbean Live — Fam",
        "price_cents": 500,
        "description": "Full access + halftime stage priority and pinned shoutout.",
    },
    {
        "name": "Africa x Caribbean Live — Captain",
        "price_cents": 1000,
        "description": "Full access + Donation Wall feature, digital badge, and free next event.",
    },
]

print("Creating Stripe Payment Links for Africa x Caribbean Live...\n")

links = {}
for tier in TIERS:
    # Create a product
    product = stripe.Product.create(
        name=tier["name"],
        description=tier["description"],
    )
    print(f"Created product: {product.name} ({product.id})")

    # Create a price
    price = stripe.Price.create(
        product=product.id,
        unit_amount=tier["price_cents"],
        currency="usd",
    )
    print(f"  Price: ${tier['price_cents']/100:.2f} ({price.id})")

    # Create a payment link with success redirect
    payment_link = stripe.PaymentLink.create(
        line_items=[{"price": price.id, "quantity": 1}],
        after_completion={
            "type": "redirect",
            "redirect": {"url": SUCCESS_URL},
        },
    )
    print(f"  Payment Link: {payment_link.url}\n")

    # Extract tier key
    tier_key = tier["name"].split("—")[1].strip().lower().replace(" ", "_")
    links[tier_key] = {
        "url": payment_link.url,
        "product_id": product.id,
        "price_id": price.id,
        "amount_cents": tier["price_cents"],
    }

# Save links to file
output_path = Path(__file__).parent.parent / "stripe_links.json"
with open(output_path, "w") as f:
    json.dump(links, f, indent=2)

print(f"Links saved to {output_path}")
print("\nDone! Update PaySection.tsx with these links, or set them in .env.local.")
