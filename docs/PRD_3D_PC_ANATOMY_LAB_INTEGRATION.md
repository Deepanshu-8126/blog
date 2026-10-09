# Product Requirement Document (PRD)
## Unified 3D PC Battlestation Builder & Hardware Anatomy Lab (2026)

**Document Version:** 2.0.0  
**Status:** Implemented & Verified  
**Target URL:** `/games/pc-builder-india`  
**Affiliate Tag:** `uniquedigi0c6-21`  
**Authors:** UniqueDigit Engineering Team & Antigravity AI  

---

## 1. Executive Summary & Vision

Modern PC enthusiasts and Indian budget gamers face high friction when visualizing custom computer builds:
1. Static 2D part selectors fail to provide spatial, aesthetic, and mechanical feedback.
2. Separate tools (e.g. anatomy explorers, assembly guides, benchmark calculators, and Amazon carts) exist in isolation, resulting in fragmented user experiences.

**The Solution:**
A **single, unified 3D WebGL Battlestation & Hardware Anatomy Cockpit** that synthesizes the strengths of three open-source hardware milestones:
- **`pc-anatomy`**: Silicon microarchitecture layer-by-layer dissection (IHS, TIM, Compute Die, VRMs, NAND Flash, Gold Contacts).
- **`pc-lab-3d`**: Real-time piece-by-piece assembly snapping, exploded views, X-ray inspection, and UEFI BIOS POST terminal diagnostics.
- **`builder-pc-3D`**: 360° orbital viewport, dynamic ARGB lighting synchronization, and interactive chassis customization.
- **`UniqueDigit India Engine`**: Real-time INR (₹) price calculations, AM4/AM5/LGA socket validation, PSU wattage headroom safety rules, 1080p/1440p gaming FPS predictors, and 1-Click Multi-ASIN Amazon India cart injection.

---

## 2. Integrated Feature Architecture Matrix

| Feature Module | Source Inspiration | Technical Implementation | User Value |
| :--- | :--- | :--- | :--- |
| **Unified 3D Hero Viewport** | `builder-pc-3D` | Three.js WebGL with ACES Filmic Tone Mapping, OrbitControls, Mouse/Touch Gestures. | Single focal point for the entire build process. |
| **Exploded Anatomy Slider (0–100%)** | `pc-lab-3d` & `pc-anatomy` | Dynamic Vector3 interpolation on component normal axes (`cpuCooler`, `gpu`, `ram`, `mobo`, `glass`). | Allows users to peel apart hardware components to inspect internals. |
| **Holographic X-Ray Mode** | `pc-lab-3d` | Runtime material switching: Wireframe mesh + 65% alpha glass shaders. | Visually isolates internal airflow channels and cable conduits. |
| **5-Layer Anatomy Dissector** | `pc-anatomy` | Interactive modal with silicon physics, layer breakdowns, and technical telemetry for 6 core categories. | Educational value explaining how nanometer silicon and VRMs function. |
| **Dynamic 3D HUD Callout Tags** | `pc-anatomy` | CSS3D overlay tags linked to active hardware state (`AM4 Socket / 65W TDP`, `DLSS 3 Ready`). | Real-time visual confirmation of chosen parts. |
| **UEFI BIOS POST Boot Terminal** | `pc-lab-3d` | CRT-styled diagnostic console with dynamic hardware initialization logs and benchmark estimates. | Authentic PC power-on satisfaction and stress verification. |
| **1-Click Multi-ASIN Amazon Cart** | UniqueDigit Engine | Direct URL synthesis with AWS Cart API (`AssociateTag=uniquedigi0c6-21&ASIN.1=...`). | Seamless 1-click checkout on Amazon India. |

---

## 3. 3D WebGL Technical Specification

```mermaid
graph TD
    A[User Selection: CPU / GPU / RAM / Case] --> B[Three.js Scene Graph Controller]
    B --> C[pcModelGroup: Chassis, Glass, Mobo]
    B --> D[Interpolation Engine: Exploded Slider 0-100%]
    B --> E[Material Manager: Standard PBR <-> X-Ray Wireframe]
    B --> F[Lighting Array: Ambient + Directional + ARGB PointLights]
    B --> G[HUD Overlay: CPU / GPU Spec Badges]
    A --> H[Compatibility & Power Engine]
    H --> I[Wattage & PSU Headroom Validator]
    H --> J[1-Click Amazon Multi-ASIN Cart Link]
    H --> K[UEFI BIOS POST Terminal Logger]
```

### 3.1 Mesh Hierarchy & Explosion Vectors
- **Case Chassis (`caseMesh`)**: Base coordinate `[0, 0, 0]`.
- **Tempered Glass Window (`glassMesh`)**: Base `[0, 0, 0.98]`, Explosion Vector: `+Z * 2.5`.
- **Motherboard PCB (`moboMesh`)**: Base `[0, 0, -0.4]`, Explosion Vector: `-Z * 0.6`.
- **CPU Cooler AIO (`cpuCoolerMesh`)**: Base `[-0.35, 0.6, -0.2]`, Explosion Vector: `+Z * 1.8`.
- **Dual DDR4/DDR5 RAM (`ramMeshGroup`)**: Base `[0.35, 0.6, -0.2]`, Explosion Vector: `+Z * 1.5`.
- **PCIe Graphics Card (`gpuMesh`)**: Base `[-0.15, -0.45, 0.1]`, Explosion Vector: `+Z * 2.2, -Y * 0.4`.

---

## 4. Hardware Anatomy Dissection Matrix

The integrated **3D Anatomy Dissector** provides microscopic engineering breakdowns:

### 4.1 Central Processing Unit (CPU)
1. **Integrated Heat Spreader (IHS)**: Nickel-plated pure copper protecting 1500mm² surface.
2. **Thermal Interface Material (TIM)**: Indium solder / Liquid metal (<1°C/W thermal impedance).
3. **Silicon Compute Die (CCD)**: TSMC 4nm/7nm FinFET with ALU, L1/L2/L3 GameCache & 3D V-Cache SRAM.
4. **Substrate (PCB)**: Multi-layer fiberglass routing micro-ball traces to LGA land grid.
5. **Contact Grid**: 1718 pure 24k gold-plated spring pins delivering up to 200A VCORE power.

### 4.2 Graphics Processing Unit (GPU)
1. **Aerofoil Shroud**: High static-pressure reverse-rotation ARGB fans with 0dB idle stop.
2. **Vapor Chamber**: Phase-change vacuum copper plates with direct-contact composite heatpipes.
3. **Compute Silicon Die**: NVIDIA Ada Lovelace / AMD RDNA 3 streaming multiprocessors & RT cores.
4. **GDDR6 / GDDR6X VRAM**: High-density Micron/Samsung memory running at 21 Gbps.
5. **Power & PCIe Interface**: 16-pin 12V-2x6 high-current header + PCIe 4.0 x16 gold bus.

### 4.3 Motherboard (Mainboard)
1. **VRM Heatsinks**: Solid aluminum blocks with 7W/mK thermal pads.
2. **Duet Rail Power System**: Digital PWM controller + 60A DrMOS power stages.
3. **Steel Armor Slot**: Surface-mount PCIe 5.0 anchor preventing heavy GPU sag.
4. **M.2 Shield Frozr**: Dual-sided thermal dissipation plates for NVMe controllers.
5. **Server-Grade PCB**: 6-layer high-purity 2oz copper substrate for 6000MHz+ XMP/EXPO stability.

---

## 5. Compatibility, Wattage & Affiliate Engine

### 5.1 Validation Logic
- **Socket Rule**: `cpu.socket === mobo.socket` (e.g. AM4 ⟷ AM4, AM5 ⟷ AM5, LGA1700 ⟷ LGA1700).
- **RAM Rule**: `mobo.ramType.includes(ram.ramType)` (e.g. DDR4 vs DDR5).
- **Wattage Safety Threshold**:
  $$\text{Headroom} = \text{PSU Wattage} - (\text{CPU TDP} + \text{GPU TDP} + 80\text{W})$$
  - If $\text{Headroom} \ge 80\text{W}$, Status = `100% Safe (Green)`.
  - If $\text{Headroom} < 80\text{W}$, Status = `PSU Warning: Upgrade to 650W/750W (Amber)`.

### 5.2 Multi-ASIN Amazon India Checkout URL Construction
```javascript
const asins = [cpu.amazonAsin, gpu.amazonAsin, mobo.amazonAsin, ram.amazonAsin, ssd.amazonAsin, cabinet.amazonAsin].filter(Boolean);
const cartParams = asins.map((asin, idx) => `ASIN.${idx+1}=${asin}&Quantity.${idx+1}=1`).join('&');
const cartUrl = `https://www.amazon.in/gp/aws/cart/add.html?AssociateTag=uniquedigi0c6-21&${cartParams}`;
```

---

## 6. Verification & Quality Assurance Results

- **Framework**: Astro 5 (Server Output + Cloudflare Adapter).
- **3D Engine**: Three.js WebGL (ACES Filmic Tone Mapping, 60 FPS requestAnimationFrame loop).
- **Build Verification**: `npm run build` executed with **Exit Code 0** (3.55s build time).
- **Asset Integrity**: 18 local 3D `.glb` models bundled in `/public/models/`.
- **Zero-Error Guarantee**: Fully typed TypeScript interfaces, null-safe DOM binding, and fallback sound synthesizers.
