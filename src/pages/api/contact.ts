import type { APIRoute } from 'astro';
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
    let name = '';
    let email = '';
    let subject = '';
    let message = '';

    if (contentType.includes('application/json')) {
      const body = await request.json();
      name = body.name?.trim() || '';
      email = body.email?.trim().toLowerCase() || '';
      subject = body.subject?.trim() || '';
      message = body.message?.trim() || '';
    } else {
      const formData = await request.formData();
      name = formData.get('name')?.toString().trim() || '';
      email = formData.get('email')?.toString().trim().toLowerCase() || '';
      subject = formData.get('subject')?.toString().trim() || '';
      message = formData.get('message')?.toString().trim() || '';
    }

    const EMAIL_REGEX = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    if (!name || name.length < 2 || name.length > 100) {
      return new Response(JSON.stringify({ error: 'Valid name is required (2-100 characters)' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    if (!email || !EMAIL_REGEX.test(email) || email.length > 254) {
      return new Response(JSON.stringify({ error: 'Valid email address is required' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    if (!message || message.length < 5 || message.length > 3000) {
      return new Response(JSON.stringify({ error: 'Message must be between 5 and 3000 characters' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    const runtime = (locals as any)?.runtime;
    const db = runtime?.env?.DB;
    const id = `contact_${Date.now().toString(36)}_${Math.random().toString(36).slice(2, 6)}`;
    const ip = request.headers.get('cf-connecting-ip') || 'unknown';
    const now = new Date().toISOString();

    if (db && typeof db.prepare === 'function') {
      await db.prepare(`
        INSERT INTO contact_submissions (id, name, email, subject, message, ip, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
      `).bind(id, name, email, subject || 'General Inquiry', message, ip, now).run();
    }

    return new Response(JSON.stringify({
      success: true,
      message: 'Thank you! Your inquiry has been received by the UniqueDigit desk.'
    }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    });
  } catch (err: any) {
    return new Response(JSON.stringify({
      error: 'Failed to process inquiry. Please try again later.'
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
};
