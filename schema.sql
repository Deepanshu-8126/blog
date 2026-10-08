-- =========================================================
-- UniqueDigit Viral Hub — Supabase Database Schema (v1.0)
-- =========================================================

create extension if not exists pgcrypto;

-- 1. Niches Table (Source of truth for Menu, Dashboard, Pipeline)
create table if not exists niches (
  id uuid primary key default gen_random_uuid(),
  slug text unique not null,
  name text not null,
  tagline text,
  grp text not null,                     -- Tech | Money | Lifestyle | Entertainment (mega-menu column)
  icon text,                             -- lucide icon name (cpu, coins, sparkles, etc.)
  page_type text not null check (page_type in ('feed','tools','dataset','movies')),
  seed_keywords text[] default '{}',     -- Google Trends seeds
  fetchers text[] default '{trends,wikipedia}',   -- trends | wikipedia | tmdb
  config jsonb default '{}',             -- {disclaimer, review, dataset_url, auth_env, auth_header}
  pin boolean default false,             -- header mein direct quick link
  is_new boolean default false,
  sort int default 0,
  active boolean default true,
  created_at timestamptz default now()
);

-- 2. Topics Table (Deduplication & Trend Tracking)
create table if not exists topics (
  id uuid primary key default gen_random_uuid(),
  niche_id uuid references niches on delete cascade,
  title text not null,
  slug text not null,
  trend_score int default 0,
  source text,
  fetched_at timestamptz default now(),
  unique(niche_id, slug)
);

-- 3. Posts Table (Articles & Guides)
create table if not exists posts (
  id uuid primary key default gen_random_uuid(),
  niche_id uuid references niches on delete cascade,
  topic_id uuid references topics on delete set null,
  slug text not null,
  title text not null,
  summary text,
  body_md text,
  faq jsonb default '[]',
  tags text[] default '{}',
  image_url text,
  image_credit text,
  source_url text,
  trend_score int default 0,
  views int default 0,
  is_breaking boolean default false,
  status text default 'published' check (status in ('draft','published','archived')),
  published_at timestamptz default now(),
  unique(niche_id, slug)
);

create index if not exists idx_posts_niche_status_pub on posts(niche_id, status, published_at desc);
create index if not exists idx_posts_status_trend on posts(status, trend_score desc, published_at desc);

-- 4. Products Table (Tools, Deals, PC Parts, Cashback offers)
create table if not exists products (
  id uuid primary key default gen_random_uuid(),
  niche_id uuid references niches on delete cascade,
  name text not null,
  tagline text,
  category text,
  badge text,
  image_url text,
  price numeric,
  rating numeric,
  url text not null,                      -- Merchant original link
  aff_url text,                           -- Filled via affiliate_rules template
  merchant text,
  active boolean default true,
  sort int default 0,
  created_at timestamptz default now()
);

-- 5. Affiliate Rules Table (EarnKaro / Affiliate link formats)
create table if not exists affiliate_rules (
  id uuid primary key default gen_random_uuid(),
  domain text unique not null,            -- amazon.in, flipkart.com, myntra.com ...
  template text not null                  -- e.g. https://ekaro.in/enkr2020/?url={enc_url}&ref=YOURID
);

-- 6. Datasets Table (Gold rates, Bullion, Currency history)
create table if not exists datasets (
  id uuid primary key default gen_random_uuid(),
  niche_id uuid references niches on delete cascade,
  data jsonb not null,
  fetched_at timestamptz default now()
);

create index if not exists idx_datasets_niche_fetched on datasets(niche_id, fetched_at desc);

-- 7. Subscribers & Pipeline Runs
create table if not exists subscribers (
  email text primary key,
  created_at timestamptz default now()
);

create table if not exists pipeline_runs (
  id uuid primary key default gen_random_uuid(),
  started_at timestamptz default now(),
  ok boolean,
  summary jsonb,
  error text
);

-- =========================================================
-- ROW LEVEL SECURITY (RLS) POLICIES
-- =========================================================
alter table niches enable row level security;
drop policy if exists r_niches on niches;
create policy r_niches on niches for select using (active = true);

alter table posts enable row level security;
drop policy if exists r_posts on posts;
create policy r_posts on posts for select using (status = 'published');

alter table products enable row level security;
drop policy if exists r_products on products;
create policy r_products on products for select using (active = true);

alter table datasets enable row level security;
drop policy if exists r_datasets on datasets;
create policy r_datasets on datasets for select using (true);

alter table topics enable row level security;
alter table affiliate_rules enable row level security;
alter table pipeline_runs enable row level security;

alter table subscribers enable row level security;
drop policy if exists i_subscribers on subscribers;
create policy i_subscribers on subscribers for insert with check (true);

-- =========================================================
-- SEED DATA (12 Niches across 4 Groups)
-- =========================================================
insert into niches(slug, name, tagline, grp, icon, page_type, seed_keywords, fetchers, config, pin, is_new, sort) values
('pc-builds', 'PC Builds', 'Custom rigs & parts', 'Tech', 'cpu', 'tools', '{gaming pc build,graphics card}', '{trends}', '{}', true, false, 1),
('gold-rate', 'Gold Rate', 'Live gold prices & trends', 'Tech', 'coins', 'dataset', '{}', '{}', '{"dataset_url":"https://api.metals.dev/v1/latest", "disclaimer":"Gold rates are indicative market rates and exclude GST and making charges."}', false, false, 2),
('ai-tools', 'AI Tools', 'Generative AI & utilities', 'Tech', 'sparkles', 'tools', '{ai tools,chatgpt alternative}', '{trends,wikipedia}', '{}', true, false, 3),
('deals', 'Deals', 'Today''s top discounts', 'Money', 'tag', 'tools', '{deals,discount}', '{trends}', '{}', true, false, 4),
('side-hustles', 'Side Hustles', 'Earn extra income', 'Money', 'briefcase', 'feed', '{side hustle,work from home}', '{trends,wikipedia}', '{}', false, false, 5),
('cashback', 'Cashback', 'Rewards & cashback offers', 'Money', 'percent', 'tools', '{cashback offers}', '{trends}', '{}', false, false, 6),
('health', 'Health', 'Wellness & fitness tips', 'Lifestyle', 'heart', 'feed', '{healthy diet,home workout}', '{trends,wikipedia}', '{"review":true,"disclaimer":"Yeh jankari sirf education ke liye hai, medical salah nahi. Kisi bhi upchar se pehle doctor se consult karein."}', false, false, 7),
('fashion', 'Fashion', 'Trends & style guides', 'Lifestyle', 'shirt', 'feed', '{fashion trends,sneakers}', '{trends,wikipedia}', '{}', false, false, 8),
('food', 'Food', 'Recipes & cooking guides', 'Lifestyle', 'utensils', 'feed', '{recipe,street food}', '{trends,wikipedia}', '{}', false, false, 9),
('gta-6', 'GTA 6', 'News, updates & guides', 'Entertainment', 'gamepad', 'feed', '{gta 6,rockstar games}', '{trends,wikipedia}', '{}', true, true, 10),
('movies', 'Movies', 'Reviews, OTT & trailers', 'Entertainment', 'clapperboard', 'movies', '{new movies,ott release}', '{trends,tmdb}', '{}', false, false, 11),
('viral', 'Viral', 'Trending internet moments', 'Entertainment', 'rocket', 'feed', '{}', '{trends}', '{}', false, false, 12)
on conflict (slug) do update set
  name = excluded.name,
  tagline = excluded.tagline,
  grp = excluded.grp,
  icon = excluded.icon,
  page_type = excluded.page_type,
  seed_keywords = excluded.seed_keywords,
  config = excluded.config,
  pin = excluded.pin,
  is_new = excluded.is_new,
  sort = excluded.sort;
