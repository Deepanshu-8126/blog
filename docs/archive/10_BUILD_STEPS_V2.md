# 10 — BUILD STEPS v2 (Cloudflare-only) — ek-ek step

Rule: har phase ka "Done when" pass hone par hi agla. File 4 (v1 steps) ke jo phases Supabase se jude the wo **replace** hain.

## Phase A — Cloudflare setup (45 min)
1. Cloudflare account; domain `uniquedigit.com` add/transfer (DNS Cloudflare par).
2. `npm i -g wrangler` → `wrangler login`.
3. `wrangler d1 create uniquedigit` → `database_id` note.
4. `wrangler kv namespace create KV` → id note.
5. (Optional) `wrangler r2 bucket create uniquedigit-assets`.
6. Keys: Gemini, Grok(xAI), YouTube Data API, TMDB, Telegram bot (BotFather), gold API.
7. Workers **Paid** plan on karo (cron + subrequest headroom).
**Done when:** `wrangler d1 list` mein DB dikhe; keys password manager mein.

## Phase B — Database
1. `wrangler d1 execute uniquedigit --remote --file=schema_d1.sql`
2. Verify: `wrangler d1 execute uniquedigit --remote --command "select slug from niches order by sort"` → 12 rows.
3. `affiliate_rules` mein EarnKaro template (dashboard se verify), `blocklist` extend.
**Done when:** 12 niches + 7 sources + blocklist rows present.

## Phase C — Engine v0 (sirf Google RSS) 
1. `engine/` Worker scaffold (`wrangler init`), bindings DB+KV, secrets.
2. `sources/gtrends.ts`: fetch `https://trends.google.com/trending/rss?geo=IN`, parse XML (title, `ht:approx_traffic`, pubDate, news items), defensive (try/catch, empty ok).
3. `resolve.ts` (norm + Jaccard), `write.ts` (topics + signals via `DB.batch`).
4. `wrangler dev --test-scheduled` → `curl "localhost:8787/__scheduled?cron=*/15+*+*+*+*"`.
**Done when:** 1 run mein ≥ 8 topics + signals D1 mein; dobara run → duplicate topics nahi (signals add hon).

## Phase D — Multi-source + scoring
1. Add `youtube`, `hn`, `wiki` (top + velocity), `gnews` (top candidates only), `tmdb`.
2. `score.ts` (file 7 §4), `hype_history` insert, stages.
3. Source fail simulate (galat key) → engine chalta rahe, weights renormalize.
4. Unit tests: norm/Jaccard, score (known inputs → known hype), gate thresholds.
**Done when:** 24h chalao; top-10 board manually dekho — bakwaas items < 2; ek source band karne par bhi board banta hai.

## Phase E — Gates + AI
1. `ai.ts`: Gemini classifier (JSON) + card writer + article writer (facts-only prompt, sources list).
2. Blocklist + safety gate; sensitive niches → `draft`.
3. Caps (cards/articles per day) from KV `cfg:engine`.
4. Wikipedia fetch for image+extract (User-Agent with contact); TMDB poster (attribution).
5. Deal Radar matcher (`products.keywords`).
**Done when:** 10 cards + 3 articles padh ke: koi invented stat/quote nahi, sources links sahi, tragedy topic skip hua (test term se).

## Phase F — Boards to KV
1. `write.ts` → `board:IN`, `board:IN:{niche}`, `home:v1`.
2. Retention job (daily): `DELETE FROM signals WHERE captured_at < now-7d` etc.
**Done when:** KV mein board 15 min ke andar refresh hota hai (`wrangler kv key get board:IN --binding KV --remote`).

## Phase G — Web (Astro on Pages)
1. v1 project (components/layout already built) lo; `src/lib/db.ts` ko D1 version se replace (file 8 §5 table). Supabase dependency hatao.
2. `trending.astro`, `api/trending.ts`, `/img`, `/go/[id]`, `api/subscribe.ts` (+Turnstile), sitemap (indexable only).
3. Templates v1: Feed/Tools/Dataset/Movies + HypeMeter/TrendRow/Sparkline components (file 9).
4. Pages project connect (Git), bindings DB+KV, env vars.
**Done when:** 12 niche URLs + `/trending` + post page live; v1 DB references zero (`grep -ri supabase`).

## Phase H — Cache + Security
1. Cache Rule (respect origin, exclude admin/api/go).
2. WAF rate limit `/api/*`; Turnstile keys; CSP.
3. `/admin` + Cloudflare Access policy (sirf tera email).
**Done when:** `curl -I` pe `cf-cache-status: HIT` (second request); admin bina login 302/403; newsletter bot-test fail.

## Phase I — Automation + Alerts
1. Engine deploy (`wrangler deploy`), crons confirm in dashboard.
2. Telegram alert (hype ≥ 75 fresh), health alert (3 fails).
3. Weekly D1 export → R2.
**Done when:** 48h bina haath lagaye board chalta rahe; ek jaan-boojh kar fail pe Telegram alert aaye.

## Phase J — Growth + Money
1. Legal pages, Search Console, sitemap submit, Bing.
2. Telegram channel public; share buttons (WhatsApp `wa.me`, X, copy).
3. AdSense apply (30–50 quality **articles** ke baad), EarnKaro links verify, `/go/` clicks track.
4. Newsletter digest cron (provider verify).
**Done when:** pehla affiliate click `clicks` column mein; Search Console mein indexing shuru.

## Phase K — Tune (ongoing)
Weekly: precision@10 ("Hot" ne traffic diya?), weights tune (`sources.weight`), thresholds, caps, naye niche add (DB row). Monthly: D1 size, quota usage, top earners.

## QA checklist (launch)
- [ ] Board 360px pe clean, no horizontal scroll
- [ ] FreshnessStamp real; LiveDot sirf ≤15 min
- [ ] Cards `noindex`; sitemap mein sirf indexable
- [ ] Safety test terms (blocklist) → ignored
- [ ] Health posts draft→review
- [ ] Koi fake number/rating/doctor nahi
- [ ] `/img` allowlist test (random host → 403)
- [ ] D1 reads: public page pe KV/edge hit (analytics se verify)
- [ ] Secrets repo mein nahi (`git grep -i "api_key"`)
- [ ] Engine paused switch kaam karta hai
- [ ] Backup restore ek baar try kiya

## Galtiyan jo avoid karni hain
1. Har request D1 hit → free quota 1 din mein khatam. **KV+edge.**
2. Ek source pe depend → Google RSS toote to site khaali. **Multi-source + degrade.**
3. Har trend ka indexable page → thin content. **Gate + noindex cards.**
4. Tragedy/death trends monetize → brand + policy risk. **Safety gate.**
5. Open `/img` proxy → abuse. **Allowlist.**
6. Cron ek heavy job → timeout/limit. **Chhote jobs, batch writes.**
7. Hype numbers fake/round → trust gaya. **Real only.**
8. pytrends use karna (archived). **RSS + other signals.**

## Timeline
Week 1: A–C · Week 2: D–F · Week 3: G–H · Week 4: I–J + launch · Phir K.
