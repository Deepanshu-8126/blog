# ARCHITECTURE.md

## 1. Big picture
```
 GitHub Actions cron (daily 6:00 IST + viral 4x/day)
        │  python pipeline.py
        ▼
 ┌──────────────────────────── PIPELINE ────────────────────────────┐
 │ 1 niches (active) ← Supabase                                        │
 │ 2 Trends (pytrends related/rising)  | TMDB trending | dataset API  │
 │ 3 Dedupe vs topics                                                  │
 │ 4 Rank + angle  → Grok (fallback Gemini)                            │
 │ 5 Facts + image → Wikipedia REST (or TMDB)                          │
 │ 6 Article JSON  → Gemini (facts-only prompt)                        │
 │ 7 Save topics+posts (draft/published) → Supabase                    │
 │ 8 Affiliate links fill (affiliate_rules)                            │
 │ 9 Log → pipeline_runs                                               │
 └─────────────────────────────────────────────────────────────────────┘
        ▼
   SUPABASE (Postgres)  ◄── read (anon key, RLS) ──  ASTRO SSR on Cloudflare Pages
                                                        │  Cache-Control s-maxage=900
                                                        ▼
                                                   Visitor (mobile)
```
**Rule:** content/menu/pages ka source of truth = **Supabase**. Code sirf 4 templates + 1 pipeline file.

## 2. Stack
| Layer | Choice | Kyun |
|---|---|---|
| Frontend | **Astro SSR + Tailwind** (`@astrojs/cloudflare`) | Fast, kam JS, SEO, rebuild nahi chahiye |
| Hosting | Cloudflare Pages | Free, edge cache |
| DB | Supabase Postgres + RLS | Data + auth-less public read |
| Pipeline | Python 3.11, `requests`, `supabase`, `pytrends` | Single file |
| Scheduler | GitHub Actions cron | Free, logs |
| AI | Gemini (writing), Grok/xAI (ranking) | User ki choice |
| Images | Wikipedia REST, TMDB | Real + credit |

## 3. Supabase schema (`schema.sql`)
```sql
create extension if not exists pgcrypto;

create table niches(
  id uuid primary key default gen_random_uuid(),
  slug text unique not null,
  name text not null,
  tagline text,
  grp text not null,                     -- Tech | Money | Lifestyle | Entertainment  (mega-menu column)
  icon text, 
  page_type text not null check (page_type in ('feed','tools','dataset','movies')),
  seed_keywords text[] default '{}',     -- Google Trends seeds
  fetchers text[] default '{trends,wikipedia}',   -- trends | wikipedia | tmdb
  config jsonb default '{}',             -- {disclaimer, review, dataset_url, auth_env, auth_header}
  pin boolean default false,             -- header mein direct link
  is_new boolean default false,
  sort int default 0,
  active boolean default true,
  created_at timestamptz default now()
);

create table topics(
  id uuid primary key default gen_random_uuid(),
  niche_id uuid references niches on delete cascade,
  title text not null, slug text not null,
  trend_score int default 0, source text,
  fetched_at timestamptz default now(),
  unique(niche_id, slug)
);

create table posts(
  id uuid primary key default gen_random_uuid(),
  niche_id uuid references niches on delete cascade,
  topic_id uuid references topics,
  slug text not null, title text not null, summary text,
  body_md text, faq jsonb default '[]', tags text[] default '{}',
  image_url text, image_credit text, source_url text,
  trend_score int default 0, views int default 0,
  is_breaking boolean default false,
  status text default 'published' check (status in ('draft','published','archived')),
  published_at timestamptz default now(),
  unique(niche_id, slug)
);
create index on posts(niche_id, status, published_at desc);
create index on posts(status, trend_score desc, published_at desc);

create table products(                    -- tools / deals / PC parts / cashback offers
  id uuid primary key default gen_random_uuid(),
  niche_id uuid references niches on delete cascade,
  name text not null, tagline text, category text, badge text,
  image_url text, price numeric, rating numeric,   -- sirf real data
  url text not null,                      -- merchant ka original link
  aff_url text,                           -- pipeline fill karta hai
  merchant text, active boolean default true, sort int default 0,
  created_at timestamptz default now()
);

create table affiliate_rules(             -- EarnKaro link format yahan
  id uuid primary key default gen_random_uuid(),
  domain text unique not null,            -- amazon.in, flipkart.com ...
  template text not null                  -- e.g. https://ekaro.in/enkr2020/?url={enc_url}&ref=YOURID
);

create table datasets(                    -- gold rate etc. history
  id uuid primary key default gen_random_uuid(),
  niche_id uuid references niches on delete cascade,
  data jsonb not null,
  fetched_at timestamptz default now()
);
create index on datasets(niche_id, fetched_at desc);

create table subscribers(email text primary key, created_at timestamptz default now());
create table pipeline_runs(id uuid primary key default gen_random_uuid(), started_at timestamptz default now(), ok boolean, summary jsonb, error text);

-- RLS: public sirf published/active padh sake, write sirf service key
alter table niches enable row level security;   create policy r on niches for select using (active);
alter table posts enable row level security;    create policy r on posts for select using (status='published');
alter table products enable row level security; create policy r on products for select using (active);
alter table datasets enable row level security; create policy r on datasets for select using (true);
alter table topics enable row level security;   -- no public policy
alter table affiliate_rules enable row level security;
alter table pipeline_runs enable row level security;
alter table subscribers enable row level security; create policy i on subscribers for insert with check (true);
```
> EarnKaro ka exact link format apne dashboard se verify karke `template` mein daalo — main guess nahi kar raha.

### Seed (12 niches)
```sql
insert into niches(slug,name,tagline,grp,icon,page_type,seed_keywords,fetchers,config,pin,is_new,sort) values
('pc-builds','PC Builds','Custom rigs & parts','Tech','cpu','tools','{gaming pc build,graphics card}','{trends}','{}',true,false,1),
('gold-rate','Gold Rate','Live gold prices','Tech','coins','dataset','{}','{}','{"dataset_url":"PASTE_API_URL","auth_env":"GOLD_API_KEY","auth_header":"x-access-token"}',false,false,2),
('ai-tools','AI Tools','Generative AI & utilities','Tech','sparkles','tools','{ai tools,chatgpt alternative}','{trends,wikipedia}','{}',true,false,3),
('deals','Deals','Today''s top discounts','Money','tag','tools','{deals,discount}','{trends}','{}',true,false,4),
('side-hustles','Side Hustles','Earn extra income','Money','briefcase','feed','{side hustle,work from home}','{trends,wikipedia}','{}',false,false,5),
('cashback','Cashback','Rewards & cashback offers','Money','percent','tools','{cashback offers}','{trends}','{}',false,false,6),
('health','Health','Wellness & fitness tips','Lifestyle','heart','feed','{healthy diet,home workout}','{trends,wikipedia}','{"review":true,"disclaimer":"Yeh jankari sirf education ke liye hai, medical salah nahi. Doctor se pucho."}',false,false,7),
('fashion','Fashion','Trends & style guides','Lifestyle','shirt','feed','{fashion trends,sneakers}','{trends,wikipedia}','{}',false,false,8),
('food','Food','Recipes & cooking','Lifestyle','utensils','feed','{recipe,street food}','{trends,wikipedia}','{}',false,false,9),
('gta-6','GTA 6','News, updates & guides','Entertainment','gamepad','feed','{gta 6,rockstar games}','{trends,wikipedia}','{}',true,true,10),
('movies','Movies','Reviews & trailers','Entertainment','clapperboard','movies','{new movies,ott release}','{trends,tmdb}','{}',false,false,11),
('viral','Viral','Trending now','Entertainment','rocket','feed','{}','{trends}','{}',false,false,12);
```

## 4. Routing (Astro)
```
src/pages/index.astro                 Home (hub preview + Trending Today)
src/pages/[niche]/index.astro         niche by slug → switch(page_type) → 4 templates
src/pages/[niche]/[post].astro        post page
src/pages/search.astro, sitemap.xml.ts, rss.xml.ts, about/contact/privacy/terms/disclosure
src/components/  Header, MegaMenu, Hero, NicheCard, TrendingList, ToolCard, DatasetCard, MovieCard, AdSlot, Newsletter, Footer
src/templates/   Feed.astro, Tools.astro, Dataset.astro, Movies.astro
src/lib/db.ts    supabase client (anon) + 6 query helpers
```
- Niche DB mein nahi mila → 404.
- MegaMenu: `select * from niches where active and show` → group by `grp` → columns. Naya `grp` aaye to naya column auto.
- Cache: response header `Cache-Control: public, s-maxage=900, stale-while-revalidate=3600`.

**Naya niche add karne ka flow (auto-sync):**
1. `insert into niches(...)` (ya Supabase dashboard se row).
2. Menu + `/{slug}` page turant aa jata hai (template = page_type).
3. Next pipeline run us niche ke liye trends→posts bana deta hai. Code change = 0.

## 5. Pipeline details
| Step | Kya | Fail hone pe |
|---|---|---|
| Trends | pytrends `related_queries` rising per seed (geo IN, 7d) | AI topic fallback |
| TMDB | `/trending/movie/week` → title, poster, overview | skip |
| Dataset | `config.dataset_url` JSON → `datasets` row | log, continue |
| Rank | Grok: monetization+freshness score; fallback Gemini | first N by trend value |
| Wikipedia | search → summary → extract + original image | image null → placeholder |
| Write | Gemini JSON {title, summary, body_md, faq, tags}, facts-only | niche skip, log |
| Save | upsert (niche_id, slug) — idempotent | |
| Affiliate | products without `aff_url` → `affiliate_rules` | |
| Log | `pipeline_runs` | |

Caps: `POSTS_PER_NICHE=3` default → 12 niches ≈ 30–36 posts/day. Pehle 2 hafte 1–2 se start karo, quality check karo.

## 6. Schedule (GitHub Actions)
```yaml
# .github/workflows/daily.yml
name: daily-pipeline
on:
  schedule: [{cron: "30 0 * * *"}]      # 06:00 IST
  workflow_dispatch:
jobs:
  run:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: "3.11"}
      - run: pip install requests supabase pytrends
      - run: python pipeline.py
        env:
          SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
          SUPABASE_SERVICE_KEY: ${{ secrets.SUPABASE_SERVICE_KEY }}
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
          GROK_API_KEY: ${{ secrets.GROK_API_KEY }}
          TMDB_API_KEY: ${{ secrets.TMDB_API_KEY }}
          GOLD_API_KEY: ${{ secrets.GOLD_API_KEY }}
```
Viral ke liye alag workflow: cron `0 */6 * * *` + `python pipeline.py --niche viral`.

## 7. Secrets
| Key | Kahan |
|---|---|
| `SUPABASE_URL`, `SUPABASE_ANON_KEY` | Cloudflare Pages env (frontend) |
| `SUPABASE_SERVICE_KEY` | **sirf** GitHub Secrets (kabhi frontend mein nahi) |
| `GEMINI_API_KEY`, `GROK_API_KEY`, `TMDB_API_KEY`, gold key | GitHub Secrets |

## 8. Monitoring
- `pipeline_runs.ok=false` → GitHub Actions failure email.
- Weekly: Search Console indexing + top 10 posts by clicks → un niches pe `POSTS_PER_NICHE` badhao.
