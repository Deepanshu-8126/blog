# 📰 UniqueDigit Media Engine — Product Requirements Document (PRD) & Architecture

**Document Version:** 2.0 (Production Blueprint)  
**Target:** 12 Specialized Editorial Niches | Zero 404s | 1000% Fact Accuracy | High-Craft Modern UI  
**Design Standard:** The Verge × Bloomberg × TechCrunch Editorial Matrix  

---

## 1. Executive Summary & Objective

UniqueDigit is evolving from a generic automated aggregator into a **specialized, multi-engine editorial media publication**. 
Each of the 12 niches operates with its own dedicated crawling pipeline, domain-specific authority sources, strict fact-grounding, and bespoke UI layout.

### Core Non-Negotiables:
1. **100% Fact Accuracy:** LLM is never allowed to hallucinate from thin air. Every post is grounded in real source text scraped first.
2. **Real Editorial Media:** Every article features verified 1200x630 web media (`og:image`) or falls back to clean CSS gradient cards. Zero local dummy JPGs, zero generic Unsplash stock.
3. **Zero 404 Breakages:** Strict URL routing and schema consistency across all categories and article endpoints.
4. **Professional Newsroom Aesthetics:** Moving away from generic template layouts to a sleek, high-contrast, typography-first editorial experience with floating navigation, live breaking tickers, and distinct niche personalities.

---

## 2. The 12 Niche Pipeline Matrix

Each niche has a dedicated data harvester, domain authority sources, and specialized content archetypes:

| # | Niche | Slug | Primary Real Harvester Sources | Content Archetype & Key Deliverables |
|---|---|---|---|---|
| 1 | **Cricket & Sports** | `cricket-sports` | Cricbuzz, ESPN Cricinfo, Google Sports RSS | Match reports, live scores, player profiles, squad selections, pitch reports |
| 2 | **Cinema & OTT** | `movies` | TMDB, Box Office India, Bollywood Hungama, Google News | Box office collection tables, OTT release dates, trailer breakdowns, verdicts |
| 3 | **AI Tools & Software** | `ai-tools` | Hacker News, ProductHunt, GitHub Trending | Tool directory, pricing breakdown, pros/cons, developer use-cases, ratings |
| 4 | **PC Builds & Hardware** | `pc-builds` | Tom's Hardware, AnandTech, TechPowerUp | Component specs, India retail pricing, benchmark comparisons, PSU/wattage guidance |
| 5 | **Gold Rate & Bullion** | `gold-rate` | MCX India, IBJA, Live Bullion Indices | 24K vs 22K multi-city spot rates, BIS hallmarking guidelines, investment analysis |
| 6 | **Deals & Loot Drops** | `deals` | DesiDime, Amazon Price drops, Flipkart BBD | Deal cards, MRP vs steal price, bank card hacks, loot score, instant checkout links |
| 7 | **Cashback & Cards** | `cashback` | CardInsider, Bank Official Reward Portals | 5% flat cashback cards, lounge access comparisons, fee waivers, reward stacking |
| 8 | **Health & Wellness** | `health` | Ministry of AYUSH, PubMed clinical archives | Science-backed routines, yoga asanas, safe usage guidelines, strict medical disclaimers |
| 9 | **Food & Cuisine** | `food` | Regional culinary archives, food trends | Balanced Ayurvedic nutrition, regional thali breakdowns, authentic preparation notes |
| 10 | **Fashion & Lifestyle** | `fashion` | FDCI, Fashion Week trends, Vogue India | Handloom trends, festive style guides, fabric breakdowns, seasonal looks |
| 11 | **Exams & Results** | `exams-results` | SSC, UPSC, NTA, CBSE official circulars | Direct result checking steps, category cut-offs, merit lists, Tier-2 preparation roadmap |
| 12 | **Viral & Trending** | `viral` | Google Trends Realtime, Reddit (r/india, r/tech) | "Why is this buzzing?" explainers, timeline of events, verified public takeaways |

---

## 3. Autonomous 4-Agent Quality Engine

Before any article enters Cloudflare D1 or goes live, it passes through 4 specialized agents:

```
[Candidate Discovery]
        │
        ▼
┌───────────────────────────────────────────────┐
│ 1. Agent Alpha (Deduplication & Canonical)   │  → Rejects semantic duplicates (>70% overlap)
└───────────────────────┬───────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│ 2. Scraper Engine (Trafilatura + OG Extractor)│  → Scrapes primary source: text (2k+ chars) + og:image
└───────────────────────┬───────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│ 3. Agent Beta (Grounded LLM Rewrite)         │  → Writes fact-locked article grounded strictly in scraped text
└───────────────────────┬───────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│ 4. Agent Gamma (Media & SEO Guardrail)        │  → Verifies image is https://, formats FAQ & JSON-LD schema
└───────────────────────┬───────────────────────┘
                        │
                        ▼
             [D1 Remote Publication]
```

1. **Agent Alpha (Deduplication Gate):** Compares candidate title against existing database topics. Disallows identical or near-identical repeat stories.
2. **Scraper Engine (Scrape-First Protocol):** Opens the primary source webpage using `trafilatura` and regex meta parsers to grab real journalistic body text and editorial `og:image`.
3. **Agent Beta (Grounded Editorial Writer):** Injects scraped text directly into the prompt. Prohibits hallucinated claims and bans force-fitting student exam tips onto unrelated sports/tech topics.
4. **Agent Gamma (Media & SEO Validator):** Guarantees zero local JPGs, verifies image URL is live HTTPS, generates complete `NewsArticle` + `FAQPage` Schema, and verifies zero 404 links.

---

## 4. UI/UX Design System Specification (The Verge / Bloomberg Look)

### 4.1 Typography Scale (Inter / Outfit)
- **Breaking Kicker:** `11px`, font-weight `800`, uppercase, letter-spacing `0.08em`
- **Main Hero Headline:** `40px - 56px`, font-weight `900`, line-height `1.08`
- **Card Titles:** `17px - 20px`, font-weight `800`, line-height `1.25`
- **Body Text:** `16px - 17px`, font-weight `450`, line-height `1.75`
- **Meta Chips:** `12px`, font-weight `700`, uppercase tracking `0.04em`

### 4.2 Modern Newsroom Layout Architecture
1. **Master Editorial Header:**
   - Floating frosted glass bar (`backdrop-filter: blur(16px)`).
   - High-contrast geometric "UD Radar" brand mark.
   - Breaking news red pulse indicator.
   - Horizontal category strip with active pill indicators.
2. **Editorial Homepage Matrix:**
   - **Lead Spotlight Story:** Dominant editorial card with full-bleed high-res photo, read time, and hype meter.
   - **4-Column Newsroom Grid:** Clean cards with 16:9 images, category tags, and relative timestamps ("Updated 2h ago").
   - **Live Trending Bar:** Numbered ranking `#1` to `#5` with flame icons and search interest meters.
3. **Specialized Niche Hubs:**
   - `DealsHub`: Loot deal boxes with discount percentages and instant checkout buttons.
   - `DatasetHub`: Real-time gold rate calculator and multi-city bullion table.
   - `ToolsHub`: Instant search bar, category filters, and software pricing badges.
   - `MoviesHub`: Theatrical box office tracker table and OTT streaming badges.

---

## 5. Execution Roadmap

- [ ] **Phase 1: Architecture & PRD Lock** (Current Step)
- [ ] **Phase 2: Master UI & Navigation Overhaul** (Modern newsroom navbar, typography lock, floating glass header)
- [ ] **Phase 3: Category Hub Polish** (Elevating all 12 category templates to premium newsroom standards)
- [ ] **Phase 4: Multi-Engine Scraper & Pipeline Verification** (Running modular niche pipelines with 100% verified sources)
- [ ] **Phase 5: Production Build & Zero-Regression Verification** (Building Astro SSR bundle, verifying all routes, deploying to Cloudflare Pages)
