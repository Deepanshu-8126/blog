# 📋 Task Plan: 12-Niche Media Architecture & Newsroom UI Overhaul

**PRD Reference:** [PRD_ARCHITECTURE.md](file:///d:/affi;ate/PRD_ARCHITECTURE.md)  
**Status:** In Execution (Phase 1 Locked)  
**Objective:** Evolve UniqueDigit into a world-class, multi-niche publication (The Verge × Bloomberg style) with 100% grounded news crawling, real editorial media, zero 404 breakages, and premium newsroom UI.

---

## Phase 1: Architecture & PRD Lock (Completed ✅)
- [x] **1.1** Define 12 dedicated niche harvester sources in [PRD_ARCHITECTURE.md](file:///d:/affi;ate/PRD_ARCHITECTURE.md).
- [x] **1.2** Design 4-Agent Quality Engine (Deduplication, Scrape-First, Grounded LLM, Media & SEO Guardrail).
- [x] **1.3** Wipe old test database to a clean slate (0 posts, schema intact).

---

## Phase 2: Newsroom UI & Navigation Modernization (Completed ✅)
- [x] **2.1** Rebuild `Header.astro` into a sleek, floating glass newsroom navbar (Bloomberg/The Verge aesthetic) with live telemetry pulse, active category indicators, search shortcut (Ctrl+K), and horizontal hub rail.
- [x] **2.2** Modernize typography & color tokens in `src/styles/global.css` (Obsidian slate glassmorphism, zero purple app styling).
- [x] **2.3** Upgrade `src/pages/index.astro` layout with a high-impact Lead Spotlight hero, 4-column editorial grid, and newsroom standby state.
- [x] **2.4** Production build verified (0 errors) & deployed to Cloudflare Pages.

---

## Phase 3: Niche-Specific Editorial Hubs & Reading Experience
- [ ] **3.1** Polish `src/pages/[niche].astro` dynamic hub templates so all 12 categories feel like distinct, world-class news sections.
- [ ] **3.2** Refine `src/pages/[niche]/[post].astro` article reading layout (clean bylines, responsive table of contents, verified source badges, reading progress indicator).
- [ ] **3.3** Verify zero 404 broken routes across all 18 niches and categories.

---

## Phase 4: Multi-Engine Pipeline & Agent Verification
- [ ] **4.1** Verify `pipeline.py` scrape-first engine with live real-time trend batches.
- [ ] **4.2** Confirm zero local JPGs, real 1200x630 editorial images, and valid JSON-LD schemas.

---

## Phase 5: Production Build, Testing & Cloudflare Deployment
- [ ] **5.1** Run `npm run build` to verify 0 SSR or TypeScript errors.
- [ ] **5.2** Deploy production bundle to Cloudflare Pages.
- [ ] **5.3** Commit all changes to GitHub `main`.

