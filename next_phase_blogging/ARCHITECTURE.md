# Multi-Agent Autonomous Architecture Specification

**Component:** Next Phase Autonomous Multi-Agent Governance Engine  
**Target Environment:** GitHub Actions (Python 3.11 Orchestrator) & Cloudflare Pages (Edge Runtime)  
**Document:** `next_phase_blogging/ARCHITECTURE.md`

---

## 1. Multi-Agent System Overview

To eliminate all content hallucinations, duplicate articles, low-resolution placeholders, and broken image cut-offs, the ingestion pipeline transitions from a monolithic script into a **Trio Agent Pipeline**:

```
 ┌────────────────────────────────────────────────────────────────────────┐
 │                      TRIO AGENT CONTROL ARCHITECTURE                   │
 ├───────────────────┬─────────────────────┬──────────────────────────────┤
 │  AGENT ALPHA      │    AGENT BETA       │       AGENT GAMMA            │
 │  (Quality & Dedupe│   (Editorial &      │   (Media & Aspect Ratio      │
 │   Guardian)       │    Monetization)    │    Quality Guardian)         │
 ├───────────────────┼─────────────────────┼──────────────────────────────┤
 │ • RSS Signal Ingest│ • Intent Archetype  │ • HEAD HTTP 200 Assertion    │
 │ • Levenshtein Dedupe│ • Humanized Story  │ • Aspect Ratio Class Tagging │
 │ • 20k Traffic Floor│ • Price Stacking Tab│ • Edge Proxy URL Formatting  │
 │ • Trend Safety Fil│ • Legal Disclaimer  │ • Fallback Redirect Injection│
 └───────────────────┴─────────────────────┴──────────────────────────────┘
```

---

## 2. Agent Breakdown & Functional Responsibilities

### 2.1. Agent Alpha: Quality & De-duplication Guardian (`agent_alpha_dedup.py`)

* **Objective:** Acts as the strict gatekeeper at the ingestion boundary. No duplicate, low-traffic, or inappropriate topic enters the pipeline.
* **Execution Flow:**
  1. **Signal Aggregation:** Collects candidate search queries from Google Trends RSS, Google News India RSS, and Box Office track feeds.
  2. **Database Cross-Reference:** Fetches recent 7-day topic slugs and canonical titles from Cloudflare D1:
     ```sql
     SELECT slug, canonical FROM topics WHERE first_seen > datetime('now', '-7 days');
     ```
  3. **Semantic Similarity Calculation:**
     * Computes Normalized Levenshtein Distance and token-set intersection against existing topics.
     * Threshold: If similarity score > `0.75`, the candidate topic is immediately dropped as a near-duplicate.
  4. **Traffic Floor Validation:**
     * Asserts query has an estimated traffic floor of at least `20K+` searches.
  5. **Safety Gatekeeper:**
     * Runs keyword safety checklist (blocks explicit adult queries, communal disharmony, sensitive tragedies).

---

### 2.2. Agent Beta: Editorial & Monetization Optimizer (`agent_beta_editorial.py`)

* **Objective:** Crafts engaging, factual, humanized editorial articles customized to the specific niche intent, embedding affiliate monetization blocks.
* **Execution Flow:**
  1. **Niche Intent Classification:**
     * Matches topic against the 5 primary archetypes:
       * **Healthcare/Wellness:** Generates PubMed/AYUSH-grounded health tips, pose checklists, dosage cautions, and certified health disclaimers.
       * **Cinema/OTT:** Generates box office collection matrix, spoiler-free plot stakes, OTT streaming platform, and audience verdict.
       * **E-Commerce/Deals:** Generates MRP vs Sale Price vs Bank Discount stacking comparison.
       * **Hardware/Tech:** Generates spec comparison tables, benchmark wattage, and buying guides.
       * **National Breaking:** Generates 3-bullet TL;DR digest, timeline of events, and verified citations.
  2. **LLM Invocation:** Calls Gemini 3.5 Flash Lite with strict JSON output schema.
  3. **Affiliate Link Embedding:** Automatically injects Amazon Associate tag (`uniquedigi0c6-21`) and merchant deep links.
  4. **Compliance Injection:** Appends FTC/India Consumer Protection legal disclaimers.

---

### 2.3. Agent Gamma: Visual & Media Quality Guardian (`agent_gamma_media.py`)

* **Objective:** Guarantees zero broken image icons, zero distorted/stretched aspect ratios, and instant edge proxying.
* **Execution Flow:**
  1. **Asset Discovery:**
     * Checks Google Trends RSS picture URL.
     * If empty, queries Wikipedia API for original unscaled Commons photos.
     * If still empty, assigns the dedicated `CATEGORY_FALLBACK_IMAGES[niche]` asset.
  2. **Pre-Flight HTTP Assertion:**
     * Performs a lightweight `requests.head(url, timeout=5)` with `UniqueDigitBot/2.0` User-Agent.
     * Asserts HTTP status `200` and `Content-Type: image/*`.
     * If any error, 404, or 429 occurs, replaces asset immediately with verified category fallback.
  3. **Aspect Ratio Analysis:**
     * Flags images as `ratio_portrait` (2:3 or 3:4), `ratio_square` (1:1), or `ratio_landscape` (16:9).
     * Injects appropriate container CSS tags into D1 metadata.
  4. **Edge Proxy Formatting:**
     * Encodes target URL into `/img?url=...` with immutable cache headers.

---

## 3. Cloudflare D1 Schema V2 Enhancements

To support multi-agent tagging and dedicated niche hubs, the `posts` table is enriched with the following schema fields:

```sql
-- Phase 2 Post Schema Enhancements
ALTER TABLE posts ADD COLUMN aspect_ratio TEXT DEFAULT 'ratio_landscape'; -- 'ratio_portrait' | 'ratio_landscape' | 'ratio_square'
ALTER TABLE posts ADD COLUMN verified_badge TEXT;                          -- 'AYUSH Verified' | 'TMDB Verified' | 'Price Glitch Verified'
ALTER TABLE posts ADD COLUMN tldr_bullets TEXT DEFAULT '[]';               -- JSON array of 3 summary bullets
ALTER TABLE posts ADD COLUMN comparison_table TEXT;                        -- JSON representation of spec/price comparison matrix
ALTER TABLE posts ADD COLUMN read_time_min INTEGER DEFAULT 3;
```

---

## 4. End-to-End Orchestration Pipeline

```python
# Conceptual Orchestration Loop (pipeline.py Phase 2)
def run_autonomous_orchestrator():
    # 1. Agent Alpha: Trend Discovery & Deduplication
    raw_candidates = fetch_all_signals()
    verified_candidates = AgentAlpha.deduplicate_and_filter(raw_candidates)
    
    for candidate in verified_candidates:
        # 2. Agent Beta: Editorial & Monetization Crafting
        article_payload = AgentBeta.write_grounded_article(candidate)
        
        # 3. Agent Gamma: Visual Verification & Media Tagging
        verified_media = AgentGamma.verify_and_proxy_asset(candidate, article_payload["niche_slug"])
        article_payload["image_url"] = verified_media["url"]
        article_payload["aspect_ratio"] = verified_media["aspect_ratio"]
        
        # 4. Persistence to Cloudflare D1
        d1_upsert_article(article_payload)
        
        # 5. Broadcast Telemetry
        send_telegram_notification(article_payload)
        
    # 6. Synchronize KV Boards
    sync_cloudflare_kv()
```
