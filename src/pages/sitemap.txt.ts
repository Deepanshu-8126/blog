import type { APIRoute } from 'astro';
import { getNiches, getAllPublishedPosts } from '../lib/db';

export const GET: APIRoute = async ({ request, locals }) => {
  const url = new URL(request.url);
  const baseUrl = `${url.protocol}//${url.host}`;

  const runtime = (locals as any)?.runtime;
  const niches = await getNiches(runtime?.env);
  const posts = await getAllPublishedPosts(1000, runtime?.env);

  const staticUrls = [
    `${baseUrl}/`,
    `${baseUrl}/trending`,
    `${baseUrl}/smartphones`,
    `${baseUrl}/calculators`,
    `${baseUrl}/yojanas`,
    `${baseUrl}/cricket`,
    `${baseUrl}/builds`,
    `${baseUrl}/about`,
    `${baseUrl}/contact`,
    `${baseUrl}/privacy`,
    `${baseUrl}/terms`,
    `${baseUrl}/disclosure`,
    `${baseUrl}/disclaimer`,
  ];

  const nicheUrls = niches.map(n => `${baseUrl}/${n.slug}`);
  const indexablePosts = posts.filter(p => p.indexable !== false && p.kind !== 'card');
  const postUrls = indexablePosts.map(p => `${baseUrl}/${p.niches?.slug || 'viral'}/${p.slug}`);

  const allUrls = [...staticUrls, ...nicheUrls, ...postUrls];

  return new Response(allUrls.join('\n'), {
    headers: {
      'Content-Type': 'text/plain; charset=utf-8',
      'Cache-Control': 'public, max-age=3600, s-maxage=3600'
    }
  });
};
