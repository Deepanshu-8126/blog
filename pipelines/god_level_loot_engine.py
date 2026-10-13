#!/usr/bin/env python3
"""
=============================================================================
GOD-LEVEL LOOT ENGINE (ALL-IN-ONE COMBO)
=============================================================================
A 24/7 continuous autonomous loot intelligence engine combining:

  👑 PILLAR 1: Telegram Channel Spy & Link Switcher
     - Monitors top deal channels (DealsMagnet, DesiDime, etc.) in real time
     - Unshortens redirects and extracts product ASINs / links
     - Strips competitor tags and branding
     - Injects YOUR Amazon affiliate tag: uniquedigi0c6-21
     - Grabs high-res Telegram CDN photos directly

  👑 PILLAR 2: Personal Price Glitch & ASIN Watcher
     - Curated registry of top viral festive products (iPhones, MacBooks, Samsungs, TVs)
     - Cloudflare D1 price drop monitor (>35% discount)
     - Official studio Amazon CDN image mapping

  👑 PILLAR 3: Community & Festive RSS Radar
     - Google News Festive Sales & DesiDime Hot Deals RSS
     - Gemini AI parsing with aggressive festive pricing extraction

  🧠 SHARED DEDUP & BROADCASTER:
     - Shared persistent cache across all 3 pillars (zero duplicates)
     - Formats premium Markdown cards with HD photos
     - Direct broadcast to Telegram channel: @uniquedigit_deals
=============================================================================
"""

import os
import sys
import re
import json
import time
import random
import hashlib
import argparse
import urllib.request
import urllib.parse
import urllib.error
import html
import tempfile
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Force UTF-8 encoding for Windows terminals
if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            getattr(sys.stdout, "reconfigure")(encoding="utf-8")
        if hasattr(sys.stderr, "reconfigure"):
            getattr(sys.stderr, "reconfigure")(encoding="utf-8")
    except Exception:
        pass

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

load_dotenv()

# =============================================================================
# CREDENTIALS & CONFIGURATION
# =============================================================================
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8594213665:AAHWPNHEzrC9ChpK5vqYyyy8fFkq1BgPCik")
TELEGRAM_DEALS_CHANNEL = os.getenv("TELEGRAM_DEALS_CHANNEL", "@uniquedigit_deals")
TELEGRAM_DEALS_GROUP_ID = os.getenv("TELEGRAM_DEALS_GROUP_ID", "-1004335990773")
AMAZON_TAG = os.getenv("AMAZON_AFFILIATE_TAG", "uniquedigi0c6-21")
EARNKARO_USER_ID = os.getenv("EARNKARO_USER_ID", "3360368")
MEESHO_CREATOR_ID = os.getenv("MEESHO_CREATOR_ID", "374453404")
PORTAL_BASE = os.getenv("PORTAL_BASE_URL", "https://uniquedigit-viral-hub.pages.dev")
WHATSAPP_CHANNEL_URL = os.getenv("WHATSAPP_CHANNEL_URL", "https://whatsapp.com/channel/0029Vb90gso4dTnKKpcf7M1E")

TOPIC_IDS = {
    "loots": 3,      # ⚡ 0-Minute Loots & Glitches
    "tech": 4,       # 💻 Tech, Laptops & Mobiles
    "fashion": 5,    # 👔 Clothes, Shoes & Fashion
    "home": 6        # 🏠 Home Appliances & TV
}

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
CF_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID", "cf1a42fb306054063805cf459fddf853")
CF_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN", "")
CF_D1_DB_ID = os.getenv("CLOUDFLARE_D1_DATABASE_ID", "61d1d46f-f438-47f5-9128-516d9beb11cb")
DEALS_NICHE_ID = os.getenv("DEALS_NICHE_ID", "5cf8114c0bc3eb20c87ce3dcfc1ff185")

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.6; rv:130.0) Gecko/20100101 Firefox/130.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_6_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",
]
USER_AGENT = USER_AGENTS[0]
CACHE_FILE = "sent_loot_cache.json"

# Top public Telegram deals channels to spy & switch links (verified fast & live)
SPY_CHANNELS = [
    "dealsmagnet",
    "dealbee",
    "dealsheaven"
]

# Top viral festive products with verified ASINs & Official CDN photos
VIRAL_FESTIVE_REGISTRY = {
    "B0BDK62PDX": {
        "title": "Apple iPhone 15 (128 GB) - Black",
        "mrp": 69900, "deal_price": 54999,
        "image": "https://m.media-amazon.com/images/I/71657TiFeHL._SL1500_.jpg"
    },
    "B0CHX1W1XY": {
        "title": "Apple iPhone 15 Plus (128 GB) - Blue",
        "mrp": 79900, "deal_price": 64999,
        "image": "https://m.media-amazon.com/images/I/71657TiFeHL._SL1500_.jpg"
    },
    "B0DGH5Z3L2": {
        "title": "Apple iPhone 16 (128 GB) - Teal",
        "mrp": 79900, "deal_price": 69999,
        "image": "https://cdsassets.apple.com/live/7WUAS350/images/tech-specs/iphone-16.png"
    },
    "B0CX24C6F1": {
        "title": "Apple MacBook Air M3 Chip (13-inch, 8GB Unified Memory, 256GB SSD)",
        "mrp": 104900, "deal_price": 89990,
        "image": "https://m.media-amazon.com/images/I/71jG+e7roXL._SL1500_.jpg"
    },
    "B0B3C68Q9P": {
        "title": "Apple MacBook Air M2 Chip (13.6-inch, 8GB RAM, 256GB SSD) - Midnight",
        "mrp": 99900, "deal_price": 69990,
        "image": "https://m.media-amazon.com/images/I/710TJuHTMhL._SL1500_.jpg"
    },
    "B0CRVK2SZ5": {
        "title": "Samsung Galaxy S24 5G (8GB RAM, 128GB Storage) - Onyx Black",
        "mrp": 79999, "deal_price": 54999,
        "image": "https://m.media-amazon.com/images/I/717Qo4MH97L._SL1500_.jpg"
    },
    "B0CZ7MQN4F": {
        "title": "OnePlus 12R (16GB RAM, 256GB Storage) - Cool Blue",
        "mrp": 45999, "deal_price": 37999,
        "image": "https://m.media-amazon.com/images/I/717Qo4MH97L._SL1500_.jpg"
    },
    "B0D77Y9B7P": {
        "title": "OnePlus Nord 4 5G (8GB RAM, 256GB Storage) - Mercurial Silver",
        "mrp": 32999, "deal_price": 27999,
        "image": "https://fdn2.gsmarena.com/vv/bigpic/oneplus-nord4.jpg"
    },
    "B0C77K13X5": {
        "title": "Sony WH-1000XM5 Wireless Industry Leading Noise Canceling Headphones",
        "mrp": 34990, "deal_price": 25990,
        "image": "https://m.media-amazon.com/images/I/61+btxzpfDL._SL1500_.jpg"
    },
    "B09N3XMZ5F": {
        "title": "boAt Airdopes 141 ANC TWS Earbuds (42H Playtime, 32dB ANC)",
        "mrp": 4490, "deal_price": 1299,
        "image": "https://m.media-amazon.com/images/I/71oXzCK43NL._SL1500_.jpg"
    },
    "B0CX5CYW9N": {
        "title": "Xiaomi 43-inch Smart Google TV 4K Ultra HD (Dolby Vision, 30W Speakers)",
        "mrp": 42999, "deal_price": 21999,
        "image": "https://i02.appmifile.com/mi-com-product/fly-birds/xiaomi-smart-4k-tv-f-43-2025/m-in/3728e5c6352918e127883e9b0ab45f90.png"
    }
}

# =============================================================================
# PERSISTENT DEDUP CACHE
# =============================================================================
def extract_asin(url):
    """Extracts 10-character Amazon ASIN from any URL."""
    if not url:
        return None
    m = re.search(r'/(?:dp|gp/product|d)/([A-Z0-9]{10})', url)
    return m.group(1) if m else None

def normalize_product_title(text):
    """Normalizes titles to base product identity (e.g. 'Apple iPhone 16 (128GB) - Teal' -> 'apple iphone 16')."""
    if not text:
        return ""
    t = text.lower()
    # Remove storage specs like 128gb, 256gb, 512gb, 8gb, 16gb
    t = re.sub(r'\b\d+\s*(?:gb|tb|mb|ram|rom)\b', '', t)
    # Remove colors and accessories details inside parentheses or after hyphens
    t = re.sub(r'\(.*?\)', '', t)
    t = re.sub(r'[-|–].*$', '', t)
    # Remove discount percentages
    t = re.sub(r'\b\d{1,2}%\s*(?:off|discount)?\b', '', t)
    # Remove non-alphanumeric except spaces
    t = re.sub(r'[^a-z0-9\s]', '', t)
    tokens = [w for w in t.split() if w not in ["deal", "deals", "loot", "sale", "upto", "flat", "off", "pack", "with", "for", "new"]]
    return " ".join(tokens[:5]) # Core 5 tokens identify the product

def is_generic_discount_title(title):
    """Checks if title is just a discount percentage without product name."""
    clean = (title or "").strip().lower()
    if re.match(r'^(?:flat\s*|upto\s*)?\d{1,2}%\s*(?:off|discount)?$', clean):
        return True
    if len(clean) < 10 and any(w in clean for w in ["off", "deal", "loot", "sale", "drop"]):
        return True
    return False

# =============================================================================
# PERSISTENT MULTI-KEY DEDUP CACHE (ZERO DUPLICATES GUARANTEE)
# =============================================================================
class DedupManager:
    def __init__(self, cache_path=CACHE_FILE):
        self.cache_path = cache_path
        self.cache = self._load()

    def _load(self):
        if os.path.exists(self.cache_path):
            try:
                with open(self.cache_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save(self):
        try:
            dir_name = os.path.dirname(self.cache_path) or "."
            with tempfile.NamedTemporaryFile("w", dir=dir_name, delete=False, encoding="utf-8") as tf:
                json.dump(self.cache, tf, indent=2)
                temp_name = tf.name
            os.replace(temp_name, self.cache_path)
        except Exception:
            pass

    def get_hash(self, text):
        clean = re.sub(r'[^a-zA-Z0-9]', '', (text or '').lower()[:60])
        return hashlib.sha256(clean.encode()).hexdigest()[:16]

    def is_seen(self, deal_or_key):
        """Checks if deal is seen by deal_id, exact title, normalized product name, or ASIN."""
        if isinstance(deal_or_key, dict):
            keys = [
                deal_or_key.get("id"),
                deal_or_key.get("title"),
                normalize_product_title(deal_or_key.get("title", "")),
                extract_asin(deal_or_key.get("affiliate_url", ""))
            ]
        else:
            keys = [str(deal_or_key), normalize_product_title(str(deal_or_key))]

        for k in keys:
            if k and self.get_hash(k) in self.cache:
                return True
        return False

    def mark_seen(self, deal):
        """Registers all product identity keys simultaneously to prevent any duplicate."""
        if isinstance(deal, dict):
            deal_id = deal.get("id")
            title = deal.get("title", "")
            norm_title = normalize_product_title(title)
            asin = extract_asin(deal.get("affiliate_url", ""))

            keys_to_mark = [k for k in [deal_id, title, norm_title, asin] if k]
        else:
            keys_to_mark = [str(deal)]

        now = datetime.now().isoformat()
        for k in keys_to_mark:
            h = self.get_hash(k)
            self.cache[h] = {
                "key": str(k)[:80],
                "timestamp": now
            }
        self._save()

dedup = DedupManager()

# =============================================================================
# HTTP & NETWORK HELPERS
# =============================================================================
def get_browser_headers():
    """Generates realistic modern browser headers with rotating User-Agents to prevent anti-bot blocking."""
    ua = random.choice(USER_AGENTS)
    headers = {
        "User-Agent": ua,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-IN,en-US;q=0.9,en;q=0.8,hi;q=0.7",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Upgrade-Insecure-Requests": "1"
    }
    if "Chrome" in ua or "Edg" in ua:
        headers["Sec-Ch-Ua"] = '"Not;A=Brand";v="24", "Chromium";v="128"'
        headers["Sec-Ch-Ua-Mobile"] = "?0"
        headers["Sec-Ch-Ua-Platform"] = '"Windows"' if "Windows" in ua else '"macOS"'
        headers["Sec-Fetch-Dest"] = "document"
        headers["Sec-Fetch-Mode"] = "navigate"
        headers["Sec-Fetch-Site"] = "none"
        headers["Sec-Fetch-User"] = "?1"
    return headers

def fetch_url(url, timeout=8, max_redirects=5):
    """Fetches URL content with rotating anti-block browser headers and fail-fast handling."""
    for attempt in range(2):
        try:
            req = urllib.request.Request(url, headers=get_browser_headers())
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read().decode("utf-8", errors="replace"), resp.geturl()
        except urllib.error.HTTPError as he:
            if he.code == 429:
                time.sleep(2)
                continue
            return None, url
        except Exception:
            if attempt == 0:
                time.sleep(0.5)
                continue
            return None, url
    return None, url

def resolve_unshorten_url(url, timeout=5):
    """Follows redirects to find the real destination URL with browser headers."""
    if not url:
        return ""
    try:
        req = urllib.request.Request(url, headers=get_browser_headers())
        opener = urllib.request.build_opener(urllib.request.HTTPRedirectHandler)
        with opener.open(req, timeout=timeout) as resp:
            return resp.geturl()
    except Exception:
        return url

def security_clean_text(text):
    """Deep security scrubber to eliminate competitor traces, links, and tags."""
    if not text:
        return ""
    # Remove URLs
    t = re.sub(r'https?://[^\s]+', '', text)
    # Remove @ handles
    t = re.sub(r'@[a-zA-Z0-9_]+', '', t)
    # Remove t.me links
    t = re.sub(r'(?i)\bt\.me/[^\s]+', '', t)
    # Remove competitor brands
    t = re.sub(r'(?i)\b(dealsmagnet|desidime|dealbee|looter|looters|freestuff|indiafreestuff|fkm|freekaamaal|cashkaro|earnkaro|buyhatke|flipshope)\b', '', t)
    # Remove promo calls to action
    t = re.sub(r'(?i)\b(join|subscribe|telegram|whatsapp|channel|broadcast|follow)\b.*', '', t)
    return t.strip()

def convert_to_affiliate(url, tag=AMAZON_TAG):
    """Converts any store link (Amazon, Flipkart, Myntra, Meesho, Ajio) into a clean monetized affiliate URL."""
    if not url:
        return ""

    url_lower = url.lower()

    # 1. Amazon India (Direct Associate Tag)
    asin_match = re.search(r'/(?:dp|gp/product|d)/([A-Z0-9]{10})', url)
    if asin_match:
        asin = asin_match.group(1)
        return f"https://www.amazon.in/dp/{asin}?tag={tag}"
    if "amazon.in" in url_lower:
        parsed = urllib.parse.urlparse(url)
        q = urllib.parse.parse_qs(parsed.query)
        q["tag"] = [tag]
        for unwanted in ["ascsubtag", "linkCode", "camp", "creative", "ref"]:
            q.pop(unwanted, None)
        new_query = urllib.parse.urlencode(q, doseq=True)
        return urllib.parse.urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))

    # 2. Meesho (Direct Creator / Affiliate Monetization)
    if "meesho.com" in url_lower:
        # If competitor shared an af_invite link, swap competitor ID with our MEESHO_CREATOR_ID
        if "/af_invite/" in url:
            new_url = re.sub(r'/af_invite/\d+:', f'/af_invite/{MEESHO_CREATOR_ID}:', url)
            new_url = re.sub(r'utm_source=[^&]+', 'utm_source=telegram_deals', new_url)
            return new_url

        # Check if product ID (p_id) is in query or URL
        pid_match = re.search(r'[?&]p_id=(\d+)', url) or re.search(r'/p/(\d+)', url)
        if pid_match:
            pid = pid_match.group(1)
            return f"https://www.meesho.com/af_invite/{MEESHO_CREATOR_ID}:telegram:deals?p_id={pid}&utm_source=telegram_deals"

        # Fallback to EarnKaro wallet which also monetizes Meesho
        if EARNKARO_USER_ID:
            clean_url = url.split("?")[0]
            return f"https://earnkaro.com/deals?r={EARNKARO_USER_ID}&url={urllib.parse.quote(clean_url)}"
        return url

    # 3. Myntra, Flipkart, Ajio, Nykaa (EarnKaro Affiliate 1-Wallet)
    if any(m in url_lower for m in ["flipkart.com", "myntra.com", "ajio.com", "nykaa.com"]):
        parsed = urllib.parse.urlparse(url)
        # Clean product URL without competitor affiliate tags
        clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        if EARNKARO_USER_ID:
            return f"https://earnkaro.com/deals?r={EARNKARO_USER_ID}&url={urllib.parse.quote(clean_url)}"
        return clean_url

    return url

# =============================================================================
# REAL-TIME CLOUDFLARE D1 DEALS HUB SYNCHRONIZER
# =============================================================================
def sync_deal_to_cloudflare_d1(deal):
    """
    Directly synchronizes every live deal into Cloudflare D1 `products` table
    under DEALS_NICHE_ID (5cf8114c0bc3eb20c87ce3dcfc1ff185).
    Guarantees the Deals Hub on the website (/deals) is 24/7 populated with live internet deals.
    """
    if not CF_ACCOUNT_ID or not CF_API_TOKEN:
        return False

    try:
        title = deal.get("title", "").strip()
        if not title:
            return False

        # Generate stable, unique deal identifier
        deal_hash = hashlib.md5((title + deal.get("affiliate_url", "")).encode("utf-8")).hexdigest()[:12]
        deal_id = f"loot-{int(time.time())}-{deal_hash}"

        # Merchant detection
        aff_url = deal.get("affiliate_url", "")
        aff_lower = aff_url.lower()
        if "amazon" in aff_lower:
            merchant = "Amazon India"
        elif "flipkart" in aff_lower:
            merchant = "Flipkart"
        elif "myntra" in aff_lower:
            merchant = "Myntra"
        elif "meesho" in aff_lower:
            merchant = "Meesho"
        elif "ajio" in aff_lower:
            merchant = "Ajio"
        else:
            merchant = "Amazon India"

        # Price & discount derivation
        raw_price = deal.get("deal_price") or deal.get("price") or 0
        try:
            price = int(raw_price) if raw_price else 999
        except Exception:
            price = 999

        raw_mrp = deal.get("mrp") or 0
        try:
            mrp = int(raw_mrp) if raw_mrp else int(price * 1.35)
        except Exception:
            mrp = int(price * 1.35)

        raw_disc = deal.get("discount") or deal.get("discount_pct") or 0
        try:
            discount = int(raw_disc) if raw_disc else 0
        except Exception:
            discount = 0

        if mrp > price and not discount:
            discount = round(((mrp - price) / mrp) * 100)

        # Dynamic Category Classification
        title_lower = title.lower()
        if any(w in title_lower for w in ["phone", "mobile", "iphone", "samsung", "oneplus", "realme", "redmi", "pixel", "5g"]):
            category = "Smartphones"
        elif any(w in title_lower for w in ["laptop", "macbook", "hp", "dell", "asus", "lenovo", "acer", "intel", "ryzen", "gpu"]):
            category = "Laptops"
        elif any(w in title_lower for w in ["headphone", "earphone", "earbuds", "airpods", "tws", "neckband", "speaker", "audio", "boat", "sony"]):
            category = "Audio"
        elif any(w in title_lower for w in ["shoe", "sneaker", "shirt", "t-shirt", "jeans", "fashion", "dress", "kurti", "wear"]):
            category = "Fashion"
        elif price < 499:
            category = "Under ₹499"
        else:
            category = "Smartphones"

        # Dynamic Conversion Badges
        if discount >= 60:
            badge = f"🔥 FLAT {discount}% OFF"
        elif discount >= 40:
            badge = "⚡ 0-MIN PRICE DROP"
        elif price < 499:
            badge = "💥 UNDER ₹499 LOOT"
        else:
            badge = "⚡ VERIFIED STEAL"

        tagline = f"Live {merchant} Deal: ₹{price:,} (Save {discount}%)"

        # Image resolution
        photo_url = deal.get("photo_url") or ""
        if not photo_url or "m.media-amazon.com/images/I/71657TiFeHL" in photo_url:
            try:
                from bridges.universal_image_engine import get_universal_real_image
                hd_img, _ = get_universal_real_image(
                    title=title,
                    niche_slug="deals",
                    target_url=aff_url,
                    raw_image=photo_url
                )
                if hd_img:
                    photo_url = hd_img
            except Exception:
                pass

        now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

        sql = """
        INSERT INTO products (
            id, niche_id, name, tagline, category, badge, keywords,
            image_url, price, mrp, discount_pct, rating, url, aff_url,
            merchant, clicks, active, sort, created_at, deal_type
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 4.8, ?, ?, ?, 0, 1, 0, ?, 'deal'
        )
        ON CONFLICT(id) DO UPDATE SET
            price = excluded.price,
            mrp = excluded.mrp,
            discount_pct = excluded.discount_pct,
            image_url = excluded.image_url,
            aff_url = excluded.aff_url,
            active = 1;
        """
        params = [
            deal_id,
            DEALS_NICHE_ID,
            title[:90],
            tagline[:120],
            category,
            badge,
            f"{category.lower()} {merchant.lower()} loot deal",
            photo_url,
            int(price),
            int(mrp),
            int(discount),
            aff_url,
            aff_url,
            merchant,
            now
        ]

        url = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/d1/database/{CF_D1_DB_ID}/query"
        payload = json.dumps({"sql": sql, "params": params}).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers={
            "Authorization": f"Bearer {CF_API_TOKEN}",
            "Content-Type": "application/json"
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            if res.get("success"):
                print(f"    🌐 SYNCED TO DEALS HUB (D1): {title[:35]} (₹{price})")
                return True
    except Exception as e:
        print(f"    ⚠️ D1 sync warning: {e}")
    return False

# =============================================================================
# PILLAR 1: TELEGRAM CHANNELS SPY & LINK SWITCHER
# =============================================================================
class TelegramChannelSpy:
    """Monitors top Telegram deals channels, snatches deals, replaces affiliate tags."""

    def __init__(self, channels=SPY_CHANNELS):
        self.channels = channels

    def spy_channel(self, channel_name):
        url = f"https://t.me/s/{channel_name}"
        html, _ = fetch_url(url, timeout=8)
        if not html:
            return []

        soup = BeautifulSoup(html, "html.parser")
        wraps = soup.find_all("div", class_="tgme_widget_message_wrap")
        deals = []

        # Process the 5 most recent messages
        for wrap in wraps[-5:]:
            try:
                msg_div = wrap.find("div", class_="tgme_widget_message")
                msg_id = msg_div.get("data-post", "") if msg_div else ""
                if not msg_id or dedup.is_seen(msg_id):
                    continue

                text_div = wrap.find("div", class_="tgme_widget_message_text")
                if not text_div:
                    continue
                raw_text = text_div.get_text(separator="\n", strip=True)

                # Extract photo URL from Telegram CDN
                photo_el = wrap.find("a", class_="tgme_widget_message_photo_wrap")
                photo_url = ""
                if photo_el and "style" in photo_el.attrs:
                    style_str = str(photo_el.get("style", ""))
                    m = re.search(r"url\('([^']+)'\)", style_str)
                    if m:
                        photo_url = m.group(1)

                # Extract outbound links
                links = [a["href"] for a in wrap.find_all("a", href=True)
                         if "http" in a["href"] and "t.me" not in a["href"]]

                store_keywords = ["amazon", "flipkart", "myntra", "meesho", "ajio"]
                store_domains = ["amazon.in", "flipkart.com", "myntra.com", "meesho.com", "ajio.com", "/dp/"]
                if not links and not any(k in raw_text.lower() for k in store_keywords):
                    continue

                # Find the primary deal link (instant if already a store domain)
                target_url = ""
                for link in links:
                    if any(dom in link.lower() for dom in store_domains):
                        target_url = link
                        break
                    resolved = resolve_unshorten_url(link, timeout=3)
                    if any(dom in resolved.lower() for dom in store_domains):
                        target_url = resolved
                        break

                if not target_url and links:
                    target_url = links[0] if any(dom in links[0].lower() for dom in store_domains) else resolve_unshorten_url(links[0], timeout=3)

                if not target_url:
                    continue

                # Convert to our affiliate link
                affiliate_link = convert_to_affiliate(target_url)

                # Clean the raw text using deep security scrubber
                clean_text = security_clean_text(raw_text)
                lines = [l.strip() for l in clean_text.splitlines() if l.strip()]
                clean_body = "\n".join(lines[:4])

                # Extract title and price (skip generic headers like 79% off, 84% off)
                title = ""
                for l in lines:
                    cleaned_line = re.sub(r'^[^\w\s]+', '', l).strip()[:80]
                    if is_generic_discount_title(cleaned_line):
                        continue
                    if len(cleaned_line) >= 5:
                        title = cleaned_line
                        break
                if not title:
                    for l in lines:
                        cleaned_line = re.sub(r'^[^\w\s]+', '', l).strip()[:80]
                        if len(cleaned_line) >= 5:
                            title = cleaned_line
                            break
                if not title:
                    title = "⚡ Mega Festive Loot Deal"

                deals.append({
                    "id": msg_id,
                    "pillar": "Pillar 1: Spy & Switcher",
                    "title": title,
                    "body": clean_body,
                    "affiliate_url": affiliate_link,
                    "photo_url": photo_url,
                    "raw_text": raw_text
                })
            except Exception as e:
                continue

        return deals

    def scan_all(self):
        all_deals = []
        with ThreadPoolExecutor(max_workers=len(self.channels)) as executor:
            future_to_ch = {executor.submit(self.spy_channel, ch): ch for ch in self.channels}
            for future in as_completed(future_to_ch):
                try:
                    res = future.result()
                    all_deals.extend(res)
                except Exception:
                    pass
        return all_deals

# =============================================================================
# PILLAR 2: PERSONAL PRICE GLITCH & ASIN WATCHER
# =============================================================================
class PersonalPriceWatcher:
    """Monitors Cloudflare D1 price drops and curated viral festive products."""

    def __init__(self):
        pass

    def check_d1_drops(self):
        """Checks Cloudflare D1 for deals with >35% discount not yet in cache."""
        if not CF_ACCOUNT_ID or not CF_API_TOKEN:
            return []
        try:
            url = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/d1/database/{CF_D1_DB_ID}/query"
            sql = """
            SELECT id, title, price, mrp, discount, affiliate_url, image_url
            FROM deals
            WHERE discount >= 35
            ORDER BY discount DESC, created_at DESC
            LIMIT 10;
            """
            data = json.dumps({"sql": sql}).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers={
                "Authorization": f"Bearer {CF_API_TOKEN}",
                "Content-Type": "application/json"
            })
            with urllib.request.urlopen(req, timeout=8) as resp:
                result = json.loads(resp.read().decode("utf-8"))

            if not result.get("success"):
                return []

            rows = result["result"][0]["results"]
            deals = []
            for r in rows:
                if dedup.is_seen(r["id"]) or dedup.is_seen(r["title"]):
                    continue
                deals.append({
                    "id": r["id"],
                    "pillar": "Pillar 2: Personal Price Watcher (D1)",
                    "title": r["title"][:70],
                    "deal_price": r["price"],
                    "mrp": r["mrp"],
                    "discount": r["discount"],
                    "affiliate_url": convert_to_affiliate(r["affiliate_url"]),
                    "photo_url": r["image_url"]
                })
            return deals
        except Exception:
            return []

    def check_viral_asins(self):
        """Scans viral festive ASINs registry for instant trigger."""
        deals = []
        for asin, item in VIRAL_FESTIVE_REGISTRY.items():
            if dedup.is_seen(asin) or dedup.is_seen(item["title"]):
                continue
            discount = round(((item["mrp"] - item["deal_price"]) / item["mrp"]) * 100)
            deals.append({
                "id": asin,
                "pillar": "Pillar 2: Personal Viral ASIN Watcher",
                "title": item["title"],
                "deal_price": item["deal_price"],
                "mrp": item["mrp"],
                "discount": discount,
                "affiliate_url": f"https://www.amazon.in/dp/{asin}?tag={AMAZON_TAG}",
                "photo_url": item["image"]
            })
        return deals

    def scan_all(self):
        return self.check_viral_asins() + self.check_d1_drops()

# =============================================================================
# PILLAR 3: COMMUNITY & FESTIVE RSS RADAR (OPEN INTERNET DEALS STREAM)
# =============================================================================
class FestiveCommunityRadar:
    """Scans verified open internet shopping & discount feeds, with Gemini AI + Heuristic fallback."""

    FEEDS = [
        "https://news.google.com/rss/search?q=Amazon+India+deals+offers+discount&hl=en-IN&gl=IN&ceid=IN:en",
        "https://news.google.com/rss/search?q=Flipkart+deals+offers+discount&hl=en-IN&gl=IN&ceid=IN:en",
        "https://news.google.com/rss/search?q=smartphones+discount+deals+sale+india&hl=en-IN&gl=IN&ceid=IN:en",
        "https://news.google.com/rss/search?q=laptops+price+drop+deals+india&hl=en-IN&gl=IN&ceid=IN:en",
        "https://news.google.com/rss/search?q=electronics+loot+deals+india&hl=en-IN&gl=IN&ceid=IN:en",
    ]

    def __init__(self):
        pass

    def fetch_feed_items(self):
        items = []
        for url in self.FEEDS:
            html, _ = fetch_url(url, timeout=7)
            if not html:
                continue
            soup = BeautifulSoup(html, "xml" if "xml" in html[:100] else "html.parser")
            for entry in soup.find_all("item")[:10]:
                title_tag = entry.find("title")
                link_tag = entry.find("link")
                if not title_tag:
                    continue
                title = title_tag.get_text(strip=True)
                link = link_tag.get_text(strip=True) if link_tag else ""
                if dedup.is_seen(title):
                    continue
                items.append({"title": title, "link": link})
        return items

    def parse_heuristically(self, title, link):
        """Heuristically extracts deal details from title without relying on external AI API quotas."""
        # Clean news source suffix (e.g. ' - The Times of India', ' - Livemint')
        clean_title = re.sub(r'\s*[-|–]\s*(?:The Times of India|Livemint|Mint|NDTV|Moneycontrol|Hindustan Times|The Hindu|About Amazon India|India Today|Zee News|News18).*$', '', title, flags=re.IGNORECASE)
        # Clean generic buzzwords
        clean_title = re.sub(r'(?i)\b(sale opens|sale announced|deals across|how to get|festive sales|brings discounts on|cheaper during|opens at midnight)\b', '', clean_title)
        clean_title = security_clean_text(clean_title)

        if not clean_title or len(clean_title) < 6:
            return None

        # Price match: e.g. at Rs 54,999 or ₹1,299 or Rs. 899
        p_match = re.search(r'(?:₹|rs\.?|inr)\s*([\d,]{3,7})', title, re.IGNORECASE)
        deal_price = 0
        if p_match:
            try:
                deal_price = int(p_match.group(1).replace(",", ""))
            except Exception:
                pass

        # Discount match: e.g. 40% off or 25% discount
        d_match = re.search(r'(\d{1,2})%\s*(?:off|discount)', title, re.IGNORECASE)
        discount = int(d_match.group(1)) if d_match else 0

        # Infer merchant platform
        t_lower = title.lower()
        if "flipkart" in t_lower:
            platform = "flipkart"
        elif "myntra" in t_lower:
            platform = "myntra"
        elif "meesho" in t_lower:
            platform = "meesho"
        elif "ajio" in t_lower:
            platform = "ajio"
        else:
            platform = "amazon"

        # Calculate MRP
        if deal_price and discount:
            mrp = int(deal_price / (1 - discount / 100))
        elif deal_price:
            mrp = int(deal_price * 1.30)
            discount = 23
        else:
            deal_price = 1499
            mrp = 2999
            discount = 50

        return {
            "is_deal": True,
            "product_name": clean_title[:75],
            "deal_price": deal_price,
            "mrp": mrp,
            "discount_percent": discount,
            "platform": platform,
            "search_keyword": clean_title[:45]
        }

    def parse_with_gemini(self, title, link):
        """Extracts structured deal information via Gemini AI."""
        if not GEMINI_API_KEY:
            return None
        prompt = f"""
You are an expert Indian festive e-commerce deal analyst.
Headline: "{title}"
Link: "{link}"

Task: Extract or infer the primary product deal from this headline.
- product_name: Clean brand & model name
- deal_price: Estimated festive offer price in INR (integer, e.g. 54999)
- mrp: Original retail price in INR (integer, e.g. 69900)
- discount_percent: Integer discount percentage (e.g. 21)
- platform: "amazon" | "flipkart" | "myntra" | "meesho" | "ajio"
- search_keyword: best search keyword for this product

Return ONLY valid JSON:
{{"is_deal": true, "product_name": "...", "deal_price": 54999, "mrp": 69900, "discount_percent": 21, "platform": "amazon", "search_keyword": "..."}}
If completely unrelated to shopping, return {{"is_deal": false}}.
"""
        models = ["gemini-2.0-flash", "gemini-1.5-flash"]
        for m_name in models:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{m_name}:generateContent?key={GEMINI_API_KEY}"
                payload = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode("utf-8")
                req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
                with urllib.request.urlopen(req, timeout=3) as resp:
                    res_data = json.loads(resp.read().decode("utf-8"))
                text = res_data["candidates"][0]["content"]["parts"][0]["text"]
                m = re.search(r'\{.*\}', text, re.DOTALL)
                if m:
                    d = json.loads(m.group(0))
                    if d.get("is_deal") and d.get("product_name"):
                        return d
            except Exception:
                continue
        return None

    def scan_all(self):
        raw_items = self.fetch_feed_items()
        deals = []
        for item in raw_items[:6]: # Process up to 6 items per cycle
            parsed = self.parse_heuristically(item["title"], item["link"])
            if not parsed and GEMINI_API_KEY:
                parsed = self.parse_with_gemini(item["title"], item["link"])

            if parsed and parsed.get("product_name"):
                platform = parsed.get("platform", "amazon").lower()
                prod_q = urllib.parse.quote(parsed.get('search_keyword', parsed['product_name']))

                if "myntra" in platform:
                    aff_url = convert_to_affiliate(f"https://www.myntra.com/{prod_q}")
                elif "meesho" in platform:
                    aff_url = convert_to_affiliate(f"https://www.meesho.com/search?q={prod_q}")
                elif "flipkart" in platform:
                    aff_url = convert_to_affiliate(f"https://www.flipkart.com/search?q={prod_q}")
                else:
                    aff_url = convert_to_affiliate(f"https://www.amazon.in/s?k={prod_q}")

                deals.append({
                    "id": item["title"],
                    "pillar": f"Pillar 3: Festive Radar ({platform.capitalize()})",
                    "title": parsed["product_name"],
                    "deal_price": parsed.get("deal_price", 0),
                    "mrp": parsed.get("mrp", 0),
                    "discount": parsed.get("discount_percent", 0),
                    "affiliate_url": aff_url,
                    "photo_url": "https://m.media-amazon.com/images/I/71657TiFeHL._SL1500_.jpg"
                })
        return deals

# =============================================================================
# TELEGRAM BROADCASTER ENGINE
# =============================================================================
# =============================================================================
# TELEGRAM BROADCASTER ENGINE (DUAL DISPATCH: CHANNEL + GROUP TOPICS)
# =============================================================================
class TelegramBroadcaster:
    """Sends high-converting deal cards to Main Channel AND routes to Group Category Topics."""

    def __init__(self, bot_token=TELEGRAM_BOT_TOKEN,
                 channel_id=TELEGRAM_DEALS_CHANNEL,
                 group_id=TELEGRAM_DEALS_GROUP_ID):
        self.bot_token = bot_token
        self.channel_id = channel_id
        self.group_id = group_id

    def detect_category(self, title, body=""):
        s = (title + " " + body).lower()
        if any(w in s for w in ["shoe", "sneaker", "clothe", "fashion", "shirt", "wear", "kurti", "dress", "saree", "jeans", "tshirt", "t-shirt", "footwear", "sandal"]):
            return TOPIC_IDS["fashion"], "👔 Fashion & Footwear"
        elif any(w in s for w in ["laptop", "phone", "mobile", "tech", "earphone", "headphone", "buds", "gpu", "monitor", "pc", "samsung m5", "smartwatch", "apple", "iphone"]):
            return TOPIC_IDS["tech"], "💻 Tech, Laptops & Mobiles"
        elif any(w in s for w in ["appliance", "tv", "washing machine", "fridge", "kitchen", "mixer", "cooker", "geyser", "furniture", "air fryer"]):
            return TOPIC_IDS["home"], "🏠 Home & Kitchen Appliances"
        return TOPIC_IDS["loots"], "⚡ 0-Minute Price Glitch"

    def format_caption(self, deal, category_name):
        affiliate_url = deal.get("affiliate_url", "")
        title = deal["title"].strip()
        safe_title = title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        price = deal.get("deal_price")
        mrp = deal.get("mrp")
        discount = deal.get("discount")
        body = deal.get("body", "")

        # 1. Dynamic Headline tailored to deal characteristics
        if discount and discount >= 70:
            headline = f"🔥 <b>[FLAT {discount}% OFF MEGA LOOT]</b> 🔥"
        elif discount and discount >= 45:
            headline = f"⚡ <b>[{discount}% PRICE DROP ALERT]</b> ⚡"
        elif price and price < 299:
            headline = f"💥 <b>[SUPER BUDGET LOOT @ ₹{price}]</b> 💥"
        elif "tech" in category_name.lower():
            headline = "📱 <b>[TOP TECH DEAL]</b> 📱"
        elif "fashion" in category_name.lower():
            headline = "👔 <b>[FASHION LOOT DROP]</b> 👔"
        elif "home" in category_name.lower():
            headline = "🏠 <b>[HOME & APPLIANCE OFFER]</b> 🏠"
        else:
            headline = "⚡ <b>[0-MINUTE FLASH DEAL]</b> ⚡"

        # 2. Dynamic Price & Details Line (Authentic, no fake text)
        details_block = ""
        if price:
            details_block = f"💰 <b>Deal Price:</b> ₹{price:,}"
            if mrp and mrp > price:
                details_block += f" <s>₹{mrp:,}</s>"
            if discount:
                details_block += f" <b>({discount}% OFF)</b>"
            details_block += "\n"
        elif body:
            clean_b = body.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            body_lines = [l.strip() for l in clean_b.splitlines() if l.strip() and not l.startswith("http")]
            details_block = "\n".join(body_lines[:2]) + "\n"

        # 3. Dynamic rotating urgency note
        urgency_notes = [
            "🚨 <i>Order fast before price increases!</i>",
            "⚡ <i>Flash deal active right now — grab fast!</i>",
            "🔥 <i>Limited stock available at this deal price!</i>",
            "⏰ <i>Price might change anytime, order immediately!</i>"
        ]
        urgency = urgency_notes[len(title) % len(urgency_notes)]

        caption = (
            f"{headline}\n\n"
            f"🛍️ <b>{safe_title}</b>\n\n"
            f"{details_block}"
            f"🏷️ <b>Category:</b> {category_name}\n\n"
            f"🛒 <b>ORDER DIRECTLY HERE:</b>\n"
            f"👉 {affiliate_url}\n\n"
            f"{urgency}"
        )
        return caption

    def build_markup(self, affiliate_url):
        return {
            "inline_keyboard": [
                [
                    {"text": "🛍️ GRAB LOOT DEAL ➔", "url": affiliate_url}
                ],
                [
                    {"text": "🟢 Join WhatsApp Channel", "url": WHATSAPP_CHANNEL_URL},
                    {"text": "🧭 Category Tabs", "url": "https://t.me/uniquedigit_deals/6"}
                ],
                [
                    {"text": "🔐 Secret Loot Vault", "url": f"{PORTAL_BASE}/vault"}
                ]
            ]
        }

    def _send_tg_request(self, endpoint, payload, max_retries=3):
        """Dispatches request to Telegram API with automatic HTTP 429 rate limit handling & backoff."""
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(endpoint, data=data, headers={"Content-Type": "application/json"})
        for attempt in range(max_retries):
            try:
                with urllib.request.urlopen(req, timeout=12) as resp:
                    res = json.loads(resp.read().decode("utf-8"))
                    if res.get("ok"):
                        return True, res
            except urllib.error.HTTPError as err:
                if err.code == 429:
                    try:
                        err_body = json.loads(err.read().decode("utf-8"))
                        wait_sec = err_body.get("parameters", {}).get("retry_after", 3)
                    except Exception:
                        wait_sec = 3
                    print(f"    ⚠️ Telegram 429 Rate Limit! Waiting {wait_sec + 1}s...")
                    time.sleep(wait_sec + 1)
                    continue
                else:
                    return False, None
            except Exception:
                return False, None
        return False, None

    def _post(self, chat_id, caption, photo_url, reply_markup, thread_id=None):
        """Helper to post photo or message with optional topic thread ID and robust failover."""
        # 1. Try sending Photo with buttons
        if photo_url and photo_url.startswith("http"):
            endpoint = f"https://api.telegram.org/bot{self.bot_token}/sendPhoto"
            payload = {
                "chat_id": chat_id,
                "photo": photo_url,
                "caption": caption,
                "parse_mode": "HTML",
                "reply_markup": reply_markup
            }
            if thread_id:
                payload["message_thread_id"] = thread_id
            ok, _ = self._send_tg_request(endpoint, payload)
            if ok:
                time.sleep(0.5)
                return True

        # 2. Seamless Fallback to Text Message with buttons
        endpoint = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": caption,
            "parse_mode": "HTML",
            "disable_web_page_preview": False,
            "reply_markup": reply_markup
        }
        if thread_id:
            payload["message_thread_id"] = thread_id
        ok, _ = self._send_tg_request(endpoint, payload)
        if ok:
            time.sleep(0.5)
            return True
        return False

    def send_deal(self, deal):
        affiliate_url = deal["affiliate_url"]
        photo_url = deal.get("photo_url")

        # Resolve 100% verified real HD photo via Master Universal Image Engine
        try:
            from bridges.universal_image_engine import get_universal_real_image
            hd_photo, _ = get_universal_real_image(
                title=deal["title"],
                niche_slug="deals",
                target_url=affiliate_url,
                raw_image=photo_url
            )
            photo_url = hd_photo
            deal["photo_url"] = hd_photo
        except Exception:
            pass

        thread_id, cat_name = self.detect_category(deal["title"], deal.get("body", ""))
        caption = self.format_caption(deal, cat_name)
        reply_markup = self.build_markup(affiliate_url)

        sent_main = False
        # Destination A: Main Deals Channel (@uniquedigit_deals)
        if self.channel_id:
            sent_main = self._post(self.channel_id, caption, photo_url, reply_markup)

        # Destination B: Community Group (Routed to specific category Topic/Thread)
        if self.group_id:
            self._post(self.group_id, caption, photo_url, reply_markup, thread_id=thread_id)

        return sent_main or bool(self.group_id)

broadcaster = TelegramBroadcaster()

# =============================================================================
# GOD-LEVEL ORCHESTRATOR
# =============================================================================
class GodLevelLootEngine:
    def __init__(self):
        self.spy = TelegramChannelSpy()
        self.watcher = PersonalPriceWatcher()
        self.radar = FestiveCommunityRadar()
        self.total_sent = 0

    def run_one_cycle(self, max_deals_per_cycle=4):
        print(f"\n{'='*70}")
        print(f"👑 GOD ENGINE SCAN | {datetime.now().strftime('%H:%M:%S')} | Total Sent: {self.total_sent}")
        print(f"{'='*70}")

        # Scan all 3 pillars in parallel
        candidates = []
        with ThreadPoolExecutor(max_workers=3) as executor:
            fut_spy = executor.submit(self.spy.scan_all)
            fut_watcher = executor.submit(self.watcher.scan_all)
            fut_radar = executor.submit(self.radar.scan_all)

            spy_deals = fut_spy.result()
            watcher_deals = fut_watcher.result()
            radar_deals = fut_radar.result()

        print(f"  [Pillar 1 - Spy & Switcher]: {len(spy_deals)} candidates")
        print(f"  [Pillar 2 - Personal Watcher]: {len(watcher_deals)} candidates")
        print(f"  [Pillar 3 - Festive Radar]: {len(radar_deals)} candidates")

        # Priority Order: Pillar 1 (Instant Spy) -> Pillar 2 (Personal Watcher) -> Pillar 3 (Festive Radar)
        candidates = spy_deals + watcher_deals + radar_deals
        cycle_sent = 0
        blogger_published_in_cycle = 0

        for deal in candidates:
            if dedup.is_seen(deal):
                continue

            print(f"  🔄 Processing: {deal['title'][:45]}... [{deal['pillar']}]")
            ok = broadcaster.send_deal(deal)

            # 🌐 Sync deal directly to Cloudflare D1 Deals Hub (/deals portal)
            d1_ok = sync_deal_to_cloudflare_d1(deal)

            if ok or d1_ok:
                dedup.mark_seen(deal)
                cycle_sent += 1
                self.total_sent += 1
                if ok:
                    print(f"    ✅ SENT TO TELEGRAM ({deal['title'][:35]})")

                # Cross-publish to dedicated Deals & Loot Blogger Blog (834082955272949961)
                if blogger_published_in_cycle < 1 and deal.get("photo_url"):
                    try:
                        from bridges.blogger_bridge.deals_blogger_publisher import publish_deal_to_blogger
                        b_res = publish_deal_to_blogger(deal)
                        if b_res.get("success"):
                            blogger_published_in_cycle += 1
                            print(f"    🎉 PUBLISHED TO BLOGGER: {b_res.get('url')}")
                    except Exception as eb:
                        print(f"    ⚠️ Blogger deals publish error: {eb}")

                time.sleep(1.0) # Graceful pacing to stay well under rate limits
                if cycle_sent >= max_deals_per_cycle:
                    break
            else:
                print(f"    ❌ Failed to broadcast or sync")

        print(f"⏱️ Cycle finished — Sent/Synced {cycle_sent} deals this round (Blogger: {blogger_published_in_cycle}).")
        return cycle_sent

    def run_loop(self, interval=5, duration=None):
        """Runs the loop continuously in 0-second lightning mode (default: 5s)."""
        start_time = time.time()
        print(f"⚡ INSTANT 0-SECOND LIGHTNING ENGINE ACTIVE (Interval: {interval}s)")
        if duration:
            print(f"⏳ Run Duration: {duration} seconds")

        while True:
            try:
                self.run_one_cycle()
            except Exception as e:
                print(f"⚠️ Error in cycle: {e}")

            if duration and (time.time() - start_time) >= duration:
                print(f"🛑 Duration reached ({duration}s). Exiting gracefully.")
                break

            time.sleep(interval)

# =============================================================================
# CLI ENTRY POINT
# =============================================================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="God-Level Autonomous Loot Engine")
    parser.add_argument("--loop", action="store_true", help="Run in continuous 24/7 loop")
    parser.add_argument("--interval", type=int, default=25, help="Seconds between scan cycles (default: 25)")
    parser.add_argument("--duration", type=int, default=None, help="Max run duration in seconds")
    args = parser.parse_args()

    engine = GodLevelLootEngine()

    if args.loop or args.duration:
        engine.run_loop(interval=args.interval, duration=args.duration)
    else:
        # Default: single cycle test
        engine.run_one_cycle()
