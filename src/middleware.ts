import { defineMiddleware } from 'astro:middleware';

export const onRequest = defineMiddleware(async (context, next) => {
  const url = context.url;
  // If URL contains double slashes (e.g. //sitemap.xml), normalize to single slash via 301 redirect
  if (url.pathname.includes('//')) {
    const cleanPath = url.pathname.replace(/\/+/g, '/');
    return context.redirect(cleanPath + url.search, 301);
  }
  return next();
});
