import type { APIRoute } from 'astro';
import { getNiches, getTrendingPosts } from '../lib/db';

export const GET: APIRoute = async ({ request, locals }) => {
  const url = new URL(request.url);
  const baseUrl = `${url.protocol}//${url.host}`;
  const currentDate = new Date().toISOString().split('T')[0];

  const runtime = (locals as any)?.runtime;
  const niches = await getNiches(runtime?.env);
  const posts = await getTrendingPosts(50, runtime?.env);

  const staticUrls = [
    { loc: `${baseUrl}/`, priority: '1.0', changefreq: 'daily' },
    { loc: `${baseUrl}/trending`, priority: '0.9', changefreq: 'hourly' },
    { loc: `${baseUrl}/builds`, priority: '0.85', changefreq: 'daily' },
    { loc: `${baseUrl}/about`, priority: '0.6', changefreq: 'monthly' },
    { loc: `${baseUrl}/contact`, priority: '0.6', changefreq: 'monthly' },
    { loc: `${baseUrl}/privacy`, priority: '0.5', changefreq: 'yearly' },
    { loc: `${baseUrl}/terms`, priority: '0.5', changefreq: 'yearly' },
    { loc: `${baseUrl}/disclosure`, priority: '0.5', changefreq: 'yearly' },
    { loc: `${baseUrl}/disclaimer`, priority: '0.5', changefreq: 'yearly' },
  ];

  const nicheUrls = niches.map(n => ({
    loc: `${baseUrl}/${n.slug}`,
    priority: '0.85',
    changefreq: 'daily'
  }));

  // File 6/8 Spec: Only indexable articles in sitemap (not raw trend cards)
  const indexablePosts = posts.filter(p => p.indexable !== false && p.kind !== 'card');

  const postUrls = indexablePosts.map(p => ({
    loc: `${baseUrl}/${p.niches?.slug || 'viral'}/${p.slug}`,
    priority: '0.80',
    changefreq: 'weekly',
    lastmod: (p.published_at && p.published_at.includes('T')) ? p.published_at.split('T')[0] : currentDate
  }));

  interface SitemapEntry {
    loc: string;
    priority: string;
    changefreq: string;
    lastmod?: string;
  }

  const allEntries: SitemapEntry[] = [...staticUrls, ...nicheUrls, ...postUrls];

  const sitemapXml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${allEntries.map(e => `  <url>
    <loc>${e.loc}</loc>
    <lastmod>${e.lastmod || currentDate}</lastmod>
    <changefreq>${e.changefreq}</changefreq>
    <priority>${e.priority}</priority>
  </url>`).join('\n')}
</urlset>`;

  return new Response(sitemapXml.trim(), {
    headers: {
      'Content-Type': 'application/xml; charset=utf-8',
      'Cache-Control': 'public, max-age=3600, s-maxage=3600'
    }
  });
};
