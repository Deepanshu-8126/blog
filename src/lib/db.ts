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
  { id: '18', slug: 'finance', name: 'Finance', tagline: 'Markets, SIPs, banking & personal finance', grp: 'Money', icon: 'trending-up', page_type: 'feed', pin: false, is_new: false, sort: 18, active: true },
  { id: '19', slug: 'real-estate', name: 'Real Estate', tagline: 'Home loans, renting tips & property guides', grp: 'Money', icon: 'home', page_type: 'feed', pin: false, is_new: true, sort: 19, active: true },
  { id: '20', slug: 'gadgets', name: 'Gadgets & Mobile', tagline: 'Best phone reviews & gadget buying guides', grp: 'Tech', icon: 'smartphone', page_type: 'feed', pin: false, is_new: true, sort: 20, active: true },
  { id: '21', slug: 'recipes', name: 'Indian Recipes', tagline: 'Quick meals, tiffin ideas & weight loss cooking', grp: 'Lifestyle', icon: 'utensils', page_type: 'feed', pin: false, is_new: true, sort: 21, active: true },
  { id: '22', slug: 'sports', name: 'Sports & Cricket', tagline: 'IPL, cricket scores & fitness for athletes', grp: 'Entertainment', icon: 'trophy', page_type: 'feed', pin: false, is_new: true, sort: 22, active: true },
  { id: '23', slug: 'parenting', name: 'Parenting & Baby', tagline: 'Newborn tips, school guides & toys reviews', grp: 'Lifestyle', icon: 'smile', page_type: 'feed', pin: false, is_new: true, sort: 23, active: true },
  { id: '24', slug: 'travel', name: 'Travel & Budget Trips', tagline: 'Budget travel, train routes & visa guides', grp: 'Lifestyle', icon: 'plane', page_type: 'feed', pin: false, is_new: true, sort: 24, active: true },
  { id: '25', slug: 'comics', name: 'Comics & Anime Lore', tagline: 'Manga recaps, superhero multiverse, release countdowns & AI strips', grp: 'Entertainment', icon: 'zap', page_type: 'feed', pin: true, is_new: true, sort: 25, active: true, config: { disclaimer: 'All recaps, reviews, and character power analyses are original editorial fan commentary created under fair use principles.' } }
];

export const SLUG_ALIASES: Record<string, string> = {
  'cricket': 'sports',
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
  'tech': 'gadgets',
  'property': 'real-estate',
  'recipe': 'recipes',
  'baby': 'parenting',
  'trip': 'travel',
  'manga': 'comics',
  'anime': 'comics',
  'webtoon': 'comics',
  'webtoons': 'comics',
  'manhwa': 'comics',
  'comic': 'comics'
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

export interface YojanaItem {
  id: string;
  name: string;
  nameHindi: string;
  category: 'kisan' | 'women' | 'health' | 'youth' | 'housing';
  benefit: string;
  benefitBadgeColor: string;
  authority: string;
  stateBadge: string;
  stateTag: string;
  summary: string;
  eligibility: string[];
  documents: string[];
  steps: string[];
  officialUrl: string;
  statusBadge: string;
}

export interface CreditCardItem {
  id: string;
  name: string;
  bank: string;
  badge: string;
  badgeColor: string;
  annualFee: string;
  cashbackRate: string;
  welcomeOffer: string;
  keyPerks: string[];
  bestFor: string;
  applyUrl: string;
  rating: string;
}

/** 10. Dynamic Yojana Fetcher */
export async function getYojanas(runtimeEnv?: any): Promise<YojanaItem[]> {
  const db = getD1(runtimeEnv);
  if (db && typeof db.prepare === 'function') {
    try {
      const rows = await db.prepare(
        'SELECT * FROM posts WHERE category = "yojana" OR niche_id = (SELECT id FROM niches WHERE slug = "yojana" OR slug = "exams-results" LIMIT 1) ORDER BY published_at DESC LIMIT 20'
      ).all();
      if (rows.results && rows.results.length > 0) {
        return (rows.results as any[]).map((r, idx) => ({
          id: r.slug || `yojana-${idx}`,
          name: r.title,
          nameHindi: r.summary || r.title,
          category: (r.category as any) || 'kisan',
          benefit: 'Direct Government Subsidy / DBT Transfer',
          benefitBadgeColor: 'bg-emerald-600 text-white',
          authority: 'Ministry / Nodal Department of India',
          stateBadge: '🇮🇳 All-India / केंद्र व राज्य सरकार',
          stateTag: 'all',
          summary: r.summary || '',
          eligibility: ['भारतीय नागरिक होना अनिवार्य है', 'आधार कार्ड व DBT बैंक खाता लिंक होना चाहिए'],
          documents: ['आधार कार्ड', 'बैंक पासबुक', 'निवास प्रमाण पत्र', 'आय प्रमाण पत्र'],
          steps: ['आधिकारिक सरकारी पोर्टल पर जाएं', 'Apply Online पर क्लिक कर फॉर्म भरें', 'आवेदन स्टेटस चेक करें'],
          officialUrl: r.source_url || 'https://www.india.gov.in',
          statusBadge: '🟢 Scheme Active'
        }));
      }
    } catch (err) {
      console.warn('[D1 getYojanas error]:', err);
    }
  }

  // Baseline standard schemes
  return [
    {
      id: 'pm-surya-ghar',
      name: 'PM-Surya Ghar: Muft Bijli Yojana',
      nameHindi: 'पीएम सूर्य घर मुफ्त बिजली योजना (₹78,000 सोलर सब्सिडी)',
      category: 'housing',
      benefit: '₹78,000 तक सीधी बैंक सब्सिडी + 300 यूनिट मुफ्त बिजली',
      benefitBadgeColor: 'bg-amber-500 text-slate-950 font-black',
      authority: 'Ministry of New & Renewable Energy (MNRE)',
      stateBadge: '🇮🇳 All-India / केंद्र सरकार',
      stateTag: 'all',
      summary: 'घर की छत पर सोलर पैनल लगाने के लिए केंद्र सरकार की ऐतिहासिक योजना, जिससे घरेलू बिजली बिल शून्य (Zero) हो जाता है।',
      eligibility: ['आवेदक भारतीय नागरिक होना चाहिए', 'वैध घरेलू बिजली कनेक्शन होना आवश्यक है', 'छत पर पर्याप्त छाया-मुक्त जगह होनी चाहिए'],
      documents: ['बिजली बिल', 'आधार कार्ड', 'बैंक पासबुक (DBT Active)', 'छत के स्वामित्व का प्रमाण'],
      steps: ['pmsuryaghar.gov.in पोर्टल पर जाएं', 'अपना राज्य व उपभोक्ता संख्या दर्ज करें', 'पैनल लगवाएं और खाते में सब्सिडी पाएं'],
      officialUrl: 'https://pmsuryaghar.gov.in',
      statusBadge: '🟢 ₹78,000 Direct Subsidy Live'
    },
    {
      id: 'pm-kisan',
      name: 'PM Kisan Samman Nidhi Yojana',
      nameHindi: 'पीएम किसान सम्मान निधि (19वीं किस्त स्टेटस)',
      category: 'kisan',
      benefit: '₹6,000 प्रति वर्ष (₹2,000 हर 4 महीने में DBT)',
      benefitBadgeColor: 'bg-emerald-600 text-white',
      authority: 'Ministry of Agriculture & Farmers Welfare',
      stateBadge: '🇮🇳 All-India / केंद्र सरकार',
      stateTag: 'all',
      summary: 'छोटे और सीमांत किसानों को आर्थिक सहायता देने के लिए केंद्र सरकार की सबसे बड़ी डायरेक्ट बैंक ट्रांसफर (DBT) योजना।',
      eligibility: ['खेती योग्य जमीन का मालिक किसान', 'बैंक खाता आधार व NPCI से DBT-लिंक्ड होना चाहिए', 'e-KYC पूरी होनी चाहिए'],
      documents: ['आधार कार्ड', 'खतौनी / जमीन के दस्तावेज', 'बैंक पासबुक', 'मोबाइल नंबर'],
      steps: ['pmkisan.gov.in पोर्टल पर जाएं', '"Know Your Status" पर क्लिक करें', 'रजिस्ट्रेशन नंबर डालकर स्थिति देखें'],
      officialUrl: 'https://pmkisan.gov.in',
      statusBadge: '🟢 19th Installment Active'
    },
    {
      id: 'ayushman-bharat',
      name: 'Ayushman Bharat PM-JAY (Golden Card)',
      nameHindi: 'आयुष्मान भारत योजना (₹5 लाख मुफ्त इलाज कार्ड)',
      category: 'health',
      benefit: '₹5,00,000 प्रति परिवार प्रति वर्ष मुफ्त कैशलेस इलाज',
      benefitBadgeColor: 'bg-rose-600 text-white',
      authority: 'National Health Authority (NHA)',
      stateBadge: '🇮🇳 All-India / 70+ Senior Citizens',
      stateTag: 'all',
      summary: 'सरकारी और प्राइवेट लिस्टेड अस्पतालों में सेकेंडरी और टर्शियरी बीमारियों के लिए देश का सबसे बड़ा फ्री हेल्थ इंश्योरेंस।',
      eligibility: ['SECC सूची या अंत्योदय राशन कार्ड धारक', '70 वर्ष या उससे अधिक आयु के सभी वरिष्ठ नागरिक', 'NFSA के पात्र लाभार्थी'],
      documents: ['आधार कार्ड', 'राशन कार्ड', 'मोबाइल नंबर'],
      steps: ['beneficiary.nha.gov.in पर लॉग इन करें', 'राशन कार्ड या आधार से पात्रता चेक करें', '5 मिनट में आयुष्मान कार्ड डाउनलोड करें'],
      officialUrl: 'https://beneficiary.nha.gov.in',
      statusBadge: '🟢 70+ Age Open for All'
    },
    {
      id: 'pm-mudra-loan',
      name: 'Pradhan Mantri MUDRA Yojana (PMMY)',
      nameHindi: 'प्रधानमंत्री मुद्रा लोन योजना (₹20 लाख तक बिना गारंटी लोन)',
      category: 'youth',
      benefit: '₹50,000 से ₹20 लाख तक का बिजनेस लोन (बिना किसी गारंटी/कोलेटरल)',
      benefitBadgeColor: 'bg-blue-600 text-white',
      authority: 'Ministry of Finance & SIDBI',
      stateBadge: '🇮🇳 All-India / युवा व व्यापारी',
      stateTag: 'all',
      summary: 'छोटे व्यापारियों, स्टार्टअप्स, दुकानदारों और युवाओं को व्यवसाय शुरू करने के लिए सस्ता सरकारी लोन।',
      eligibility: ['18 वर्ष से अधिक आयु का भारतीय नागरिक', 'गैर-कॉर्पोरेट लघु/सूक्ष्म व्यवसाय', 'क्लीन सिबिल हिस्ट्री'],
      documents: ['आधार कार्ड व पैन कार्ड', 'बिजनेस पता व प्रोजेक्ट रिपोर्ट', '6 महीने का बैंक स्टेटमेंट'],
      steps: ['udyamimitra.in या बैंक शाखा जाएं', 'शिशु, किशोर या तरुण लोन चुनें', 'फॉर्म भरकर लोन प्राप्त करें'],
      officialUrl: 'https://www.mudra.org.in',
      statusBadge: '🟢 Limit Raised to ₹20L'
    }
  ];
}

/** 11. Dynamic Credit Cards Fetcher */
export async function getCreditCards(runtimeEnv?: any): Promise<CreditCardItem[]> {
  const db = getD1(runtimeEnv);
  if (db && typeof db.prepare === 'function') {
    try {
      const rows = await db.prepare(
        'SELECT * FROM products WHERE category = "credit-card" AND active = 1 ORDER BY sort ASC, created_at DESC'
      ).all();
      if (rows.results && rows.results.length > 0) {
        return (rows.results as any[]).map(p => ({
          id: p.id,
          name: p.name,
          bank: p.tagline || 'Bank Partner',
          badge: p.badge || 'RECOMMENDED',
          badgeColor: 'bg-emerald-500 text-white',
          annualFee: '₹0 (Lifetime Free)',
          cashbackRate: '5% - 10% Cashback',
          welcomeOffer: 'Exclusive Welcome Benefits',
          keyPerks: ['5% - 10% Cashback on online orders', 'Zero joining fee', 'Instant paperless KYC'],
          bestFor: p.keywords || 'Daily online shopping & rewards',
          applyUrl: p.aff_url || p.url,
          rating: '4.9 / 5'
        }));
      }
    } catch (err) {
      console.warn('[D1 getCreditCards error]:', err);
    }
  }

  // Baseline standard cards
  return [
    {
      id: 'amazon-pay-icici',
      name: 'Amazon Pay ICICI Bank Credit Card',
      bank: 'ICICI Bank',
      badge: '🏆 #1 BEST LIFETIME FREE CARD',
      badgeColor: 'bg-emerald-500 text-white',
      annualFee: '₹0 (Lifetime FREE Forever)',
      cashbackRate: '5% Unlimited Amazon Cashback',
      welcomeOffer: '₹1,500 Amazon Pay Reward Balance',
      keyPerks: [
        '5% Unlimited Cashback on Amazon (Prime Users)',
        '3% Unlimited Cashback on Amazon (Non-Prime Users)',
        '2% Cashback on 100+ Partner Merchants',
        '1% Cashback on all other retail & online spends'
      ],
      bestFor: 'Daily Amazon shoppers & zero annual fee seekers',
      applyUrl: 'https://www.amazon.in/s?k=amazon+pay+icici+credit+card&tag=uniquedigi0c6-21',
      rating: '4.9 / 5'
    },
    {
      id: 'swiggy-hdfc',
      name: 'Swiggy HDFC Bank Credit Card',
      bank: 'HDFC Bank',
      badge: '🍔 10% FOOD & GROCERY CASHBACK',
      badgeColor: 'bg-amber-500 text-slate-950 font-black',
      annualFee: '₹500 (Waived on ₹2 Lakh Spend)',
      cashbackRate: '10% Flat Cashback on Swiggy',
      welcomeOffer: '3 Months Free Swiggy One Membership',
      keyPerks: [
        '10% Flat Cashback on Food Delivery, Instamart & Dineout',
        '5% Cashback on Top E-Commerce (Amazon, Flipkart, Myntra, Uber)',
        'Direct monthly statement cashback credit'
      ],
      bestFor: 'Foodies, daily Instamart grocery buyers & online shoppers',
      applyUrl: 'https://www.amazon.in/s?k=hdfc+bank+credit+card&tag=uniquedigi0c6-21',
      rating: '4.8 / 5'
    },
    {
      id: 'sbi-cashback',
      name: 'SBI Cashback Credit Card',
      bank: 'State Bank of India',
      badge: '⚡ 5% FLAT ONLINE SHOPPING',
      badgeColor: 'bg-indigo-600 text-white',
      annualFee: '₹999 (Waived on ₹2 Lakh Spend)',
      cashbackRate: '5% Flat Online Cashback Across All Sites',
      welcomeOffer: 'Direct Auto-Credit in Monthly Statement',
      keyPerks: [
        '5% Cashback on almost all online platforms',
        '1% Cashback on all offline retail spends',
        'Cashback direct statement bill me minus hota hai'
      ],
      bestFor: 'Unfiltered online shopping across multiple websites',
      applyUrl: 'https://www.amazon.in/s?k=sbi+credit+card&tag=uniquedigi0c6-21',
      rating: '4.9 / 5'
    }
  ];
}

/** 12. Dynamic Site URL Helper */
export function getSiteUrl(runtimeEnv?: any): string {
  if (runtimeEnv?.SITE_URL) return runtimeEnv.SITE_URL.replace(/\/$/, '');
  return 'https://uniquedigit-viral-hub.pages.dev';
}

/** 13. Cricket & Sports Hub Models & Dynamic Fetcher */
export interface MatchFixture {
  id: string;
  matchNo: number;
  team1: string;
  team1Short: string;
  team1Color: string;
  team2: string;
  team2Short: string;
  team2Color: string;
  date: string;
  time: string;
  venue: string;
  city: string;
  status: 'Upcoming' | 'Live' | 'Completed';
  liveStream: string;
}

export interface TeamStanding {
  pos: number;
  team: string;
  short: string;
  color: string;
  played: number;
  won: number;
  lost: number;
  nrr: string;
  points: number;
  form: string[];
}

export interface FantasyTip {
  id: string;
  match: string;
  venue: string;
  pitchType: 'Batting Paradise' | 'Spin Friendly' | 'Pace & Bounce' | 'Balanced';
  avgScore: number;
  keyPlayers: string[];
  captainPicks: string[];
  differentialPick: string;
  advice: string;
}

export interface CricketProduct {
  id: string;
  title: string;
  category: string;
  price: string;
  mrp: string;
  discount: string;
  image: string;
  rating: string;
  affiliateUrl: string;
}

export interface CricketData {
  standings: TeamStanding[];
  fixtures: MatchFixture[];
  fantasyTips: FantasyTip[];
  gear: CricketProduct[];
}

export async function getCricketData(runtimeEnv?: any): Promise<CricketData> {
  const db = getD1(runtimeEnv);
  // Default dynamic baseline data
  const standings: TeamStanding[] = [
    { pos: 1, team: 'Chennai Super Kings', short: 'CSK', color: 'from-amber-500 to-yellow-400', played: 14, won: 10, lost: 4, nrr: '+0.782', points: 20, form: ['W', 'W', 'L', 'W', 'W'] },
    { pos: 2, team: 'Mumbai Indians', short: 'MI', color: 'from-blue-600 to-blue-400', played: 14, won: 9, lost: 5, nrr: '+0.614', points: 18, form: ['W', 'W', 'W', 'L', 'W'] },
    { pos: 3, team: 'Kolkata Knight Riders', short: 'KKR', color: 'from-purple-800 to-amber-500', played: 14, won: 9, lost: 5, nrr: '+0.542', points: 18, form: ['L', 'W', 'W', 'W', 'L'] },
    { pos: 4, team: 'Royal Challengers Bengaluru', short: 'RCB', color: 'from-red-600 to-black', played: 14, won: 8, lost: 6, nrr: '+0.320', points: 16, form: ['W', 'W', 'W', 'W', 'W'] },
    { pos: 5, team: 'Sunrisers Hyderabad', short: 'SRH', color: 'from-orange-600 to-black', played: 14, won: 8, lost: 6, nrr: '+0.280', points: 16, form: ['L', 'L', 'W', 'W', 'L'] },
    { pos: 6, team: 'Rajasthan Royals', short: 'RR', color: 'from-pink-600 to-blue-700', played: 14, won: 7, lost: 7, nrr: '+0.110', points: 14, form: ['L', 'L', 'L', 'W', 'L'] },
    { pos: 7, team: 'Gujarat Titans', short: 'GT', color: 'from-slate-800 to-amber-400', played: 14, won: 6, lost: 8, nrr: '-0.125', points: 12, form: ['W', 'L', 'L', 'L', 'W'] },
    { pos: 8, team: 'Delhi Capitals', short: 'DC', color: 'from-blue-700 to-red-600', played: 14, won: 5, lost: 9, nrr: '-0.342', points: 10, form: ['L', 'W', 'L', 'L', 'L'] },
    { pos: 9, team: 'Lucknow Super Giants', short: 'LSG', color: 'from-cyan-600 to-blue-800', played: 14, won: 5, lost: 9, nrr: '-0.450', points: 10, form: ['L', 'L', 'L', 'W', 'L'] },
    { pos: 10, team: 'Punjab Kings', short: 'PBKS', color: 'from-red-600 to-yellow-500', played: 14, won: 3, lost: 11, nrr: '-0.730', points: 6, form: ['L', 'L', 'L', 'L', 'L'] }
  ];

  const fixtures: MatchFixture[] = [
    {
      id: 'm-1',
      matchNo: 1,
      team1: 'Chennai Super Kings',
      team1Short: 'CSK',
      team1Color: 'bg-amber-500 text-slate-950',
      team2: 'Royal Challengers Bengaluru',
      team2Short: 'RCB',
      team2Color: 'bg-red-600 text-white',
      date: 'Friday, March 27',
      time: '7:30 PM IST',
      venue: 'MA Chidambaram Stadium (Chepauk)',
      city: 'Chennai',
      status: 'Upcoming',
      liveStream: 'JioCinema & Star Sports 1 HD'
    },
    {
      id: 'm-2',
      matchNo: 2,
      team1: 'Mumbai Indians',
      team1Short: 'MI',
      team1Color: 'bg-blue-600 text-white',
      team2: 'Kolkata Knight Riders',
      team2Short: 'KKR',
      team2Color: 'bg-purple-800 text-white',
      date: 'Saturday, March 28',
      time: '7:30 PM IST',
      venue: 'Wankhede Stadium',
      city: 'Mumbai',
      status: 'Upcoming',
      liveStream: 'JioCinema & Star Sports 1 HD'
    },
    {
      id: 'm-3',
      matchNo: 3,
      team1: 'Sunrisers Hyderabad',
      team1Short: 'SRH',
      team1Color: 'bg-orange-600 text-white',
      team2: 'Rajasthan Royals',
      team2Short: 'RR',
      team2Color: 'bg-pink-600 text-white',
      date: 'Sunday, March 29',
      time: '3:30 PM IST',
      venue: 'Rajiv Gandhi International Cricket Stadium',
      city: 'Hyderabad',
      status: 'Upcoming',
      liveStream: 'JioCinema & Star Sports 1 HD'
    },
    {
      id: 'm-4',
      matchNo: 4,
      team1: 'Gujarat Titans',
      team1Short: 'GT',
      team1Color: 'bg-slate-900 text-amber-300',
      team2: 'Delhi Capitals',
      team2Short: 'DC',
      team2Color: 'bg-blue-700 text-white',
      date: 'Sunday, March 29',
      time: '7:30 PM IST',
      venue: 'Narendra Modi Stadium',
      city: 'Ahmedabad',
      status: 'Upcoming',
      liveStream: 'JioCinema & Star Sports 1 HD'
    }
  ];

  const fantasyTips: FantasyTip[] = [
    {
      id: 'tip-chepauk',
      match: 'CSK vs RCB (Chepauk Opener)',
      venue: 'MA Chidambaram Stadium, Chennai',
      pitchType: 'Spin Friendly',
      avgScore: 168,
      keyPlayers: ['Ravindra Jadeja', 'Virat Kohli', 'Ruturaj Gaikwad', 'Glenn Maxwell'],
      captainPicks: ['Ravindra Jadeja (All-Rounder)', 'Ruturaj Gaikwad (Anchor)'],
      differentialPick: 'Maheesh Theekshana (High spin grip at Chepauk)',
      advice: 'Chepauk pitches slow down drastically in the 2nd innings. Opt for finger spinners and anchors who play spin well.'
    },
    {
      id: 'tip-wankhede',
      match: 'MI vs KKR (Wankhede Clash)',
      venue: 'Wankhede Stadium, Mumbai',
      pitchType: 'Batting Paradise',
      avgScore: 202,
      keyPlayers: ['Suryakumar Yadav', 'Andre Russell', 'Jasprit Bumrah', 'Phil Salt'],
      captainPicks: ['Suryakumar Yadav (360° hitter)', 'Andre Russell (Death overs bat+bowl)'],
      differentialPick: 'Tilak Varma (Consistent middle-order)',
      advice: 'True red-soil bounce with short boundaries and evening dew. Stack top-order power hitters and death yorker specialists.'
    }
  ];

  const gear: CricketProduct[] = [
    {
      id: 'sg-cricket-bat',
      title: 'SG Sierra Kashmir Willow Cricket Bat (Full Size Adult)',
      category: 'Bats',
      price: '₹1,499',
      mrp: '₹2,399',
      discount: '37% OFF',
      image: 'https://m.media-amazon.com/images/I/713v9qU6aML._SL1500_.jpg',
      rating: '4.4 ★ (3,120+ reviews)',
      affiliateUrl: 'https://www.amazon.in/s?k=SG+Kashmir+Willow+Cricket+Bat&tag=uniquedigi0c6-21'
    },
    {
      id: 'sg-cricket-kit',
      title: 'SG Economy Full Cricket Kit with Bat, Pads, Gloves & Bag',
      category: 'Kits',
      price: '₹4,899',
      mrp: '₹7,500',
      discount: '35% OFF',
      image: 'https://m.media-amazon.com/images/I/81xU-oU6YCL._SL1500_.jpg',
      rating: '4.3 ★ (1,840+ reviews)',
      affiliateUrl: 'https://www.amazon.in/s?k=SG+Cricket+Kit+Complete&tag=uniquedigi0c6-21'
    },
    {
      id: 'csk-jersey',
      title: 'Official CSK Fan Jersey 2026 Edition (Dry-Fit Breathable)',
      category: 'Merch',
      price: '₹699',
      mrp: '₹1,299',
      discount: '46% OFF',
      image: 'https://m.media-amazon.com/images/I/61tFpDk+g9L._SL1500_.jpg',
      rating: '4.6 ★ (4,900+ reviews)',
      affiliateUrl: 'https://www.amazon.in/s?k=CSK+Yellow+Cricket+Jersey&tag=uniquedigi0c6-21'
    },
    {
      id: 'leather-cricket-balls',
      title: 'SG Club Leather Cricket Ball (Pack of 2, 4-Piece Alum Tanned)',
      category: 'Balls',
      price: '₹749',
      mrp: '₹1,100',
      discount: '32% OFF',
      image: 'https://m.media-amazon.com/images/I/71R2cE8Y09L._SL1500_.jpg',
      rating: '4.5 ★ (2,450+ reviews)',
      affiliateUrl: 'https://www.amazon.in/s?k=SG+Leather+Cricket+Ball&tag=uniquedigi0c6-21'
    }
  ];

  return { standings, fixtures, fantasyTips, gear };
}

/** 14. Smartphone Catalog Models & Dynamic Fetcher */
export interface SmartphoneItem {
  id: string;
  name: string;
  tagline: string;
  category: 'under10k' | 'under15k' | 'under25k' | 'under40k' | 'flagship';
  price: string;
  mrp: string;
  discount: string;
  verdictBadge: string;
  badgeColor: string;
  image: string;
  processor: string;
  display: string;
  camera: string;
  battery: string;
  antutu?: string;
  pros: string[];
  cons: string[];
  amazonAsin: string;
  amazonUrl: string;
  highlight: string;
}

export async function getSmartphones(runtimeEnv?: any): Promise<SmartphoneItem[]> {
  const db = getD1(runtimeEnv);
  if (db && typeof db.prepare === 'function') {
    try {
      const rows = await db.prepare(
        'SELECT * FROM products WHERE category LIKE "under%" OR category = "flagship" ORDER BY sort ASC'
      ).all();
      if (rows.results && rows.results.length > 0) {
        return (rows.results as any[]).map(p => ({
          id: p.id,
          name: p.name,
          tagline: p.tagline || '',
          category: p.category as any,
          price: `₹${p.price?.toLocaleString('en-IN') || '0'}`,
          mrp: `₹${p.mrp?.toLocaleString('en-IN') || '0'}`,
          discount: p.discount ? `${p.discount}% OFF` : '',
          verdictBadge: p.badge || 'RECOMMENDED',
          badgeColor: 'bg-emerald-500 text-white',
          image: p.image_url || '/img?title=Smartphone',
          processor: p.keywords || 'High Performance Processor',
          display: '120Hz AMOLED Display',
          camera: '50MP OIS Camera',
          battery: '5000mAh Fast Charging',
          antutu: '600,000+ Score',
          pros: ['High Performance', 'Vibrant Display', 'Long Battery'],
          cons: ['No Charger in Box'],
          amazonAsin: p.asin || '',
          amazonUrl: p.aff_url || p.url,
          highlight: p.tagline || p.name
        }));
      }
    } catch (err) {
      console.warn('[D1 getSmartphones error]:', err);
    }
  }

  return [
    {
      id: 'cmf-phone-1',
      name: 'CMF Phone 1 by Nothing (5G)',
      tagline: 'Super Clean Nothing OS, 120Hz Super AMOLED & Modular Design',
      category: 'under15k',
      price: '₹14,999',
      mrp: '₹19,999',
      discount: '25% OFF',
      verdictBadge: '🏆 BEST VALUE 5G OVERALL',
      badgeColor: 'bg-emerald-500 text-white',
      image: 'https://m.media-amazon.com/images/I/717Qo4MH97L._SL1500_.jpg',
      processor: 'MediaTek Dimensity 7300 (4nm)',
      display: '6.67" 120Hz Super AMOLED, 2000 nits Peak',
      camera: '50MP Sony Main Sensor + 16MP Selfie',
      battery: '5000mAh • 33W Fast Charging',
      antutu: '670,000+ Score',
      pros: ['Zero Bloatware / Clean Nothing OS', 'Brilliant 120Hz Super AMOLED Display', 'Removable Back Cover / Modular Screws'],
      cons: ['No Charger in Box', 'Single Speaker (No Stereo)'],
      amazonAsin: 'B0D7HVN3V8',
      amazonUrl: 'https://www.amazon.in/s?k=CMF+Phone+1+5G&tag=uniquedigi0c6-21',
      highlight: "India's cleanest 5G phone under ₹15,000 with zero spam ads."
    },
    {
      id: 'nord-ce4',
      name: 'OnePlus Nord CE4 5G',
      tagline: '100W SuperVOOC Flash Charge & Snapdragon 7 Gen 3 Powerhouse',
      category: 'under25k',
      price: '₹22,999',
      mrp: '₹24,999',
      discount: '8% OFF',
      verdictBadge: '⚡ BEST MID-RANGE ALL-ROUNDER',
      badgeColor: 'bg-blue-600 text-white',
      image: 'https://m.media-amazon.com/images/I/71657TiFeHL._SL1500_.jpg',
      processor: 'Qualcomm Snapdragon 7 Gen 3 (4nm)',
      display: '6.7" 120Hz Fluid AMOLED, HDR10+',
      camera: '50MP Sony LYT-600 with OIS + 8MP Ultrawide',
      battery: '5500mAh Monster • 100W Charging (100% in 29m)',
      antutu: '820,000+ Score',
      pros: ['Insane 100W Fast Charging included in box', 'Massive 5500mAh Battery (2 Days)', 'OIS Sony LYT Camera produces crisp shots'],
      cons: ['Plastic Frame Design', 'No Alert Slider'],
      amazonAsin: 'B0CX21C8S2',
      amazonUrl: 'https://www.amazon.in/s?k=OnePlus+Nord+CE4+5G&tag=uniquedigi0c6-21',
      highlight: 'The ultimate daily driver under ₹25k: charges 1-100% in under 30 minutes.'
    },
    {
      id: 'iqoo-z9x',
      name: 'iQOO Z9x 5G',
      tagline: '6000mAh Ultra Battery & Slimmest Design under ₹13,000',
      category: 'under15k',
      price: '₹12,499',
      mrp: '₹17,999',
      discount: '31% OFF',
      verdictBadge: '🔋 2-DAY BATTERY CHAMPION',
      badgeColor: 'bg-amber-400 text-slate-950',
      image: 'https://m.media-amazon.com/images/I/71oXzCK43NL._SL1500_.jpg',
      processor: 'Snapdragon 6 Gen 1 (4nm)',
      display: '6.72" 120Hz Ultra Bright Display (1000 nits)',
      camera: '50MP AI Dual Camera + 8MP Selfie',
      battery: '6000mAh Gigantic Battery • 44W FlashCharge',
      antutu: '560,000+ Score',
      pros: ['Huge 6000mAh Battery yet only 7.99mm thin', 'Dual Stereo Speakers with 300% Audio Booster', 'IP64 Dust & Water Splash Resistance'],
      cons: ['LCD Screen instead of AMOLED', 'Funtouch OS has pre-installed apps'],
      amazonAsin: 'B0CZDNKCS2',
      amazonUrl: 'https://www.amazon.in/s?k=iQOO+Z9x+5G&tag=uniquedigi0c6-21',
      highlight: 'Perfect for students, delivery executives and travellers needing 2-day battery life.'
    },
    {
      id: 'poco-m6-5g',
      name: 'POCO M6 5G',
      tagline: 'Most Affordable 5G Smartphone in India with Dimensity 6100+',
      category: 'under10k',
      price: '₹8,999',
      mrp: '₹13,999',
      discount: '36% OFF',
      verdictBadge: '💰 BEST 5G UNDER ₹10,000',
      badgeColor: 'bg-emerald-600 text-white',
      image: 'https://m.media-amazon.com/images/I/71jG+e7roXL._SL1500_.jpg',
      processor: 'MediaTek Dimensity 6100+ 5G (6nm)',
      display: '6.74" 90Hz HD+ Corning Gorilla Glass 3',
      camera: '50MP AI Dual Camera with Night Mode',
      battery: '5000mAh • 18W Fast Charging Support',
      antutu: '410,000+ Score',
      pros: ['True 5G bands support under ₹9k', 'Smooth 90Hz Gorilla Glass Display', 'Premium Sky Glass design look'],
      cons: ['HD+ resolution (Not FHD+)', '10W slow charger in box'],
      amazonAsin: 'B0CQGBG21Y',
      amazonUrl: 'https://www.amazon.in/s?k=POCO+M6+5G&tag=uniquedigi0c6-21',
      highlight: 'Lowest price entry into 5G in India. Tested with Airtel & Jio True 5G.'
    },
    {
      id: 'oneplus-12r',
      name: 'OnePlus 12R 5G (Flagship Killer)',
      tagline: 'Snapdragon 8 Gen 2, 4th Gen LTPO AMOLED & 5500mAh 100W Monster',
      category: 'under40k',
      price: '₹37,999',
      mrp: '₹42,999',
      discount: '12% OFF',
      verdictBadge: '🎮 PERFORMANCE & BGMI KING',
      badgeColor: 'bg-purple-600 text-white',
      image: 'https://m.media-amazon.com/images/I/717Qo4MH97L._SL1500_.jpg',
      processor: 'Snapdragon 8 Gen 2 (4nm) Flagship SoC',
      display: '6.78" 1.5K 120Hz ProXDR LTPO4 AMOLED (4500 nits)',
      camera: '50MP Sony IMX890 OIS Flagship Sensor + 4K 60fps',
      battery: '5500mAh • 100W SuperVOOC (Charger included)',
      antutu: '1,500,000+ Score',
      pros: ['Flagship 8 Gen 2 handles 90fps BGMI flawlessly', 'Best-in-class 4500 nits LTPO4 display', 'Premium Aluminum Frame + Gorilla Glass Victus 2'],
      cons: ['8MP Ultrawide is average', 'No Wireless Charging'],
      amazonAsin: 'B0CQPV3M4R',
      amazonUrl: 'https://www.amazon.in/s?k=OnePlus+12R+5G&tag=uniquedigi0c6-21',
      highlight: 'Matches 90% of ₹70,000 flagships at half the price. The #1 recommendation under ₹40k.'
    },
    {
      id: 'iphone-16',
      name: 'Apple iPhone 16 (128GB)',
      tagline: 'A18 Pro Bionic, Camera Control Button & Apple Intelligence Ready',
      category: 'flagship',
      price: '₹75,900',
      mrp: '₹79,900',
      discount: '5% OFF',
      verdictBadge: '👑 BEST COMPACT FLAGSHIP',
      badgeColor: 'bg-slate-900 text-white',
      image: 'https://m.media-amazon.com/images/I/71657TiFeHL._SL1500_.jpg',
      processor: 'Apple A18 Bionic (3nm Next-Gen)',
      display: '6.1" Super Retina XDR OLED, 2000 nits Outdoor',
      camera: '48MP Fusion Camera + 2x Telephoto + 12MP Macro',
      battery: 'All-Day Battery Life • USB-C 30W Fast Charge',
      antutu: '1,750,000+ Score',
      pros: ['Dedicated Touch-Sensitive Camera Control Button', 'Next-Gen Apple Intelligence with Action Button', 'Industry best 4K Dolby Vision Video recording'],
      cons: ['Still 60Hz Display (Not 120Hz ProMotion)', '20W charging is slower than Android flagships'],
      amazonAsin: 'B0DGJ9M8V2',
      amazonUrl: 'https://www.amazon.in/s?k=iPhone+16&tag=uniquedigi0c6-21',
      highlight: 'The most refined iPhone for photography, reels creators, and long-term 5-year reliability.'
    }
  ];
}

/** 15. PC Builds Hub Models & Dynamic Fetchers */
export interface PcBuildItem {
  slug: string;
  title: string;
  price: string;
  badge: string;
  badgeColor: string;
  specs: string;
  fps: string;
  tag: string;
}

export interface PcBuildDetail {
  slug: string;
  title: string;
  tagline: string;
  budget: string;
  badge: string;
  badgeColor: string;
  cpu: string;
  cpuAsin: string;
  gpu: string;
  gpuAsin: string;
  mobo: string;
  moboAsin: string;
  ram: string;
  ramAsin: string;
  ssd: string;
  ssdAsin: string;
  psuCase: string;
  psuAsin: string;
  gtaFps: string;
  valFps: string;
  cpFps: string;
  bgmiFps: string;
  wattage: string;
  ups: string;
  asins: string[];
}

const PC_BUILDS_MAP: Record<string, PcBuildDetail> = {
  'student-35000': {
    slug: 'student-35000',
    title: 'Best Gaming PC Build Under ₹35,000 in India (2026)',
    tagline: 'Student Budget & Esports King (GTA 5, Valorant, BGMI, Coding)',
    budget: '₹34,890',
    badge: 'STUDENT BUDGET',
    badgeColor: 'bg-emerald-500 text-white',
    cpu: 'AMD Ryzen 5 5600 (6-Core, 12-Thread, 4.4GHz)',
    cpuAsin: 'B09VCHR1VH',
    gpu: 'ZOTAC GeForce GTX 1650 4GB GDDR6',
    gpuAsin: 'B07ZKSZ5MV',
    mobo: 'MSI B550M PRO-VDH WiFi (AM4)',
    moboAsin: 'B08BCR4Z9P',
    ram: 'Corsair Vengeance LPX 16GB (8GBx2) DDR4 3200MHz',
    ramAsin: 'B0143UM4TC',
    ssd: 'Crucial P3 500GB NVMe PCIe 3.0 M.2 SSD',
    ssdAsin: 'B0B25L3P3T',
    psuCase: 'Ant Esports ICE-112 Mid-Tower + 550W PSU Combo',
    psuAsin: 'B097Z77M1T',
    gtaFps: '95 FPS',
    valFps: '280 FPS',
    cpFps: '55 FPS',
    bgmiFps: '140 FPS',
    wattage: '320W',
    ups: '600VA / 360W',
    asins: ['B09VCHR1VH', 'B07ZKSZ5MV', 'B08BCR4Z9P', 'B0143UM4TC', 'B0B25L3P3T', 'B097Z77M1T']
  },
  'budget-gaming-50000': {
    slug: 'budget-gaming-50000',
    title: 'Best Gaming PC Build Under ₹50,000 with RTX 4060 in India',
    tagline: '1080p Ultra Gaming & Ray Tracing Beast with DLSS 3',
    budget: '₹54,980',
    badge: 'VALUE GAMING KING',
    badgeColor: 'bg-amber-400 text-slate-950',
    cpu: 'AMD Ryzen 5 5600 (6-Core, 12-Thread, 4.4GHz)',
    cpuAsin: 'B09VCHR1VH',
    gpu: 'Gigabyte GeForce RTX 4060 Eagle OC 8GB GDDR6',
    gpuAsin: 'B0C8JZKV6T',
    mobo: 'MSI B550M PRO-VDH WiFi (AM4)',
    moboAsin: 'B08BCR4Z9P',
    ram: 'Corsair Vengeance LPX 16GB (8GBx2) DDR4 3200MHz',
    ramAsin: 'B0143UM4TC',
    ssd: 'WD Blue SN580 1TB NVMe PCIe Gen 4x4 SSD (4150 MB/s)',
    ssdAsin: 'B0C8XMH264',
    psuCase: 'Ant Esports ICE-112 Mid-Tower + 550W PSU Combo',
    psuAsin: 'B097Z77M1T',
    gtaFps: '125 FPS',
    valFps: '380 FPS',
    cpFps: '78 FPS',
    bgmiFps: '180 FPS',
    wattage: '410W',
    ups: '600VA / 360W',
    asins: ['B09VCHR1VH', 'B0C8JZKV6T', 'B08BCR4Z9P', 'B0143UM4TC', 'B0C8XMH264', 'B097Z77M1T']
  },
  'editing-workstation-85000': {
    slug: 'editing-workstation-85000',
    title: 'Video Editing & 3D Render Workstation PC Under ₹85,000 (India)',
    tagline: 'Intel 13th Gen + 32GB DDR5 (Premiere Pro, DaVinci, Blender, After Effects)',
    budget: '₹84,970',
    badge: 'CREATOR WORKSTATION',
    badgeColor: 'bg-blue-600 text-white',
    cpu: 'Intel Core i5-13400F (10 Cores, 16 Threads, 4.6GHz)',
    cpuAsin: 'B0BN5ZW62Z',
    gpu: 'Gigabyte GeForce RTX 4060 8GB GDDR6 (CUDA & NVENC)',
    gpuAsin: 'B0C8JZKV6T',
    mobo: 'MSI PRO B760M-P DDR5 Motherboard (LGA1700)',
    moboAsin: 'B0BNP5C9XW',
    ram: 'Corsair Vengeance RGB 32GB (16GBx2) DDR5 6000MHz',
    ramAsin: 'B0BPTKD797',
    ssd: 'WD Blue SN580 1TB NVMe Gen4 (4150 MB/s Read)',
    ssdAsin: 'B0C8XMH264',
    psuCase: 'Deepcool CC560 V2 ARGB + Deepcool PK650D 650W Bronze',
    psuAsin: 'B09NLH6V32',
    gtaFps: '135 FPS',
    valFps: '420 FPS',
    cpFps: '82 FPS',
    bgmiFps: '190 FPS',
    wattage: '460W',
    ups: '1100VA / 660W',
    asins: ['B0BN5ZW62Z', 'B0C8JZKV6T', 'B0BNP5C9XW', 'B0BPTKD797', 'B0C8XMH264', 'B09NLH6V32']
  },
  '4k-gaming-120000': {
    slug: '4k-gaming-120000',
    title: 'High-End 4K Gaming PC Build Under ₹1.2 Lakh (India 2026)',
    tagline: 'Ryzen 7 7800X3D + RTX 4070 Super (4K 120Hz Ultra Gaming)',
    budget: '₹1,24,960',
    badge: '4K ULTRA BEAST',
    badgeColor: 'bg-purple-600 text-white',
    cpu: 'AMD Ryzen 7 7800X3D (World #1 3D V-Cache Gaming CPU)',
    cpuAsin: 'B0BTZB7F88',
    gpu: 'Gigabyte GeForce RTX 4070 Super 12GB OC GDDR6X',
    gpuAsin: 'B0CS9K4X6K',
    mobo: 'Gigabyte B650M Gaming WiFi (AM5 / DDR5)',
    moboAsin: 'B0C9J7V2T4',
    ram: 'Corsair Vengeance RGB 32GB (16GBx2) DDR5 6000MHz',
    ramAsin: 'B0BPTKD797',
    ssd: 'Samsung 990 PRO 1TB PCIe 4.0 M.2 NVMe (7450 MB/s)',
    ssdAsin: 'B0B9C3Z31R',
    psuCase: 'Corsair 4000D Airflow + Corsair RM750e 750W Gold Modular',
    psuAsin: 'B08C7BGV3D',
    gtaFps: '175 FPS',
    valFps: '580 FPS',
    cpFps: '120 FPS',
    bgmiFps: '240 FPS',
    wattage: '540W',
    ups: '1100VA / 660W',
    asins: ['B0BTZB7F88', 'B0CS9K4X6K', 'B0C9J7V2T4', 'B0BPTKD797', 'B0B9C3Z31R', 'B08C7BGV3D']
  },
  'rgb-dream-150000': {
    slug: 'rgb-dream-150000',
    title: 'Ultimate ARGB Dream Gaming Rig Under ₹1.5 Lakh (India)',
    tagline: 'Full Liquid Cooling AIO, 6x ARGB Sync, RTX 4070 Super, 32GB DDR5',
    budget: '₹1,48,900',
    badge: 'ULTIMATE RGB DREAM',
    badgeColor: 'bg-gradient-to-r from-pink-500 via-purple-500 to-cyan-500 text-white',
    cpu: 'AMD Ryzen 7 7800X3D (World #1 3D V-Cache Gaming)',
    cpuAsin: 'B0BTZB7F88',
    gpu: 'Gigabyte GeForce RTX 4070 Super 12GB OC GDDR6X',
    gpuAsin: 'B0CS9K4X6K',
    mobo: 'Gigabyte B650M Gaming WiFi (AM5 / DDR5)',
    moboAsin: 'B0C9J7V2T4',
    ram: 'Corsair Vengeance RGB 32GB (16GBx2) DDR5 6000MHz',
    ramAsin: 'B0BPTKD797',
    ssd: 'Samsung 990 PRO 1TB PCIe 4.0 M.2 SSD (7450 MB/s)',
    ssdAsin: 'B0B9C3Z31R',
    psuCase: 'Corsair 4000D Airflow Tempered Glass + 750W Gold PSU',
    psuAsin: 'B08C7BGV3D',
    gtaFps: '185 FPS',
    valFps: '600 FPS',
    cpFps: '125 FPS',
    bgmiFps: '240 FPS',
    wattage: '560W',
    ups: '1100VA / 660W',
    asins: ['B0BTZB7F88', 'B0CS9K4X6K', 'B0C9J7V2T4', 'B0BPTKD797', 'B0B9C3Z31R', 'B08C7BGV3D']
  }
};

export async function getPcBuilds(runtimeEnv?: any): Promise<PcBuildItem[]> {
  return [
    {
      slug: 'student-35000',
      title: 'Student Budget Gaming PC',
      price: '₹34,890',
      badge: 'STUDENT BUDGET',
      badgeColor: 'bg-emerald-500 text-white',
      specs: 'AMD Ryzen 5 5600 • GTX 1650 • 16GB RAM • 500GB SSD',
      fps: 'GTA 5: 95 FPS | Val: 280 FPS',
      tag: 'Best for Coding, Esports & School Work'
    },
    {
      slug: 'budget-gaming-50000',
      title: 'Value King 1080p Ultra Gaming Rig',
      price: '₹54,980',
      badge: 'VALUE GAMING KING',
      badgeColor: 'bg-amber-400 text-slate-950',
      specs: 'Ryzen 5 5600 • RTX 4060 8GB • 16GB RAM • 1TB NVMe',
      fps: 'GTA 5: 125 FPS | Val: 380 FPS | Cyberpunk: 78 FPS',
      tag: 'DLSS 3 & Ray Tracing King under ₹55k'
    },
    {
      slug: 'editing-workstation-85000',
      title: 'Video Editing & 3D Render Workstation',
      price: '₹84,970',
      badge: 'CREATOR WORKSTATION',
      badgeColor: 'bg-blue-600 text-white',
      specs: 'Intel Core i5-13400F 10-Core • RTX 4060 • 32GB DDR5 • 1TB Gen4',
      fps: '4K Video Editing • Premiere Pro & DaVinci Ready',
      tag: '32GB High-Speed DDR5 Memory'
    },
    {
      slug: '4k-gaming-120000',
      title: 'High-End 4K Esports & Creator Beast',
      price: '₹1,24,960',
      badge: '4K ULTRA BEAST',
      badgeColor: 'bg-purple-600 text-white',
      specs: 'Ryzen 7 7800X3D (3D V-Cache) • RTX 4070 Super 12GB • 32GB DDR5',
      fps: '4K 120 FPS Ultra Gaming & Streamer Rig',
      tag: 'World #1 Gaming CPU (7800X3D)'
    },
    {
      slug: 'rgb-dream-150000',
      title: 'Ultimate ARGB Dream Showcase Rig',
      price: '₹1,48,900',
      badge: 'ULTIMATE RGB DREAM',
      badgeColor: 'bg-gradient-to-r from-pink-500 via-purple-500 to-cyan-500 text-white',
      specs: 'Ryzen 7 7800X3D • RTX 4070 Super • Corsair 4000D • 750W Gold',
      fps: '6x ARGB Aura Sync • 4K Max Settings 144Hz',
      tag: 'Full Tempered Glass & Liquid AIO'
    }
  ];
}

export async function getPcBuildBySlug(slug: string, runtimeEnv?: any): Promise<PcBuildDetail | null> {
  const target = PC_BUILDS_MAP[slug] || PC_BUILDS_MAP['budget-gaming-50000'];
  return target || null;
}

