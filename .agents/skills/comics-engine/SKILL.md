---
name: comics-engine
description: Autonomous Anime, Manga, Webtoon, and Comic lore, recap, release radar, and AI comic strip generator with 100% fair-use compliance.
version: 1.0.0
---

# 💥 Comics & Manga Lore Engine Skill

Master operational guidelines for autonomous Manga, Anime, Webtoon, and Superhero lore publishing, zero-copyright legal compliance, and interactive visual craft.

## 1. Core Principles
- **100% Fair-Use Compliance**: Never re-upload raw manga scans or copyrighted comic panels. All content is strictly analytical commentary, recap critique, and original lore synthesis protected under Section 52(1)(a) Indian Copyright Act and US 17 U.S.C. § 107.
- **AI-Generated Stylized Imagery**: Every article uses original AI character art (Midjourney, FLUX, Gemini) or official CC-BY press media.
- **Engagement Multipliers**: Always include a Chapter Drop Countdown, Power Tier Matrix, and Spoiler Shield.

## 2. 4 Autonomous Pillars

| Pillar ID | Pillar Focus | Key Content Types |
| :--- | :--- | :--- |
| `recap` | Manga & Comic Recaps | Solo Leveling, One Piece, JJK, Marvel endings explained |
| `radar` | Chapter Drop Radar | Next chapter countdown, official MangaPlus/Viz drop dates |
| `lore` | Character Power Scaling | SSS-Tier power breakdowns, battle analysis, hax abilities |
| `strips` | AI Relatable Desi Webcomics | 3-panel relatable engineering, corporate & student life strips |

## 3. Standard Execution Workflow

1. **Query Ingestion**:
   - Harvest high-intent autocomplete queries (e.g. `solo leveling ragnarok ending explained`, `one piece chapter release date countdown`).
2. **AI Visual Generation**:
   - Construct cinematic prompt:
     `"Masterpiece digital comic illustration of [Character/Concept], dramatic lighting, high contrast ink lines, anime concept art, 4k resolution, 16:9 aspect ratio"`
3. **Structured Article Synthesis**:
   - **Position 0 Quick Answer**: 45-50 word crisp answer for Google Featured Snippets.
   - **Interactive Table of Contents**: H2 anchor jumps.
   - **Power Matrix / Lore Table**: Structured markdown table with stat comparisons.
   - **Official Source Links**: Link to official platforms (MangaPlus by Shueisha, Viz Media, Marvel Unlimited) as an authentic citation.
4. **Dual Syndication**:
   - Write to Cloudflare D1 `posts` table (`niche_id: comics`).
   - Ping IndexNow and sync to Google Blogger.
