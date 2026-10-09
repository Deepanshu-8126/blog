import type { APIRoute } from 'astro';
import { getD1 } from '../../lib/db';

export const GET: APIRoute = async ({ request, locals }) => {
  const url = new URL(request.url);
  const q = url.searchParams.get('q')?.trim() || '';

  if (!q || q.length < 2) {
    return new Response(JSON.stringify({ results: [], query: q }), {
      status: 200,
      headers: {
        'Content-Type': 'application/json',
        'Cache-Control': 'public, max-age=60, s-maxage=120'
      }
    });
  }

  const runtime = (locals as any)?.runtime;
  const db = getD1(runtime?.env);

  if (!db) {
    return new Response(JSON.stringify({ results: [], error: 'Database unavailable' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }

  try {
    const searchPattern = `%${q}%`;
    const rows = await db.prepare(`
      SELECT 
        posts.id, posts.slug, posts.title, posts.summary, posts.image_url, 
        posts.hype, posts.views, posts.is_breaking, posts.published_at,
        niches.slug as niche_slug, niches.name as niche_name
      FROM posts
      LEFT JOIN niches ON posts.niche_id = niches.id
      WHERE (posts.title LIKE ? OR posts.summary LIKE ? OR posts.slug LIKE ?)
        AND posts.status = 'published'
      ORDER BY posts.hype DESC, posts.published_at DESC
      LIMIT 30
    `).bind(searchPattern, searchPattern, searchPattern).all();

    const results = (rows.results || []).map((r: any) => ({
      id: r.id,
      slug: r.slug,
      title: r.title,
      summary: r.summary,
      image_url: r.image_url,
      hype: r.hype,
      views: r.views,
      is_breaking: Boolean(r.is_breaking),
      published_at: r.published_at,
      niche_slug: r.niche_slug || 'viral',
      niche_name: r.niche_name || 'Viral'
    }));

    return new Response(JSON.stringify({ results, count: results.length, query: q }), {
      status: 200,
      headers: {
        'Content-Type': 'application/json',
        'Cache-Control': 'public, max-age=120, s-maxage=300'
      }
    });
  } catch (err: any) {
    return new Response(JSON.stringify({ results: [], error: err?.message || 'Search failed' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
};
