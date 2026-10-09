# 📋 Task Plan: UniqueDigit 3D Battlestation & Viral Hub Ecosystem

**Created:** 2026-10-09  
**Status:** In Execution  
**Current Phase:** Phase 4 (UI & Mobile Craft Optimization)  

---

## Phase 1: Engine Stability & Core Fixes (COMPLETED)
- [x] **1.1** Fix `ReferenceError: boot is not defined` in `public/js/pc-3d-scene.js`.
- [x] **1.2** Add defensive null-checks in `setRoom()` to prevent `setHex` runtime crashes.
- [x] **1.3** Clean up duplicate `setPart()` definitions and integrate procedural cables & animated drop.
- [x] **1.4** Verify 3D engine execution via Node VM simulator (Pass with 0 errors).

---

## Phase 2: Layout & Sticky Collision Resolution (COMPLETED)
- [x] **2.1** Restructure `src/pages/pc-builder-india.astro` into balanced 2-Column Studio Grid (`lg:grid-cols-12`).
- [x] **2.2** Move 12-component Bill of Materials (BOM) Table into full-width bottom section below viewport.
- [x] **2.3** Eliminate header slicing and awkward vertical stretching.
- [x] **2.4** Remove dead links (`/pc-lab-3d/index.html`).

---

## Phase 3: Mobile Responsiveness & Real-Time Sync (COMPLETED)
- [x] **3.1** Optimize 3D canvas viewport heights for mobile screens (`h-[340px]` to `h-[580px]`).
- [x] **3.2** Implement horizontal smooth-scrolling toolbars for camera presets, display apps, and room themes.
- [x] **3.3** Add real-time dynamic camera focus when switching components (PC Tower / Peripherals / Gadgets).
- [x] **3.4** Add glassmorphic Mobile Sticky Floating Action Bar with live price, wattage, and 1-click Amazon Cart button.
- [x] **3.5** Verify build integrity with `npm run build` (Exit code 0).

---

## Phase 4: Advanced Features & Polish (IN PROGRESS)
- [ ] **4.1** Implement Canvas-based Instagram Spec Card download in `pc-builder-india.astro`.
- [ ] **4.2** Enhance WhatsApp Share with clean formatted markdown + affiliate links (`uniquedigi0c6-21`).
- [ ] **4.3** Add interactive CPU/GPU bottleneck indicator percentage to FPS widget.
- [ ] **4.4** Add smooth sound effects (optional toggle for PC boot & part click).

---

## Phase 5: Verification & Production Ready
- [ ] **5.1** Test all 4 Quick Presets (₹35k, ₹55k, ₹85k, ₹1.5L+) on mobile and desktop.
- [ ] **5.2** Verify Amazon affiliate link generation for all 12 categories.
- [ ] **5.3** Complete production build check and Cloudflare Pages compatibility.
