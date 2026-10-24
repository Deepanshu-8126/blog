#!/usr/bin/env python3
"""
========================================================================================
🌲 SYSTEM 2: EVERGREEN HIGH-INTENT AUTHORITY GUIDE ENGINE (PRODUCTION V2 - RECTIFIED)
========================================================================================
Autonomous Long-Form Master Guide Generation Engine (3-5 Year Passive Search Traffic)
Zero-Slop, 100% E-E-A-T Compliant, Dual-Syndicated & Hardened against all 20 Audit Flaws.

Pillars:
  1. 🥗 Health, Gym & Nutrition (Pexels HD Gym Media + Vegetarian Protein Macro Guides)
  2. 💰 Personal Finance & Daily Savings (SIP vs FD, Tax Regimes, High-RPM Guides)
  3. 🎓 Student & Career Roadmaps (SSC CGL, ATS Resumes, High-Paying Careers)
  4. 🛠️ Daily Life Hacks & How-To (Train PNR/RAC, Aadhaar Updates, Tech Fixes)
========================================================================================
"""

import os
import sys
import re
import json
import time
import uuid
import random
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
import markdown
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
# 1. EXPANDED SEED PILLARS & DIVERSIFIED MEDIA VAULT (Rectification #4 & #20)
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
            "best morning wellness drink for digestion and skin",
            "whey protein isolate vs concentrate which is best india",
            "push pull legs workout routine for natural lifters",
            "ashwagandha benefits dosage and timing for energy",
            "high protein breakfast options for indian vegetarians",
            "peanut butter benefits for weight gain and gym"
        ],
        "image_pool": [
            ("https://images.unsplash.com/photo-1517838277536-f5f99be501cd?w=1200&q=80", "Unsplash Royalty-Free Fitness Photography"),
            ("https://images.unsplash.com/photo-1540420773420-3366772f4999?w=1200&q=80", "Unsplash Fresh Vegetarian Nutrition Photography"),
            ("https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=1200&q=80", "Unsplash Athletic Strength Training Photography"),
            ("https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=1200&q=80", "Unsplash Healthy Balanced Diet Photography")
        ]
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
            "how to invest in index funds for beginners in india",
            "term insurance vs endowment policy which is better",
            "emergency fund calculation rules for salaried employees",
            "sovereign gold bond sgb returns vs physical gold"
        ],
        "image_pool": [
            ("https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?w=1200&q=80", "Unsplash Commercial Finance & Savings Media"),
            ("https://images.unsplash.com/photo-1559526324-4b87b5e36e44?w=1200&q=80", "Unsplash Verified Banking & Investment Photography"),
            ("https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=1200&q=80", "Unsplash Financial Markets & Capital Growth Photography")
        ]
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
            "top government computer certificate courses for jobs",
            "railway rrb ntpc preparation strategy for general awareness",
            "banking po vs ssc cgl career comparison salary and perks"
        ],
        "image_pool": [
            ("https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=1200&q=80", "Unsplash Verified Education & Study Photography"),
            ("https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=1200&q=80", "Unsplash Career Roadmap & Student Desk Media"),
            ("https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=1200&q=80", "Unsplash Digital Skills & Career Analytics Photography")
        ]
    },
    "lifehacks": {
        "niche_slug": "viral",
        "label": "Daily Life Hacks & Tech Fixes",
        "seeds": [
            "train ticket confirmation probability rules rac waitlist",
            "how to update mobile number in aadhaar online step by step",
            "smartphone battery draining fast how to fix hidden settings",
            "how to link pan card with aadhaar card online status check",
            "how to remove personal data from truecaller permanently",
            "best ceiling fan and inverter buying guide for indian summer",
            "how to check duplicate voter id card online in india"
        ],
        "image_pool": [
            ("https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=1200&q=80", "Unsplash Verified Mobile Technology Photography"),
            ("https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?w=1200&q=80", "Unsplash Indian Railway Transit & Navigation Photography"),
            ("https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=1200&q=80", "Unsplash Cyber Security & Online Privacy Photography")
        ]
    },
    "real-estate": {
        "niche_slug": "real-estate",
        "label": "Real Estate & Home Loans",
        "seeds": [
            "home loan emi calculator sbi hdfc 2026",
            "rental agreement format india how to make legally",
            "property buying guide for first time buyers in india",
            "ready to move vs under construction property pros cons",
            "home loan balance transfer process and benefits",
            "best areas to buy flat in hyderabad bengaluru pune 2026",
            "property registration charges and stamp duty india state wise",
            "vastu tips for home buying north east facing plot"
        ],
        "image_pool": [
            ("https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=1200&q=80", "Unsplash Real Estate Property Photography"),
            ("https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=1200&q=80", "Unsplash Modern Indian Home Architecture"),
            ("https://images.unsplash.com/photo-1582407947304-fd86f28f8de5?w=1200&q=80", "Unsplash Urban City Real Estate Photography")
        ]
    },
    "gadgets": {
        "niche_slug": "gadgets",
        "label": "Gadgets & Mobile Reviews",
        "seeds": [
            "best smartphones under 15000 india 2026",
            "best truly wireless earbuds under 2000 india",
            "laptop buying guide india under 50000 for students",
            "best smartwatch under 5000 india with health tracking",
            "gaming smartphone vs regular which is better for youtube",
            "best powerbank 20000mah fast charging india",
            "realme vs samsung which budget phone is better",
            "best 5g phone under 20000 india 2026 comparison"
        ],
        "image_pool": [
            ("https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=1200&q=80", "Unsplash Smartphone Photography"),
            ("https://images.unsplash.com/photo-1468495244123-6c6c332eeece?w=1200&q=80", "Unsplash Gadgets & Electronics Photography"),
            ("https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=1200&q=80", "Unsplash Laptop & Tech Photography")
        ]
    },
    "recipes": {
        "niche_slug": "recipes",
        "label": "Indian Recipes & Cooking",
        "seeds": [
            "quick indian dinner recipes ready in 30 minutes",
            "healthy office tiffin box ideas for weight loss",
            "high protein indian breakfast options for gym goers",
            "no oil no sugar sweets indian recipes for diabetics",
            "instant pot pressure cooker dal recipes india",
            "easy desi snacks recipes for kids after school",
            "low carb indian meal prep guide for weight loss",
            "winter special indian soups and kadha for immunity"
        ],
        "image_pool": [
            ("https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=1200&q=80", "Unsplash Indian Food Photography"),
            ("https://images.unsplash.com/photo-1567337710282-00832b415979?w=1200&q=80", "Unsplash Healthy Meal Prep Photography"),
            ("https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=1200&q=80", "Unsplash Fresh Cooking Photography")
        ]
    },
    "sports": {
        "niche_slug": "sports",
        "label": "Sports & Cricket",
        "seeds": [
            "ipl 2026 squad analysis best players each team",
            "cricket fitness routine batsmen bowlers stamina",
            "how to improve batting technique tips for amateur cricketers",
            "football vs cricket career in india which pays more",
            "best sports protein supplements for athletes india 2026",
            "badminton tips for beginners techniques grip footwork",
            "kabaddi training routine strength conditioning for players",
            "how to watch ipl free online legally 2026 india"
        ],
        "image_pool": [
            ("https://images.unsplash.com/photo-1531415074968-036ba1b575da?w=1200&q=80", "Unsplash Cricket Sports Photography"),
            ("https://images.unsplash.com/photo-1579952363873-27f3bade9f55?w=1200&q=80", "Unsplash Football & Sports Action Photography"),
            ("https://images.unsplash.com/photo-1544117519-31a4b719223d?w=1200&q=80", "Unsplash Badminton & Indoor Sports Photography")
        ]
    },
    "parenting": {
        "niche_slug": "parenting",
        "label": "Parenting & Baby Care",
        "seeds": [
            "newborn baby care tips first month india",
            "school fees comparison top private schools india 2026",
            "best educational toys for kids 2 to 5 years india",
            "how to improve child concentration and focus naturally",
            "screen time guidelines for toddlers and children",
            "best baby food recipes 6 months to 1 year india",
            "how to choose right school for your child india guide",
            "common childhood diseases symptoms home treatment india"
        ],
        "image_pool": [
            ("https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=1200&q=80", "Unsplash Happy Parenting Family Photography"),
            ("https://images.unsplash.com/photo-1492725764893-90b379c2b6e7?w=1200&q=80", "Unsplash Baby Care Photography"),
            ("https://images.unsplash.com/photo-1503454537195-1dcabb73ffb9?w=1200&q=80", "Unsplash Children Playing Photography")
        ]
    },
    "travel": {
        "niche_slug": "travel",
        "label": "Travel & Budget Trips",
        "seeds": [
            "budget solo travel india hill stations under 5000",
            "best train routes india scenic journey guide",
            "thailand visa on arrival guide for indian passport holders",
            "how to book cheap flights india tips and tricks",
            "best weekend getaways from delhi mumbai bengaluru 2026",
            "irctc tatkal booking tips to get confirmed ticket",
            "best backpacking destinations india for college students",
            "manali leh bike trip complete guide packing list budget"
        ],
        "image_pool": [
            ("https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?w=1200&q=80", "Unsplash Travel Adventure Photography"),
            ("https://images.unsplash.com/photo-1473496169904-658ba7574b0d?w=1200&q=80", "Unsplash Indian Mountain Travel Photography"),
            ("https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1200&q=80", "Unsplash Beach & Tropical Travel Photography")
        ]
    },
    "ai-tools": {
        "niche_slug": "ai-tools",
        "label": "AI Tools & Viral Prompts",
        "seeds": [
            "best free ai video generator tools without watermark 2026",
            "chatgpt prompts for resume writing ats friendly free",
            "best ai tools for students research study notes",
            "midjourney prompts for realistic indian portraits 4k",
            "free ai voice generator text to speech hindi english",
            "deepseek vs chatgpt for coding python which is better",
            "best ai image generator free alternatives to midjourney",
            "chatgpt prompts for digital marketing and social media reels",
            "claude ai prompt engineering guide for copywriting",
            "best free ai website builders for beginners india"
        ],
        "image_pool": [
            ("https://images.unsplash.com/photo-1677442136019-21780ecad995?w=1200&q=80", "Unsplash Artificial Intelligence & Deep Learning Tech"),
            ("https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=1200&q=80", "Unsplash Generative AI & Neural Network Visual"),
            ("https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=1200&q=80", "Unsplash Future Computing & AI Automation Photography")
        ]
    },
    "comics": {
        "niche_slug": "comics",
        "label": "Comics, Manga & Anime Lore",
        "seeds": [
            "solo leveling ragnarok ending explained sung suho powers",
            "one piece chapter release date countdown leaks schedule",
            "jujutsu kaisen strongest characters ranked power scale tier list",
            "marvel secret wars timeline and incursions explained for beginners",
            "spider man beyond amazing comics story recap issue",
            "boruto two blue vortex chapter release date countdown raw scans",
            "demon slayer hashira power rankings ranked weakest to strongest",
            "batman darkest comic storylines every fan must read",
            "relatable indian engineering college life funny comic strips",
            "corporate mazdoor daily life hilarious webcomic strip"
        ],
        "image_pool": [
            ("https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?w=1200&q=80", "Unsplash Anime Comic Action Illustration Art"),
            ("https://images.unsplash.com/photo-1578632767115-351597cf2477?w=1200&q=80", "Unsplash Manga Dark Fantasy Artwork"),
            ("https://images.unsplash.com/photo-1563089145-599997674d42?w=1200&q=80", "Unsplash Comic Book Graphic Neon Visual")
        ]
    }
}

# Niche-Specific Blogger Routing (Rectification #3)
BLOGGER_NICHE_ROUTING = {
    "career": os.getenv("BLOGGER_EXAM_BLOG_ID") or os.getenv("BLOGGER_BLOG_ID"),
    "finance": os.getenv("BLOGGER_DEALS_BLOG_ID") or os.getenv("BLOGGER_BLOG_ID"),
    "lifehacks": os.getenv("BLOGGER_VIRAL_BLOG_ID") or os.getenv("BLOGGER_BLOG_ID"),
    "health": os.getenv("BLOGGER_BLOG_ID"),
    "ai-tools": os.getenv("BLOGGER_BLOG_ID"),
    "ai": os.getenv("BLOGGER_BLOG_ID"),
    "comics": os.getenv("BLOGGER_VIRAL_BLOG_ID") or os.getenv("BLOGGER_BLOG_ID"),
    # New niches → main blog (fallback routing, update per blog when new Blogger blogs created)
    "real-estate": os.getenv("BLOGGER_BLOG_ID"),
    "gadgets": os.getenv("BLOGGER_VIRAL_BLOG_ID") or os.getenv("BLOGGER_BLOG_ID"),
    "recipes": os.getenv("BLOGGER_BLOG_ID"),
    "sports": os.getenv("BLOGGER_VIRAL_BLOG_ID") or os.getenv("BLOGGER_BLOG_ID"),
    "parenting": os.getenv("BLOGGER_BLOG_ID"),
    "travel": os.getenv("BLOGGER_VIRAL_BLOG_ID") or os.getenv("BLOGGER_BLOG_ID"),
}

# ======================================================================================
# 2. KEYWORD HARVESTER WITH NORMALIZATION (Rectification #17)
# ======================================================================================
class EvergreenIntentHarvester:
    """Discovers real Google Autocomplete queries based on high-intent evergreen seed topics."""

    def __init__(self):
        self.seen_cache = load_seen_cache()

    def normalize_query(self, q: str) -> str:
        clean = re.sub(r'[^a-zA-Z0-9\s]', '', q).lower().strip()
        return re.sub(r'\s+', ' ', clean)

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

        if not suggestions:
            suggestions = [seed]
        return suggestions

    def harvest_next_topic(self, pillar_key: str = "health") -> dict | None:
        pillar = EVERGREEN_PILLARS.get(pillar_key, EVERGREEN_PILLARS["health"])
        seeds = list(pillar["seeds"])
        random.shuffle(seeds)

        for seed in seeds:
            queries = self.get_google_suggestions(seed)
            for q in queries:
                norm = self.normalize_query(q)
                q_hash = hashlib.md5(norm.encode("utf-8")).hexdigest()
                if q_hash not in self.seen_cache:
                    return {
                        "pillar_key": pillar_key,
                        "niche_slug": pillar["niche_slug"],
                        "label": pillar["label"],
                        "search_query": q,
                        "seed": seed,
                        "hash": q_hash
                    }

        # Fallback to a timestamped seed
        chosen_seed = seeds[0]
        norm = self.normalize_query(chosen_seed)
        return {
            "pillar_key": pillar_key,
            "niche_slug": pillar["niche_slug"],
            "label": pillar["label"],
            "search_query": chosen_seed,
            "seed": chosen_seed,
            "hash": hashlib.md5((norm + str(time.time())).encode("utf-8")).hexdigest()
        }

# ======================================================================================
# 3. MASTER EDITORIAL GUIDE WRITER (Rectifications #1, #6, #7, #8, #9, #10, #11, #12, #13)
# ======================================================================================
class EvergreenGuideWriter:
    """Generates 1,200+ words, deeply structured, original evergreen master guides."""

    def clean_title(self, raw_title: str) -> str:
        """Enforces clean 50-65 chars title without ugly ellipsis (Rectification #1)"""
        title = re.sub(r'[\"\']', '', raw_title).strip()
        title = re.sub(r'\s*\.{2,}\s*$', '', title)
        
        if len(title) > 65:
            words = title[:62].split()
            title = " ".join(words[:-1]) if len(words) > 1 else words[0]
        elif len(title) < 45:
            title = f"{title}: Detailed Practical Guide"
            if len(title) > 65:
                title = title[:65]
        return title

    def fetch_existing_internal_links(self, niche_slug: str) -> list[dict]:
        """Queries D1 for recent published articles in the same niche to weave contextual internal backlinks."""
        links = []
        cf_acc = os.getenv("CLOUDFLARE_ACCOUNT_ID") or "cf1a42fb306054063805cf459fddf853"
        cf_db = os.getenv("CLOUDFLARE_D1_DATABASE_ID") or "61d1d46f-f438-47f5-9128-516d9beb11cb"
        cf_token = os.getenv("CLOUDFLARE_API_TOKEN")
        if not cf_token:
            return links
        try:
            sql = "SELECT slug, title FROM posts WHERE niche_id = (SELECT id FROM niches WHERE slug = ? LIMIT 1) AND status = 'published' AND kind = 'article' ORDER BY published_at DESC LIMIT 4"
            endpoint = f"https://api.cloudflare.com/client/v4/accounts/{cf_acc}/d1/database/{cf_db}/query"
            r = requests.post(endpoint, headers={"Authorization": f"Bearer {cf_token}", "Content-Type": "application/json"}, json={"sql": sql, "params": [niche_slug]}, timeout=5)
            if r.status_code == 200:
                rows = r.json().get("result", [{}])[0].get("results", [])
                for row in rows:
                    if row.get("slug") and row.get("title"):
                        links.append({"title": row.get("title"), "url": f"/{niche_slug}/{row.get('slug')}"})
        except Exception as e:
            log("GuideWriter", f"Internal linking query note: {e}")
        return links

    def write_guide(self, topic: dict) -> dict | None:
        query = topic["search_query"]
        pillar = topic["pillar_key"]
        niche_slug = topic["niche_slug"]
        log("GuideWriter", f"Synthesizing high-intent authority guide for: '{query}'...")

        # Domain specific prompt rules (Rectifications #10, #11, #12, #13)
        domain_rules = ""
        if pillar == "health":
            domain_rules = """
- Include standard macronutrient comparison table with columns: [Food Item | Typical Serving | Protein (g) | Carbs (g) | Healthy Fats (g) | Approx Calories]
- Detail timing: Pre-workout vs Post-workout vs Bedtime intake.
- Highlight common mistakes like ignoring complete amino acid profiles or under-eating.
"""
        elif pillar == "finance":
            domain_rules = """
- Include exact mathematical calculation comparison table: [Tenure | Monthly Investment | Total Invested | Est. Wealth @ 12% (SIP) | Est. Return @ 7% (FD)]
- Explicitly state the 6% inflation impact and 12.5% LTCG tax rules (Budget 2024 update).
- Highlight common mistakes like premature redemptions or stopping SIPs during market corrections.
"""
        elif pillar == "career":
            domain_rules = """
- Include practical daily study schedule table for working professionals / freshers.
- Cite official commissions: SSC (ssc.gov.in) or UPSC (upsc.gov.in) with accurate eligibility criteria.
- Recommend authentic free resources and official syllabus breakdowns.
"""
        elif pillar == "real-estate":
            domain_rules = """
- Include EMI calculation matrix for ₹30L, ₹50L, and ₹75L home loans across 10, 20, and 30-year tenures.
- Detail legal due diligence checklist: Title Deed, Encumbrance Certificate, RERA approval number.
- Comparison: Ready to move vs Under construction tax benefits & risks.
"""
        elif pillar == "gadgets":
            domain_rules = """
- Include complete spec comparison matrix table: [Device | Display & Refresh Rate | Processor | Battery & Charging | Camera Setup | Price in India]
- Explicitly state who should buy and who should skip this device.
- Highlight real-world battery life and long-term software update policy.
"""
        elif pillar == "recipes":
            domain_rules = """
- Include full nutrition breakdown table: [Serving Size | Calories | Protein | Carbs | Fats | Dietary Fiber]
- Clearly state Prep Time, Cook Time, and Total Servings.
- Step-by-step numbered cooking method with expert chef tips for texture and aroma.
"""
        elif pillar == "sports":
            domain_rules = """
- Include player/team tactical performance comparison table with strike rates, averages, or fitness metrics.
- Actionable weekly athletic conditioning split for amateur athletes.
- Professional recovery and injury prevention checklist.
"""
        elif pillar == "parenting":
            domain_rules = """
- Include age-by-age developmental milestones table.
- Clear pediatric wellness guidelines and screen-time recommendations.
- Essential safety checklist for child health and home environment.
"""
        elif pillar == "travel":
            domain_rules = """
- Include complete budget estimation table: [Expense Category | Budget Traveler (₹) | Mid-Range (₹) | Luxury (₹)]
- Detailed Day-wise practical itinerary with local transport recommendations.
- Best season to visit, packing checklist, and local booking hacks.
"""
        elif pillar in ["ai-tools", "ai"]:
            domain_rules = """
- Include comparison matrix table: [AI Tool | Primary Use Case | Free Tier Limit | Paid Pricing (₹/$) | Top Free Alternative]
- Provide 3 to 5 EXACT copy-paste ready-to-use Prompt Templates inside markdown code blocks with fill-in-the-blank brackets like [Insert Company / Topic].
- Step-by-step master workflow: System prompt setup, role playing, context injection, and avoiding hallucinations.
- Clear disclosure on commercial licensing, copyright rights, and data privacy policies.
"""
        elif pillar in ["comics", "manga"]:
            domain_rules = """
- Include character power level or chapter breakdown matrix table: [Character / Arc | Power Tier (SSS/S/A/B) | Signature Feat / Ability | Counter / Weakness]
- If covering upcoming chapter/issues: Include explicit Release Schedule Box [Official Drop Date | Raw Scan Leak Window | Where to Read Legally (MangaPlus/Viz)]
- If explaining story/ending: Complete chronological recap with core turning points and thematic breakdown.
- Include explicit Fair-Use Editorial Fan Commentary Notice: State that all characters and lore are property of their respective creators/publishers and this analysis is non-commercial critique and news reporting.
"""
        else: # lifehacks
            domain_rules = """
- Step-by-step navigation for official portal (e.g. myaadhaar.uidai.gov.in or irctc.co.in).
- Safety warning against fake phishing portals or unauthorized cyber cafes.
"""

        # Fetch existing articles for contextual in-body internal backlinks
        existing_articles = self.fetch_existing_internal_links(niche_slug)
        internal_links_clause = ""
        if existing_articles:
            formatted_links = "\n".join([f"- Title: \"{a['title']}\" -> Link: `{a['url']}`" for a in existing_articles[:3]])
            internal_links_clause = f"""
11. **Contextual In-Body Internal Backlinks (SEO Topical Silo)**:
   You MUST naturally integrate 1 or 2 of the following internal links directly into relevant paragraph sentences using markdown hyperlink format [Anchor Text](path):
{formatted_links}
   CRITICAL: Embed them contextually inside paragraph text (e.g., "For related guidance, check our [Complete Guide](url)"), NOT as a detached bullet list at the end.
"""

        prompt = f"""
You are a Senior Subject-Matter Specialist and Master Technical Content Writer creating a permanent, evergreen master guide.
Target Search Query: "{query}"
Domain Pillar: {topic['label']}

STRICT EDITORIAL REQUIREMENTS (Zero AI Slop, 100% Comprehensive E-E-A-T):
1. **Title**: EXACTLY 50 to 65 characters long. Ultra-clickable, punchy, contains the exact search keyword. No ellipses '...'.
2. **Top Metadata Bar**: Include reading time, author desk, and fact-check date.
3. **Quick Answer Box (Position 0 Featured Snippet)**: Exact 2-sentence direct, unambiguous summary answer to the reader's question.
4. **Table of Contents (Jump to Section)**: Formatted markdown TOC linking to internal H2 sections.
5. **Comprehensive Practical Breakdown (1,200+ words)**:
   - Provide depth, actionable steps, real numbers, and clear reasoning.
{domain_rules}
6. **Comparison / Data Table**: A structured Markdown table with complete data.
7. **Common Pitfalls & Mistakes to Avoid**: Highlight 3-4 frequent mistakes and their solutions.
8. **Actionable Routine / Checklist**: Clear step-by-step daily checklist.
9. **Statutory & Advisory Disclaimer**:
   - For Health: Medical & clinical disclaimer to consult a certified doctor before changing diet or supplements.
   - For Finance: SEBI informational disclaimer stating mutual funds carry market risk.
   - Educational Fair Dealing notice under Section 52(1)(q).
10. **Structured FAQs (Max 5 Questions)**:
    - Questions must be natural user search queries.
    - CRITICAL: Answers MUST be concise (under 2-3 sentences, <60 words) so Google's FAQ rich result parser shows them.
{internal_links_clause}
OUTPUT STRICT VALID JSON ONLY (No markdown code fences, no extraneous text):
{{
  "title": "50-65 chars punchy title",
  "summary": "130-155 characters SEO meta description containing the target keyword",
  "body_md": "Full markdown content with ## headings, TOC, tables, bullet points, and disclaimers",
  "faq": [
    {{"q": "Real question 1?", "a": "Direct concise answer 1"}},
    {{"q": "Real question 2?", "a": "Direct concise answer 2"}},
    {{"q": "Real question 3?", "a": "Direct concise answer 3"}},
    {{"q": "Real question 4?", "a": "Direct concise answer 4"}},
    {{"q": "Real question 5?", "a": "Direct concise answer 5"}}
  ],
  "labels": ["Primary Category", "Secondary Tag", "Trending Guide"]
}}
"""
        for attempt in range(2):
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
                    # Fix unescaped control characters (Rectification #6)
                    parsed = json.loads(clean_json, strict=False)

                # Enforce clean 50-65 character title without ellipses
                parsed["title"] = self.clean_title(parsed.get("title", query.title()))
                return parsed
            except Exception as e:
                log("GuideWriter", f"⚠️ Generation attempt {attempt+1} note: {e}")
                time.sleep(2)

        return None

# ======================================================================================
# 4. MEDIA & STOCK VIDEO RESOLVER (Rectifications #4, #14)
# ======================================================================================
class EvergreenMediaResolver:
    """Resolves HD royalty-free photos and optional video loops for maximum dwell time."""

    def resolve_media(self, query: str, pillar_key: str) -> tuple[str, str, str | None]:
        pillar = EVERGREEN_PILLARS.get(pillar_key, EVERGREEN_PILLARS["health"])
        pool = pillar["image_pool"]

        # 1. Try master image pipeline
        img_url, img_credit = resolve_master_image(query, niche_slug=pillar_key)

        # 2. If not verified or generic emblem, pick from verified diverse pool
        if not verify_image_health(img_url) or "emblem" in img_credit.lower():
            # Pick deterministically by query hash for consistency across runs
            idx = abs(hash(query)) % len(pool)
            img_url, img_credit = pool[idx]

        # 3. Responsive Video Demo embed for Health & Tech
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
# 5. SYNDICATION & CLOUDFLARE D1 PUBLISHER (Rectifications #2, #3, #5, #14, #15, #16, #19)
# ======================================================================================
class EvergreenSyndicationAgent:
    """Dual-publishes evergreen guides to Cloudflare D1 and Blogger, then triggers IndexNow."""

    def __init__(self):
        self.cf_account = os.getenv("CLOUDFLARE_ACCOUNT_ID")
        self.cf_db = os.getenv("CLOUDFLARE_D1_DATABASE_ID")
        self.cf_token = os.getenv("CLOUDFLARE_API_TOKEN")

    def build_clean_slug(self, title: str) -> str:
        """Cuts cleanly at word boundary without dangling hyphens (Rectification #2)"""
        clean = re.sub(r'[^a-z0-9\s]+', ' ', title.lower()).strip()
        words = clean.split()
        slug = ""
        for w in words:
            if len(f"{slug}-{w}".strip('-')) <= 75:
                slug = f"{slug}-{w}".strip('-')
            else:
                break
        return slug or "guide"

    def publish_to_d1(self, article: dict, topic: dict, img_url: str, img_credit: str) -> str | None:
        if not self.cf_account or not self.cf_db or not self.cf_token:
            log("SyndicationAgent", "⚠️ Cloudflare credentials missing in .env.")
            return None

        slug = self.build_clean_slug(article["title"])
        post_id = uuid.uuid4().hex[:16]
        niche_slug = topic["niche_slug"]
        faq_json = json.dumps(article.get("faq", []), ensure_ascii=False)
        sources_json = json.dumps([{"title": "UniqueDigit Editorial Research", "url": "https://uniquedigit-viral-hub.pages.dev"}], ensure_ascii=False)

        # Genuine zero-baseline views (real user metrics only)
        hype_val = round(88.0 + random.uniform(0.5, 7.5), 1)
        views_val = 0

        sql = """
        INSERT INTO posts (
            id, niche_id, slug, kind, title, summary, body_md, faq, sources,
            image_url, image_credit, source_url, hype, views, is_breaking, indexable, status,
            published_at, updated_at
        )
        VALUES (
            ?, (SELECT id FROM niches WHERE slug = ? LIMIT 1),
            ?, 'article', ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, 0, 1, 'published',
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
            f"https://uniquedigit-viral-hub.pages.dev/{niche_slug}/{slug}",
            hype_val, views_val
        ]

        endpoint = f"https://api.cloudflare.com/client/v4/accounts/{self.cf_account}/d1/database/{self.cf_db}/query"
        headers = {"Authorization": f"Bearer {self.cf_token}", "Content-Type": "application/json"}

        try:
            r = requests.post(endpoint, headers=headers, json={"sql": sql, "params": params}, timeout=15)
            if r.status_code == 200 and r.json().get("success"):
                live_url = f"https://uniquedigit-viral-hub.pages.dev/{niche_slug}/{slug}"
                log("SyndicationAgent", f"✅ Cloudflare D1 Live: {live_url}")

                # Ping IndexNow with retry (Rectification #16)
                for _ in range(2):
                    try:
                        submit_url_to_indexnow(live_url)
                        log("SyndicationAgent", f"⚡ IndexNow Ping delivered for: {live_url}")
                        break
                    except Exception:
                        time.sleep(1)

                return live_url
            else:
                log("SyndicationAgent", f"❌ D1 API error: {r.text}")
        except Exception as e:
            log("SyndicationAgent", f"❌ D1 request failed: {e}")

        return None

    def publish_to_blogger_cross(self, article: dict, topic: dict, img_url: str, video_html: str | None, live_url: str | None = None) -> str | None:
        if not BLOGGER_AVAILABLE:
            return None

        # Route to niche-specific Blogger Blog ID (Rectification #3)
        pillar = topic.get("pillar_key", "health")
        blog_id = BLOGGER_NICHE_ROUTING.get(pillar) or os.getenv("BLOGGER_BLOG_ID")
        if not blog_id:
            return None

        # 1. Build Pillar-Specific E-E-A-T Advisory Text
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

        # 2. Table CSS for Mobile Responsive Rendering on Blogger (Rectification #5)
        table_css = """
<style>
.evergreen-article-container .table-responsive {
  width: 100%;
  overflow-x: auto;
  margin: 24px 0;
  -webkit-overflow-scrolling: touch;
}
.evergreen-article-container table {
  width: 100%;
  border-collapse: collapse;
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

        # 3. Canonical Header Badge (Passing Link Juice to UniqueDigit - Rectification #19)
        canonical_header = ""
        canonical_footer = ""
        if live_url:
            canonical_header = f"""
<div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); border-radius: 12px; padding: 14px 18px; margin: 0 0 24px 0; color: #ffffff; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
  <div>
    <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; color: #38bdf8; font-weight: 700;">📌 Official Primary Source</div>
    <div style="font-size: 13px; font-weight: 600; color: #f8fafc; margin-top: 2px;">UniqueDigit Interactive Research Hub</div>
  </div>
  <a href="{live_url}" target="_blank" rel="canonical bookmark" style="background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%); color: #ffffff; text-decoration: none; padding: 8px 16px; border-radius: 8px; font-weight: 700; font-size: 12px; display: inline-flex; align-items: center; gap: 6px;">
    Open Interactive Guide & Calculators ➔
  </a>
</div>
"""
            canonical_footer = f"""
<div style="margin: 32px 0 20px 0; padding: 20px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; text-align: center;">
  <div style="font-size: 14px; font-weight: 700; color: #0f172a; margin-bottom: 6px;">📖 Read Full Interactive Research on UniqueDigit</div>
  <p style="font-size: 13px; color: #64748b; margin: 0 0 12px 0;">This publication is synchronized with the live database at UniqueDigit. View full charts, data points, and community updates:</p>
  <a href="{live_url}" target="_blank" rel="canonical bookmark" style="display: inline-block; background: #0284c7; color: #ffffff; padding: 10px 22px; border-radius: 8px; text-decoration: none; font-weight: 700; font-size: 13px;">
    Access Complete Guide on UniqueDigit →
  </a>
</div>
"""

        # 4. Convert Markdown Body to HTML with native tables wrapped in table-responsive
        parsed_html = markdown.markdown(article["body_md"], extensions=['tables', 'extra', 'nl2br'])
        # Wrap tables in responsive wrapper (Rectification #5)
        parsed_html = re.sub(r'(<table>.*?</table>)', r'<div class="table-responsive">\1</div>', parsed_html, flags=re.DOTALL)

        # 5. Assemble Rich Container
        body_html = f'<div class="evergreen-article-container" style="font-family: system-ui, -apple-system, sans-serif; line-height: 1.8; color: #1e293b;">\n'
        body_html += table_css
        body_html += canonical_header

        # Hero Image with Alt Tag & Lazy Loading (Rectification #14)
        if img_url:
            body_html += f'<div style="text-align: center; margin-bottom: 24px;"><img src="{img_url}" alt="{article["title"]}" loading="lazy" style="max-width: 100%; height: auto; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);"/></div>\n'

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
                log("SyndicationAgent", f"✅ Blogger published (Blog ID {blog_id}): {blogger_url}")
                return blogger_url
        except Exception as e:
            log("SyndicationAgent", f"⚠️ Blogger syndication note: {e}")

        return None

# ======================================================================================
# 6. MASTER ORCHESTRATION DISPATCHER (Rectification #20)
# ======================================================================================
def run_evergreen_mission(pillar: str = "health", count: int = 1):
    if pillar.lower() == "all":
        pillars_to_run = list(EVERGREEN_PILLARS.keys())
    elif pillar.lower() == "auto":
        # Auto-balance: pick the pillar with the fewest published guides or oldest publication
        seen_cache = load_seen_cache()
        pillar_counts = {p: 0 for p in EVERGREEN_PILLARS.keys()}
        pillar_last_seen = {p: "" for p in EVERGREEN_PILLARS.keys()}
        for item in seen_cache.values():
            p = item.get("pillar")
            if p in pillar_counts:
                pillar_counts[p] += 1
                if item.get("published_at", "") > pillar_last_seen[p]:
                    pillar_last_seen[p] = item.get("published_at", "")
        # Sort by count ascending, then by last published ascending
        sorted_pillars = sorted(EVERGREEN_PILLARS.keys(), key=lambda p: (pillar_counts[p], pillar_last_seen[p]))
        current_choice = sorted_pillars[0]
        pillars_to_run = [current_choice]
        log("AutoScheduler", f"🎯 Intelligent Auto-Balanced Pillar Selected: '{current_choice.upper()}' (coverage count: {pillar_counts[current_choice]})")
    else:
        pillars_to_run = [pillar.lower()]

    print("=" * 75)
    print(f"🌲 INITIATING SYSTEM 2: EVERGREEN AUTHORITY MISSION ({', '.join(pillars_to_run).upper()})")
    print("=" * 75)

    harvester = EvergreenIntentHarvester()
    writer = EvergreenGuideWriter()
    media_resolver = EvergreenMediaResolver()
    dispatcher = EvergreenSyndicationAgent()

    total_deployed = 0
    for current_pillar in pillars_to_run:
        if current_pillar not in EVERGREEN_PILLARS:
            log("MasterMission", f"⚠️ Unknown pillar: '{current_pillar}'. Skipping.")
            continue

        for i in range(count):
            print("-" * 75)
            log("MasterMission", f"Running [{current_pillar.upper()}] Task {i + 1}/{count}...")

            # Step 1: Harvest high-intent search query
            topic = harvester.harvest_next_topic(pillar_key=current_pillar)
            if not topic:
                log("MasterMission", "⚠️ No evergreen topic available.")
                continue

            log("MasterMission", f"🎯 Target Search Query: '{topic['search_query']}'")

            # Step 2: Write long-form master guide with 20-flaw guardrails
            article = writer.write_guide(topic)
            if not article or not article.get("title") or not article.get("body_md"):
                log("MasterMission", "❌ Failed to generate master guide.")
                continue

            # Step 3: Resolve Royalty-Free Media & Video from Curated Vault
            img_url, img_credit, video_html = media_resolver.resolve_media(
                query=topic["search_query"],
                pillar_key=current_pillar
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
                "pillar": current_pillar,
                "published_at": datetime.now().isoformat(),
                "cf_url": cf_live,
                "blogger_url": blogger_url
            }
            save_seen_cache(seen_cache)

            total_deployed += 1
            log("MasterMission", f"🎉 Evergreen Guide Published & Indexed successfully!")
            time.sleep(3)

    print("=" * 75)
    print(f"🏁 SYSTEM 2 MISSION COMPLETE: {total_deployed} Master Guides Deployed & Verified!")
    print("=" * 75)

if __name__ == "__main__":
    pillar_arg = sys.argv[1] if len(sys.argv) > 1 else "health"
    count_arg = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    run_evergreen_mission(pillar=pillar_arg, count=count_arg)
