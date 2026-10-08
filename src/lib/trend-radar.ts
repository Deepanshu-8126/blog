/**
 * UniqueDigit Multi-Source Trend Radar Agent (Level 3 Automation)
 * Aggregates real-time trending signals across:
 * - Google Trends (India Realtime & Daily)
 * - Quick Commerce Deals (Blinkit, Zepto, Instamart, Amazon Lightning Deals)
 * - AI Tools & Prompt Libraries (HuggingFace, ProductHunt, GitHub Trends)
 * - Viral Social & Entertainment Buzz (TMDB, X/Reddit Tech Signals)
 */

export interface TrendSignal {
  id: string;
  source: 'google-trends' | 'quick-commerce' | 'ai-radar' | 'entertainment' | 'fashion-loot';
  title: string;
  category: string;
  nicheSlug: string;
  velocityScore: number; // 0 - 100
  merchant?: 'Amazon' | 'Blinkit' | 'Zepto' | 'Instamart' | 'Myntra' | 'EarnKaro';
  discountText?: string;
  verified: boolean;
  discoveredAt: string;
}

export const LIVE_RADAR_SEEDS: Record<string, string[]> = {
  'tech-gaming': ['RTX 5070', 'GTA 6 PC specs', 'Snapdragon 8 Elite', 'Ryzen 9800X3D', 'PS5 Pro India price'],
  'quick-deals': ['Blinkit midnight sale', 'Zepto 50% discount code', 'Amazon lightning deals electronics', 'Myntra sneaker loot under 999'],
  'ai-saas': ['DeepSeek v3', 'Claude 3.7 Sonnet', 'Cursor AI workflows', 'Sora release date', 'Midjourney v7 prompt library'],
  'lifestyle-wellness': ['Authentic Whey protein sale', 'Daily Gold rate Mumbai Delhi', 'Swiggy gourmet coupons', 'MakeMyTrip flight flash sale']
};

/**
 * Normalizes and categorizes raw trending queries into the 12 site niches
 */
export function classifyTrendSignal(rawQuery: string): { nicheSlug: string; category: string } {
  const q = rawQuery.toLowerCase();

  if (q.includes('gta') || q.includes('gaming') || q.includes('game') || q.includes('ps5') || q.includes('xbox')) {
    return { nicheSlug: 'gta-6', category: 'Gaming & Entertainment' };
  }
  if (q.includes('rtx') || q.includes('gpu') || q.includes('processor') || q.includes('ram') || q.includes('pc build') || q.includes('laptop')) {
    return { nicheSlug: 'pc-builds', category: 'PC Hardware & Tech' };
  }
  if (q.includes('ai') || q.includes('gpt') || q.includes('claude') || q.includes('prompt') || q.includes('deepseek') || q.includes('cursor')) {
    return { nicheSlug: 'ai-tools', category: 'AI Tools & Software' };
  }
  if (q.includes('gold') || q.includes('silver') || q.includes('bullion') || q.includes('24k') || q.includes('22k')) {
    return { nicheSlug: 'gold-rate', category: 'Precious Metals & Rates' };
  }
  if (q.includes('movie') || q.includes('ott') || q.includes('netflix') || q.includes('box office') || q.includes('trailer')) {
    return { nicheSlug: 'movies', category: 'Movies & OTT Releases' };
  }
  if (q.includes('protein') || q.includes('diet') || q.includes('workout') || q.includes('health') || q.includes('yoga')) {
    return { nicheSlug: 'health', category: 'Health & Wellness' };
  }
  if (q.includes('sneaker') || q.includes('myntra') || q.includes('ajio') || q.includes('fashion') || q.includes('shoes') || q.includes('watch')) {
    return { nicheSlug: 'fashion', category: 'Fashion & Loot Deals' };
  }
  if (q.includes('blinkit') || q.includes('zepto') || q.includes('swiggy') || q.includes('zomato') || q.includes('food') || q.includes('grocery')) {
    return { nicheSlug: 'food', category: 'Food & Quick Commerce Deals' };
  }
  if (q.includes('credit card') || q.includes('cashback') || q.includes('recharge') || q.includes('upi') || q.includes('bank')) {
    return { nicheSlug: 'cashback', category: 'Cashback & Bank Rewards' };
  }

  return { nicheSlug: 'deals', category: 'Today Top Discounts' };
}
