import type { APIRoute } from 'astro';
import { getProductById, trackProductClick } from '../../lib/db';

export const GET: APIRoute = async ({ params, locals, redirect }) => {
  const { id } = params;
  if (!id) {
    return new Response('Product ID missing', { status: 404 });
  }

  const runtime = (locals as any)?.runtime;
  const product = await getProductById(id, runtime?.env);

  // If product does not exist in DB, strictly return 404
  if (!product) {
    return new Response('Affiliate link target not found', { status: 404 });
  }

  const destination = product.aff_url || product.url;
  if (!destination) {
    return new Response('Affiliate destination missing', { status: 404 });
  }

  // Security: Ensure destination is a valid external URL
  try {
    const parsed = new URL(destination);
    if (!['http:', 'https:'].includes(parsed.protocol)) {
      return new Response('Invalid destination protocol', { status: 400 });
    }
  } catch {
    return new Response('Invalid destination format', { status: 400 });
  }

  // Track click asynchronously without blocking redirect
  if (runtime?.ctx?.waitUntil) {
    runtime.ctx.waitUntil(trackProductClick(id, runtime.env));
  } else {
    trackProductClick(id, runtime?.env).catch(() => {});
  }

  return redirect(destination, 302);
};
