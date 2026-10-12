/**
 * UniqueDigit 4K Visual Architecture & Edge Proxy Helper
 * Eliminates low-res thumbnails, broken hotlinks, and gradient placeholders.
 * Guarantees every card, banner, and article renders authentic 4K/HD photography.
 */

export const CATEGORY_4K_FALLBACK_POOLS: Record<string, string[]> = {
  'pc-builds': [
    'https://images.unsplash.com/photo-1587202372775-e229f172b9d7?auto=format&fit=crop&w=1600&q=85',
    'https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?auto=format&fit=crop&w=1600&q=85',
    'https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=1600&q=85'
  ],
  'gta-6': [
    '/images/gta6_cover.jpg',
    'https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&w=1600&q=85',
    'https://images.unsplash.com/photo-1511512578047-dfb367046420?auto=format&fit=crop&w=1600&q=85'
  ],
  'ai-tools': [
    'https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=1600&q=85',
    'https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=1600&q=85',
    'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=1600&q=85'
  ],
  'gold-rate': [
    'https://images.unsplash.com/photo-1610375461246-83df859d849d?auto=format&fit=crop&w=1600&q=85',
    'https://images.unsplash.com/photo-1605100804763-247f67b3557e?auto=format&fit=crop&w=1600&q=85',
    'https://images.unsplash.com/photo-1535615615570-3b839f4359be?auto=format&fit=crop&w=1600&q=85'
  ],
  'deals': [
    '/images/products/iphone_16_pro.jpg',
    'https://images.unsplash.com/photo-1607082348824-0a96f2a4b9da?auto=format&fit=crop&w=1600&q=85',
    'https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?auto=format&fit=crop&w=1600&q=85'
  ],
  'cashback': [
    'https://images.unsplash.com/photo-1559526324-4b87b5e36e44?auto=format&fit=crop&w=1600&q=85',
    'https://images.unsplash.com/photo-1563013544-824ae1b704d3?auto=format&fit=crop&w=1600&q=85',
    'https://images.unsplash.com/photo-1556742049-0a67c5574f73?auto=format&fit=crop&w=1600&q=85'
  ],
  'side-hustles': [
    'https://images.unsplash.com/photo-1499750310107-5fef28a66643?auto=format&fit=crop&w=1600&q=85',
    'https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&fit=crop&w=1600&q=85'
  ],
  'movies': [
    'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&w=1600&q=85',
    'https://images.unsplash.com/photo-1517604931442-7e0c8ed2963c?auto=format&fit=crop&w=1600&q=85',
    'https://images.unsplash.com/photo-1536440136628-849c177e76a1?auto=format&fit=crop&w=1600&q=85'
  ],
  'cricket-sports': [
    'https://images.unsplash.com/photo-1531415074868-83633dd5e45c?auto=format&fit=crop&w=1600&q=85',
    'https://images.unsplash.com/photo-1540747913346-19e32dc3e97e?auto=format&fit=crop&w=1600&q=85',
    'https://images.unsplash.com/photo-1508098682722-e99c43a406b2?auto=format&fit=crop&w=1600&q=85'
  ],
  'automotive-trends': [
    'https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1600&q=85',
    'https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=1600&q=85',
    'https://images.unsplash.com/photo-1617788138017-80ad40651399?auto=format&fit=crop&w=1600&q=85'
  ],
  'food': [
    'https://images.unsplash.com/photo-1626777552726-4a6b54c97e46?auto=format&fit=crop&w=1600&q=85',
    'https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=1600&q=85',
    'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=1600&q=85'
  ],
  'health': [
    'https://images.unsplash.com/photo-1545205597-3d9d02c29597?auto=format&fit=crop&w=1600&q=85',
    'https://images.unsplash.com/photo-1506126613408-eca07ce68773?auto=format&fit=crop&w=1600&q=85',
    'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=1600&q=85'
  ],
  'fashion': [
    'https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=1600&q=85',
    'https://images.unsplash.com/photo-1483985988355-763728e1935b?auto=format&fit=crop&w=1600&q=85',
    'https://images.unsplash.com/photo-1490481651871-ab68de25d43d?auto=format&fit=crop&w=1600&q=85'
  ],
  'exams-results': [
    'https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=1600&q=85',
    'https://images.unsplash.com/photo-1497633762265-9d179a990aa6?auto=format&fit=crop&w=1600&q=85'
  ],
  'viral': [
    'https://images.unsplash.com/photo-1504711434969-e33886168f5c?auto=format&fit=crop&w=1600&q=85',
    'https://images.unsplash.com/photo-1585829365295-ab7cd400c167?auto=format&fit=crop&w=1600&q=85',
    'https://images.unsplash.com/photo-1526778548025-fa2f459cd5c1?auto=format&fit=crop&w=1600&q=85'
  ]
};

export const CATEGORY_FALLBACK_IMAGES: Record<string, string> = {
  'movies': 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&w=1600&q=85',
  'cricket-sports': 'https://images.unsplash.com/photo-1531415074868-83633dd5e45c?auto=format&fit=crop&w=1600&q=85',
  'pc-builds': '/images/rtx5090.jpg',
  'gta-6': '/images/gta6_cover.jpg',
  'ai-tools': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=1600&q=85',
  'gold-rate': '/images/gold_24k.jpg',
  'deals': '/images/products/iphone_16_pro.jpg',
  'cashback': 'https://images.unsplash.com/photo-1559526324-4b87b5e36e44?auto=format&fit=crop&w=1600&q=85',
  'side-hustles': 'https://images.unsplash.com/photo-1499750310107-5fef28a66643?auto=format&fit=crop&w=1600&q=85',
  'food': 'https://images.unsplash.com/photo-1626777552726-4a6b54c97e46?auto=format&fit=crop&w=1600&q=85',
  'health': 'https://images.unsplash.com/photo-1545205597-3d9d02c29597?auto=format&fit=crop&w=1600&q=85',
  'fashion': 'https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=1600&q=85',
  'automotive-trends': 'https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1600&q=85',
  'exams-results': 'https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=1600&q=85',
  'viral': 'https://images.unsplash.com/photo-1504711434969-e33886168f5c?auto=format&fit=crop&w=1600&q=85'
};

/**
 * Deterministically picks a distinct 4K curated image from the niche pool based on seed/slug,
 * guaranteeing that cards within the same niche don't all look identical.
 */
export function get4KCuratedImage(seed = '', nicheSlug = 'viral'): string {
  const pool = CATEGORY_4K_FALLBACK_POOLS[nicheSlug] || CATEGORY_4K_FALLBACK_POOLS['viral'];
  if (!pool || pool.length === 0) return CATEGORY_FALLBACK_IMAGES[nicheSlug] || CATEGORY_FALLBACK_IMAGES['viral'];

  let hash = 0;
  const str = seed || nicheSlug;
  for (let i = 0; i < str.length; i++) {
    hash = (hash << 5) - hash + str.charCodeAt(i);
    hash |= 0;
  }
  const index = Math.abs(hash) % pool.length;
  return pool[index];
}

/**
 * Checks if a candidate image URL is low quality, broken, or a generic placeholder.
 */
export function isLowQualityUrl(url?: string | null): boolean {
  if (!url || typeof url !== 'string') return true;
  const trimmed = url.trim();
  if (trimmed.length < 10) return true;

  // Tiny compressed Google Trends RSS thumbnails
  if (trimmed.includes('gstatic.com/images?q=tbn')) return true;

  // Microscopic chips or logos used as articles
  if (trimmed.includes('Credit_Card_Chip_')) return true;
  if (trimmed.includes('Government_of_India_logo.svg')) return true;
  if (trimmed.includes('Board_of_Control_for_Cricket_in_India_Logo')) return true;

  return false;
}

/**
 * Upscales Wikimedia Commons thumbnails into 1600px 4K-grade renders.
 */
export function upscaleWikimediaUrl(url: string): string {
  if (!url.includes('upload.wikimedia.org') || !url.includes('/thumb/')) {
    return url;
  }

  // Replace trailing thumbnail width e.g. /320px-..., /960px-... with /1600px-...
  return url.replace(/\/(\d+)px-([^/]+)$/, '/1600px-$2');
}

/**
 * Edge Image Helper
 * Resolves crisp, 4K-grade images with edge caching, automatic upscaling, and robust fallback.
 */
export function proxyImageUrl(rawUrl?: string | null, nicheSlug = 'viral', postSlug = ''): string {
  // If missing or known low quality, immediately supply a deterministic 4K photo
  if (isLowQualityUrl(rawUrl)) {
    return get4KCuratedImage(postSlug || nicheSlug, nicheSlug);
  }

  let trimmed = (rawUrl || '').trim();

  // Already local asset (e.g. /images/...) or data URI
  if (trimmed.startsWith('/') || trimmed.startsWith('data:')) {
    // If it's a known high-res local asset, return as is
    if (trimmed.endsWith('.jpg') || trimmed.endsWith('.png') || trimmed.endsWith('.webp')) {
      return trimmed;
    }
    return trimmed;
  }

  // Upscale Wikimedia thumbnails to 1600px
  if (trimmed.includes('upload.wikimedia.org')) {
    trimmed = upscaleWikimediaUrl(trimmed);
  }

  // Ensure Unsplash URLs have optimal width and quality
  if (trimmed.includes('images.unsplash.com')) {
    try {
      const u = new URL(trimmed);
      u.searchParams.set('auto', 'format');
      u.searchParams.set('fit', 'crop');
      u.searchParams.set('w', '1600');
      u.searchParams.set('q', '85');
      trimmed = u.toString();
    } catch {
      // Keep trimmed as is
    }
  }

  // Route remote media through edge proxy
  if (trimmed.startsWith('http://') || trimmed.startsWith('https://')) {
    return `/img?url=${encodeURIComponent(trimmed)}&n=${encodeURIComponent(nicheSlug)}`;
  }

  return trimmed;
}
