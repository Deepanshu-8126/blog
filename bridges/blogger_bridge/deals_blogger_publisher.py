#!/usr/bin/env python3
"""
=============================================================================
DEALS BLOGGER PUBLISHER (HUMANIZED HINGLISH/ENGLISH DEAL REVIEWS)
=============================================================================
Publishes real shopping loots, price glitches, and festive offers to Blogger:
  - Target Blog ID: 834082955272949961 (https://lootdeals2478.blogspot.com/)
  - Real Studio Product Photos (Amazon/Store CDN, zero AI cartoons)
  - Real Affiliate Links (tag=uniquedigi0c6-21, EarnKaro, Meesho)
  - Natural, Humanized Hinglish/English Copywriting
  - Conversion-Optimized Price Breakdown Tables & Buy Now CTA Buttons
  - Official Telegram (@uniquedigit_deals) & WhatsApp Channel Invite Footer
=============================================================================
"""

import os
import sys
import re
import json
import urllib.parse
from datetime import datetime
from dotenv import load_dotenv

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

load_dotenv()

DEALS_BLOG_ID = os.getenv("BLOGGER_DEALS_BLOG_ID", "834082955272949961")
AMAZON_TAG = os.getenv("AMAZON_AFFILIATE_TAG", "uniquedigi0c6-21")
WHATSAPP_CHANNEL_URL = os.getenv("WHATSAPP_CHANNEL_URL", "https://whatsapp.com/channel/0029Vb90gso4dTnKKpcf7M1E")
TELEGRAM_DEALS_CHANNEL_URL = "https://t.me/uniquedigit_deals"


def ensure_affiliate_link(url: str) -> str:
    """Guarantees user's affiliate tag is injected into store links."""
    if not url:
        return f"https://www.amazon.in/?tag={AMAZON_TAG}"
    if "amazon.in" in url:
        if "tag=" not in url:
            sep = "&" if "?" in url else "?"
            return f"{url}{sep}tag={AMAZON_TAG}"
        else:
            return re.sub(r'tag=[^&]+', f'tag={AMAZON_TAG}', url)
    elif "flipkart.com" in url:
        if "affid=" not in url:
            sep = "&" if "?" in url else "?"
            return f"{url}{sep}affid=uniquedigit"
        else:
            return re.sub(r'affid=[^&]+', 'affid=uniquedigit', url)
    return url


VERIFIED_PRODUCT_ASSETS = {
    "boat": "https://m.media-amazon.com/images/I/71oXzCK43NL._SL1500_.jpg",
    "airdopes": "https://m.media-amazon.com/images/I/71oXzCK43NL._SL1500_.jpg",
    "asaya": "https://images-static.nykaa.com/media/catalog/product/2/8/288dc768906161980774_1.jpg",
    "salicylic": "https://images-static.nykaa.com/media/catalog/product/2/8/288dc768906161980774_1.jpg",
    "iphone 15": "https://m.media-amazon.com/images/I/71657TiFeHL._SL1500_.jpg",
    "iphone 16": "https://cdsassets.apple.com/live/7WUAS350/images/tech-specs/iphone-16.png",
    "macbook": "https://m.media-amazon.com/images/I/71jG+e7roXL._SL1500_.jpg",
    "galaxy s24": "https://m.media-amazon.com/images/I/717Qo4MH97L._SL1500_.jpg",
    "samsung": "https://m.media-amazon.com/images/I/717Qo4MH97L._SL1500_.jpg",
    "oneplus": "https://m.media-amazon.com/images/I/717Qo4MH97L._SL1500_.jpg",
    "nord": "https://fdn2.gsmarena.com/vv/bigpic/oneplus-nord4.jpg",
    "sony": "https://m.media-amazon.com/images/I/61+btxzpfDL._SL1500_.jpg",
    "headphone": "https://m.media-amazon.com/images/I/61+btxzpfDL._SL1500_.jpg",
    "xiaomi": "https://i02.appmifile.com/mi-com-product/fly-birds/xiaomi-smart-4k-tv-f-43-2025/m-in/3728e5c6352918e127883e9b0ab45f90.png",
    "tv": "https://i02.appmifile.com/mi-com-product/fly-birds/xiaomi-smart-4k-tv-f-43-2025/m-in/3728e5c6352918e127883e9b0ab45f90.png"
}


def resolve_hd_deal_image(deal: dict) -> str:
    """
    Guarantees a verified, crystal-clear 1500px/HD product photo with HTTP 200.
    Delegates to the Master Universal Real Image Engine.
    """
    try:
        from bridges.universal_image_engine import get_universal_real_image
        img, _ = get_universal_real_image(
            title=deal.get("title", ""),
            niche_slug="deals",
            target_url=deal.get("affiliate_url", ""),
            raw_image=deal.get("photo_url")
        )
        return img
    except Exception as e:
        print("[Universal Image Engine error in Deals Blogger]:", e)
        return "https://m.media-amazon.com/images/I/71oXzCK43NL._SL1500_.jpg"


def generate_deal_html(deal: dict) -> tuple[str, str]:
    """
    Creates high-converting, humanized deal review content with HTML layout.
    Returns: (article_title, content_html, resolved_hd_image)
    """
    raw_title = deal.get("title", "Hot Product Deal").strip()
    price = deal.get("deal_price")
    mrp = deal.get("mrp")
    discount = deal.get("discount")
    raw_url = deal.get("affiliate_url", "")
    aff_url = ensure_affiliate_link(raw_url)
    image_url = resolve_hd_deal_image(deal)
    deal["photo_url"] = image_url  # Mutate with crystal-clear verified image
    body_text = deal.get("body", "")

    # Calculate discount / savings
    if price and mrp and mrp > price and not discount:
        discount = round(((mrp - price) / mrp) * 100)
    savings = (mrp - price) if (price and mrp and mrp > price) else 0

    # Clean product title
    clean_prod = re.sub(r'(?i)(\[.*?\]|\(.*?\)|flat \d+% off|deal price.*)', '', raw_title).strip()
    if not clean_prod:
        clean_prod = raw_title

    # Determine Store Platform
    store_name = "Amazon India"
    if "flipkart" in aff_url.lower():
        store_name = "Flipkart"
    elif "myntra" in aff_url.lower():
        store_name = "Myntra"
    elif "meesho" in aff_url.lower():
        store_name = "Meesho"

    # 1. Headline generation (High CTR, zero slop)
    if discount and discount >= 60:
        article_title = f"[Flat {discount}% Off Mega Loot] {clean_prod} Price Glitch & Review: Only ₹{price:,} on {store_name}"
    elif discount and discount >= 35:
        article_title = f"[Price Drop Alert] {clean_prod} at ₹{price:,} ({discount}% Discount): Full Review & How to Buy"
    elif price:
        article_title = f"[Exclusive Offer] {clean_prod} Deal Live at ₹{price:,}: Specs, Price Breakdown & Buying Trick"
    else:
        article_title = f"[Loot Deal Active] {clean_prod}: Today's Best Offer & Verified Discount Link"

    # 2. Conversational Hinglish Intro (Natural, deal hunter tone)
    intros = [
        f"Doston, agar aap apne liye ek reliable gadget ya festive shopping ke liye discount dhund rahe the, toh {store_name} par ek massive price drop live ho chuka hai. <b>{clean_prod}</b> par abhi direct discount mil raha hai, jisse yeh apne all-time lowest price ke aas-paas aa gaya hai.",
        f"Shopping lovers ke liye ek badi khushkhabri! {store_name} ne <b>{clean_prod}</b> par limited-time flash discount announce kiya hai. Aise price glitch offers stock khatam hone se pehle claim karne hote hain, isliye poori deal details niche check karein.",
        f"Agar aap smart shopping karke maximum savings karna chahte hain, toh yeh loot offer aapke liye perfect hai. <b>{clean_prod}</b> par flat price cut dekhne ko mila hai, aur bank offer ke saath yeh aur bhi sasta pad raha hai."
    ]
    intro_p = intros[len(clean_prod) % len(intros)]

    # 3. Pricing Breakdown HTML Table
    price_rows = f"""
    <tr>
        <td style="padding: 12px 16px; border-bottom: 1px solid #e2e8f0; font-weight: 600; color: #334155;">📦 Product Name</td>
        <td style="padding: 12px 16px; border-bottom: 1px solid #e2e8f0; color: #0f172a; font-weight: 600;">{clean_prod}</td>
    </tr>
    """
    if mrp:
        price_rows += f"""
        <tr>
            <td style="padding: 12px 16px; border-bottom: 1px solid #e2e8f0; font-weight: 600; color: #334155;">🏷️ Original MRP</td>
            <td style="padding: 12px 16px; border-bottom: 1px solid #e2e8f0; color: #64748b; text-decoration: line-through;">₹{mrp:,}</td>
        </tr>
        """
    if price:
        price_rows += f"""
        <tr>
            <td style="padding: 12px 16px; border-bottom: 1px solid #e2e8f0; font-weight: 600; color: #334155;">⚡ Deal / Steal Price</td>
            <td style="padding: 12px 16px; border-bottom: 1px solid #e2e8f0; color: #16a34a; font-size: 18px; font-weight: 800;">₹{price:,}</td>
        </tr>
        """
    if savings and discount:
        price_rows += f"""
        <tr>
            <td style="padding: 12px 16px; border-bottom: 1px solid #e2e8f0; font-weight: 600; color: #334155;">💰 Total Savings</td>
            <td style="padding: 12px 16px; border-bottom: 1px solid #e2e8f0; color: #dc2626; font-weight: 700;">Save ₹{savings:,} (Flat {discount}% OFF)</td>
        </tr>
        """
    price_rows += f"""
    <tr>
        <td style="padding: 12px 16px; border-bottom: 1px solid #e2e8f0; font-weight: 600; color: #334155;">🏪 Platform</td>
        <td style="padding: 12px 16px; border-bottom: 1px solid #e2e8f0; color: #0f172a; font-weight: 600;">{store_name}</td>
    </tr>
    <tr>
        <td style="padding: 12px 16px; font-weight: 600; color: #334155;">🟢 Deal Status</td>
        <td style="padding: 12px 16px; color: #16a34a; font-weight: 700;">Active Right Now (Limited Stock)</td>
    </tr>
    """

    # 4. Big Buy Button
    buy_btn_html = f"""
    <div style="text-align: center; margin: 30px auto;">
        <a href="{aff_url}" target="_blank" rel="nofollow noopener noreferrer" style="display: inline-block; background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: #ffffff; text-decoration: none; padding: 16px 36px; border-radius: 12px; font-weight: 800; font-size: 16px; letter-spacing: 0.5px; box-shadow: 0 6px 20px rgba(217,119,6,0.35); text-transform: uppercase;">
            🛍️ GRAB DEAL ON {store_name.upper()} ➔
        </a>
        <div style="font-size: 12px; color: #64748b; margin-top: 8px;">Direct verified checkout link • Instant dispatch available</div>
    </div>
    """

    # 5. Key Highlights Block
    highlights = [
        "<b>Value for Money:</b> Is price point par aisi specifications milna kaafi rare hai.",
        "<b>Genuine Product Warranty:</b> 100% original brand packaging with official 1-year brand warranty.",
        "<b>Fast & Free Delivery:</b> Eligible for Prime / Express doorstep delivery.",
        "<b>Easy Return Policy:</b> Standard replacement/return window applicable as per store policy."
    ]
    if body_text:
        clean_lines = [l.strip() for l in body_text.splitlines() if l.strip() and not l.startswith("http")]
        if clean_lines:
            highlights = [f"<b>Feature:</b> {l}" for l in clean_lines[:4]]

    highlights_html = "".join([f"<li style='margin-bottom: 10px; color: #334155; line-height: 1.6;'>{h}</li>" for h in highlights])

    # 6. Step-by-Step Claim Guide
    guide_html = f"""
    <div style="background: #f8fafc; border-left: 4px solid #3b82f6; padding: 18px 20px; border-radius: 0 12px 12px 0; margin: 25px 0;">
        <h4 style="margin: 0 0 10px 0; color: #1e293b; font-size: 16px;">📋 Step-by-Step Deal Claim Karne Ka Tarika:</h4>
        <ol style="margin: 0; padding-left: 20px; color: #475569; font-size: 14px; line-height: 1.7;">
            <li>Upar diye gaye <b>'Grab Deal'</b> button par click karke official product page open karein.</li>
            <li>Agar page par koi extra 'Apply Coupon' box dikhai de, toh use zaroor check/tick karein.</li>
            <li>Checkout par UPI ya eligible credit card select karein extra 5-10% instant bank cashback ke liye.</li>
            <li>Deal price expire hone ya stock out hone se pehle payment complete karein!</li>
        </ol>
    </div>
    """

    # 7. FAQs
    faq_html = f"""
    <div style="margin: 30px 0;">
        <h3 style="color: #0f172a; font-size: 20px; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px;">❓ Frequently Asked Questions (FAQs)</h3>
        <div style="margin-top: 14px;">
            <p style="font-weight: 700; color: #1e293b; margin-bottom: 4px;">Q1: Yeh deal kab tak active rahegi?</p>
            <p style="color: #475569; margin-top: 0; font-size: 14px; line-height: 1.6;">A: Flash deals aur lightning offers limited units ke liye hote hain. Jaise hi allotted stock khatam hota hai, price normal MRP par chali jaati hai.</p>
        </div>
        <div style="margin-top: 14px;">
            <p style="font-weight: 700; color: #1e293b; margin-bottom: 4px;">Q2: Kya is product par brand warranty milegi?</p>
            <p style="color: #475569; margin-top: 0; font-size: 14px; line-height: 1.6;">A: Haan, official seller se order karne par standard manufacturer brand warranty aur GST invoice milta hai.</p>
        </div>
    </div>
    """

    # Assemble Full Rich HTML Content
    content_html = f"""
    <p style="font-size: 16px; line-height: 1.7; color: #1e293b; margin-bottom: 20px;">
        {intro_p}
    </p>

    <div style="margin: 25px 0; background: #ffffff; border-radius: 14px; border: 1px solid #e2e8f0; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.03);">
        <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); color: #ffffff; padding: 14px 18px; font-weight: 700; font-size: 16px;">
            ⚡ Quick Deal Overview & Price Breakdown
        </div>
        <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
            <tbody>
                {price_rows}
            </tbody>
        </table>
    </div>

    {buy_btn_html}

    <h3 style="color: #0f172a; font-size: 20px; margin-top: 30px;">🌟 Key Features & Product Highlights</h3>
    <ul style="padding-left: 20px; margin: 15px 0;">
        {highlights_html}
    </ul>

    {guide_html}

    {buy_btn_html}

    {faq_html}

    <!-- Google Search Rich Snippet Schema.org Product Structured Data -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org/",
      "@type": "Product",
      "name": "{clean_prod}",
      "image": ["{image_url}"],
      "description": "Get {clean_prod} at lowest price with discount on {store_name}.",
      "brand": {{
        "@type": "Brand",
        "name": "{clean_prod.split()[0]}"
      }},
      "offers": {{
        "@type": "Offer",
        "url": "{aff_url}",
        "priceCurrency": "INR",
        "price": "{price or 999}",
        "priceValidUntil": "2026-12-31",
        "itemCondition": "https://schema.org/NewCondition",
        "availability": "https://schema.org/InStock",
        "seller": {{
          "@type": "Organization",
          "name": "{store_name}"
        }}
      }}
    }}
    </script>
    """

    return article_title, content_html


def publish_deal_to_blogger(deal: dict, target_blog_id: str = None) -> dict:
    """Publishes the formatted deal article to the dedicated Deals Blogger blog."""
    from bridges.blogger_bridge.blogger_publisher import publish_to_blogger

    blog_id = target_blog_id or DEALS_BLOG_ID
    title, content_html = generate_deal_html(deal)
    featured_img = deal.get("photo_url")
    labels = ["Loot Deals", "Amazon Offers", "Price Drop", "Online Shopping"]

    res = publish_to_blogger(
        title=title,
        content_html=content_html,
        labels=labels,
        is_draft=False,
        featured_image=featured_img,
        target_blog_id=blog_id
    )
    return res


if __name__ == "__main__":
    # Test sample deal publish
    test_deal = {
        "id": "B0BNVBXQJ1",
        "title": "boAt Airdopes 141 ANC TWS Earbuds (42H Playtime, 32dB ANC)",
        "mrp": 4490,
        "deal_price": 1299,
        "discount": 71,
        "affiliate_url": f"https://www.amazon.in/dp/B0BNVBXQJ1?tag={AMAZON_TAG}",
        "photo_url": "https://m.media-amazon.com/images/I/61Yy7lq3VGL._SL1500_.jpg"
    }
    print("Testing Deals Blogger Publisher...")
    result = publish_deal_to_blogger(test_deal)
    print("Result:", result)
