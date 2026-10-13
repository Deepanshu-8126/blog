export interface Niche {
  id: string;
  slug: string;
  name: string;
  tagline: string;
  grp: 'Tech' | 'Money' | 'Lifestyle' | 'Entertainment' | string;
  icon: string;
  page_type: 'feed' | 'tools' | 'dataset' | 'movies' | 'health' | 'deals';
  seed_keywords?: string[];
  fetchers?: string[];
  config?: {
    disclaimer?: string;
    review?: boolean;
    dataset_url?: string;
    auth_env?: string;
    auth_header?: string;
    value_path?: string;
    label?: string;
    unit?: string;
    rows_path?: string;
  };
  pin?: boolean;
  is_new?: boolean;
  sort?: number;
  active?: boolean;
}

export interface Post {
  id: string;
  niche_id: string;
  topic_id?: string;
  kind?: 'card' | 'article';
  category?: string;
  slug: string;
  title: string;
  summary: string;
  body_md: string;
  faq?: Array<{ q: string; a: string }>;
  tags?: string[];
  sources?: Array<{ title: string; url: string; publisher?: string }>;
  image_url?: string;
  image_credit?: string;
  source_url?: string;
  hype?: number;
  trend_score: number;
  views?: number;
  is_breaking?: boolean;
  indexable?: boolean;
  status: 'published' | 'draft' | 'archived';
  published_at: string;
  updated_at?: string;
  niches?: Niche;
}

export interface Product {
  id: string;
  niche_id: string;
  name: string;
  tagline?: string;
  category?: string;
  badge?: string;
  keywords?: string;
  image_url?: string;
  price?: number;
  mrp?: number;
  discount_pct?: number;
  cpa_payout?: number;
  cashback_user?: number;
  coupon_code?: string;
  deal_type?: string;
  rating?: number;
  url: string;
  aff_url?: string;
  merchant?: string;
  clicks?: number;
  active?: boolean;
  sort?: number;
}

export interface DatasetEntry {
  id: string | number;
  niche_id: string;
  data: any;
  fetched_at: string;
}

// =========================================================
// Fallback Seed Data (Used for Dev / Build when D1 is offline)
// =========================================================

export const SEED_NICHES: Niche[] = [
  { id: '1', slug: 'pc-builds', name: 'PC Builds', tagline: 'Custom rigs & parts', grp: 'Tech', icon: 'cpu', page_type: 'tools', pin: true, is_new: false, sort: 1, active: true },
  { id: '2', slug: 'gold-rate', name: 'Gold Rate', tagline: 'Live gold prices & trends', grp: 'Tech', icon: 'coins', page_type: 'dataset', pin: false, is_new: false, sort: 2, active: true, config: { disclaimer: 'Gold rates are indicative market rates and exclude GST and making charges.' } },
  { id: '3', slug: 'ai-tools', name: 'AI Tools', tagline: 'Generative AI & utilities', grp: 'Tech', icon: 'sparkles', page_type: 'tools', pin: true, is_new: false, sort: 3, active: true },
  { id: '4', slug: 'deals', name: 'Deals', tagline: "Today's top discounts", grp: 'Money', icon: 'tag', page_type: 'deals', pin: true, is_new: false, sort: 4, active: true },
  { id: '5', slug: 'side-hustles', name: 'Side Hustles', tagline: 'Earn extra income', grp: 'Money', icon: 'briefcase', page_type: 'feed', pin: false, is_new: false, sort: 5, active: true },
  { id: '6', slug: 'cashback', name: 'Cashback', tagline: 'Rewards & cashback offers', grp: 'Money', icon: 'percent', page_type: 'deals', pin: false, is_new: false, sort: 6, active: true },
  { id: '7', slug: 'health', name: 'Health', tagline: 'Wellness & fitness tips', grp: 'Lifestyle', icon: 'heart', page_type: 'health', pin: false, is_new: false, sort: 7, active: true, config: { review: true, disclaimer: 'This information is strictly for educational purposes and is not medical advice. Always consult a qualified healthcare physician.' } },
  { id: '8', slug: 'fashion', name: 'Fashion', tagline: 'Trends & style guides', grp: 'Lifestyle', icon: 'shirt', page_type: 'feed', pin: false, is_new: false, sort: 8, active: true },
  { id: '9', slug: 'food', name: 'Food', tagline: 'Recipes & cooking guides', grp: 'Lifestyle', icon: 'utensils', page_type: 'feed', pin: false, is_new: false, sort: 9, active: true },
  { id: '10', slug: 'gta-6', name: 'GTA 6', tagline: 'News, updates & guides', grp: 'Entertainment', icon: 'gamepad', page_type: 'feed', pin: true, is_new: true, sort: 10, active: true },
  { id: '11', slug: 'movies', name: 'Movies', tagline: 'Reviews, OTT & trailers', grp: 'Entertainment', icon: 'clapperboard', page_type: 'movies', pin: false, is_new: false, sort: 11, active: true },
  { id: '12', slug: 'viral', name: 'Viral', tagline: 'Trending internet moments', grp: 'Entertainment', icon: 'rocket', page_type: 'feed', pin: false, is_new: false, sort: 12, active: true },
  { id: '13', slug: 'cricket-sports', name: 'Cricket Sports', tagline: 'Live scores, match analysis & team updates', grp: 'Lifestyle', icon: 'trophy', page_type: 'feed', pin: true, is_new: true, sort: 13, active: true },
  { id: '14', slug: 'football-sports', name: 'Football & Sports', tagline: 'ISL, Premier League & global football', grp: 'Lifestyle', icon: 'trophy', page_type: 'feed', pin: false, is_new: false, sort: 14, active: true },
  { id: '15', slug: 'automotive-trends', name: 'Automotive', tagline: 'EVs, bikes & new car launches in India', grp: 'Lifestyle', icon: 'car', page_type: 'feed', pin: false, is_new: false, sort: 15, active: true },
  { id: '16', slug: 'exams-results', name: 'Exams & Results', tagline: 'Govt jobs, admit cards & board results', grp: 'Education', icon: 'book', page_type: 'feed', pin: false, is_new: false, sort: 16, active: true },
  { id: '17', slug: 'entertainment-celebrity', name: 'Entertainment & Lifestyle', tagline: 'Celebrity news, red carpets & lifestyle buzz', grp: 'Entertainment', icon: 'film', page_type: 'feed', pin: false, is_new: false, sort: 17, active: true },
  { id: '18', slug: 'finance', name: 'Finance', tagline: 'Markets, SIPs, banking & personal finance', grp: 'Money', icon: 'trending-up', page_type: 'feed', pin: false, is_new: false, sort: 18, active: true }
];

export const SLUG_ALIASES: Record<string, string> = {
  'cricket': 'cricket-sports',
  'sports': 'cricket-sports',
  'football': 'football-sports',
  'builds': 'pc-builds',
  'pc': 'pc-builds',
  'gold': 'gold-rate',
  'ai': 'ai-tools',
  'auto': 'automotive-trends',
  'automotive': 'automotive-trends',
  'cars': 'automotive-trends',
  'bikes': 'automotive-trends',
  'exam': 'exams-results',
  'exams': 'exams-results',
  'results': 'exams-results',
  'ent': 'entertainment-celebrity',
  'celebrity': 'entertainment-celebrity',
  'bollywood': 'movies',
  'cinema': 'movies',
  'tech': 'pc-builds'
};
export const SEED_POSTS: Post[] = [];

export const SEED_PRODUCTS: Product[] = [];

// Helper to safely get D1 instance
export function getD1(runtimeEnv?: any): any {
  return runtimeEnv?.DB || runtimeEnv?.env?.DB || (globalThis as any)?.DB || null;
}

function parseJson<T>(val: any, fallback: T): T {
  if (!val) return fallback;
  if (typeof val === 'object') return val;
  try {
    return JSON.parse(val);
  } catch {
    return fallback;
  }
}

function mapNicheRow(row: any): Niche {
  return {
    ...row,
    pin: Boolean(row.pin),
    is_new: Boolean(row.is_new),
    active: Boolean(row.active),
    seed_keywords: parseJson(row.seed_keywords, []),
    fetchers: parseJson(row.fetchers, []),
    config: parseJson(row.config, {})
  };
}

function mapPostRow(row: any, niche?: Niche): Post {
  const resolvedNiche = niche || (row.niche_slug ? {
    id: row.niche_id,
    slug: row.niche_slug,
    name: row.niche_name || row.niche_slug,
    tagline: '',
    grp: row.niche_grp || 'Tech',
    icon: '⚡',
    page_type: 'feed',
    seed_keywords: [],
    fetchers: [],
    config: {},
    pin: false,
    is_new: false,
    sort: 0,
    active: true,
    created_at: row.published_at
  } as Niche : undefined);

  return {
    ...row,
    is_breaking: Boolean(row.is_breaking),
    indexable: Boolean(row.indexable),
    faq: parseJson(row.faq, []),
    sources: parseJson(row.sources, []),
    trend_score: row.hype || row.trend_score || 0,
    niches: resolvedNiche
  };
}

// =========================================================
// Core Cloudflare D1 Query Helpers
// =========================================================

/** 1. Get all active niches for MegaMenu and Header */
export async function getNiches(runtimeEnv?: any): Promise<Niche[]> {
  const db = getD1(runtimeEnv);
  if (db && typeof db.prepare === 'function') {
    try {
      const res = await db.prepare('SELECT * FROM niches WHERE active = 1 ORDER BY sort ASC').all();
      if (res.results && res.results.length > 0) {
        return res.results.map(mapNicheRow);
      }
    } catch (err) {
      console.warn('[D1 getNiches fallback]:', err);
    }
  }
  return SEED_NICHES;
}

/** 2. Get single niche by slug (case-insensitive with alias fallback) */
export async function getNicheBySlug(slug: string, runtimeEnv?: any): Promise<Niche | null> {
  const rawSlug = slug?.toLowerCase();
  const normalizedSlug = SLUG_ALIASES[rawSlug] || rawSlug;
  const db = getD1(runtimeEnv);
  if (db && typeof db.prepare === 'function') {
    try {
      const row = await db.prepare('SELECT * FROM niches WHERE (LOWER(slug) = ? OR LOWER(slug) = ?) AND active = 1 LIMIT 1').bind(rawSlug, normalizedSlug).first();
      if (row) return mapNicheRow(row);
    } catch (err) {
      console.warn('[D1 getNicheBySlug fallback]:', err);
    }
  }
  const niches = await getNiches(runtimeEnv);
  return niches.find(n => n.slug.toLowerCase() === normalizedSlug || n.slug.toLowerCase() === rawSlug) || null;
}

/** 3. Get published posts for a niche with pagination support */
export async function getPostsByNiche(nicheId: string, limit = 12, runtimeEnv?: any, offset = 0): Promise<Post[]> {
  const db = getD1(runtimeEnv);
  if (db && typeof db.prepare === 'function') {
    try {
      const res = await db.prepare(
        'SELECT * FROM posts WHERE niche_id = ? AND status = "published" ORDER BY published_at DESC LIMIT ? OFFSET ?'
      ).bind(nicheId, limit, offset).all();
      if (res && Array.isArray(res.results)) {
        return res.results.map((r: any) => mapPostRow(r));
      }
    } catch (err) {
      console.warn('[D1 getPostsByNiche error]:', err);
    }
  }
  return [];
}

/** 3b. Get total published post count for a niche */
export async function getPostsCountByNiche(nicheId: string, runtimeEnv?: any): Promise<number> {
  const db = getD1(runtimeEnv);
  if (db && typeof db.prepare === 'function') {
    try {
      const res = await db.prepare(
        'SELECT count(*) as count FROM posts WHERE niche_id = ? AND status = "published"'
      ).bind(nicheId).first();
      return Number(res?.count || 0);
    } catch (err) {
      console.warn('[D1 getPostsCountByNiche error]:', err);
    }
  }
  return 0;
}

/** 4. Get trending posts across all niches */
export async function getTrendingPosts(limit = 5, runtimeEnv?: any): Promise<Post[]> {
  const db = getD1(runtimeEnv);
  if (db && typeof db.prepare === 'function') {
    try {
      const res = await db.prepare(`
        SELECT posts.*, niches.slug as niche_slug, niches.name as niche_name, niches.grp as niche_grp 
        FROM posts 
        LEFT JOIN niches ON posts.niche_id = niches.id 
        WHERE posts.status = "published" 
        ORDER BY posts.hype DESC, posts.published_at DESC 
        LIMIT ?
      `).bind(limit).all();
      if (res && Array.isArray(res.results)) {
        return res.results.map((r: any) => mapPostRow(r));
      }
    } catch (err) {
      console.warn('[D1 getTrendingPosts error]:', err);
    }
  }
  return [];
}

/** 4b. Get all published posts for full XML sitemap indexing */
export async function getAllPublishedPosts(limit = 1000, runtimeEnv?: any): Promise<Post[]> {
  const db = getD1(runtimeEnv);
  if (db && typeof db.prepare === 'function') {
    try {
      const res = await db.prepare(`
        SELECT posts.*, niches.slug as niche_slug, niches.name as niche_name, niches.grp as niche_grp 
        FROM posts 
        LEFT JOIN niches ON posts.niche_id = niches.id 
        WHERE posts.status = "published" AND (posts.indexable = 1 OR posts.indexable IS NULL)
        ORDER BY posts.published_at DESC 
        LIMIT ?
      `).bind(limit).all();
      if (res && Array.isArray(res.results)) {
        return res.results.map((r: any) => mapPostRow(r));
      }
    } catch (err) {
      console.warn('[D1 getAllPublishedPosts error]:', err);
    }
  }
  return [];
}

/** 4c. Get published posts by editorial group (e.g. 'Tech', 'Money', 'Entertainment', 'Lifestyle') */
export async function getPostsByGroup(grp: string, limit = 4, excludeSlugs: string[] = [], runtimeEnv?: any): Promise<Post[]> {
  const db = getD1(runtimeEnv);
  if (db && typeof db.prepare === 'function') {
    try {
      let query = `
        SELECT posts.*, niches.slug as niche_slug, niches.name as niche_name, niches.grp as niche_grp 
        FROM posts 
        JOIN niches ON posts.niche_id = niches.id 
        WHERE posts.status = "published" AND LOWER(niches.grp) = LOWER(?)
      `;
      const binds: any[] = [grp];

      if (excludeSlugs.length > 0) {
        const placeholders = excludeSlugs.map(() => '?').join(',');
        query += ` AND posts.slug NOT IN (${placeholders})`;
        binds.push(...excludeSlugs);
      }

      query += ` ORDER BY posts.published_at DESC LIMIT ?`;
      binds.push(limit);

      const res = await db.prepare(query).bind(...binds).all();
      if (res && Array.isArray(res.results)) {
        return res.results.map((r: any) => mapPostRow(r));
      }
    } catch (err) {
      console.warn('[D1 getPostsByGroup error]:', err);
    }
  }
  return [];
}

/** 5. Get products / tools for a niche with optional limit & offset pagination */
export async function getProductsByNiche(
  nicheId: string,
  limitOrEnv?: number | any,
  runtimeEnv?: any,
  offset = 0
): Promise<Product[]> {
  const isLimitNumber = typeof limitOrEnv === 'number';
  const limit = isLimitNumber ? limitOrEnv : 12;
  const env = isLimitNumber ? runtimeEnv : limitOrEnv;

  const db = getD1(env);
  if (db && typeof db.prepare === 'function') {
    try {
      const res = await db.prepare(
        'SELECT * FROM products WHERE niche_id = ? AND active = 1 ORDER BY sort ASC, created_at DESC, clicks DESC LIMIT ? OFFSET ?'
      ).bind(nicheId, limit, offset).all();
      if (res.results && res.results.length > 0) {
        return res.results as Product[];
      }
    } catch (err) {
      console.warn('[D1 getProductsByNiche fallback]:', err);
    }
  }
  const filtered = SEED_PRODUCTS.filter(pr => pr.niche_id === nicheId);
  return filtered.slice(offset, offset + limit);
}

/** 5a. Get total count of active products in a niche */
export async function getProductsCountByNiche(nicheId: string, runtimeEnv?: any): Promise<number> {
  const db = getD1(runtimeEnv);
  if (db && typeof db.prepare === 'function') {
    try {
      const res = await db.prepare(
        'SELECT COUNT(*) as count FROM products WHERE niche_id = ? AND active = 1'
      ).bind(nicheId).first();
      if (res && typeof (res as any).count === 'number') {
        return (res as any).count;
      }
    } catch (err) {
      console.warn('[D1 getProductsCountByNiche error]:', err);
    }
  }
  return SEED_PRODUCTS.filter(pr => pr.niche_id === nicheId).length;
}

/** 5b. Get all active products across niches (Highest Revenue Payout First) */
export async function getAllProducts(runtimeEnv?: any): Promise<Product[]> {
  const db = getD1(runtimeEnv);
  if (db && typeof db.prepare === 'function') {
    try {
      const res = await db.prepare(
        'SELECT * FROM products WHERE active = 1 ORDER BY sort ASC, created_at DESC, clicks DESC'
      ).all();
      if (res.results && res.results.length > 0) {
        return res.results as Product[];
      }
    } catch (err) {
      console.warn('[D1 getAllProducts fallback]:', err);
    }
  }
  return SEED_PRODUCTS;
}

/** 6. Get post by niche slug and post slug */
export async function getPost(nicheSlug: string, postSlug: string, runtimeEnv?: any): Promise<Post | null> {
  const niche = await getNicheBySlug(nicheSlug, runtimeEnv);
  if (!niche) return null;

  const db = getD1(runtimeEnv);
  if (db && typeof db.prepare === 'function') {
    try {
      const row = await db.prepare(
        'SELECT * FROM posts WHERE niche_id = ? AND slug = ? AND status = "published" LIMIT 1'
      ).bind(niche.id, postSlug).first();
      if (row) {
        return mapPostRow(row, niche);
      }
      return null;
    } catch (err) {
      console.warn('[D1 getPost error]:', err);
    }
  }

  return null;
}

/** 7. Track product affiliate click in D1 */
export async function trackProductClick(productId: string, runtimeEnv?: any): Promise<void> {
  const db = getD1(runtimeEnv);
  if (db && typeof db.prepare === 'function') {
    try {
      await db.prepare('UPDATE products SET clicks = clicks + 1 WHERE id = ?').bind(productId).run();
    } catch (err) {
      console.warn('[D1 trackProductClick error]:', err);
    }
  }
}

/** 8. Get Product by ID for /go/[id] redirection */
export async function getProductById(productId: string, runtimeEnv?: any): Promise<Product | null> {
  const db = getD1(runtimeEnv);
  if (db && typeof db.prepare === 'function') {
    try {
      const row = await db.prepare('SELECT * FROM products WHERE id = ? LIMIT 1').bind(productId).first();
      if (row) return row as Product;
    } catch (err) {
      console.warn('[D1 getProductById fallback]:', err);
    }
  }
  return import.meta.env.DEV ? (SEED_PRODUCTS.find(p => p.id === productId) || null) : null;
}

/** 9. Newsletter subscription in D1 */
export async function subscribeNewsletter(email: string, runtimeEnv?: any): Promise<{ success: boolean; error?: string }> {
  const db = getD1(runtimeEnv);
  if (db && typeof db.prepare === 'function') {
    try {
      await db.prepare('INSERT OR IGNORE INTO subscribers (email) VALUES (?)').bind(email.toLowerCase().trim()).run();
      return { success: true };
    } catch (err: any) {
      return { success: false, error: err.message };
    }
  }
  return { success: true };
}
