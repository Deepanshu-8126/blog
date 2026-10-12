"""
UniqueDigit daily pipeline (All-in-One Cloudflare D1 Edition)

Usage:
  python pipeline.py                  # all active niches
  python pipeline.py --niche ai-tools # one niche
  python pipeline.py --dry            # no DB writes, prints only

Env:
  CLOUDFLARE_ACCOUNT_ID
  CLOUDFLARE_D1_DATABASE_ID
  CLOUDFLARE_API_TOKEN
  GEMINI_API_KEY
Optional:
  GROK_API_KEY, TMDB_API_KEY, POSTS_PER_NICHE, AMAZON_ASSOCIATE_TAG
"""
import json, os, re, sys, time, uuid, urllib.parse, subprocess
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

from dotenv import load_dotenv
load_dotenv()

import requests
import trafilatura

DRY = "--dry" in sys.argv
ONLY = sys.argv[sys.argv.index("--niche") + 1] if "--niche" in sys.argv else None

GEMINI_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite")
GROK_KEY = os.environ.get("GROK_API_KEY")
GROK_MODEL = os.environ.get("GROK_MODEL", "grok-4")
TMDB_KEY = os.environ.get("TMDB_API_KEY")
GEO = os.environ.get("TRENDS_GEO", "IN")
N_POSTS = int(os.environ.get("POSTS_PER_NICHE", "2"))
AMAZON_TAG = os.environ.get("AMAZON_ASSOCIATE_TAG", "uniquedigi0c6-21")
UA = {"User-Agent": "UniqueDigitBot/1.0 (contact: info@uniquedigit.in)"}

CF_ACCOUNT = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "cf1a42fb306054063805cf459fddf853")
CF_D1_DB = os.environ.get("CLOUDFLARE_D1_DATABASE_ID", "61d1d46f-f438-47f5-9128-516d9beb11cb")
CF_TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN", "")
CF_KV_ID = os.environ.get("CLOUDFLARE_KV_NAMESPACE_ID", "2ab0d1c56e1c471fa658e522912373ec")

TG_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TG_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")
TG_DEALS_CHANNEL = os.environ.get("TELEGRAM_DEALS_CHANNEL", "@uniquedigit_deals")
TG_DEALS_GROUP_ID = os.environ.get("TELEGRAM_DEALS_GROUP_ID", "-1004335990773")
TOPIC_IDS = {
    "loots": 3,      # ⚡ 0-Minute Loots & Glitches
    "tech": 4,       # 💻 Tech, Laptops & Mobiles
    "fashion": 5,    # 👔 Clothes, Shoes & Fashion
    "home": 6        # 🏠 Home Appliances & TV
}
PORTAL_BASE = os.environ.get("PORTAL_BASE_URL", "https://uniquedigit-viral-hub.pages.dev")
AFFILIATE_DISCLAIMER = "\n\n---\n*Disclaimer: UniqueDigit participates in affiliate programs including Amazon Associates. When you purchase through links on our site, we may earn an affiliate commission at no extra cost to you.*"


# ---------- Dual-Destination Telegram Dispatcher ----------
def send_telegram(title, niche_name, post_slug, niche_slug="viral", image_url=None, deal_meta=None):
    if not TG_BOT_TOKEN:
        return

    post_url = f"{PORTAL_BASE}/{niche_slug}/{post_slug}"
    safe_title = str(title).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    safe_niche = str(niche_name).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    # 1. Admin Private Channel (Always receives ALL posts: cricket, exam, health, deals)
    if TG_CHAT_ID:
        admin_text = (
            f"📡 <b>[ADMIN RADAR] Published Live</b>\n\n"
            f"📌 <b>Category:</b> {safe_niche} (<code>{niche_slug}</code>)\n"
            f"📝 <b>Title:</b> {safe_title}\n"
            f"🔗 <b>URL:</b> <a href=\"{post_url}\">{post_url}</a>\n\n"
            f"⚡ <i>Auto-synced to Cloudflare D1</i>"
        )
        try:
            url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
            requests.post(url, json={"chat_id": TG_CHAT_ID, "text": admin_text, "parse_mode": "HTML"}, timeout=10)
        except Exception as e:
            print("[Admin Telegram alert failed]:", e)

    # 2. Public Loot Deals Channel (ONLY for Deals, Loot, and Discount Drops!)
    is_loot_deal = (niche_slug in ["deals", "cashback"]) or bool(deal_meta) or any(
        kw in safe_title.lower() for kw in ["deal", "loot", "discount", "off", "price drop", "glitch", "coupon", "steal", "sale"]
    )

    if not is_loot_deal:
        return

    # Extract dynamic deal intelligence if provided
    dm = deal_meta or {}
    mrp = dm.get("mrp")
    steal_price = dm.get("steal_price")
    discount = dm.get("discount", "Steal Drop")
    loot_score = dm.get("loot_score", "9.8/10")
    bank_hack = dm.get("bank_hack", "Extra Instant Card / UPI Discount Active")
    store_name = dm.get("store", "STORE").upper()
    aff_url = dm.get("aff_url") or post_url

    price_block = ""
    if mrp and steal_price:
        price_block = f"📉 <b>MRP:</b> <s>{mrp}</s> ➡️ <b>Steal Price:</b> {steal_price} ({discount})\n"
    elif steal_price:
        price_block = f"📉 <b>Steal Price:</b> {steal_price} ({discount})\n"

    deal_caption = (
        f"⚡ <b>[0-MINUTE PRICE GLITCH ALERT]</b> ⚡\n\n"
        f"🛍️ <b>{safe_title}</b>\n\n"
        f"{price_block}"
        f"🏷️ <b>Category:</b> {safe_niche}\n"
        f"🟢 <b>Loot Score:</b> {loot_score}\n"
        f"💳 <b>Bank Hack / Trick:</b> {bank_hack}\n\n"
        f"✂️ <b>HOW TO CLAIM LOOT:</b>\n"
        f"1. Tap the deal button below.\n"
        f"2. Apply coupon/code on store page if available.\n"
        f"3. Pay via UPI/Card for final lowest price!\n\n"
        f"🚨 <i>Limited Stock! Buy before price increases or stock ends.</i>"
    )

    reply_markup = {
        "inline_keyboard": [
            [
                {"text": f"🛍️ GRAB ON {store_name} ➔", "url": aff_url}
            ],
            [
                {"text": "🧭 Top Category Tabs", "url": "https://t.me/uniquedigit_deals/6"},
                {"text": "🔐 Secret Loot Vault", "url": f"{PORTAL_BASE}/vault"}
            ]
        ]
    }

    # Fetch photo bytes if image available
    photo_bytes = None
    if image_url:
        try:
            if str(image_url).startswith("http"):
                r_img = requests.get(image_url, headers=UA, timeout=7)
                if r_img.status_code == 200 and len(r_img.content) > 1000:
                    photo_bytes = r_img.content
            elif os.path.exists(image_url):
                with open(image_url, "rb") as f:
                    photo_bytes = f.read()
        except Exception as e:
            print("[Image fetch for Telegram failed]:", e)

    # Fallback to local default product image if no remote image
    if not photo_bytes and os.path.exists("public/images/products/iphone_16_pro.jpg"):
        try:
            with open("public/images/products/iphone_16_pro.jpg", "rb") as f:
                photo_bytes = f.read()
        except Exception:
            pass

    def dispatch_tg(chat_id, thread_id=None):
        try:
            if photo_bytes:
                data = {
                    "chat_id": chat_id,
                    "caption": deal_caption,
                    "parse_mode": "HTML",
                    "reply_markup": json.dumps(reply_markup)
                }
                if thread_id:
                    data["message_thread_id"] = thread_id
                files = {"photo": ("deal.jpg", photo_bytes, "image/jpeg")}
                res = requests.post(f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendPhoto", data=data, files=files, timeout=15)
            else:
                payload = {
                    "chat_id": chat_id,
                    "text": deal_caption,
                    "parse_mode": "HTML",
                    "reply_markup": reply_markup
                }
                if thread_id:
                    payload["message_thread_id"] = thread_id
                res = requests.post(f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage", json=payload, timeout=10)
            
            resp_json = res.json()
            if resp_json.get("ok"):
                msg_id = resp_json.get("result", {}).get("message_id")
                # Auto-pin mega price glitch loots
                if msg_id and any(kw in safe_title.lower() for kw in ["glitch", "free", "all-time low", "steal"]):
                    requests.post(
                        f"https://api.telegram.org/bot{TG_BOT_TOKEN}/pinChatMessage",
                        json={"chat_id": chat_id, "message_id": msg_id, "disable_notification": False},
                        timeout=5
                    )
                return True
            else:
                print(f"[Telegram send failed to {chat_id}]:", resp_json.get("description"))
                return False
        except Exception as e:
            print(f"[Telegram dispatch error {chat_id}]:", e)
            return False

    # Destination A: Broadcast to Main Deals Channel
    if TG_DEALS_CHANNEL:
        if dispatch_tg(TG_DEALS_CHANNEL):
            print(f"[Public Deals Channel Broadcast Sent]: {safe_title}")

    # Destination B: Smart AI Forum Topic Routing in Community Group (200k members)
    if TG_DEALS_GROUP_ID:
        lower_str = (safe_title + " " + safe_niche).lower()
        if any(w in lower_str for w in ["clothe", "fashion", "shirt", "shoe", "sneaker", "kurti", "wear", "dress", "saree", "jeans"]):
            thread_id = TOPIC_IDS["fashion"]
        elif any(w in lower_str for w in ["laptop", "phone", "mobile", "tech", "earphone", "headphone", "buds", "gpu", "rtx", "ssd", "monitor", "pc"]):
            thread_id = TOPIC_IDS["tech"]
        elif any(w in lower_str for w in ["appliance", "tv", "washing machine", "fridge", "kitchen", "air fryer", "cooker", "geyser"]):
            thread_id = TOPIC_IDS["home"]
        else:
            thread_id = TOPIC_IDS["loots"]

        if dispatch_tg(TG_DEALS_GROUP_ID, thread_id=thread_id):
            print(f"[Forum Topic Routed -> Thread {thread_id}]: {safe_title}")


# ---------- Google Blogger Multi-Destination Publisher ----------
BLOGGER_ROUTING = {
    # 1. Exams & Sarkari Results -> Dedicated Sarkari Result & Exam Alert Blog
    "exams-results": os.getenv("BLOGGER_EXAM_BLOG_ID", "1366151638291560024"),
    
    # 2. Tech, AI, PC Builds, Deals, Side-Hustles -> Primary AI Tools Hub Blog
    "ai-tools": os.getenv("BLOGGER_AI_BLOG_ID", "2280231208480007821"),
    "pc-builds": os.getenv("BLOGGER_AI_BLOG_ID", "2280231208480007821"),
    "side-hustles": os.getenv("BLOGGER_AI_BLOG_ID", "2280231208480007821"),
    "tech": os.getenv("BLOGGER_AI_BLOG_ID", "2280231208480007821"),
    "deals": os.getenv("BLOGGER_AI_BLOG_ID", "2280231208480007821"),
    "viral": os.getenv("BLOGGER_AI_BLOG_ID", "2280231208480007821"),
}

def send_blogger(title, body_md, tags=None, image_url=None, niche_slug=""):
    """Automatically cross-publishes targeted articles to specific Google Blogger blogs."""
    target_blog_id = BLOGGER_ROUTING.get(niche_slug)
    if not target_blog_id:
        # Keep Blogger topical authority clean
        return None

    try:
        from bridges.blogger_bridge.blogger_publisher import publish_to_blogger
        import markdown
        content_html = markdown.markdown(body_md or "", extensions=['extra', 'tables'])
        res = publish_to_blogger(
            title, 
            content_html, 
            labels=tags, 
            is_draft=False, 
            featured_image=image_url,
            target_blog_id=target_blog_id
        )
        return res
    except Exception as e:
        print(f"[Blogger cross-publish error for {niche_slug}]:", e)
        return None


# ---------- Storage Optimization (Prevent 5GB D1 Bloat) ----------
def cleanup_old_data():
    """Retains last 90 days of posts to keep D1 SQLite lightweight and fast"""
    print("[D1 Storage Optimizer] Pruning articles older than 90 days...")
    d1_query("DELETE FROM posts WHERE published_at < datetime('now', '-90 days')")
    d1_query("DELETE FROM signals WHERE captured_at < datetime('now', '-14 days')")


# ---------- Cloudflare D1 Helpers ----------
def d1_query(sql, params=None):
    if DRY:
        print(f"[dry d1] {sql[:100]} | params: {params}")
        return []

    # 1. Direct Cloudflare REST API (preferred in CI if token present)
    if CF_ACCOUNT and CF_D1_DB and CF_TOKEN:
        url = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT}/d1/database/{CF_D1_DB}/query"
        headers = {
            "Authorization": f"Bearer {CF_TOKEN}",
            "Content-Type": "application/json"
        }
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
                    continue
                else:
                    break
            except Exception as e:
                if attempt == 2:
                    print("[D1 REST query error]:", e)
                time.sleep(1.5 * (attempt + 1))

    # 2. Local/Remote Wrangler CLI execution fallback
    try:
        formatted_sql = sql
        if params:
            for p in params:
                if p is None:
                    formatted_sql = formatted_sql.replace("?", "NULL", 1)
                elif isinstance(p, (int, float)):
                    formatted_sql = formatted_sql.replace("?", str(p), 1)
                else:
                    escaped_str = str(p).replace("'", "''")
                    formatted_sql = formatted_sql.replace("?", f"'{escaped_str}'", 1)

        # Run wrangler directly
        cmd = ["npx", "wrangler", "d1", "execute", "uniquedigit-db", "--remote", "--json", f"--command={formatted_sql}"]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=30, shell=True)
        if res.returncode == 0 and res.stdout:
            start_idx = res.stdout.find("[")
            if start_idx != -1:
                parsed = json.loads(res.stdout[start_idx:])
                if parsed and len(parsed) > 0:
                    return parsed[0].get("results", [])
    except Exception as e:
        print("[Wrangler D1 execution fallback error]:", e)

    return []


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", str(s).lower()).strip("-")[:80]


def gemini(prompt):
    if not GEMINI_KEY:
        print("GEMINI_API_KEY not set")
        return {"title": "Default Title", "summary": "Summary", "body_md": "Body content", "faq": [], "tags": []}
    
    models_to_try = [GEMINI_MODEL, "gemini-3.5-flash-lite", "gemini-3.8-flash", "gemini-flash-latest"]
    # Deduplicate while preserving order
    seen_models = []
    for m in models_to_try:
        if m and m not in seen_models:
            seen_models.append(m)

    for model in seen_models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_KEY}"
        for retry in range(2):
            try:
                r = requests.post(
                    url,
                    json={"contents": [{"parts": [{"text": prompt}]}],
                          "generationConfig": {"responseMimeType": "application/json", "temperature": 0.4}},
                    timeout=90
                )
                r.raise_for_status()
                text = r.json()["candidates"][0]["content"]["parts"][0]["text"]
                return json.loads(text)
            except Exception as e:
                print(f"[Gemini model {model} attempt {retry+1} failed]:", e)
                time.sleep(1)
                continue

    raise RuntimeError("All Gemini models failed")


def grok(prompt):
    if not GROK_KEY:
        return None
    try:
        r = requests.post(
            "https://api.x.ai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROK_KEY}"},
            json={"model": GROK_MODEL, "messages": [{"role": "user", "content": prompt}],
                  "response_format": {"type": "json_object"}},
            timeout=90)
        r.raise_for_status()
        return json.loads(r.json()["choices"][0]["message"]["content"])
    except Exception as e:
        print("grok failed:", e)
        return None


# ---------- Sources ----------
def is_thumbnail(url: str | None) -> bool:
    if not url or not isinstance(url, str):
        return True
    u_lower = url.lower()
    return any(p in u_lower for p in [
        "encrypted-tbn", "gstatic.com/images?q=tbn", "credit_card_chip",
        "bcci_logo", "flag_of_india", "government_of_india_logo"
    ])


def fetch_google_trends_rss(geo=GEO):
    """
    Fetches real-time trending searches from the official Google Trends RSS feed for India.
    Zero 404 errors, zero API keys required, includes real editorial image & publisher attribution.
    """
    trends = []
    url = f"https://trends.google.com/trending/rss?geo={geo}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(r.content)
            for item in root.findall(".//item"):
                title_elem = item.find("title")
                approx_elem = item.find("{https://trends.google.com/trending/rss}approx_traffic")
                pic_elem = item.find("{https://trends.google.com/trending/rss}picture")
                pic_source_elem = item.find("{https://trends.google.com/trending/rss}picture_source")
                news_elem = item.find("{https://trends.google.com/trending/rss}news_item")

                title = title_elem.text.strip() if title_elem is not None and title_elem.text else ""
                if not title:
                    continue

                traffic_str = approx_elem.text if approx_elem is not None and approx_elem.text else "100"
                clean_traffic = traffic_str.replace("+", "").replace(",", "")
                if "M" in clean_traffic:
                    traffic_num = int(float(clean_traffic.replace("M", "")) * 1000)
                elif "K" in clean_traffic:
                    traffic_num = int(float(clean_traffic.replace("K", "")))
                else:
                    try:
                        traffic_num = max(10, int(clean_traffic) // 1000)
                    except Exception:
                        traffic_num = 100

                pic_raw = pic_elem.text if pic_elem is not None and pic_elem.text else ""
                pic_url = pic_raw if (pic_raw and not is_thumbnail(pic_raw)) else None
                pic_source = pic_source_elem.text if pic_source_elem is not None and pic_source_elem.text else "Google Trends / Verified News"

                news_title = ""
                news_url = ""
                if news_elem is not None:
                    nt = news_elem.find("{https://trends.google.com/trending/rss}news_item_title")
                    nu = news_elem.find("{https://trends.google.com/trending/rss}news_item_url")
                    if nt is not None and nt.text:
                        news_title = nt.text.strip()
                    if nu is not None and nu.text:
                        news_url = nu.text.strip()

                trends.append({
                    "title": title,
                    "score": traffic_num,
                    "image": pic_url,
                    "credit": pic_source,
                    "url": news_url or f"https://trends.google.com/trending?geo={geo}",
                    "facts": f"Breaking verified news context: {news_title}" if news_title else ""
                })
    except Exception as e:
        print("[Google Trends RSS fetcher warning]:", e)

    if not trends:
        # Fallback to Google News India Top Stories to guarantee 24/7 stream
        try:
            r_news = requests.get(f"https://news.google.com/rss?hl=en-{geo}&gl={geo}&ceid={geo}:en", headers=headers, timeout=15)
            if r_news.status_code == 200:
                import xml.etree.ElementTree as ET
                root = ET.fromstring(r_news.content)
                for item in root.findall(".//item")[:10]:
                    t_elem = item.find("title")
                    link_elem = item.find("link")
                    if t_elem is not None and t_elem.text:
                        raw_t = t_elem.text.split(" - ")[0].strip()
                        trends.append({
                            "title": raw_t,
                            "score": 90,
                            "image": None,
                            "credit": "Google News India",
                            "url": link_elem.text if link_elem is not None and link_elem.text else "https://news.google.com/",
                            "facts": f"Trending national headline: {t_elem.text}"
                        })
        except Exception as e:
            print("[Google News fallback warning]:", e)

    return trends


NICHE_SEARCH_MAP = {
    "ai-tools": "AI tools OR ChatGPT alternative OR generative AI",
    "pc-builds": "gaming PC build OR graphics card RTX OR AMD processor",
    "side-hustles": "side hustle ideas OR make money online OR freelancing India",
    "exams-results": "sarkari result OR admit card OR exam cutoff OR answer key",
    "health": "gym workout routine OR muscle building exercises OR fitness diet",
    "food": "trending recipe OR street food India OR easy cooking hack",
    "deals": "festive deals discount OR price drop sale Amazon Flipkart",
    "fashion": "fashion trends 2026 OR sneaker drops OR viral outfit style"
}

def fetch_niche_news_rss(query, geo="IN"):
    """Fetches real-time targeted news items from Google News RSS for a specific niche"""
    url = f"https://news.google.com/rss/search?q={urllib.parse.quote(query)}&hl=en-{geo}&gl={geo}&ceid={geo}:en"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    items = []
    try:
        r = requests.get(url, headers=headers, timeout=12)
        if r.status_code == 200:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(r.content)
            for item in root.findall(".//item")[:10]:
                t_elem = item.find("title")
                link_elem = item.find("link")
                if t_elem is not None and t_elem.text:
                    raw_title = t_elem.text.split(" - ")[0].strip()
                    publisher = t_elem.text.split(" - ")[-1].strip() if " - " in t_elem.text else "Google News"
                    items.append({
                        "title": raw_title,
                        "score": 92,
                        "url": link_elem.text if link_elem is not None else "",
                        "credit": publisher,
                        "facts": f"Recent verified reporting from {publisher}: {t_elem.text}"
                    })
    except Exception:
        pass
    return items

def get_trends(seeds=None, niche_slug=None):
    out = {}
    # 1. Fetch targeted niche news from Google News RSS if available
    if niche_slug and niche_slug in NICHE_SEARCH_MAP:
        for t in fetch_niche_news_rss(NICHE_SEARCH_MAP[niche_slug], GEO):
            out[t["title"]] = {
                "score": t["score"],
                "url": t.get("url"),
                "facts": t.get("facts", ""),
                "credit": t.get("credit", "Google News")
            }

    # 2. Fetch live rising trends from official Google Trends RSS
    for t in fetch_google_trends_rss(GEO)[:15]:
        if t["title"] not in out:
            out[t["title"]] = {
                "score": t["score"],
                "url": t.get("url"),
                "facts": t.get("facts", ""),
                "credit": t.get("credit", "Verified News")
            }
    
    # 3. If seeds provided, augment with matching keyword variations
    if seeds:
        for s in seeds[:3]:
            if s not in out:
                out[s] = {"score": 75, "url": f"https://news.google.com/search?q={urllib.parse.quote(s)}", "facts": "", "credit": "Google News"}
    return out


def tmdb_trending():
    if not TMDB_KEY:
        return []
    try:
        r = requests.get("https://api.themoviedb.org/3/trending/movie/week",
                         params={"api_key": TMDB_KEY}, timeout=30)
        r.raise_for_status()
        return [{"title": m["title"], "image": f"https://image.tmdb.org/t/p/w500{m['poster_path']}" if m.get("poster_path") else None,
                 "facts": m.get("overview", ""), "date": m.get("release_date", "")}
                for m in r.json().get("results", [])[:10]]
    except Exception as e:
        print("tmdb failed:", e)
        return []


def fetch_indian_box_office_trends():
    """Fetches real-time Indian theatrical and OTT movie releases from Google News RSS"""
    url = "https://news.google.com/rss/search?q=box+office+movie+India+when:5d&hl=en-IN&gl=IN&ceid=IN:en"
    movies = []
    try:
        r = requests.get(url, headers=UA, timeout=20)
        if r.status_code == 200:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(r.content)
            for item in root.findall(".//item")[:15]:
                t = item.find("title")
                desc = item.find("description")
                link = item.find("link")
                if t is not None and t.text:
                    title_text = t.text.split(" - ")[0].strip()
                    movies.append({
                        "title": title_text,
                        "facts": desc.text if desc is not None and desc.text else "Live theatrical box office tracking.",
                        "url": link.text if link is not None and link.text else "https://news.google.com/"
                    })
    except Exception as e:
        print("[Indian Box Office RSS warning]:", e)
    return movies


def wiki(query):
    """Robust multi-candidate Wikipedia search for real entity posters and photography with strict relevance filter"""
    candidates = [
        query,
        re.sub(r'(?i)(box office|collection|nears|worldwide|day \d+|review|wrap|grossing|vs|match|score).*', '', query).strip(' :-,'),
        query.split(':')[0].strip(),
        query.split('-')[0].strip()
    ]
    seen = set()
    cleaned = []
    for c in candidates:
        if c and len(c) >= 3 and c.lower() not in seen:
            seen.add(c.lower())
            cleaned.append(c)

    for q in cleaned:
        try:
            s = requests.get("https://en.wikipedia.org/w/rest.php/v1/search/title",
                             params={"q": q, "limit": 4}, headers=UA, timeout=20).json()
            for p in s.get("pages", []):
                key = p.get("key")
                title = p.get("title", "")
                desc = p.get("description", "")
                if not key:
                    continue

                # Strict relevance check: query keywords must match candidate title/description
                q_words = [w.lower() for w in re.findall(r'[a-zA-Z0-9]+', q) if len(w) >= 4]
                if q_words:
                    combined_target = (title + " " + desc).lower()
                    if not any(w in combined_target for w in q_words):
                        continue  # Skip mismatched pages (e.g. BCCI for Cars)

                d = requests.get("https://en.wikipedia.org/api/rest_v1/page/summary/" + urllib.parse.quote(key),
                                 headers=UA, timeout=20).json()
                img = (d.get("originalimage") or d.get("thumbnail") or {}).get("source")
                if img:
                    return {
                        "extract": d.get("extract", ""),
                        "image": img,
                        "url": d.get("content_urls", {}).get("desktop", {}).get("page")
                    }
                if d.get("extract") and not img:
                    return {
                        "extract": d.get("extract", ""),
                        "image": None,
                        "url": d.get("content_urls", {}).get("desktop", {}).get("page")
                    }
        except Exception as e:
            continue
    return None


def rank(n, titles):
    prompt = (f"Niche: {n['name']} (India audience). Candidate trending topics: {json.dumps(titles)}.\n"
              f"Pick the {N_POSTS} best for a useful, non-clickbait article with affiliate/ad potential. "
              'Return JSON: {"picks":[{"title":"<exact candidate>","angle":"<1 line useful angle>"}]}')
    res = grok(prompt) or gemini(prompt)
    picks = [p for p in res.get("picks", []) if p.get("title") in titles]
    return picks[:N_POSTS] or [{"title": t, "angle": ""} for t in titles[:N_POSTS]]


def ai_topics(n):
    res = gemini(f"List 8 currently relevant, specific article topics for the niche '{n['name']}' "
                 f"for an Indian audience. JSON: {{\"topics\":[\"...\"]}}")
    if isinstance(res, list):
        return {t: 50 for t in res if isinstance(t, str)}
    if isinstance(res, dict):
        return {t: 50 for t in res.get("topics", []) if isinstance(t, str)}
    return {}


# ---------- Real News Media & Aspect Ratio Extractor (Zero Local Fallbacks) ----------
from urllib.parse import urlparse

def extract_og_image(url: str, timeout: int = 8) -> str | None:
    """Real news article se og:image extract karo. 1200x630 editorial photo."""
    if not url or not url.startswith("http"):
        return None
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        resp = requests.get(url, headers=headers, timeout=timeout)
        resp.raise_for_status()
        
        # og:image extract
        match = re.search(r'<meta[^>]+(?:property|name)=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']', resp.text, re.IGNORECASE)
        if not match:
            match = re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+(?:property|name)=["\']og:image["\']', resp.text, re.IGNORECASE)
        if match:
            img_url = match.group(1).strip()
            if img_url.startswith("https://") and not any(bad in img_url.lower() for bad in ["logo", "icon", "placeholder", "favicon"]):
                return img_url
        
        # Fallback: Twitter card image
        match = re.search(r'<meta[^>]+(?:property|name)=["\']twitter:image["\'][^>]+content=["\']([^"\']+)["\']', resp.text, re.IGNORECASE)
        if match:
            img_url = match.group(1).strip()
            if img_url.startswith("https://") and not any(bad in img_url.lower() for bad in ["logo", "icon", "placeholder", "favicon"]):
                return img_url
        
        # Fallback: Pehla <img> tag with src
        match = re.search(r'<img[^>]+src=["\'](https://[^"\']+\.(?:jpg|jpeg|png|webp))["\']', resp.text, re.IGNORECASE)
        if match:
            img_url = match.group(1).strip()
            if not any(bad in img_url.lower() for bad in ["logo", "icon", "placeholder", "avatar"]):
                return img_url
            
    except Exception:
        pass
    return None


def extract_image_from_rss(rss_item_xml: str) -> str | None:
    """Google Trends / Google News RSS se real image extract karo."""
    if not rss_item_xml:
        return None
    try:
        # <ht:picture> tag (Google Trends RSS)
        match = re.search(r'<ht:picture>(?:<!\[CDATA\[)?(https?://[^\]<>\s"]+)(?:\]\]>)?</ht:picture>', rss_item_xml)
        if match:
            return match.group(1).strip()
        
        # <media:content> tag
        match = re.search(r'<media:content[^>]+url=["\'](https://[^"\']+)["\']', rss_item_xml)
        if match:
            return match.group(1).strip()
        
        # <enclosure> tag
        match = re.search(r'<enclosure[^>]+url=["\'](https://[^"\']+\.(?:jpg|jpeg|png|webp))["\']', rss_item_xml, re.IGNORECASE)
        if match:
            return match.group(1).strip()
            
    except Exception:
        pass
    return None


def get_real_image(article_url: str = "", rss_xml: str = "", niche_slug: str = "") -> str | None:
    """
    Priority:
    1. RSS se image (real news photo)
    2. Article page se og:image (editorial photo)
    3. None (frontend mein clean gradient card dikhega, ZERO local JPGs)
    """
    # 1. RSS se try karo
    if rss_xml:
        img = extract_image_from_rss(rss_xml)
        if img:
            return img
    
    # 2. Article page se og:image
    if article_url and article_url.startswith("http"):
        img = extract_og_image(article_url)
        if img:
            return img
    
    return None


def scrape_grounded_article(url: str, timeout: int = 10) -> dict:
    """
    Advanced Multi-Source Scraper Engine:
    Pehle source news article se real factual journalistic text aur high-res 1200x630 og:image extract karta hai.
    Feeds real verified facts into LLM prompt before writing to eliminate hallucinations.
    """
    if not url or not url.startswith("http"):
        return {"text": "", "image": None, "title": None}

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,hi;q=0.8"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        if resp.status_code != 200:
            return {"text": "", "image": None, "title": None}

        # 1. Real og:image extraction
        img = None
        m = re.search(r'<meta[^>]+(?:property|name)=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']', resp.text, re.IGNORECASE)
        if not m:
            m = re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+(?:property|name)=["\']og:image["\']', resp.text, re.IGNORECASE)
        if m:
            c_img = m.group(1).strip()
            if c_img.startswith("https://") and not any(bad in c_img.lower() for bad in ["logo", "favicon", "avatar", "default_share", "app_icon"]):
                img = c_img

        # Fallback to twitter:image
        if not img:
            m_tw = re.search(r'<meta[^>]+(?:property|name)=["\']twitter:image["\'][^>]+content=["\']([^"\']+)["\']', resp.text, re.IGNORECASE)
            if m_tw:
                c_img = m_tw.group(1).strip()
                if c_img.startswith("https://") and not any(bad in c_img.lower() for bad in ["logo", "favicon", "avatar"]):
                    img = c_img

        # 2. Extract grounded journalistic article text via trafilatura
        doc = trafilatura.bare_extraction(resp.text)
        art_text = doc.text if doc and doc.text else ""
        art_title = doc.title if doc and doc.title else ""
        if not img and doc and doc.image and doc.image.startswith("https://"):
            img = doc.image

        return {
            "text": art_text,
            "image": img,
            "title": art_title
        }
    except Exception:
        return {"text": "", "image": None, "title": None}


def agent_alpha_check(candidate_title: str, candidate_slug: str, existing_titles: list) -> tuple[bool, str]:
    """
    Agent Alpha: Semantic & Title De-duplication Gate.
    Ensures no duplicate or near-identical topics are published.
    """
    if not candidate_title:
        return False, "Empty candidate title"

    clean_cand = re.sub(r'[^a-zA-Z0-9\s]', '', candidate_title.lower()).strip()
    cand_words = set(w for w in clean_cand.split() if len(w) >= 4)

    for ex in existing_titles:
        if not ex:
            continue
        clean_ex = re.sub(r'[^a-zA-Z0-9\s]', '', ex.lower()).strip()
        if clean_cand == clean_ex:
            return False, f"Exact match with '{ex}'"

        ex_words = set(w for w in clean_ex.split() if len(w) >= 4)
        if cand_words and ex_words:
            overlap = cand_words.intersection(ex_words)
            if len(overlap) >= 3 and len(overlap) / max(len(cand_words), len(ex_words)) > 0.7:
                return False, f"High semantic similarity with '{ex}'"

    return True, "Unique topic verified"


def agent_gamma_verify_image(image_url: str | None, niche_slug: str = "viral", topic_query: str = "", article_url: str = "") -> tuple[str | None, str]:
    """
    Agent Gamma: Media & Real Link Guardian.
    Validates image URL is a real https:// link. ZERO low-res scraps or local JPG fallbacks allowed!
    """
    target = None if is_thumbnail(image_url) else image_url

    if not target and article_url and article_url.startswith("http") and "google.com" not in article_url:
        og = extract_og_image(article_url)
        if og and not is_thumbnail(og):
            target = og

    if not target and topic_query:
        try:
            w = wiki(topic_query)
            if w and w.get("image") and not is_thumbnail(w["image"]):
                target = w["image"]
        except Exception:
            pass

    if target and isinstance(target, str) and target.startswith("http") and not is_thumbnail(target):
        return target, "Verified Real Web Media"

    # Dynamic High-Resolution Editorial Banner (Ensures 100% unique, topic-specific 1200x630 visual for every post)
    if topic_query:
        clean_topic = re.sub(r'[^a-zA-Z0-9\s]', '', topic_query).strip()[:80]
        encoded = urllib.parse.quote(f"{clean_topic} Indian students examination educational news photograph high quality banner")
        return f"https://image.pollinations.ai/prompt/{encoded}?width=1200&height=630&nologo=true", "Dynamic Editorial AI Banner"

    return None, "No Real Media (Clean Gradient Card)"


def write_article(n, title, angle, facts, trend):
    cfg = json.loads(n.get("config") or "{}") if isinstance(n.get("config"), str) else (n.get("config") or {})
    is_exam = n.get("slug") == "exams-results" or "result" in title.lower() or "exam" in title.lower() or "admit card" in title.lower()
    
    prompt = f"""You are an elite Indian journalist and education editor for UniqueDigit & Sarkari Result Alert.
Topic: {title} | Niche: {n['name']} | Angle: {angle} | Google Trends Interest: +{trend}k.

GROUNDED FACTS & CONTEXT (Use ONLY verified claims):
{facts or 'Keep analysis objective, explanatory, and grounded in common industry standards without fabricating numbers.'}

AUTONOMOUS INTENT & MULTI-CASE ARCHETYPE HANDLING (Agent Beta):
1. Detect why the user is searching for "{title}" RIGHT NOW:
   - Case A (Exam/Result/Admit Card/Sarkari - TONE: NATURAL CONVERSATIONAL HINGLISH):
     * TONE & LANGUAGE: Write in 100% natural, authentic Hinglish (Roman Hindi mixed with English keywords, exactly like Jagran Josh, Live Hindustan, and Amar Ujala).
     * HEADLINE FORMAT: "[Direct Link Active] {title}: Scorecard aise karein download, yahan dekhein category-wise cutoff marks"
     * SECTION 1 (⚡ Quick Highlights Box): Markdown table with Exam Name, Conducting Authority, Status: 🟢 Declared / Active, Required Login Details, and Official Portal Link.
     * SECTION 2 (📋 Step-by-Step Scorecard Check Karne Ka Tarika): Numbered 1-2-3-4 steps in clear, friendly Hinglish.
     * SECTION 3 (📊 Expected Category-Wise Cutoff): Markdown table for General (UR), OBC, EWS, SC, ST.
     * SECTION 4 (🔗 Official Direct Link Callout): Prominent action callout box with direct official website URL.
     * SECTION 5 (⚠️ Scorecard Verification & Advisory): What details to check (Name, Marks, QR Code) and warning against fake websites.
     * SECTION 6 (❓ Important FAQs): 3 direct user questions answered in crisp 2 sentences each.
   - Case B (Shopping/Deal/Loot): Provide a price-to-value verdict, key specs, warranty note, and why this discount matters.
   - Case C (Tech/Gaming/Hardware): Provide performance benchmarks, compatibility requirements, and pros/cons.
   - Case D (Trending Viral/Event): Explain what happened, why it is buzzing in India, and key verified takeaways.
   - Case E (Movies / Cinema & Box Office):
     Write a deeply humanized, compelling cinematic story that movie lovers actually search for:
     * Hook & Plot Setup: The story premise, character stakes, and why the plot is captivating (no spoilers).
     * Star Cast & Power Performances: Key actors and who stole the show.
     * Box Office Tracker: A neat markdown table with Day 1, Weekend, and Total Worldwide collections.
     * OTT Streaming Intel: Streaming rights platform (Netflix/Prime Video/Hotstar) and expected digital premiere.
     * Audience Consensus & Final Ticket Verdict: Should readers book a ticket or wait for OTT?
   - Case F (Health / Ayurveda / Wellness):
     Provide strict evidence-based advice referencing peer-reviewed clinical data or Ministry of AYUSH protocols.
     * Dos and Don'ts checklist.
     * Safe usage, precautions, and when to consult a registered medical practitioner.
     * Zero miracle-cure claims or unverified health promises.
   - Case G (Gym Exercises, Workout Routine & Fitness):
     * Target muscle groups and step-by-step correct exercise form.
     * Exact Sets, Reps, and Rest periods for beginner vs intermediate.
     * Common gym mistakes and injury prevention tips.
     * High-protein Indian diet support (Paneer, Soya chunks, Eggs, Whey).
   - Case H (Food Recipes, Street Food & Cooking):
     * Prep time, cooking time, and serving portions.
     * Complete ingredients checklist in standard Indian units.
     * Step-by-step foolproof cooking method.
     * Secret chef hacks to get authentic restaurant-style taste at home.
   - Case I (AI Tools, SaaS & Software Guides):
     * Practical real-world use case for Indian students, creators, and freelancers.
     * Detailed Free Tier vs Paid Tier breakdown.
     * Feature comparison table with alternatives.
     * Step-by-step getting started guide.

2. HUMANIZATION & STRICT ANTI-AI SLOP RULES:
   - WRITE LIKE A PASSIONATE, EXPERT INDIAN BLOGGER TALKING TO A SMART FRIEND.
   - BANNED CLICHES (NEVER USE): "In conclusion", "delve into", "tapestry", "beacon", "testament to", "fast-paced world", "it is important to remember", "furthermore", "moreover", "revolutionize", "game-changer".
   - Use punchy, engaging human transitions: "Here is the real deal", "The bottom line", "Why everyone is buzzing about this", "What you should actually do".
   - Structure the response in clean, engaging Markdown (550-700 words) using:
     * ## Catchy, clear subheadings
     * Markdown comparison tables or bulleted checklists
     * Natural conversational flow tailored for Indian readers.
     * Zero clickbait, zero hallucinated claims{', include standard safety note' if cfg.get('disclaimer') else ''}.

Return strict JSON:
{{
  "title": "Clear, engaging headline matching reader intent",
  "summary": "Compelling summary under 160 chars for Google SERP meta description",
  "body_md": "Full markdown content with ## subheadings, bullet points, and tables",
  "faq": [
    {{"q": "Real question users ask on Google", "a": "Direct, helpful 2-sentence answer"}},
    {{"q": "Second popular search query", "a": "Direct, helpful 2-sentence answer"}},
    {{"q": "Third question regarding cutoff/pricing/dates", "a": "Direct, helpful 2-sentence answer"}}
  ],
  "tags": ["Tag1", "Tag2", "Tag3", "Tag4"],
  "deal_intel": {{
    "is_deal": true,
    "product_name": "Specific Product Name",
    "mrp": "₹24,999",
    "steal_price": "₹14,490",
    "discount": "42% OFF",
    "loot_score": "9.7/10",
    "bank_hack": "Extra Instant Card / UPI discount or coupon box hack",
    "store": "Amazon India",
    "aff_url": "https://www.amazon.in/s?k=Search+Product&tag=uniquedigi0c6-21"
  }}
}}"""
    return gemini(prompt)


# ---------- Main Pipeline Runner ----------
def process_niche(n):
    cfg = json.loads(n.get("config") or "{}") if isinstance(n.get("config"), str) else (n.get("config") or {})
    fetchers = json.loads(n.get("fetchers") or "[]") if isinstance(n.get("fetchers"), str) else (n.get("fetchers") or [])
    seeds = json.loads(n.get("seed_keywords") or "[]") if isinstance(n.get("seed_keywords"), str) else (n.get("seed_keywords") or [])
    
    if n.get("page_type") == "dataset":
        return 0

    cands = {}
    # 1. Fetch real-time trends & niche seed expansions
    for q, data in get_trends(seeds, niche_slug=n.get("slug")).items():
        cands[q] = data if isinstance(data, dict) else {"score": data}

    # If Movies niche, scan live Indian box office and theatrical releases
    if n.get("slug") == "movies":
        for m in fetch_indian_box_office_trends():
            cands[m["title"]] = {
                "score": 98,
                "facts": m["facts"],
                "url": m["url"]
            }

    if "tmdb" in fetchers:
        for m in tmdb_trending():
            cands[m["title"]] = {"score": 100, "image": m["image"], "credit": "TMDB",
                                 "facts": m["facts"], "url": "https://www.themoviedb.org/"}

    # 2. Augment with fresh AI topics if needed
    if not cands or len(cands) < 4:
        for t, s in ai_topics(n).items():
            if t not in cands:
                cands[t] = {"score": s}

    # Check already existing topics in D1 for Agent Alpha de-duplication
    existing_records = d1_query("SELECT canonical, slug FROM topics WHERE niche_id = ?", [n["id"]])
    seen_slugs = {row["slug"] for row in existing_records}
    existing_titles = [row.get("canonical") for row in existing_records if row.get("canonical")]

    titles = [t for t in cands if slugify(t) not in seen_slugs][:25]
    if not titles:
        print(f"[{n['slug']}] No new trending topics.")
        return 0

    made = 0
    for pick in rank(n, titles):
        t, c = pick["title"], cands[pick["title"]]

        # Agent Alpha Gate: Uniqueness & Semantic De-duplication
        is_unique, alpha_msg = agent_alpha_check(t, "", existing_titles)
        if not is_unique:
            print(f"[{n['slug']} Agent Alpha Filtered]: {t} -> {alpha_msg}")
            continue

        facts, raw_img, credit, src = c.get("facts", ""), c.get("image"), c.get("credit"), c.get("url")
        image = None if is_thumbnail(raw_img) else raw_img

        if src and src.startswith("http") and "google.com" not in src:
            scraped_niche = scrape_grounded_article(src)
            if scraped_niche.get("text"):
                facts = scraped_niche["text"]
            if scraped_niche.get("image") and not is_thumbnail(scraped_niche["image"]):
                image = scraped_niche["image"]
                credit = "Verified News Publisher"

        # Enrich facts and images with Wikipedia
        if "wikipedia" in fetchers or not facts or not image or is_thumbnail(image):
            w = wiki(t)
            if w:
                facts = (facts + "\n" + w["extract"]).strip()
                if (not image or is_thumbnail(image)) and w.get("image") and not is_thumbnail(w["image"]):
                    image, credit, src = w["image"], "Wikipedia / Wikimedia Commons", w["url"]

        # Agent Gamma Gate: Media & Aspect Ratio Guardian
        image, gamma_status = agent_gamma_verify_image(image, n["slug"], t, src or "")

        try:
            a = write_article(n, t, pick.get("angle", ""), facts, c["score"])
        except Exception as e:
            print(f"[{n['slug']}] write failed for {t}:", e)
            continue

        topic_id = str(uuid.uuid4())
        topic_slug = slugify(t)
        post_id = str(uuid.uuid4())
        post_slug = slugify(a.get("title")) or topic_slug

        # Insert topic into Cloudflare D1
        d1_query(
            "INSERT OR IGNORE INTO topics (id, canonical, ckey, slug, niche_id, hype, stage, status) VALUES (?, ?, ?, ?, ?, ?, 'hot', 'article')",
            [topic_id, t, slugify(t), topic_slug, n["id"], c["score"]]
        )

        # Insert post into Cloudflare D1
        d1_query(
            """INSERT OR REPLACE INTO posts 
               (id, niche_id, topic_id, kind, slug, title, summary, body_md, faq, sources, image_url, image_credit, source_url, hype, is_breaking, indexable, status, published_at)
               VALUES (?, ?, ?, 'article', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, 'published', strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))""",
            [
                post_id, n["id"], topic_id, post_slug,
                a.get("title", t), a.get("summary", "")[:200], (a.get("body_md", "") + AFFILIATE_DISCLAIMER),
                json.dumps(a.get("faq", [])),
                json.dumps([{"title": credit or "Verified News", "url": src or ""}]) if (credit or src) else "[]",
                image, credit, src, c["score"],
                1 if c["score"] >= 80 else 0
            ]
        )
        existing_titles.append(t)
        # Dispatch instant Telegram alert
        send_telegram(a.get("title", t), n["name"], post_slug, niche_slug=n["slug"], image_url=image, deal_meta=a.get("deal_intel"))
        # Dispatch instant Google Blogger cross-post
        send_blogger(a.get("title", t), a.get("body_md", ""), tags=a.get("tags", [n["name"]]), image_url=image, niche_slug=n.get("slug"))
        made += 1
        time.sleep(1)
    return made


SEED_NICHES = [
    {"id": "1", "slug": "pc-builds", "name": "PC Builds", "tagline": "Custom rigs & parts", "grp": "Tech", "icon": "cpu", "page_type": "tools", "seed_keywords": '["gaming pc build","graphics card"]', "fetchers": '["trends"]'},
    {"id": "2", "slug": "gold-rate", "name": "Gold Rate", "tagline": "Live gold prices & trends", "grp": "Tech", "icon": "coins", "page_type": "dataset"},
    {"id": "3", "slug": "ai-tools", "name": "AI Tools", "tagline": "Generative AI & utilities", "grp": "Tech", "icon": "sparkles", "page_type": "tools", "seed_keywords": '["ai tools","chatgpt alternative"]', "fetchers": '["trends","wikipedia"]'},
    {"id": "4", "slug": "deals", "name": "Deals", "tagline": "Today's top discounts", "grp": "Money", "icon": "tag", "page_type": "tools", "seed_keywords": '["deals","discount"]', "fetchers": '["trends"]'},
    {"id": "5", "slug": "side-hustles", "name": "Side Hustles", "tagline": "Earn extra income", "grp": "Money", "icon": "briefcase", "page_type": "feed", "seed_keywords": '["side hustle","work from home"]', "fetchers": '["trends","wikipedia"]'},
    {"id": "6", "slug": "cashback", "name": "Cashback", "tagline": "Rewards & cashback offers", "grp": "Money", "icon": "percent", "page_type": "tools", "seed_keywords": '["cashback offers"]', "fetchers": '["trends"]'},
    {"id": "7", "slug": "health", "name": "Health", "tagline": "Wellness & fitness tips", "grp": "Lifestyle", "icon": "heart", "page_type": "feed", "seed_keywords": '["healthy diet","home workout"]', "fetchers": '["trends","wikipedia"]', "config": '{"review":true,"disclaimer":"Medical disclaimer."}'},
    {"id": "8", "slug": "fashion", "name": "Fashion", "tagline": "Trends & style guides", "grp": "Lifestyle", "icon": "shirt", "page_type": "feed", "seed_keywords": '["fashion trends","sneakers"]', "fetchers": '["trends","wikipedia"]'},
    {"id": "9", "slug": "food", "name": "Food", "tagline": "Recipes & cooking guides", "grp": "Lifestyle", "icon": "utensils", "page_type": "feed", "seed_keywords": '["recipe","street food"]', "fetchers": '["trends","wikipedia"]'},
    {"id": "10", "slug": "gta-6", "name": "GTA 6", "tagline": "News, updates & guides", "grp": "Entertainment", "icon": "gamepad", "page_type": "feed", "seed_keywords": '["gta 6","rockstar games"]', "fetchers": '["trends","wikipedia"]'},
    {"id": "11", "slug": "movies", "name": "Movies", "tagline": "Reviews, OTT & trailers", "grp": "Entertainment", "icon": "clapperboard", "page_type": "movies", "seed_keywords": '["new movies","ott release"]', "fetchers": '["trends","tmdb"]'},
    {"id": "12", "slug": "viral", "name": "Viral", "tagline": "Trending internet moments", "grp": "Entertainment", "icon": "rocket", "page_type": "feed", "seed_keywords": '[]', "fetchers": '["trends"]'},
    {"id": "13", "slug": "exams-results", "name": "Exams & Results", "tagline": "Sarkari results, admit cards & notes", "grp": "Education", "icon": "book-open", "page_type": "feed", "seed_keywords": '["ssc cgl result","cbse board exam","neet admit card","sarkari result","jee main","ncert solutions"]', "fetchers": '["trends","wikipedia"]'}
]

# ---------- Universal Autonomous Trend Discovery (Auto-Niche Creation) ----------
def process_national_breaking_trends():
    """Scans all trending searches in India and dynamically creates/assigns niches on the fly"""
    print("--- [Radar Agent] Scanning National Real-Time Indian Search Trends ---")
    rss_trends = fetch_google_trends_rss(GEO)
    if not rss_trends:
        print("[Radar Agent] No trends returned from Google Trends RSS.")
        return 0

    existing_records = d1_query("SELECT canonical, slug FROM topics")
    existing_slugs = {row["slug"] for row in existing_records}
    existing_titles = [row.get("canonical") for row in existing_records if row.get("canonical")]
    candidates = [item for item in rss_trends if slugify(item["title"]) not in existing_slugs][:6]
    
    if not candidates:
        print("[Radar Agent] No new unhandled national trends found.")
        return 0

    print(f"[Radar Agent] Discovered {len(candidates)} new breaking national trends: {[c['title'] for c in candidates]}")
    processed = 0

    for cand in candidates:
        query = cand["title"]

        # Agent Alpha Gate: Uniqueness & Semantic De-duplication
        is_unique, alpha_msg = agent_alpha_check(query, "", existing_titles)
        if not is_unique:
            print(f"[Radar Agent Alpha Filtered]: {query} -> {alpha_msg}")
            continue

        facts = cand.get("facts", "")
        raw_img = cand.get("image")
        image = None if is_thumbnail(raw_img) else raw_img
        credit = cand.get("credit", "Google Trends / Verified News")
        src = cand.get("url")

        # =========================================================================
        # PRO ARCHITECTURE: SCRAPE FIRST -> EXTRACT REAL FACTS & IMAGE -> PHIR LLM
        # =========================================================================
        scraped = {"text": "", "image": None, "title": None}
        if src and src.startswith("http") and "google.com" not in src:
            scraped = scrape_grounded_article(src)

        # Merge real journalistic facts
        grounded_facts = scraped.get("text") or facts
        real_headline = scraped.get("title") or query

        # Real news photo priority: Scraped og:image > Wikipedia entity
        if scraped.get("image") and not is_thumbnail(scraped["image"]):
            image = scraped["image"]
            credit = "Verified News Publisher"
        elif (not image or is_thumbnail(image)) and src and src.startswith("http") and "google.com" not in src:
            og = extract_og_image(src)
            if og and not is_thumbnail(og):
                image = og
                credit = "Verified News Publisher"

        if not image or is_thumbnail(image):
            w = wiki(query)
            if w:
                if not grounded_facts or len(grounded_facts) < 100:
                    grounded_facts = (grounded_facts + "\n" + w.get("extract", "")).strip()
                if w.get("image") and not is_thumbnail(w["image"]):
                    image, credit, src = w["image"], "Wikimedia Commons", w["url"]
                else:
                    image = None

        # Agent Gamma Media Validator: Zero local JPG fallbacks!
        image, gamma_status = agent_gamma_verify_image(image, "", query, src or "")

        prompt = f"""You are the Chief Editorial AI for UniqueDigit India.
Breaking Search Trend in India: "{query}"
Verified Source Headline: "{real_headline}"

100% VERIFIED PRIMARY FACTS (Extracted directly from source reporting):
\"\"\"
{grounded_facts[:3000] if grounded_facts else 'Topic buzzing across India. Focus on core user intent and verified aspects.'}
\"\"\"

STRICT EDITORIAL GROUNDING GUIDELINES:
1. Ground your article 100% in the real facts provided above. NEVER hallucinate fake numbers or unverified claims.
2. STRICT RULE: DO NOT force unrelated hybrid angles (NEVER convert a cricket match, weather event, gadget, or movie into a student study/exam time management guide!). Stay 100% focused on what the user searched for.
3. Categorize this trend into a suitable category: "cricket-sports", "movies", "exams-results", "gaming", "tech-reviews", "deals", "health", "finance", or "viral".
   - If topic mentions cricket, sports, teams, scores, or matches -> MUST be "cricket-sports".
   - If topic mentions movies, actors, trailers, box office -> MUST be "movies".
   - If topic mentions official exams, CBSE, UPSC, SSC, NEET, JEE, sarkari result, admit card -> MUST be "exams-results".
4. Write a highly engaging, humanized, fact-grounded article (450-600 words) tailored to why Indian users are searching for "{query}" right now.
5. Include FAQ schema and tags.

Return strict JSON:
{{
  "niche_slug": "clean-kebab-slug",
  "niche_name": "Display Name (e.g., Cricket & Sports, Movies, Tech)",
  "niche_tagline": "Short 1-line description",
  "niche_group": "Tech | Entertainment | Lifestyle | Money | Education",
  "niche_icon": "gamepad | sparkles | cpu | book-open | tag | heart | clapperboard | trophy",
  "title": "Engaging, click-worthy, non-clickbait headline",
  "summary": "Meta summary under 160 characters",
  "body_md": "Full markdown with ## subheadings, comparison points, and guides",
  "faq": [{{"q": "Popular question", "a": "Direct 2-sentence answer"}}],
  "tags": ["Tag1", "Tag2"]
}}"""
        try:
            res = gemini(prompt)
        except Exception as e:
            print(f"[Universal Radar failed for {query}]:", e)
            continue

        q_lower = query.lower()
        # Deterministic Guardrails to prevent misclassification
        if any(w in q_lower for w in ["cricket", "t20", "odi", "ipl", "bcci", "match", "wicket", "ind vs", "test series", "world cup"]):
            n_slug = "cricket-sports"
            n_name = "Cricket & Sports"
            n_grp = "Entertainment"
            n_icon = "trophy"
        elif any(w in q_lower for w in ["trailer", "box office", "teaser", "cinema", "movie review"]):
            n_slug = "movies"
            n_name = "Movies"
            n_grp = "Entertainment"
            n_icon = "clapperboard"
        elif any(w in q_lower for w in ["ssc", "upsc", "neet", "jee", "cbse", "admit card", "sarkari", "cutoff", "answer key", "syllabus", "hall ticket"]):
            n_slug = "exams-results"
            n_name = "Exams & Results"
            n_grp = "Education"
            n_icon = "book-open"
        else:
            n_slug = slugify(res.get("niche_slug") or "viral")
            if n_slug == "exams-results" and not any(w in q_lower for w in ["exam", "result", "admit", "card", "board", "neet", "jee", "ssc", "upsc", "cbse", "sarkari"]):
                n_slug = "viral"
                n_name = "Viral"
                n_grp = "Entertainment"
                n_icon = "rocket"
            else:
                n_name = res.get("niche_name") or n_slug.title()
                n_grp = res.get("niche_group") or "Entertainment"
                n_icon = res.get("niche_icon") or "sparkles"

        n_tagline = res.get("niche_tagline") or f"Latest updates on {n_name}"

        # 1. Auto-create Niche in D1 if it doesn't already exist
        niche_id = str(uuid.uuid4())
        d1_query(
            "INSERT OR IGNORE INTO niches (id, slug, name, tagline, grp, icon, page_type, active) VALUES (?, ?, ?, ?, ?, ?, 'feed', 1)",
            [niche_id, n_slug, n_name, n_tagline, n_grp, n_icon]
        )

        # Get the actual niche_id in case it existed
        niche_record = d1_query("SELECT id FROM niches WHERE slug = ?", [n_slug])
        actual_niche_id = niche_record[0]["id"] if niche_record else niche_id

        topic_id = str(uuid.uuid4())
        topic_slug = slugify(query)
        post_id = str(uuid.uuid4())
        post_slug = slugify(res.get("title")) or topic_slug

        d1_query(
            "INSERT OR IGNORE INTO topics (id, canonical, ckey, slug, niche_id, hype, stage, status) VALUES (?, ?, ?, ?, ?, 100, 'peak', 'article')",
            [topic_id, query, slugify(query), topic_slug, actual_niche_id]
        )

        d1_query(
            """INSERT OR REPLACE INTO posts 
               (id, niche_id, topic_id, kind, slug, title, summary, body_md, faq, sources, image_url, image_credit, source_url, hype, is_breaking, indexable, status, published_at)
               VALUES (?, ?, ?, 'article', ?, ?, ?, ?, ?, ?, ?, ?, ?, 100, 1, 1, 'published', strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))""",
            [
                post_id, actual_niche_id, topic_id, post_slug,
                res.get("title", query), res.get("summary", "")[:200], (res.get("body_md", "") + AFFILIATE_DISCLAIMER),
                json.dumps(res.get("faq", [])),
                json.dumps([{"title": credit or "Google Trends", "url": src or ""}]) if (credit or src) else "[]",
                image, credit, src
            ]
        )

        send_telegram(res.get("title", query), n_name, post_slug, niche_slug=n_slug, image_url=image, deal_meta=res.get("deal_intel"))
        # Dispatch instant Google Blogger cross-post
        send_blogger(res.get("title", query), res.get("body_md", ""), tags=res.get("tags", [n_name]), image_url=image, niche_slug=n_slug)
        print(f"[Radar Agent Published]: {res.get('title')} -> /{n_slug}/{post_slug}")
        processed += 1
        time.sleep(1)

    return processed


# ---------- Cloudflare KV Trend Sync (Edge Cache for Homepage & /trending) ----------
def sync_kv_boards():
    """Builds and writes live real-time trend boards into Cloudflare KV (boards:v1 and board:IN)"""
    if DRY:
        print("[dry] skipping KV sync")
        return
    if not (CF_ACCOUNT and CF_KV_ID and CF_TOKEN):
        print("[KV sync skipped] Cloudflare credentials missing")
        return

    print("--- [KV Sync] Synchronizing live trends and D1 articles to Cloudflare KV ---")
    rows = d1_query("""
        SELECT posts.id, posts.title, posts.slug as post_slug, posts.kind as post_kind,
               posts.hype, posts.published_at as updated_at,
               niches.slug as niche_slug, niches.name as niche_name
        FROM posts
        LEFT JOIN niches ON posts.niche_id = niches.id
        WHERE posts.status = 'published'
        ORDER BY posts.hype DESC, posts.published_at DESC
        LIMIT 30
    """)
    if not rows:
        print("[KV sync] No published posts found to sync.")
        return

    global_trends = []
    niches_map = {}

    for idx, r in enumerate(rows):
        n_slug = r.get("niche_slug") or "viral"
        item = {
            "id": r.get("id") or f"trend-{idx}",
            "title": r.get("title"),
            "slug": r.get("post_slug"),
            "hype": r.get("hype") or 90,
            "growth": 0.18,
            "stage": "hot" if idx < 5 else "emerging",
            "n": idx + 1,
            "sources": ["gtrends", "verified-news"],
            "spark": [65, 72, 78, 85, 90, 94, r.get("hype") or 95],
            "niche": r.get("niche_name") or n_slug.title(),
            "niche_slug": n_slug,
            "approx_traffic": f"{r.get('hype') or 50}K+",
            "updated_at": r.get("updated_at") or time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "post_slug": r.get("post_slug"),
            "post_kind": r.get("post_kind") or "article"
        }
        global_trends.append(item)
        if n_slug not in niches_map:
            niches_map[n_slug] = []
        niches_map[n_slug].append(item)

    payload = {
        "sig": "uniquedigit-live-v1",
        "global": global_trends,
        "niches": niches_map,
        "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }

    payload_json = json.dumps(payload, ensure_ascii=False)
    headers = {
        "Authorization": f"Bearer {CF_TOKEN}",
        "Content-Type": "application/json"
    }

    # 1. Update boards:v1
    url1 = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT}/storage/kv/namespaces/{CF_KV_ID}/values/boards:v1"
    try:
        r1 = requests.put(url1, headers=headers, data=payload_json.encode("utf-8"), timeout=15)
        if r1.status_code == 200:
            print("[KV Sync] boards:v1 successfully written to Cloudflare KV!")
        else:
            print(f"[KV Sync boards:v1 warning]: HTTP {r1.status_code} {r1.text[:100]}")
    except Exception as e:
        print("[KV Sync error boards:v1]:", e)

    # 2. Update board:IN (legacy key fallback)
    url2 = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT}/storage/kv/namespaces/{CF_KV_ID}/values/board:IN"
    try:
        r2 = requests.put(url2, headers=headers, data=json.dumps(global_trends, ensure_ascii=False).encode("utf-8"), timeout=15)
        if r2.status_code == 200:
            print("[KV Sync] board:IN successfully written to Cloudflare KV!")
        else:
            print(f"[KV Sync board:IN warning]: HTTP {r2.status_code} {r2.text[:100]}")
    except Exception as e:
        print("[KV Sync error board:IN]:", e)


def main():
    print("--- Running UniqueDigit Universal Autonomous Pipeline (Level 3 Edition) ---")
    cleanup_old_data()

    # Phase 1: Universal Autonomous National Radar (Discovers any new viral gaming, news, exam, tech trend)
    if not ONLY:
        national_count = process_national_breaking_trends()
        print(f"[Radar Complete] Published {national_count} breaking national articles.")
    else:
        national_count = 0

    # Phase 2: Seeded Specialized Niches
    niches = d1_query("SELECT * FROM niches WHERE active = 1 ORDER BY sort ASC")
    if not niches:
        print("[Notice] Using local baseline niches for dry run.")
        niches = SEED_NICHES

    if ONLY:
        niches = [n for n in niches if n["slug"] == ONLY]

    summary = {"national_breaking": national_count}
    for n in niches:
        try:
            count = process_niche(n)
            summary[n["slug"]] = count
            print(f"[{n['slug']}] Generated {count} articles.")
        except Exception as e:
            summary[n["slug"]] = f"ERROR: {e}"
            print(f"[{n['slug']}] Failed:", e)

    # Phase 3: Synchronize Live Trend Board to Cloudflare KV
    sync_kv_boards()

    print("Pipeline finished:", summary)


if __name__ == "__main__":
    main()
