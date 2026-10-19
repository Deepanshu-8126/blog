import type { APIRoute } from 'astro';

export const GET: APIRoute = async () => {
  const baseUrl = 'https://uniquedigit-viral-hub.pages.dev';

  const robots = `# UniqueDigit Production Autonomous Sentinel (Verified: 2026)
User-agent: *
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
