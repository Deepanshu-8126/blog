/**
 * Edge Image Helper
 * Automatically routes remote Wikimedia, Wikipedia, and third-party media through
 * our local Cloudflare Worker /img proxy to eliminate 429 rate limits, bypass CORS/referrer blocks,
 * and provide immutable edge caching.
 */
export const CATEGORY_FALLBACK_IMAGES: Record<string, string> = {
  'movies': 'https://upload.wikimedia.org/wikipedia/en/d/d9/Drishyam-_The_Conclusion_poster.jpg',
  'cricket-sports': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/Board_of_Control_for_Cricket_in_India_Logo_%282024%29.svg/960px-Board_of_Control_for_Cricket_in_India_Logo_%282024%29.svg.png',
  'pc-builds': '/images/rtx5090.jpg',
  'gta-6': '/images/gta6_cover.jpg',
  'ai-tools': '/images/ai_tools.jpg',
  'gold-rate': '/images/gold_24k.jpg',
  'deals': '/images/products/iphone_16_pro.jpg',
  'cashback': 'https://upload.wikimedia.org/wikipedia/commons/2/2a/Credit_Card_Chip_%2834684294971%29.jpg',
  'food': 'https://upload.wikimedia.org/wikipedia/commons/e/ef/Tradtional_Thali.jpg',
  'health': 'https://upload.wikimedia.org/wikipedia/commons/b/b0/Beach_asana_class%2C_Plage_Pereire%2C_Arcachon%2C_2015.jpg',
  'fashion': 'https://upload.wikimedia.org/wikipedia/commons/a/a6/Carolina_Herrera_AW14_12.jpg',
  'automotive-trends': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Tata_Nexon_Blue_Dual_Tone.jpg/960px-Tata_Nexon_Blue_Dual_Tone.jpg',
  'exams-results': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Government_of_India_logo.svg/960px-Government_of_India_logo.svg.png',
  'viral': 'https://upload.wikimedia.org/wikipedia/en/a/a1/Stree_2.jpg'
};

export function proxyImageUrl(rawUrl?: string | null, nicheSlug?: string): string {
  let target = rawUrl;
  if (!target || typeof target !== 'string' || target.trim().length < 5) {
    target = (nicheSlug && CATEGORY_FALLBACK_IMAGES[nicheSlug]) || '/images/ai_tools.jpg';
  }

  const trimmed = target.trim();

  // Already local or data URI
  if (trimmed.startsWith('/') || trimmed.startsWith('data:')) {
    return trimmed;
  }

  // Route remote media through edge proxy
  if (trimmed.startsWith('http://') || trimmed.startsWith('https://')) {
    return `/img?url=${encodeURIComponent(trimmed)}`;
  }

  return trimmed;
}
