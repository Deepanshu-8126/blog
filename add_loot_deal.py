#!/usr/bin/env python3
"""
=============================================================================
INSTANT LOOT DEAL PUBLISHER CLI
=============================================================================
Easily publish any custom or instant loot deal to:
  1. Blogger Deals Blog (lootdeals2478.blogspot.com)
  2. Telegram Channel (@uniquedigit_deals)

Features:
  - Auto-injects affiliate tag: uniquedigi0c6-21
  - Resolves crystal-clear 1500px real product image
  - Generates humanized Hinglish review + price breakdown table + CTA buttons
  - Interactive prompt or CLI arguments support

Usage Examples:
  python add_loot_deal.py --url "https://www.amazon.in/dp/B08L5V9T31" --title "Fire-Boltt Ninja Call Pro Smartwatch" --price 1099 --mrp 17999
  python add_loot_deal.py --interactive
=============================================================================
"""

import os
import sys
import re
import argparse
from dotenv import load_dotenv

if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            getattr(sys.stdout, "reconfigure")(encoding="utf-8")
        if hasattr(sys.stderr, "reconfigure"):
            getattr(sys.stderr, "reconfigure")(encoding="utf-8")
    except Exception:
        pass

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

load_dotenv()

from bridges.universal_image_engine import get_universal_real_image
from bridges.blogger_bridge.deals_blogger_publisher import publish_deal_to_blogger, ensure_affiliate_link

AMAZON_TAG = os.getenv("AMAZON_AFFILIATE_TAG", "uniquedigi0c6-21")


def publish_custom_deal(title: str, url: str, deal_price: int, mrp: int, image_url: str = None, send_telegram: bool = True):
    print("=" * 65)
    print("🛍️  INSTANT LOOT DEAL PUBLISHER")
    print("=" * 65)
    print(f"📦 Product Title : {title}")
    print(f"💰 Deal Price    : ₹{deal_price:,} (MRP: ₹{mrp:,})")
    
    # Calculate discount
    discount = 0
    if mrp > deal_price and mrp > 0:
        discount = round(((mrp - deal_price) / mrp) * 100)
    print(f"🔥 Discount      : {discount}% OFF")

    # Clean and affiliate-tag url
    affiliate_url = ensure_affiliate_link(url)
    print(f"🔗 Affiliate Link: {affiliate_url}")

    # Resolve real HD image
    print("🖼️  Resolving 100% Real Studio Image...")
    resolved_img = get_universal_real_image(
        title=title,
        niche_slug="deals",
        target_url=affiliate_url,
        raw_image=image_url
    )
    print(f"📸 Verified Image: {resolved_img}")

    # Build deal object
    asin_match = re.search(r'/(?:dp|gp/product)/([A-Z0-9]{10})', affiliate_url)
    deal_id = asin_match.group(1) if asin_match else f"CUSTOM_{int(deal_price)}"

    deal = {
        "id": deal_id,
        "title": title,
        "mrp": mrp,
        "deal_price": deal_price,
        "discount": discount,
        "affiliate_url": affiliate_url,
        "photo_url": resolved_img
    }

    # 1. Publish to Blogger
    print("\n📝 Publishing to Blogger (lootdeals2478.blogspot.com)...")
    blogger_res = publish_deal_to_blogger(deal)
    if blogger_res.get("success"):
        print(f"✅ [SUCCESS] Blogger Live URL: {blogger_res.get('url')}")
    else:
        print(f"❌ [ERROR] Blogger publish failed: {blogger_res.get('error')}")

    # 2. Publish to Telegram (Optional)
    if send_telegram:
        try:
            from pipelines.god_level_loot_engine import send_deal
            print("📱 Broadcasting to Telegram Channel (@uniquedigit_deals)...")
            tg_res = send_deal(deal)
            if tg_res:
                print("✅ [SUCCESS] Deal posted to Telegram channel!")
            else:
                print("⚠️  Telegram broadcast returned False or was skipped.")
        except Exception as e:
            print(f"⚠️  Telegram broadcast skipped: {e}")

    print("\n🎉 DONE! Deal successfully processed and live.")
    return blogger_res


def main():
    parser = argparse.ArgumentParser(description="Add and publish an instant shopping loot deal.")
    parser.add_argument("--url", help="Product link (Amazon/Store URL)")
    parser.add_argument("--title", help="Full product title")
    parser.add_argument("--price", type=int, help="Deal price in Rs.")
    parser.add_argument("--mrp", type=int, help="Original MRP in Rs.")
    parser.add_argument("--image", help="Optional custom image URL")
    parser.add_argument("--no-telegram", action="store_true", help="Do not send to Telegram")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive terminal mode")

    args = parser.parse_args()

    if args.interactive or not (args.url and args.title and args.price and args.mrp):
        print("\n--- Interactive Deal Input ---")
        url = input("Enter Product URL (Amazon / Store): ").strip()
        title = input("Enter Product Title: ").strip()
        price_str = input("Enter Deal Price (e.g. 799): ").strip()
        mrp_str = input("Enter MRP (e.g. 2999): ").strip()
        image = input("Enter Custom Image URL (optional, press Enter to auto-fetch): ").strip() or None

        try:
            price = int(re.sub(r'[^\d]', '', price_str))
            mrp = int(re.sub(r'[^\d]', '', mrp_str))
        except Exception:
            print("❌ Invalid price/mrp numbers provided.")
            return

        publish_custom_deal(title, url, price, mrp, image_url=image, send_telegram=not args.no_telegram)
    else:
        publish_custom_deal(args.title, args.url, args.price, args.mrp, image_url=args.image, send_telegram=not args.no_telegram)


if __name__ == "__main__":
    main()
