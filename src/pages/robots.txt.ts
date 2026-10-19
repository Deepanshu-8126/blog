import type { APIRoute } from 'astro';

export const GET: APIRoute = async ({ request }) => {
  const url = new URL(request.url);
  const host = request.headers.get('x-forwarded-host') || url.host;
  const baseUrl = `https://${host}`;

  const robots = `User-agent: *
Allow: /
Disallow: /api/
Disallow: /go/
Disallow: /admin/

Sitemap: ${baseUrl}/sitemap.xml
Sitemap: ${baseUrl}/sitemap.txt
Sitemap: ${baseUrl}/rss.xml
`;

  return new Response(robots, {
    headers: {
      'Content-Type': 'text/plain; charset=utf-8',
      'Cache-Control': 'public, max-age=86400'
    }
  });
};
