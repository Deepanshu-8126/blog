# UniqueDigit - Blog Feature PRD

## Product Overview
UniqueDigit needs a dedicated blogging platform integrated with its existing Supabase CMS. The blog will feature article posts with rich content, categories, tags, and full CRUD functionality for the content team.

## Target Audience
- Content writers and editors
- Tech enthusiasts reading PC build guides, AI tools reviews
- Indian audience looking for tech deals, gold rates, and earning tips
- Search engine users looking for authentic tech content

## Core Features

### 1. Blog Listing Page (`/blog`)
- Grid/masonry layout of blog posts
- Filter by category/tags (Tech, AI, Deals, Gold, Lifestyle)
- Pagination or infinite scroll
- Search functionality
- Sort by: latest, most viewed, trending

### 2. Blog Post Detail Page (`/blog/[slug]`)
- Full rich text content (Markdown/HTML)
- Author information
- Related posts sidebar
- Table of contents for long articles
- Print/Share buttons
- Comment system (optional)

### 3. Content Management (Admin)
- **Create New Post**: Form with title, slug, excerpt, body (Markdown), tags, status
- **Edit Post**: Update existing content
- **Delete Post**: Soft delete (change status to 'archived')
- **Publish/Unpublish**: Toggle status between draft/published/archived
- **Featured Posts**: Mark posts as featured on homepage

### 4. SEO Features
- Meta title and description per post
- Open Graph tags (title, description, image)
- Twitter Cards support
- Schema.org Article markup
- Auto-generated sitemap entries

### 5. User Engagement
- Read time estimation
- View counter
- Like/Dislike functionality
- Share to social media
- Related posts algorithm

### 6. Categories & Tags
- Predefined categories: Tech, AI Tools, Deals, Gold Rate, Lifestyle, Side Hustles
- Custom tags per post
- Category/tag pages showing all posts in that category

## Technical Requirements

### Database Schema (Supabase)
```sql
CREATE TABLE blog_posts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  excerpt TEXT,
  body_md TEXT NOT NULL,
  status TEXT DEFAULT 'draft' CHECK (status IN ('draft', 'published', 'archived')),
  published_at TIMESTAMP,
  author TEXT,
  read_time INTEGER,
  view_count INTEGER DEFAULT 0,
  like_count INTEGER DEFAULT 0,
  dislike_count INTEGER DEFAULT 0,
  image_url TEXT,
  tags TEXT[] DEFAULT '{}',
  category TEXT DEFAULT 'Tech',
  meta_title TEXT,
  meta_description TEXT,
  og_image TEXT,
  og_title TEXT,
  og_description TEXT,
  created_at TIMESTAMP DEFAULT now(),
  updated_at TIMESTAMP DEFAULT now()
);

CREATE INDEX idx_blog_posts_slug ON blog_posts(slug);
CREATE INDEX idx_blog_posts_category ON blog_posts(category);
CREATE INDEX idx_blog_posts_status ON blog_posts(status);
CREATE INDEX idx_blog_posts_published_at ON blog_posts(published_at);
```

### API Endpoints
- `GET /api/blog` - List posts with pagination/filter
- `GET /api/blog/[slug]` - Get single post
- `POST /api/blog` - Create new post (admin)
- `PUT /api/blog/[id]` - Update post (admin)
- `DELETE /api/blog/[id]` - Delete post (admin)
- `GET /api/blog/categories` - Get all categories/tags

### Frontend Components
- `BlogListing.astro` - Grid/list view of posts
- `BlogPost.astro` - Single post detail page with TOC
- `BlogForm.astro` - Admin post creation/editing form
- `BlogHeader.astro` - Blog navigation and filters
- `RelatedPosts.astro` - Sidebar component

### Design Specifications
- **Color Scheme**: Match existing brand (brand primary, slate neutrals)
- **Typography**: Inter font, JetBrains Mono for code blocks
- **Responsive**: Mobile-first, works on all devices
- **Performance**: Images optimized, lazy loading, minimal CSS
- **Accessibility**: Semantic HTML, proper contrast, keyboard navigation

### Admin Integration
- Add blog section to existing CMS workflow
- Replace static content with dynamic DB-driven posts
- Maintain consistency with existing niche pages (pc-builds, ai-tools, etc.)

### Export & Sharing
- RSS feed generation (`/rss.xml`)
- Social share buttons (Twitter, LinkedIn, Telegram)
- Copy link functionality
- Print-friendly version

## User Stories

### As a Content Editor
I want to create and manage blog posts through a simple interface so that I can publish tech articles without developer help.

### As a Reader
I want to easily find and read blog posts about tech, AI tools, deals, and lifestyle topics with good reading experience.

### As a Search Engine User
I want well-structured blog content with proper SEO so that I can find authentic UniqueDigit content when searching for tech topics.

### As a Regular Visitor
I want to discover related posts, see read time, and easily share interesting articles with my network.

## Acceptance Criteria

1. ✅ Blog listing page loads at `/blog` with 10+ sample posts
2. ✅ Individual post page at `/blog/[slug]` renders correctly
3. ✅ Admin can create/edit/delete posts via API
4. ✅ Posts have proper meta tags for SEO
5. ✅ Related posts functionality works
6. ✅ RSS feed available at `/rss.xml`
7. ✅ Mobile-responsive design on all pages
8. ✅ No broken links or 404s
9. ✅ Performance score > 90 (Lighthouse)
10. ✅ Accessibility score > 80 (axe-core)

## Dependencies
- `@astrojs/supabase` for database integration
- `remark` or `rehype` for Markdown processing
- `gray-matter` for frontmatter parsing
- `reading-time` for estimated read time
- `@astrojs/seo` for SEO metadata
- `date-fns` for date formatting

## Timeline
- **Week 1**: Database schema, API routes, basic listing page
- **Week 2**: Post detail page, SEO, categories/tags
- **Week 3**: Admin form, related posts, sharing features
- **Week 4**: Testing, performance optimization, documentation

## Success Metrics
- 50+ blog posts within first month
- Average read time > 3 minutes
- 70%+ posts published (not draft)
- Search engine indexing within 48 hours
- Zero critical bugs in first release