import type { APIRoute } from 'astro';
import { subscribeNewsletter } from '../../lib/db';
import { verifyCsrfOrigin } from '../../lib/auth';

export const POST: APIRoute = async ({ request, locals }) => {
  try {
    if (!verifyCsrfOrigin(request)) {
      return new Response(JSON.stringify({ error: 'CSRF Origin Mismatch' }), {
        status: 403,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    const contentType = request.headers.get('content-type') || '';
    let email = '';
    let cfTurnstileToken = '';

    if (contentType.includes('application/json')) {
      const body = await request.json();
      email = body.email;
      cfTurnstileToken = body['cf-turnstile-response'] || '';
    } else {
      const formData = await request.formData();
      email = formData.get('email')?.toString() || '';
      cfTurnstileToken = formData.get('cf-turnstile-response')?.toString() || '';
    }

    const EMAIL_REGEX = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    email = email.trim().toLowerCase();

    if (!email || !EMAIL_REGEX.test(email) || email.length > 254) {
      return new Response(JSON.stringify({ error: 'Valid email is required' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    const runtime = (locals as any)?.runtime;
    const turnstileSecret = runtime?.env?.TURNSTILE_SECRET_KEY;
    const isDev = import.meta.env.DEV;

    // Fail-closed Turnstile security in production
    if (!isDev && turnstileSecret) {
      if (!cfTurnstileToken) {
        return new Response(JSON.stringify({ error: 'Bot verification token required' }), {
          status: 403,
          headers: { 'Content-Type': 'application/json' }
        });
      }

      const verifyRes = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `secret=${encodeURIComponent(turnstileSecret)}&response=${encodeURIComponent(cfTurnstileToken)}`
      });
      const verifyOutcome = await verifyRes.json() as any;
      if (!verifyOutcome.success) {
        return new Response(JSON.stringify({ error: 'Turnstile verification failed' }), {
          status: 403,
          headers: { 'Content-Type': 'application/json' }
        });
      }
    }

    const res = await subscribeNewsletter(email, runtime?.env);
    if (!res.success) {
      return new Response(JSON.stringify({ error: res.error || 'Failed to subscribe' }), {
        status: 500,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    return new Response(JSON.stringify({ success: true, message: 'Subscribed successfully!' }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    });
  } catch (err: any) {
    return new Response(JSON.stringify({ error: 'Internal server error' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
};
