import { createClient } from '@supabase/supabase-js';

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
  };
  pin?: boolean;
  is_new?: boolean;
  sort?: number;
  active?: boolean;
}

export interface Post {
  id: string;
  niche_id: string;
  slug: string;
  title: string;
  summary: string;
  body_md: string;
  faq?: Array<{ q: string; a: string }>;
  tags?: string[];
  image_url?: string;
  image_credit?: string;
  source_url?: string;
  trend_score: number;
  views?: number;
  is_breaking?: boolean;
  status: 'published' | 'draft' | 'archived';
  published_at: string;
  niches?: Niche;
}

export interface Product {
  id: string;
  niche_id: string;
  name: string;
  tagline?: string;
  category?: string;
  badge?: string;
  image_url?: string;
  price?: number;
  rating?: number;
  url: string;
  aff_url?: string;
  merchant?: string;
  active?: boolean;
  sort?: number;
}

export interface DatasetEntry {
  id: string;
  niche_id: string;
  data: any;
  fetched_at: string;
}

// Fallback seed data if Supabase connection is not yet configured
export const SEED_NICHES: Niche[] = [
  { id: '1', slug: 'pc-builds', name: 'PC Builds', tagline: 'Custom rigs & parts', grp: 'Tech', icon: 'cpu', page_type: 'tools', pin: true, is_new: false, sort: 1, active: true },
  { id: '2', slug: 'gold-rate', name: 'Gold Rate', tagline: 'Live gold prices & trends', grp: 'Tech', icon: 'coins', page_type: 'dataset', pin: false, is_new: false, sort: 2, active: true, config: { disclaimer: 'Gold rates are indicative market rates and exclude GST and making charges.' } },
  { id: '3', slug: 'ai-tools', name: 'AI Tools', tagline: 'Generative AI & utilities', grp: 'Tech', icon: 'sparkles', page_type: 'tools', pin: true, is_new: false, sort: 3, active: true },
  { id: '4', slug: 'deals', name: 'Deals', tagline: "Today's top discounts", grp: 'Money', icon: 'tag', page_type: 'tools', pin: true, is_new: false, sort: 4, active: true },
  { id: '5', slug: 'side-hustles', name: 'Side Hustles', tagline: 'Earn extra income', grp: 'Money', icon: 'briefcase', page_type: 'feed', pin: false, is_new: false, sort: 5, active: true },
  { id: '6', slug: 'cashback', name: 'Cashback', tagline: 'Rewards & cashback offers', grp: 'Money', icon: 'percent', page_type: 'tools', pin: false, is_new: false, sort: 6, active: true },
  { id: '7', slug: 'health', name: 'Health', tagline: 'Wellness & fitness tips', grp: 'Lifestyle', icon: 'heart', page_type: 'feed', pin: false, is_new: false, sort: 7, active: true, config: { review: true, disclaimer: 'Yeh jankari sirf education ke liye hai, medical salah nahi. Kisi bhi upchar se pehle doctor se consult karein.' } },
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
    title: 'GTA 6 PC Specs & Realistic India Pricing: What System Do You Need?',
    summary: 'Comprehensive analysis of expected PC requirements for Grand Theft Auto VI, ray tracing hardware demands, and build cost in India.',
    body_md: `## GTA 6 PC Hardware Demands\nRockstar Games title Grand Theft Auto VI is expected to set a new benchmark in open-world graphics simulation. With advanced ray-traced global illumination and complex crowd AI, hardware selection is paramount.\n\n### Minimum vs Recommended Hardware\n- **Target 1080p 60FPS:** AMD Ryzen 5 7600X or Intel Core i5-13600K paired with NVIDIA RTX 4060 Ti / AMD Radeon RX 7700 XT.\n- **Target 1440p / 4K Ultra:** AMD Ryzen 7 7800X3D and NVIDIA GeForce RTX 4080 Super.\n\n### Storage & Memory\nA minimum of 32GB DDR5 RAM is strongly advised along with high-speed NVMe Gen4 SSD storage to avoid texture streaming bottlenecks.`,
    faq: [
      { q: 'Will GTA 6 run on 16GB RAM?', a: 'While 16GB might meet minimum specs, 32GB RAM will prevent stutters in dense city areas.' },
      { q: 'When is GTA 6 releasing on PC?', a: 'PC release is expected following the initial console launch.' }
    ],
    tags: ['GTA 6', 'Gaming PC', 'Rockstar Games'],
    image_url: 'https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&w=1200&q=80',
    image_credit: 'Unsplash / Gaming Rig',
    trend_score: 980,
    views: 12400,
    is_breaking: true,
    status: 'published',
    published_at: new Date().toISOString()
  },
  {
    id: 'p2',
    niche_id: '3',
    slug: 'top-10-free-ai-tools-for-freelancers-2026',
    title: '10 Best Free AI Productivity Tools for Indian Freelancers & Creators',
    summary: 'Boost workflow efficiency with top free and freemium AI tools for coding, writing, video rendering, and voiceovers.',
    body_md: `## Generative AI for Modern Freelancers\nArtificial intelligence has transitioned from experimental curiosity into essential daily utilities. Here are top-ranked productivity tools:\n\n### 1. Claude 3.7 & GPT-4o\nIdeal for complex logical programming, code debugging, and structuring high-converting proposals.\n\n### 2. ElevenLabs & Suno\nPremier audio synthesis and background audio design for YouTube Shorts and Instagram Reels.\n\n### 3. Perplexity AI\nReplacing standard web search with fast, cited, grounded research summaries.`,
    faq: [
      { q: 'Are these tools accessible on mobile?', a: 'Yes, all featured tools support mobile web apps and native Android/iOS applications.' }
    ],
    tags: ['AI Tools', 'Freelancing', 'Productivity'],
    image_url: 'https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=1200&q=80',
    image_credit: 'Unsplash / AI Brain',
    trend_score: 850,
    views: 8900,
    is_breaking: false,
    status: 'published',
    published_at: new Date(Date.now() - 3600000 * 4).toISOString()
  },
  {
    id: 'p3',
    niche_id: '2',
    slug: '24k-gold-rate-analysis-festive-season-india',
    title: '24K vs 22K Gold Rate Market Trends: What Buyers Must Check in 2026',
    summary: 'Everything you need to know about BIS 6-digit HUID hallmarking, making charges calculation, and MCX price movements.',
    body_md: `## Understanding Bullion Purity\nWhen purchasing gold in India, understanding the distinction between investment bullion and wearable ornaments is critical.\n\n### 24K vs 22K Hallmarking\n- **24 Karat (999 Purity):** Pure gold used for minted bars and investment coins.\n- **22 Karat (916 Purity):** Standard alloy with 91.6% purity used for durable jewellery.\n\n### Crucial Buying Checklist\nAlways verify the 6-digit alphanumeric HUID stamped on your jewellery via the official BIS Care app before making payment.`,
    faq: [
      { q: 'What is HUID in gold jewellery?', a: 'HUID is a unique 6-digit alphanumeric code laser-engraved on hallmarked gold items.' }
    ],
    tags: ['Gold Rate', 'Bullion', 'MCX India'],
    image_url: 'https://images.unsplash.com/photo-1610375461246-83df859d849d?auto=format&fit=crop&w=1200&q=80',
    image_credit: 'Unsplash / Gold Bullion',
    trend_score: 720,
    views: 6500,
    is_breaking: false,
    status: 'published',
    published_at: new Date(Date.now() - 3600000 * 12).toISOString()
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
    image_url: 'https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?auto=format&fit=crop&w=600&q=80',
    price: 36999,
    rating: 4.9,
    url: 'https://www.amazon.in/dp/B0BTZB7F88',
    aff_url: 'https://www.amazon.in/dp/B0BTZB7F88?tag=uniquedigi0c6-21',
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
    image_url: 'https://images.unsplash.com/photo-1587202372775-e229f172b9d7?auto=format&fit=crop&w=600&q=80',
    price: 59990,
    rating: 4.8,
    url: 'https://www.amazon.in/dp/B0CS9K4X6K',
    aff_url: 'https://www.amazon.in/dp/B0CS9K4X6K?tag=uniquedigi0c6-21',
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
    image_url: 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=600&q=80',
    price: 1650,
    rating: 4.9,
    url: 'https://cursor.com',
    aff_url: 'https://cursor.com/?ref=uniquedigit',
    merchant: 'Cursor',
    active: true,
    sort: 1
  }
];

// Supabase client instance
const supabaseUrl = import.meta.env.PUBLIC_SUPABASE_URL || '';
const supabaseAnonKey = import.meta.env.PUBLIC_SUPABASE_ANON_KEY || '';

export const supabase = (supabaseUrl && supabaseAnonKey)
  ? createClient(supabaseUrl, supabaseAnonKey)
  : null;

// =========================================================
// 6 Core Query Helpers (F1 to F8)
// =========================================================

/** 1. Get all active niches for MegaMenu and Routes */
export async function getNiches(): Promise<Niche[]> {
  if (!supabase) return SEED_NICHES;
  try {
    const { data, error } = await supabase
      .from('niches')
      .select('*')
      .eq('active', true)
      .order('sort', { ascending: true });
    if (error || !data || data.length === 0) return SEED_NICHES;
    return data as Niche[];
  } catch {
    return SEED_NICHES;
  }
}

/** 2. Get single niche by slug */
export async function getNicheBySlug(slug: string): Promise<Niche | null> {
  const niches = await getNiches();
  return niches.find(n => n.slug === slug) || null;
}

/** 3. Get published posts for a niche */
export async function getPostsByNiche(nicheId: string, limit = 12): Promise<Post[]> {
  if (!supabase) {
    return SEED_POSTS.filter(p => p.niche_id === nicheId || p.niches?.id === nicheId).slice(0, limit);
  }
  try {
    const { data, error } = await supabase
      .from('posts')
      .select('*, niches(*)')
      .eq('niche_id', nicheId)
      .eq('status', 'published')
      .order('published_at', { ascending: false })
      .limit(limit);
    if (error || !data || data.length === 0) {
      return SEED_POSTS.filter(p => p.niche_id === nicheId).slice(0, limit);
    }
    return data as Post[];
  } catch {
    return SEED_POSTS.filter(p => p.niche_id === nicheId).slice(0, limit);
  }
}

/** 4. Get trending posts across all niches (last 24h) */
export async function getTrendingPosts(limit = 5): Promise<Post[]> {
  if (!supabase) {
    return [...SEED_POSTS].sort((a, b) => b.trend_score - a.trend_score).slice(0, limit);
  }
  try {
    const { data, error } = await supabase
      .from('posts')
      .select('*, niches(*)')
      .eq('status', 'published')
      .order('trend_score', { ascending: false })
      .limit(limit);
    if (error || !data || data.length === 0) {
      return [...SEED_POSTS].sort((a, b) => b.trend_score - a.trend_score).slice(0, limit);
    }
    return data as Post[];
  } catch {
    return [...SEED_POSTS].sort((a, b) => b.trend_score - a.trend_score).slice(0, limit);
  }
}

/** 5. Get products / tools for a niche */
export async function getProductsByNiche(nicheId: string): Promise<Product[]> {
  if (!supabase) {
    return SEED_PRODUCTS.filter(pr => pr.niche_id === nicheId);
  }
  try {
    const { data, error } = await supabase
      .from('products')
      .select('*')
      .eq('niche_id', nicheId)
      .eq('active', true)
      .order('sort', { ascending: true });
    if (error || !data || data.length === 0) {
      return SEED_PRODUCTS.filter(pr => pr.niche_id === nicheId);
    }
    return data as Product[];
  } catch {
    return SEED_PRODUCTS.filter(pr => pr.niche_id === nicheId);
  }
}

/** 6. Get post by niche slug and post slug */
export async function getPost(nicheSlug: string, postSlug: string): Promise<Post | null> {
  const niche = await getNicheBySlug(nicheSlug);
  if (!niche) return null;

  if (!supabase) {
    const p = SEED_POSTS.find(post => post.slug === postSlug);
    if (p) return { ...p, niches: niche };
    return null;
  }

  try {
    const { data, error } = await supabase
      .from('posts')
      .select('*, niches(*)')
      .eq('niche_id', niche.id)
      .eq('slug', postSlug)
      .eq('status', 'published')
      .single();
    return data as Post;
  } catch {
    const p = SEED_POSTS.find(post => post.slug === postSlug);
    if (p) return { ...p, niches: niche };
    return null;
  }
}

