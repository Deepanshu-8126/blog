import type { APIRoute } from 'astro';

export const GET: APIRoute = async ({ request }) => {
  const url = new URL(request.url);
  const targetUrlStr = url.searchParams.get('url') || url.searchParams.get('u');

  if (!targetUrlStr) {
    return new Response(null, { status: 400 });
  }

  let targetUrl: URL;
  try {
    targetUrl = new URL(targetUrlStr);
  } catch {
    return new Response(null, { status: 400 });
  }

  // Gracefully redirect the browser directly to the image source with full CDN speed
  return Response.redirect(targetUrl.toString(), 302);
};
