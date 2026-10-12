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
 * Resolves real web media through the edge proxy.
 * Returns null if no real web media exists, allowing the UI to render an authentic CSS gradient card.
 */
export function proxyImageUrl(rawUrl?: string | null, nicheSlug = 'viral'): string | null {
  if (!isRealWebImage(rawUrl)) {
    return null;
  }

  let trimmed = rawUrl!.trim();

  // Upscale Wikimedia thumbnails to 1600px high-res
  if (trimmed.includes('upload.wikimedia.org')) {
    trimmed = upscaleWikimediaUrl(trimmed);
  }

  return `/img?url=${encodeURIComponent(trimmed)}&n=${encodeURIComponent(nicheSlug)}`;
}
