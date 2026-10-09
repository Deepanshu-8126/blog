# 6 — PRD ADD-ON v2: Cloudflare-only + Hype Engine

> Yeh add-on PRD 1–5 ke **upar** lagta hai. Jo yahan likha hai wo v1 ko override karta hai; baaki v1 valid hai.

## 1. Decisions (final)
| # | Decision | Kyun |
|---|---|---|
| D1 | **Supabase hata do.** Sab kuch Cloudflare par: domain/DNS, hosting, database (**D1**), cache (**KV**), images (**R2**, optional), scheduler (**Cron Triggers**), security (WAF/Turnstile/Access) | Ek vendor, ek dashboard, ek bill, edge pe data user ke paas |
| D2 | **Pipeline Python → TypeScript Worker.** GitHub Actions ki zarurat nahi | Cron seedha Cloudflare mein; D1 ko binding se direct write |
| D3 | **Google Trends ka source badlo.** `pytrends` April 2025 mein archive ho gaya; official Trends API abhi sirf application-gated alpha hai (aur "trending now" cover nahi karta) | Primary: Google **Trending Now RSS** (`trends.google.com/trending/rss?geo=IN`) — Worker se fetch hota hai. Optional: paid scraper API / alpha access mil jaye to |
| D4 | **"Hype" = multi-signal score, sirf Google Trends nahi.** Google + News + Wikipedia + YouTube + HN + TMDB (+ optional X via Grok) | Ek source fragile hai (RSS mein per-geo sirf ~10–20 items); multi-source = reliable + corroboration |
| D5 | **Two-tier content:** Trend Board (live list, har topic) vs Articles (sirf jo threshold cross kare) | Thin-content/AdSense risk kam, speed zyada |
| D6 | Python pipeline.py (file 5) **deprecated**; schema v1 (Postgres) deprecated → `schema_d1.sql` | pytrends dead + Supabase out |

## 2. Goal (v2)
"**Jo abhi India mein hype ho raha hai, wo sabse pehle, sabse saaf, aur kamai ke saath.**"
- Trend detect hone ke **30 min ke andar** board pe.
- Board freshness ≤ 15 min.
- Har trend ke saath: hype score (real data), kyun trend ho raha hai (news links), related deal/tool (affiliate).

## 3. v1 se kya badla
| Area | v1 | v2 |
|---|---|---|
| DB | Supabase Postgres | Cloudflare D1 (SQLite) |
| Cache | Cloudflare edge (manual) | KV precomputed boards + edge cache |
| Pipeline | Python, GitHub Actions daily | TS Worker, Cron har 15 min / hourly / daily |
| Trends | pytrends | Trending-Now RSS + 5 aur signals |
| Images | hotlink | Allowlisted `/img` proxy (Wikipedia, TMDB) + edge cache; R2 optional |
| Admin | Supabase dashboard | `/admin` Cloudflare Access ke peeche (review queue) |
| Update rate | daily | board 15 min, articles on-threshold |

`src/lib/db.ts` ek hi file hai jahan DB touch hota hai → frontend migration = us file ka rewrite (function names same rahenge). Templates/components waise hi.

## 4. New functional requirements
| ID | Requirement | Pri |
|---|---|---|
| F13 | `/trending` live board: top 30 topics, hype meter, stage badge, sources, sparkline | P0 |
| F14 | Hype score engine (file 7) — har 15 min recompute, history store | P0 |
| F15 | Ingest workers: Google RSS, Google News RSS, Wikipedia pageviews, YouTube mostPopular, HN, TMDB | P0 |
| F16 | Entity merge (same topic alag naam se aaye to ek ho) | P0 |
| F17 | Publish gate: Trend Card (auto, noindex) → Article (hype threshold) | P0 |
| F18 | Safety gate: blocklist + AI classifier (tragedy/death/crime/adult/YMYL → no auto-publish) | P0 |
| F19 | Niche routing: topic → 12 niches ka best fit (AI), `niche_id` set | P0 |
| F20 | **Deal Radar**: trending topic ke tokens se `products` match → affiliate card inline | P1 |
| F21 | Home pe "Hype Today" strip + per-niche top-3 | P0 |
| F22 | `/api/trending` JSON (KV se, 60s cache) + client auto-refresh har 60s | P1 |
| F23 | Telegram channel auto-alert (hype ≥ 75, fresh) | P1 |
| F24 | Daily/weekly email digest cron (Resend/Brevo etc.) | P2 |
| F25 | Web push (OneSignal/native) for "Peak" alerts | P2 |
| F26 | Dynamic OG share images per trend | P2 |
| F27 | `/admin` (Cloudflare Access): drafts review, blocklist, source weights, kill-switch | P0 |
| F28 | Turnstile on newsletter, WAF rate limit on `/api/*` | P0 |
| F29 | Pipeline health alert (Telegram/email) jab cron fail ho | P0 |
| F30 | Data retention jobs (signals 7d, hype_history 30d) | P0 |

## 5. Hype → money map
| Trend type | Page | Earning |
|---|---|---|
| Product/phone/gadget launch | Card + Deal Radar | EarnKaro (Amazon/Flipkart etc.) |
| AI tool / app | Tools niche card | Affiliate / sponsored listing |
| Movie/OTT/Game | Movies/GTA6 | Ads + OTT/gear affiliate |
| Gold/market | Dataset page | Ads |
| Pure news/viral | Board only (+ short card) | Ads + newsletter growth |
| Tragedy/death/crime | **Skip** | — |

## 6. Success metrics
| Metric | Target |
|---|---|
| Detect→board latency | < 30 min |
| Board data age | ≤ 15 min p95 |
| Cron success rate | ≥ 98% |
| Topics promoted to articles / day | 10–30 (cap), not 100+ |
| Articles indexed / published | ≥ 70% (30 din baad) |
| Board → article CTR | ≥ 15% |
| Deal Radar CTR | ≥ 2% |
| Telegram subs (M3) | 1,000 |

## 7. Rules (v1 §7 + naye)
1. Hype/traffic numbers **sirf real** — Google ka `approx_traffic` ek *floor* hai ("200+" = at least 200), isko "exact searches" mat likho; "200+ searches" jaisa hi dikhao.
2. Cards `noindex,follow` jab tak promote na hon; sirf unique-value waale articles index hon.
3. Har trend page pe ≥ 2 independent source links (news publishers) — apna AI text sirf summary.
4. Health/finance/legal-sensitive trends → review queue, auto-publish nahi.
5. Real people (celebs) ke baare mein: sirf public, sourced facts; koi gossip/defamation/likeness claim nahi; images sirf Wikipedia/TMDB license ke saath.
6. Source terms: Wikimedia — User-Agent with contact; TMDB — attribution; YouTube API — ToS (quota, no re-hosting video); Reddit (agar use ho) — official OAuth API only.
7. Google RSS/unofficial endpoints ka SLA nahi — engine ko **graceful degrade** karna hai (ek source gira to baaki se chalo, board khali nahi).

## 8. Risks
| Risk | Mitigation |
|---|---|
| Google RSS format/limit change | Parser defensive + alert + paid scraper API fallback + other signals |
| Free plan limits (D1 reads 5M/day, writes 100k/day; 50 subrequests/invocation) | Precomputed KV boards, batch writes, retention, **Workers Paid** recommended for cron |
| AI wrong facts | Facts-only prompt + source links + review for sensitive |
| Trend ⟶ low-quality spam | Gate (hype≥55 & ≥2 sources), daily cap, noindex cards |
| Single-vendor lock-in | Data portable (D1 = SQLite export); schema plain SQL |
| Cloudflare cache + fresh data conflict | Board JSON short TTL (60s), articles longer (15m) |

## 9. Cost (rough; pricing pages se verify karo)
- Domain (Cloudflare Registrar) — at-cost.
- Pages + D1 + KV + R2: free tier mein shuru; limits file 8 mein.
- **Workers Paid plan** (≈ $5/month, verify) — cron + zyada subrequests ke liye recommended.
- Gemini/Grok/Workers AI — usage-based; cap env var se.
- YouTube Data API — free quota (key).

## 10. Out of scope (v2)
User accounts, comments, native app, Hindi full translation (v3), paid subscriptions.
