import type { APIRoute } from 'astro';
import { getTrendingPosts } from '../lib/db';

export const GET: APIRoute = async ({ request, locals }) => {
  const url = new URL(request.url);
  const baseUrl = `${url.protocol}//${url.host}`;
  const runtime = (locals as any)?.runtime;
  const posts = await getTrendingPosts(20, runtime?.env);
  const buildDate = new Date().toUTCString();

  const itemsXml = posts.map(p => {
    const slug = p.niches?.slug || 'viral';
    const itemUrl = `${baseUrl}/${slug}/${p.slug}`;
    return `    <item>
      <title><![CDATA[${p.title}]]></title>
      <link>${itemUrl}</link>
      <guid isPermaLink="true">${itemUrl}</guid>
      <pubDate>${new Date(p.published_at).toUTCString()}</pubDate>
      <description><![CDATA[${p.summary}]]></description>
      <category>${p.niches?.name || 'Tech'}</category>
    </item>`;
  }).join('\n');

  const rssXml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>UniqueDigit — Viral Tech, Deals &amp; Real-Time Intelligence</title>
    <link>${baseUrl}</link>
    <description>Daily India tech trends, hardware benchmarks, AI tools directory, and bullion pricing.</description>
    <language>en-in</language>
    <lastBuildDate>${buildDate}</lastBuildDate>
    <atom:link href="${baseUrl}/rss.xml" rel="self" type="application/rss+xml"/>
${itemsXml}
  </channel>
</rss>`;

  return new Response(rssXml, {
    headers: {
      'Content-Type': 'application/xml; charset=utf-8',
      'Cache-Control': 'public, max-age=3600, s-maxage=3600'
    }
  });
};
