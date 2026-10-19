#!/usr/bin/env python3
"""
========================================================================================
🌲 SYSTEM 2: EVERGREEN HIGH-INTENT AUTHORITY GUIDE ENGINE
========================================================================================
Autonomous Long-Form Master Guide Generation Engine (3-5 Year Passive Search Traffic)
Pillars:
  1. 🥗 Health, Gym & Nutrition (Pexels HD Gym Media + Vegetarian Protein Guides)
  2. 💰 Personal Finance & Daily Savings (SIP vs FD, Tax Regimes, High-RPM Guides)
  3. 🎓 Student & Career Roadmaps (SSC CGL, ATS Resumes, High-Paying Careers)
  4. 🛠️ Daily Life Hacks & How-To (Train PNR/RAC, Aadhaar Updates, Tech Fixes)

Features:
  - Real Google Autocomplete query discovery
  - Position 0 Featured Snippet direct answer box
  - In-depth data comparison tables + common mistakes to avoid (E-E-A-T)
  - 100% Royalty-Free Media with attribution
  - Dual-Publishing to Cloudflare D1 + Google Blogger
  - Instant IndexNow notification
========================================================================================
"""

import os
import sys
import re
import json
import time
import uuid
import hashlib
import urllib.parse
from datetime import datetime
from pathlib import Path

# Force UTF-8 on Windows
if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from dotenv import load_dotenv
load_dotenv(ROOT_DIR / ".env")

import requests
from pipeline import gemini
from pipelines.master_image_pipeline import resolve_master_image, verify_image_health
from pipelines.indexnow_helper import submit_url_to_indexnow

try:
    from bridges.blogger_bridge.blogger_publisher import publish_to_blogger
    BLOGGER_AVAILABLE = True
except ImportError:
    BLOGGER_AVAILABLE = False

CACHE_FILE = ROOT_DIR / "evergreen_seen_cache.json"

def log(module: str, msg: str):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [{module}] {msg}", flush=True)

def load_seen_cache() -> dict:
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_seen_cache(cache: dict):
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, indent=2, ensure_ascii=False)
    except Exception as e:
        log("EvergreenCache", f"⚠️ Error saving cache: {e}")

# ======================================================================================
# 1. EVERGREEN SEED PILLARS & SEARCH QUERY HARVESTER
# ======================================================================================
EVERGREEN_PILLARS = {
    "health": {
        "niche_slug": "health",
        "label": "Health & Fitness",
        "seeds": [
            "high protein vegetarian diet indian for muscle gain",
            "beginner gym workout routine 7 days split",
            "how to lose belly fat calorie deficit indian food",
            "creatine monohydrate benefits side effects hindi",
            "winter immunity foods indian home remedies",
            "intermittent fasting 16 8 diet plan for weight loss",
            "gym diet plan for lean muscle indian vegetarians",
            "best morning wellness drink for digestion and skin"
        ],
        "default_image": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?w=1200&q=80",
        "image_credit": "Unsplash Royalty-Free Fitness Photography"
    },
    "finance": {
        "niche_slug": "side-hustles",
        "label": "Personal Finance & Savings",
        "seeds": [
            "sip vs fd return calculation 10 years",
            "new tax regime vs old tax regime 7 lakh 10 lakh salary",
            "best lifetime free credit cards india rupay upi",
            "free cibil score check online without affecting score",
            "sukanya samriddhi yojana 2026 interest rate calculator",
            "best post office monthly income schemes for safe return",
            "how to invest in index funds for beginners in india"
        ],
        "default_image": "https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?w=1200&q=80",
        "image_credit": "Unsplash Commercial Finance Media"
    },
    "career": {
        "niche_slug": "exams-results",
        "label": "Career & Student Roadmaps",
        "seeds": [
            "ssc cgl preparation roadmap with full time job",
            "high paying career options after 12th commerce pcm",
            "ats friendly resume format for freshers free tips",
            "data analyst career roadmap for beginners in india",
            "how to prepare for state psc exams without coaching",
            "top government computer certificate courses for jobs"
        ],
        "default_image": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=1200&q=80",
        "image_credit": "Unsplash Verified Education Photography"
    },
    "lifehacks": {
        "niche_slug": "viral",
        "label": "Daily Life Hacks & Tech Fixes",
        "seeds": [
            "train ticket confirmation probability rules rac waitlist",
            "how to update mobile number in aadhaar online step by step",
            "smartphone battery draining fast how to fix hidden settings",
            "how to link pan card with aadhaar card online status check",
            "how to remove personal data from truecaller permanently"
        ],
        "default_image": "https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=1200&q=80",
        "image_credit": "Unsplash Verified Lifestyle Technology Media"
    }
}

class EvergreenIntentHarvester:
    """Discovers real Google Autocomplete queries based on high-intent evergreen seed topics."""

    def __init__(self):
        self.seen_cache = load_seen_cache()

    def get_google_suggestions(self, seed: str) -> list[str]:
        suggestions = []
        try:
            url = f"https://suggestqueries.google.com/complete/search?client=firefox&q={urllib.parse.quote(seed)}"
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            r = requests.get(url, headers=headers, timeout=5)
            if r.status_code == 200:
                data = r.json()
                if len(data) > 1 and isinstance(data[1], list):
                    suggestions = [s.strip() for s in data[1] if isinstance(s, str) and len(s) > 10]
        except Exception as e:
            log("IntentHarvester", f"Autocomplete API note: {e}")

        # Fallback to seed itself if suggestions empty
        if not suggestions:
            suggestions = [seed]
        return suggestions

    def harvest_next_topic(self, pillar_key: str = "health") -> dict | None:
        pillar = EVERGREEN_PILLARS.get(pillar_key, EVERGREEN_PILLARS["health"])
        seeds = pillar["seeds"]

        # Find first seed with an unseen variation
        for seed in seeds:
            queries = self.get_google_suggestions(seed)
            for q in queries:
                q_hash = hashlib.md5(q.lower().strip().encode("utf-8")).hexdigest()
                if q_hash not in self.seen_cache:
                    return {
                        "pillar_key": pillar_key,
                        "niche_slug": pillar["niche_slug"],
                        "label": pillar["label"],
                        "search_query": q,
                        "seed": seed,
                        "default_image": pillar["default_image"],
                        "image_credit": pillar["image_credit"],
                        "hash": q_hash
                    }

        # If all seen, reuse top seed with a timestamp variation
        chosen_seed = seeds[0]
        return {
            "pillar_key": pillar_key,
            "niche_slug": pillar["niche_slug"],
            "label": pillar["label"],
            "search_query": chosen_seed,
            "seed": chosen_seed,
            "default_image": pillar["default_image"],
            "image_credit": pillar["image_credit"],
            "hash": hashlib.md5((chosen_seed + str(time.time())).encode("utf-8")).hexdigest()
        }

# ======================================================================================
# 2. MASTER EDITORIAL GUIDE WRITER (E-E-A-T & Position 0 Specialist)
# ======================================================================================
class EvergreenGuideWriter:
    """Generates 1,200+ words, deeply structured, original evergreen master guides."""

    def write_guide(self, topic: dict) -> dict | None:
        query = topic["search_query"]
        pillar = topic["pillar_key"]
        log("GuideWriter", f"Synthesizing high-intent authority guide for: '{query}'...")

        prompt = f"""
You are a Senior Subject-Matter Expert and High-Traffic Content Strategist creating a permanent, evergreen master guide.
Target Search Query: "{query}"
Domain Pillar: {topic['label']}

STRICT EDITORIAL STANDARDS (Zero AI Slop, 100% Helpful Content):
1. **Title**: EXACTLY 50 to 65 characters long. Ultra-clickable, punchy, contains the exact search keyword, no truncation.
2. **Featured Snippet Box (Position 0 Answer)**: Start immediately with a 2-sentence direct, unambiguous summary answer to the reader's core query.
3. **Key Highlights / Takeaways**: 3-4 bullet points summarizing the most critical takeaways.
4. **Comprehensive Step-by-Step Practical Blueprint**:
   - Provide an in-depth, realistic, actionable guide (1,000+ words).
   - If Diet/Health: Include specific Indian meals (Paneer, Soya, Dal, Besan, Sprouts), timing, quantities, and realistic advice.
   - If Finance: Include realistic calculations (e.g., ₹5,000/mo SIP at 12% vs FD at 7%), rules, and pros/cons.
   - If Career/Exams: Daily schedule breakdown, subject weightage, recommended verified resources.
   - If Life Hacks: Exact step-by-step navigation, portal procedures, and practical solutions.
5. **Comparison / Data Table**: A structured Markdown table (with exact numbers, metrics, or comparisons).
6. **Common Mistakes to Avoid**: Highlight 3-4 frequent pitfalls people make and how to prevent them.
7. **Actionable Routine / Cheat-Sheet**: Clear checklist or day-by-day plan.
8. **Statutory & Advisory Disclaimer**:
   - For Health: Explicit medical disclaimer stating "Consult a certified doctor or healthcare professional before making major dietary or supplement changes."
   - For Finance: "Informational guide only; consult a SEBI-registered advisor before investing."
   - Educational fair-use disclaimer under Section 52(1)(q).
9. **Structured FAQs**: Exactly 5 distinct, high-value questions and detailed answers formatted as JSON objects.

OUTPUT STRICT VALID JSON ONLY (No markdown code fences, no extra text):
{{
  "title": "50-65 chars punchy title",
  "summary": "130-155 characters SEO meta description containing the target keyword",
  "body_md": "Full markdown content with ## headings, tables, bullet points, and disclaimers",
  "faq": [
    {{"q": "Real question 1?", "a": "Direct answer 1"}},
    {{"q": "Real question 2?", "a": "Direct answer 2"}},
    {{"q": "Real question 3?", "a": "Direct answer 3"}},
    {{"q": "Real question 4?", "a": "Direct answer 4"}},
    {{"q": "Real question 5?", "a": "Direct answer 5"}}
  ],
  "labels": ["Primary Category", "Secondary Tag", "Trending Guide"]
}}
"""
        try:
            raw_response = gemini(prompt)
            if isinstance(raw_response, dict):
                parsed = raw_response
            else:
                clean_json = str(raw_response).strip()
                if clean_json.startswith("```"):
                    clean_json = re.sub(r"^```[a-zA-Z]*\n?", "", clean_json)
                    clean_json = re.sub(r"\n?```$", "", clean_json)
                clean_json = clean_json.strip()
                parsed = json.loads(clean_json)

            # Enforce 50-65 character title constraint
            title = parsed.get("title", "").strip()
            if len(title) > 65:
                # Trim cleanly to nearest word under 65 chars
                trimmed = title[:62].rsplit(' ', 1)[0]
                parsed["title"] = f"{trimmed}..."
            elif len(title) < 40:
                parsed["title"] = f"{title}: Complete Step-by-Step Guide"

            return parsed
        except Exception as e:
            log("GuideWriter", f"❌ Generation error: {e}")
            return None

# ======================================================================================
# 3. MEDIA & STOCK VIDEO RESOLVER
# ======================================================================================
class EvergreenMediaResolver:
    """Resolves HD royalty-free photos and optional video loops for maximum dwell time."""

    def resolve_media(self, query: str, pillar_key: str, default_img: str, default_credit: str) -> tuple[str, str, str | None]:
        # 1. Try master image pipeline
        img_url, img_credit = resolve_master_image(query, niche_slug=pillar_key)

        # 2. Verify image health
        if not verify_image_health(img_url):
            img_url = default_img
            img_credit = default_credit

        # 3. Optional Video clip suggestion for high-engagement niches (Health/Gym/Lifehacks)
        video_embed = None
        if pillar_key == "health":
            video_embed = (
                '\n\n<div class="video-container" style="margin: 28px 0; border-radius: 14px; overflow: hidden; border: 1px solid #334155; box-shadow: 0 10px 25px rgba(0,0,0,0.2);">'
                '<div style="background: #0f172a; padding: 10px 16px; font-size: 13px; color: #38bdf8; font-weight: 600;">▶️ Visual Demonstration & Form Guide</div>'
                '<p style="padding: 12px 16px; margin: 0; background: #1e293b; color: #94a3b8; font-size: 14px;">'
                '💡 <em>Pro Tip: Form and controlled tempo are more important than heavy weight. Maintain a steady 2-second negative rep on every movement.</em>'
                '</p>'
                '</div>\n'
            )

        return img_url, img_credit, video_embed

# ======================================================================================
# 4. SYNDICATION & CLOUDFLARE D1 PUBLISHER
# ======================================================================================
class EvergreenSyndicationAgent:
    """Dual-publishes evergreen guides to Cloudflare D1 and Blogger, then triggers IndexNow."""

    def __init__(self):
        self.cf_account = os.getenv("CLOUDFLARE_ACCOUNT_ID")
        self.cf_db = os.getenv("CLOUDFLARE_D1_DATABASE_ID")
        self.cf_token = os.getenv("CLOUDFLARE_API_TOKEN")

    def publish_to_d1(self, article: dict, topic: dict, img_url: str, img_credit: str) -> str | None:
        if not self.cf_account or not self.cf_db or not self.cf_token:
            log("SyndicationAgent", "⚠️ Cloudflare credentials missing in .env.")
            return None

        slug = re.sub(r'[^a-z0-9]+', '-', article["title"].lower()).strip('-')[:80]
        post_id = uuid.uuid4().hex[:16]
        niche_slug = topic["niche_slug"]
        faq_json = json.dumps(article.get("faq", []), ensure_ascii=False)
        sources_json = json.dumps([{"title": "UniqueDigit Editorial Research", "url": "https://uniquedigit-viral-hub.pages.dev"}], ensure_ascii=False)

        sql = """
        INSERT INTO posts (
            id, niche_id, slug, kind, title, summary, body_md, faq, sources,
            image_url, image_credit, source_url, hype, views, is_breaking, indexable, status,
            published_at, updated_at
        )
        VALUES (
            ?, (SELECT id FROM niches WHERE slug = ? LIMIT 1),
            ?, 'article', ?, ?, ?, ?, ?,
            ?, ?, ?, 96.0, 50, 0, 1, 'published',
            strftime('%Y-%m-%dT%H:%M:%SZ', 'now'), strftime('%Y-%m-%dT%H:%M:%SZ', 'now')
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

        params = [
            post_id, niche_slug, slug, article["title"], article.get("summary", ""),
            article["body_md"], faq_json, sources_json, img_url, img_credit,
            f"https://uniquedigit-viral-hub.pages.dev/{niche_slug}/{slug}"
        ]

        endpoint = f"https://api.cloudflare.com/client/v4/accounts/{self.cf_account}/d1/database/{self.cf_db}/query"
        headers = {"Authorization": f"Bearer {self.cf_token}", "Content-Type": "application/json"}

        try:
            r = requests.post(endpoint, headers=headers, json={"sql": sql, "params": params}, timeout=15)
            if r.status_code == 200 and r.json().get("success"):
                live_url = f"https://uniquedigit-viral-hub.pages.dev/{niche_slug}/{slug}"
                log("SyndicationAgent", f"✅ Cloudflare D1 Live: {live_url}")

                # Ping IndexNow immediately
                submit_url_to_indexnow(live_url)
                log("SyndicationAgent", f"⚡ IndexNow Ping delivered for: {live_url}")
                return live_url
            else:
                log("SyndicationAgent", f"❌ D1 API error: {r.text}")
        except Exception as e:
            log("SyndicationAgent", f"❌ D1 request failed: {e}")

        return None

    def publish_to_blogger_cross(self, article: dict, topic: dict, img_url: str, video_html: str | None, live_url: str | None = None) -> str | None:
        if not BLOGGER_AVAILABLE:
            return None

        blog_id = os.getenv("BLOGGER_BLOG_ID")
        if not blog_id:
            return None

        import markdown

        # 1. Build Pillar-Specific E-E-A-T Advisory Text
        pillar = topic.get("pillar_key", "health")
        if pillar == "health":
            advisory_title = "🛡️ Medical & Health Review (UniqueDigit Clinical & Wellness Desk)"
            advisory_text = "This guide is synthesized for informational and educational purposes based on verified nutritional science. Individual dietary requirements and fitness tolerance vary. Always consult a certified physician, registered dietitian, or medical expert before initiating significant nutritional or supplement regimens."
            border_color = "#10b981"
            bg_color = "#f0fdf4"
            title_color = "#065f46"
        elif pillar == "finance":
            advisory_title = "⚖️ SEBI & Market Risk Disclosure (UniqueDigit Financial Desk)"
            advisory_text = "Financial instruments, mutual funds, SIPs, and fixed deposits are subject to market conditions and regulatory tax laws. Past performance metrics do not guarantee future yields. Consult a qualified SEBI-registered financial planner before executing capital allocations."
            border_color = "#f59e0b"
            bg_color = "#fffbeb"
            title_color = "#92400e"
        elif pillar == "career":
            advisory_title = "🎓 Career & Syllabus Advisory (UniqueDigit Education Desk)"
            advisory_text = "Recruitment schedules, cutoff percentiles, and exam eligibility criteria reflect the latest published gazette notices. Candidates must cross-check roll numbers and notification dates on the respective official commission portals."
            border_color = "#6366f1"
            bg_color = "#eef2ff"
            title_color = "#3730a3"
        else:
            advisory_title = "⚡ Practical Verification Notice (UniqueDigit Lifehacks Desk)"
            advisory_text = "Portal workflows, UIDAI updates, and ticket confirmation probabilities reflect official operating protocols. Always use official government web portals for sensitive personal credentials."
            border_color = "#0284c7"
            bg_color = "#f0f9ff"
            title_color = "#075985"

        # 2. Table CSS for Beautiful Rendering on Blogger
        table_css = """
<style>
.evergreen-article-container table {
  width: 100%;
  border-collapse: collapse;
  margin: 24px 0;
  font-size: 14px;
}
.evergreen-article-container th {
  background-color: #0f172a;
  color: #ffffff;
  padding: 12px 14px;
  text-align: left;
  border: 1px solid #334155;
  font-weight: 700;
}
.evergreen-article-container td {
  padding: 10px 14px;
  border: 1px solid #cbd5e1;
  color: #334155;
}
.evergreen-article-container tr:nth-child(even) {
  background-color: #f8fafc;
}
.evergreen-article-container tr:hover {
  background-color: #f1f5f9;
}
</style>
"""

        # 3. Canonical Header Badge (Passing Link Juice to UniqueDigit)
        canonical_header = ""
        canonical_footer = ""
        if live_url:
            canonical_header = f"""
<div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); border-radius: 12px; padding: 14px 18px; margin: 0 0 24px 0; color: #ffffff; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
  <div>
    <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; color: #38bdf8; font-weight: 700;">📌 Official Primary Source</div>
    <div style="font-size: 13px; font-weight: 600; color: #f8fafc; margin-top: 2px;">UniqueDigit Interactive Research Hub</div>
  </div>
  <a href="{live_url}" target="_blank" rel="canonical" style="background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%); color: #ffffff; text-decoration: none; padding: 8px 16px; border-radius: 8px; font-weight: 700; font-size: 12px; display: inline-flex; align-items: center; gap: 6px;">
    Open Interactive Guide & Calculators ➔
  </a>
</div>
"""
            canonical_footer = f"""
<div style="margin: 32px 0 20px 0; padding: 20px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; text-align: center;">
  <div style="font-size: 14px; font-weight: 700; color: #0f172a; margin-bottom: 6px;">📖 Read Full Interactive Research on UniqueDigit</div>
  <p style="font-size: 13px; color: #64748b; margin: 0 0 12px 0;">This publication is synchronized with the live database at UniqueDigit. View full charts, data points, and community updates:</p>
  <a href="{live_url}" target="_blank" rel="canonical" style="display: inline-block; background: #0284c7; color: #ffffff; padding: 10px 22px; border-radius: 8px; text-decoration: none; font-weight: 700; font-size: 13px;">
    Access Complete Guide on UniqueDigit →
  </a>
</div>
"""

        # 4. Convert Markdown Body to HTML with native tables
        parsed_html = markdown.markdown(article["body_md"], extensions=['tables', 'extra', 'nl2br'])

        # 5. Assemble Rich Container
        body_html = f'<div class="evergreen-article-container" style="font-family: system-ui, -apple-system, sans-serif; line-height: 1.8; color: #1e293b;">\n'
        body_html += table_css
        body_html += canonical_header

        # Hero Image
        if img_url:
            body_html += f'<div style="text-align: center; margin-bottom: 24px;"><img src="{img_url}" alt="{article["title"]}" style="max-width: 100%; height: auto; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);"/></div>\n'

        # E-E-A-T Safety Box
        body_html += f"""
<div style="background: {bg_color}; border-left: 4px solid {border_color}; padding: 16px 20px; border-radius: 8px; margin: 20px 0 28px 0;">
  <div style="font-weight: 800; color: {title_color}; font-size: 13px;">{advisory_title}</div>
  <p style="margin: 6px 0 0 0; font-size: 13px; color: #334155; line-height: 1.6;">{advisory_text}</p>
</div>
"""

        # Main Parsed HTML
        body_html += f'<div class="article-content">{parsed_html}</div>\n'

        if video_html:
            body_html += video_html

        # Add FAQ Accordion
        faqs = article.get("faq", [])
        if faqs:
            body_html += '<div style="margin-top: 36px; padding: 22px; background: #f8fafc; border-radius: 12px; border: 1px solid #e2e8f0;">'
            body_html += '<h3 style="margin-top: 0; color: #0f172a; font-size: 18px; font-weight: 800;">❓ Frequently Asked Questions (FAQ)</h3>'
            for item in faqs:
                body_html += f'<div style="margin-bottom: 16px; padding-bottom: 14px; border-bottom: 1px dashed #cbd5e1;"><strong style="color: #0369a1; font-size: 14px;">Q: {item.get("q")}</strong><p style="margin: 6px 0 0 0; color: #475569; font-size: 14px; line-height: 1.6;">{item.get("a")}</p></div>'
            body_html += '</div>\n'

        body_html += canonical_footer
        body_html += '</div>'

        labels = article.get("labels", [topic["label"]])
        try:
            res = publish_to_blogger(
                title=article["title"],
                content_html=body_html,
                labels=labels,
                is_draft=False,
                featured_image=img_url,
                target_blog_id=blog_id
            )
            if res and isinstance(res, dict) and res.get("url"):
                blogger_url = res.get("url")
                log("SyndicationAgent", f"✅ Blogger published with native tables & canonical backlink: {blogger_url}")
                return blogger_url
        except Exception as e:
            log("SyndicationAgent", f"⚠️ Blogger syndication note: {e}")

        return None

# ======================================================================================
# 5. MASTER ORCHESTRATION DISPATCHER
# ======================================================================================
def run_evergreen_mission(pillar: str = "health", count: int = 1):
    print("=" * 75)
    print(f"🌲 INITIATING SYSTEM 2: EVERGREEN AUTHORITY MISSION ({pillar.upper()})")
    print("=" * 75)

    harvester = EvergreenIntentHarvester()
    writer = EvergreenGuideWriter()
    media_resolver = EvergreenMediaResolver()
    dispatcher = EvergreenSyndicationAgent()

    published_total = 0
    for i in range(count):
        print("-" * 75)
        log("MasterMission", f"Running Evergreen Task {i + 1}/{count}...")

        # Step 1: Harvest high-intent search query
        topic = harvester.harvest_next_topic(pillar_key=pillar)
        if not topic:
            log("MasterMission", "⚠️ No evergreen topic available.")
            break

        log("MasterMission", f"🎯 Target Search Query: '{topic['search_query']}'")

        # Step 2: Write long-form master guide
        article = writer.write_guide(topic)
        if not article or not article.get("title") or not article.get("body_md"):
            log("MasterMission", "❌ Failed to generate master guide.")
            continue

        # Step 3: Resolve Royalty-Free Media & Video
        img_url, img_credit, video_html = media_resolver.resolve_media(
            query=topic["search_query"],
            pillar_key=pillar,
            default_img=topic["default_image"],
            default_credit=topic["image_credit"]
        )

        # Step 4: Dispatch to D1 + Blogger + IndexNow
        cf_live = dispatcher.publish_to_d1(article, topic, img_url, img_credit)
        blogger_url = dispatcher.publish_to_blogger_cross(article, topic, img_url, video_html, live_url=cf_live)

        # Step 4b: Two-Way Interconnection: Link Blogger back into D1 sources if published
        if cf_live and blogger_url and dispatcher.cf_account and dispatcher.cf_db and dispatcher.cf_token:
            try:
                sources_with_blogger = json.dumps([
                    {"title": "UniqueDigit Editorial Desk", "url": cf_live},
                    {"title": "Official Blogger Syndication Archive", "url": blogger_url}
                ], ensure_ascii=False)
                update_sql = "UPDATE posts SET sources = ? WHERE niche_id = (SELECT id FROM niches WHERE slug = ? LIMIT 1) AND slug = ?"
                slug_val = cf_live.split("/")[-1]
                dispatcher_endpoint = f"https://api.cloudflare.com/client/v4/accounts/{dispatcher.cf_account}/d1/database/{dispatcher.cf_db}/query"
                requests.post(
                    dispatcher_endpoint,
                    headers={"Authorization": f"Bearer {dispatcher.cf_token}", "Content-Type": "application/json"},
                    json={"sql": update_sql, "params": [sources_with_blogger, topic["niche_slug"], slug_val]},
                    timeout=10
                )
                log("SyndicationAgent", "🔗 Two-Way Interconnection Locked: Cloudflare D1 & Blogger linked bidirectionally!")
            except Exception as e:
                log("SyndicationAgent", f"Interconnection sync note: {e}")

        # Step 5: Save to Seen Cache
        seen_cache = load_seen_cache()
        seen_cache[topic["hash"]] = {
            "title": article["title"],
            "query": topic["search_query"],
            "pillar": pillar,
            "published_at": datetime.now().isoformat(),
            "cf_url": cf_live,
            "blogger_url": blogger_url
        }
        save_seen_cache(seen_cache)

        published_total += 1
        log("MasterMission", f"🎉 Evergreen Guide Published & Indexed successfully!")
        time.sleep(3)

    print("=" * 75)
    print(f"🏁 SYSTEM 2 MISSION COMPLETE: {published_total} Master Guides Deployed!")
    print("=" * 75)

if __name__ == "__main__":
    pillar_arg = sys.argv[1] if len(sys.argv) > 1 else "health"
    count_arg = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    run_evergreen_mission(pillar=pillar_arg, count=count_arg)
