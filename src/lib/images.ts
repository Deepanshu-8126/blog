/**
 * Edge Image Helper
 * Automatically routes remote Wikimedia, Wikipedia, and third-party media through
 * our local Cloudflare Worker /img proxy to eliminate 429 rate limits, bypass CORS/referrer blocks,
 * and provide immutable edge caching.
 */
export function proxyImageUrl(rawUrl?: string | null): string {
  if (!rawUrl || typeof rawUrl !== 'string') {
    return '/images/ai_tools.jpg';
  }

  const trimmed = rawUrl.trim();
  if (!trimmed || trimmed.length < 5) {
    return '/images/ai_tools.jpg';
  }

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
