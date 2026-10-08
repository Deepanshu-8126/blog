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
import json, os, re, sys, time, uuid, urllib.parse
from dotenv import load_dotenv
load_dotenv()

import requests

DRY = "--dry" in sys.argv
ONLY = sys.argv[sys.argv.index("--niche") + 1] if "--niche" in sys.argv else None

GEMINI_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
GROK_KEY = os.environ.get("GROK_API_KEY")
GROK_MODEL = os.environ.get("GROK_MODEL", "grok-4")
TMDB_KEY = os.environ.get("TMDB_API_KEY")
GEO = os.environ.get("TRENDS_GEO", "IN")
N_POSTS = int(os.environ.get("POSTS_PER_NICHE", "3"))
AMAZON_TAG = os.environ.get("AMAZON_ASSOCIATE_TAG", "uniquedigi0c6-21")
UA = {"User-Agent": "UniqueDigitBot/1.0 (contact: info@uniquedigit.in)"}

CF_ACCOUNT = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "")
CF_D1_DB = os.environ.get("CLOUDFLARE_D1_DATABASE_ID", "")
CF_TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN", "")


# ---------- Cloudflare D1 Helpers ----------
def d1_query(sql, params=None):
    if DRY or not (CF_ACCOUNT and CF_D1_DB and CF_TOKEN):
        print(f"[dry/local d1] {sql[:120]} | params: {params}")
        return []
    url = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT}/d1/database/{CF_D1_DB}/query"
    headers = {
        "Authorization": f"Bearer {CF_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {"sql": sql, "params": params or []}
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        r.raise_for_status()
        res = r.json()
        if res.get("result") and len(res["result"]) > 0:
            return res["result"][0].get("results", [])
        return []
    except Exception as e:
        print("D1 query error:", e)
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
def get_trends(seeds):
    out = {}
    try:
        from pytrends.request import TrendReq
        py = TrendReq(hl="en-IN", tz=330, timeout=(5, 20))
        for s in seeds[:3]:
            py.build_payload([s], timeframe="now 7-d", geo=GEO)
            rising = py.related_queries().get(s, {}).get("rising")
            if rising is not None:
                for _, row in rising.head(8).iterrows():
                    out[str(row["query"])] = int(row["value"])
            time.sleep(2)
        if not seeds:
            df = py.trending_searches(pn="india")
            for q in df[0].head(10):
                out[str(q)] = 100
    except Exception as e:
        print("trends failed:", e)
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
    prompt = f"""Write a helpful article for an Indian audience. Niche: {n['name']}.
Title idea: {title}. Angle: {angle}. Google Trends interest score: {trend}.
FACTS (use ONLY these; do not invent statistics, prices, dates, quotes, or product claims):
{facts or 'No extra facts available - keep it general, explanatory, and clearly hedged.'}
Rules: plain simple English/Hinglish-friendly, no clickbait, no medical/financial advice{', add a short safety note' if cfg.get('disclaimer') else ''}.
Return JSON: {{"title":"","summary":"<=160 chars","body_md":"400-600 words markdown with ## headings","faq":[{{"q":"","a":""}}],"tags":["",""]}}"""
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
               (id, niche_id, topic_id, slug, title, summary, body_md, faq, tags, image_url, image_credit, source_url, trend_score, status)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            [
                post_id, n["id"], topic_id, post_slug,
                a.get("title", t), a.get("summary", "")[:200], a.get("body_md", ""),
                json.dumps(a.get("faq", [])), json.dumps(a.get("tags", [])),
                image, credit, src, c["score"],
                "draft" if cfg.get("review") else "published"
            ]
        )
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
    {"id": "12", "slug": "viral", "name": "Viral", "tagline": "Trending internet moments", "grp": "Entertainment", "icon": "rocket", "page_type": "feed", "seed_keywords": '[]', "fetchers": '["trends"]'}
]

def main():
    print("--- Running UniqueDigit Pipeline (Cloudflare D1 Edition) ---")
    niches = d1_query("SELECT * FROM niches WHERE active = 1 ORDER BY sort ASC")
    if not niches:
        print("[Notice] Using local baseline niches for dry run.")
        niches = SEED_NICHES

    if ONLY:
        niches = [n for n in niches if n["slug"] == ONLY]

    summary = {}
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
