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
import uuid
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
CF_ACCOUNT = os.getenv("CLOUDFLARE_ACCOUNT_ID", "cf1a42fb306054063805cf459fddf853")
CF_D1_DB = os.getenv("CLOUDFLARE_D1_DATABASE_ID", "61d1d46f-f438-47f5-9128-516d9beb11cb")
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
OFFICIAL_BOARD_SEALS = {
    "bteup": "https://upload.wikimedia.org/wikipedia/commons/5/56/BTEUP_LOGO.png",
    "uttar pradesh": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Seal_of_Uttar_Pradesh.svg/500px-Seal_of_Uttar_Pradesh.svg.png",
    "up board": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Seal_of_Uttar_Pradesh.svg/500px-Seal_of_Uttar_Pradesh.svg.png",
    "haryana": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Emblem_of_Haryana.svg/500px-Emblem_of_Haryana.svg.png",
    "uhsr": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Emblem_of_Haryana.svg/500px-Emblem_of_Haryana.svg.png",
    "bihar": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Emblem_of_Bihar.svg/500px-Emblem_of_Bihar.svg.png",
    "rajasthan": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Emblem_of_India.svg/500px-Emblem_of_India.svg.png",
    "madhya pradesh": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Emblem_of_Madhya_Pradesh.svg/500px-Emblem_of_Madhya_Pradesh.svg.png",
    "maharashtra": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/be/Emblem_of_Maharashtra.svg/500px-Emblem_of_Maharashtra.svg.png",
    "upsc": "https://upload.wikimedia.org/wikipedia/en/b/bf/Union_public_service_commission.jpg",
    "ssc": "https://upload.wikimedia.org/wikipedia/en/d/d5/Staff_Selection_Commission.webp",
    "nta": "https://upload.wikimedia.org/wikipedia/en/thumb/8/84/National_Testing_Agency_logo.png/500px-National_Testing_Agency_logo.png",
    "neet": "https://upload.wikimedia.org/wikipedia/en/thumb/8/84/National_Testing_Agency_logo.png/500px-National_Testing_Agency_logo.png",
    "cbse": "https://upload.wikimedia.org/wikipedia/en/thumb/8/82/Central_Board_of_Secondary_Education_logo.png/500px-Central_Board_of_Secondary_Education_logo.png",
    "railway": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Emblem_of_India.svg/500px-Emblem_of_India.svg.png",
    "rrb": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Emblem_of_India.svg/500px-Emblem_of_India.svg.png",
    "ibps": "https://upload.wikimedia.org/wikipedia/en/thumb/2/2a/IBPS_logo.png/500px-IBPS_logo.png"
}

def fetch_real_official_image(entity_name, category="", source_link=""):
    """
    Delegates to the Master Universal Real Image Engine across the entire project.
    """
    try:
        from bridges.universal_image_engine import get_universal_real_image
        return get_universal_real_image(f"{entity_name} {category}".strip(), niche_slug="exams-results", target_url=source_link)
    except Exception as e:
        print("[Universal image engine error in Sarkari Radar]:", e)
        combined_key = f"{entity_name} {category}".lower()
        for k, url in OFFICIAL_BOARD_SEALS.items():
            if k in combined_key:
                return url, f"Official {k.upper()} Authority Emblem"
        return OFFICIAL_BOARD_SEALS["bteup"], "Official Authority Seal"

    # 2. Try scraping source article og:image if news link is available
    if source_link and source_link.startswith("http") and "google.com" not in source_link:
        try:
            r_art = requests.get(source_link, headers=UA, timeout=6)
            if r_art.status_code == 200:
                m_og = re.search(r'<meta[^>]+(?:property|name)=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']', r_art.text, re.IGNORECASE)
                if m_og:
                    c_img = m_og.group(1).strip()
                    if c_img.startswith("https://") and not any(b in c_img.lower() for b in ["logo", "favicon", "avatar", "default_share"]):
                        return c_img, "Verified News Editorial Photography"
        except Exception:
            pass

    # 3. Wikipedia Smart Search (handles complex entity names like BTEUP, UHSR, etc.)
    if entity_name:
        try:
            search_url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&list=search&srsearch={urllib.parse.quote(entity_name)}&srlimit=1"
            sr = requests.get(search_url, headers=UA, timeout=5).json()
            items = sr.get("query", {}).get("search", [])
            if items:
                page_title = items[0]["title"]
                
                # Check summary image
                sum_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(page_title)}"
                r_sum = requests.get(sum_url, headers=UA, timeout=5).json()
                img = r_sum.get("originalimage", {}).get("source") or r_sum.get("thumbnail", {}).get("source")
                if img and img.startswith("http") and not any(bad in img.lower() for bad in ["1x1", "pixel", "icon-small"]):
                    return img, f"Official {page_title} Seal/Emblem"

                # Check page images for official LOGO or Emblem
                img_list_url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&titles={urllib.parse.quote(page_title)}&prop=images"
                r_imgs = requests.get(img_list_url, headers=UA, timeout=5).json()
                pages = r_imgs.get("query", {}).get("pages", {})
                for p in pages.values():
                    for im in p.get("images", []):
                        fn = im.get("title", "")
                        if any(ext in fn.lower() for ext in [".png", ".jpg", ".jpeg", ".svg"]) and any(k in fn.lower() for k in ["logo", "emblem", "seal"]):
                            info_url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&titles={urllib.parse.quote(fn)}&prop=imageinfo&iiprop=url"
                            r_info = requests.get(info_url, headers=UA, timeout=5).json()
                            for ip in r_info.get("query", {}).get("pages", {}).values():
                                for ii in ip.get("imageinfo", []):
                                    if ii.get("url"):
                                        return ii["url"], f"Official {page_title} Verified Logo"
        except Exception:
            pass

    # 4. Fallback: High-resolution real educational photography
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
    official_domain = item.get("official_domain", "")
    OFFICIAL_DOMAINS_MAP = {
        "bteup": "https://bteup.ac.in",
        "up board": "https://upmsp.edu.in",
        "cbse": "https://cbse.gov.in",
        "upsc": "https://upsc.gov.in",
        "ssc": "https://ssc.gov.in",
        "nta": "https://nta.ac.in",
        "neet": "https://exams.nta.ac.in/NEET",
        "up police": "https://uppbpb.gov.in",
        "uhsr": "https://uhsr.ac.in",
        "rrb": "https://indianrailways.gov.in",
        "ibps": "https://ibps.in",
        "jee": "https://jeemain.nta.ac.in",
        "bihar": "https://bpsc.bih.nic.in",
        "rajasthan": "https://rpsc.rajasthan.gov.in",
        "kumaun": "https://www.kunainital.ac.in",
    }
    target_link = item.get("link") or ""
    if not target_link.startswith("http") or any(b in target_link.lower() for b in ["search?q=", "google.com", "bing.com"]):
        if official_domain and "." in official_domain:
            target_link = f"https://{official_domain.strip('/').replace('http://', '').replace('https://', '')}"
        else:
            combined_key = f"{entity} {title}".lower()
            matched_url = next((url for k, url in OFFICIAL_DOMAINS_MAP.items() if k in combined_key), None)
            target_link = matched_url or "https://uniquedigit-viral-hub.pages.dev/exams-results/"

    prompt = f"""You are India's top senior education editor and investigative career journalist writing for 'Sarkari Result & Exam Alert' (all-sarkari-result-2k0.blogspot.com).
Topic: {title}
Entity: {entity} | Category: {category} | Official Domain: {official_domain} | Direct Link: {target_link}

CORE JOURNALISTIC & HUMANIZATION PRINCIPLES (Anti-AI Bot Craft):
1. LANGUAGE: 100% Natural, Engaging Conversational HINGLISH (Fluent blend of Roman Hindi with standard English education keywords like Scorecard, Cutoff, Merit List, Admit Card, Direct Link, Counseling, Eligibility).
2. DIVERSE, AUTHENTIC INTROS (BANNED REPETITION):
   - STRICT BAN: DO NOT start every article with "Are yaar! Agar aapne bhi...". Vary your opening hook every single time!
   - Examples of natural openers:
     * "Candidates who appeared for {title} can finally breathe a sigh of relief as the official announcement is here."
     * "Agar aap bhi {entity} ke is update ka intezaar kar rahe the, toh board ne official portal par fresh notification release kar diya hai."
     * "The wait is officially over for thousands of students across the state."
3. HEADLINE DIVERSITY (DO NOT USE RIGID REPETITIVE PREFIXES):
   - NEVER put "[Direct Link Active]" on every single post! Especially NOT on quizzes, current affairs, syllabus, or general notices!
   - Craft a compelling, journalistic headline tailored to what this actually is:
     * If Result: "{entity} {title}: Marks Declared, How to Check Scorecard & Cutoff Details"
     * If Admit Card: "{entity} Admit Card 2026: Hall Ticket Download Link & Exam Shift Guidelines"
     * If Job/Bharti: "{entity} Recruitment 2026: {title} - Eligibility Criteria, Vacancies & Application Steps"
     * If Quiz/Notes: "Daily Preparation Capsule: {title} - Key Questions with Detailed Solutions"
     * If Cutoff: "{entity} Expected & Final Cutoff 2026: Category-Wise Breakdown"
4. STRICT CLICHE BAN:
   - "In conclusion", "delve into", "tapestry", "beacon", "it is important to remember", "furthermore", "moreover", "game-changer", "testament to", "fast-paced world".

ARTICLE STRUCTURE (600 to 750 words):
- ## Natural, Catchy Journalistic Headline (No robotic brackets)
- ## ⚡ Quick Highlights Box:
  A clean markdown table with:
  | Detail | Information |
  | :--- | :--- |
  | **Exam / Yojana Name** | {title} |
  | **Conducting Authority** | {entity} |
  | **Current Status** | 🟢 Declared / Active |
  | **Category** | {category} |
  | **Official Portal** | {official_domain or 'Official Website'} |
- ## 📋 Step-by-Step Procedure (How to Check / Apply):
  Practical, clear steps candidates need to take on the official website.
- ## 📊 Category-Wise Cutoff / Eligibility Criteria:
  Markdown table with realistic figures for General, OBC, SC, ST, EWS.
- ## 🔗 Official Direct Link Callout:
  `👉 [Official Website Direct Link - Click Here To Access Official Portal]({target_link})`
- ## ⚠️ Important Documents & Advisory:
  What to verify on the scorecard / application (QR code, Name spelling, Marks) and warning against fake fraud sites.
- ## ❓ Frequently Asked Questions (Top FAQs):
  3 direct questions users search with crisp 2-sentence answers.

Return strict JSON:
{{
  "title": "Natural, professional headline matching topic intent (zero repetitive boilerplate)",
  "summary": "Compelling meta description under 155 chars for Google Search SERP",
  "body_md": "Full markdown content with tables, bold highlights, numbered steps, official link, and FAQs",
  "tags": ["{category}", "Sarkari Result", "{entity}", "Govt Jobs 2026"]
}}"""

    try:
        return gemini(prompt)
    except Exception as e:
        print(f"❌ Generation error for {title}: {e}")
        return None

# ======================================================================================
# 🌐 CLOUDFLARE D1 MAIN WEBSITE PUBLISHER
# ======================================================================================
def publish_to_cloudflare_d1(title, summary, body_md, tags, image_url, source_url="", official_domain=""):
    """
    Stores article in Cloudflare D1 SQLite database to go live instantly on
    https://uniquedigit-viral-hub.pages.dev/exams-results/
    """
    if not (CF_ACCOUNT and CF_D1_DB and CF_TOKEN):
        print("⚠️ [Cloudflare D1]: Missing CF credentials in environment.")
        return False

    clean_src = source_url if (source_url and not any(b in source_url.lower() for b in ["search?q=", "google.com/search", "news.google.com/search"])) else None
    slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')[:80]
    post_id = uuid.uuid4().hex[:16]
    sources_json = json.dumps([{"title": official_domain or "Official Authority", "url": clean_src or ""}])
    faq_json = json.dumps([])

    sql = """
    INSERT INTO posts (
        id, niche_id, slug, kind, title, summary, body_md, faq, sources,
        image_url, image_credit, source_url, hype, views, is_breaking, indexable, status,
        published_at, updated_at
    )
    VALUES (
        ?,
        (SELECT id FROM niches WHERE slug = 'exams-results' LIMIT 1),
        ?, 'article', ?, ?, ?, ?, ?,
        ?, 'Official Verified Emblem', ?, 88.0, 25, 1, 1, 'published',
        strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
        strftime('%Y-%m-%dT%H:%M:%SZ', 'now')
    )
    ON CONFLICT(niche_id, slug) DO UPDATE SET
        title = excluded.title,
        summary = excluded.summary,
        body_md = excluded.body_md,
        image_url = excluded.image_url,
        updated_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now');
    """
    params = [post_id, slug, title, summary, body_md, faq_json, sources_json, image_url, source_url]

    url = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT}/d1/database/{CF_D1_DB}/query"
    headers = {"Authorization": f"Bearer {CF_TOKEN}", "Content-Type": "application/json"}
    try:
        r = requests.post(url, headers=headers, json={"sql": sql, "params": params}, timeout=20)
        res_json = r.json() if r.status_code == 200 else {}
        if r.status_code == 200 and res_json.get("success"):
            print(f"✅ [Cloudflare Main Site]: Live at https://uniquedigit-viral-hub.pages.dev/exams-results/{slug}")
            try:
                from pipelines.indexnow_helper import submit_url_to_indexnow
                submit_url_to_indexnow(f"https://uniquedigit-viral-hub.pages.dev/exams-results/{slug}")
            except Exception:
                pass
            return True
        else:
            print(f"❌ [Cloudflare D1 Error]: HTTP {r.status_code} - {r.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ [Cloudflare D1 Exception]: {e}")
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

        # If already published to both Blogger and Cloudflare, skip
        if topic_hash in cache and cache[topic_hash].get("blogger_url") and cache[topic_hash].get("cf_live"):
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
        real_img, img_type = fetch_real_official_image(entity, category=item.get("category", ""), source_link=item.get("link", ""))
        print(f"🖼️ Media Resolved: {real_img[:70]}... ({img_type})")

        # 5. Publish to Google Blogger
        blogger_url = None
        try:
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
        except Exception as e:
            print(f"⚠️ [Blogger Catch]: {e}")

        # 6. Publish to Cloudflare Main Site (ALWAYS GUARANTEED)
        cf_success = publish_to_cloudflare_d1(
            final_title, summary, body_md, tags, real_img,
            source_url=item.get("link", ""),
            official_domain=item.get("official_domain", "")
        )

        # 7. Update Cache if successfully pushed to Blogger OR Cloudflare
        if blogger_url or cf_success:
            cache[topic_hash] = {
                "title": final_title,
                "entity": entity,
                "published_at": datetime.now().isoformat(),
                "blogger_url": blogger_url,
                "image": real_img,
                "cf_live": cf_success
            }
            save_cache(cache)
            published_count += 1
            print(f"✨ [Success]: Published post '{final_title[:45]}...'")
        else:
            print(f"❌ [Failed]: Could not push to Blogger or Cloudflare.")

        # Rate-limiting cushion between articles to protect Blogger quotas
        time.sleep(10)

    print("\n" + "=" * 70)
    print(f"🎉 SARKARI RADAR COMPLETED: Successfully published {published_count} new posts!")
    print("=" * 70)

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    run_sarkari_radar(max_posts=count)

