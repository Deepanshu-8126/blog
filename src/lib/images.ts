/**
 * UniqueDigit Real News Media & Direct Image Helper
 * Zero Stock, Zero Local JPG Fallbacks.
 * 100% Real Scraped Web Media with 4K Direct Edge Streaming & Browser Security Headers.
 */

export function isRealWebImage(url?: string | null): boolean {
  if (!url || typeof url !== 'string') return false;
  const trimmed = url.trim();
  if (!trimmed.startsWith('https://') && !trimmed.startsWith('http://')) return false;

  const lower = trimmed.toLowerCase();
  // Strict permanent bans on generic fallbacks & synthetic illustrators
  if (lower.includes('unsplash.com')) return false;
  if (lower.includes('robinhood.com')) return false;
  if (lower.includes('telesco.pe')) return false;
  if (lower.includes('pollinations.ai')) return false;
  if (lower.includes('placeholder')) return false;

  // Filter out microscopic chips, SVGs of flags/logos, or dummy placeholders
  if (lower.includes('credit_card_chip')) return false;
  if (lower.includes('government_of_india_logo')) return false;
  if (lower.includes('board_of_control_for_cricket_in_india_logo')) return false;
  if (lower.includes('flag_of_india')) return false;
  if (lower.includes('thermally_agitated_molecule')) return false;
  if (lower.includes('ai_tools.jpg')) return false;
  // Filter out low-res 100px Google Trends thumbnail scraps
  if (lower.includes('encrypted-tbn') || lower.includes('gstatic.com/images?q=tbn')) return false;

  return true;
}

/**
 * Normalizes Wikimedia Commons thumbnails to strictly supported standard sizes (500px/960px).
 * Prevents HTTP 400 Bad Request error from Wikimedia size validation.
 */
export function upscaleWikimediaUrl(url: string): string {
  if ((!url.includes('upload.wikimedia.org') && !url.includes('thumb.wikimedia.org')) || !url.includes('/thumb/')) {
    return url;
  }
  // SVG-derived PNGs must remain at 500px standard size
  if (url.includes('.svg/')) {
    return url.replace(/\/(\d+)px-([^/]+)$/, '/500px-$2');
  }
  // Standard raster JPG/PNG upgraded to valid production 960px width
  return url.replace(/\/(\d+)px-([^/]+)$/, '/960px-$2');
}

/**
 * Image URL Resolver — Pure Structural Logic
 * Routes images through /img edge proxy.
 * If rawUrl is missing, invalid, or empty, routes to /img?title=...&niche=...
 * which dynamically generates a sleek vector SVG card with ZERO external storage or hardcoded links.
 */
export function proxyImageUrl(rawUrl?: string | null, nicheSlug = 'viral', slugOrTitle = ''): string {
  const titleParam = encodeURIComponent(slugOrTitle || 'UniqueDigit');
  const nicheParam = encodeURIComponent(nicheSlug || 'viral');

  if (!rawUrl || typeof rawUrl !== 'string') {
    return `/img?title=${titleParam}&niche=${nicheParam}`;
  }

  const trimmed = rawUrl.trim();
  if (trimmed.startsWith('/')) {
    return trimmed;
  }

  if (!isRealWebImage(trimmed)) {
    return `/img?title=${titleParam}&niche=${nicheParam}`;
  }

  let url = trimmed;
  if (url.startsWith('http://')) {
    url = url.replace('http://', 'https://');
  }

  if (url.includes('upload.wikimedia.org') || url.includes('thumb.wikimedia.org')) {
    url = upscaleWikimediaUrl(url);
  }

  return `/img?url=${encodeURIComponent(url)}&title=${titleParam}&niche=${nicheParam}`;
}

export function resolveProductImage(rawUrl?: string | null, name = '', category = ''): string {
  const title = name || category || 'Product Deal';
  if (!rawUrl || typeof rawUrl !== 'string') {
    return `/img?title=${encodeURIComponent(title)}&niche=deals`;
  }
  const trimmed = rawUrl.trim();
  if (!trimmed || !isRealWebImage(trimmed)) {
    return `/img?title=${encodeURIComponent(title)}&niche=deals`;
  }
  return proxyImageUrl(trimmed, 'deals', title);
}
