import type { APIRoute } from 'astro';

export const GET: APIRoute = async () => {
  return new Response('uniquedigit2026indexnow\n', {
    headers: {
      'Content-Type': 'text/plain; charset=utf-8',
      'Cache-Control': 'public, max-age=86400'
    }
  });
};
