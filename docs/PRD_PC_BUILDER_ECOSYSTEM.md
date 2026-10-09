# 📄 Product Requirements Document (PRD) — UniqueDigit 3D Battlestation & PC Studio

**Version:** 4.2 Pro  
**Status:** In Progress / Active  
**Author:** Google Antigravity & UniqueDigit Core Team  
**Primary Affiliate Tag:** `uniquedigi0c6-21` (Amazon India)  
**Target Market:** Indian PC Gamers, Content Creators, Tech Enthusiasts, & Mobile Shoppers  

---

## 1. Executive Summary & Product Vision

### 1.1 Problem Statement
In India, building a gaming PC or desk battlestation is plagued by fragmented sources:
- Pricing discrepancies between offline Nehru Place/Lamington Road and online Amazon India.
- Incompatible hardware choices (socket mismatches, RAM generation errors, cabinet GPU clearance issues, underpowered PSUs).
- Static 2D websites lacking visual engagement or real-time 3D feedback.
- Poor mobile optimization for phone-first Indian users.

### 1.2 Solution & Value Proposition
**UniqueDigit 3D Battlestation Studio** is India's first fully interactive, real-time 3D PC builder and desk ecosystem simulator:
1. **Real-time 3D WebGL Visualization**: 12 modular slots (CPU, GPU, Motherboard, RAM, NVMe SSD, Cabinet/PSU, Monitor, Keyboard, Mouse, MacBook/Laptop, Flagship Phone, Studio Audio).
2. **Dynamic Real-Time Sync**: Instant price calculation (₹ INR), power consumption (Watts), esports FPS benchmarks (Valorant, GTA V/6, Cyberpunk 2077, CS 2), and compatibility validation.
3. **Mobile-First Glassmorphism Experience**: Optimized viewport heights, touch gestures, and a floating sticky footer for seamless shopping on phones.
4. **1-Click High-Conversion Amazon Checkout**: Pre-tagged affiliate cart integration (`uniquedigi0c6-21`) + instant WhatsApp sharing & Instagram spec cards.

---

## 2. Target User Personas

| Persona | Description | Core Need | Key Feature |
|---|---|---|---|
| **Esports Gamer (Budget ₹35k - ₹55k)** | High school / college student wanting 1080p competitive smoothness. | High FPS in Valorant/CS 2 under budget. | ₹35k / ₹55k Quick Presets & FPS Predictor. |
| **Creator / Streamer (₹85k - ₹1.5L)** | Video editor & 1440p streamer. | Multitasking, NVMe speed, aesthetic ARGB studio. | Room themes, ARGB sync, studio tech gadgets. |
| **Enthusiast / Power User (₹1.5L+)** | Seeking flagship 4K performance & luxury battlestation. | Top-tier RTX 4080/4090, 240Hz OLED, flagship ecosystem. | Exploded 3D view, 360° Studio Tour, HWiNFO telemetry. |

---

## 3. System Architecture & Feature Breakdown

### 3.1 Three.js 3D WebGL Battlestation Engine
- **Chassis & Hardware Mesh Generation**: Real slot-based mounting with procedural cable routing (`CatmullRomCurve3`) and animated part drops.
- **Physical Materials**: Clearcoat glass side panel (`MeshPhysicalMaterial`), brushed aluminium, and emissive ARGB strips.
- **Interactive Displays**: Multi-mode monitor screens (HWiNFO Live Telemetry, Cyberpunk 2077, VS Code React, Synthwave).
- **Showroom Tech Ecosystem**: MacBook Pro 16", iPhone 16 Pro, Galaxy S25 Ultra, Studio Audiophile Headphones with close-up inspection HUD.
- **Camera Cockpit**: Presets (`hero`, `tower`, `peri`, `laptop`, `phone`, `headphones`), Exploded View toggle, and Cinematic 360° Tour.

### 3.2 Dynamic Catalog & Real-Time Engine
- **Catalog Structure**: Curated Indian market hardware with real Amazon ASINs, direct prices, specifications, and images.
- **Instant Calculations**:
  - `Total Price (INR)`: Real-time summation of selected parts.
  - `Estimated Wattage`: Accurate TDP calculations + 35% safety headroom.
  - `Esports FPS Predictor`: Algorithmic frame rate estimation for 1080p/1440p Ultra.
  - `Socket & Clearance Matrix`: Compatibility verification between CPU socket (AM4/AM5/LGA1700), DDR4/DDR5 RAM, and Motherboard chipset.

### 3.3 Mobile & Responsive Design Architecture
- **Responsive Viewport**: Fluid heights (`h-[340px]` on mobile to `h-[580px]` on desktop).
- **Mobile Floating Sticky Bar**: Fixed bottom HUD showing Live Total, Active Step, Wattage, Smooth 3D scroll, and 1-Click Amazon Buy.
- **Horizontal Scrolling Toolbars**: Zero awkward line breaks for camera buttons, presets, and ARGB palettes.

---

## 4. Monetization & Viral Conversion Strategy

1. **Direct Amazon India Cart Integration**:
   - Primary 1-Click Buy button linking to Amazon search/cart with `tag=uniquedigi0c6-21`.
   - Individual component "Buy on Amazon" links for each of the 12 items.
2. **Social Viral Loops**:
   - **WhatsApp Share**: One-click formatted message with full part breakdown and affiliate links.
   - **Instagram Spec Card**: Canvas-rendered snapshot of the custom build for Instagram Stories.
3. **SEO & Discovery**:
   - Target Keywords: `3d pc builder india`, `gaming pc setup simulator`, `custom pc builder amazon india`, `budget gaming pc 50000 india`.
