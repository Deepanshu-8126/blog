import type { APIRoute } from 'astro';
import { CATEGORY_FALLBACK_IMAGES } from '../lib/images';

function isAllowedHost(hostname: string): boolean {
  const h = hostname.toLowerCase();
  return (
    // Wikimedia & Wikipedia
    h.endsWith('.wikimedia.org') ||
    h.endsWith('.wikipedia.org') ||
    h === 'image.tmdb.org' ||
    // Google & News Wire
    h.endsWith('.gstatic.com') ||
    h.endsWith('.googleusercontent.com') ||
    // High-Res Photography CDNs
    h.endsWith('.unsplash.com') ||
    h.endsWith('.pexels.com') ||
    h.endsWith('.pixabay.com') ||
    h.endsWith('.imgur.com') ||
    h.endsWith('.ytimg.com') ||
    h.endsWith('.youtube.com') ||
    // E-commerce CDNs
    h.endsWith('.media-amazon.com') ||
    h.endsWith('.ssl-images-amazon.com') ||
    h.endsWith('.amazon.com') ||
    h.endsWith('.flixcart.com') ||
    h.endsWith('.myntassets.com') ||
    h.endsWith('.meesho.com') ||
    h.endsWith('.ajio.com') ||
    h.endsWith('.tatacliq.com') ||
    // Indian News & Media Publishers
    h.endsWith('.ndtvimg.com') ||
    h.endsWith('.indianexpress.com') ||
    h.endsWith('.hindustantimes.com') ||
    h.endsWith('.livemint.com') ||
    h.endsWith('.toiimg.com') ||
    h.endsWith('.indiatimes.com') ||
    h.endsWith('.tosshub.com') ||
    h.endsWith('.etimg.com') ||
    h.endsWith('.hscicdn.com') ||
    h.endsWith('.cricbuzz.com') ||
    h.endsWith('.moneycontrol.com') ||
    h.endsWith('.firstpost.com') ||
    h.endsWith('.thehindu.com') ||
    h.endsWith('.news18.com') ||
    h.endsWith('.abplive.com') ||
    h.endsWith('.jagranimages.com') ||
    h.endsWith('.bhaskarassets.com') ||
    h.endsWith('.ptinews.com') ||
    h.endsWith('.ani-news.com') ||
    h.endsWith('.reuters.com') ||
    h.endsWith('.bbci.co.uk') ||
    h.endsWith('.cnn.com') ||
    h.endsWith('.rottentomatoes.com') ||
    h.endsWith('.uniquedigit.in')
  );
}

function getSafeFallbackUrl(nicheSlug?: string | null): string {
  const slug = (nicheSlug || 'viral').toLowerCase();
  return CATEGORY_FALLBACK_IMAGES[slug] || CATEGORY_FALLBACK_IMAGES['viral'];
}

export const GET: APIRoute = async ({ request }) => {
  const url = new URL(request.url);
  const targetUrlStr = url.searchParams.get('url') || url.searchParams.get('u');
  const nicheSlug = url.searchParams.get('n') || url.searchParams.get('niche');
  const fallback = getSafeFallbackUrl(nicheSlug);

  if (!targetUrlStr) {
    return Response.redirect(fallback, 302);
  }

  let targetUrl: URL;
  try {
    targetUrl = new URL(targetUrlStr);
  } catch {
    return Response.redirect(fallback, 302);
  }

  // Security: Host allowlist
  if (!isAllowedHost(targetUrl.hostname) || targetUrl.protocol !== 'https:') {
    return Response.redirect(fallback, 302);
  }

  try {
    const upstreamRes = await fetch(targetUrl.toString(), {
      headers: {
        'User-Agent': 'UniqueDigitBot/2.0 (https://uniquedigit.in; contact@uniquedigit.in)'
      },
      redirect: 'follow',
      signal: AbortSignal.timeout(8000)
    });

    if (!upstreamRes.ok) {
      return Response.redirect(fallback, 302);
    }

    const contentType = upstreamRes.headers.get('content-type') || 'image/jpeg';

    return new Response(upstreamRes.body, {
      status: 200,
      headers: {
        'Content-Type': contentType,
        'Cache-Control': 'public, max-age=604800, s-maxage=2592000, immutable',
        'Access-Control-Allow-Origin': '*'
      }
    });
  } catch (err: any) {
    return Response.redirect(fallback, 302);
  }
};
