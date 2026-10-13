import type { APIRoute } from 'astro';

export const GET: APIRoute = async () => {
  return new Response('e8b912c47a504efea389127d40cb91af', {
    headers: {
      'Content-Type': 'text/plain; charset=utf-8',
      'Cache-Control': 'public, max-age=86400'
    }
  });
};
