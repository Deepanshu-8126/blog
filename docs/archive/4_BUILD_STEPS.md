# BUILD_STEPS.md — ek-ek step, har step ka "Done when"

Rule: ek phase complete hone se pehle agla mat shuru karo.

## Phase 0 — Accounts & keys (30 min)
1. Supabase project banao → URL, anon key, service_role key copy.
2. Gemini API key (Google AI Studio). 3. xAI (Grok) API key. 4. TMDB API key (free).
5. GitHub repo (private). 6. Cloudflare account. 7. EarnKaro account + link format note.
6. Gold price API choose karo (JSON endpoint + key).
**Done when:** sab keys ek password manager mein, koi bhi chat/code mein paste nahi.

## Phase 1 — Database (30 min)
1. `3_ARCHITECTURE.md` ka schema Supabase SQL editor mein run.
2. Seed insert (12 niches) run.
3. `affiliate_rules` mein apne EarnKaro template ke 2–3 merchants daalo.
**Done when:** `select count(*) from niches` = 12; anon key se `niches` readable, `topics` NOT readable.

## Phase 2 — Pipeline local (1–2 hr)
1. `pip install requests supabase pytrends`
2. Env vars set (SUPABASE_URL, SUPABASE_SERVICE_KEY, GEMINI_API_KEY, GROK_API_KEY, TMDB_API_KEY).
3. `python pipeline.py --niche ai-tools --dry`
**Done when:** console mein trends list, ranked picks, ek article JSON print; DB mein kuch write nahi hua.

## Phase 3 — Pipeline real run
1. `python pipeline.py --niche ai-tools`
2. Supabase mein `posts` open karo; 1 post padho: facts sahi? koi invented stat? image aayi?
3. Dubara same command → duplicate nahi bana.
4. `--niche movies` (TMDB poster), `--niche gold-rate` (dataset row) test.
5. `python pipeline.py` (sab niches).
**Done when:** har feed/tools/movies niche mein ≥1 post, gold-rate mein ≥1 dataset row, `pipeline_runs.ok=true`.

## Phase 4 — Frontend shell
1. `npm create astro@latest` → `npx astro add tailwind cloudflare`
2. `.env`: `PUBLIC_SUPABASE_URL`, `PUBLIC_SUPABASE_ANON_KEY`.
3. `src/lib/db.ts` + tokens (`2_DESIGN.md §B`).
4. Header + **MegaMenu** (DB se, 4 columns; mobile accordion sheet).
**Done when:** menu 12 items DB se dikhata hai; row delete karo → menu se gayab (hardcode nahi).

## Phase 5 — Niche templates
1. `[niche]/index.astro` — slug lookup, `page_type` se template.
2. Feed → Tools → Dataset → Movies (is order mein).
3. Empty states.
**Done when:** 12 URLs sab khulte hain (`/ai-tools`, `/pc-builds`, `/gold-rate`, `/deals`, `/side-hustles`, `/cashback`, `/health`, `/fashion`, `/food`, `/gta-6`, `/movies`, `/viral`), kisi mein error nahi.

## Phase 6 — Post page + SEO
1. `[niche]/[post].astro`, image + credit, FAQ, related.
2. `<title>`, meta description, OpenGraph, canonical, JSON-LD Article/FAQ.
3. sitemap.xml, rss.xml, robots.txt.
4. Disclosure + niche disclaimer component.
**Done when:** Lighthouse mobile ≥ 90 (perf, SEO), disclaimer health post pe dikh raha.

## Phase 7 — Home + Trending
1. Hero (top trend), 4 NicheCards, Trending Today (24h), Latest per group.
2. Breaking ticker (sirf real `is_breaking`).
**Done when:** home pe koi fake number/text nahi.

## Phase 8 — Affiliate
1. `products` mein 10–20 real products/tools per tools-niche (manual ya CSV import).
2. Pipeline `fill_affiliate` run → `aff_url` bhara.
3. Button component: `rel="sponsored nofollow noopener" target="_blank"`.
4. Apne EarnKaro dashboard mein ek test click track hota hai ya nahi dekho.
**Done when:** har product button apna `aff_url` kholta hai; manual 3 links check.

## Phase 9 — Deploy
1. GitHub push → Cloudflare Pages connect, build `npm run build`, env vars daalo.
2. Custom domain `uniquedigit.com` → DNS.
**Done when:** live URL pe sab 12 pages + sitemap.

## Phase 10 — Automation
1. GitHub Secrets daalo; `daily.yml` add (architecture §6).
2. `workflow_dispatch` se manual run.
3. Viral workflow (6h).
**Done when:** Actions green, kal subah naye posts apne aap aaye.

## Phase 11 — Legal + Ads
1. About, Contact (real email), Privacy, Terms, Affiliate Disclosure, Disclaimer.
2. Search Console + Bing verify, sitemap submit.
3. 30–50 quality posts hone ke baad AdSense apply. Pehle AdSlot placeholders (fixed height).
**Done when:** legal pages footer mein, Search Console mein pages index hone lage.

## Phase 12 — "Naya niche" test (sync proof)
1. Supabase mein 13th row insert (e.g. `crypto`, grp `Money`, `feed`).
2. Page refresh → menu mein dikha, `/crypto` khula (empty state).
3. Pipeline run → posts aaye.
**Done when:** bina code touch kiye naya niche live.

## Phase 13 — QA checklist (launch se pehle)
- [ ] 360px mobile pe koi horizontal scroll nahi
- [ ] Har post mein source/credit link
- [ ] Health posts `draft` → manually review → publish
- [ ] Koi invented price/stat/quote nahi (10 random posts padho)
- [ ] Fake numbers/ratings/doctors kahin nahi
- [ ] Ad slots CLS < 0.1
- [ ] Service key repo/frontend bundle mein nahi (`grep -r service_role .`)
- [ ] RLS: anon se `topics`, `affiliate_rules` read fail

## Common design galtiyan (avoid)
1. Menu/pages hardcode → naya niche code maangta hai. **DB-driven rakho.**
2. 12 alag templates → ek bug 12 jagah. **4 templates.**
3. Pipeline bina dedupe → duplicate posts → Google penalty.
4. Daily 100+ AI posts → thin content. **Cap + review.**
5. Affiliate link har component mein alag → rule badalna mushkil. **Ek component.**
6. Service key frontend mein.
7. Ad slot bina fixed height → layout jump.
8. Sirf AI se likhwana bina facts → hallucination. **Facts-only prompt.**

## Realistic timeline
Week 1: Phase 0–3 · Week 2: 4–7 · Week 3: 8–10 · Week 4: 11–13 + launch. Phir sirf monitor + niche tuning.
