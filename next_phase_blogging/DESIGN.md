# Design System Tokens & Dedicated Niche UI Specs

**Document:** `next_phase_blogging/DESIGN.md`  
**Framework:** Astro 5 + Tailwind CSS + Vanilla CSS Tokens  
**Typography:** Inter (Headings & Body), JetBrains Mono / Space Mono (Telemetry & Metrics)  
**Aesthetic:** Modern Glassmorphism, Deep Dark Viewports, Ambient Glow Backdrops, Zero Distortion

---

## 1. Global Design Tokens

```css
:root {
  /* Surface & Base */
  --bg-canvas: #090d16;
  --bg-card: #0f172a;
  --bg-card-subtle: #1e293b;
  --border-subtle: rgba(255, 255, 255, 0.08);
  --border-focus: rgba(99, 102, 241, 0.4);

  /* Typography Colors */
  --text-primary: #f8fafc;
  --text-secondary: #94a3b8;
  --text-muted: #64748b;
  --text-accent: #38bdf8;

  /* Universal Shadows & Ambient Radii */
  --radius-card: 1.5rem;      /* 24px */
  --radius-button: 0.875rem;  /* 14px */
  --radius-chip: 9999px;
  --shadow-ambient: 0 20px 40px -15px rgba(0, 0, 0, 0.7);
}
```

---

## 2. Dedicated Niche Color Schemes & Atmospheres

Each specialized niche hub features an atmospheric palette tailored to user emotion and domain intent:

```
┌────────────────────────────────────────────────────────────────────────┐
│                      NICHE PALETTE MATRIX                              │
├───────────────────┬─────────────────────────────────┬──────────────────┤
│ Niche             │ Dominant Accents                │ Psychological Tone│
├───────────────────┼─────────────────────────────────┼──────────────────┤
│ 🩺 Healthcare     │ Emerald (#10b981) + Cyan        │ Trust, Clarity,  │
│                   │ Tint: rgba(16, 185, 129, 0.12)  │ Vitality         │
├───────────────────┼─────────────────────────────────┼──────────────────┤
│ 📰 Newsroom       │ Crimson (#ef4444) + Amber       │ Urgency, Breaking│
│                   │ Tint: rgba(239, 68, 68, 0.12)   │ Telemetry        │
├───────────────────┼─────────────────────────────────┼──────────────────┤
│ 🎬 Cinema & OTT   │ Purple (#8b5cf6) + Gold (#fbbf24)│ Theatrical Drama,│
│                   │ Tint: rgba(139, 92, 246, 0.15)  │ Cinema Lighting  │
├───────────────────┼─────────────────────────────────┼──────────────────┤
│ 🛍️ Deals Radar    │ Fuchsia (#d946ef) + Neon Lime   │ High Excitement, │
│                   │ Tint: rgba(217, 70, 239, 0.14)  │ Flash Drops      │
├───────────────────┼─────────────────────────────────┼──────────────────┤
│ ⚡ Tech & AI      │ Electric Indigo (#6366f1) + Sky │ Precision, High  │
│                   │ Tint: rgba(99, 102, 241, 0.12)  │ Performance      │
└───────────────────┴─────────────────────┴──────────────────────────────┘
```

---

## 3. Dedicated Component Specifications

### 3.1. Healthcare Trust Badge & Safety Box (`HealthDisclaimer.astro`)
```html
<div class="rounded-2xl border border-emerald-500/30 bg-emerald-950/20 p-4 backdrop-blur-md">
  <div class="flex items-center gap-2 mb-2">
    <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
    <span class="text-xs font-mono font-bold uppercase tracking-wider text-emerald-300">
      Verified Medical Protocol
    </span>
  </div>
  <p class="text-xs text-slate-300 leading-relaxed">
    <strong>Educational Notice:</strong> Verified against Ministry of AYUSH and clinical literature. Consult a certified medical doctor before taking any supplements or beginning intense workouts.
  </p>
</div>
```

### 3.2. Cinema Box Office Collection Matrix (`BoxOfficeTable.astro`)
```html
<div class="rounded-2xl overflow-hidden border border-purple-500/20 bg-slate-900/90 shadow-2xl">
  <div class="bg-gradient-to-r from-purple-900/60 to-slate-900 px-4 py-3 border-b border-purple-500/20 flex justify-between items-center">
    <h4 class="text-xs font-black uppercase tracking-wider text-purple-200">Theatrical Box Office Tracker</h4>
    <span class="text-[10px] font-mono text-amber-300">Worldwide Gross</span>
  </div>
  <table class="w-full text-xs text-left">
    <thead class="bg-white/5 text-slate-400 font-mono text-[10px]">
      <tr>
        <th class="p-3">Timeline</th>
        <th class="p-3">India Net</th>
        <th class="p-3">Overseas</th>
        <th class="p-3">Worldwide Total</th>
      </tr>
    </thead>
    <tbody class="divide-y divide-white/5 text-slate-200 font-medium">
      <tr>
        <td class="p-3 font-bold text-white">Opening Weekend</td>
        <td class="p-3">₹142.50 Cr</td>
        <td class="p-3">₹48.00 Cr</td>
        <td class="p-3 font-mono font-bold text-amber-300">₹190.50 Cr</td>
      </tr>
    </tbody>
  </table>
</div>
```

### 3.3. Double-Layer Ambient Image Frame (`AmbientMediaFrame.astro`)
```html
<div class="relative w-full aspect-video rounded-3xl overflow-hidden bg-slate-950 flex items-center justify-center border border-white/10 shadow-ambient group">
  <!-- Background Ambient Glow -->
  <img
    src={proxyImageUrl(url)}
    alt=""
    aria-hidden="true"
    loading="lazy"
    class="absolute inset-0 w-full h-full object-cover filter blur-2xl opacity-40 scale-110 pointer-events-none"
  />
  <div class="absolute inset-0 bg-slate-950/25 backdrop-blur-[1px]"></div>

  <!-- Foreground Natural Image (Zero Cropping, Crisp Edges) -->
  <img
    src={proxyImageUrl(url)}
    alt={title}
    loading="lazy"
    class="relative z-10 max-h-full max-w-full object-contain filter drop-shadow-[0_15px_30px_rgba(0,0,0,0.85)] group-hover:scale-105 transition-transform duration-500"
    onerror={`this.onerror=null; this.src='${fallbackUrl}';`}
  />
</div>
```
