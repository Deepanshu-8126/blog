-- Cloudflare D1 (SQLite) schema v2.  Apply:  npx wrangler d1 execute uniquedigit --remote --file=schema_d1.sql
-- Notes: ids = 16-byte hex; times = ISO-8601 UTC text; arrays/objects = JSON text.

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS niches (
  id            TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
  slug          TEXT UNIQUE NOT NULL,
  name          TEXT NOT NULL,
  tagline       TEXT,
  grp           TEXT NOT NULL,                       -- Tech | Money | Lifestyle | Entertainment (mega-menu column)
  icon          TEXT,
  page_type     TEXT NOT NULL CHECK (page_type IN ('feed','tools','dataset','movies')),
  seed_keywords TEXT NOT NULL DEFAULT '[]',          -- JSON array (routing hints for classifier)
  fetchers      TEXT NOT NULL DEFAULT '["trends","wikipedia"]',
  config        TEXT NOT NULL DEFAULT '{}',          -- JSON {disclaimer, review, dataset_url, value_path, ...}
  pin           INTEGER NOT NULL DEFAULT 0,
  is_new        INTEGER NOT NULL DEFAULT 0,
  sort          INTEGER NOT NULL DEFAULT 0,
  active        INTEGER NOT NULL DEFAULT 1,
  created_at    TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now'))
);

-- A "topic" = one merged entity across all sources
CREATE TABLE IF NOT EXISTS topics (
  id          TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
  canonical   TEXT NOT NULL,                         -- display title
  ckey        TEXT NOT NULL,                         -- normalized sorted-token key
  slug        TEXT NOT NULL,
  niche_id    TEXT REFERENCES niches(id) ON DELETE SET NULL,
  hype        REAL NOT NULL DEFAULT 0,
  growth      REAL NOT NULL DEFAULT 0,
  stage       TEXT NOT NULL DEFAULT 'emerging' CHECK (stage IN ('emerging','hot','peak','cooling','gone')),
  n_sources   INTEGER NOT NULL DEFAULT 0,
  status      TEXT NOT NULL DEFAULT 'tracking' CHECK (status IN ('tracking','board','card','article','ignored')),
  safety      TEXT,                                  -- JSON classifier result
  merged_into TEXT REFERENCES topics(id),
  first_seen  TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now')),
  last_seen   TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now'))
);
CREATE INDEX IF NOT EXISTS idx_topics_ckey ON topics(ckey);
CREATE INDEX IF NOT EXISTS idx_topics_hype ON topics(status, hype DESC);
CREATE INDEX IF NOT EXISTS idx_topics_seen ON topics(last_seen);

-- Raw per-source observations (retention 7 days)
CREATE TABLE IF NOT EXISTS signals (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  topic_id    TEXT NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
  source      TEXT NOT NULL,
  value       REAL,                                  -- source-specific magnitude (traffic floor, views, points...)
  rank        INTEGER,
  url         TEXT,
  meta        TEXT,                                  -- JSON (news titles/links, etc.)
  captured_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now'))
);
CREATE INDEX IF NOT EXISTS idx_signals_topic ON signals(topic_id, source, captured_at DESC);
CREATE INDEX IF NOT EXISTS idx_signals_time ON signals(captured_at);

-- Hype over time for sparklines (retention 30 days)
CREATE TABLE IF NOT EXISTS hype_history (
  topic_id TEXT NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
  ts       TEXT NOT NULL,
  hype     REAL NOT NULL,
  PRIMARY KEY (topic_id, ts)
);

CREATE TABLE IF NOT EXISTS posts (
  id           TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
  niche_id     TEXT NOT NULL REFERENCES niches(id) ON DELETE CASCADE,
  topic_id     TEXT REFERENCES topics(id) ON DELETE SET NULL,
  kind         TEXT NOT NULL DEFAULT 'article' CHECK (kind IN ('card','article')),
  slug         TEXT NOT NULL,
  title        TEXT NOT NULL,
  summary      TEXT,
  body_md      TEXT,
  faq          TEXT NOT NULL DEFAULT '[]',
  sources      TEXT NOT NULL DEFAULT '[]',           -- JSON [{title,url,publisher}]
  image_url    TEXT,
  image_credit TEXT,
  source_url   TEXT,
  hype         REAL NOT NULL DEFAULT 0,
  views        INTEGER NOT NULL DEFAULT 0,
  is_breaking  INTEGER NOT NULL DEFAULT 0,
  indexable    INTEGER NOT NULL DEFAULT 0,           -- cards = 0 until promoted
  status       TEXT NOT NULL DEFAULT 'published' CHECK (status IN ('draft','published','archived')),
  published_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now')),
  updated_at   TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now')),
  UNIQUE (niche_id, slug),
  UNIQUE (topic_id, kind)
);
CREATE INDEX IF NOT EXISTS idx_posts_niche ON posts(niche_id, status, published_at DESC);
CREATE INDEX IF NOT EXISTS idx_posts_hype  ON posts(status, hype DESC, published_at DESC);

CREATE TABLE IF NOT EXISTS post_tags (
  post_id TEXT NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
  tag     TEXT NOT NULL,
  PRIMARY KEY (post_id, tag)
);
CREATE INDEX IF NOT EXISTS idx_tags ON post_tags(tag);

CREATE TABLE IF NOT EXISTS products (
  id        TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
  niche_id  TEXT NOT NULL REFERENCES niches(id) ON DELETE CASCADE,
  name      TEXT NOT NULL,
  tagline   TEXT,
  category  TEXT,
  badge     TEXT,
  keywords  TEXT NOT NULL DEFAULT '',                -- space-separated, for Deal Radar match
  image_url TEXT,
  price     REAL,
  rating    REAL,
  url       TEXT NOT NULL,
  aff_url   TEXT,
  merchant  TEXT,
  clicks    INTEGER NOT NULL DEFAULT 0,
  active    INTEGER NOT NULL DEFAULT 1,
  sort      INTEGER NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now'))
);
CREATE INDEX IF NOT EXISTS idx_products_niche ON products(niche_id, active, sort);

CREATE TABLE IF NOT EXISTS affiliate_rules (
  id       TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
  domain   TEXT UNIQUE NOT NULL,
  template TEXT NOT NULL                              -- e.g. https://.../?url={enc_url}&ref=YOURID  (EarnKaro dashboard se verify)
);

CREATE TABLE IF NOT EXISTS datasets (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  niche_id   TEXT NOT NULL REFERENCES niches(id) ON DELETE CASCADE,
  data       TEXT NOT NULL,                           -- JSON
  fetched_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now'))
);
CREATE INDEX IF NOT EXISTS idx_datasets ON datasets(niche_id, fetched_at DESC);

CREATE TABLE IF NOT EXISTS sources (
  key          TEXT PRIMARY KEY,
  weight       REAL NOT NULL,
  enabled      INTEGER NOT NULL DEFAULT 1,
  interval_min INTEGER NOT NULL DEFAULT 15,
  last_run     TEXT,
  last_ok      INTEGER
);

CREATE TABLE IF NOT EXISTS blocklist (
  term   TEXT PRIMARY KEY,
  reason TEXT
);

CREATE TABLE IF NOT EXISTS subscribers (
  email      TEXT PRIMARY KEY,
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now'))
);

CREATE TABLE IF NOT EXISTS pipeline_runs (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  job        TEXT NOT NULL,                           -- ingest | score | write | daily
  started_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now')),
  ok         INTEGER,
  summary    TEXT,
  error      TEXT
);

-- ---------- seed: sources ----------
INSERT OR IGNORE INTO sources(key,weight,interval_min) VALUES
 ('gtrends',0.30,15),('gnews',0.20,30),('wiki',0.15,60),('youtube',0.10,30),
 ('hn',0.08,30),('tmdb',0.05,360),('social',0.12,60);
UPDATE sources SET enabled=0 WHERE key='social';   -- optional, enable after keys

-- ---------- seed: 12 niches ----------
INSERT OR IGNORE INTO niches(slug,name,tagline,grp,icon,page_type,seed_keywords,fetchers,config,pin,is_new,sort) VALUES
('pc-builds','PC Builds','Custom rigs & parts','Tech','cpu','tools','["gaming pc","graphics card","cpu","ssd"]','[]','{}',1,0,1),
('gold-rate','Gold Rate','Live gold prices','Tech','coins','dataset','[]','[]','{"dataset_url":"PASTE_API_URL","auth_env":"GOLD_API_KEY","auth_header":"x-access-token","value_path":"price_gram_24k","label":"24K Gold / gram","unit":"₹","rows_path":"cities"}',0,0,2),
('ai-tools','AI Tools','Generative AI & utilities','Tech','sparkles','tools','["ai","chatgpt","gemini","llm","agent"]','[]','{}',1,0,3),
('deals','Deals','Today''s top discounts','Money','tag','tools','["sale","discount","offer","deal"]','[]','{}',1,0,4),
('side-hustles','Side Hustles','Earn extra income','Money','briefcase','feed','["side hustle","freelance","work from home"]','[]','{}',0,0,5),
('cashback','Cashback','Rewards & cashback offers','Money','percent','tools','["cashback","coupon","reward"]','[]','{}',0,0,6),
('health','Health','Wellness & fitness tips','Lifestyle','heart','feed','["diet","workout","sleep","wellness"]','[]','{"review":true,"disclaimer":"Yeh jankari sirf education ke liye hai, medical salah nahi. Doctor se pucho."}',0,0,7),
('fashion','Fashion','Trends & style guides','Lifestyle','shirt','feed','["fashion","sneakers","outfit","style"]','[]','{}',0,0,8),
('food','Food','Recipes & cooking','Lifestyle','utensils','feed','["recipe","street food","cooking"]','[]','{}',0,0,9),
('gta-6','GTA 6','News, updates & guides','Entertainment','gamepad','feed','["gta 6","rockstar","gta vi"]','[]','{}',1,1,10),
('movies','Movies','Reviews & trailers','Entertainment','clapperboard','movies','["movie","trailer","ott","box office"]','[]','{}',0,0,11),
('viral','Viral','Trending now','Entertainment','rocket','feed','[]','[]','{}',0,0,12);

-- ---------- seed: blocklist (extend in /admin) ----------
INSERT OR IGNORE INTO blocklist(term,reason) VALUES
 ('suicide','safety'),('rape','safety'),('murder','safety'),('obituary','safety'),('porn','adult'),('nude','adult');
