# PRD + Architecture: UniqueDigit 3D PC Builder & Battlestation Simulator

> Purpose: single source of truth to rebuild the 3D PC builder inside Cursor. Give this file to Cursor as context (`@PRD_3D_PC_Builder_UniqueDigit.md`) and build phase by phase using Section 16 prompts.
> Audience: Cursor / developer. Market: India (INR, Amazon India, EarnKaro). Surface: blog/affiliate site, mobile-first.

---

## 1. Product Summary

**One line:** A step-by-step 3D PC builder where a visitor picks CPU → GPU → Motherboard → RAM → SSD → Case/PSU → Monitor → Keyboard → Mouse, watches the PC assemble in 3D in real time, sees compatibility + estimated FPS + total INR cost, then buys via affiliate links or shares the build.

**Business goal:** Affiliate revenue (Amazon India / EarnKaro), SEO traffic, shareable viral builds, longer session time.

**Success metrics (90 days):**
| Metric | Target |
|---|---|
| Builder completion (reach step 9 / summary) | ≥ 35% of starters |
| Affiliate click-through from summary | ≥ 12% |
| Avg session duration on builder | ≥ 4 min |
| Share/Download card usage | ≥ 8% |
| Mobile LCP | < 2.5 s (3D loads lazily, never blocks LCP) |
| 3D frame rate on mid-range Android | ≥ 30 fps |

---

## 2. Problems in the Current Build (from screenshot review)

Fix all of these first. They are the reason it feels "not pro".

1. **Broken product images**: alt text is showing ("Corsair Vengeance LPX 16GB"). Need image fallback, fixed aspect ratio, lazy load, and local/CDN-hosted images.
2. **3D canvas is basically empty**: huge dark area, only a cropped purple shape at the bottom. Model is off-center, camera framing is wrong, no visible PC/desk. Need auto-framing camera (fit to bounding box).
3. **Overlapping UI on the 3D view**: hint text ("Hover & Click any 3D part · Drag to rotate…") overlaps the keyboard label. Floating toolbar (browser extension-looking pill) sits on top of the right panel. Labels must live in a controlled HUD layer with collision-safe positions.
4. **Price inconsistency**: preset says "₹55K 1080p Value King" but total is ₹78,464. Preset names must match actual totals (or be computed).
5. **Duplicate nav item**: "PC Builds" appears twice in the header.
6. **Too many stacked small mono-font labels**: low contrast, tiny (9–10px). Accessibility fail. Min 12px body, 11px only for badges.
7. **Right panel cut-off**: step tabs overflow ("5. NVM…") with no scroll indicator. Needs horizontal scroll with fade edges, or collapse to a stepper.
8. **Claims risk**: "Verified Indian Amazon Prices (2026)" and "Zero fake metrics" while FPS values are estimates. Label FPS as *Estimated*, show price "last updated" time, and never say "verified" unless a live price source backs it.
9. **Huge empty space** below footer and the ad slot looks like an empty box. Hide ad slot until an ad actually loads.
10. **Wording typos on hero text/CTAs** and inconsistent casing. Run a copy pass.
11. **Big dead area on the left column** below the 3D card while the right column is long. Make the left 3D viewer `position: sticky`.

---

## 3. Users & Use Cases

| Persona | Need | Key features |
|---|---|---|
| Budget gamer (16–22, India) | "Best PC under ₹X" | Budget presets, FPS estimate, compatibility auto-fix |
| First-time builder | "Will this work together?" | Plain-language compatibility, build guide videos |
| Content creator | 1440p/4K + editing | Workload tags (Gaming/Editing/Streaming) |
| Blog reader / Insta user | Wants to flex a build | 3D share card, WhatsApp share, setup themes |

---

## 4. Feature Scope

### 4.1 MVP (ship first)
- 9-step guided builder with progress stepper, Back/Next, skip optional steps
- Part picker cards (3–6 options per step, filter + sort, search)
- **Live 3D assembly**: parts appear/animate into the case as chosen
- Compatibility engine (socket, RAM type, PSU wattage, case size, GPU clearance, cooler)
- Total price (INR) + power draw (W) + PSU recommendation
- Estimated FPS panel (clearly labeled estimate)
- Build summary table + "Add all to Amazon" (affiliate links)
- Quick presets (₹35K / ₹55K / ₹85K / ₹1.5L+) computed to match budget
- Share: WhatsApp, copy link, download spec card (image)
- Shareable build URL (state encoded in query string)
- Mobile layout with bottom sheet
- 3D fallback (static render image) when WebGL unavailable / low-end device

### 4.2 V2 (after MVP is stable)
- **Video features** (see 4.3)
- Bottleneck checker (CPU vs GPU balance)
- Compare two builds side-by-side
- Price history sparkline + price drop alert (email/WhatsApp opt-in)
- Studio themes (Cyber Neon, Studio White, Astro Space, Warm Wood) + RGB sync color picker
- Cable management / airflow toggle visualization
- AI assistant: "Build me a PC under ₹60K for Valorant + editing" → fills the builder
- Save build to account (optional login) / localStorage
- Leaderboard / community builds gallery (viral loop)
- Embed mode for blog posts (see Section 9)

### 4.3 Video features (you asked for these)
1. **Part explainer videos**: each part card has a "Why this?" 20–40 s clip or YouTube embed (lite-youtube, loads only on click).
2. **Build assembly walkthrough**: a "How to assemble" tab with chaptered YouTube video (timestamps per step: CPU install, RAM, SSD, GPU, cable). Chapters link from the builder step.
3. **3D build replay video**: "Record my build" → captures canvas to a 10–15 s MP4/WebM (MediaRecorder API) showing the PC assembling + rotating, for Insta Reels / Shorts. This is the strongest viral feature.
4. **FPS benchmark clips**: per-game embedded YouTube benchmark for the chosen GPU (curated links in data, not auto-searched).
5. Respect privacy: use `youtube-nocookie.com`, facade/lite embed, no autoplay with sound.

---

## 5. UX Flow & Information Architecture

```
Landing/Hero → choose path:
  A) Start from scratch (Step 1 CPU)
  B) Pick a preset budget
  C) Describe needs (AI, V2)
        ↓
Step pipeline (1 CPU → 9 Mouse), 3D updates live on every pick
        ↓
Summary: compatibility report · FPS · price · power
        ↓
Actions: Buy on Amazon · Share · Download card · Record video · Save
```

### 5.1 Desktop layout (≥1024px)
- 12-col grid, max width 1200px.
- **Left (5 cols): sticky 3D viewer card** (height `min(78vh, 720px)`), with HUD overlay: status, camera tabs, theme chips, totals.
- **Right (7 cols): step panel**: stepper at top, part cards list, then FPS card, then breakdown table.
- Hero stays compact (title, 1-line subtitle, presets). Move total cost + power into the 3D card HUD AND keep a sticky top mini-bar on scroll.

### 5.2 Mobile layout (<768px)
- 3D viewer on top, fixed aspect ~ 4:5, collapses to 40vh when the part list is scrolled.
- Part list lives in a **bottom sheet** (peek / half / full snap points).
- Stepper becomes a horizontal chip row with auto-scroll to active step.
- Sticky bottom bar: `₹ total` + `Next →`.
- Touch: one finger rotate, pinch zoom, double-tap reset. Tap a 3D part → opens its card.

### 5.3 Empty / loading / error states (required)
- 3D loading: skeleton with progress % (use `useProgress`)
- Image fail: gradient placeholder with category icon
- Incompatible pick: card shows red badge + "Fix automatically" button
- Offline/price missing: "Check price on Amazon" instead of a wrong number

---

## 6. UI Design System

### 6.1 Direction
Dark "gaming hardware" 3D stage on the left, clean light content panel on the right. Premium, not noisy: fewer micro-labels, more whitespace, one accent.

### 6.2 Tokens
```css
:root {
  --bg: #f6f6fb;
  --surface: #ffffff;
  --ink: #0f1020;
  --muted: #5b5f7a;
  --border: #e6e6f0;

  --stage-bg: #0a0a14;          /* 3D card */
  --stage-surface: #12121f;
  --brand: #6d28d9;             /* purple */
  --brand-ink: #ffffff;
  --accent: #fbbf24;            /* CTA yellow, Amazon action */
  --success: #16a34a;
  --warn: #f59e0b;
  --danger: #dc2626;
  --neon-cyan: #22d3ee;         /* only inside 3D stage */

  --radius-sm: 8px; --radius-md: 14px; --radius-lg: 22px;
  --shadow-card: 0 8px 30px rgba(20,20,50,.08);
  --font-ui: "Inter", system-ui, sans-serif;
  --font-display: "Space Grotesk", "Inter", sans-serif;
  --font-mono: "JetBrains Mono", ui-monospace, monospace; /* numbers/FPS only */
}
@media (prefers-color-scheme: dark) { /* full dark theme tokens here */ }
```

### 6.3 Type scale
H1 40/44 (mobile 28/34) · H2 24/30 · H3 18/24 · Body 15/24 · Small 13/20 · Badge 11/14 (min). Mono only for numbers, not for labels.

### 6.4 Components
`StepperBar`, `PartCard` (image, title, 2–3 spec chips, price, state: default/selected/incompatible), `Stage3D`, `StageHUD`, `CameraTabs` (Desk / Tower / Peripherals), `ThemeChips`, `RGBPicker`, `TotalsBar`, `CompatBanner`, `FPSCard`, `BreakdownTable`, `ShareSheet`, `VideoEmbed`, `PresetChips`, `BottomSheet`, `Toast`.

### 6.5 Motion
- Part pick → part flies in along a path to its slot (400–600 ms, ease-out), subtle glow pulse.
- Step change → camera glides to that part's focus point.
- Respect `prefers-reduced-motion`: swap to instant transitions.

### 6.6 Accessibility
- Every 3D interaction has a non-3D equivalent (the card list).
- Keyboard: arrow keys switch steps, Enter selects, `Esc` closes sheets.
- Contrast ≥ 4.5:1, focus rings visible, `aria-live` for total/compat changes.

---

## 7. 3D Architecture

### 7.1 Stack
- **three.js** via **React Three Fiber (`@react-three/fiber`)**
- **`@react-three/drei`**: `OrbitControls`, `useGLTF`, `Environment`, `ContactShadows`, `Html`, `Bounds`, `useProgress`, `PerformanceMonitor`
- **`@react-three/postprocessing`**: light Bloom only on desktop (RGB glow)
- **gltf-transform / gltfpack**: Draco + meshopt compression, KTX2 textures
- **Zustand**: build state shared between UI and 3D

### 7.2 Model strategy (important decision)
Do NOT model every product. Use **parametric generic models per category** with product-specific tweaks:

| Category | Model approach |
|---|---|
| Case | 3–4 GLB cases (mini / mid / full tower, glass side), pick closest to the chosen case |
| Motherboard | Generic ATX / mATX / ITX board GLB with named slot nodes |
| CPU / Cooler | Generic CPU + 3 cooler types (stock, tower, AIO) |
| RAM | 1 stick GLB, instanced ×2/×4, color/heatsink variants (RGB/no RGB) |
| GPU | 3 size classes (short / mid / long, 2 or 3 fan), brand-tinted shroud color |
| SSD | M.2 stick GLB |
| PSU | Generic box, hidden unless side panel is open |
| Monitor | 24" / 27" / 32" GLB, screen texture shows the game wallpaper |
| Keyboard / Mouse | Generic 65% / TKL / full + mouse GLB, RGB emissive material |

Each GLB uses **named anchor nodes** (e.g. `slot_gpu`, `slot_ram_1..4`, `slot_m2_1`, `slot_cpu`) so code never hard-codes positions.

### 7.3 Scene graph
```
<Canvas dpr={[1, 1.75]} shadows="basic" gl={{ antialias: true, powerPreference: "high-performance" }}>
  <Suspense fallback={<StageLoader/>}>
    <Environment preset="city" />            // low-res HDRI, lazy
    <Room theme={theme} />                    // desk, wall, props per theme
    <Bounds fit clip observe margin={1.2}>    // AUTO-FRAME FIX for empty canvas
      <PCRig build={build}/>                  // case + parts, driven by store
      <Peripherals build={build}/>
    </Bounds>
    <ContactShadows .../>
  </Suspense>
  <CameraRig target={focusPoint} preset={cameraTab}/>
  <OrbitControls enablePan={false} minPolarAngle={0.6} maxPolarAngle={1.6} minDistance={..} maxDistance={..}/>
  <PerformanceMonitor onDecline={lowerQuality}/>
</Canvas>
```

### 7.4 Interaction
- **Raycasting** via R3F pointer events: hover = outline/emissive boost + tooltip (Drei `Html`), click = select category and scroll the card list to that step.
- Tooltips render in an `Html` layer with `zIndexRange` and a collision pass so they never overlap (fixes screenshot bug #3).
- Camera presets: **Desk** (wide), **PC Tower** (case close-up, side panel fades), **Peripherals** (keyboard/mouse). Animate with damped lerp.
- "Explode view" toggle: parts offset along their slot normal.

### 7.5 Performance budget
- Total GLB payload ≤ **3 MB** initial (case + board + GPU), rest lazy by step.
- Draw calls < 150, triangles < 400k desktop / < 150k mobile.
- Detect device tier (`detect-gpu`): high → bloom + shadows; low → no bloom, no shadows, DPR 1.
- Pause rendering when offscreen (`IntersectionObserver` + `frameloop="demand"` / `"never"`).
- Load 3D **after** main content (dynamic import, `ssr: false`), show static poster image first (good for LCP/SEO).
- Dispose geometries/materials on unmount; cache GLBs with `useGLTF.preload` for next step only.

### 7.6 Fallbacks
1. No WebGL → static pre-rendered image of the selected combo (or generic) + all features still work.
2. Low-end device → "Lite 3D" (no shadows/bloom, simpler models).
3. Error boundary around the Canvas, with a "Reload 3D" button.

---

## 8. Data Architecture

### 8.1 Part schema (JSON / DB)
```ts
type Part = {
  id: string;                    // "cpu_amd_ryzen_5_5600"
  category: "cpu"|"gpu"|"mobo"|"ram"|"ssd"|"case"|"psu"|"cooler"|"monitor"|"keyboard"|"mouse";
  brand: string; name: string; image: string; // local/CDN, with width/height
  price: { inr: number; updatedAt: string; source: "paapi"|"manual"|"earnkaro" };
  affiliate: { amazonUrl: string; asin?: string; earnkaroUrl?: string };
  specs: Record<string, string|number|boolean>; // category-specific, see below
  model3d: { glb: string; variant?: string; tint?: string; scale?: number };
  tags: string[];                // "budget", "esports", "creator", "rgb"
  benchmarks?: { gpuScore?: number; cpuScore?: number };
  videos?: { explainer?: string; benchmark?: string };
};
```
Category specs (minimum):
- CPU: `socket, cores, threads, boostGHz, tdpW, igpu`
- GPU: `chip, vramGB, lengthMM, tdpW, powerConnectors, slots`
- Mobo: `socket, chipset, formFactor, ramType, ramSlots, maxRamGB, m2Slots, wifi`
- RAM: `type (DDR4/DDR5), speedMHz, kitGB, sticks, heightMM`
- SSD: `interface, gen, capacityGB, readMBs`
- Case: `formFactorsSupported, maxGpuLengthMM, maxCoolerHeightMM, psuIncluded, psuWatt`
- PSU: `watt, efficiency, modular`
- Monitor: `sizeIn, resolution, refreshHz, panel`

### 8.2 Storage
- MVP: static JSON in repo (`/data/parts/*.json`) + build-time validation with **zod**.
- V2: Postgres/Supabase tables `parts`, `price_snapshots`, `builds`, `events`; admin panel to edit parts/prices.

### 8.3 Build state
```ts
type Build = { cpu?: id; gpu?: id; mobo?: id; ram?: id; ssd?: id; case?: id; psu?: id; monitor?: id; keyboard?: id; mouse?: id; theme: ThemeId; rgb: string };
```
Serialize to URL: `/pc-builder?b=cpu.r5-5600,gpu.rtx4060,...&t=cyber&c=7c3aed` (short IDs, no PII).

---

## 9. Blog Integration (Embed Strategy)

Pick one (build the first, offer the others later):
1. **Dedicated route** `/pc-builder` inside the site (best for SEO) — primary.
2. **Embed in any blog post** via iframe: `<iframe src="/embed/pc-builder?preset=55k" loading="lazy" ...>` with `postMessage` height auto-resize.
3. **Web component** `<ud-pc-builder preset="55k" theme="dark">` for other sites/CMS.

> Open question for owner: which platform is the blog on (WordPress / Next.js / Webflow / custom)? The builder should be a Next.js (App Router) app; WordPress embeds via iframe/shortcode.

SEO: server-render the step content, FAQ, and spec tables (so Google sees text); JSON-LD `ItemList` + `FAQPage`; canonical per preset page (`/pc-builder/55k-gaming-pc-india`), unique copy per preset.

---

## 10. Compatibility Engine

Pure functions, unit-tested, no UI dependency. Each rule returns `{ level: "ok"|"warn"|"error", message, fix? }`.

| Rule | Logic |
|---|---|
| CPU ↔ Mobo socket | `cpu.socket === mobo.socket` else error |
| BIOS support | warn if chipset may need BIOS update for newer CPU |
| RAM ↔ Mobo type | `ram.type === mobo.ramType` else error |
| RAM capacity/slots | `ram.sticks <= mobo.ramSlots` and kit ≤ maxRam |
| Case ↔ Mobo size | mobo form factor in `case.formFactorsSupported` |
| GPU ↔ Case length | `gpu.lengthMM <= case.maxGpuLengthMM` |
| Cooler ↔ Case height | `cooler.heightMM <= case.maxCoolerHeightMM` |
| PSU wattage | `psu.watt >= (cpu.tdp + gpu.tdp + 150) * 1.2`; error if < required, warn if barely OK |
| PSU connectors | GPU power connectors available |
| M.2 | SSD interface/gen supported by mobo (warn when downgrading gen) |
| Monitor | warn if refresh/resolution is wasted for the chosen GPU tier |
| iGPU | if no GPU and CPU has no iGPU → error |

**Auto-fix:** when a user changes an earlier part (e.g., CPU socket), downstream incompatible picks are flagged and a "Replace with compatible" suggestion appears. Never silently delete picks.

Sorting rule: in each step, **compatible parts first**, incompatible greyed with the reason.

---

## 11. FPS Estimation (honest version)

- Label everywhere: **"Estimated FPS"** + tooltip: "Based on benchmark averages; real performance varies."
- Method: `fps = baseFps[game][gpuTier] * cpuFactor(cpu, game) * resolutionFactor * settingsFactor`, capped by CPU limit; DLSS/FSR only when GPU supports it.
- Data: hand-curated table from public benchmarks, stored as JSON with a source URL + date per game. Never invent numbers.
- Games to start: Valorant, GTA V, Cyberpunk 2077, BGMI/emulator, Fortnite, CS2.
- Resolution/settings toggle: 1080p/1440p/4K, Medium/High/Ultra.
- Show a **bottleneck meter** (CPU vs GPU ratio) in V2.

---

## 12. Pricing, Affiliate & Legal

- Prefer **Amazon PA-API** / EarnKaro product feed for prices. If prices are manual, show "Price as of {date}" and the "Check price" fallback. Do not label prices "verified" unless fetched live.
- Amazon Associates India has rules on displaying prices/stale data and required disclosure — **check the current Operating Agreement before launch** (I may be out of date).
- Affiliate disclosure visible near the CTA, not only in the footer.
- "Add all to Amazon cart" uses Amazon's add-to-cart form URL with the Associates tag; individual links as fallback. Open with `rel="sponsored nofollow noopener"`.
- Pages: Affiliate Disclosure, Privacy (analytics, share-card uploads), Terms, Disclaimer (estimates, compatibility advice is guidance not guarantee).
- Cookie/consent banner if using ads/analytics per applicable rules.

---

## 13. Share Card & Video Export

- **Spec card image**: render an offscreen React node → PNG via `html-to-image` (1080×1350 for Insta, 1080×1920 for Stories). Include 3D snapshot (`canvas.toDataURL` with `preserveDrawingBuffer` only during capture), parts list, total, FPS, URL/QR.
- **Build video**: `canvas.captureStream(30)` + `MediaRecorder` → WebM (convert/offer MP4 where supported). Script: assembly animation → 360° orbit → price card end frame.
- WhatsApp share: `https://wa.me/?text=` with build URL + OG image.
- **OG image** per build URL generated server-side (Vercel OG / satori) so link previews look great.

---

## 14. Tech Stack & Project Structure

**Stack:** Next.js (App Router) · TypeScript · Tailwind CSS · Zustand · React Three Fiber + drei · zod · Vitest · Playwright · Framer Motion (UI) · Vercel/Cloudflare hosting · GA4 or Plausible.

```
/app
  /pc-builder/page.tsx            # main route (SSR content + client builder)
  /pc-builder/[preset]/page.tsx   # SEO preset pages
  /embed/pc-builder/page.tsx      # iframe embed
  /api/og/route.tsx               # OG image
  /api/prices/route.ts            # price proxy / cache (V2)
/components
  /builder   StepperBar PartCard PartList CompatBanner TotalsBar FPSCard BreakdownTable
  /stage     Stage3D PCRig Room CameraRig Hud Tooltips Loader
  /share     ShareSheet SpecCard VideoRecorder
  /ui        BottomSheet Toast Chip Button
/lib
  compat/    rules.ts engine.ts *.test.ts
  fps/       estimate.ts
  build/     store.ts serialize.ts presets.ts
  three/     anchors.ts loaders.ts quality.ts
/data
  parts/*.json  fps/*.json  videos.json
/public/models/*.glb  /public/img/parts/*
```

---

## 15. Analytics & QA

**Events:** `builder_start, step_view{n}, part_pick{id}, compat_error{rule}, preset_click, share_click{type}, card_download, video_record, affiliate_click{part,store}, add_all_click, 3d_fail{reason}`.

**Acceptance checklist:**
- [ ] 3D shows a centered, fully visible PC on first load (desktop + mobile)
- [ ] Picking any part visibly updates the 3D within 600 ms
- [ ] No overlapping text/HUD at 360px, 768px, 1280px, 1920px
- [ ] No broken images (all parts have fallback)
- [ ] Every preset total is within ±5% of its label
- [ ] All compatibility rules have unit tests (≥ 30 cases)
- [ ] Lighthouse mobile: Performance ≥ 80, Accessibility ≥ 95, SEO ≥ 95
- [ ] Works with WebGL disabled
- [ ] Build URL round-trips (copy link → open → same build)
- [ ] Affiliate links tagged, disclosure visible near CTA

---

## 16. Build Plan: Cursor Prompts (run in order)

> Tip: start every Cursor chat with `@PRD_3D_PC_Builder_UniqueDigit.md`. Commit after each phase.

### Phase 0: Setup
```
Read @PRD_3D_PC_Builder_UniqueDigit.md fully. Scaffold a Next.js App Router + TypeScript + Tailwind project with the folder structure in Section 14. Add zustand, three, @react-three/fiber, @react-three/drei, zod, vitest. Add the design tokens from Section 6.2 to globals.css. Do not build features yet. Show me the tree.
```

### Phase 1: Data + compatibility (no UI)
```
Implement Section 8 and Section 10. Create zod schemas, 5+ sample parts per category in /data/parts, and /lib/compat with pure rule functions plus Vitest tests (30+ cases covering every rule). Run the tests and fix failures.
```

### Phase 2: State + builder UI (2D only)
```
Build the builder UI per Sections 5 and 6: StepperBar, PartCard (with image fallback), PartList with compatible-first sorting, TotalsBar, CompatBanner, BreakdownTable. Zustand store with URL serialization (Section 8.3). Mobile bottom sheet. Make it fully usable without 3D.
```

### Phase 3: 3D stage
```
Build /components/stage per Section 7 using generic placeholder geometry first (boxes with correct proportions) driven by named anchors. Implement Bounds auto-framing so the PC is always centered, camera presets (Desk / Tower / Peripherals), hover highlight + click-to-select-step, tooltips in a collision-safe Html layer, loader with progress, error boundary, and WebGL fallback poster. Lazy-load the Canvas (ssr:false).
```

### Phase 4: Real models + polish
```
Replace placeholders with compressed GLBs (Draco/meshopt) using the anchor naming in Section 7.2. Add part fly-in animation, explode view, RGB emissive materials with the color picker, and 4 studio themes. Add PerformanceMonitor + device-tier quality levels per Section 7.5. Respect prefers-reduced-motion.
```

### Phase 5: FPS, presets, summary
```
Implement Section 11 FPS estimator with labeled estimates and a resolution/settings toggle. Generate presets (35K/55K/85K/1.5L+) by a budget solver that picks compatible parts and ensure totals match labels within 5%. Build the final summary view and "Add all to Amazon" with affiliate tagging and disclosure per Section 12.
```

### Phase 6: Share + video
```
Implement Section 13: spec card PNG export, WhatsApp share, per-build OG image route, and the 3D build video recorder (MediaRecorder on canvas.captureStream) with assembly -> orbit -> price end card. Add the video embed components from Section 4.3 using lite youtube-nocookie facades.
```

### Phase 7: SEO, embed, QA
```
Add SSR content, JSON-LD (ItemList + FAQPage), preset landing pages, iframe embed route with postMessage auto-height (Section 9). Add analytics events from Section 15. Run Playwright tests for the acceptance checklist and Lighthouse; fix everything below target.
```

---

## 17. Master Prompt (single-shot version for Cursor Agent)

```
You are a senior front-end + 3D engineer. Using @PRD_3D_PC_Builder_UniqueDigit.md as the spec, build the UniqueDigit 3D PC Builder end to end in Next.js + TypeScript + Tailwind + React Three Fiber.

Rules:
1. Work phase by phase (Section 16). After each phase: run build, lint, tests; fix; summarize; wait for my "continue".
2. Compatibility logic must be pure, typed, and unit-tested. Never put compat rules in components.
3. 3D must auto-frame the model (Bounds), never show an empty canvas, and must degrade gracefully (no WebGL, low-end, error).
4. Mobile-first. Test at 360, 768, 1280. No overlapping UI. Min text 12px (badges 11px).
5. Never invent prices, benchmarks, or "verified" claims. Use data files with updatedAt + source. FPS is always labeled "Estimated".
6. Every image has a fallback; every 3D action has a non-3D equivalent; keyboard accessible.
7. Keep initial JS and 3D payload within the budgets in Section 7.5.
8. Ask me before adding paid services or changing the stack.

Start with Phase 0 and show the folder tree.
```

---

## 18. Risks & Open Questions

| Risk / Question | Mitigation |
|---|---|
| 3D models cost time/money | Use generic parametric models (7.2); buy/CC0 base models from Sketchfab/Poly Haven with license check |
| Price data goes stale | PA-API/EarnKaro feed, show timestamps, "Check price" fallback |
| Heavy 3D hurts mobile SEO/LCP | Lazy load after content, poster image, quality tiers |
| Amazon policy changes | Re-check Associates agreement before launch and quarterly |
| Blog platform unknown | Confirm (Section 9); default to Next.js route + iframe embed |
| Who maintains parts data? | Admin JSON/CSV import now, admin panel in V2 |