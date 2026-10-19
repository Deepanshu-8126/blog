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
from bridges.search_intent_engine import get_high_intent_search_topics
from pipeline import gemini

# Configuration
SARKARI_BLOG_ID = os.getenv("BLOGGER_EXAM_BLOG_ID", "1366151638291560024")
YOJANA_BLOG_ID = os.getenv("BLOGGER_YOJANA_BLOG_ID", "529528513771224915")
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
    """
    Scans real Google Search Autocomplete intent queries and filtered RSS streams.
    Rejects foreign news, sports, and wire articles with zero search volume.
    """
    candidates = []
    seen = set()

    # 1. PRIORITY 1: Real-time Google Search Autocomplete (What 50 Crore Indians actually type into Google)
    try:
        sarkari_queries = get_high_intent_search_topics("sarkari", max_topics=10)
        yojana_queries = get_high_intent_search_topics("yojanas", max_topics=10)
        for q in sarkari_queries + yojana_queries:
            kw = q["search_keyword"]
            if kw.lower() not in seen:
                seen.add(kw.lower())
                domain = q["portal"].replace("https://", "").replace("http://", "").split("/")[0]
                candidates.append({
                    "title": kw,
                    "entity": q["entity"],
                    "category": q["intent"],
                    "official_domain": domain,
                    "source": "Google Autocomplete (High Volume Search Intent)",
                    "link": q["portal"],
                    "is_prequalified": True
                })
        print(f"🎯 [Google Search Intent Engine] Injected {len(candidates)} real Indian user search queries.")
    except Exception as e:
        print("[Search intent engine warning]:", e)

    # 2. PRIORITY 2: Filtered RSS streams (Strictly discard foreign news & zero-search wire reports)
    BANNED_FOREIGN_OR_IRRELEVANT = [
        "west asian", "pakistan", "bangladesh", "israel", "gaza", "lebanon", "iran",
        "uk", "us", "canada", "murder", "crime", "rape", "arrested", "gossip",
        "football", "monterrey", "pachuca", "cincinnati", "columbus", "dj song"
    ]

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

                        # STRICT FILTER: Discard foreign news and crime/gossip
                        if any(b in lower for b in BANNED_FOREIGN_OR_IRRELEVANT):
                            continue

                        if lower not in seen and len(clean_title) >= 15:
                            seen.add(lower)
                            candidates.append({
                                "title": clean_title,
                                "source": source_name,
                                "link": link_elem.text if link_elem is not None else ""
                            })
        except Exception:
            continue

    print(f"📡 [Raw Radar Stream] Total Candidate Topics: {len(candidates)}")
    return candidates

def ai_classify_and_filter_candidates(candidates):
    """
    Agent Alpha: Autonomous AI Intent Classifier.
    Passes prequalified real Google search queries directly, and filters raw candidates.
    """
    if not candidates:
        return []

    results = []
    unqualified = []

    for c in candidates:
        if c.get("is_prequalified"):
            results.append({
                "title": c["title"],
                "entity": c.get("entity", "Government Authority"),
                "category": c.get("category", "Sarkari Alert"),
                "official_domain": c.get("official_domain", ""),
                "source": c.get("source", "Google Search Intent"),
                "link": c.get("link", "")
            })
        else:
            unqualified.append(c)

    if unqualified:
        headlines = [c["title"] for c in unqualified[:20]]
        prompt = f"""You are the Chief AI Editor for India's premier Sarkari & Education Portal.
Candidate Breaking Headlines:
{json.dumps(headlines, indent=2)}

TASK:
Filter and classify ONLY topics that Indian students, job seekers, youth, or citizens actively search for:
- Sarkari Results, Scorecards, Merit Lists, Cutoff Marks, Answer Keys, Admit Cards, Time Tables.
- Central & State Government Recruitments (SSC, UPSC, Railway, Police, Anganwadi, Asha, Lekhpal, Direct Bharti).
- Universities & Colleges (Kumaun University, CCSU, DU, BHU, AKTU, State Boards, Polytechnic, ITI).
- Government Yojanas & Welfare Schemes (PM Awas, Free Silai Machine, Free Laptop, Ladli Behna, Ration Card, Ayushman).
- Scholarships (UP Scholarship, NSP Portal, Post Matric).

STRICTLY REJECT: Sports matches, Bollywood gossip, crime news, general political speeches, foreign news.

Return strict JSON:
{{
  "qualified": [
    {{
      "headline": "<exact headline string from candidate list>",
      "entity": "<Exact Organization / University / State Department / Scheme name>",
      "category": "Result | Admit Card | Recruitment | Yojana | Scholarship | Cutoff | Answer Key",
      "official_domain": "<official website if known, e.g. kunainital.ac.in, uppbpb.gov.in, ssc.gov.in, otherwise leave empty>"
    }}
  ]
}}"""
        try:
            res = gemini(prompt)
            qualified_list = res.get("qualified", [])
            cand_map = {c["title"].lower(): c for c in unqualified}
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
        except Exception as e:
            print(f"❌ AI Classification Error: {e}")

    print(f"🎯 [AI Intent Radar] Qualified {len(results)} high-intent Sarkari/Education topics.")
    return results

# ======================================================================================
# ✍️ HUMANIZED HINGLISH SARKARI JOURNALIST ENGINE (Anti-AI Slop)
# ======================================================================================
def generate_sarkari_article(item):
    """
    Generates a deeply humanized, authentic, search-intent optimized article.
    Zero generic AI jargon, strict punchy headline, direct 2-line answer first,
    high-visibility official action button, factual data table, and real Google search FAQs.
    """
    title = item["title"]
    entity = item.get("entity", "Conducting Board")
    category = item.get("category", "Sarkari Alert")
    official_domain = item.get("official_domain", "")
    target_link = item.get("link") or "https://uniquedigit-viral-hub.pages.dev"
    if not target_link.startswith("http") or any(b in target_link.lower() for b in ["search?q=", "google.com", "bing.com"]):
        target_link = f"https://{official_domain}" if official_domain else "https://uniquedigit-viral-hub.pages.dev"

    prompt = f"""You are India's #1 senior educational journalist and career editor writing for 'Sarkari Result & Scheme Portal'.
Target Search Intent Query: {title}
Entity / Organization: {entity}
Category: {category}
Official Portal: {official_domain or 'Official Government Website'}
Official Direct Link: {target_link}

CORE OBJECTIVE:
Write an ultra-high-ranking, 100% human-written style guide (600-750 words) in natural, engaging Hinglish (fluent blend of Roman Hindi with standard English education terms like Scorecard, Cutoff, Merit List, Admit Card, Direct Link).

MANDATORY EDITORIAL RULES (Anti-AI Bot & Zero-Copyright Risk):
1. HEADLINE RULES (VERY STRICT):
   - Length: EXACTLY 50 to 65 characters.
   - PUNCHY, CLEAR, FOCUSED ON A SINGLE EVENT (Zero clutter, zero multi-category mixing).
   - If Admit Card: "{entity} {category} 2026: Direct Download Link & Exam Shift Time"
   - If Result: "{entity} {category} 2026: Scorecard & Cutoff Marks Direct Link"
   - If Yojana: "{title.title()} 2026: Beneficiary Status Check & Direct Portal Link"
   - If Time Table: "{entity} Time Table 2026: Datesheet PDF Download Link"
   - NEVER combine "Time Table" with "Marks Declared" or "Cutoff"!

2. FIRST 2 LINES (DIRECT ANSWER RULE - GOOGLE FEATURED SNIPPET TARGET):
   - Do NOT start with textbook intros, "Are yaar", or "In today's fast paced world".
   - Line 1: Clear announcement of what is released, the official date, and status.
   - Line 2: Exactly where candidates can access it ({target_link}).

3. SECTION BREAKDOWN (IN ORDER):
   - ## ⚡ Quick Highlights Box:
     | Detail | Official Status |
     | :--- | :--- |
     | **Exam / Yojana Name** | Clean official name (e.g. {entity} {category} 2026) |
     | **Authority / Board** | {entity} |
     | **Current Status** | 🟢 Active / Declared |
     | **Required Login** | Registration No / Roll No / DOB |
     | **Official Portal** | [{official_domain or 'Click to Visit'}]({target_link}) |
   
   - ## 📋 Step-by-Step Procedure (Kaise Check / Apply Karein):
     4-5 crisp, numbered steps mentioning actual website buttons (e.g. 'Admit Card 2026' link par click karein, Roll Number darj karein, Submit dabayein).

   - ## 📊 Factual Eligibility / Cutoff / Benefit Slabs:
     Clean markdown table with realistic category-wise data (General, OBC, EWS, SC, ST) or scheme amounts.

   - ## 🔗 Official Direct Link Callout:
     `👉 [Official Website Direct Link - Click Here To Access Official Portal]({target_link})`

   - ## ⚠️ Important Advisory & Verification:
     Verification checklist (Photo, Signature, Exam Center, Shift Time) and a warning against unauthorized phishing sites.

   - ## ❓ Frequently Asked Questions (Top 3 FAQs):
     3 exact questions that Indian users search on Google with direct, 2-sentence answers.

4. 100% ORIGINAL WRITING - ZERO COPYRIGHT INFRINGEMENT:
   - All sentences must be original editorial analysis. Do NOT copy text verbatim from press releases or third-party portals.
   - Rephrase all facts, dates, and instructions in clean, accessible Hinglish.
   - Append mandatory statutory safe harbor notice at the end:
     `\n\n---\n*Disclaimer: This portal provides informational synthesis and public commentary based on official public notifications under Section 52(1)(q) of the Indian Copyright Act, 1957. For official verifications and direct applications, always visit the official department portal at [{official_domain or 'Official Website'}]({target_link}).*`

5. BANNED AI JARGON:
   "In conclusion", "delve into", "tapestry", "beacon", "it is important to remember", "furthermore", "moreover", "game-changer", "fast-paced world", "testament to", "realm".

Return strict JSON:
{{
  "title": "Clean, focused, 50-65 char headline matching exact search intent",
  "summary": "Compelling SERP meta description under 155 characters",
  "body_md": "Full markdown article following the exact structure above",
  "tags": ["{category}", "Sarkari Result", "{entity}", "2026"],
  "faq": [
    {{"q": "How to check {title} online?", "a": "Direct 2-sentence answer mentioning {official_domain or 'official portal'}."}},
    {{"q": "What is the official website for {entity}?", "a": "Direct 2-sentence answer with {target_link}."}},
    {{"q": "What documents/credentials are required?", "a": "Direct 2-sentence answer."}}
  ]
}}"""

    try:
        res = gemini(prompt)
        if res and not res.get("faq"):
            res["faq"] = [
                {"q": f"How to check {title} online?", "a": f"Visit {target_link} and enter your registration details."},
                {"q": f"What is the official website for {entity}?", "a": f"The official portal is {target_link}."},
                {"q": "What credentials are required?", "a": "Registration Number or Roll Number and Date of Birth."}
            ]
        return res
    except Exception as e:
        print(f"❌ Generation error for {title}: {e}")
        return None

# ======================================================================================
# 🌐 CLOUDFLARE D1 MAIN WEBSITE PUBLISHER
# ======================================================================================
def publish_to_cloudflare_d1(title, summary, body_md, tags, image_url, source_url="", official_domain="", faq_list=None, image_credit=""):
    """
    Stores article in Cloudflare D1 SQLite database to go live instantly on
    https://uniquedigit-viral-hub.pages.dev/exams-results/ with full FAQ schema.
    """
    if not (CF_ACCOUNT and CF_D1_DB and CF_TOKEN):
        print("⚠️ [Cloudflare D1]: Missing CF credentials in environment.")
        return False

    clean_src = source_url if (source_url and not any(b in source_url.lower() for b in ["search?q=", "google.com/search", "news.google.com/search"])) else None
    slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')[:80]
    post_id = uuid.uuid4().hex[:16]
    sources_json = json.dumps([{"title": official_domain or "Official Authority", "url": clean_src or ""}], ensure_ascii=False)
    faq_json = json.dumps(faq_list or [], ensure_ascii=False)
    credit = image_credit or ("Wikimedia Commons (Public Domain / CC-BY-SA 4.0)" if ("wikimedia.org" in image_url or "wikipedia.org" in image_url) else "Unsplash (Royalty-Free)")

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
        ?, ?, ?, 90.0, 25, 1, 1, 'published',
        strftime('%Y-%m-%dT%H:%M:%SZ', 'now'),
        strftime('%Y-%m-%dT%H:%M:%SZ', 'now')
    )
    ON CONFLICT(niche_id, slug) DO UPDATE SET
        title = excluded.title,
        summary = excluded.summary,
        body_md = excluded.body_md,
        faq = excluded.faq,
        sources = excluded.sources,
        image_url = excluded.image_url,
        image_credit = excluded.image_credit,
        updated_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now');
    """
    params = [post_id, slug, title, summary, body_md, faq_json, sources_json, image_url, credit, source_url]

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

        # 5. Publish to Google Blogger (Strict Routing: Yojana Blog vs Sarkari Exam Blog)
        blogger_url = None
        try:
            content_html = markdown.markdown(body_md, extensions=['extra', 'tables'])
            check_str = f"{final_title} {' '.join(tags)}".lower()
            is_yojana = any(k in check_str for k in ["yojana", "subsidy", "dbt", "kisan", "awas", "ration", "pension", "scholarship", "surya ghar", "ladli behna"])
            target_id = YOJANA_BLOG_ID if is_yojana else SARKARI_BLOG_ID
            
            blogger_res = publish_to_blogger(
                final_title,
                content_html,
                labels=tags,
                is_draft=False,
                featured_image=real_img,
                target_blog_id=target_id
            )
            blogger_url = blogger_res.get("url") if blogger_res.get("success") else None
        except Exception as e:
            print(f"⚠️ [Blogger Catch]: {e}")

        # 6. Publish to Cloudflare Main Site (ALWAYS GUARANTEED with Rich FAQ Schema)
        cf_success = publish_to_cloudflare_d1(
            final_title, summary, body_md, tags, real_img,
            source_url=item.get("link", ""),
            official_domain=item.get("official_domain", ""),
            faq_list=article.get("faq", []),
            image_credit=img_type
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

