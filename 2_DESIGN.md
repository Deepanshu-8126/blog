# DESIGN.md — 7 screenshots ka analysis + final design system

## A. Screenshot analysis (kya lena hai, kya nahi)

| # | Site | Style | **Lena hai** | **Nahi lena** |
|---|---|---|---|---|
| 1 | UniqueDigit mega menu | Purple header, white rounded card, 4 columns | **Header + More mega menu exactly** (icon circle gradient, title+subtitle rows, "NEW" chip, footer strip "View all categories") | "200+ guides added" jab tak real count na ho |
| 2 | Viral Editorial | Serif logo, green accent, whitespace | Numbered Trending list (01–05), featured hero with meta (author/read time), "Latest Stories" 3-col card grid, newsletter strip | Fake "92% open rate / 50k subs" stats |
| 3 | NewsHub | Red/navy news | Breaking ticker, hero + 3 latest cards, sidebar "Trending Now", **clearly labeled ad slot** ("ADVERTISEMENT") | "ECONOMY IN CRISIS" jaisi panic headlines |
| 4 | Viral Hub | Purple gradient hero, pastel niche cards | **Niche-color cards** (green/yellow/blue/pink) with "TRENDING +230K" chip, bottom "Trending Now" ticker bar, hero with CTA pair | "Taylor Swift / Netflix" copyrighted stills |
| 5 | Viral Now | Black + yellow, loud | Dark Trending sidebar, 5-card "Trending now" strip, Save/bookmark icon, newsletter box | ALL-CAPS clickbait, fake "12.4K watching", fake subscriber number |
| 6 | EduAI | Indigo, tool cards | **Tools template**: category sidebar with counts, tool card (badge + rating + "Try Now"), compare table, search bar | Fake reviews/ratings |
| 7 | HealthCare+ | Teal, medical | Article cards with read-time/date, **Symptom-style disclaimer line** | Fake doctors, "HIPAA", phone number, booking — hum clinic nahi hain |

**Final feel:** UniqueDigit purple shell (#1) + pastel niche colors (#4) + editorial reading comfort (#2) + tools grid (#6).

## B. Design tokens
```css
:root{
  --brand:#5B2FD0; --brand-dark:#3E1FA0; --brand-soft:#EFEAFD;
  --ink:#111827; --muted:#6B7280; --bg:#F6F5FB; --card:#FFFFFF; --line:#E8E6F0;
  --breaking:#E11D2E; --cta:#FFD21F; --cta-ink:#1A1A1A;
  /* niche group colors: chip + card bg */
  --tech:#2F80ED;      --tech-bg:#DCEFFB;
  --money:#D99A00;     --money-bg:#FFF1CC;
  --life:#1FA971;      --life-bg:#DDF5E7;
  --ent:#E0348B;       --ent-bg:#FDE1EE;
  --radius:16px; --radius-sm:10px; --shadow:0 8px 30px rgba(40,20,100,.10);
}
@media (prefers-color-scheme:dark){ :root{--bg:#0F0D1A;--card:#181528;--ink:#F3F2FA;--muted:#A4A0BC;--line:#2A2644} }
```
- Font: **Inter** (headings 800, body 400/500). Article body: Inter 17px/1.7 (ya Source Serif 4 optional).
- Scale: 12 / 14 / 16 / 20 / 28 / 40. Spacing 4-pt grid.
- Tailwind: tokens `tailwind.config` mein colors extend; `group` color DB ke `niches.grp` se map (Tech→tech, etc.).

## C. Components (ek baar banao, sab jagah reuse)
1. **Header** — logo "UniqueDigit / Viral Hub", links Home · AI Tools · Deals · PC Rig · Gaming (pinned niches: `niches.pin=true`), **More** button, search, bell, avatar.
2. **MegaMenu** — DB se `grp` ke hisaab se 4 columns; row = icon-circle + name + tagline + optional NEW chip; footer strip + "View all categories →". **Mobile:** full-screen sheet, accordion per group (4 columns mobile pe nahi chalega).
3. **BreakingTicker** — sirf tab dikhe jab last 3h mein post `is_breaking=true`. Auto-scroll, LIVE dot sirf real.
4. **HeroFeature** — gradient/image, niche chip, H1, 1-line summary, meta (read time, views real), 2 CTA.
5. **NicheCard** — pastel bg (group color), chip "TRENDING +230K" (trend_score), image, title, 2-line summary, footer stats.
6. **TrendingList** — numbered 01–05, title, views/time. Sidebar (desktop) / horizontal scroll (mobile).
7. **ToolCard / ProductCard** — image/logo, badge, name, 1-line, price/rating (sirf agar data real), **[Try Now / Buy]** button = `aff_url`, `rel="sponsored nofollow noopener"`.
8. **DatasetCard** — big number (e.g. ₹/10g), change %, line chart (history), city table.
9. **MovieCard** — TMDB poster 2:3, title, release date, trailer link, OTT note.
10. **AdSlot** — fixed min-height (CLS), label "ADVERTISEMENT", 3 positions only.
11. **NewsletterStrip**, **Footer** (legal links + affiliate disclosure), **DisclaimerBar** (niche.config.disclaimer).
12. **Breadcrumb** + **Related posts**.

## D. Page layouts (4 templates)
**Home `/`** — Header → (Breaking) → Hero (top trend #1) → "Trending Across Niches" (4 NicheCards, ek per group) → Trending Today list → Latest per group → Newsletter → Footer.

**feed** (health, fashion, food, side-hustles, gta-6, viral)
Hero (latest) → filter chips (tags) → card grid 3-col (1-col mobile) → sidebar Trending + AdSlot → pagination "Load more".

**tools** (ai-tools, pc-builds, deals, cashback)
Search bar → left category list with counts (desktop) / chips (mobile) → ToolCard grid 4-col → compare table → newsletter. Products `products` table se.

**dataset** (gold-rate)
DatasetCard (live rate) → chart 7d/30d → city table → explainer posts below → disclaimer + source link.

**movies**
Trending poster row → "Now trending" grid → each → post page (review/summary, trailer, where to watch) → affiliate (subscriptions/gear) only if relevant.

**Post page `/{niche}/{slug}`**
Breadcrumb → H1 → meta → hero image + credit → AdSlot → body → related ToolCards (same niche products) → FAQ → AdSlot → related posts → disclosure.

## E. Rules (galti design mein hi pakadne ke liye)
- Mobile 360px pe pehle design; desktop baad mein.
- Touch target ≥ 44px. Contrast ≥ 4.5:1 (yellow button pe dark text).
- Har image `width/height` + `loading=lazy` (hero eager) → CLS 0.
- Koi bhi hardcoded text list nahi: menu, cards, chips sab DB se.
- Empty state har template ke liye ("Abhi posts aa rahe hain…") — naya niche khaali dikhe to bhi crash na ho.
- Sab affiliate buttons ek component se → ek jagah rule change.
- Health pe: no urgency colors, no "cure" language; disclaimer sticky-top of article.
