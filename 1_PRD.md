# PRD — UniqueDigit Viral Hub (v1.0)

## 1. Goal
Ek auto-updating multi-niche blog/hub jo **affiliate (EarnKaro) + ads (AdSense)** se kamaye.
Content daily Google Trends + Wikipedia/TMDB data + AI (Gemini/Grok) se banta hai, **sab data Supabase mein**, code minimal.

**North-star:** Month-6 tak ₹30–50k/month. (Target hai, guarantee nahi — traffic quality pe depend karta hai.)

## 2. Users
| User | Kya chahiye | Kahan se aata hai |
|---|---|---|
| Deal hunter (India, mobile) | Loot deals, cashback, gold rate | Google search, WhatsApp share |
| Tech/AI curious | AI tools list, PC build | Google, Reddit, YouTube |
| Trend reader | Viral news, movies, GTA 6 | Discover, social |

Traffic ~85% mobile → **mobile-first**.

## 3. Scope (12 niche pages)
Group → Niche (slug) → page_type
- **Tech:** PC Builds (`pc-builds`, tools) · Gold Rate (`gold-rate`, dataset) · AI Tools (`ai-tools`, tools)
- **Money:** Deals (`deals`, tools) · Side Hustles (`side-hustles`, feed) · Cashback (`cashback`, tools)
- **Lifestyle:** Health (`health`, feed) · Fashion (`fashion`, feed) · Food (`food`, feed)
- **Entertainment:** GTA 6 (`gta-6`, feed) · Movies (`movies`, movies) · Viral (`viral`, feed)

Plus: Home `/` (hub preview + Trending Today), post page `/{niche}/{post}`, search, newsletter, legal pages.

> 12 pages = **4 templates** (feed / tools / dataset / movies). 13th niche = DB mein ek row, code nahi.

## 4. Functional requirements
| ID | Requirement | Priority |
|---|---|---|
| F1 | Mega menu (4 columns) DB ke `niches` table se bane. Item click = alag page redirect, scroll nahi | P0 |
| F2 | Har niche ka apna dashboard (template `page_type` se decide) | P0 |
| F3 | Daily pipeline: trends → topic rank → facts+image → AI article → Supabase | P0 |
| F4 | Real images: Wikipedia (people/places/things), TMDB (movie posters). Credit/link store ho | P0 |
| F5 | Har product/tool pe affiliate button; link `affiliate_rules` se auto-banta hai | P0 |
| F6 | New niche = DB row insert → menu, page, pipeline sab auto-sync | P0 |
| F7 | Home pe "Trending Today" (last 24h top posts by trend_score) | P0 |
| F8 | Dataset pages (Gold Rate): API se rate + history chart | P1 |
| F9 | Newsletter signup (Supabase `subscribers`) | P1 |
| F10 | Draft/review mode per niche (`config.review=true`) — health jaisa sensitive content publish se pehle check | P0 |
| F11 | Pipeline log (`pipeline_runs`) — fail hua to dikhe | P1 |
| F12 | Sitemap + RSS DB se auto | P1 |

## 5. Non-functional
- LCP < 2.5s on 4G mobile; CLS < 0.1 (ad slots ki height reserved)
- Cost ≈ ₹0 start mein (Cloudflare Pages, Supabase free, GitHub Actions free; AI API usage-based)
- Secrets code mein nahi; service key sirf GitHub Secrets mein
- Pipeline idempotent: dubara chalao to duplicate nahi

## 6. Earning model
1. **EarnKaro affiliate** — tools/deals/cashback/PC parts pe "Buy/Try Now". Sabse fast income.
2. **AdSense** (ya Ezoic/Mediavine later) — 3 fixed slots: post-top, mid-article, sidebar/footer.
3. **Newsletter** — list build, later sponsor.
4. Later: sponsored listings in AI Tools directory.

Revenue formula: `Visitors × affiliate CTR × conversion × commission + Pageviews × RPM/1000`.

## 7. Content quality rules (ye skip kiya to site dub sakti hai)
Google AI-mass-content ko "scaled content abuse" maan sakta hai. Isliye:
1. Har post mein **real data** ho (trend number, price, Wikipedia fact, source link) — sirf AI fluff nahi.
2. AI ko sirf **diye hue facts** use karne ka order; stats/prices/quotes invent nahi.
3. Clickbait heading nahi ("You won't believe…") — trust + AdSense approval dono ke liye.
4. **Fake cheezein mat dalo:** fake "12.4K watching", fake subscriber count, fake doctors/reviews, fake ratings. Screenshots mein ye sab mock hain — real data ho tabhi dikhao.
5. Health = YMYL: disclaimer har page pe, "doctor se pucho", koi diagnosis/dosage nahi, review mode ON.
6. Affiliate disclosure har page pe: "Hum commission kama sakte hain."
7. Images: Wikipedia/Commons ke license alag hote hain — credit link dikhao; movie poster sirf TMDB API se, TMDB attribution ke saath.
8. Required pages: About, Contact, Privacy, Terms, Affiliate Disclosure, Disclaimer (AdSense approval).

## 8. KPIs
| Metric | M1 | M3 | M6 |
|---|---|---|---|
| Published posts | 300 | 900 | 1800 |
| Indexed pages | 150 | 600 | 1500 |
| Monthly sessions | 2k | 25k | 100k |
| Affiliate CTR | 1% | 2% | 3% |
| Newsletter subs | 50 | 500 | 3000 |

## 9. Risks
| Risk | Fix |
|---|---|
| pytrends unofficial, kabhi block/break | Retry + fallback (AI topic suggestions) + official Google Trends API/SerpApi option |
| Thin AI content, no index | Quality rules §7, daily cap `POSTS_PER_NICHE`, review mode |
| Affiliate API unclear | `affiliate_rules` template approach; EarnKaro dashboard se link format verify |
| AI API cost | Gemini Flash cheap; Grok sirf ranking; cap per run |
| Copyright images | Wikipedia + TMDB only, credit store |

## 10. Out of scope (v1)
User login, comments, mobile app, multi-language, paid subscription.
