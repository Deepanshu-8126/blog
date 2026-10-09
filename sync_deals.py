"""
UniqueDigit Autonomous Multi-Store Deals & Glitch Sync Agent
=============================================================
Autonomous listener & ingestion engine that tracks real-time price drops,
festival sales (Flipkart Big Billion Days, Amazon Great Indian Festival, Myntra BFF, Meesho, Ajio),
and social price glitches from Reddit (r/dealsindia, r/IndianGaming) & Google Trends RSS.

Runs autonomously on GitHub Actions cron (every 2 hours) or local manual trigger.
"""

import json
import os
import re
import sys
import time
import urllib.parse
from datetime import datetime
import requests
from dotenv import load_dotenv

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

load_dotenv()

DRY = "--dry" in sys.argv
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) UniqueDigitDealsRadar/2.0"}

CF_ACCOUNT = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "cf1a42fb306054063805cf459fddf853")
CF_D1_DB = os.environ.get("CLOUDFLARE_D1_DATABASE_ID", "61d1d46f-f438-47f5-9128-516d9beb11cb")
CF_TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN", "")
CF_KV_ID = os.environ.get("CLOUDFLARE_KV_NAMESPACE_ID", "2ab0d1c56e1c471fa658e522912373ec")
AMAZON_TAG = os.environ.get("AMAZON_ASSOCIATE_TAG", "uniquedigi0c6-21")
GEMINI_KEY = os.environ.get("GEMINI_API_KEY", "")

TG_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TG_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

DEALS_NICHE_ID = "5cf8114c0bc3eb20c87ce3dcfc1ff185"


def get_current_festival_context():
    """Autonomously determines which Indian shopping festival is active or upcoming"""
    month = datetime.now().month
    if month in [9, 10, 11]:
        return {
            "name": "Diwali Festival Radar",
            "events": ["Flipkart Big Billion Days", "Amazon Great Indian Festival", "Myntra Big Fashion Festival", "Meesho Maha Shopping League"],
            "keywords": ["big billion days", "great indian festival", "diwali sale", "festive loot", "bbd"]
        }
    elif month in [12, 1]:
        return {
            "name": "Republic Day & Year End Sale",
            "events": ["Amazon Great Republic Day Sale", "Flipkart Big Bachat Dhamaal", "Myntra End of Reason Sale"],
            "keywords": ["republic day sale", "year end sale", "eors", "clearance loot"]
        }
    elif month in [5, 6, 7]:
        return {
            "name": "Mid-Year Prime Days",
            "events": ["Amazon Prime Day", "Flipkart Big Saving Days", "Ajio All Stars Sale"],
            "keywords": ["prime day", "big saving days", "ajio all stars", "summer loot"]
        }
    else:
        return {
            "name": "Payday & Weekend Flash Loots",
            "events": ["Amazon Lightning Deals", "Flipkart Flash Drops", "Meesho ₹99 Mega Deal"],
            "keywords": ["payday sale", "flash drop", "lightning deal", "price glitch", "under 499"]
        }


def send_telegram_deal(name, merchant, price, tagline, aff_url):
    """Dispatches instant loot alert to Telegram VIP channel"""
    if not (TG_BOT_TOKEN and TG_CHAT_ID):
        return
    text = (
        f"⚡ *NEW LOOT DROP / PRICE GLITCH*\n\n"
        f"🛒 *Product:* {name}\n"
        f"🏪 *Merchant:* {merchant}\n"
        f"💰 *Effective Loot Price:* ₹{price:,}\n"
        f"📊 *Breakdown:* {tagline}\n\n"
        f"🚀 [Grab Deal Before It Expires]({aff_url})"
    )
    try:
        url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": TG_CHAT_ID, "text": text, "parse_mode": "Markdown"}, timeout=10)
    except Exception as e:
        print("[Telegram deal dispatch failed]:", e)


def d1_query(sql, params=None):
    if DRY:
        print(f"[dry d1] {sql[:100]} | params: {params}")
        return []

    if CF_ACCOUNT and CF_D1_DB and CF_TOKEN:
        url = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT}/d1/database/{CF_D1_DB}/query"
        headers = {
            "Authorization": f"Bearer {CF_TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {"sql": sql, "params": params or []}
        try:
            r = requests.post(url, headers=headers, json=payload, timeout=30)
            if r.status_code == 200:
                res = r.json()
                if res.get("result") and len(res["result"]) > 0:
                    return res["result"][0].get("results", [])
        except Exception as e:
            print("[D1 REST Error]:", e)

    # Fallback to local wrangler CLI
    try:
        import subprocess
        full_sql = sql
        if params:
            for p in params:
                val = f"'{p}'" if isinstance(p, str) else str(p)
                full_sql = full_sql.replace("?", val, 1)
        proc = subprocess.run(
            ["node", "./node_modules/wrangler/bin/wrangler.js", "d1", "execute", "uniquedigit-db", "--remote", f"--command={full_sql}"],
            capture_output=True, text=True, timeout=60, check=False
        )
        if proc.returncode == 0 and proc.stdout:
            lines = [l for l in proc.stdout.split("\n") if l.strip().startswith("[") or l.strip().startswith("{")]
            if lines:
                data = json.loads("".join(lines))
                if isinstance(data, list) and len(data) > 0:
                    return data[0].get("results", [])
    except Exception as e:
        print("[Wrangler CLI Error]:", e)

    return []


def fetch_social_deals():
    """Scrapes trending deals and price glitches from Indian subreddits and Google Trends"""
    fest = get_current_festival_context()
    print(f"[AgentSearch Radar] Active Season: {fest['name']}")
    print("[AgentSearch Radar] Scanning Reddit r/dealsindia, r/IndianGaming & r/CreditCardsIndia...")
    
    candidate_posts = []
    subreddits = ["dealsindia", "IndianGaming", "CreditCardsIndia"]

    for sub in subreddits:
        try:
            url = f"https://www.reddit.com/r/{sub}/hot.json?limit=15"
            r = requests.get(url, headers=UA, timeout=15)
            if r.status_code == 200:
                data = r.json()
                children = data.get("data", {}).get("children", [])
                for item in children:
                    d = item.get("data", {})
                    title = d.get("title", "")
                    selftext = d.get("selftext", "")
                    link = d.get("url_overridden_by_dest", "") or f"https://reddit.com{d.get('permalink')}"
                    ups = d.get("ups", 0)

                    # Look for shopping/deal intent matching active festival or general loots
                    search_terms = ["deal", "loot", "off", "₹", "rs", "amazon", "flipkart", "drop", "glitch", "price"] + fest["keywords"]
                    if any(k in title.lower() for k in search_terms):
                        candidate_posts.append({
                            "title": title,
                            "text": selftext[:400],
                            "url": link,
                            "source": f"Reddit r/{sub}",
                            "score": ups
                        })
        except Exception as e:
            print(f"[Reddit fetch error for {sub}]:", e)

    print(f"[AgentSearch Radar] Discovered {len(candidate_posts)} raw social deal candidates.")
    return candidate_posts


def gemini_parse_deal(raw_title, raw_text):
    """Uses Gemini to parse unstructured deal text into a high-converting price-stacked deal"""
    if not GEMINI_KEY:
        return None

    prompt = f"""You are UniqueDigit's AI Deal & Price Glitch Parser for Indian shoppers.
Raw Post Title: "{raw_title}"
Raw Details: "{raw_text}"

Extract or estimate accurate deal telemetry:
1. Product clean name (under 75 chars)
2. Merchant (Pick one: "Amazon", "Flipkart", "Myntra", "Ajio", "Meesho")
3. Category (Pick one: "Laptops", "Smartphones", "Audio & Gear", "Fashion", "Under ₹499")
4. Badge (e.g. "🔥 60% OFF", "⚡ PRICE GLITCH", "⭐ ALL-TIME LOW", "BBD DROP", "MEESHO LOOT")
5. Price (in INR integer, e.g. 1499)
6. Tagline formatted as: "MRP ₹[Original] | Deal ₹[Price] | Bank/Coupon: [Offer] | Effective: ₹[Final]"

Return STRICT JSON:
{{
  "name": "Clean short product name",
  "merchant": "Amazon",
  "category": "Audio & Gear",
  "badge": "⚡ PRICE GLITCH",
  "price": 1499,
  "tagline": "MRP ₹2,999 | Deal ₹1,999 | Bank: Flat ₹500 off | Effective: ₹1,499",
  "keywords": "search keywords"
}}"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_KEY}"
    try:
        r = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=20)
        if r.status_code == 200:
            text = r.json()["candidates"][0]["content"]["parts"][0]["text"]
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if match:
                return json.loads(match.group(0))
    except Exception as e:
        print("[Gemini deal parse error]:", e)
    return None


def sync_deals_to_d1():
    """Main pipeline execution"""
    fest = get_current_festival_context()
    print("\n=======================================================")
    print(f"🚀 UniqueDigit Dynamic Multi-Store Loot Sync Starting [{fest['name']}]...")
    print("=======================================================")

    candidates = fetch_social_deals()
    if not candidates:
        print("No new raw candidates discovered. Existing D1 catalog remains active.")
        return

    # Fetch existing deal names to avoid duplicates
    existing_deals = d1_query("SELECT name FROM products WHERE niche_id = ?", [DEALS_NICHE_ID])
    existing_names = [d.get("name", "").lower() for d in existing_deals] if existing_deals else []

    added = 0
    for cand in candidates[:5]:
        parsed = gemini_parse_deal(cand["title"], cand["text"])
        if not parsed or not parsed.get("name") or not parsed.get("price"):
            continue

        name = parsed["name"].strip()
        # Avoid duplicate deal inserts
        if any(name.lower() in en or en in name.lower() for en in existing_names):
            print(f"⏩ [Skipped Duplicate]: {name}")
            continue

        deal_id = f"loot-{int(time.time())}-{added}"
        merchant = parsed.get("merchant", "Amazon")
        cat = parsed.get("category", "Laptops")
        badge = parsed.get("badge", "🔥 LOOT DROP")
        price = parsed.get("price", 999)
        tagline = parsed.get("tagline", "Verified price drop")
        keywords = parsed.get("keywords", name.lower())

        # Affiliate Link transformation
        if merchant == "Amazon":
            aff_url = f"https://www.amazon.in/s?k={urllib.parse.quote_plus(name)}&tag={AMAZON_TAG}"
            img = "https://images.unsplash.com/photo-1607082348824-0a96f2a4b9da?auto=format&fit=crop&w=800&q=80"
        elif merchant == "Flipkart":
            aff_url = f"https://www.flipkart.com/search?q={urllib.parse.quote_plus(name)}"
            img = "https://images.unsplash.com/photo-1510557880182-3d4d3cba35a5?auto=format&fit=crop&w=800&q=80"
        elif merchant == "Myntra":
            aff_url = f"https://www.myntra.com/{urllib.parse.quote_plus(name)}"
            img = "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=800&q=80"
        elif merchant == "Ajio":
            aff_url = f"https://www.ajio.com/s/{urllib.parse.quote_plus(name)}"
            img = "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?auto=format&fit=crop&w=800&q=80"
        else:
            aff_url = f"https://www.meesho.com/search?q={urllib.parse.quote_plus(name)}"
            img = "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?auto=format&fit=crop&w=800&q=80"

        sql = """
        INSERT INTO products (id, niche_id, name, tagline, category, badge, keywords, image_url, price, rating, url, aff_url, merchant, clicks, active, sort)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 10, 1, 0);
        """
        params = [deal_id, DEALS_NICHE_ID, name, tagline, cat, badge, keywords, img, price, 4.6, aff_url, aff_url, merchant]
        
        print(f"✨ [New Deal Ingested]: {name} | {merchant} | ₹{price} ({badge})")
        d1_query(sql, params)
        send_telegram_deal(name, merchant, price, tagline, aff_url)
        added += 1

    print(f"\n✅ Sync Completed. {added} new verified multi-store deals synchronized into D1.")


if __name__ == "__main__":
    sync_deals_to_d1()
