import type { APIRoute } from 'astro';

function isAllowedHost(hostname: string): boolean {
  const h = hostname.toLowerCase();
  return (
    h.endsWith('.wikimedia.org') ||
    h.endsWith('.wikipedia.org') ||
    h === 'image.tmdb.org' ||
    h.endsWith('.gstatic.com') ||
    h.endsWith('.googleusercontent.com') ||
    h.endsWith('.unsplash.com') ||
    h.endsWith('.media-amazon.com') ||
    h.endsWith('.flixcart.com') ||
    h.endsWith('.myntassets.com') ||
    h.endsWith('.meesho.com') ||
    h.endsWith('.ajio.com') ||
    h.endsWith('.uniquedigit.in')
  );
}

export const GET: APIRoute = async ({ request }) => {
  const url = new URL(request.url);
  const targetUrlStr = url.searchParams.get('url') || url.searchParams.get('u');

  if (!targetUrlStr) {
    return Response.redirect(new URL('/images/ai_tools.jpg', request.url).toString(), 302);
  }

  let targetUrl: URL;
  try {
    targetUrl = new URL(targetUrlStr);
  } catch {
    return Response.redirect(new URL('/images/ai_tools.jpg', request.url).toString(), 302);
  }

  // Security: Host allowlist
  if (!isAllowedHost(targetUrl.hostname) || targetUrl.protocol !== 'https:') {
    return Response.redirect(new URL('/images/ai_tools.jpg', request.url).toString(), 302);
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
      return Response.redirect(new URL('/images/ai_tools.jpg', request.url).toString(), 302);
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
    return Response.redirect(new URL('/images/ai_tools.jpg', request.url).toString(), 302);
  }
};
