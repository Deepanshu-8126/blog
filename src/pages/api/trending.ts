import type { APIRoute } from 'astro';
import { getBoard } from '../../lib/kv';

export const GET: APIRoute = async ({ locals }) => {
  try {
    const runtime = (locals as any)?.runtime;
    const board = await getBoard(runtime?.env);

    return new Response(JSON.stringify(board), {
      status: 200,
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'Cache-Control': 'public, s-maxage=60, stale-while-revalidate=120',
        'Access-Control-Allow-Origin': '*'
      }
    });
  } catch (err: any) {
    return new Response(JSON.stringify({ error: 'Failed to fetch trending data' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
};
