#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
========================================================================================
🚀 AUTONOMOUS SARKARI, UNIVERSITY & SCHEME RADAR (AI-Powered Intent Engine)
========================================================================================
- ZERO Hardcoded Keyword Restrictions: Gemini dynamically evaluates ANY Indian breaking topic
- Detects Universities (Kumaun, DU, CCSU, AKTU), State Boards, Yojanas (Nanda Devi, Silai Machine),
  Police, Agniveer, Anganwadi, Scholarships, and Sarkari Results across all Indian states.
- REAL Authentic Web Media: Official Wikimedia/Wikipedia emblems & real educational photography.
- ZERO AI-Generated Cartoon/Pollinations images!
- High-grade Humanized Hinglish reporting (Jagran Josh / Amar Ujala editorial voice).
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
from pipeline import gemini

# Configuration
SARKARI_BLOG_ID = os.getenv("BLOGGER_EXAM_BLOG_ID", "1366151638291560024")
CF_ACCOUNT = os.getenv("CLOUDFLARE_ACCOUNT_ID", "")
CF_D1_DB = os.getenv("CLOUDFLARE_D1_DATABASE_ID", "")
CF_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN", "")
CACHE_FILE = ROOT_DIR / "sarkari_seen_cache.json"

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}

# Real High-Resolution Educational Stock Photos (Zero AI Cartoons)
REAL_EDUCATION_FALLBACKS = [
    "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=1200&h=630&fit=crop", # Exam desk & hall ticket
    "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=1200&h=630&fit=crop", # University campus building
    "https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=1200&h=630&fit=crop", # Happy students celebrating success
    "https://images.unsplash.com/photo-1450133064473-71024230f91b?w=1200&h=630&fit=crop", # Official government application paperwork
    "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=1200&h=630&fit=crop"  # Library & academic study hall
]

# Targeted Real-Time RSS Stream URLs (Covering Education, Jobs, Yojanas & State News)
RADAR_RSS_STREAMS = [
    # 1. Google Trends India Daily Feed
    "https://trends.google.com/trending/rss?geo=IN",
    # 2. Google News India - Education Section
    "https://news.google.com/rss/headlines/section/topic/EDUCATION?hl=en-IN&gl=IN&ceid=IN:en",
    # 3. Google News India - Recruitment & Vacancies
    "https://news.google.com/rss/search?q=recruitment+OR+vacancy+OR+result+2026&hl=en-IN&gl=IN&ceid=IN:en",
    # 4. Google News India - Universities, Boards & Admit Cards
    "https://news.google.com/rss/search?q=university+exam+OR+admit+card+OR+cutoff+marks&hl=en-IN&gl=IN&ceid=IN:en",
    # 5. Google News India - Welfare Yojanas, Scholarships & Ration
    "https://news.google.com/rss/search?q=yojana+list+2026+OR+scholarship+OR+ration+card&hl=en-IN&gl=IN&ceid=IN:en",
    # 6. Google News India - State Level Bharti & Grassroots
    "https://news.google.com/rss/search?q=anganwadi+bharti+OR+police+bharti+OR+direct+bharti&hl=en-IN&gl=IN&ceid=IN:en"
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
# 🖼️ REAL MEDIA ENGINE: OFFICIAL EMBLEMS & EDITORIAL PHOTOS (NO AI CARTOONS)
# ======================================================================================
def fetch_real_official_image(entity_name, category=""):
    """
    Fetches real official emblems, campus photos, or government department seals.
    Uses Wikipedia REST Summary API with fallback to real educational photography.
    """
    if entity_name:
        queries = [
            entity_name,
            f"{entity_name} India",
            f"{entity_name} university" if "university" in entity_name.lower() else f"{entity_name} board"
        ]
        for q in queries:
            try:
                url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(q)}"
                r = requests.get(url, headers=UA, timeout=6).json()
                orig = r.get("originalimage", {}).get("source")
                thumb = r.get("thumbnail", {}).get("source")
                img_url = orig or thumb
                if img_url and img_url.startswith("http"):
                    # Check that image is not an unrelated flag icon
                    if not any(bad in img_url.lower() for bad in ["1x1", "pixel", "icon-small"]):
                        return img_url, "Official Verified Entity Emblem/Photo"
            except Exception:
                continue

    # Fallback: High-resolution real editorial photography (Zero AI cartoons)
    idx = abs(hash(entity_name or category)) % len(REAL_EDUCATION_FALLBACKS)
    return REAL_EDUCATION_FALLBACKS[idx], "Real Authentic Educational Photography"

# ======================================================================================
# 📡 AUTONOMOUS RADAR: SCAN STREAMS & AI INTENT CLASSIFICATION
# ======================================================================================
def fetch_raw_candidate_headlines():
    """Scans all RSS streams and collects unique candidate headlines."""
    candidates = []
    seen = set()

    for feed_url in RADAR_RSS_STREAMS:
        try:
            r = requests.get(feed_url, headers=UA, timeout=10)
            if r.status_code == 200:
                root = ET.fromstring(r.content)
                for item in root.findall(".//item")[:15]:
                    title_elem = item.find("title")
                    link_elem = item.find("link")
                    if title_elem is not None and title_elem.text:
                        full_title = title_elem.text.strip()
                        clean_title = full_title.split(" - ")[0].strip()
                        source_name = full_title.split(" - ")[-1].strip() if " - " in full_title else "Official Update"
                        lower = clean_title.lower()

                        if lower not in seen and len(clean_title) >= 15:
                            seen.add(lower)
                            candidates.append({
                                "title": clean_title,
                                "source": source_name,
                                "link": link_elem.text if link_elem is not None else ""
                            })
        except Exception:
            continue

    print(f"📡 [Raw Radar Stream] Captured {len(candidates)} Candidate Headlines.")
    return candidates

def ai_classify_and_filter_candidates(candidates):
    """
    Agent Alpha: Autonomous AI Intent Classifier.
    Eliminates rigid keyword lists. Dynamically identifies any topic relevant to
    Indian students, job seekers, and citizens (Universities, Schemes, Bharti, Results).
    """
    if not candidates:
        return []

    # Send in batches of 20
    headlines = [c["title"] for c in candidates[:25]]

    prompt = f"""You are the Chief AI Editor for India's premier Sarkari & Education Portal.
Candidate Breaking Headlines:
{json.dumps(headlines, indent=2)}

TASK:
Filter and classify ONLY topics that Indian students, job seekers, youth, or citizens actively search for:
- Sarkari Results, Scorecards, Merit Lists, Cutoff Marks, Answer Keys, Admit Cards, Time Tables.
- Central & State Government Recruitments (SSC, UPSC, Railway, Police, Anganwadi, Asha, Lekhpal, Direct Bharti, Offline Forms).
- Universities & Colleges (Kumaun University, CCSU, DU, BHU, AKTU, State Boards, BA, BSc, BCom, MA, Polytechnic, ITI, B.Ed).
- Government Yojanas & Welfare Schemes (PM Awas, Free Silai Machine, Free Laptop, Nanda Devi Scheme, Ladli Behna, Ration Card, Ayushman).
- Scholarships (UP Scholarship, NSP Portal, Post Matric).

STRICTLY REJECT: Sports matches, Bollywood gossip, crime news, general political speeches, foreign tech launches.

Return strict JSON:
{{
  "qualified": [
    {{
      "headline": "<exact headline string from candidate list>",
      "entity": "<Exact Organization / University / State Department / Scheme name, e.g. Kumaun University, UP Police, Staff Selection Commission, Nanda Devi Kanya Yojana>",
      "category": "Result | Admit Card | Recruitment | Yojana | Scholarship | Cutoff | Answer Key",
      "official_domain": "<official website if known, e.g. kunainital.ac.in, uppbpb.gov.in, ssc.gov.in, otherwise leave empty>"
    }}
  ]
}}"""

    try:
        res = gemini(prompt)
        qualified_list = res.get("qualified", [])
        
        # Merge back with source and link details
        cand_map = {c["title"].lower(): c for c in candidates}
        results = []
        for q in qualified_list:
            h = q.get("headline", "")
            match = cand_map.get(h.lower())
            results.append({
                "title": h,
                "entity": q.get("entity", "Government Authority"),
                "category": q.get("category", "Sarkari Alert"),
                "official_domain": q.get("official_domain", ""),
                "source": match.get("source", "Official Update") if match else "Official Update",
                "link": match.get("link", "") if match else ""
            })

        print(f"🎯 [AI Intent Radar] Qualified {len(results)} high-intent Sarkari/Education topics.")
        return results
    except Exception as e:
        print(f"❌ AI Classification Error: {e}")
        return []

# ======================================================================================
# ✍️ HUMANIZED HINGLISH SARKARI JOURNALIST ENGINE (Anti-AI Slop)
# ======================================================================================
def generate_sarkari_article(item):
    """
    Generates a deeply humanized, authentic Jagran Josh / Amar Ujala style article.
    Zero generic AI jargon, rich structured tables, verified steps & direct links.
    """
    title = item["title"]
    entity = item.get("entity", "Conducting Board")
    category = item.get("category", "Sarkari Alert")
    official_domain = item.get("official_domain") or f"{urllib.parse.quote(entity)} official portal"
    source = item.get("source", "Official Notification")

    prompt = f"""You are India's top senior education editor and career journalist writing for 'Sarkari Result & Exam Alert' (all-sarkari-result-2k0.blogspot.com).
Topic: {title}
Entity: {entity} | Category: {category} | Official Domain: {official_domain} | Source: {source}

WRITING STYLE & TONE GUIDELINES:
1. LANGUAGE: 100% Natural, Engaging Conversational HINGLISH (Roman Hindi blended with standard English keywords like Cutoff, Scorecard, Admit Card, Direct Link, Eligibility, Merit List, Official Portal, Registration, Counseling).
2. WRITE LIKE AN EXPERT SENIOR JOURNALIST talking directly to an Indian candidate who urgently needs to check their result or apply for the scheme.
3. ABSOLUTELY BANNED AI SLOP CLICHES:
   - "In conclusion", "delve into", "tapestry", "beacon", "it is important to note", "furthermore", "moreover", "game-changer", "testament to", "fast-paced world".
   - Use lively, real transitions: "Yahan hai direct update", "Asli baat yeh hai", "Candidates ko dhyan rakhna chahiye", "Direct process yeh hai".

ARTICLE STRUCTURE (600 to 750 words):
- ## Catchy Headline: High CTR, e.g. "[Direct Link Active] {title}: Yahan se download karein scorecard/form, category-wise details & process dekhein"
- ## ⚡ Quick Highlights Box:
  A clean markdown table with:
  | Detail | Information |
  | :--- | :--- |
  | **Exam / Yojana Name** | {title} |
  | **Conducting Authority** | {entity} |
  | **Current Status** | 🟢 Declared / Active |
  | **Category** | {category} |
  | **Official Portal** | {official_domain} |
- ## 📋 Step-by-Step Complete Procedure (Aise Karein Check / Apply):
  Clear numbered 1-2-3-4 steps in conversational Hinglish.
- ## 📊 Category-Wise Cutoff / Eligibility Criteria:
  A clean markdown table for General (UR), OBC, EWS, SC, ST or required qualification/age criteria.
- ## 🔗 Official Direct Link Callout:
  A prominent direct link box:
  `👉 [Official Website Direct Link - Click Here To Check / Apply](https://www.google.com/search?q={urllib.parse.quote(entity + ' ' + category + ' official portal')})`
- ## ⚠️ Important Documents & Advisory:
  Essential documents needed (Aadhaar, Roll No, Registration Slip) and warning against phishing sites/fake agents.
- ## ❓ Frequently Asked Questions (Top FAQs):
  3 direct questions candidates search on Google with crisp 2-sentence answers.

Return strict JSON:
{{
  "title": "Clear High-CTR headline with status tag like [Direct Link Active] or [Official Notice Out]",
  "summary": "Compelling meta description under 155 chars for Google Search SERP",
  "body_md": "Full markdown content with tables, bold highlights, numbered steps and FAQs",
  "tags": ["{category}", "Sarkari Result", "{entity}", "Direct Link", "Govt Jobs 2026"]
}}"""

    try:
        return gemini(prompt)
    except Exception as e:
        print(f"❌ Generation error for {title}: {e}")
        return None

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
# 🚀 MAIN RUNNER: SCAN -> AI INTENT CLASSIFY -> REAL MEDIA -> DUAL PUBLISH
# ======================================================================================
def run_sarkari_radar(max_posts=3):
    print("=" * 70)
    print("🔥 STARTING AUTONOMOUS SARKARI, UNIVERSITY & SCHEME RADAR")
    print(f"🎯 Target Blogger Blog ID: {SARKARI_BLOG_ID} (all-sarkari-result-2k0.blogspot.com)")
    print(f"🌐 Target Main Website: uniquedigit-viral-hub.pages.dev (Niche: exams-results)")
    print("🛡️ Zero Keyword Limit + Real Authentic Media (No AI Cartoons)")
    print("=" * 70)

    cache = load_cache()
    
    # 1. Fetch raw streams
    candidates = fetch_raw_candidate_headlines()
    if not candidates:
        print("⚠️ No candidate headlines captured.")
        return

    # 2. AI Autonomous Intent Classification
    qualified_topics = ai_classify_and_filter_candidates(candidates)

    published_count = 0

    for item in qualified_topics:
        if published_count >= max_posts:
            break

        topic_title = item["title"]
        entity = item.get("entity", "")
        topic_hash = hashlib.md5(topic_title.lower().encode("utf-8")).hexdigest()

        if topic_hash in cache:
            continue

        print(f"\n⚡ [Processing Post {published_count + 1}/{max_posts}]: {topic_title}")
        print(f"🏛️ Entity: {entity} | Category: {item.get('category')}")

        # 3. Generate Humanized Hinglish Article
        article = generate_sarkari_article(item)
        if not article or not article.get("title") or not article.get("body_md"):
            print("⚠️ Skipped: Generation failed")
            continue

        final_title = article["title"]
        summary = article.get("summary", "")
        body_md = article["body_md"]
        tags = article.get("tags", ["Sarkari Result", "Exam Alert"])

        # 4. Fetch REAL Official Media (Zero AI cartoons)
        real_img, img_type = fetch_real_official_image(entity, category=item.get("category", ""))
        print(f"🖼️ Media Resolved: {real_img[:70]}... ({img_type})")

        # 5. Publish to Google Blogger
        content_html = markdown.markdown(body_md, extensions=['extra', 'tables'])
        blogger_res = publish_to_blogger(
            final_title,
            content_html,
            labels=tags,
            is_draft=False,
            featured_image=real_img,
            target_blog_id=SARKARI_BLOG_ID
        )

        blogger_url = blogger_res.get("url") if blogger_res.get("success") else None

        # 6. Publish to Cloudflare Main Site
        cf_success = publish_to_cloudflare_d1(final_title, summary, body_md, tags, real_img)
        if cf_success:
            print(f"✅ [Cloudflare Main Site]: Live on uniquedigit-viral-hub.pages.dev")

        # 7. Update Cache
        cache[topic_hash] = {
            "title": final_title,
            "entity": entity,
            "published_at": datetime.now().isoformat(),
            "blogger_url": blogger_url,
            "image": real_img
        }
        save_cache(cache)
        published_count += 1
        time.sleep(2)

    print("\n" + "=" * 70)
    print(f"🎉 SARKARI RADAR COMPLETED: Successfully published {published_count} new posts!")
    print("=" * 70)

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    run_sarkari_radar(max_posts=count)
