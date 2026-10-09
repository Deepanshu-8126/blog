# 8 — ARCHITECTURE v2 (Cloudflare-only)

## 1. Picture
```
                    ┌────────────── Cloudflare ──────────────┐
 Cron (15m/1h/daily)│                                          │
        │           │  Worker: uniquedigit-engine (TS)         │
        └──────────►│   ingest → resolve → score → gate →      │
                    │   write(D1) → publish boards(KV) → alerts│
                    │        │            │          │         │
                    │        ▼            ▼          ▼         │
                    │      D1 (SQL)     KV (boards)  R2 (opt)  │
                    │        ▲            ▲                    │
 Visitor ──► CDN ──►│  Pages: Astro SSR (uniquedigit.com)      │
            cache   │   /, /[niche], /[niche]/[post], /trending│
                    │   /api/trending  /api/subscribe  /img    │
                    │   /go/[id] (affiliate redirect+count)    │
                    │   /admin (Cloudflare Access)             │
                    └──────────────────────────────────────────┘
 External (read-only fetch): Google Trends RSS, Google News RSS, Wikimedia, YouTube API, HN, TMDB, Gemini, Grok
```
**Do deployables:** `web` (Pages) aur `engine` (Worker). Pages Functions mein cron trigger nahi hota → isliye engine alag Worker hai. Dono **same D1 + KV** se bind hote hain.

## 2. Service map
| Need | Cloudflare service | Kaam |
|---|---|---|
| Domain/DNS/SSL | Registrar + DNS | `uniquedigit.com` |
| Website | Pages (Astro SSR, `@astrojs/cloudflare`) | pages + API routes |
| Database | **D1** | niches, topics, signals, posts, products… |
| Fast reads | **KV** | precomputed boards, config, rate flags |
| Files | **R2** (optional) | OG images, mirrored images, backups |
| Scheduler | **Cron Triggers** (engine Worker) | ingest/score/daily |
| Protection | WAF rate limit, **Turnstile**, bot mode | `/api/*`, newsletter |
| Admin auth | **Cloudflare Access** | `/admin*` |
| Observability | Workers Logs | engine + web |
| (Phase 2) | Queues, Workers AI, Vectorize | fan-out, embeddings dedupe |

## 3. Limits jo design ko chalate hain (docs se verified; dobara check karte raho)
| Limit | Free | Paid | Design impact |
|---|---|---|---|
| D1 rows read / day | 5 M | 25 B/month incl. | Public pages **KV/edge cache** se; D1 sirf miss pe |
| D1 rows written / day | 100 k | 50 M/month incl. | Snapshot batch writes + retention; index writes bhi count hote hain |
| D1 DB size | 500 MB | 10 GB | Retention jobs (signals 7d, hype_history 30d) |
| Queries per Worker invocation | 50 | 1000 | Free pe engine ko `db.batch()` + chhote jobs; **Paid recommended** |
| KV reads / day | 100 k | 10 M/month incl. | Board JSON ek key; edge cache bhi |
| Cron CPU | — | docs: up to 15 min CPU per cron/queue invocation | Engine ek run mein sab nipta sakta hai (Paid) |

**Rule:** public traffic **kabhi D1 scan nahi karta**: `/trending`, home, niche front pages → KV/edge cached JSON. D1 reads sirf post page miss, search, admin.

## 4. Cron schedule (engine `wrangler.toml`)
```toml
name = "uniquedigit-engine"
main = "src/index.ts"
compatibility_date = "2024-11-01"
compatibility_flags = ["nodejs_compat"]

[triggers]
crons = ["*/15 * * * *", "7 * * * *", "30 0 * * *"]   # fast / hourly / daily (06:00 IST)

[[d1_databases]]
binding = "DB"
database_name = "uniquedigit"
database_id = "<from wrangler d1 create>"

[[kv_namespaces]]
binding = "KV"
id = "<from wrangler kv namespace create>"
```
`scheduled(event)` mein `event.cron` se job choose:
| Cron | Job |
|---|---|
| `*/15` | ingest(gtrends, youtube, hn) → resolve → score → gate → cards → KV boards |
| `7 *` | ingest(wiki velocity, gnews for top 30) → rescore → article promote check → Telegram alert |
| `30 0` | dataset fetch (gold), tmdb, retention deletes, affiliate fill, daily digest, health report |

Secrets: `wrangler secret put GEMINI_API_KEY | GROK_API_KEY | YT_API_KEY | TMDB_API_KEY | TELEGRAM_BOT_TOKEN | GOLD_API_KEY`.

## 5. Web app (Pages) — bindings
Pages project → Settings → Bindings: `DB` (D1), `KV`. Astro mein runtime: `Astro.locals.runtime.env.DB`.
```
src/lib/db.ts          D1 queries (same function names as v1 → templates untouched)
src/lib/kv.ts          getBoard(), getHome()
src/pages/trending.astro        live board (KV)
src/pages/api/trending.ts       JSON (KV) Cache-Control: s-maxage=60
src/pages/api/subscribe.ts      Turnstile verify → D1
src/pages/go/[id].ts            302 to aff_url, clicks+1 (waitUntil)
src/pages/img.ts                allowlist proxy (upload.wikimedia.org, image.tmdb.org) + Cache API
src/pages/admin/*.astro         review queue, blocklist, source weights, pause switch  (Access)
src/pages/sitemap.xml.ts        only posts.indexable=1
```

### db.ts migration (v1 → v2): function-by-function
| v1 (Supabase) | v2 (D1) |
|---|---|
| `getNiches` | `SELECT * FROM niches WHERE active=1 ORDER BY sort` (+ JSON.parse config/arrays) |
| `getPosts({tag,q})` | `posts` JOIN `niches`; tag → `JOIN post_tags`; q → `LIKE ?` (FTS5 later) ; limit+1 for hasNext |
| `getTrending` | KV `board:IN` (fallback D1 `ORDER BY hype DESC`) |
| `getPost` | `WHERE niche_id=? AND slug=? AND status='published'` |
| `getProducts` | `products WHERE niche_id=? AND active=1` |
| `getDatasets` | `datasets` last N, JSON.parse |
| `getBreaking` | `posts WHERE is_breaking=1 AND published_at > now-3h` |
| `.contains('tags')` | `post_tags` join |
| arrays | JSON text → parse in a `row()` helper |

## 6. KV keys
| Key | Value | Writer | TTL |
|---|---|---|---|
| `board:IN` | JSON top 30 topics `{id,title,slug,hype,stage,n,sources[],spark[],niche,post?}` | engine */15 | none (overwritten) |
| `board:IN:{niche}` | top 10 per niche | engine | none |
| `home:v1` | hero + per-group cards | engine | none |
| `cfg:engine` | `{paused:false, caps:{cards:60,articles:30}}` | admin | none |
| `rl:{ip}:{min}` | rate counters (if needed beyond WAF) | web | 120s |

## 7. Caching
- HTML pages: `Cache-Control: public, s-maxage=300, stale-while-revalidate=3600` (post pages 900).
- `/trending`: s-maxage 120 + client JS poll `/api/trending` (s-maxage 60) → effectively ≤ 2 min stale.
- Cloudflare dynamic HTML ko default cache nahi karta → **Cache Rule**: "Cache eligible + respect origin headers" for `/*` except `/admin*`, `/api/subscribe`, `/go/*`.
- Images: `/img` → `Cache-Control: public, max-age=31536000, immutable`.

## 8. Security
- `/admin*` Cloudflare Access (email OTP / Google SSO) — app code mein bhi `Cf-Access-Jwt-Assertion` verify.
- Turnstile on newsletter; WAF rate limit `/api/*` (e.g. 30 req/min/IP).
- `/img` open proxy na bane: **hostname allowlist + size cap + content-type image/** only.
- Secrets sirf `wrangler secret`/Pages env; D1 queries hamesha `.bind()` (no string concat).
- Markdown render: raw HTML strip (AI output untrusted).
- CSP header: script-src self + AdSense domains (jab ads on ho).
- Affiliate links: `rel="sponsored nofollow noopener"`.
- Backups: weekly `wrangler d1 export` → R2 (daily cron); D1 Time Travel (free plan par 7 din) bhi hai.

## 9. Observability & alerts
- `pipeline_runs` har job ka row; 3 consecutive fail → Telegram "engine down".
- Daily health report: sources ok/fail, topics tracked, cards/articles made, KV board age.
- `/admin/health` page: same data.

## 10. Repo layout (monorepo)
```
uniquedigit/
  web/        Astro (Pages)         wrangler.toml (pages) + src/
  engine/     Worker (TS)           wrangler.toml + src/{index,sources/*,resolve,score,gate,write,ai,telegram}.ts
  db/         schema_d1.sql, migrations/0001_*.sql
  docs/       1..10 md
  .github/    (optional) CI: typecheck + wrangler deploy on push
```
Deploy: `wrangler deploy` (engine), Pages Git integration (web). Migrations: numbered SQL files, `wrangler d1 migrations apply`.

## 11. Engine module contract
```ts
interface Raw { source:string; term:string; value?:number; rank?:number; url?:string; meta?:any }
interface Source { key:string; fetch(env):Promise<Raw[]> }        // add new source = 1 file + 1 row in `sources`
resolve(raw[]) -> topicId[]     score(topicIds) -> {hype,growth,stage,n}
gate(topic) -> 'ignore'|'board'|'card'|'article'
write(): D1 batch + KV put
```
Naya signal add karna = file + `sources` row; naya niche = `niches` row (v1 jaisa auto-sync).

## 12. Cost/usage estimate (per day, 15-min cadence)
- Ingest ≈ 96 runs × ~4 fetches; scoring reads ≈ topics(≤300) × snapshots → batched.
- Signal writes ≈ 96 × ~60 = ~5–6k rows (+ index rows) → free write cap (100k) mein.
- Public reads: KV/edge → D1 reads negligible.
- AI calls: cards ≤ 60 + articles ≤ 30 + classifier ≈ ~150/day (Gemini Flash level cost).
