# 📋 Task Plan: Comprehensive UI/UX Design System Overhaul & 100+ Flaw Resolution

**Created:** 2026-10-09  
**Status:** In Execution  
**Objective:** Complete design transformation of UniqueDigit into a world-class, premium intelligence hub with distinct niche personalities, sleek vector branding, unified design tokens, and resolution of all UI/UX deficiencies.

---

## Phase 1: Comprehensive UI/UX Audit & Architecture (Current)
- [x] **1.1** Conduct full-spectrum audit of 100+ UI/UX flaws across all views (documented in `findings.md`).
- [ ] **1.2** Architect unified Design System tokens in `src/styles/global.css` (HSL semantic scales, elevation layers, glassmorphism, typography rhythm).
- [ ] **1.3** Establish Niche Persona styling rules (Dark Cyberpunk for Gaming/GTA-6, Bullion Gold for Gold Rate, Silicon Minimal for AI Tools, Emerald Deal Matrix for Deals & Cashback).

---

## Phase 2: Brand Identity & Master Navigation Overhaul
- [ ] **2.1** Design modern SVG Vector Brand Insignia (replacing generic box logo with precision geometric "UD" Radar Monogram).
- [ ] **2.2** Rebuild `Header.astro` with premium floating glassmorphism, active indicator pills, smooth search trigger, and distinct group accents.
- [ ] **2.3** Refactor `MegaMenu.astro` with rich preview cards, category icons, and high-contrast typography.
- [ ] **2.4** Modernize Mobile Bottom Sheet and sticky thumb navigation.

---

## Phase 3: Specialized Niche Vibe & Hub Templates
- [ ] **3.1** Overhaul `gta-6` and Gaming UI with custom dark/neon esports telemetry cards, benchmark badges, and high-impact visual design.
- [ ] **3.2** Overhaul `gold-rate` UI with live bullion ticker, interactive city price comparator, and hallmark authenticity badges.
- [ ] **3.3** Overhaul `ai-tools` and `pc-builds` (`Tools.astro`) with real-time instant JavaScript search/filter, category pills, and clean specs grid.
- [ ] **3.4** Overhaul `movies` (`Movies.astro`) with modern OTT streaming platform badges, cinema poster cards, and watchlist filters.
- [ ] **3.5** Overhaul `health`, `food`, `fashion`, `side-hustles` (`Feed.astro`) with contextual reading tags, author fact-check badges, and clean editorial cards.

---

## Phase 4: Core Components & Reading Experience
- [ ] **4.1** Upgrade `NicheCard.astro` with subtle micro-interactions, standardized image aspect ratios, elevation hover states, and clear typography.
- [ ] **4.2** Upgrade `TrendRow.astro` with rank glow badges (#1 gold, #2 silver, #3 bronze), live traffic pills, and responsive action triggers.
- [ ] **4.3** Redesign `AmazonDealBox.astro` into a high-trust shopping module with live discount highlights, merchant tags, and verified store badges.
- [ ] **4.4** Enhance `[post].astro` article reading experience with reading progress bar, estimated read time, table of contents, and refined typography.

---

## Phase 5: Verification, Build & Deployment
- [ ] **5.1** Run full TypeScript & Astro production build check (`npm run build`).
- [ ] **5.2** Verify all 12 category routes and article pages live.
- [ ] **5.3** Deploy live to Cloudflare Pages and commit all changes to Git.
