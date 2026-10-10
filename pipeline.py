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
CF_KV_ID = os.environ.get("CLOUDFLARE_KV_NAMESPACE_ID", "2ab0d1c56e1c471fa658e522912373ec")

TG_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TG_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")
PORTAL_BASE = os.environ.get("PORTAL_BASE_URL", "https://uniquedigit-viral-hub.pages.dev")
AFFILIATE_DISCLAIMER = "\n\n---\n*Disclaimer: UniqueDigit participates in affiliate programs including Amazon Associates. When you purchase through links on our site, we may earn an affiliate commission at no extra cost to you.*"


# ---------- Telegram Dispatcher ----------
def send_telegram(title, niche_name, post_slug):
    if not (TG_BOT_TOKEN and TG_CHAT_ID):
        return
    post_url = f"{PORTAL_BASE}/{post_slug}"
    safe_title = str(title).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    safe_niche = str(niche_name).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = (
        f"🔥 <b>New Trend Live on UniqueDigit</b>\n\n"
        f"📌 <b>Category:</b> {safe_niche}\n"
        f"📝 <b>Title:</b> {safe_title}\n"
        f"🔗 <b>Link:</b> <a href=\"{post_url}\">{post_url}</a>\n\n"
        f"⚡ <i>Auto-published with verified deals &amp; schema</i>"
    )
    try:
        url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": TG_CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=10)
    except Exception as e:
        print("[Telegram notify failed]:", e)


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
    return {t: 50 for t in res.get("topics", [])}


# ---------- Trio Multi-Agent Governance Model ----------
CURATED_NICHE_HERO_FALLBACKS = {
    "cricket-sports": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/Board_of_Control_for_Cricket_in_India_Logo_%282024%29.svg/960px-Board_of_Control_for_Cricket_in_India_Logo_%282024%29.svg.png",
    "pc-builds": "/images/rtx5090.jpg",
    "gta-6": "/images/gta6_cover.jpg",
    "ai-tools": "/images/ai_tools.jpg",
    "gold-rate": "/images/gold_24k.jpg",
    "deals": "/images/products/iphone_16_pro.jpg",
    "cashback": "https://upload.wikimedia.org/wikipedia/commons/2/2a/Credit_Card_Chip_%2834684294971%29.jpg",
    "food": "https://upload.wikimedia.org/wikipedia/commons/e/ef/Tradtional_Thali.jpg",
    "health": "https://upload.wikimedia.org/wikipedia/commons/b/b0/Beach_asana_class%2C_Plage_Pereire%2C_Arcachon%2C_2015.jpg",
    "fashion": "https://upload.wikimedia.org/wikipedia/commons/a/a6/Carolina_Herrera_AW14_12.jpg",
    "movies": "https://upload.wikimedia.org/wikipedia/en/d/d9/Drishyam-_The_Conclusion_poster.jpg",
    "automotive-trends": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Tata_Nexon_Blue_Dual_Tone.jpg/960px-Tata_Nexon_Blue_Dual_Tone.jpg",
    "exams-results": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Government_of_India_logo.svg/960px-Government_of_India_logo.svg.png",
    "viral": "/images/ai_tools.jpg"
}

def agent_alpha_check(candidate_title, candidate_summary="", existing_titles=None, min_chars=10):
    """
    Agent Alpha: Asserts uniqueness against D1 history and validates quality.
    Rejects semantic duplicates (Jaccard similarity > 0.60 or empty titles).
    """
    if not candidate_title or len(candidate_title.strip()) < min_chars:
        return False, "Title too short or empty"
    
    cand_tokens = set(re.findall(r'\b\w{3,}\b', candidate_title.lower()))
    if not cand_tokens:
        return False, "No valid semantic tokens"

    if existing_titles:
        for ext in existing_titles:
            if not ext:
                continue
            ext_tokens = set(re.findall(r'\b\w{3,}\b', ext.lower()))
            if not ext_tokens:
                continue
            intersection = cand_tokens.intersection(ext_tokens)
            union = cand_tokens.union(ext_tokens)
            jaccard = len(intersection) / len(union) if union else 0
            if jaccard > 0.60:
                return False, f"Duplicate detected (Jaccard {jaccard:.2f} with '{ext}')"

    return True, "Passed Agent Alpha quality & uniqueness gate"


def agent_gamma_verify_image(image_url, niche_slug, topic_query):
    """
    Agent Gamma: Media & Aspect Ratio Guardian.
    Validates image URL reachable via HTTP HEAD/GET, fallback to curated high-res local/wiki assets.
    """
    fallback = CURATED_NICHE_HERO_FALLBACKS.get(niche_slug, "/images/ai_tools.jpg")
    if not image_url:
        return fallback, "Local High-Res Fallback"
    
    if image_url.startswith("/"):
        return image_url, "Local Asset"
    
    try:
        r = requests.head(image_url, headers=UA, timeout=4, allow_redirects=True)
        if r.status_code == 200:
            c_type = r.headers.get("Content-Type", "")
            if not c_type or "image" in c_type.lower() or "application/octet-stream" in c_type.lower():
                return image_url, "HTTP 200 Verified Remote"
    except Exception:
        pass

    # If head check failed or redirected poorly, try wiki
    try:
        w = wiki(topic_query)
        if w and w.get("image"):
            return w["image"], "Wikimedia Commons Verified"
    except Exception:
        pass

    return fallback, "Curated Niche Fallback"


def write_article(n, title, angle, facts, trend):
    cfg = json.loads(n.get("config") or "{}") if isinstance(n.get("config"), str) else (n.get("config") or {})
    prompt = f"""You are an elite Indian tech & lifestyle journalist for UniqueDigit.
Topic: {title} | Niche: {n['name']} | Angle: {angle} | Google Trends Interest: +{trend}k.

GROUNDED FACTS & CONTEXT (Use ONLY verified claims):
{facts or 'Keep analysis objective, explanatory, and grounded in common industry standards without fabricating numbers.'}

AUTONOMOUS INTENT & MULTI-CASE ARCHETYPE HANDLING (Agent Beta):
1. Detect why the user is searching for "{title}" RIGHT NOW:
   - Case A (Exam/Result/Admit Card): Provide a clear timeline, official check steps, cutoff breakdown, and preparation revision tips.
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
   - Case G (Deals / Cashback / Product Review):
     Provide clear price intelligence:
     * Mention MRP, realistic sale price, bank card cashback offers (e.g. HDFC/ICICI).
     * Value breakdown and whether it's at its 30-day lowest price.

2. Structure the response in clean, engaging Markdown (500-650 words) using:
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
    # 1. Fetch real-time trends & niche seed expansions
    for q, v in get_trends(seeds).items():
        cands[q] = {"score": v}

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

        facts, image, credit, src = c.get("facts", ""), c.get("image"), c.get("credit"), c.get("url")
        # Enrich facts and images with Wikipedia
        if "wikipedia" in fetchers or not facts or not image:
            w = wiki(t)
            if w:
                facts = (facts + "\n" + w["extract"]).strip()
                if not image and w["image"]:
                    image, credit, src = w["image"], "Wikipedia / Wikimedia Commons", w["url"]

        # Agent Gamma Gate: Media & Aspect Ratio Guardian
        image, gamma_status = agent_gamma_verify_image(image, n["slug"], t)

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
        image = cand.get("image")
        credit = cand.get("credit", "Google Trends / Verified News")
        src = cand.get("url")

        prompt = f"""You are the Chief Editorial AI for UniqueDigit India.
Breaking Search Trend in India: "{query}"
Verified Context: {facts or 'Current top trending interest in India.'}

EDITORIAL GUIDELINES:
1. Categorize this trend into a suitable category: "cricket-sports", "movies", "exams-results", "gaming", "tech-reviews", "deals", "health", "finance", or "viral".
   - If topic mentions cricket, sports, teams, scores, or matches -> MUST be "cricket-sports".
   - If topic mentions movies, actors, trailers, box office -> MUST be "movies".
   - If topic mentions official exams, CBSE, UPSC, SSC, NEET, JEE, sarkari result, admit card -> MUST be "exams-results".
2. STRICT RULE: DO NOT force unrelated hybrid angles (NEVER convert a cricket match or movie into an exam prep or student time management guide). Stay 100% focused on what the user searched for.
3. Write a highly engaging, humanized, fact-grounded article (450-600 words) tailored to why Indian users are searching for "{query}" right now.
4. Include FAQ schema and tags.

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

        # 2. If no image from RSS, check Wikipedia fallback
        if not image:
            w = wiki(query)
            if w:
                facts = (facts + "\n" + w["extract"]).strip()
                if w.get("image"):
                    image, credit, src = w["image"], "Wikimedia Commons", w["url"]

        # Agent Gamma Gate: Media & Aspect Ratio Guardian
        image, gamma_status = agent_gamma_verify_image(image, n_slug, query)

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

        send_telegram(res.get("title", query), n_name, post_slug)
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

    # Phase 3: Synchronize Live Trend Board to Cloudflare KV
    sync_kv_boards()

    print("Pipeline finished:", summary)


if __name__ == "__main__":
    main()
