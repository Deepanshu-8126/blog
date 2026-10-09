import type { APIRoute } from 'astro';
import productsData from '../../../public/data/products.json';

export const GET: APIRoute = async ({ locals }) => {
  try {
    // 1. Check if Cloudflare R2 bucket binding exists in runtime context
    const runtime = (locals as any)?.runtime;
    const r2 = runtime?.env?.R2 || (globalThis as any)?.R2;

    if (r2 && typeof r2.get === 'function') {
      const obj = await r2.get('products/products.json');
      if (obj) {
        const text = await obj.text();
        return new Response(text, {
          status: 200,
          headers: {
            'Content-Type': 'application/json; charset=utf-8',
            'Cache-Control': 'public, max-age=60',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
          }
        });
      }
    }

    // 2. Local Fallback / Development Server response
    return new Response(JSON.stringify(productsData), {
      status: 200,
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'Cache-Control': 'public, max-age=60',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
      }
    });
  } catch (err: any) {
    // Graceful error fallback
    return new Response(JSON.stringify(productsData), {
      status: 200,
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'Access-Control-Allow-Origin': '*'
      }
    });
  }
};

export const OPTIONS: APIRoute = async () => {
  return new Response(null, {
    status: 204,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type'
    }
  });
};
