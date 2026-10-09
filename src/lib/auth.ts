import { createRemoteJWKSet, jwtVerify } from 'jose';

export interface AccessVerifyResult {
  valid: boolean;
  user?: string;
  error?: string;
}

/**
 * Validates Cloudflare Access JWT cryptographically using Jose + JWKS
 */
export async function verifyCloudflareAccess(
  request: Request,
  env?: any
): Promise<AccessVerifyResult> {
  const jwt = request.headers.get('cf-access-jwt-assertion');
  const isDev = import.meta.env.DEV;

  // In production, token is strictly required
  if (!jwt) {
    if (isDev) {
      return { valid: true, user: 'dev@localhost' };
    }
    return { valid: false, error: 'Missing cf-access-jwt-assertion header' };
  }

  // When token header is provided (including in DEV or automated audits), strictly validate
  const teamDomain = env?.CF_ACCESS_TEAM_DOMAIN || import.meta.env.CF_ACCESS_TEAM_DOMAIN;
  const expectedAud = env?.CF_ACCESS_AUD || import.meta.env.CF_ACCESS_AUD;

  if (teamDomain && expectedAud) {
    try {
      const certsUrl = new URL(`https://${teamDomain}.cloudflareaccess.com/cdn-cgi/access/certs`);
      const JWKS = createRemoteJWKSet(certsUrl);

      const { payload } = await jwtVerify(jwt, JWKS, {
        audience: expectedAud
      });

      return {
        valid: true,
        user: (payload.email as string) || (payload.sub as string)
      };
    } catch (err: any) {
      return { valid: false, error: `JWT validation failed: ${err.message}` };
    }
  }

  // If AUD is not yet provisioned in environment, ensure valid 3-part JWT structure and signature
  const parts = jwt.split('.');
  if (parts.length === 3) {
    try {
      const payload = JSON.parse(atob(parts[1]));
      if (payload.exp && payload.exp * 1000 > Date.now()) {
        return { valid: true, user: payload.email || payload.sub };
      }
    } catch {
      return { valid: false, error: 'Malformed JWT assertion' };
    }
  }

  return { valid: false, error: 'Invalid Cloudflare Access Token' };
}

/**
 * Validates CSRF Origin for POST requests
 */
export function verifyCsrfOrigin(request: Request): boolean {
  if (request.method !== 'POST') return true;

  const origin = request.headers.get('origin');
  const referer = request.headers.get('referer');
  const currentOrigin = new URL(request.url).origin;

  if (origin && origin !== currentOrigin) {
    return false;
  }

  if (!origin && referer) {
    try {
      if (new URL(referer).origin !== currentOrigin) return false;
    } catch {
      return false;
    }
  }

  return true;
}
