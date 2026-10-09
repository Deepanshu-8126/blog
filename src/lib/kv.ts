export interface TrendItem {
  id: string;
  title: string;
  slug: string;
  hype: number;
  growth: number;
  stage: 'emerging' | 'hot' | 'peak' | 'cooling' | 'gone';
  n: number;
  sources: string[];
  spark: number[];
  niche?: string;
  niche_slug?: string;
  approx_traffic?: string;
  updated_at?: string;
  post_slug?: string;
  post_kind?: 'card' | 'article';
  deal_product?: {
    id: string;
    name: string;
    aff_url: string;
    price?: number;
  };
}

export const SEED_TRENDS: TrendItem[] = [
  {
    id: 't1',
    title: 'GTA 6 PC Specs & Realistic System Requirements India',
    slug: 'gta-6-pc-specs-release-date-india-pricing',
    hype: 96,
    growth: 0.08,
    stage: 'peak',
    n: 4,
    sources: ['gtrends', 'youtube', 'gnews', 'wiki'],
    spark: [65, 72, 78, 85, 90, 94, 96],
    niche: 'Entertainment',
    niche_slug: 'gta-6',
    approx_traffic: '500K+',
    updated_at: new Date(Date.now() - 1000 * 60 * 4).toISOString(),
    post_slug: 'gta-6-pc-specs-release-date-india-pricing',
    post_kind: 'article',
    deal_product: {
      id: 'pr2',
      name: 'GeForce RTX 4070 Super 12GB',
      aff_url: 'https://www.amazon.in/dp/B0CS9K4X6K?tag=uniquedigi0c6-21',
      price: 59990
    }
  },
  {
    id: 't2',
    title: '24K Gold Rate Hits New High in MCX Market Today',
    slug: '24k-gold-rate-analysis-festive-season-india',
    hype: 89,
    growth: 0.12,
    stage: 'hot',
    n: 3,
    sources: ['gtrends', 'gnews', 'wiki'],
    spark: [68, 70, 75, 80, 84, 87, 89],
    niche: 'Tech',
    niche_slug: 'gold-rate',
    approx_traffic: '250K+',
    updated_at: new Date(Date.now() - 1000 * 60 * 8).toISOString(),
    post_slug: '24k-gold-rate-analysis-festive-season-india',
    post_kind: 'article'
  },
  {
    id: 't3',
    title: 'Claude 3.7 & DeepSeek V3: Best Free AI Tools for Coders',
    slug: 'top-10-free-ai-tools-for-freelancers-2026',
    hype: 84,
    growth: 0.19,
    stage: 'hot',
    n: 3,
    sources: ['hn', 'gnews', 'wiki'],
    spark: [42, 54, 62, 71, 78, 81, 84],
    niche: 'Tech',
    niche_slug: 'ai-tools',
    approx_traffic: '120K+',
    updated_at: new Date(Date.now() - 1000 * 60 * 12).toISOString(),
    post_slug: 'top-10-free-ai-tools-for-freelancers-2026',
    post_kind: 'article',
    deal_product: {
      id: 'pr3',
      name: 'Cursor AI Pro Subscription',
      aff_url: 'https://cursor.com/?ref=uniquedigit',
      price: 1650
    }
  },
  {
    id: 't4',
    title: 'Amazon Great Indian Festival Tech & Laptop Early Deals',
    slug: 'amazon-great-indian-festival-loot-deals',
    hype: 78,
    growth: 0.15,
    stage: 'hot',
    n: 2,
    sources: ['gtrends', 'gnews'],
    spark: [50, 58, 64, 69, 72, 75, 78],
    niche: 'Money',
    niche_slug: 'deals',
    approx_traffic: '180K+',
    updated_at: new Date(Date.now() - 1000 * 60 * 15).toISOString(),
    deal_product: {
      id: 'pr1',
      name: 'AMD Ryzen 7 7800X3D Processor',
      aff_url: 'https://www.amazon.in/dp/B0BTZB7F88?tag=uniquedigi0c6-21',
      price: 36999
    }
  },
  {
    id: 't5',
    title: 'Ryzen 7 7800X3D Price Cut: Best Gaming CPU Under ₹35,000',
    slug: 'ryzen-7800x3d-price-drop-india',
    hype: 75,
    growth: 0.22,
    stage: 'peak',
    n: 3,
    sources: ['gtrends', 'youtube', 'hn'],
    spark: [35, 45, 52, 60, 68, 72, 75],
    niche: 'Tech',
    niche_slug: 'pc-builds',
    approx_traffic: '80K+',
    updated_at: new Date(Date.now() - 1000 * 60 * 10).toISOString(),
    deal_product: {
      id: 'pr1',
      name: 'AMD Ryzen 7 7800X3D',
      aff_url: 'https://www.amazon.in/dp/B0BTZB7F88?tag=uniquedigi0c6-21',
      price: 36999
    }
  },
  {
    id: 't6',
    title: 'Flipkart Cashback Credit Card Hacks for Big Billion Days',
    slug: 'flipkart-cashback-credit-card-tricks',
    hype: 69,
    growth: 0.11,
    stage: 'emerging',
    n: 2,
    sources: ['gtrends', 'gnews'],
    spark: [40, 48, 55, 60, 64, 67, 69],
    niche: 'Money',
    niche_slug: 'cashback',
    approx_traffic: '90K+',
    updated_at: new Date(Date.now() - 1000 * 60 * 20).toISOString()
  },
  {
    id: 't7',
    title: 'Pushpa 2 & Stree 2 OTT Release Date and Platform Confirmed',
    slug: 'pushpa-2-stree-2-ott-release-date',
    hype: 65,
    growth: -0.25,
    stage: 'cooling',
    n: 3,
    sources: ['tmdb', 'youtube', 'gnews'],
    spark: [92, 88, 81, 76, 71, 68, 65],
    niche: 'Entertainment',
    niche_slug: 'movies',
    approx_traffic: '150K+',
    updated_at: new Date(Date.now() - 1000 * 60 * 25).toISOString()
  },
  {
    id: 't8',
    title: 'Top 5 Legit Remote Side Hustles for College Students in India',
    slug: 'remote-side-hustles-students-india',
    hype: 61,
    growth: 0.14,
    stage: 'emerging',
    n: 2,
    sources: ['gtrends', 'youtube'],
    spark: [30, 38, 44, 49, 53, 58, 61],
    niche: 'Money',
    niche_slug: 'side-hustles',
    approx_traffic: '45K+',
    updated_at: new Date(Date.now() - 1000 * 60 * 18).toISOString()
  },
  {
    id: 't9',
    title: 'Intermittent Fasting 16:8 Protocol for Rapid Weight Loss',
    slug: 'intermittent-fasting-guide-india',
    hype: 57,
    growth: 0.05,
    stage: 'emerging',
    n: 2,
    sources: ['wiki', 'gtrends'],
    spark: [48, 50, 52, 54, 55, 56, 57],
    niche: 'Lifestyle',
    niche_slug: 'health',
    approx_traffic: '35K+',
    updated_at: new Date(Date.now() - 1000 * 60 * 22).toISOString()
  },
  {
    id: 't10',
    title: 'Oversized Streetwear Hoodies & Sneakers Style Trends 2026',
    slug: 'oversized-streetwear-sneakers-india',
    hype: 54,
    growth: 0.08,
    stage: 'emerging',
    n: 2,
    sources: ['gtrends', 'youtube'],
    spark: [32, 38, 42, 46, 49, 52, 54],
    niche: 'Lifestyle',
    niche_slug: 'fashion',
    approx_traffic: '40K+',
    updated_at: new Date(Date.now() - 1000 * 60 * 14).toISOString()
  },
  {
    id: 't11',
    title: 'High Protein Vegetarian Diet Plan for Indian Gym Goers',
    slug: 'high-protein-veg-diet-indian-fitness',
    hype: 52,
    growth: 0.06,
    stage: 'emerging',
    n: 2,
    sources: ['gtrends', 'wiki'],
    spark: [36, 40, 43, 46, 49, 51, 52],
    niche: 'Lifestyle',
    niche_slug: 'food',
    approx_traffic: '28K+',
    updated_at: new Date(Date.now() - 1000 * 60 * 16).toISOString()
  },
  {
    id: 't12',
    title: 'Latest Viral Internet Meme Sensation Taking Over Reels',
    slug: 'viral-internet-meme-breakdown-india',
    hype: 48,
    growth: -0.15,
    stage: 'cooling',
    n: 2,
    sources: ['youtube', 'gtrends'],
    spark: [78, 70, 62, 56, 52, 50, 48],
    niche: 'Entertainment',
    niche_slug: 'viral',
    approx_traffic: '60K+',
    updated_at: new Date(Date.now() - 1000 * 60 * 28).toISOString()
  }
];

export interface BoardsPayload {
  sig: string;
  global: TrendItem[];
  niches?: Record<string, TrendItem[]>;
  updated_at?: string;
}

export async function getBoardsPayload(runtimeEnv?: any): Promise<BoardsPayload | null> {
  try {
    const kv = runtimeEnv?.KV || (globalThis as any)?.KV;
    if (kv && typeof kv.get === 'function') {
      // 1. Primary single combined key
      const data = await kv.get('boards:v1', { type: 'json' });
      if (data && typeof data === 'object' && Array.isArray((data as any).global)) {
        return data as BoardsPayload;
      }
      // 2. Legacy fallback if boards:v1 not yet populated
      const legacy = await kv.get('board:IN', { type: 'json' });
      if (Array.isArray(legacy) && legacy.length > 0) {
        return {
          sig: 'legacy',
          global: legacy as TrendItem[],
          niches: {},
          updated_at: legacy[0]?.updated_at
        };
      }
    }
  } catch (err) {
    console.warn('[KV getBoardsPayload error]:', err);
  }
  return null;
}

export async function getBoard(runtimeEnv?: any): Promise<TrendItem[]> {
  const payload = await getBoardsPayload(runtimeEnv);
  if (payload && Array.isArray(payload.global) && payload.global.length > 0) {
    return payload.global;
  }
  return SEED_TRENDS;
}

export async function getNicheBoard(nicheSlug: string, runtimeEnv?: any): Promise<TrendItem[]> {
  const payload = await getBoardsPayload(runtimeEnv);
  if (payload?.niches && Array.isArray(payload.niches[nicheSlug]) && payload.niches[nicheSlug].length > 0) {
    return payload.niches[nicheSlug];
  }
  if (payload && Array.isArray(payload.global) && payload.global.length > 0) {
    const filtered = payload.global.filter(t => t.niche_slug === nicheSlug);
    if (filtered.length > 0) return filtered;
  }
  return SEED_TRENDS.filter(t => t.niche_slug === nicheSlug);
}

export async function getHomeBoard(runtimeEnv?: any): Promise<{ hero: TrendItem | null; top5: TrendItem[]; latest: TrendItem[] }> {
  const board = await getBoard(runtimeEnv);
  return {
    hero: board[0] || SEED_TRENDS[0] || null,
    top5: board.slice(0, 5),
    latest: board.slice(5, 12)
  };
}
