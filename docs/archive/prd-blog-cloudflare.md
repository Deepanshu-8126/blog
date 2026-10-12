# UniqueDigit - Blog Feature PRD (Cloudflare Edition)

## Product Overview
UniqueDigit uses Cloudflare Pages + D1 Database (or KV) for its backend. The blog feature will be built natively on Cloudflare's platform, avoiding Supabase dependency entirely.

## Tech Stack
- **Frontend**: Astro + Cloudflare Pages
- **Database**: Cloudflare D1 (SQLite-compatible) or KV (key-value)
- **Auth**: Cloudflare Access / JWT, or simple API tokens
- **Rendering**: Astro Islands architecture (static by default, API routes on edge)

## Database Options

### Option A: Cloudflare D1 (Recommended)
- SQLite-compatible SQL database
- Edge locations worldwide
- Built-in for Cloudflare Pages

### Option B: Cloudflare KV
- Simple key-value store
- Extremely fast
- Great for blogs with predictable structure

## Schema: D1 SQL Approach

```sql
CREATE TABLE blog_posts (
  id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  slug TEXT UNIQUE NOT NULL,
  title TEXT NOT NULL,
  excerpt TEXT,
  body_md TEXT NOT NULL,
  status TEXT DEFAULT 'draft' CHECK (status IN ('draft', 'published', 'archived')),
  published_at INTEGER, -- Unix timestamp
  author TEXT,
  read_time INTEGER,
  view_count INTEGER DEFAULT 0,
  like_count INTEGER DEFAULT 0,
  dislike_count INTEGER DEFAULT 0,
  image_url TEXT,
  tags TEXT DEFAULT '',
  category TEXT DEFAULT 'Tech',
  meta_title TEXT,
  meta_description TEXT,
  og_image TEXT,
  og_title TEXT,
  og_description TEXT,
  created_at INTEGER DEFAULT (CAST(strftime('%s', 'now') AS INTEGER)),
  updated_at INTEGER DEFAULT (CAST(strftime('%s', 'now') AS INTEGER))
);

-- Indexes for performance
CREATE INDEX idx_blog_posts_slug ON blog_posts(slug);
CREATE INDEX idx_blog_posts_status ON blog_posts(status);
CREATE INDEX idx_blog_posts_category ON blog_posts(category);
CREATE INDEX idx_blog_posts_published ON blog_posts(published_at);
```

## Schema: KV Approach (Simpler)

```javascript
// Types for KV storage
interface BlogPost {
  id: string;
  slug: string;
  title: string;
  excerpt: string;
  body_md: string;
  status: 'draft' | 'published' | 'archived';
  published_at?: number;
  author?: string;
  read_time?: number;
  view_count?: number;
  like_count?: number;
  dislike_count?: number;
  image_url?: string;
  tags: string[];
  category: string;
  meta_title?: string;
  meta_description?: string;
  og_image?: string;
  og_title?: string;
  og_description?: string;
  created_at: number;
  updated_at: number;
}

// Example KV namespace binding
// In astro.config.ml: d1: D1Namespace
// const posts = await env.D1.posts().select('*').where('status = ?', ['published'])
```

## API Routes (Cloudflare Functions)

### `GET /api/blog`
- List posts with pagination: `?page=1&limit=10&category=Tech&status=published`
- Search: `?search=ai%20tools`
- Sort: `?sort=latest&sort=oldest&sort=most_viewed`

### `GET /api/blog/[slug]`
- Return single post by slug
- Increment view_count atomically

### `POST /api/blog`
- Create new post (admin authenticated)
- Body: { title, slug, excerpt, body_md, status, category, tags, ... }

### `PUT /api/blog/[id]`
- Update existing post
- Partial update support

### `DELETE /api/blog/[id]`
- Soft delete: set status = 'archived'

### `GET /api/blog/categories`
- Return all unique categories/tags

## Frontend Components

### `src/pages/blog.astro`
- Blog listing grid
- Filter by category/tags
- Search bar
- Sort options
- Pagination (Astro's `cursor` based or page-based)

### `src/pages/blog/[slug].astro`
- Post detail page
- Table of contents (from H2/H3 headers)
- Related posts (same category)
- Share buttons (Twitter, Copy link)
- Related: Next/Prev posts navigation

### `src/components/BlogPostCard.astro`
- Reusable card component for listing
- Image, title, excerpt, meta info
- Badge for status (New, Hot, Top)

### `src/components/BlogSearchFilter.astro`
- Category checkboxes
- Search input
- Sort dropdown

## SEO Implementation

### Meta Tags per Post
```astro
---
const { slug } = Astro.params;
const post = await fetch(`/api/blog/${slug}`).then(r => r.json());
---

<html>
  <head>
    <title>{post.meta_title || `${post.title} - UniqueDigit`}</title>
    <meta name="description" content={post.meta_description || post.excerpt || ''}>
    <meta property="og:title" content={post.og_title || post.title}>
    <meta property="og:description" content={post.og_description || ''}>
    <meta property="og:image" content={post.og_image || '/og-image.png'}>
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content={post.title}>
    <meta name="twitter:description" content={post.excerpt}>
  </head>
</html>
```

### Sitemap Integration
- Add `/blog` and `/blog/[slug]` routes to sitemap
- Priority: 0.8 for posts, 0.5 for category pages
- Lastmod: from published_at or updated_at

## Admin Interface (Simple)

Since this is Cloudflare-native, admin can be:

### Option 1: Cloudflare Dashboard
- Direct D1 KV/SQL editing via dashboard
- No custom admin UI needed initially

### Option 2: Simple API Tokens
- POSTman / curl to create posts
- Token-based auth on API routes

### Option 3: Third-party Headless CMS
- Directus (self-hosted on Cloudflare Workers)
- Strapi (with Cloudflare deployment)
- Or just use `curl` to API endpoints

## Example: Creating a Post (curl)

```bash
curl -X POST "https://uniquedigit.pages.dev/api/blog" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "slug": "new-ai-tool-review",
    "title": "Review: New AI Tool for Developers",
    "excerpt": "First look at the latest generative AI coding assistant",
    "body_md": "# Review\n\n... content ...",
    "status": "published",
    "category": "AI",
    "tags": ["AI", "Tools", "Development"],
    "meta_title": "AI Tool Review - UniqueDigit",
    "meta_description": "Review of new AI coding assistant"
  }'
```

## Migration from Existing Setup

Current state has:
- `SEED_NICHES` with 8+ niches
- `db.ts` with Niche/Post interfaces
- Static content in pages

Migration plan:
1. Keep existing niches system as-is
2. Add `blog_posts` table to D1 database
3. Create API routes under `/api/blog/`
4. Add `/blog` page that queries the API
5. Update `db.ts` to include BlogPost interface if needed
6. No breaking changes to existing pages

## Performance Targets

| Metric | Target |
|--------|--------|
| **Page Load** | < 1s on 3G |
| **Time to First Byte** | < 200ms (Edge) |
| **Lighthouse Score** | > 90 |
| **TTFB for API** | < 50ms |
| **Database Query** | < 10ms (D1 cached) |

## Security

- API routes protected with admin token in header
- CORS configured for `uniquedigit.pages.dev` only
- Rate limiting on write endpoints (10 req/min per IP)
- SQL injection prevention (parameterized queries in D1)
- XSS sanitization on body_md (Astro escapes by default)

## Error Handling

- `404` for non-existent blog slugs
- `400` for invalid slugs (alphanumeric + hyphens only)
- `401` / `403` for unauthenticated admin attempts
- `500` with user-friendly message on DB errors
- Graceful degradation if DB is temporarily unavailable

## Deployment Checklist

- [ ] Create D1 database in Cloudflare dashboard
- [ ] Run `npx astro db deploy` to create schema
- [ ] Add admin token to Cloudflare Settings > Variables
- [ ] Test API endpoints with curl/Postman
- [ ] Build and deploy: `npm run build`
- [ ] Verify `/blog` page loads correctly
- [ ] Check sitemap includes blog routes
- [ ] Test mobile responsiveness
- [ ] Set up analytics (Cloudflare Analytics or Plausible)

## Success Metrics

- ✅ 20+ blog posts within first 2 weeks
- ✅ Average read time > 3 minutes
- ✅ 70%+ posts published (status = published)
- ✅ Search engine indexing within 24 hours (Cloudflare auto-ping)
- ✅ Zero critical bugs
- ✅ Mobile-first design passes all tests
- ✅ API responds in < 100ms average

## Timeline (4 Weeks)

| Week | Deliverable |
|------|-------------|
| **1** | D1 database setup, schema creation, basic API routes (GET list, GET one), `/blog` listing page |
| **2** | POST/PUT/DELETE API, post detail page `/blog/[slug]`, SEO meta tags, categories/tags filtering |
| **3** | Admin API (with token auth), related posts, share buttons, RSS feed `/rss.xml` |
| **4** | Performance optimization, error handling, documentation, final testing, deployment |

## Dependencies (Add to package.json)

```json
{
  "dependencies": {
    // Already have these:
    "astro": "^5.4.2",
    "@astrojs/cloudflare": "^12.2.0",
    
    // Add these for blog:
    "drizzle-orm": "^0.35.0", // Optional: if using Drizzle ORM
    "hastscript": "^3.1.0", // For HTML manipulation
    "reading-time": "^1.5.0", // Estimated read time
    "date-fns": "^4.1.0", // Date formatting
    
    // Optional: directus/strapi if wanting full CMS
    // "directus": "^10.0.0"
  }
}
```

## Cloudflare Specific Config

### `astro.config.mjs`
```javascript
import { defineConfig } from 'astro';
import cloudflare from '@astrojs/cloudflare';

export default defineConfig({
  adapter: cloudflare(),
  // D1 configuration will be auto-detected
  // or manually add:
  // d1: {
  //   database: "uniquedigit_blog"
  // }
});
```

### `wrangler.toml` (for KV/D1)
```toml
name = "uniquedigit"

[d1.databases]
db-name = "blog"
migration-batch-size = 100

[vars]
ADMIN_TOKEN = "your-super-secret-admin-token"
```

## Roadmap Beyond v1

- **v2**: Comment system (utterances or disqus alternative)
- **v2**: Newsletter signup integration
- **v2**: Author profiles with avatar/bio
- **v2**: News/category feed generation
- **v3**: Multi-language support (i18n)
- **v3**: Premium content paywall
- **v3**: Video embedding support (Youptube, Vimeo)

---

**Note**: This PRD is optimized for Cloudflare's platform. If you later decide to switch to Supabase, the API patterns are similar but database implementation would differ.