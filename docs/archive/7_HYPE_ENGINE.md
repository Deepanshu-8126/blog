# 7 — HYPE ENGINE (trending kaise hoga)

Idea: ek signal pe bharosa nahi. **Kai sources ka "kitna tez badh raha hai" + "kitne sources ek saath bol rahe hain"** = hype.

## 1. Signals (sab Cloudflare Worker se `fetch()` ho sakte hain)
| Key | Source | Kya milta hai | Cadence | Auth | Notes |
|---|---|---|---|---|---|
| `gtrends` | `https://trends.google.com/trending/rss?geo=IN` | ~10–20 trending searches, `approx_traffic` (floor, jaise "200K+"), pubDate, related news links | 15 min | none | Unofficial-public feed; format badal sakta hai. Multi-geo: IN primary, US/GB optional |
| `gnews` | `https://news.google.com/rss/search?q=<topic>&hl=en-IN&gl=IN&ceid=IN:en` | Topic ke liye last-6h articles, distinct publishers | 30 min, sirf top candidates | none | "News velocity" + source links |
| `wiki` | Wikimedia Pageviews API (`/metrics/pageviews/top/...` aur `per-article/...`) | Daily top articles + article ka 7d baseline | hourly/daily | none (User-Agent zaroori) | Velocity = aaj vs 7d avg. Image + summary bhi yahin se |
| `youtube` | YouTube Data API `videos?chart=mostPopular&regionCode=IN` | Top videos, views, publish time | 30 min | API key | Entertainment/viral ke liye. Quota dekhte raho |
| `hn` | `hacker-news.firebaseio.com/v0/topstories` + items | Tech/AI points, comments | 30 min | none | Tech/AI Tools niche ke liye |
| `tmdb` | TMDB `/trending/movie/day` | Movies trending | 6 hr | key | Poster + attribution |
| `social` (optional) | xAI/Grok live search / X pulse | "X pe kya chal raha" ka summary | hourly | key | Provider features change hote hain — optional, fail ho to ignore |
| `interest` (optional) | Paid Trends scraper API / alpha API | Interest-over-time (0–100) | daily, top 10 only | key | Sirf sparkline/validation ke liye; core engine isse independent |

**Source registry D1 `sources` table mein** (key, weight, enabled, interval_min) → admin se on/off, naya source = row + ek fetcher function.

## 2. Pipeline (har 15 min)
```
 ingest(all due sources)              → raw items [{source, term, value, rank, url, ts}]
 normalize(term)                      → lower, strip punctuation/emoji, collapse spaces
 resolve entity (merge)               → topic_id (existing or new)
 insert signal snapshot               → signals table
 score(topic)                         → hype, velocity, stage
 gate(topic)                          → ignore | track | card | article
 write boards                         → KV board:IN, board:IN:{niche}, home:v1
 housekeeping                         → retention deletes (daily)
```

## 3. Entity resolution (same topic ko ek karna)
"Ind vs Aus", "India vs Australia live score", "IND v AUS" → ek topic.
1. `norm()` : lowercase, remove stopwords (live, score, news, today, vs/v → "vs", update, price…), sort tokens.
2. Candidate match: pehle exact `canonical_key`; phir **token Jaccard ≥ 0.6** against topics seen in last 48h.
3. (Phase 2) embeddings: Workers AI embedding + Vectorize cosine ≥ 0.85 for hard cases (model name Cloudflare docs se verify karo).
4. Merge karne par `topics.merged_into` set, signals re-point.
5. Canonical title = sabse zyada sources/most frequent form; Wikipedia match mil jaye to Wikipedia title.

## 4. Scoring (explainable, tunable)
Har topic `t`, har source `s` ke liye latest snapshot:

- `p_s` = **percentile rank** of value within that source's last-24h items (0–1) → scale-free.
- `g_s` = **growth** vs 3–6h pehle: `(v_now − v_prev) / max(v_prev, floor_s)`; `u_s = sigmoid(2·g_s)` (0–1). Naya topic (no prev) → `u_s = 0.75` (new = rising).
- `a_s = 0.6·p_s + 0.4·u_s`
- `base = Σ_s w_s · a_s`  (weights sum 1; default: gtrends .30, gnews .20, wiki .15, youtube .10, hn .08, tmdb .05, social .12)
- `n` = distinct sources with `a_s ≥ 0.3`; `corro = min(2, 1 + 0.25·(n − 1))`
- `age_h` = hours since `first_seen`; `fresh = exp(−max(0, age_h − 6)/18)` (6h tak full, phir decay)
- **`hype = clamp(100 · base · corro · fresh, 0, 100)`**

Weights agar kisi source ka data na aaye → baaki weights renormalize (graceful degrade).

### Stage (badge)
| Stage | Rule | UI |
|---|---|---|
| 🌱 Emerging | hype 25–55 aur growth > 0, n ≤ 1 | "Rising" |
| 🔥 Hot | hype ≥ 55 aur n ≥ 2 | "Hot" |
| 🚀 Peak | hype ≥ 75, growth ≈ flat (|g| < 0.1) | "Peaking" |
| 🧊 Cooling | growth < −0.2 do snapshots lagataar | "Cooling" |
| ⚫ Gone | 24h koi signal nahi | board se hata |

## 5. Gates (quality + safety)
```
if blocklisted(term) or safety_flag in (tragedy, death, crime_victim, adult, hate) → status=ignored
elif hype < 25                          → track only (board mein nahi)
elif 25 ≤ hype < 55 or n < 2            → board entry, no page
elif hype ≥ 55 and n ≥ 2                → create Trend Card (auto, noindex, ≤200 words, sources)
elif hype ≥ 70 for ≥ 3 snapshots or card traffic high → promote to Article (index)
sensitive (health/finance/legal) → draft + admin review (never auto-publish)
daily cap: cards ≤ 60, articles ≤ 30 (env)
```
**Safety classifier** (Gemini/Workers AI, JSON out): `{category, sensitive, safe_to_monetize, niche_slug, intent: news|buy|learn, affiliate_fit 0-1}`. Prompt mein strict: unknown → `safe_to_monetize=false`.

## 6. Card vs Article
| | Trend Card | Article |
|---|---|---|
| Trigger | hype ≥ 55 & n ≥ 2 | hype ≥ 70 sustained / manual promote |
| Length | 120–200 words | 400–700 words |
| Input | RSS news titles+links, Wikipedia extract, signal numbers | + more news, FAQ, related products |
| Index | `noindex,follow` | indexable, in sitemap |
| Latency | < 15 min | 1–6 h |
| Purpose | speed, board engagement | SEO + earning |

Prompt rules (dono): sirf diye gaye facts; koi invented number/quote/date; source list end mein; neutral tone; clickbait nahi; real person pe sirf sourced public info.

## 7. Deal Radar (earning)
Topic tokens vs `products(name, tags)` — LIKE/FTS match; top 3 → inline cards ("Trending: iPhone 17 — dekho deals"). Agar match nahi, niche ke top products fallback. Click = `aff_url`, `rel="sponsored nofollow"`. Track clicks via `/go/{id}` redirect Worker (D1 `clicks` count) — apna CTR data mile.

## 8. Anti-gaming / reliability
- Google RSS ka `approx_traffic` floor hai — percentile ke liye use karo, absolute claim mat karo.
- Single-source spikes (n=1) kabhi 55 se upar nahi jate (corroboration gate).
- Source down → `pipeline_runs` mein warn, weights renormalize, board chalta rahe.
- Duplicate cards roko: `unique(topic_id, kind)`.
- Admin kill-switch: `config` KV `engine:paused=1` → ingest chalta, publishing band.

## 9. Evaluate (1–2 hafte)
Backtest: apne snapshots ko Google Trends UI/Search Console ke saath compare karo — kya hamare "Hot" topics ne 24h mein traffic diya? Weights tune karo (`sources.weight`). Metric: precision@10 of "Hot" (ground truth = topic ne 24h mein Search Console impressions/hamari clicks di).
