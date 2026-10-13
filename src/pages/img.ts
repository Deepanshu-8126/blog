import type { APIRoute } from 'astro';

function generateSvgFallback(title = 'UniqueDigit Editorial', niche = 'Trending'): string {
  const safeTitle = (title || 'UniqueDigit Trending').replace(/[<>&"]/g, '');
  const safeNiche = (niche || 'EDITORIAL').toUpperCase().replace(/[<>&"]/g, '');
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 675" width="1200" height="675">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0f172a" />
      <stop offset="50%" stop-color="#1e1b4b" />
      <stop offset="100%" stop-color="#311042" />
    </linearGradient>
    <linearGradient id="badgeGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#38bdf8" />
      <stop offset="100%" stop-color="#818cf8" />
    </linearGradient>
  </defs>
  <rect width="1200" height="675" fill="url(#bgGrad)" />
  <circle cx="150" cy="120" r="280" fill="#38bdf8" opacity="0.08" />
  <circle cx="1050" cy="550" r="320" fill="#f43f5e" opacity="0.08" />
  
  <rect x="80" y="80" width="220" height="42" rx="21" fill="rgba(255,255,255,0.08)" stroke="rgba(255,255,255,0.15)" stroke-width="1" />
  <text x="190" y="106" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="800" fill="#38bdf8" text-anchor="middle" letter-spacing="1.5">⚡ ${safeNiche}</text>
  
  <text x="80" y="320" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="50" font-weight="900" fill="#ffffff">
    <tspan x="80" dy="0">${safeTitle.slice(0, 40)}</tspan>
    ${safeTitle.length > 40 ? `<tspan x="80" dy="65">${safeTitle.slice(40, 80)}...</tspan>` : ''}
  </text>
  
  <rect x="80" y="550" width="1040" height="1" fill="rgba(255,255,255,0.12)" />
  <text x="80" y="585" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="15" font-weight="600" fill="#94a3b8" letter-spacing="1">UNIQUEDIGIT VIRAL HUB • 100% VERIFIED EDITORIAL WIRE</text>
</svg>`;
}

export const GET: APIRoute = async ({ request }) => {
  const url = new URL(request.url);
  const targetUrlStr = url.searchParams.get('url') || url.searchParams.get('u');
  const title = url.searchParams.get('title') || 'UniqueDigit Editorial';
  const niche = url.searchParams.get('niche') || 'Trending';

  if (!targetUrlStr) {
    return new Response(generateSvgFallback(title, niche), {
      headers: {
        'Content-Type': 'image/svg+xml; charset=utf-8',
        'Cache-Control': 'public, max-age=86400, s-maxage=86400'
      }
    });
  }

  let targetUrl: URL;
  try {
    targetUrl = new URL(targetUrlStr);
  } catch {
    return new Response(generateSvgFallback(title, niche), {
      headers: {
        'Content-Type': 'image/svg+xml; charset=utf-8',
        'Cache-Control': 'public, max-age=86400, s-maxage=86400'
      }
    });
  }

  // Ensure HTTPS
  if (targetUrl.protocol === 'http:') {
    targetUrl.protocol = 'https:';
  }

  // Fix Wikimedia non-standard sizes that return 400
  let fetchUrl = targetUrl.toString();
  if (fetchUrl.includes('wikimedia.org') && fetchUrl.includes('/thumb/')) {
    // Non-standard sizes 1024px, 800px, 1200px replaced by standard 960px or 500px
    fetchUrl = fetchUrl.replace(/\/1024px-([^/]+)$/, '/960px-$1');
    fetchUrl = fetchUrl.replace(/\/800px-([^/]+)$/, '/960px-$1');
    fetchUrl = fetchUrl.replace(/\/1200px-([^/]+)$/, '/960px-$1');
  }

  const isWikimedia = fetchUrl.includes('wikimedia.org') || fetchUrl.includes('wikipedia.org');
  const reqHeaders: Record<string, string> = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8'
  };
  if (isWikimedia) {
    reqHeaders['Referer'] = 'https://en.wikipedia.org/';
  }

  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 6000);

    const res = await fetch(fetchUrl, {
      headers: reqHeaders,
      signal: controller.signal
    });
    clearTimeout(timeoutId);

    if (res.ok) {
      const contentType = res.headers.get('content-type') || 'image/jpeg';
      const arrayBuffer = await res.arrayBuffer();

      if (arrayBuffer.byteLength > 200) {
        return new Response(arrayBuffer, {
          headers: {
            'Content-Type': contentType,
            'Cache-Control': 'public, max-age=604800, s-maxage=604800, immutable',
            'Access-Control-Allow-Origin': '*'
          }
        });
      }
    }
  } catch (err) {
    // Fetch failed, proceed to fallback
  }

  // Return bulletproof SVG fallback if remote image returns 400/403/404/429
  return new Response(generateSvgFallback(title, niche), {
    headers: {
      'Content-Type': 'image/svg+xml; charset=utf-8',
      'Cache-Control': 'public, max-age=86400, s-maxage=86400',
      'Access-Control-Allow-Origin': '*'
    }
  });
};
