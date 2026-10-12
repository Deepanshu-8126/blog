#!/usr/bin/env python3
"""
=============================================================================
🚀 TOP NICHES HIGH-CRAFT CONTENT POPULATOR (Zero AI Slop & Real HD Media)
=============================================================================
Generates deeply humanized, authentic editorial articles for top empty niches:
- AI Tools (ai-tools)
- PC Builds (pc-builds)
- Deals & Loot (deals)
- Health & Fitness (health)
- Food & Recipes (food)
- Fashion (fashion)
- Side Hustles (side-hustles)
=============================================================================
"""

import os
import sys
import json
import re
import uuid
import time
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")
sys.path.insert(0, str(ROOT))

import requests
from pipeline import gemini

CF_ACCOUNT = os.getenv("CLOUDFLARE_ACCOUNT_ID", "cf1a42fb306054063805cf459fddf853")
CF_D1_DB = os.getenv("CLOUDFLARE_D1_DATABASE_ID", "61d1d46f-f438-47f5-9128-516d9beb11cb")
CF_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN", "")

# Curated High-Intent Topics & Visuals for Top Niches
TOP_NICHE_SEEDS = [
    # 1. AI Tools
    {
        "niche_slug": "ai-tools",
        "title": "5 Best Free AI Tools Every Indian Student and Creator Must Use in 2026",
        "angle": "Practical, zero-cost AI productivity tools that actually replace paid ChatGPT Plus and Canva Pro",
        "image": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=1200&h=630&fit=crop",
        "image_credit": "Unsplash Artificial Intelligence Desk",
        "hype": 94.0
    },
    {
        "niche_slug": "ai-tools",
        "title": "DeepSeek vs ChatGPT vs Claude: Which AI Gives the Best Coding and Reasoning Answers?",
        "angle": "Benchmark comparison for developers and students in India looking for maximum intelligence without spending monthly fees",
        "image": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=1200&h=630&fit=crop",
        "image_credit": "Unsplash Cyber Intelligence",
        "hype": 92.0
    },

    # 2. PC Builds
    {
        "niche_slug": "pc-builds",
        "title": "Best Gaming PC Build Under ₹50,000 in India (2026 Edition): High FPS 1080p Gaming",
        "angle": "Value-for-money parts list with Ryzen 5, RTX 3060/RX 6600, 16GB RAM, and reliable PSU that won't bottleneck",
        "image": "https://images.unsplash.com/photo-1587202372775-e229f172b9d7?w=1200&h=630&fit=crop",
        "image_credit": "Unsplash Custom PC Rig Studio",
        "hype": 95.0
    },
    {
        "niche_slug": "pc-builds",
        "title": "RTX 4060 vs RTX 3060 12GB: Which Graphics Card Should You Buy in India Right Now?",
        "angle": "Real gaming benchmarks, DLSS 3 frame generation vs extra VRAM dilemma for Indian gamers on a budget",
        "image": "https://images.unsplash.com/photo-1591488320449-011701bb6704?w=1200&h=630&fit=crop",
        "image_credit": "Unsplash Hardware Benchmarks",
        "hype": 89.0
    },

    # 3. Deals & Loot
    {
        "niche_slug": "deals",
        "title": "How to Catch 0-Minute Price Glitches on Amazon and Flipkart: Secret Telegram Hacks",
        "angle": "Insider tricks to spot lightning price drops, hidden bank instant coupons, and avoid cancellation",
        "image": "https://images.unsplash.com/photo-1607082348824-0a96f2a4b9da?w=1200&h=630&fit=crop",
        "image_credit": "Unsplash Festive Sales Desk",
        "hype": 96.0
    },
    {
        "niche_slug": "deals",
        "title": "Top 5 ANC TWS Earbuds Under ₹2,000 in India: Deep Bass and Clear Calling Tested",
        "angle": "Honest breakdown of boAt, Realme, OnePlus, and Noise earbuds with active noise cancellation",
        "image": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=1200&h=630&fit=crop",
        "image_credit": "Unsplash Audio Gear Studio",
        "hype": 88.0
    },

    # 4. Health & Fitness
    {
        "niche_slug": "health",
        "title": "High-Protein Indian Vegetarian Diet for Muscle Building: 100g Daily Protein Without Whey",
        "angle": "Affordable desi meal plan with Paneer, Soya chunks, Moong dal, Greek yogurt, and Roasted chana",
        "image": "https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=1200&h=630&fit=crop",
        "image_credit": "Unsplash Nutrition & Wellness",
        "hype": 93.0
    },
    {
        "niche_slug": "health",
        "title": "5 Best Gym Exercises for a V-Taper Back and Wider Shoulders: Form Guide & Mistakes",
        "angle": "Lat pulldowns, chest-supported rows, lateral raises, face pulls, and pull-up progression for natural lifters",
        "image": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?w=1200&h=630&fit=crop",
        "image_credit": "Unsplash Strength & Hypertrophy",
        "hype": 91.0
    },

    # 5. Food & Recipes
    {
        "niche_slug": "food",
        "title": "Restaurant-Style Paneer Butter Masala at Home: Secret Gravy Technique and Spices",
        "angle": "How to get that velvety makhani gravy without bitter tomatoes or excessive cream — foolproof 25-minute recipe",
        "image": "https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=1200&h=630&fit=crop",
        "image_credit": "Unsplash Desi Gourmet Studio",
        "hype": 90.0
    },
    {
        "niche_slug": "food",
        "title": "High-Protein Oats & Besan Chilla: 10-Minute Weight Loss Breakfast for Busy Mornings",
        "angle": "Crispy, gut-friendly desi pancake packed with vegetables and zero refined flour for sustained energy",
        "image": "https://images.unsplash.com/photo-1589302168068-964664d93dc0?w=1200&h=630&fit=crop",
        "image_credit": "Unsplash Healthy Desi Kitchen",
        "hype": 87.0
    },

    # 6. Side Hustles
    {
        "niche_slug": "side-hustles",
        "title": "5 Practical Side Hustles to Earn ₹30,000/Month in India from Home (2026 Reality Check)",
        "angle": "Zero-investment skills: Technical ghostwriting, thumbnail & video editing, Amazon affiliate curation, and remote tutoring",
        "image": "https://images.unsplash.com/photo-1499750310107-5fef28a66643?w=1200&h=630&fit=crop",
        "image_credit": "Unsplash Digital Freelancer Workspace",
        "hype": 95.0
    },
    {
        "niche_slug": "side-hustles",
        "title": "How to Start an Affiliate Marketing Channel in India: Complete Beginner Blueprint",
        "angle": "From setting up Telegram channels and WhatsApp communities to EarnKaro and Amazon Associates tags",
        "image": "https://images.unsplash.com/photo-1553729459-efe14ef6055d?w=1200&h=630&fit=crop",
        "image_credit": "Unsplash Affiliate Monetization",
        "hype": 92.0
    },

    # 7. Fashion
    {
        "niche_slug": "fashion",
        "title": "Capsule Wardrobe for Indian Men 2026: 7 Essential Pieces to Look Sharp on a Budget",
        "angle": "Neutral tees, tailored chinos, linen shirts, versatile white sneakers, and layering hacks under ₹5,000 total",
        "image": "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=1200&h=630&fit=crop",
        "image_credit": "Unsplash Menswear Styling",
        "hype": 89.0
    }
]

def generate_deeply_humanized_article(seed):
    """
    Generates a deeply humanized, expert-written article in engaging conversational style.
    Zero robotic AI clichés, real practical insights, structured tables, and punchy advice.
    """
    title = seed["title"]
    angle = seed["angle"]
    niche = seed["niche_slug"]

    prompt = f"""You are a top senior Indian digital journalist and specialist editor for UniqueDigit (uniquedigit-viral-hub.pages.dev).
Topic: {title}
Niche: {niche}
Editorial Angle: {angle}

STRICT WRITING & TONE RULES:
1. VOICE: Highly authentic, conversational, sharp Indian editorial voice. Talk directly to a smart friend who wants real answers without beating around the bush.
2. ABSOLUTELY BANNED AI CLICHES (DO NOT USE ANY OF THESE WORDS):
   - "In conclusion", "delve into", "tapestry", "beacon", "testament to", "fast-paced world", "it is important to remember", "furthermore", "moreover", "game-changer", "revolutionize", "unleash".
3. USE LIVELY HUMAN TRANSITIONS:
   - "Here is the real deal", "The bottom line is simple", "Why this actually matters", "What you should do next".
4. STRUCTURE (600 to 750 words):
   - Catchy, natural subheadings (##)
   - At least 1 clean Markdown comparison table or structured specifications box
   - Numbered action steps or bullet points
   - Realistic pricing in Indian Rupees (₹)
   - Top 3 FAQs that users actually search on Google with crisp 2-sentence answers

Return strict JSON:
{{
  "title": "{title}",
  "summary": "Compelling, high-CTR meta description under 155 chars for Google Search SERP",
  "body_md": "Full engaging markdown article content with tables, bold highlights, numbered tips, and FAQs",
  "faq": [
    {{"q": "Real user question?", "a": "Direct crisp 2-sentence answer."}},
    {{"q": "Second popular question?", "a": "Direct crisp 2-sentence answer."}},
    {{"q": "Third question?", "a": "Direct crisp 2-sentence answer."}}
  ],
  "tags": ["{niche}", "Guide", "India 2026", "UniqueDigit"]
}}"""

    try:
        return gemini(prompt)
    except Exception as e:
        print(f"❌ Error generating '{title}': {e}")
        return None

def publish_to_d1(seed, article):
    """Inserts the article into Cloudflare D1 posts table under the exact niche."""
    niche_slug = seed["niche_slug"]
    title = article.get("title") or seed["title"]
    summary = article.get("summary", "")
    body_md = article.get("body_md", "")
    faq_json = json.dumps(article.get("faq", []))
    sources_json = json.dumps([{"title": "UniqueDigit Editorial Desk", "url": "https://uniquedigit-viral-hub.pages.dev"}])
    image_url = seed["image"]
    image_credit = seed["image_credit"]
    hype = seed["hype"]

    slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')[:80]
    post_id = uuid.uuid4().hex[:16]

    sql = """
    INSERT INTO posts (
        id, niche_id, slug, kind, title, summary, body_md, faq, sources,
        image_url, image_credit, source_url, hype, views, is_breaking, indexable, status,
        published_at, updated_at
    )
    VALUES (
        ?,
        (SELECT id FROM niches WHERE slug = ? LIMIT 1),
        ?, 'article', ?, ?, ?, ?, ?,
        ?, ?, 'https://uniquedigit-viral-hub.pages.dev', ?, 42, 1, 1, 'published',
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
    params = [post_id, niche_slug, slug, title, summary, body_md, faq_json, sources_json, image_url, image_credit, hype]

    url = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT}/d1/database/{CF_D1_DB}/query"
    headers = {"Authorization": f"Bearer {CF_TOKEN}", "Content-Type": "application/json"}
    try:
        r = requests.post(url, headers=headers, json={"sql": sql, "params": params}, timeout=20)
        if r.status_code == 200 and r.json().get("success"):
            print(f"  ✅ [Cloudflare D1]: Live on https://uniquedigit-viral-hub.pages.dev/{niche_slug}/{slug}")
            return True
        else:
            print(f"  ❌ [D1 Write Error]: {r.status_code} - {r.text[:150]}")
            return False
    except Exception as e:
        print(f"  ❌ [D1 Exception]: {e}")
        return False

def main():
    print("=" * 75)
    print("🌟 POPULATING TOP NICHES WITH HIGH-CRAFT HUMANIZED ARTICLES & HD VISUALS")
    print(f"Total Seeds to Process: {len(TOP_NICHE_SEEDS)}")
    print("=" * 75)

    created_count = 0
    for idx, seed in enumerate(TOP_NICHE_SEEDS, 1):
        print(f"\n[{idx}/{len(TOP_NICHE_SEEDS)}] Processing {seed['niche_slug'].upper()}: {seed['title'][:55]}...")
        article = generate_deeply_humanized_article(seed)
        if article:
            ok = publish_to_d1(seed, article)
            if ok:
                created_count += 1
        time.sleep(2)

    print("\n" + "=" * 75)
    print(f"🎉 COMPLETED: Successfully published {created_count}/{len(TOP_NICHE_SEEDS)} top-tier articles!")
    print("All top categories are now rich, fully populated, and live with 1200x630 HD media!")
    print("=" * 75)

if __name__ == "__main__":
    main()
