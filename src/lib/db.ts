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
