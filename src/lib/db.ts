export interface Niche {
  id: string;
  slug: string;
  name: string;
  tagline: string;
  grp: 'Tech' | 'Money' | 'Lifestyle' | 'Entertainment' | string;
  icon: string;
  page_type: 'feed' | 'tools' | 'dataset' | 'movies';
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
  { id: '4', slug: 'deals', name: 'Deals', tagline: "Today's top discounts", grp: 'Money', icon: 'tag', page_type: 'tools', pin: true, is_new: false, sort: 4, active: true },
  { id: '5', slug: 'side-hustles', name: 'Side Hustles', tagline: 'Earn extra income', grp: 'Money', icon: 'briefcase', page_type: 'feed', pin: false, is_new: false, sort: 5, active: true },
  { id: '6', slug: 'cashback', name: 'Cashback', tagline: 'Rewards & cashback offers', grp: 'Money', icon: 'percent', page_type: 'tools', pin: false, is_new: false, sort: 6, active: true },
  { id: '7', slug: 'health', name: 'Health', tagline: 'Wellness & fitness tips', grp: 'Lifestyle', icon: 'heart', page_type: 'feed', pin: false, is_new: false, sort: 7, active: true, config: { review: true, disclaimer: 'This information is strictly for educational purposes and is not medical advice. Always consult a qualified healthcare physician.' } },
  { id: '8', slug: 'fashion', name: 'Fashion', tagline: 'Trends & style guides', grp: 'Lifestyle', icon: 'shirt', page_type: 'feed', pin: false, is_new: false, sort: 8, active: true },
  { id: '9', slug: 'food', name: 'Food', tagline: 'Recipes & cooking guides', grp: 'Lifestyle', icon: 'utensils', page_type: 'feed', pin: false, is_new: false, sort: 9, active: true },
  { id: '10', slug: 'gta-6', name: 'GTA 6', tagline: 'News, updates & guides', grp: 'Entertainment', icon: 'gamepad', page_type: 'feed', pin: true, is_new: true, sort: 10, active: true },
  { id: '11', slug: 'movies', name: 'Movies', tagline: 'Reviews, OTT & trailers', grp: 'Entertainment', icon: 'clapperboard', page_type: 'movies', pin: false, is_new: false, sort: 11, active: true },
  { id: '12', slug: 'viral', name: 'Viral', tagline: 'Trending internet moments', grp: 'Entertainment', icon: 'rocket', page_type: 'feed', pin: false, is_new: false, sort: 12, active: true }
];

export const SEED_POSTS: Post[] = [
  {
    id: 'p1',
    niche_id: '10',
    slug: 'gta-6-pc-specs-release-date-india-pricing',
    kind: 'article',
    title: 'GTA 6 PC Specs & Realistic India Pricing: What System Do You Need?',
    summary: 'Comprehensive analysis of expected PC requirements for Grand Theft Auto VI, ray tracing hardware demands, and build cost in India.',
    body_md: `## GTA 6 PC Hardware Demands\nRockstar Games title Grand Theft Auto VI is expected to set a new benchmark in open-world graphics simulation. With advanced ray-traced global illumination and complex crowd AI, hardware selection is paramount.\n\n### Minimum vs Recommended Hardware\n- **Target 1080p 60FPS:** AMD Ryzen 5 7600X or Intel Core i5-13600K paired with NVIDIA RTX 4060 Ti / AMD Radeon RX 7700 XT.\n- **Target 1440p / 4K Ultra:** AMD Ryzen 7 7800X3D and NVIDIA GeForce RTX 4080 Super.\n\n### Storage & Memory\nA minimum of 32GB DDR5 RAM is strongly advised along with high-speed NVMe Gen4 SSD storage to avoid texture streaming bottlenecks.`,
    faq: [
      { q: 'Will GTA 6 run on 16GB RAM?', a: 'While 16GB might meet minimum specs, 32GB RAM will prevent stutters in dense city areas.' },
      { q: 'When is GTA 6 releasing on PC?', a: 'PC release is expected following the initial console launch.' }
    ],
    tags: ['GTA 6', 'Gaming PC', 'Rockstar Games'],
    sources: [
      { title: 'Rockstar Games Official Wire', url: 'https://rockstargames.com' },
      { title: 'Digital Foundry Architecture Breakdown', url: 'https://eurogamer.net' }
    ],
    image_url: '/images/gta6_cover.jpg',
    image_credit: 'Rockstar Games / GTA VI Artwork',
    hype: 96,
    trend_score: 980,
    views: 12400,
    is_breaking: true,
    indexable: true,
    status: 'published',
    published_at: new Date().toISOString()
  },
  {
    id: 'p2',
    niche_id: '3',
    slug: 'top-10-free-ai-tools-for-freelancers-2026',
    kind: 'article',
    title: '10 Best Free AI Productivity Tools for Indian Freelancers & Creators',
    summary: 'Boost workflow efficiency with top free and freemium AI tools for coding, writing, video rendering, and voiceovers.',
    body_md: `## Generative AI for Modern Freelancers\nArtificial intelligence has transitioned from experimental curiosity into essential daily utilities. Here are top-ranked productivity tools:\n\n### 1. Claude 3.7 & GPT-4o\nIdeal for complex logical programming, code debugging, and structuring high-converting proposals.\n\n### 2. ElevenLabs & Suno\nPremier audio synthesis and background audio design for YouTube Shorts and Instagram Reels.\n\n### 3. Perplexity AI\nReplacing standard web search with fast, cited, grounded research summaries.`,
    faq: [
      { q: 'Are these tools accessible on mobile?', a: 'Yes, all featured tools support mobile web apps and native Android/iOS applications.' }
    ],
    tags: ['AI Tools', 'Freelancing', 'Productivity'],
    sources: [
      { title: 'Hacker News AI Top Threads', url: 'https://news.ycombinator.com' }
    ],
    image_url: '/images/ai_tools.jpg',
    image_credit: 'AI Developer Studio Lab',
    hype: 84,
    trend_score: 850,
    views: 8900,
    is_breaking: false,
    indexable: true,
    status: 'published',
    published_at: new Date(Date.now() - 3600000 * 4).toISOString()
  },
  {
    id: 'p3',
    niche_id: '2',
    slug: '24k-gold-rate-analysis-festive-season-india',
    kind: 'article',
    title: '24K vs 22K Gold Rate Market Trends: What Buyers Must Check in 2026',
    summary: 'Everything you need to know about BIS 6-digit HUID hallmarking, making charges calculation, and MCX price movements.',
    body_md: `## Understanding Bullion Purity\nWhen purchasing gold in India, understanding the distinction between investment bullion and wearable ornaments is critical.\n\n### 24K vs 22K Hallmarking\n- **24 Karat (999 Purity):** Pure gold used for minted bars and investment coins.\n- **22 Karat (916 Purity):** Standard alloy with 91.6% purity used for durable jewellery.\n\n### Crucial Buying Checklist\nAlways verify the 6-digit alphanumeric HUID stamped on your jewellery via the official BIS Care app before making payment.`,
    faq: [
      { q: 'What is HUID in gold jewellery?', a: 'HUID is a unique 6-digit alphanumeric code laser-engraved on hallmarked gold items.' }
    ],
    tags: ['Gold Rate', 'Bullion', 'MCX India'],
    sources: [
      { title: 'Bureau of Indian Standards Guidelines', url: 'https://bis.gov.in' }
    ],
    image_url: '/images/gold_24k.jpg',
    image_credit: 'Bullion Market 999.9 Fine Gold',
    hype: 89,
    trend_score: 720,
    views: 6500,
    is_breaking: false,
    indexable: true,
    status: 'published',
    published_at: new Date(Date.now() - 3600000 * 12).toISOString()
  },
  {
    id: 'p4',
    niche_id: '1',
    slug: 'rtx-5090-india-benchmarks',
    kind: 'article',
    title: 'RTX 5090 India Real-World Benchmarks & Thermals',
    summary: 'Detailed test of RTX 5090 wattage, ray tracing performance, DLSS 4 frame generation, and India retail pricing expectations.',
    body_md: `## Next-Gen Blackwell Architecture Breakdown\nThe NVIDIA GeForce RTX 5090 represents an unprecedented generational leap in graphics horsepower.\n\n### Key Benchmark Highlights\n- Cyberpunk 2077 (4K Path Tracing): Exceeds 115 FPS with DLSS 4.\n- Black Myth Wukong (4K Cinematic): 98 FPS average with full ray tracing.\n- Thermals & Power Draw: Peak power consumption hovers around 575W.`,
    faq: [
      { q: 'What PSU wattage is needed for RTX 5090?', a: 'A high quality 1000W or 1200W ATX 3.1 certified power supply is strongly recommended.' }
    ],
    tags: ['RTX 5090', 'GPU', 'NVIDIA'],
    sources: [
      { title: 'NVIDIA Official Architecture Brief', url: 'https://nvidia.com' }
    ],
    image_url: '/images/rtx5090.jpg',
    image_credit: 'Founders Edition Lab Rig',
    hype: 98,
    trend_score: 950,
    views: 15600,
    is_breaking: true,
    indexable: true,
    status: 'published',
    published_at: new Date(Date.now() - 3600000 * 2).toISOString()
  }
];

export const SEED_PRODUCTS: Product[] = [
  {
    id: 'pr1',
    niche_id: '1',
    name: 'AMD Ryzen 7 7800X3D Processor',
    tagline: 'World’s Best Gaming CPU with 3D V-Cache',
    category: 'Processors',
    badge: 'Top Pick',
    keywords: 'ryzen cpu processor amd gaming pc 7800x3d',
    image_url: '/images/rtx5090.jpg',
    price: 36999,
    rating: 4.9,
    url: 'https://www.amazon.in/s?k=AMD+Ryzen+7+7800X3D+Processor',
    aff_url: 'https://www.amazon.in/s?k=AMD+Ryzen+7+7800X3D+Processor&tag=uniquedigi0c6-21',
    merchant: 'Amazon India',
    active: true,
    sort: 1
  },
  {
    id: 'pr2',
    niche_id: '1',
    name: 'Gigabyte GeForce RTX 4070 Super Eagle OC 12GB',
    tagline: '1440p Ultra Ray Tracing Powerhouse',
    category: 'Graphics Cards',
    badge: 'Best Value',
    keywords: 'gpu graphics card rtx 4070 nvidia gigabyte',
    image_url: '/images/rtx5090.jpg',
    price: 59990,
    rating: 4.8,
    url: 'https://www.amazon.in/s?k=Gigabyte+GeForce+RTX+4070+Super+12GB',
    aff_url: 'https://www.amazon.in/s?k=Gigabyte+GeForce+RTX+4070+Super+12GB&tag=uniquedigi0c6-21',
    merchant: 'Amazon India',
    active: true,
    sort: 2
  },
  {
    id: 'pr3',
    niche_id: '3',
    name: 'Cursor AI Code Editor Pro',
    tagline: 'Next-Generation AI-First IDE for Developers',
    category: 'Development',
    badge: 'Editor Choice',
    keywords: 'ai coding editor cursor claude gpt',
    image_url: '/images/ai_tools.jpg',
    price: 1650,
    rating: 4.9,
    url: 'https://cursor.com',
    aff_url: 'https://cursor.com/?ref=uniquedigit',
    merchant: 'Cursor',
    active: true,
    sort: 1
  }
];

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

/** 2. Get single niche by slug */
export async function getNicheBySlug(slug: string, runtimeEnv?: any): Promise<Niche | null> {
  const db = getD1(runtimeEnv);
  if (db && typeof db.prepare === 'function') {
    try {
      const row = await db.prepare('SELECT * FROM niches WHERE slug = ? AND active = 1 LIMIT 1').bind(slug).first();
      if (row) return mapNicheRow(row);
    } catch (err) {
      console.warn('[D1 getNicheBySlug fallback]:', err);
    }
  }
  const niches = await getNiches(runtimeEnv);
  return niches.find(n => n.slug === slug) || null;
}

/** 3. Get published posts for a niche with pagination support */
export async function getPostsByNiche(nicheId: string, limit = 12, runtimeEnv?: any, offset = 0): Promise<Post[]> {
  const db = getD1(runtimeEnv);
  if (db && typeof db.prepare === 'function') {
    try {
      const res = await db.prepare(
        'SELECT * FROM posts WHERE niche_id = ? AND status = "published" ORDER BY published_at DESC LIMIT ? OFFSET ?'
      ).bind(nicheId, limit, offset).all();
      if (res.results && res.results.length > 0) {
        return res.results.map((r: any) => mapPostRow(r));
      }
    } catch (err) {
      console.warn('[D1 getPostsByNiche fallback]:', err);
    }
  }
  return SEED_POSTS.filter(p => p.niche_id === nicheId || p.niches?.id === nicheId).slice(offset, offset + limit);
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
      console.warn('[D1 getPostsCountByNiche fallback]:', err);
    }
  }
  return SEED_POSTS.filter(p => p.niche_id === nicheId || p.niches?.id === nicheId).length;
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
      if (res.results && res.results.length > 0) {
        return res.results.map((r: any) => mapPostRow(r));
      }
    } catch (err) {
      console.warn('[D1 getTrendingPosts fallback]:', err);
    }
  }
  return [...SEED_POSTS].sort((a, b) => (b.hype || b.trend_score) - (a.hype || a.trend_score)).slice(0, limit);
}

/** 5. Get products / tools for a niche */
export async function getProductsByNiche(nicheId: string, runtimeEnv?: any): Promise<Product[]> {
  const db = getD1(runtimeEnv);
  if (db && typeof db.prepare === 'function') {
    try {
      const res = await db.prepare(
        'SELECT * FROM products WHERE niche_id = ? AND active = 1 ORDER BY sort ASC'
      ).bind(nicheId).all();
      if (res.results && res.results.length > 0) {
        return res.results as Product[];
      }
    } catch (err) {
      console.warn('[D1 getProductsByNiche fallback]:', err);
    }
  }
  return SEED_PRODUCTS.filter(pr => pr.niche_id === nicheId);
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
    } catch (err) {
      console.warn('[D1 getPost fallback]:', err);
    }
  }

  const p = SEED_POSTS.find(post => post.slug === postSlug);
  if (p) return { ...p, niches: niche };
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
