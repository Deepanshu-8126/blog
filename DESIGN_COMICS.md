# 💥 Comics, Manga & Anime Lore — Design System Specification (DESIGN.md)

This document serves as the single source of truth for the **Comics, Manga & Superhero Lore** vertical within the UniqueDigit platform, designed according to `/design-system`, `/design-md`, and `/banner-design` protocols.

---

## 1. Brand Identity & Art Direction

- **Archetype**: Neo-Cyber Manga / Comic Con Dark Mode
- **Mood**: Electric, high-octane, immersive, editorial, 100% authentic fan-first
- **Target Audience**: Anime fans, manga readers, Marvel/DC enthusiasts, webtoon/manhwa communities in India & globally

---

## 2. Token Architecture (Three-Layer Hierarchy)

### Primitive Tokens
```css
/* Color Palette */
--color-obsidian-950: #0a0c10;
--color-slate-900: #0f172a;
--color-slate-800: #1e293b;
--color-neon-purple-500: #a855f7;
--color-neon-purple-600: #9333ea;
--color-cyber-red-500: #ef4444;
--color-electric-amber-400: #fbbf24;
--color-manga-cyan-400: #22d3ee;
--color-pure-white: #ffffff;

/* Spacing & Radii */
--radius-card: 20px;
--radius-badge: 9999px;
--radius-panel: 24px;
```

### Semantic Tokens
```css
--surface-canvas: var(--color-obsidian-950);
--surface-card: var(--color-slate-900);
--surface-card-border: rgba(168, 85, 247, 0.25);
--accent-primary: var(--color-neon-purple-500);
--accent-warning-spoiler: var(--color-cyber-red-500);
--accent-tier-god: var(--color-electric-amber-400);
--accent-verified: var(--color-manga-cyan-400);
--text-primary: var(--color-pure-white);
--text-muted: #94a3b8;
```

### Component Tokens
```css
--tier-card-bg: linear-gradient(135deg, rgba(168, 85, 247, 0.12) 0%, rgba(15, 23, 42, 0.95) 100%);
--countdown-badge-bg: rgba(239, 68, 68, 0.15);
--countdown-badge-border: rgba(239, 68, 68, 0.4);
--spoiler-box-bg: rgba(239, 68, 68, 0.08);
```

---

## 3. Typography Hierarchy

- **Hero Headlines**: Display Sans (`Outfit`, `Syne`, or `Cabinet Grotesk`), 800-900 Black weight, tight tracking (`-0.03em`).
- **Body Content**: Clean Reading Serif/Sans (`Inter`, `-apple-system`), 1.8 line-height for effortless long-form lore consumption.
- **Data & Stats**: Monospace (`JetBrains Mono`, `Roboto Mono`) for Chapter numbers, Power scale ratings, and countdown timers.

---

## 4. Banner & Hero Visual Standards (`/banner-design`)

- **Aspect Ratio**: 16:9 (1200 x 675 px) for primary Google Discover, and 1.91:1 (1200 x 628 px) for OpenGraph social cards.
- **Safe Zone**: Keep character focal point and title typography within the central 70% safe zone.
- **Visual Composition**:
  - Dramatic dynamic angle (rule of thirds).
  - High-contrast edge backlighting (Purple / Cyan / Crimson rim glow).
  - Zero stock-photo feel: Always stylized anime illustration / comic panel aesthetic.

---

## 5. Specialized Component Specifications

1. **Chapter Drop Countdown (`<ComicCountdown />`)**:
   - Live real-time countdown badge indicating Days, Hours, Mins until raw scan / official MangaPlus release.
2. **Power Level Tier List (`<PowerTierList />`)**:
   - Rank categories: SSS-Tier (God), SS-Tier (Universal), S-Tier (Continental), A-Tier (Commander).
   - Dynamic power rating bar out of 100 with stat breakdown (Attack, Speed, Hax/Abilities).
3. **Spoiler Shield Alert**:
   - Collapsible spoiler accordion preventing accidental plot reveals for anime-only fans.
