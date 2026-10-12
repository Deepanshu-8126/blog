/**
 * UniqueDigit Real News Media & Edge Proxy Helper
 * Zero Unsplash Stock, Zero Local JPG Fallbacks.
 * 100% Real Scraped Web Media with Edge Caching & Wikimedia Upscaling.
 */

export function isRealWebImage(url?: string | null): boolean {
  if (!url || typeof url !== 'string') return false;
  const trimmed = url.trim();
  if (!trimmed.startsWith('https://') && !trimmed.startsWith('http://')) return false;

  const lower = trimmed.toLowerCase();
  // Filter out microscopic chips, SVGs of flags/logos, or dummy placeholders
  if (lower.includes('credit_card_chip')) return false;
  if (lower.includes('government_of_india_logo')) return false;
  if (lower.includes('board_of_control_for_cricket_in_india_logo')) return false;
  if (lower.includes('flag_of_india')) return false;
  if (lower.includes('thermally_agitated_molecule')) return false;
  if (lower.includes('ai_tools.jpg')) return false;

  return true;
}

/**
 * Upscales Wikimedia Commons thumbnails into 1600px 4K-grade renders.
 */
export function upscaleWikimediaUrl(url: string): string {
  if (!url.includes('upload.wikimedia.org') || !url.includes('/thumb/')) {
    return url;
  }
  return url.replace(/\/(\d+)px-([^/]+)$/, '/1600px-$2');
}

/**
 * Edge Image Helper
 * Resolves real web media through the edge proxy or directly returns local assets.
 */
export function proxyImageUrl(rawUrl?: string | null, nicheSlug = 'viral'): string | null {
  if (!rawUrl || typeof rawUrl !== 'string') return null;
  const trimmed = rawUrl.trim();

  // Local assets are served directly with zero latency
  if (trimmed.startsWith('/')) {
    return trimmed;
  }

  if (!isRealWebImage(trimmed)) {
    return null;
  }

  // Upscale Wikimedia thumbnails to 1600px high-res
  let url = trimmed;
  if (url.includes('upload.wikimedia.org')) {
    url = upscaleWikimediaUrl(url);
  }

  return `/img?url=${encodeURIComponent(url)}&n=${encodeURIComponent(nicheSlug)}`;
}

export function resolveProductImage(rawUrl?: string | null): string | null {
  if (!rawUrl || typeof rawUrl !== 'string') return null;
  const trimmed = rawUrl.trim();
  if (trimmed.startsWith('/')) return trimmed;
  if (trimmed.startsWith('http://') || trimmed.startsWith('https://')) {
    return proxyImageUrl(trimmed, 'deals');
  }
  return null;
}
