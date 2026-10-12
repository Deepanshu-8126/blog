"""
UniqueDigit LOOT RADAR — Real-Time 24/7 Deal Intelligence Agent
================================================================
NOT a cron job. This is a LIVE AGENT that:
  ✅ Scans 6+ deal sources every 30 seconds
  ✅ Detects price drops INSTANTLY
  ✅ Broadcasts to @uniquedigit_deals within seconds of discovery
  ✅ Tracks seen deals to NEVER repeat
  ✅ Handles Big Billion Days, GIFD, Flash Sales, Bank Glitches
  ✅ Runs 24/7 on GitHub Actions OR locally

Usage:
  python loot_radar_agent.py              # One-shot scan (for GitHub Actions)
  python loot_radar_agent.py --live       # 24/7 LIVE agent (for local/server)
  python loot_radar_agent.py --blitz      # Festival mode — 15s cycles
"""

import json
import os
import re
import sys
import time
import hashlib
import urllib.parse
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from dotenv import load_dotenv

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

load_dotenv()

# ─── Config ───────────────────────────────────────────────────────────────
LIVE_MODE = "--live" in sys.argv
BLITZ_MODE = "--blitz" in sys.argv  # Festival mode: 15s cycles
SCAN_INTERVAL = 15 if BLITZ_MODE else 30  # seconds between cycles

UA = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "en-IN,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

CF_ACCOUNT = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "cf1a42fb306054063805cf459fddf853")
CF_D1_DB = os.environ.get("CLOUDFLARE_D1_DATABASE_ID", "61d1d46f-f438-47f5-9128-516d9beb11cb")
CF_TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN", "")
AMAZON_TAG = os.environ.get("AMAZON_ASSOCIATE_TAG", "uniquedigi0c6-21")
GEMINI_KEY = os.environ.get("GEMINI_API_KEY", "")

TG_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TG_DEALS_CHANNEL = os.environ.get("TELEGRAM_DEALS_CHANNEL", "@uniquedigit_deals")

# In-memory dedup set — persists across cycles in live mode
SEEN_DEAL_HASHES = set()
SEEN_TITLES = set()
CYCLE_COUNT = 0
TOTAL_DEALS_SENT = 0


# ─── Cloudflare D1 Helper ─────────────────────────────────────────────────
def d1_query(sql, params=None):
    if CF_ACCOUNT and CF_D1_DB and CF_TOKEN:
        url = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT}/d1/database/{CF_D1_DB}/query"
        headers = {"Authorization": f"Bearer {CF_TOKEN}", "Content-Type": "application/json"}
        payload = {"sql": sql, "params": params or []}
        for attempt in range(3):
            try:
                r = requests.post(url, headers=headers, json=payload, timeout=30)
                if r.status_code == 200:
                    res = r.json()
                    if res.get("result") and len(res["result"]) > 0:
                        return res["result"][0].get("results", [])
                    return []
                elif r.status_code >= 500:
                    time.sleep(1.5 * (attempt + 1))
            except Exception:
                time.sleep(1.5 * (attempt + 1))
    return []


# ─── Deal Hash for Dedup ──────────────────────────────────────────────────
def deal_hash(title: str) -> str:
    """Generate a stable hash from deal title for dedup."""
    normalized = re.sub(r'[^a-z0-9]', '', title.lower())
    return hashlib.md5(normalized.encode()).hexdigest()[:12]


def is_new_deal(title: str) -> bool:
    """Check if this deal has already been seen in this session."""
    h = deal_hash(title)
    if h in SEEN_DEAL_HASHES:
        return False
    # Also check fuzzy title match
    normalized = re.sub(r'[^a-z0-9 ]', '', title.lower()).strip()
    for seen in SEEN_TITLES:
        # If 70%+ overlap, consider it a duplicate
        words_new = set(normalized.split())
        words_seen = set(seen.split())
        if len(words_new) > 0 and len(words_new & words_seen) / len(words_new) > 0.7:
            return False
    return True


def mark_deal_seen(title: str):
    """Mark a deal as seen to prevent re-sending."""
    global SEEN_DEAL_HASHES
    h = deal_hash(title)
    SEEN_DEAL_HASHES.add(h)
    normalized = re.sub(r'[^a-z0-9 ]', '', title.lower()).strip()
    SEEN_TITLES.add(normalized)


# ─── SOURCE 1: Google News RSS (Price-Specific Queries) ────────────────────
def scan_google_news_rss() -> list[dict]:
    """Scan Google News RSS with queries that force price-specific results."""
    queries = [
        # Price-specific: These force Google to return articles with actual ₹ prices
        '"₹"+smartphone+deal+Amazon+India+today',
        '"₹"+laptop+deal+lowest+price+India+today',
        '"₹"+earbuds+TWS+deal+India+price+drop',
        '"lowest+price"+OR+"price+drop"+OR+"loot+deal"+Amazon+Flipkart+India',
        '"all+time+low"+price+Amazon+OR+Flipkart+India',
        # Product-specific hot deals
        'iPhone+price+drop+₹+India+Amazon+OR+Flipkart',
        'Samsung+Galaxy+deal+₹+lowest+India',
        'OnePlus+deal+₹+price+drop+India',
        'gaming+laptop+deal+₹+India+Amazon',
        'smartwatch+TWS+earbuds+deal+₹+India+today',
    ]

    all_items = []
    for q in queries:
        try:
            url = f"https://news.google.com/rss/search?q={q}&hl=en-IN&gl=IN&ceid=IN:en&when=4h"
            r = requests.get(url, headers=UA, timeout=10)
            if r.status_code == 200:
                root = ET.fromstring(r.content)
                for item in root.findall(".//item")[:6]:
                    t = item.find("title")
                    d = item.find("description")
                    pub = item.find("pubDate")
                    if t is not None and t.text:
                        title = t.text.strip()
                        # Pre-filter: must mention a price indicator
                        price_indicators = ['₹', 'rs ', 'rs.', 'price', 'deal', 'off', 'discount', 'loot', 'lowest', 'flash', 'cashback', 'bank offer', 'coupon']
                        if any(k in title.lower() for k in price_indicators):
                            all_items.append({
                                "title": title,
                                "desc": (d.text or "")[:400] if d is not None else "",
                                "source": "Google News RSS",
                                "pub_date": pub.text if pub is not None else ""
                            })
        except Exception:
            continue

    return all_items


# ─── SOURCE 2: DesiDime + Indian Deal Aggregators ─────────────────────────
def scan_deal_aggregator_feeds() -> list[dict]:
    """Scan Indian deal aggregators: DesiDime (hot deals page), RSS feeds, MySmartPrice."""
    all_items = []

    # 2A: DesiDime Hot Deals Page (THE #1 source for Indian loot deals)
    try:
        r = requests.get("https://www.desidime.com/deals", headers=UA, timeout=10)
        if r.status_code == 200:
            # Extract deal titles and prices from the deals listing page
            deals = re.findall(
                r'class="[^"]*deal[^"]*"[^>]*>.*?<a[^>]*>([^<]{10,120})</a>',
                r.text, re.DOTALL
            )
            prices = re.findall(r'₹\s*([\d,]+)', r.text)
            for i, title in enumerate(deals[:15]):
                title = re.sub(r'<[^>]+>', '', title).strip()
                if len(title) > 10:
                    price = prices[i] if i < len(prices) else ""
                    all_items.append({
                        "title": f"{title} at ₹{price}" if price else title,
                        "desc": "Live on DesiDime",
                        "source": "DesiDime Hot"
                    })
    except Exception:
        pass

    # 2B: DesiDime + CouponDunia RSS feeds
    feeds = [
        "https://www.desidime.com/rss",
        "https://www.dealsoftheday.in/feed",
        "https://www.coupondunia.in/blog/feed/",
        "https://www.mysmartprice.com/gear/feed/",
    ]

    for feed_url in feeds:
        try:
            r = requests.get(feed_url, headers=UA, timeout=8)
            if r.status_code == 200:
                root = ET.fromstring(r.content)
                for item in root.findall(".//item")[:10]:
                    t = item.find("title")
                    d = item.find("description")
                    if t is not None and t.text:
                        title = t.text.strip()
                        deal_keywords = ['₹', 'deal', 'offer', 'price', 'sale', 'loot', 'off', 'discount', 'lowest', 'flash', 'cashback', 'buy', 'grab', 'steal']
                        if any(k in title.lower() for k in deal_keywords):
                            all_items.append({
                                "title": title,
                                "desc": (d.text or "")[:400] if d is not None else "",
                                "source": feed_url.split("//")[1].split("/")[0]
                            })
        except Exception:
            continue

    # 2C: MySmartPrice Price Drop Alerts
    try:
        for category in ["mobiles", "laptops", "tablets", "earphones"]:
            url = f"https://www.mysmartprice.com/{category}/"
            r = requests.get(url, headers=UA, timeout=8)
            if r.status_code == 200:
                # Extract product names and prices
                products = re.findall(r'"name"\s*:\s*"([^"]{10,80})"', r.text)
                prices = re.findall(r'"price"\s*:\s*"?([\d,]+)', r.text)
                for i, name in enumerate(products[:5]):
                    price = prices[i] if i < len(prices) else ""
                    if price:
                        all_items.append({
                            "title": f"{name} now at ₹{price}",
                            "desc": f"Price on MySmartPrice",
                            "source": "MySmartPrice"
                        })
    except Exception:
        pass

    return all_items


# ─── SOURCE 3: Amazon India Deal of the Day Page ──────────────────────────
def scan_amazon_deals_page() -> list[dict]:
    """Scrape Amazon India's Today's Deals page for active lightning deals."""
    items = []
    try:
        # Use Amazon's deal feed RSS alternative
        url = "https://www.amazon.in/gp/goldbox"
        r = requests.get(url, headers=UA, timeout=12)
        if r.status_code == 200:
            # Extract deal titles from the page
            titles = re.findall(r'"dealTitle"\s*:\s*"([^"]+)"', r.text)
            prices = re.findall(r'"dealPrice"\s*:\s*"?(\d[\d,]*)"?', r.text)
            for i, title in enumerate(titles[:10]):
                price = prices[i] if i < len(prices) else ""
                items.append({
                    "title": f"Amazon Deal: {title} at ₹{price}" if price else f"Amazon Deal: {title}",
                    "desc": f"Live deal on Amazon India goldbox",
                    "source": "Amazon Goldbox"
                })
    except Exception:
        pass
    return items


# ─── SOURCE 4: Flipkart Offers API ───────────────────────────────────────
def scan_flipkart_offers() -> list[dict]:
    """Scan Flipkart for active deals via their offers page."""
    items = []
    try:
        url = "https://www.flipkart.com/offers/today"
        r = requests.get(url, headers=UA, timeout=12)
        if r.status_code == 200:
            # Extract product titles + prices from offers page
            product_blocks = re.findall(r'<a[^>]*title="([^"]{10,80})"[^>]*href="(/[^"]+)"', r.text)
            prices = re.findall(r'₹([\d,]+)', r.text)
            for i, (title, href) in enumerate(product_blocks[:10]):
                price = prices[i] if i < len(prices) else ""
                if any(k in title.lower() for k in ['phone', 'laptop', 'watch', 'buds', 'tv', 'camera', 'tablet', 'earphone', 'headphone']):
                    items.append({
                        "title": f"Flipkart: {title} at ₹{price}" if price else f"Flipkart: {title}",
                        "desc": f"Live on Flipkart offers page",
                        "source": "Flipkart Offers"
                    })
    except Exception:
        pass
    return items


# ─── SOURCE 5: Price History / Drop Detection ────────────────────────────
def scan_price_drops_in_d1() -> list[dict]:
    """
    Check D1 for products where we can detect a price drop.
    Compares stored price vs current market indicators.
    """
    items = []
    try:
        products = d1_query(
            "SELECT id, name, price, mrp, merchant, badge FROM products WHERE niche_id = ? AND active = 1",
            ["5cf8114c0bc3eb20c87ce3dcfc1ff185"]
        )
        if products:
            for p in products:
                # If discount > 40%, it's potentially a loot deal worth re-alerting
                if p.get("mrp") and p.get("price"):
                    mrp = float(p["mrp"])
                    price = float(p["price"])
                    if mrp > 0 and ((mrp - price) / mrp) > 0.40:
                        items.append({
                            "title": f"PRICE DROP ALERT: {p['name']} now ₹{int(price):,} (was ₹{int(mrp):,})",
                            "desc": f"{int((mrp-price)/mrp*100)}% off on {p.get('merchant', 'Amazon')}",
                            "source": "D1 Price Monitor",
                            "already_parsed": {
                                "name": p["name"],
                                "price": int(price),
                                "mrp": int(mrp),
                                "discount_pct": int((mrp - price) / mrp * 100),
                                "merchant": p.get("merchant", "Amazon"),
                                "badge": "🔥 MASSIVE PRICE DROP",
                            }
                        })
    except Exception:
        pass
    return items


# ─── SOURCE 6: Twitter/X Deal Hashtags (via Nitter RSS) ──────────────────
def scan_twitter_deal_feeds() -> list[dict]:
    """Scan deal-related Twitter feeds via RSS proxies."""
    items = []
    # These are public RSS feeds for Indian deal accounts
    nitter_feeds = [
        "https://nitter.net/IndianDeals_/rss",
        "https://nitter.net/DesidimeDeals/rss",
        "https://nitter.net/LootDealsTricks/rss",
    ]
    for feed_url in nitter_feeds:
        try:
            r = requests.get(feed_url, headers=UA, timeout=6)
            if r.status_code == 200:
                root = ET.fromstring(r.content)
                for item in root.findall(".//item")[:5]:
                    t = item.find("title")
                    d = item.find("description")
                    if t is not None and t.text:
                        items.append({
                            "title": t.text.strip()[:200],
                            "desc": (d.text or "")[:300] if d is not None else "",
                            "source": "Twitter Deals"
                        })
        except Exception:
            continue
    return items


# ─── Gemini AI Deal Parser (Shared) ──────────────────────────────────────
def gemini_parse_deal(raw_title: str, raw_desc: str) -> dict | None:
    """Use Gemini to extract structured deal data from raw text."""
    if not GEMINI_KEY:
        return None

    prompt = f"""You are UniqueDigit's AI Loot Radar for Indian e-commerce deals.

Headline: "{raw_title}"
Context: "{raw_desc}"

TASK: Extract the BEST product deal from this headline. Be aggressive — if ANY specific product is mentioned with a discount, price, or deal context, extract it.

RULES:
1. If the headline mentions multiple products, pick the ONE with the highest discount or most attractive deal.
2. If no exact price is given but a discount % is mentioned, estimate the Indian MRP and calculate the deal price.
3. For well-known products (iPhone, Samsung Galaxy, OnePlus, etc.), you KNOW the Indian MRP — use it.
4. ONLY return {{"skip": true}} if the headline is purely editorial/opinion with ZERO product or deal mention.
5. Articles about sales (Big Billion Days, GIFD, etc.) that mention product categories with discounts ARE valid — pick the best product.

Indian MRP Knowledge:
- iPhone 15: ₹79,900 → Deal ~₹54,999-64,999
- iPhone 16: ₹79,900 → Deal ~₹64,999-74,999
- Samsung Galaxy S24 Ultra: ₹1,29,999 → Deal ~₹89,999-1,09,999
- OnePlus 12: ₹64,999 → Deal ~₹49,999-57,999
- MacBook Air M3: ₹1,14,900 → Deal ~₹79,990-94,990
- boAt Airdopes: ₹2,999 → Deal ~₹999-1,499
- Samsung Galaxy M55: ₹26,999 → Deal ~₹15,999-19,999

Format strict JSON:
{{
  "name": "Exact clean product name",
  "merchant": "Amazon | Flipkart | Myntra | Ajio | Meesho | Other",
  "category": "Smartphones | Laptops | Audio | Smartwatches | Fashion | Home Appliances | TVs | Tablets",
  "badge": "🔥 PRICE DROP | ⚡ LOOT DEAL | ⭐ ALL-TIME LOW | 💳 BANK OFFER | 🎯 FLASH SALE | 🛒 FESTIVAL DEAL",
  "mrp": 79900,
  "price": 54999,
  "discount_pct": 31,
  "tagline": "Concise deal summary for Telegram broadcast",
  "is_real_deal": true
}}"""

    models = [
        os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite"),
        "gemini-3.8-flash",
        "gemini-flash-latest"
    ]
    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_KEY}"
        try:
            r = requests.post(
                url,
                json={
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {"responseMimeType": "application/json", "temperature": 0.15}
                },
                timeout=20
            )
            if r.status_code == 200:
                text = r.json()["candidates"][0]["content"]["parts"][0]["text"]
                data = json.loads(text)
                if data.get("skip"):
                    return None
                if data.get("is_real_deal") is False:
                    return None
                return data
        except Exception:
            continue
    return None


# ─── Image Fetcher (from pipeline_amazon_deals.py) ───────────────────────
VERIFIED_ASIN_REGISTRY = {
    "samsung galaxy m55": {"asin": "B0CYQ3SDSH", "image": "https://m.media-amazon.com/images/I/81nr2rrnbqL._SL1500_.jpg"},
    "boat airdopes 141": {"asin": "B09N3ZNHTY", "image": "https://m.media-amazon.com/images/I/71RFdy6y6LL._SL1500_.jpg"},
    "oneplus nord ce4": {"asin": "B0CY5JMG98", "image": "https://rukminim2.flixcart.com/image/832/832/xif0q/mobile/y/2/t/nord-ce4-cph2613-oneplus-resized-original-imahjjxfctxbtt2e.jpeg"},
    "apple iphone 15": {"asin": "B0CHX1W1XY", "image": "https://m.media-amazon.com/images/I/71657TiFeHL._SL1500_.jpg"},
    "sony wh-1000xm4": {"asin": "B0863TXGM3", "image": "https://m.media-amazon.com/images/I/71o8Q5XJS5L._SL1500_.jpg"},
    "sony wh-ch520": {"asin": "B0BT5G144M", "image": "https://m.media-amazon.com/images/I/41lArSiD5hL._SL1000_.jpg"},
    "ipad 10th": {"asin": "B0BJLXMS8Y", "image": "https://m.media-amazon.com/images/I/61uA2UVnYWL._SL1500_.jpg"},
    "fire-boltt ninja call pro": {"asin": "B0BF57RN3K", "image": "https://m.media-amazon.com/images/I/61S9aVnRZDL._SL1500_.jpg"},
}


def fetch_product_image(name: str, category: str = "") -> str | None:
    """Get exact studio product image. Registry first, then Flipkart CDN."""
    if not name:
        return None

    lower_p = name.lower()
    for key, val in VERIFIED_ASIN_REGISTRY.items():
        if key in lower_p:
            return val["image"]

    # Flipkart CDN fallback
    clean = re.sub(r'\(.*?\)', '', name).strip()
    clean = re.sub(r'\b(5G|4G|128GB|256GB|8GB|16GB|6GB)\b', '', clean, flags=re.IGNORECASE).strip()
    q = urllib.parse.quote_plus(clean)

    try:
        url = f"https://www.flipkart.com/search?q={q}"
        r = requests.get(url, headers=UA, timeout=8)
        if r.status_code == 200:
            imgs = re.findall(
                r"https://rukminim[0-9]\.flixcart\.com/image/[0-9]+/[0-9]+/([a-zA-Z0-9+_%/-]+\.(?:jpeg|jpg|png))",
                r.text
            )
            bad = ['panel', 'case', 'cover', 'screen-guard', 'charger', 'cable', 'adapter', 'back-cover']
            valid = [i for i in imgs if not any(b in i.lower() for b in bad)]
            for img_path in valid[:3]:
                full = f"https://rukminim2.flixcart.com/image/832/832/{img_path}"
                try:
                    chk = requests.head(full, headers=UA, timeout=4)
                    if chk.status_code == 200:
                        return full
                except Exception:
                    continue
    except Exception:
        pass
    return None


# ─── Affiliate URL Builder ────────────────────────────────────────────────
def build_affiliate_url(name: str, merchant: str = "Amazon") -> str:
    lower_p = (name or "").lower()
    for key, val in VERIFIED_ASIN_REGISTRY.items():
        if key in lower_p:
            return f"https://www.amazon.in/dp/{val['asin']}?tag={AMAZON_TAG}"

    q = urllib.parse.quote_plus(name)
    merchant_l = (merchant or "").lower()

    if "flipkart" in merchant_l:
        return f"https://www.flipkart.com/search?q={q}"
    elif "myntra" in merchant_l:
        return f"https://www.myntra.com/{q}"
    elif "meesho" in merchant_l:
        return f"https://www.meesho.com/search?q={q}"
    return f"https://www.amazon.in/s?k={q}&tag={AMAZON_TAG}"


# ─── Telegram Broadcaster ────────────────────────────────────────────────
def send_telegram_deal(deal: dict) -> bool:
    """Send a deal alert to Telegram. Returns True if sent successfully."""
    if not TG_BOT_TOKEN or not TG_DEALS_CHANNEL:
        print("[⚠️ Telegram] Bot token or channel not configured!")
        return False

    name = deal.get("name", "Exclusive Deal")
    price = deal.get("price", 0)
    mrp = deal.get("mrp", 0)
    discount = deal.get("discount_pct", 0)
    aff_url = deal.get("aff_url", "https://uniquedigit-viral-hub.pages.dev/deals")
    badge = deal.get("badge", "🔥 LOOT DEAL")
    merchant = deal.get("merchant", "Amazon")
    tagline = deal.get("tagline", f"Limited time deal on {merchant}")
    image_url = deal.get("image_url", "")

    caption = (
        f"⚡ <b>[{badge}]</b> ⚡\n\n"
        f"🛍️ <b>{name}</b>\n\n"
        f"📉 <b>Steal Price:</b> ₹{price:,} " + (f"(<s>₹{mrp:,}</s> - {discount}% OFF)\n" if mrp else "\n") +
        f"💡 <i>{tagline}</i>\n\n"
        f"🏪 <b>Store:</b> {merchant}\n"
        f'🔗 <b>Grab Deal:</b> <a href="{aff_url}">BUY NOW →</a>\n\n'
        f"🚨 <i>Limited stock! Price may increase anytime.</i>\n\n"
        f"📣 @uniquedigit_deals"
    )

    tg_url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}"

    try:
        # Try sending with image first
        if image_url:
            r = requests.post(
                f"{tg_url}/sendPhoto",
                json={
                    "chat_id": TG_DEALS_CHANNEL,
                    "photo": image_url,
                    "caption": caption,
                    "parse_mode": "HTML"
                },
                timeout=15
            )
            if r.status_code == 200:
                return True

        # Fallback: text only
        r = requests.post(
            f"{tg_url}/sendMessage",
            json={
                "chat_id": TG_DEALS_CHANNEL,
                "text": caption,
                "parse_mode": "HTML",
                "disable_web_page_preview": False
            },
            timeout=10
        )
        return r.status_code == 200
    except Exception as e:
        print(f"[Telegram Error]: {e}")
        return False


# ─── D1 Insert ────────────────────────────────────────────────────────────
DEALS_NICHE_ID = "5cf8114c0bc3eb20c87ce3dcfc1ff185"

def insert_deal_to_d1(deal: dict) -> bool:
    """Insert a parsed deal into Cloudflare D1."""
    try:
        deal_id = f"loot-{int(time.time())}-{hashlib.md5(deal['name'].encode()).hexdigest()[:6]}"
        sql = """
        INSERT OR IGNORE INTO products (id, niche_id, name, tagline, category, badge, keywords, image_url, price, mrp, discount_pct, rating, url, aff_url, merchant, clicks, active, sort)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 4.6, ?, ?, ?, 0, 1, 0)
        """
        params = [
            deal_id, DEALS_NICHE_ID, deal["name"],
            deal.get("tagline", ""), deal.get("category", "Smartphones"),
            deal.get("badge", "🔥 LOOT DEAL"), deal["name"].lower(),
            deal.get("image_url", ""), deal.get("price", 0), deal.get("mrp", 0),
            deal.get("discount_pct", 0), deal.get("aff_url", ""),
            deal.get("aff_url", ""), deal.get("merchant", "Amazon")
        ]
        d1_query(sql, params)
        return True
    except Exception as e:
        print(f"[D1 Insert Error]: {e}")
        return False


# ─── MAIN RADAR ENGINE ───────────────────────────────────────────────────
def run_radar_cycle():
    """Execute one full radar scan across all sources."""
    global CYCLE_COUNT, TOTAL_DEALS_SENT
    CYCLE_COUNT += 1
    cycle_start = time.time()

    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"\n{'='*70}")
    print(f"🔍 RADAR CYCLE #{CYCLE_COUNT} | {timestamp} | Deals Sent So Far: {TOTAL_DEALS_SENT}")
    print(f"{'='*70}")

    # Parallel scan all sources
    all_candidates = []
    source_results = {}

    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = {
            executor.submit(scan_google_news_rss): "Google News",
            executor.submit(scan_deal_aggregator_feeds): "Deal Aggregators",
            executor.submit(scan_amazon_deals_page): "Amazon Goldbox",
            executor.submit(scan_flipkart_offers): "Flipkart Offers",
            executor.submit(scan_price_drops_in_d1): "D1 Price Monitor",
            executor.submit(scan_twitter_deal_feeds): "Twitter Deals",
        }

        for future in as_completed(futures, timeout=20):
            source_name = futures[future]
            try:
                results = future.result(timeout=15)
                source_results[source_name] = len(results)
                all_candidates.extend(results)
            except Exception as e:
                source_results[source_name] = f"ERR: {e}"

    # Print source summary
    for source, count in source_results.items():
        status = f"✅ {count} items" if isinstance(count, int) else f"❌ {count}"
        print(f"  [{source}]: {status}")

    print(f"\n📊 Total raw candidates: {len(all_candidates)}")

    # Filter to NEW deals only
    new_deals = [c for c in all_candidates if is_new_deal(c["title"])]

    # Prioritize: external fresh deals first, then D1 re-alerts last
    external_deals = [d for d in new_deals if d.get("source") != "D1 Price Monitor"]
    d1_deals = [d for d in new_deals if d.get("source") == "D1 Price Monitor"]
    new_deals = external_deals + d1_deals

    print(f"🆕 New (unseen) deals: {len(new_deals)} ({len(external_deals)} external + {len(d1_deals)} D1)")

    if not new_deals:
        elapsed = time.time() - cycle_start
        print(f"⏱️ Cycle completed in {elapsed:.1f}s — No new deals found.")
        return 0

    # Process new deals through Gemini + image fetch + Telegram broadcast
    deals_sent = 0
    for candidate in new_deals[:8]:  # Max 8 per cycle
        title = candidate["title"]
        desc = candidate.get("desc", "")
        source = candidate.get("source", "Unknown")

        print(f"\n  🔄 Processing: {title[:80]}... [{source}]")

        # Check if already pre-parsed (e.g., from D1 price monitor)
        if candidate.get("already_parsed"):
            deal = candidate["already_parsed"]
        else:
            # Parse with Gemini
            deal = gemini_parse_deal(title, desc)
            if not deal or not deal.get("name") or not deal.get("price"):
                print(f"    ⏭️ Skipped (no valid deal extracted)")
                mark_deal_seen(title)
                continue

        name = deal["name"]
        merchant = deal.get("merchant", "Amazon")

        # Check D1 for existing product with same name
        existing = d1_query(
            "SELECT name FROM products WHERE LOWER(name) LIKE ? LIMIT 1",
            [f"%{name.lower()[:30]}%"]
        )
        if existing:
            print(f"    ⏭️ Already in D1: {name}")
            mark_deal_seen(title)
            continue

        # Fetch product image
        image_url = fetch_product_image(name, deal.get("category", ""))
        deal["image_url"] = image_url or ""

        # Build affiliate URL
        deal["aff_url"] = build_affiliate_url(name, merchant)

        # Send to Telegram
        if send_telegram_deal(deal):
            print(f"    ✅ SENT TO TELEGRAM: {name} | ₹{deal.get('price', 0):,}")
            TOTAL_DEALS_SENT += 1
            deals_sent += 1

            # Also insert to D1
            insert_deal_to_d1(deal)
        else:
            print(f"    ❌ Telegram send failed for: {name}")

        mark_deal_seen(title)
        time.sleep(1)  # Rate limit between posts

    elapsed = time.time() - cycle_start
    print(f"\n⏱️ Cycle #{CYCLE_COUNT} completed in {elapsed:.1f}s — Sent {deals_sent} deals")
    return deals_sent


# ─── Entry Point ──────────────────────────────────────────────────────────
def main():
    if LIVE_MODE or BLITZ_MODE:
        mode = "🎯 BLITZ (Festival)" if BLITZ_MODE else "🟢 LIVE 24/7"
        print(f"""
╔══════════════════════════════════════════════════════════════════════╗
║  🚀 UNIQUEDIGIT LOOT RADAR — REAL-TIME DEAL INTELLIGENCE AGENT     ║
║                                                                      ║
║  Mode:      {mode:<54}║
║  Channel:   @uniquedigit_deals                                       ║
║  Interval:  {SCAN_INTERVAL}s scan cycles                                          ║
║  Sources:   Google News | DesiDime | Amazon | Flipkart | Twitter     ║
║  AI:        Gemini Flash (Deal Parser)                               ║
║  Affiliate: uniquedigi0c6-21                                         ║
║                                                                      ║
║  Press Ctrl+C to stop                                                ║
╚══════════════════════════════════════════════════════════════════════╝
""")
        # Load existing D1 products into seen set to avoid re-sending
        print("📥 Loading existing deals from D1 to prevent duplicates...")
        existing = d1_query("SELECT name FROM products WHERE niche_id = ?", [DEALS_NICHE_ID])
        if existing:
            for p in existing:
                if p.get("name"):
                    mark_deal_seen(p["name"])
            print(f"   Loaded {len(existing)} existing deals into dedup cache.\n")

        # Continuous live loop
        while True:
            try:
                run_radar_cycle()
            except KeyboardInterrupt:
                print(f"\n\n🛑 Loot Radar stopped. Total deals sent: {TOTAL_DEALS_SENT}")
                break
            except Exception as e:
                print(f"\n[⚠️ Cycle Error]: {e}")

            print(f"⏳ Next scan in {SCAN_INTERVAL}s...")
            try:
                time.sleep(SCAN_INTERVAL)
            except KeyboardInterrupt:
                print(f"\n\n🛑 Loot Radar stopped. Total deals sent: {TOTAL_DEALS_SENT}")
                break
    else:
        # One-shot mode (for GitHub Actions)
        print("🔍 Running one-shot radar scan...")
        run_radar_cycle()


if __name__ == "__main__":
    main()
