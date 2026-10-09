# 9 — DESIGN ADD-ON: Hype UI

Base design = file 2. Yahan sirf naye components/pages.

## 1. Naye components
| Component | Spec |
|---|---|
| **HypeMeter** | Pill/bar 0–100. Colors: <25 grey, 25–54 amber, 55–74 orange `🔥`, ≥75 red `🚀`. Number + label ("Hot"). `aria-label="Hype 82 out of 100"` |
| **StageBadge** | 🌱 Emerging · 🔥 Hot · 🚀 Peaking · 🧊 Cooling (text + icon, sirf colour par depend nahi) |
| **SourceDots** | Chhote chips: `Google` `News` `Wiki` `YouTube` `HN` — kaun-kaun se sources confirm kar rahe. Tap = tooltip |
| **Sparkline** | Inline SVG, last 24h `hype_history` (server-side computed polyline, JS nahi) |
| **TrendRow** | `01` rank · title · StageBadge · HypeMeter · SourceDots · sparkline · "Read →" (agar post hai) · "Deals →" (agar match) |
| **TrendCard (post)** | Chhota page: H1, hype header strip, 3–4 line summary, "Kyun trend ho raha hai" (news links), related deals, source list |
| **FreshnessStamp** | "Updated 4 min ago" (`updated_at` real; >30 min ho to amber "delayed") |
| **LiveDot** | Green dot sirf jab data age ≤ 15 min; warna nahi dikhana (fake LIVE nahi) |
| **DealRadarCard** | ToolCard variant + "Trending" chip |
| **TelegramCTA** | "Alerts chahiye? Telegram join karo" (sticky bottom on mobile, dismissible) |

## 2. `/trending` page
```
[Header]
H1 "Abhi kya trend ho raha hai (India)"   FreshnessStamp  LiveDot
Filter chips: All | Tech | Money | Lifestyle | Entertainment   (client-side filter on same JSON)
[TrendRow × 30]   (mobile: 2-line card layout)
AdSlot (after row 5), AdSlot (after row 15)
Newsletter + TelegramCTA
```
- Data: server render from KV `board:IN`; client JS har 60s `/api/trending` se refresh (diff update, scroll na jumpe).
- Empty/error: "Data refresh ho raha hai…" + last known board (stale OK, "delayed" tag).
- Mobile: TrendRow = rank + title (2 lines) / meter + badge / sources; sparkline hide <380px.
- Filter chips ka count = real.

## 3. Home changes
1. **Hype Today strip** (hero ke neeche): top 5 TrendRow-compact, "See all →" `/trending`.
2. Hero = top **article** (indexable), card nahi.
3. Niche cards mein "🔥 +hype" chip real hype se.
4. BreakingTicker = `is_breaking` (hype ≥ 85 aur n ≥ 3) — auto, 3h expiry.

## 4. Niche pages
Feed/Tools/Movies/Dataset ke upar **"Trending in {niche}"** (top 3 from `board:IN:{niche}`) — khaali ho to hide.

## 5. Post page (Trend Card vs Article)
- Card: top pe HypeMeter + FreshnessStamp; body short; "Sources" list; "Full explainer aa raha hai" **sirf agar** promote queue mein ho (warna mat dikhao).
- Article: v1 post page + HypeMeter strip + related TrendRows (same niche).
- Dono: Deal Radar block, affiliate disclosure, ad slots, JSON-LD (Article/NewsArticle — sirf articles), `noindex` cards.

## 6. `/admin` (Cloudflare Access, desktop-first, simple tables)
- **Review queue:** drafts (health etc.) — Preview, Edit, Publish, Reject.
- **Topics:** last 100, hype, status, force promote/ignore, add blocklist term.
- **Sources:** enable/disable, weight sliders, last_run/last_ok.
- **Engine:** pause switch, caps.
- **Health:** pipeline_runs last 50, board age.

## 7. Rules
- Koi bhi number real data se; "approx traffic" ko "200K+ searches" format mein (floor) dikhao.
- Colors ke saath icon/text (accessibility).
- Sparkline ke liye minimum 3 points, warna "New" chip.
- Animations minimal (prefers-reduced-motion respect).
- CLS: TrendRow fixed height; JS refresh sirf content swap.
- Hindi/Hinglish microcopy theek hai, titles English (search intent).
