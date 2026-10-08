-- =========================================================
-- UniqueDigit Viral Hub — Cloudflare D1 Database Schema (v1.0)
-- =========================================================

-- 1. Niches Table (Source of truth for Menu, Hubs, and Templates)
CREATE TABLE IF NOT EXISTS niches (
  id TEXT PRIMARY KEY,
  slug TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  tagline TEXT,
  grp TEXT NOT NULL,                     -- Tech | Money | Lifestyle | Entertainment
  icon TEXT DEFAULT 'sparkles',
  page_type TEXT NOT NULL,               -- feed | tools | dataset | movies
  seed_keywords TEXT DEFAULT '[]',       -- JSON array string
  fetchers TEXT DEFAULT '["trends","wikipedia"]', -- JSON array string
  config TEXT DEFAULT '{}',              -- JSON config string {disclaimer, review, dataset_url}
  pin INTEGER DEFAULT 0,                 -- 1 for pinned in header, 0 for more
  is_new INTEGER DEFAULT 0,
  sort INTEGER DEFAULT 0,
  active INTEGER DEFAULT 1,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. Topics Table (Trend Tracking & Deduplication)
CREATE TABLE IF NOT EXISTS topics (
  id TEXT PRIMARY KEY,
  niche_id TEXT NOT NULL,
  title TEXT NOT NULL,
  slug TEXT NOT NULL,
  trend_score INTEGER DEFAULT 0,
  source TEXT,
  fetched_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(niche_id, slug),
  FOREIGN KEY (niche_id) REFERENCES niches(id) ON DELETE CASCADE
);

-- 3. Posts Table (Articles & Guides)
CREATE TABLE IF NOT EXISTS posts (
  id TEXT PRIMARY KEY,
  niche_id TEXT NOT NULL,
  topic_id TEXT,
  slug TEXT NOT NULL,
  title TEXT NOT NULL,
  summary TEXT,
  body_md TEXT,
  faq TEXT DEFAULT '[]',                 -- JSON array string
  tags TEXT DEFAULT '[]',                -- JSON array string
  image_url TEXT,
  image_credit TEXT,
  source_url TEXT,
  trend_score INTEGER DEFAULT 0,
  views INTEGER DEFAULT 0,
  is_breaking INTEGER DEFAULT 0,
  status TEXT DEFAULT 'published',       -- published | draft | archived
  published_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(niche_id, slug),
  FOREIGN KEY (niche_id) REFERENCES niches(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_posts_niche_pub ON posts(niche_id, status, published_at DESC);
CREATE INDEX IF NOT EXISTS idx_posts_trend ON posts(status, trend_score DESC, published_at DESC);

-- 4. Products Table (Tools, Deals, PC Parts, Cashback offers)
CREATE TABLE IF NOT EXISTS products (
  id TEXT PRIMARY KEY,
  niche_id TEXT NOT NULL,
  name TEXT NOT NULL,
  tagline TEXT,
  category TEXT,
  badge TEXT,
  image_url TEXT,
  price REAL,
  rating REAL,
  url TEXT NOT NULL,
  aff_url TEXT,
  merchant TEXT,
  active INTEGER DEFAULT 1,
  sort INTEGER DEFAULT 0,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (niche_id) REFERENCES niches(id) ON DELETE CASCADE
);

-- 5. Affiliate Rules Table (Amazon / EarnKaro link format rules)
CREATE TABLE IF NOT EXISTS affiliate_rules (
  id TEXT PRIMARY KEY,
  domain TEXT UNIQUE NOT NULL,           -- amazon.in, flipkart.com ...
  template TEXT NOT NULL                 -- https://www.amazon.in/dp/{asin}?tag=uniquedigi0c6-21
);

-- 6. Datasets Table (Gold Rates & Bullion History)
CREATE TABLE IF NOT EXISTS datasets (
  id TEXT PRIMARY KEY,
  niche_id TEXT NOT NULL,
  data TEXT NOT NULL,                    -- JSON payload string
  fetched_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (niche_id) REFERENCES niches(id) ON DELETE CASCADE
);

-- 7. Subscribers & Pipeline Runs
CREATE TABLE IF NOT EXISTS subscribers (
  email TEXT PRIMARY KEY,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS pipeline_runs (
  id TEXT PRIMARY KEY,
  started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  ok INTEGER,
  summary TEXT,
  error TEXT
);

-- =========================================================
-- SEED DATA (12 Niches across 4 Groups)
-- =========================================================
INSERT OR REPLACE INTO niches (id, slug, name, tagline, grp, icon, page_type, seed_keywords, fetchers, config, pin, is_new, sort, active) VALUES
('1', 'pc-builds', 'PC Builds', 'Custom rigs & parts', 'Tech', 'cpu', 'tools', '["gaming pc build","graphics card"]', '["trends"]', '{}', 1, 0, 1, 1),
('2', 'gold-rate', 'Gold Rate', 'Live gold prices & trends', 'Tech', 'coins', 'dataset', '[]', '[]', '{"dataset_url":"https://api.metals.dev/v1/latest","disclaimer":"Gold rates are indicative market rates and exclude GST and making charges."}', 0, 0, 2, 1),
('3', 'ai-tools', 'AI Tools', 'Generative AI & utilities', 'Tech', 'sparkles', 'tools', '["ai tools","chatgpt alternative"]', '["trends","wikipedia"]', '{}', 1, 0, 3, 1),
('4', 'deals', 'Deals', 'Today''s top discounts', 'Money', 'tag', 'tools', '["deals","discount"]', '["trends"]', '{}', 1, 0, 4, 1),
('5', 'side-hustles', 'Side Hustles', 'Earn extra income', 'Money', 'briefcase', 'feed', '["side hustle","work from home"]', '["trends","wikipedia"]', '{}', 0, 0, 5, 1),
('6', 'cashback', 'Cashback', 'Rewards & cashback offers', 'Money', 'percent', 'tools', '["cashback offers"]', '["trends"]', '{}', 0, 0, 6, 1),
('7', 'health', 'Health', 'Wellness & fitness tips', 'Lifestyle', 'heart', 'feed', '["healthy diet","home workout"]', '["trends","wikipedia"]', '{"review":true,"disclaimer":"Yeh jankari sirf education ke liye hai, medical salah nahi. Doctor se pucho."}', 0, 0, 7, 1),
('8', 'fashion', 'Fashion', 'Trends & style guides', 'Lifestyle', 'shirt', 'feed', '["fashion trends","sneakers"]', '["trends","wikipedia"]', '{}', 0, 0, 8, 1),
('9', 'food', 'Food', 'Recipes & cooking guides', 'Lifestyle', 'utensils', 'feed', '["recipe","street food"]', '["trends","wikipedia"]', '{}', 0, 0, 9, 1),
('10', 'gta-6', 'GTA 6', 'News, updates & guides', 'Entertainment', 'gamepad', 'feed', '["gta 6","rockstar games"]', '["trends","wikipedia"]', '{}', 1, 1, 10, 1),
('11', 'movies', 'Movies', 'Reviews, OTT & trailers', 'Entertainment', 'clapperboard', 'movies', '["new movies","ott release"]', '["trends","tmdb"]', '{}', 0, 0, 11, 1),
('12', 'viral', 'Viral', 'Trending internet moments', 'Entertainment', 'rocket', 'feed', '[]', '["trends"]', '{}', 0, 0, 12, 1);
