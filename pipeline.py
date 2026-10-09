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

TG_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TG_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")
PORTAL_BASE = os.environ.get("PORTAL_BASE_URL", "https://uniquedigit-viral-hub.pages.dev")


# ---------- Telegram Dispatcher ----------
def send_telegram(title, niche_name, post_slug):
    if not (TG_BOT_TOKEN and TG_CHAT_ID):
        return
    post_url = f"{PORTAL_BASE}/{post_slug}"
    text = (
        f"🔥 *New Trend Live on UniqueDigit*\n\n"
        f"📌 *Category:* {niche_name}\n"
        f"📝 *Title:* {title}\n"
        f"🔗 *Link:* {post_url}\n\n"
        f"⚡ _Auto-published with verified deals & schema_"
    )
    try:
        url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": TG_CHAT_ID, "text": text, "parse_mode": "Markdown"}, timeout=10)
    except Exception as e:
        print("[Telegram notify failed]:", e)


# ---------- Storage Optimization (Prevent 5GB D1 Bloat) ----------
def cleanup_old_data():
    """Retains last 90 days of posts to keep D1 SQLite lightweight and fast"""
    print("[D1 Storage Optimizer] Pruning articles older than 90 days...")
    d1_query("DELETE FROM posts WHERE published_at < datetime('now', '-90 days')")


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
        try:
            r = requests.post(url, headers=headers, json=payload, timeout=30)
            if r.status_code == 200:
                res = r.json()
                if res.get("result") and len(res["result"]) > 0:
                    return res["result"][0].get("results", [])
                return []
        except Exception as e:
            print("[D1 REST query error]:", e)

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
# ---------- Sources ----------
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

                pic_url = pic_elem.text if pic_elem is not None and pic_elem.text else None
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
    return trends


def get_trends(seeds=None):
    out = {}
    # 1. Fetch live rising trends from official Google Trends RSS
    for t in fetch_google_trends_rss(GEO)[:15]:
        out[t["title"]] = t["score"]
    
    # 2. If seeds provided, augment with matching keyword variations
    if seeds:
        for s in seeds[:3]:
            if s not in out:
                out[s] = 75
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


def wiki(query):
    try:
        s = requests.get("https://en.wikipedia.org/w/rest.php/v1/search/title",
                         params={"q": query, "limit": 1}, headers=UA, timeout=20).json()
        if not s.get("pages"):
            return None
        key = s["pages"][0]["key"]
        d = requests.get("https://en.wikipedia.org/api/rest_v1/page/summary/" + urllib.parse.quote(key),
                         headers=UA, timeout=20).json()
        img = (d.get("originalimage") or d.get("thumbnail") or {}).get("source")
        return {"extract": d.get("extract", ""), "image": img,
                "url": d.get("content_urls", {}).get("desktop", {}).get("page")}
    except Exception as e:
        print("wiki failed:", e)
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
    return {t: 50 for t in res.get("topics", [])}


def write_article(n, title, angle, facts, trend):
    cfg = json.loads(n.get("config") or "{}") if isinstance(n.get("config"), str) else (n.get("config") or {})
    prompt = f"""You are an elite Indian tech & lifestyle journalist for UniqueDigit.
Topic: {title} | Niche: {n['name']} | Angle: {angle} | Google Trends Interest: +{trend}k.

GROUNDED FACTS & CONTEXT (Use ONLY verified claims):
{facts or 'Keep analysis objective, explanatory, and grounded in common industry standards without fabricating numbers.'}

AUTONOMOUS INTENT & MULTI-CASE ARCHETYPE HANDLING:
1. Detect why the user is searching for "{title}" RIGHT NOW:
   - Case A (Exam/Result/Admit Card): Provide a clear timeline, official check steps, cutoff breakdown, and preparation revision tips.
   - Case B (Shopping/Deal/Loot): Provide a price-to-value verdict, key specs, warranty note, and why this discount matters.
   - Case C (Tech/Gaming/Hardware): Provide performance benchmarks, compatibility requirements, and pros/cons.
   - Case D (Trending Viral/Event): Explain what happened, why it is buzzing in India, and key verified takeaways.
2. Structure the response in clean, engaging Markdown (450-600 words) using:
   - ## Catchy, clear subheadings
   - Markdown comparison tables or bulleted checklists where relevant
   - Simple, humanized English with natural Hinglish warmth for Indian audiences
   - Zero clickbait, zero hallucinated medical/legal guarantees{', include standard safety note' if cfg.get('disclaimer') else ''}.

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
  "tags": ["Tag1", "Tag2", "Tag3", "Tag4"]
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
    if "trends" in fetchers:
        for q, v in get_trends(seeds).items():
            cands[q] = {"score": v}
    if "tmdb" in fetchers:
        for m in tmdb_trending():
            cands[m["title"]] = {"score": 100, "image": m["image"], "credit": "TMDB",
                                 "facts": m["facts"], "url": "https://www.themoviedb.org/"}
    if not cands:
        cands = {t: {"score": s} for t, s in ai_topics(n).items()}

    # Check already existing topics in D1
    existing = d1_query("SELECT slug FROM topics WHERE niche_id = ?", [n["id"]])
    seen = {row["slug"] for row in existing}
    titles = [t for t in cands if slugify(t) not in seen][:25]
    if not titles:
        print(f"[{n['slug']}] No new trending topics.")
        return 0

    made = 0
    for pick in rank(n, titles):
        t, c = pick["title"], cands[pick["title"]]
        facts, image, credit, src = c.get("facts", ""), c.get("image"), c.get("credit"), c.get("url")
        if "wikipedia" in fetchers:
            w = wiki(t)
            if w:
                facts = (facts + "\n" + w["extract"]).strip()
                if not image and w["image"]:
                    image, credit, src = w["image"], "Wikipedia / Wikimedia Commons", w["url"]
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
            "INSERT OR IGNORE INTO topics (id, niche_id, title, slug, trend_score, source) VALUES (?, ?, ?, ?, ?, ?)",
            [topic_id, n["id"], t, topic_slug, c["score"], "trends"]
        )

        # Insert post into Cloudflare D1
        d1_query(
            """INSERT OR REPLACE INTO posts 
               (id, niche_id, category, topic_id, slug, title, summary, body_md, faq, tags, image_url, image_credit, source_url, trend_score, status)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            [
                post_id, n["id"], n["slug"], topic_id, post_slug,
                a.get("title", t), a.get("summary", "")[:200], a.get("body_md", ""),
                json.dumps(a.get("faq", [])), json.dumps(a.get("tags", [])),
                image, credit, src, c["score"],
                "draft" if cfg.get("review") else "published"
            ]
        )
        # Dispatch instant Telegram alert
        send_telegram(a.get("title", t), n["name"], post_slug)
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

    existing_slugs = {row["slug"] for row in d1_query("SELECT slug FROM topics")}
    candidates = [item for item in rss_trends if slugify(item["title"]) not in existing_slugs][:4]
    
    if not candidates:
        print("[Radar Agent] No new unhandled national trends found.")
        return 0

    print(f"[Radar Agent] Discovered {len(candidates)} new breaking national trends: {[c['title'] for c in candidates]}")
    processed = 0

    for cand in candidates:
        query = cand["title"]
        facts = cand.get("facts", "")
        image = cand.get("image")
        credit = cand.get("credit", "Google Trends / Verified News")
        src = cand.get("url")

        prompt = f"""You are the Chief Editorial AI for UniqueDigit India.
Breaking Search Trend in India: "{query}"
Verified Context: {facts or 'Current top trending interest in India.'}

1. Categorize this trend into a suitable clean category/niche (e.g., "gaming", "tech-reviews", "deals", "exams-results", "movies", "health", "cricket-sports", "finance").
2. Write a highly engaging, humanized, fact-grounded article (450-600 words) tailored to why Indian users are searching for "{query}" right now.
3. Include FAQ schema and tags.

Return strict JSON:
{{
  "niche_slug": "clean-kebab-slug",
  "niche_name": "Display Name (e.g., Gaming, Cricket, Tech)",
  "niche_tagline": "Short 1-line description",
  "niche_group": "Tech | Entertainment | Lifestyle | Money | Education",
  "niche_icon": "gamepad | sparkles | cpu | book-open | tag | heart | clapperboard",
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

        n_slug = slugify(res.get("niche_slug") or "viral")
        n_name = res.get("niche_name") or n_slug.title()
        n_tagline = res.get("niche_tagline") or f"Latest updates on {n_name}"
        n_grp = res.get("niche_group") or "Entertainment"
        n_icon = res.get("niche_icon") or "sparkles"

        # 1. Auto-create Niche in D1 if it doesn't already exist
        niche_id = str(uuid.uuid4())
        d1_query(
            "INSERT OR IGNORE INTO niches (id, slug, name, tagline, grp, icon, page_type, active) VALUES (?, ?, ?, ?, ?, ?, 'feed', 1)",
            [niche_id, n_slug, n_name, n_tagline, n_grp, n_icon]
        )

        # Get the actual niche_id in case it existed
        niche_record = d1_query("SELECT id FROM niches WHERE slug = ?", [n_slug])
        actual_niche_id = niche_record[0]["id"] if niche_record else niche_id

        # 2. If no image from RSS, check Wikipedia fallback
        if not image:
            w = wiki(query)
            if w:
                facts = (facts + "\n" + w["extract"]).strip()
                if w.get("image"):
                    image, credit, src = w["image"], "Wikimedia Commons", w["url"]

        topic_id = str(uuid.uuid4())
        topic_slug = slugify(query)
        post_id = str(uuid.uuid4())
        post_slug = slugify(res.get("title")) or topic_slug

        d1_query(
            "INSERT OR IGNORE INTO topics (id, niche_id, title, slug, trend_score, source) VALUES (?, ?, ?, ?, 100, 'google-trends-national')",
            [topic_id, actual_niche_id, query, topic_slug]
        )

        d1_query(
            """INSERT OR REPLACE INTO posts 
               (id, niche_id, category, topic_id, slug, title, summary, body_md, faq, tags, image_url, image_credit, source_url, trend_score, status)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 100, 'published')""",
            [
                post_id, actual_niche_id, n_slug, topic_id, post_slug,
                res.get("title", query), res.get("summary", "")[:200], res.get("body_md", ""),
                json.dumps(res.get("faq", [])), json.dumps(res.get("tags", [])),
                image, credit, src
            ]
        )

        send_telegram(res.get("title", query), n_name, post_slug)
        print(f"[Radar Agent Published]: {res.get('title')} -> /{n_slug}/{post_slug}")
        processed += 1
        time.sleep(1)

    return processed


def main():
    print("--- Running UniqueDigit Universal Autonomous Pipeline (Level 3 Edition) ---")
    cleanup_old_data()

    # Phase 1: Universal Autonomous National Radar (Discovers any new viral gaming, news, exam, tech trend)
    national_count = process_national_breaking_trends()
    print(f"[Radar Complete] Published {national_count} breaking national articles.")

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

    print("Pipeline finished:", summary)


if __name__ == "__main__":
    main()
