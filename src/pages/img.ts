import type { APIRoute } from 'astro';

// Strict allowlist: Exactly Wikimedia and TMDB per File 6 / File 8 spec
const ALLOWED_HOSTS = new Set([
  'upload.wikimedia.org',
  'image.tmdb.org'
]);

export const GET: APIRoute = async ({ request }) => {
  const url = new URL(request.url);
  // Support both ?url= and ?u=
  const targetUrlStr = url.searchParams.get('url') || url.searchParams.get('u');

  if (!targetUrlStr) {
    return new Response('Missing url/u parameter', { status: 400 });
  }

  let targetUrl: URL;
  try {
    targetUrl = new URL(targetUrlStr);
  } catch {
    return new Response('Invalid url format', { status: 400 });
  }

  // Security: Exact hostname match only (prevents evil.com or subdomain trickery)
  if (!ALLOWED_HOSTS.has(targetUrl.hostname.toLowerCase())) {
    return new Response('Host not permitted (403 Forbidden)', { status: 403 });
  }

  // Protocol & Port check: Only HTTPS, standard port
  if (targetUrl.protocol !== 'https:' || (targetUrl.port && targetUrl.port !== '443')) {
    return new Response('Only standard HTTPS allowed', { status: 403 });
  }

  try {
    const upstreamRes = await fetch(targetUrl.toString(), {
      headers: {
        'User-Agent': 'UniqueDigit-Bot/2.0 (contact@uniquedigit.in; education/research)'
      },
      redirect: 'manual', // Prevent SSRF open-redirect bypass
      signal: AbortSignal.timeout(5000)
    });

    if (upstreamRes.status >= 300 && upstreamRes.status < 400) {
      return new Response('Upstream redirect not permitted (SSRF protection)', { status: 403 });
    }

    if (!upstreamRes.ok) {
      return new Response('Upstream fetch error', { status: upstreamRes.status });
    }

    const contentType = upstreamRes.headers.get('content-type') || '';
    if (!contentType.startsWith('image/')) {
      return new Response('Target resource is not an image', { status: 400 });
    }

    // Proxy with immutable cache
    return new Response(upstreamRes.body, {
      status: 200,
      headers: {
        'Content-Type': contentType,
        'Cache-Control': 'public, max-age=31536000, immutable',
        'Access-Control-Allow-Origin': '*'
      }
    });
  } catch (err: any) {
    return new Response('Proxy fetch failure', { status: 502 });
  }
};
