import type { APIRoute } from 'astro';
import { getTrendingPosts } from '../lib/db';

function xmlEscape(str: string): string {
  if (!str) return '';
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

export const GET: APIRoute = async ({ request, locals }) => {
  const url = new URL(request.url);
  const host = request.headers.get('x-forwarded-host') || url.host;
  const baseUrl = `https://${host}`;
  const runtime = (locals as any)?.runtime;
  const posts = await getTrendingPosts(25, runtime?.env);
  const buildDate = new Date().toUTCString();

  const itemsXml = posts.map(p => {
    const slug = p.niches?.slug || 'viral';
    const rawUrl = `${baseUrl}/${slug}/${p.slug}`;
    const itemUrl = xmlEscape(rawUrl);
    const escapedImg = p.image_url ? xmlEscape(p.image_url) : '';
    const imageTag = escapedImg ? `
      <enclosure url="${escapedImg}" length="0" type="image/jpeg" />
      <media:content url="${escapedImg}" medium="image" />` : '';
    const safeTitle = (p.title || '').replace(/\]\]>/g, ']]&gt;');
    const safeSummary = (p.summary || '').replace(/\]\]>/g, ']]&gt;');

    return `    <item>
      <title><![CDATA[${safeTitle}]]></title>
      <link>${itemUrl}</link>
      <guid isPermaLink="true">${itemUrl}</guid>
      <pubDate>${new Date(p.published_at).toUTCString()}</pubDate>
      <description><![CDATA[${safeSummary}]]></description>
      <category>${xmlEscape(p.niches?.name || 'Tech')}</category>${imageTag}
    </item>`;
  }).join('\n');

  const rssXml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:media="http://search.yahoo.com/mrss/">
  <channel>
    <title>UniqueDigit - Viral Tech, Deals &amp; Real-Time Intelligence</title>
    <link>${baseUrl}</link>
    <description>Daily India tech trends, educational alerts, Sarkari results, and verified intelligence.</description>
    <language>en-in</language>
    <lastBuildDate>${buildDate}</lastBuildDate>
    <atom:link href="${baseUrl}/rss.xml" rel="self" type="application/rss+xml"/>
${itemsXml}
  </channel>
</rss>`;

  return new Response(rssXml.trim(), {
    headers: {
      'Content-Type': 'application/xml; charset=utf-8',
      'Cache-Control': 'public, max-age=1800, s-maxage=1800'
    }
  });
};
