#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
========================================================================================
🚀 SARKARI RESULT & SCHEME RADAR ENGINE (Autonomous 24/7 Publisher)
========================================================================================
Dedicated Isolated Pipeline for:
- Central & State Govt Jobs (SSC, UPSC, Railway, Police, Anganwadi, Asha, Lekhpal)
- Defence & Forces (Agniveer Army, Navy, Airforce, NDA, CDS)
- All Universities & Colleges (BA, BSc, BCom, MA, ITI, Polytechnic, Board Results)
- Sarkari Yojanas (PM Kisan, Free Silai Machine, Free Laptop, Awas, Ladli Behna, Nanda Devi)
- Direct Bharti, Offline Forms, Admit Cards, Answer Keys, Cutoffs & Last Date Alerts

Destination Routing:
- Google Blogger: 'Sarkari Result & Exam Alert' (Blog ID: 1366151638291560024)
- Cloudflare D1 Main Portal: 'uniquedigit-viral-hub.pages.dev' (Category: exams-results)
========================================================================================
"""

import os
import sys
import json
import re
import time
import hashlib
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

# Force UTF-8 encoding on Windows
if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Root path resolution
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from dotenv import load_dotenv
load_dotenv(ROOT_DIR / ".env")

import requests
import markdown
from bridges.blogger_bridge.blogger_publisher import publish_to_blogger

# Configuration
SARKARI_BLOG_ID = os.getenv("BLOGGER_EXAM_BLOG_ID", "1366151638291560024")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
CF_ACCOUNT = os.getenv("CLOUDFLARE_ACCOUNT_ID", "")
CF_D1_DB = os.getenv("CLOUDFLARE_D1_DATABASE_ID", "")
CF_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN", "")
CACHE_FILE = ROOT_DIR / "sarkari_seen_cache.json"

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}

# ======================================================================================
# 🎯 DYNAMIC INTENT & SARKARI TOPIC PATTERNS
# ======================================================================================
SARKARI_INTENT_KEYWORDS = [
    # Exam & Results
    "result", "scorecard", "merit list", "marksheet", "allotment", "cut off", "cutoff",
    # Hall Ticket & Answers
    "admit card", "hall ticket", "call letter", "answer key", "answer sheet", "omr",
    # Syllabus & Pattern
    "syllabus", "exam pattern", "previous paper", "model paper", "exam date",
    # Yojanas & Schemes
    "yojana", "scheme", "awas yojana", "silai machine", "free laptop", "smartphone yojana",
    "ladli behna", "nanda devi", "shiksha prothsahan", "kanya sumangala", "pm kisan",
    # Scholarships & Welfare
    "scholarship", "nsp portal", "up scholarship", "ration card", "ayushman card", "voter list",
    # Central Jobs
    "ssc cgl", "ssc chsl", "ssc gd", "ssc mts", "upsc", "railway", "rrb", "group d", "ntpc",
    # State & Police & Grassroots Bharti
    "police bharti", "lekhpal", "patwari", "anganwadi", "asha", "gram sevak", "peon bharti",
    "uksssc", "ukpsc", "upsssc", "bssc", "jssc", "hssc", "rsmssb", "mppeb", "vyapam",
    # Defence & Forces
    "agniveer", "army bharti", "navy bharti", "airforce", "nda", "cds", "crpf", "bsf", "cisf",
    # Banks
    "ibps", "sbi po", "sbi clerk", "rbi assistant",
    # University & Academic Boards
    "university", "kumaun university", "garwal university", "ccsu", "aktu", "du", "bhu",
    "polytechnic", "iti", "ba result", "bsc result", "bcom result", "ma result", "b.ed",
    "cbse", "up board", "bihar board", "uk board", "hbse", "rbse", "neet", "jee", "cuet", "ctet",
    # Offline & Special
    "offline form", "direct bharti", "walk in interview", "joining letter", "document verification",
    "last date", "aaj last date"
]

# Targeted Google News RSS Query Feeds
SARKARI_RSS_FEEDS = [
    "https://news.google.com/rss/search?q=sarkari+result+OR+admit+card+OR+cutoff+marks&hl=en-IN&gl=IN&ceid=IN:en",
    "https://news.google.com/rss/search?q=anganwadi+bharti+OR+police+bharti+OR+direct+recruitment+2026&hl=en-IN&gl=IN&ceid=IN:en",
    "https://news.google.com/rss/search?q=yojana+list+2026+OR+scholarship+status+OR+ration+card&hl=en-IN&gl=IN&ceid=IN:en",
    "https://news.google.com/rss/search?q=university+results+2026+OR+polytechnic+OR+ITI+result&hl=en-IN&gl=IN&ceid=IN:en",
    "https://news.google.com/rss/search?q=SSC+OR+Railway+RRB+OR+Agniveer+Bharti+2026&hl=en-IN&gl=IN&ceid=IN:en",
    "https://news.google.com/rss/search?q=Uttarakhand+recruitment+OR+UPSSSC+OR+BSSC+notification&hl=en-IN&gl=IN&ceid=IN:en",
]

def load_cache():
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_cache(cache):
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

# ======================================================================================
# 📡 RADAR: FETCH REAL-TIME BREAKING SARKARI SIGNALS
# ======================================================================================
def fetch_sarkari_trends():
    """Scans Google Trends Daily Feed & 6 Targeted Sarkari News Feeds."""
    signals = []
    seen_titles = set()

    # 1. Official Google Trends India Daily Feed
    try:
        r = requests.get("https://trends.google.com/trending/rss?geo=IN", headers=UA, timeout=10)
        if r.status_code == 200:
            root = ET.fromstring(r.content)
            for item in root.findall(".//item"):
                title_elem = item.find("title")
                if title_elem is not None and title_elem.text:
                    t = title_elem.text.strip()
                    lower_t = t.lower()
                    if any(k in lower_t for k in SARKARI_INTENT_KEYWORDS):
                        if lower_t not in seen_titles:
                            seen_titles.add(lower_t)
                            signals.append({
                                "title": t,
                                "source": "Google Trends Daily",
                                "raw_facts": f"Trending in India right now on Google Search: {t}"
                            })
    except Exception as e:
        print(f"⚠️ Trends RSS Error: {e}")

    # 2. Targeted Sarkari & State Board RSS Feeds
    for feed_url in SARKARI_RSS_FEEDS:
        try:
            r = requests.get(feed_url, headers=UA, timeout=10)
            if r.status_code == 200:
                root = ET.fromstring(r.content)
                for item in root.findall(".//item")[:10]:
                    title_elem = item.find("title")
                    link_elem = item.find("link")
                    if title_elem is not None and title_elem.text:
                        full_title = title_elem.text.strip()
                        clean_title = full_title.split(" - ")[0].strip()
                        source_name = full_title.split(" - ")[-1].strip() if " - " in full_title else "Official Update"
                        lower_clean = clean_title.lower()

                        if any(k in lower_clean for k in SARKARI_INTENT_KEYWORDS):
                            if lower_clean not in seen_titles:
                                seen_titles.add(lower_clean)
                                signals.append({
                                    "title": clean_title,
                                    "source": source_name,
                                    "link": link_elem.text if link_elem is not None else "",
                                    "raw_facts": f"Latest verified notice reported by {source_name}: {full_title}"
                                })
        except Exception:
            continue

    print(f"📡 [Sarkari Radar] Scanned & Discovered {len(signals)} Active Signals.")
    return signals

# ======================================================================================
# ✍️ HUMANIZED HINGLISH SARKARI JOURNALIST ENGINE (Anti-AI Slop)
# ======================================================================================
def generate_sarkari_article(signal):
    """
    Generates a 100% humanized, authentic Jagran Josh / SarkariNetwork style article.
    Zero generic cliches, zero AI-slop, rich tables & direct official links.
    """
    title = signal["title"]
    source = signal.get("source", "Official Update")
    facts = signal.get("raw_facts", "")

    prompt = f"""You are India's top education and Sarkari job editor for 'Sarkari Result & Exam Alert' (all-sarkari-result-2k0.blogspot.com).
Breaking Topic: {title}
Source Info: {source} | Verified Facts: {facts}

WRITING STYLE & TONE GUIDELINES:
1. LANGUAGE: 100% Natural, Engaging Conversational HINGLISH (Roman Hindi script blended with English terminology like Cutoff, Scorecard, Admit Card, Direct Link, Eligibility, Merit List, Official Portal, Registration).
2. WRITE LIKE AN EXPERT SENIOR JOURNALIST explaining step-by-step to an Indian candidate who urgently needs to check or apply.
3. ABSOLUTELY BANNED AI PHRASES:
   - "In conclusion", "delve into", "tapestry", "beacon", "it is important to note", "furthermore", "moreover", "game-changer", "testament to".
4. STRUCTURE REQUIREMENTS (550 to 700 words):
   - ## Catchy Headline: High CTR, e.g. "[Direct Link Active] {title}: Yahan se karein direct download, dekhein category-wise details & process"
   - ## ⚡ Quick Overview Highlights Box:
     A clean markdown table with:
     | Detail | Information |
     | :--- | :--- |
     | **Exam / Yojana Name** | ... |
     | **Conducting Authority** | ... |
     | **Status** | 🟢 Active / Declared |
     | **Category** | Sarkari Result / Admit Card / Yojana |
     | **Official Portal** | Official website name/domain |
   - ## 📋 Step-by-Step Complete Procedure (Aise Karein Check / Apply):
     Clear numbered 1-2-3-4 steps in conversational Hinglish.
   - ## 📊 Category-Wise Cutoff / Eligibility Criteria:
     A clear markdown table for General (UR), OBC, EWS, SC, ST or required qualification/age limits.
   - ## 🔗 Official Direct Link Callout:
     A prominent direct link box for the user:
     `👉 [Official Website Direct Link - Click Here To Check / Apply](https://google.com/search?q={urllib.parse.quote(title + ' official website')})`
   - ## ⚠️ Important Documents & Advisory:
     Documents needed (Aadhaar, Roll No, Marksheet) and warning against fake brokers/phishing portals.
   - ## ❓ Frequently Asked Questions (Top FAQs):
     3 questions Indian candidates search on Google with crisp 2-sentence answers.

Return strict JSON:
{{
  "title": "Clear High-CTR headline with status tag like [Declared] or [Direct Link Active]",
  "summary": "Compelling meta description under 155 chars for Google Search SERP",
  "body_md": "Full markdown content with tables, bold highlights and steps",
  "tags": ["Sarkari Result", "Admit Card", "Exam Alert 2026", "Direct Link", "Govt Jobs"]
}}"""

    try:
        from pipeline import gemini
        return gemini(prompt)
    except Exception as e:
        print(f"❌ Gemini Generation Error: {e}")
        return None


# ======================================================================================
# 🖼️ DYNAMIC 1200x630 TOPIC-SPECIFIC BANNER GENERATOR
# ======================================================================================
def get_sarkari_banner_image(topic_title):
    """Generates a dynamic 1200x630 high-res visual banner specifically for this exam/scheme."""
    clean_topic = re.sub(r'[^a-zA-Z0-9\s]', '', topic_title).strip()[:75]
    prompt_str = f"{clean_topic} Indian students examination hall government notice educational banner high quality photograph"
    encoded = urllib.parse.quote(prompt_str)
    return f"https://image.pollinations.ai/prompt/{encoded}?width=1200&height=630&nologo=true"

# ======================================================================================
# 🌐 CLOUDFLARE D1 MAIN WEBSITE PUBLISHER
# ======================================================================================
def publish_to_cloudflare_d1(title, summary, body_md, tags, image_url):
    """Stores article in D1 SQLite so it shows live on uniquedigit-viral-hub.pages.dev"""
    if not (CF_ACCOUNT and CF_D1_DB and CF_TOKEN):
        return False

    slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')[:80]
    sql = """
    INSERT INTO posts (slug, title, summary, body_md, image_url, niche_id, tags, published_at, view_count)
    VALUES (?, ?, ?, ?, ?, (SELECT id FROM niches WHERE slug = 'exams-results' LIMIT 1), ?, datetime('now'), 0)
    ON CONFLICT(slug) DO UPDATE SET title=excluded.title, body_md=excluded.body_md;
    """
    params = [slug, title, summary, body_md, image_url, json.dumps(tags)]

    url = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT}/d1/database/{CF_D1_DB}/query"
    headers = {"Authorization": f"Bearer {CF_TOKEN}", "Content-Type": "application/json"}
    try:
        r = requests.post(url, headers=headers, json={"sql": sql, "params": params}, timeout=20)
        return r.status_code == 200
    except Exception:
        return False

# ======================================================================================
# 🚀 MAIN RUNNER: SCAN -> GENERATE -> DUAL PUBLISH
# ======================================================================================
def run_sarkari_radar(max_posts=3):
    print("=" * 70)
    print("🔥 STARTING SARKARI & EXAM RESULT RADAR PIPELINE")
    print(f"🎯 Target Blogger Blog ID: {SARKARI_BLOG_ID} (all-sarkari-result-2k0.blogspot.com)")
    print(f"🌐 Target Main Website: uniquedigit-viral-hub.pages.dev (Niche: exams-results)")
    print("=" * 70)

    cache = load_cache()
    signals = fetch_sarkari_trends()

    published_count = 0

    for s in signals:
        if published_count >= max_posts:
            break

        topic_title = s["title"]
        topic_hash = hashlib.md5(topic_title.lower().encode("utf-8")).hexdigest()

        if topic_hash in cache:
            continue

        print(f"\n⚡ [Processing Signal {published_count + 1}/{max_posts}]: {topic_title}")

        # 1. Generate Article
        article = generate_sarkari_article(s)
        if not article or not article.get("title") or not article.get("body_md"):
            print("⚠️ Skipped: Failed generation")
            continue

        final_title = article["title"]
        summary = article.get("summary", "")
        body_md = article["body_md"]
        tags = article.get("tags", ["Sarkari Result", "Exam Alert"])

        # 2. Dynamic Banner Image
        banner_img = get_sarkari_banner_image(topic_title)
        print(f"🖼️ Banner Generated: {banner_img[:80]}...")

        # 3. Publish to Google Blogger
        content_html = markdown.markdown(body_md, extensions=['extra', 'tables'])
        blogger_res = publish_to_blogger(
            final_title,
            content_html,
            labels=tags,
            is_draft=False,
            featured_image=banner_img,
            target_blog_id=SARKARI_BLOG_ID
        )

        blogger_url = blogger_res.get("url") if blogger_res.get("success") else None

        # 4. Publish to Cloudflare Main Site
        cf_success = publish_to_cloudflare_d1(final_title, summary, body_md, tags, banner_img)
        if cf_success:
            print(f"✅ [Cloudflare Main Site]: Published to uniquedigit-viral-hub.pages.dev")

        # 5. Update Cache
        cache[topic_hash] = {
            "title": final_title,
            "published_at": datetime.now().isoformat(),
            "blogger_url": blogger_url
        }
        save_cache(cache)
        published_count += 1
        time.sleep(2)

    print("\n" + "=" * 70)
    print(f"🎉 SARKARI RADAR COMPLETED: Published {published_count} new posts!")
    print("=" * 70)

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    run_sarkari_radar(max_posts=count)
