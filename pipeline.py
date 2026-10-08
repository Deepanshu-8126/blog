"""
UniqueDigit daily pipeline (single file, DB-driven)

Usage:
  python pipeline.py                  # all active niches
  python pipeline.py --niche ai-tools # one niche
  python pipeline.py --dry            # no DB writes, prints only

Env: SUPABASE_URL, SUPABASE_SERVICE_KEY, GEMINI_API_KEY
Optional: GROK_API_KEY, TMDB_API_KEY, GEMINI_MODEL, GROK_MODEL, TRENDS_GEO, POSTS_PER_NICHE
"""
import json, os, re, sys, time, urllib.parse
from dotenv import load_dotenv
load_dotenv()

import requests
from supabase import create_client

DRY = "--dry" in sys.argv
ONLY = sys.argv[sys.argv.index("--niche") + 1] if "--niche" in sys.argv else None

GEMINI_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
GROK_KEY = os.environ.get("GROK_API_KEY")
GROK_MODEL = os.environ.get("GROK_MODEL", "grok-4")
TMDB_KEY = os.environ.get("TMDB_API_KEY")
GEO = os.environ.get("TRENDS_GEO", "IN")
N_POSTS = int(os.environ.get("POSTS_PER_NICHE", "3"))
UA = {"User-Agent": "UniqueDigitBot/1.0 (contact: info@uniquedigit.in)"}

SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "")

SB = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY) if (SUPABASE_URL and SUPABASE_SERVICE_KEY) else None


# ---------- helpers ----------
def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", str(s).lower()).strip("-")[:80]


def save(table, row, conflict=None):
    if DRY or not SB:
        print(f"[dry] {table}:", json.dumps(row, ensure_ascii=False)[:300])
        return {"id": None}
    q = SB.table(table)
    r = (q.upsert(row, on_conflict=conflict) if conflict else q.insert(row)).execute()
    return r.data[0] if r.data else {}


def gemini(prompt):
    if not GEMINI_KEY:
        print("GEMINI_API_KEY not set")
        return {"title": "Default Title", "summary": "Summary", "body_md": "Body content", "faq": [], "tags": []}
    r = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent",
        headers={"x-goog-api-key": GEMINI_KEY},
        json={"contents": [{"parts": [{"text": prompt}]}],
              "generationConfig": {"responseMimeType": "application/json", "temperature": 0.4}},
        timeout=90)
    r.raise_for_status()
    return json.loads(r.json()["candidates"][0]["content"]["parts"][0]["text"])


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


# ---------- sources ----------
def get_trends(seeds):
    """Google Trends rising queries (pytrends = unofficial; fallback exists)."""
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
        if not seeds:  # general trending searches
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
    """Returns {extract, image, url} or None. Image license: Wikipedia/Commons."""
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


def save_dataset(n, cfg):
    h = {}
    if cfg.get("auth_env"):
        h[cfg.get("auth_header", "Authorization")] = os.environ.get(cfg["auth_env"], "")
    try:
        d = requests.get(cfg["dataset_url"], headers=h, timeout=30)
        d.raise_for_status()
        save("datasets", {"niche_id": n["id"], "data": d.json()})
    except Exception as e:
        print(f"[{n['slug']}] dataset fetch failed:", e)


# ---------- AI steps ----------
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
    cfg = n.get("config") or {}
    prompt = f"""Write a helpful article for an Indian audience. Niche: {n['name']}.
Title idea: {title}. Angle: {angle}. Google Trends interest score: {trend}.
FACTS (use ONLY these; do not invent statistics, prices, dates, quotes, or product claims):
{facts or 'No extra facts available - keep it general, explanatory, and clearly hedged.'}
Rules: plain simple English/Hinglish-friendly, no clickbait, no medical/financial advice{', add a short safety note' if cfg.get('disclaimer') else ''}.
Return JSON: {{"title":"","summary":"<=160 chars","body_md":"400-600 words markdown with ## headings","faq":[{{"q":"","a":""}}],"tags":["",""]}}"""
    return gemini(prompt)


# ---------- affiliate ----------
def fill_affiliate():
    if not SB:
        return
    rules = {r["domain"]: r["template"] for r in SB.table("affiliate_rules").select("*").execute().data}
    for p in SB.table("products").select("id,url").is_("aff_url", "null").execute().data:
        host = urllib.parse.urlparse(p["url"]).netloc.replace("www.", "")
        tpl = next((t for d, t in rules.items() if d in host), None)
        if tpl and not DRY:
            link = tpl.replace("{enc_url}", urllib.parse.quote(p["url"], safe="")).replace("{url}", p["url"])
            SB.table("products").update({"aff_url": link}).eq("id", p["id"]).execute()


# ---------- per niche ----------
def process(n):
    cfg, fetchers = n.get("config") or {}, n.get("fetchers") or []
    made = 0
    if cfg.get("dataset_url"):
        save_dataset(n, cfg)
    if n["page_type"] == "dataset":
        return 0

    cands = {}  # title -> {score, image, credit, facts, url}
    if "trends" in fetchers:
        for q, v in get_trends(n.get("seed_keywords") or []).items():
            cands[q] = {"score": v}
    if "tmdb" in fetchers:
        for m in tmdb_trending():
            cands[m["title"]] = {"score": 100, "image": m["image"], "credit": "TMDB",
                                 "facts": m["facts"], "url": "https://www.themoviedb.org/"}
    if not cands:
        cands = {t: {"score": s} for t, s in ai_topics(n).items()}

    seen = {r["slug"] for r in SB.table("topics").select("slug").eq("niche_id", n["id"]).execute().data} if SB else set()
    titles = [t for t in cands if slugify(t) not in seen][:25]
    if not titles:
        print(f"[{n['slug']}] nothing new")
        return 0

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
        topic = save("topics", {"niche_id": n["id"], "title": t, "slug": slugify(t),
                                "trend_score": c["score"], "source": "tmdb" if "tmdb" in (n.get("fetchers") or []) else "trends"},
                     "niche_id,slug")
        save("posts", {"niche_id": n["id"], "topic_id": topic.get("id"), "slug": slugify(a["title"]) or slugify(t),
                       "title": a["title"], "summary": a["summary"][:200], "body_md": a["body_md"],
                       "faq": a.get("faq", []), "tags": a.get("tags", []),
                       "image_url": image, "image_credit": credit, "source_url": src,
                       "trend_score": c["score"],
                       "status": "draft" if cfg.get("review") else "published"},
             "niche_id,slug")
        made += 1
        time.sleep(1)
    return made


def main():
    if not SB:
        print("SUPABASE credentials not found. Running in mock/dry mode.")
        return
    q = SB.table("niches").select("*").eq("active", True)
    if ONLY:
        q = q.eq("slug", ONLY)
    summary, err = {}, None
    for n in q.execute().data:
        try:
            summary[n["slug"]] = process(n)
            print(f"[{n['slug']}] posts: {summary[n['slug']]}")
        except Exception as e:
            summary[n["slug"]] = f"ERROR {e}"
            err = (err or "") + f"{n['slug']}: {e}\n"
            print(f"[{n['slug']}] failed:", e)
    try:
        fill_affiliate()
    except Exception as e:
        err = (err or "") + f"affiliate: {e}\n"
    save("pipeline_runs", {"ok": err is None, "summary": summary, "error": err})
    if err:
        sys.exit(1)


if __name__ == "__main__":
    main()
