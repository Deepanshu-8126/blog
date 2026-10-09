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
    title: '24K Gold Rate Today in India (MCX Spot & City Bullion Prices)',
    slug: '24k-gold-rate-analysis-festive-season-india',
    hype: 98,
    growth: 0.16,
    stage: 'peak',
    n: 4,
    sources: ['gtrends', 'gnews', 'wiki'],
    spark: [75, 80, 84, 88, 92, 95, 98],
    niche: 'Tech & Market',
    niche_slug: 'gold-rate',
    approx_traffic: '650K+',
    updated_at: new Date(Date.now() - 1000 * 60 * 3).toISOString(),
    post_slug: '24k-gold-rate-analysis-festive-season-india',
    post_kind: 'article'
  },
  {
    id: 't2',
    title: 'Claude 3.5 Sonnet & Cursor AI: Best Free AI Tools for Indian Coders',
    slug: 'top-10-free-ai-tools-for-freelancers-2026',
    hype: 95,
    growth: 0.22,
    stage: 'hot',
    n: 4,
    sources: ['hn', 'gnews', 'wiki'],
    spark: [60, 68, 75, 82, 88, 92, 95],
    niche: 'AI & Software',
    niche_slug: 'ai-tools',
    approx_traffic: '320K+',
    updated_at: new Date(Date.now() - 1000 * 60 * 6).toISOString(),
    post_slug: 'top-10-free-ai-tools-for-freelancers-2026',
    post_kind: 'article',
    deal_product: {
      id: 'pr3',
      name: 'Cursor AI Pro IDE',
      aff_url: 'https://cursor.com/?ref=uniquedigit',
      price: 1650
    }
  },
  {
    id: 't3',
    title: 'Best Cashback Credit Cards in India (2026): 5% Flat Savings',
    slug: 'best-cashback-credit-cards-india-2026',
    hype: 92,
    growth: 0.18,
    stage: 'hot',
    n: 3,
    sources: ['gtrends', 'gnews'],
    spark: [55, 64, 72, 80, 85, 89, 92],
    niche: 'Money & Cards',
    niche_slug: 'cashback',
    approx_traffic: '280K+',
    updated_at: new Date(Date.now() - 1000 * 60 * 8).toISOString(),
    post_slug: 'best-cashback-credit-cards-india-2026',
    post_kind: 'article',
    deal_product: {
      id: 'pr_sbi_cashback',
      name: 'SBI Cashback Credit Card',
      aff_url: 'https://www.sbicard.com',
      price: 999
    }
  },
  {
    id: 't4',
    title: 'RTX 5090 & RTX 4070 Super: Real-World Gaming Benchmarks in India',
    slug: 'rtx-5090-india-benchmarks',
    hype: 89,
    growth: 0.14,
    stage: 'hot',
    n: 3,
    sources: ['gtrends', 'youtube', 'hn'],
    spark: [62, 70, 76, 81, 84, 87, 89],
    niche: 'Hardware & PC',
    niche_slug: 'pc-builds',
    approx_traffic: '190K+',
    updated_at: new Date(Date.now() - 1000 * 60 * 11).toISOString(),
    post_slug: 'rtx-5090-india-benchmarks',
    post_kind: 'article',
    deal_product: {
      id: 'pr_rtx_4070_super',
      name: 'GeForce RTX 4070 Super 12GB',
      aff_url: 'https://www.amazon.in/s?k=RTX+4070+Super+Graphics+Card&tag=uniquedigi0c6-21',
      price: 59990
    }
  },
  {
    id: 't5',
    title: '100g Daily Protein: Practical Indian Vegetarian Meal Prep Plan',
    slug: 'high-protein-vegetarian-indian-diet-plan',
    hype: 86,
    growth: 0.12,
    stage: 'hot',
    n: 3,
    sources: ['gtrends', 'gnews', 'wiki'],
    spark: [50, 60, 68, 74, 80, 83, 86],
    niche: 'Health & Diet',
    niche_slug: 'food',
    approx_traffic: '210K+',
    updated_at: new Date(Date.now() - 1000 * 60 * 14).toISOString(),
    post_slug: 'high-protein-vegetarian-indian-diet-plan',
    post_kind: 'article'
  },
  {
    id: 't6',
    title: 'GTA 6 PC Specs & Realistic System Requirements India',
    slug: 'gta-6-pc-specs-release-date-india-pricing',
    hype: 84,
    growth: 0.08,
    stage: 'hot',
    n: 4,
    sources: ['gtrends', 'youtube', 'gnews', 'wiki'],
    spark: [65, 72, 76, 79, 81, 83, 84],
    niche: 'Gaming',
    niche_slug: 'gta-6',
    approx_traffic: '500K+',
    updated_at: new Date(Date.now() - 1000 * 60 * 18).toISOString(),
    post_slug: 'gta-6-pc-specs-release-date-india-pricing',
    post_kind: 'article'
  },
  {
    id: 't7',
    title: 'Top 7 High-Income Remote Side Hustles in India for 2026',
    slug: 'top-7-remote-side-hustles-india-2026',
    hype: 80,
    growth: 0.15,
    stage: 'emerging',
    n: 2,
    sources: ['gtrends', 'youtube'],
    spark: [40, 50, 59, 68, 73, 77, 80],
    niche: 'Money & Careers',
    niche_slug: 'side-hustles',
    approx_traffic: '140K+',
    updated_at: new Date(Date.now() - 1000 * 60 * 22).toISOString(),
    post_slug: 'top-7-remote-side-hustles-india-2026',
    post_kind: 'article'
  },
  {
    id: 't8',
    title: 'Weekend OTT Watchlist: Top Movies & Crime Series Streaming Now',
    slug: 'upcoming-ott-releases-friday-india',
    hype: 76,
    growth: 0.10,
    stage: 'emerging',
    n: 3,
    sources: ['tmdb', 'youtube', 'gnews'],
    spark: [45, 52, 60, 66, 70, 73, 76],
    niche: 'Entertainment',
    niche_slug: 'movies',
    approx_traffic: '180K+',
    updated_at: new Date(Date.now() - 1000 * 60 * 25).toISOString(),
    post_slug: 'upcoming-ott-releases-friday-india',
    post_kind: 'article'
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
