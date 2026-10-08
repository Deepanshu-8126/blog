/* ============================================================
   PC Lab 3D — part definitions & 3D builders
   Four modes: e (Elementary), h (High School), c (College), t (Tinkerer)
   ============================================================ */
window.PC = window.PC || {};

PC.MODE_ORDER = ["e", "h", "c", "t"];

PC.MODES = {
  e: {
    id: "e", name: "Elementary", emoji: "🧒", color: "#4ade80",
    tagline: "Main parts in everyday words",
    cam: { pos: [98, 56, 94], tgt: [0, 24, 0] },
    entry: [150, 85, 170], explodeScale: 30,
    seq: ["case","psu","mobo","cpu","cooler","ram0","storage","gpu","panel","monitor"],
    boot: ["Turning on… ✓","The brain is thinking! 🧠","Memory is ready! 📝","Storage is ready! 💾","The screen works! 🖥️","All done — great job! 🎉"]
  },
  h: {
    id: "h", name: "High School", emoji: "🎒", color: "#38bdf8",
    tagline: "Main parts + real technical terms",
    cam: { pos: [98, 56, 94], tgt: [0, 24, 0] },
    entry: [150, 85, 170], explodeScale: 30,
    seq: ["case","psu","mobo","cpu","paste","cooler","ram0","ram1","ssd","hdd","gpu","cables","panel","monitor"],
    boot: ["PC Lab UEFI v3.1","CPU: 8 cores @ 4.5 GHz … OK","Memory: 16 GB DDR5 … OK","Storage: SSD 1 TB … OK","GPU: initialized … OK","All systems nominal","Booting OS…"]
  },
  c: {
    id: "c", name: "College", emoji: "🎓", color: "#a78bfa",
    tagline: "Full build: peripherals, power, cables",
    cam: { pos: [98, 56, 94], tgt: [0, 24, 0] },
    entry: [150, 85, 170], explodeScale: 30,
    seq: ["case","psu","mobo","cables24","cables8","cpu","aio","ram0","ram1","nvme","ssd","hdd","gpu","pciecable","sata","wifi","fans","fpanel","panel","monitor","keyboard","mouse","speakers","webcam"],
    boot: ["AMI BIOS v3.1.0","CPU: Core i7 — 8C/16T … OK","RAM: 32 GB DDR5-6000 … OK","NVMe: 2 TB @ PCIe 4.0 x4 … OK","GPU: PCIe x16, 16 GB … OK","USB: 14 devices found","LAN: 2.5 GbE link up","All checks passed","Booting OS…"]
  },
  t: {
    id: "t", name: "Tinkerer", emoji: "🔧", color: "#fbbf24",
    tagline: "Motherboard-level: chips & electronics",
    cam: { pos: [0, 58, 106], tgt: [0, 6, 0] },
    entry: [0, 108, 84], explodeScale: 22,
    seq: ["pcb","ios","socket","cpu","vrm-mos","vrm-choke","vrm-cap","dimm","ram0","ram1","chipset","bios","crystal","cmos","m2slot","nvme","sata","headers","audio","lan","pcie"],
    boot: ["Power good: 3.3 V ✓  5 V ✓  12 V ✓","VRM phases: 8 active","Clock: 32.768 kHz ✓","SPI flash: UEFI loaded","Memory training… OK","POST code: 0x7E","Handoff to OS ✓"]
  }
};

/* ============================ Textures ============================ */
PC.Tex = (function () {
  function canvas(w, h) {
    const c = document.createElement("canvas");
    c.width = w; c.height = h;
    return c;
  }
  function tex(c) {
    const t = new THREE.CanvasTexture(c);
    t.colorSpace = THREE.SRGBColorSpace;
    t.anisotropy = 4;
    return t;
  }

  /* PCB trace texture */
  const traces = (function () {
    const c = canvas(512, 512);
    const x = c.getContext("2d");
    x.fillStyle = "#145c3e"; x.fillRect(0, 0, 512, 512);
    x.strokeStyle = "#35a06c"; x.lineWidth = 3;
    for (let i = 0; i < 46; i++) {
      let px = 20 + Math.random() * 472, py = 20 + Math.random() * 472;
      x.beginPath(); x.moveTo(px, py);
      for (let s = 0; s < 5; s++) {
        const horiz = Math.random() < 0.5;
        const len = 30 + Math.random() * 90;
        px = Math.min(492, Math.max(20, px + (horiz ? len * (Math.random() < 0.5 ? 1 : -1) : 0)));
        py = Math.min(492, Math.max(20, py + (horiz ? 0 : len * (Math.random() < 0.5 ? 1 : -1))));
        x.lineTo(px, py);
      }
      x.stroke();
    }
    x.fillStyle = "#c9a45c";
    for (let i = 0; i < 130; i++) {
      x.beginPath();
      x.arc(20 + Math.random() * 472, 20 + Math.random() * 472, 2.2 + Math.random() * 2.6, 0, Math.PI * 2);
      x.fill();
    }
    const t = tex(c);
    return { texture: t };
  })();

  const pcbFaceMat = new THREE.MeshStandardMaterial({ map: traces.texture, roughness: 0.45, metalness: 0.25 });
  const pcbEdgeMat = new THREE.MeshStandardMaterial({ color: 0x1a4a36, roughness: 0.7, metalness: 0.1 });

  /* Screen (monitor) */
  const screenCanvas = canvas(640, 400);
  const screenCtx = screenCanvas.getContext("2d");
  screenCtx.fillStyle = "#02040a"; screenCtx.fillRect(0, 0, 640, 400);
  const screenTex = tex(screenCanvas);
  const screenMat = new THREE.MeshStandardMaterial({
    map: screenTex, emissive: 0xffffff, emissiveMap: screenTex,
    emissiveIntensity: 0.9, roughness: 0.35, metalness: 0.05
  });

  /* Keyboard keycaps */
  const keys = (function () {
    const c = canvas(1024, 288);
    const x = c.getContext("2d");
    x.fillStyle = "#141821"; x.fillRect(0, 0, 1024, 288);
    const cols = 15, rows = 5;
    const pad = 14, gap = 6;
    const kw = (1024 - pad * 2 - gap * (cols - 1)) / cols;
    const kh = (288 - pad * 2 - gap * (rows - 1)) / rows;
    for (let r = 0; r < rows; r++) {
      for (let cc = 0; cc < cols; cc++) {
        const kx = pad + cc * (kw + gap), ky = pad + r * (kh + gap);
        x.fillStyle = "#2b323f";
        x.beginPath();
        x.roundRect(kx, ky, kw, kh, 7);
        x.fill();
        x.fillStyle = "rgba(255,255,255,0.10)";
        x.beginPath();
        x.roundRect(kx + 3, ky + 3, kw - 6, kh - 10, 5);
        x.fill();
      }
    }
    const t = tex(c);
    const mat = new THREE.MeshStandardMaterial({ map: t, roughness: 0.6 });
    return { texture: t, mat };
  })();

  /* Generic label sticker */
  function label(text, w, h, bg, fg, fs) {
    const c = canvas(w, h);
    const x = c.getContext("2d");
    x.fillStyle = bg || "#1b2029"; x.fillRect(0, 0, w, h);
    x.fillStyle = fg || "#9fb2c8";
    x.font = "700 " + (fs || Math.round(h * 0.42)) + "px 'Segoe UI', Arial, sans-serif";
    x.textAlign = "center"; x.textBaseline = "middle";
    x.fillText(text, w / 2, h / 2);
    return tex(c);
  }

  /* Fan hub decal */
  const fanDecal = label("PC LAB", 128, 128, "#151a23", "#4d5a6e", 26);

  return {
    pcbFaceMat, pcbEdgeMat, traces,
    screen: { canvas: screenCanvas, ctx: screenCtx, texture: screenTex, mat: screenMat },
    keysMat: keys.mat,
    label,
    fanDecal
  };
})();

/* ============================ Helpers ============================ */
PC.Parts = (function () {
  const geoCache = {};
  function rboxGeo(w, h, d, r) {
    const key = w + "|" + h + "|" + d + "|" + r;
    if (geoCache[key]) return geoCache[key];
    const ww = Math.max(0.02, w - 2 * r), hh = Math.max(0.02, h - 2 * r), dd = Math.max(0.02, d - 2 * r);
    const s = new THREE.Shape();
    const x0 = -ww / 2, y0 = -hh / 2;
    s.moveTo(x0 + r, y0);
    s.lineTo(x0 + ww - r, y0);
    s.absarc(x0 + ww - r, y0 + r, r, -Math.PI / 2, 0, false);
    s.lineTo(x0 + ww, y0 + hh - r);
    s.absarc(x0 + ww - r, y0 + hh - r, r, 0, Math.PI / 2, false);
    s.lineTo(x0 + r, y0 + hh);
    s.absarc(x0 + r, y0 + hh - r, r, Math.PI / 2, Math.PI, false);
    s.lineTo(x0, y0 + r);
    s.absarc(x0 + r, y0 + r, r, Math.PI, Math.PI * 1.5, false);
    const g = new THREE.ExtrudeGeometry(s, {
      depth: dd, bevelEnabled: true, bevelThickness: r,
      bevelSize: Math.max(0.001, r - 0.001), bevelSegments: 2, curveSegments: 8
    });
    g.translate(0, 0, -dd / 2);
    geoCache[key] = g;
    return g;
  }

  function makeP() {
    const p = {};
    p.mat = (color, opts) => new THREE.MeshStandardMaterial(Object.assign(
      { color: color || 0x222222, roughness: 0.55, metalness: 0.2 }, opts || {}));
    p.mesh = (geo, color, opts) => {
      const m = new THREE.Mesh(geo, p.mat(color, opts));
      m.castShadow = !opts || opts.castShadow !== false;
      m.receiveShadow = true;
      m.at = function (x, y, z) { this.position.set(x, y, z); return this; };
      return m;
    };
    p.rbox = (w, h, d, r, color, opts) => p.mesh(rboxGeo(w, h, d, r), color, opts);
    p.box = (w, h, d, color, opts) => p.mesh(new THREE.BoxGeometry(w, h, d), color, opts);
    p.cyl = (rt, rb, h, seg, color, opts) => p.mesh(new THREE.CylinderGeometry(rt, rb, h, seg || 24), color, opts);
    p.sphere = (r, color, opts) => p.mesh(new THREE.SphereGeometry(r, 26, 18), color, opts);
    p.torus = (R, rt, color, opts) => p.mesh(new THREE.TorusGeometry(R, rt, 10, 32), color, opts);
    p.tube = (pts, r, color, opts) => p.mesh(new THREE.TubeGeometry(
      new THREE.CatmullRomCurve3(pts.map(q => new THREE.Vector3(q[0], q[1], q[2]))),
      Math.max(10, pts.length * 8), r, 10, false), color, opts);
    p.grp = () => new THREE.Group();
    return p;
  }

  /* Fan facing +x. Returns {group, blades, spin} */
  function fan(P, size, depth, bladeColor, frameColor) {
    const group = P.grp();
    group.add(P.rbox(depth, size, size, depth * 0.4, frameColor, { roughness: 0.6 }));
    const ring = P.torus(size * 0.36, depth * 0.3, 0x141922, { roughness: 0.7 });
    ring.rotation.y = Math.PI / 2;
    group.add(ring);
    const blades = P.grp();
    const hub = P.cyl(size * 0.09, size * 0.09, depth + 0.5, 16, bladeColor, { roughness: 0.45 });
    hub.rotation.z = Math.PI / 2;
    blades.add(hub);
    const decal = new THREE.Mesh(new THREE.CircleGeometry(size * 0.07, 18), new THREE.MeshStandardMaterial({ map: PC.Tex.fanDecal, roughness: 0.4 }));
    decal.position.x = depth / 2 + 0.28; decal.rotation.y = Math.PI / 2;
    blades.add(decal);
    for (let i = 0; i < 7; i++) {
      const b = P.box(depth + 0.4, size * 0.27, size * 0.075, bladeColor, { roughness: 0.45 });
      b.position.y = size * 0.185;
      b.rotation.x = (i / 7) * Math.PI * 2;
      blades.add(b);
    }
    group.add(blades);
    return { group, blades, spin: { obj: blades, axis: "x", speed: 6.5 } };
  }

  /* ============ Anchor positions (fixed) ============ */
  const TOWER = { casePos: [0, 0, 0], mobo: [-11.6, 23.25, 0] };
  const TINK = { pcb: [0, 0.4, 0] };
  const moboW = (lx, ly, lz) => [TOWER.mobo[0] + lx, TOWER.mobo[1] + ly, TOWER.mobo[2] + lz];
  const boardW = (lx, ly, lz) => [TINK.pcb[0] + lx, TINK.pcb[1] + ly, TINK.pcb[2] + lz];

  /* ============================ Tower builders ============================ */

  function buildCase(P) {
    const g = P.grp();
    const M = 0x3a4352, MD = 0x2c333f;
    g.add(P.rbox(26, 1.2, 46, 0.5, MD).at(0, 0.6, 0));
    g.add(P.rbox(26, 1.2, 46, 0.5, MD).at(0, 47.4, 0));
    g.add(P.rbox(1.4, 48, 46, 0.4, M).at(-12.3, 24, 0));
    /* feet */
    g.add(P.rbox(3, 0.9, 3, 0.3, 0x171b22).at(-8, -0.15, -18));
    g.add(P.rbox(3, 0.9, 3, 0.3, 0x171b22).at(-8, -0.15, 18));
    g.add(P.rbox(3, 0.9, 3, 0.3, 0x171b22).at(8, -0.15, -18));
    g.add(P.rbox(3, 0.9, 3, 0.3, 0x171b22).at(8, -0.15, 18));
    const frontMat = new THREE.MeshStandardMaterial({ color: 0x0c0f15, roughness: 0.35, metalness: 0.3, transparent: true, opacity: 0.5 });
    const front = new THREE.Mesh(rboxGeo(26, 48, 1.4, 0.5), frontMat);
    front.position.set(0, 24, 22.3);
    g.add(front);
    const cut1 = P.cyl(4.3, 4.3, 1.7, 26, 0x0a0d12, { roughness: 0.9 });
    cut1.rotation.x = Math.PI / 2; cut1.position.set(0, 10, 23.1); g.add(cut1);
    const cut2 = P.cyl(4.3, 4.3, 1.7, 26, 0x0a0d12, { roughness: 0.9 });
    cut2.rotation.x = Math.PI / 2; cut2.position.set(0, 32, 23.1); g.add(cut2);
    /* drive cage (front-bottom) */
    g.add(P.rbox(0.6, 15, 13, 0.2, M).at(-6.9, 14, 14.3));
    g.add(P.rbox(0.6, 15, 13, 0.2, M).at(-3.1, 14, 14.3));
    /* power button + front I/O */
    const btn = P.cyl(0.85, 0.85, 1.5, 18, 0x10151f, { roughness: 0.3 });
    btn.position.set(7, 48.05, 16); g.add(btn);
    const usb = P.box(2.4, 0.5, 1.3, 0x0c1018, { roughness: 0.4 });
    usb.position.set(10, 48.05, 16); g.add(usb);
    /* RGB strip (power LED) */
    const stripMat = P.mat(0x111111, { emissive: 0x000000, emissiveIntensity: 0, roughness: 0.4 });
    const strip = new THREE.Mesh(rboxGeo(21, 0.8, 0.8, 0.3), stripMat);
    strip.position.set(0, 45.4, 21.2); g.add(strip);
    /* rear exhaust ring */
    const rear = P.torus(4.3, 0.35, 0x141922, { roughness: 0.7 });
    rear.position.set(0, 38, -23.4); g.add(rear);
    return { group: g, leds: [{ mat: stripMat, color: 0x35e0ff, intensity: 3.0 }] };
  }

  function buildPanel(P) {
    const g = P.grp();
    const frameMat = P.mat(0x2b323d, { roughness: 0.5, metalness: 0.6 });
    g.add(P.rbox(1.4, 45.6, 41.6, 0.3, 0x2b323d, { roughness: 0.5, metalness: 0.6 }));
    const glass = new THREE.Mesh(rboxGeo(0.6, 42.5, 38.5, 0.3),
      new THREE.MeshStandardMaterial({ color: 0xa8d8ee, roughness: 0.06, metalness: 0.1, transparent: true, opacity: 0.28 }));
    glass.position.set(0.15, 0, 0); g.add(glass);
    const thumb = P.cyl(0.55, 0.55, 0.8, 14, 0x39424f, { metalness: 0.7, roughness: 0.3 });
    thumb.rotation.z = Math.PI / 2; thumb.position.set(0.9, 18, 0); g.add(thumb);
    return { group: g };
  }

  function buildPsu(P) {
    const g = P.grp();
    g.add(P.rbox(14, 8.6, 16, 0.9, 0x232833, { roughness: 0.4, metalness: 0.4 }));
    const sticker = new THREE.Mesh(new THREE.BoxGeometry(6.6, 3.4, 0.3),
      new THREE.MeshStandardMaterial({ map: PC.Tex.label("650W · 80+ GOLD", 256, 128, "#232833", "#c9d2df", 30), roughness: 0.5 }));
    sticker.position.set(0.3, 0, 8.1); g.add(sticker);
    const grill = P.torus(3.6, 0.3, 0x151a23, { roughness: 0.7 });
    grill.rotation.x = Math.PI / 2; grill.position.set(0, -4.4, 0); g.add(grill);
    const plug = P.box(2.6, 1.4, 1.2, 0x0c1018); plug.position.set(0, 3, -8.2); g.add(plug);
    const sw = P.box(1.2, 1.0, 0.8, 0x3d4653, { roughness: 0.4 }); sw.position.set(5.5, 3, -8.1); g.add(sw);
    return { group: g };
  }

  function buildMobo(P) {
    const g = P.grp();
    /* board plane YZ, facing +x: +x face gets the PCB texture */
    const geo = new THREE.BoxGeometry(0.4, 30.5, 24.4);
    const board = new THREE.Mesh(geo, [PC.Tex.pcbFaceMat, PC.Tex.pcbEdgeMat, PC.Tex.pcbEdgeMat, PC.Tex.pcbEdgeMat, PC.Tex.pcbEdgeMat, PC.Tex.pcbEdgeMat]);
    g.add(board);
    /* CPU socket area */
    g.add(P.rbox(0.16, 5.6, 5.6, 0.15, 0x0a0d12).at(0.1, 8.5, 0));
    g.add(P.rbox(0.12, 6.0, 6.0, 0.12, 0x39424f).at(0.16, 8.5, 0));
    /* VRM heatsinks */
    g.add(P.rbox(0.55, 3.6, 1.7, 0.15, 0x4a5362, { metalness: 0.7, roughness: 0.35 }).at(0.35, 8.5, -4.4));
    g.add(P.rbox(0.55, 3.6, 1.7, 0.15, 0x4a5362, { metalness: 0.7, roughness: 0.35 }).at(0.35, 8.5, 4.4));
    /* DIMM slot deco */
    for (const z of [-4.5, -1.5, 1.5, 4.5]) {
      g.add(P.rbox(0.5, 0.6, 13.6, 0.2, 0x0b0e13, { roughness: 0.7 }).at(0.12, 8.25, z));
    }
    /* PCIe x16 slot deco */
    g.add(P.rbox(0.32, 0.55, 12.6, 0.1, 0x0b0e13).at(0.1, -7.5, 0));
    g.add(P.rbox(0.3, 0.7, 3.6, 0.1, 0x8d97a5, { metalness: 0.8, roughness: 0.3 }).at(0.12, -7.5, -13.4));
    /* M.2 deco */
    g.add(P.rbox(0.14, 0.4, 8.6, 0.1, 0x0b0e13).at(0.08, -2.5, 0));
    /* chipset heatsink */
    g.add(P.rbox(0.6, 3.6, 3.6, 0.2, 0x39424f, { metalness: 0.6, roughness: 0.4 }).at(0.35, -3, 7.6));
    g.add(P.rbox(0.6, 2.2, 2.2, 0.2, 0x39424f, { metalness: 0.6, roughness: 0.4 }).at(0.35, -12.5, 5));
    /* capacitors */
    for (let i = 0; i < 5; i++) {
      const cap = P.cyl(0.5, 0.5, 0.8, 14, 0x2a3340, { roughness: 0.35 });
      cap.rotation.z = Math.PI / 2; cap.position.set(0.5, 1.6, -9.5 + i * 2.2);
      g.add(cap);
    }
    /* rear I/O cluster — vertical stack hugging the board's top-rear edge
       (board is 30.5 tall → ±15.25; base 3 keeps ports −0.5…14.95 on the board) */
    const ioY = [-3.5, -1.5, 0.5, 2.5, 4.5, 6.5, 9.5, 11.5];
    const ioC = [0x1d4ed8, 0x1d4ed8, 0x9aa4b2, 0x0c0e13, 0xb91c1c, 0x111827, 0x34d399, 0xec4899];
    for (let i = 0; i < 8; i++) {
      g.add(P.box(0.6, i < 6 ? 1.1 : 0.9, 1.7, ioC[i], { roughness: 0.4 }).at(0.35, 3 + ioY[i], -12.3));
    }
    return { group: g };
  }

  function buildCpu(P, scale) {
    const g = P.grp();
    const s = scale || 1;
    const ihs = P.rbox(4.6 * s, 0.5 * s, 4.6 * s, 0.35, 0xd9dee6, { metalness: 0.8, roughness: 0.22 });
    ihs.position.set(0, 0.3 * s, 0);
    const sub = P.rbox(4.8 * s, 0.3 * s, 4.8 * s, 0.3, 0x1d4d2e, { roughness: 0.5 });
    sub.position.set(0, -0.04 * s, 0);
    const gold = P.rbox(4.9 * s, 0.07 * s, 4.9 * s, 0.2, 0xc9a45c, { metalness: 0.9, roughness: 0.25 });
    gold.position.set(0, -0.2 * s, 0);
    const dot = P.box(0.5, 0.04, 0.5, 0x8d97a5, { metalness: 0.7, roughness: 0.3 });
    dot.position.set(-1.8 * s, 0.56 * s, 1.8 * s);
    g.add(ihs, sub, gold, dot);
    return { group: g };
  }

  function buildCooler(P) {
    const g = P.grp();
    /* tower cooler standing in front of the board, fan facing viewer */
    g.add(P.rbox(5.6, 0.9, 5.6, 0.3, 0x9aa4b2, { metalness: 0.85, roughness: 0.3 }).at(0.45, 0.45, 0));
    for (const [dy, dz] of [[0.4, -2.0], [0.4, 2.0], [0.4, -1.0], [0.4, 1.0]]) {
      const pipe = P.cyl(0.32, 0.32, 7.2, 12, 0x7d8794, { metalness: 0.9, roughness: 0.25 });
      pipe.rotation.z = Math.PI / 2; pipe.position.set(3.8, dy, dz); g.add(pipe);
    }
    g.add(P.rbox(6.2, 9.6, 9.8, 0.4, 0x6b7483, { metalness: 0.85, roughness: 0.4 }).at(4.3, 5.2, 0));
    g.add(P.rbox(6.2, 0.5, 9.8, 0.3, 0x5a626f, { metalness: 0.8, roughness: 0.4 }).at(4.3, 10.05, 0));
    const f = fan(P, 9.6, 2.2, 0x232a35, 0x161b24);
    f.group.position.set(8.3, 5.2, 0);
    g.add(f.group);
    return { group: g, spin: [f.spin] };
  }

  function buildRam(P, withSlot, scale, rise) {
    const g = P.grp();
    const s = scale || 1, up = rise === "y";
    if (withSlot !== false) {
      g.add(P.rbox(0.55, 0.5, 13.8 * s, 0.22, 0x0c0f14, { roughness: 0.7 }).at(0, 0.25, 0));
    }
    const stick = up
      ? P.rbox(0.32, 3.4 * s, 13.4 * s, 0.15, 0x1d2836, { roughness: 0.4 }).at(0, 1.9 * s, 0)
      : P.rbox(3.4 * s, 0.35, 13.4 * s, 0.15, 0x1d2836, { roughness: 0.4 }).at(1.9 * s, 0.45, 0);
    const sp = up
      ? P.rbox(0.4, 0.7 * s, 13.4 * s, 0.12, 0x39424f, { metalness: 0.5, roughness: 0.35 }).at(0, 3.2 * s, 0)
      : P.rbox(0.4, 0.7 * s, 13.4 * s, 0.12, 0x39424f, { metalness: 0.5, roughness: 0.35 }).at(3.3 * s, 0.45, 0);
    const pins = up
      ? P.box(0.12, 0.5 * s, 12.6 * s, 0xc9a45c, { metalness: 0.9, roughness: 0.25 }).at(0, 0.75 * s, 0)
      : P.box(0.5 * s, 0.12, 12.6 * s, 0xc9a45c, { metalness: 0.9, roughness: 0.25 }).at(1.0 * s, 0.45, 0);
    g.add(stick, sp, pins);
    return { group: g };
  }

  function buildGpu(P) {
    const g = P.grp();
    g.add(P.rbox(2.4, 11.2, 26.4, 0.3, 0x2e3848, { roughness: 0.35 }).at(0, 0, 0));
    g.add(P.rbox(2.7, 11.6, 26.8, 0.3, 0x465062, { metalness: 0.6, roughness: 0.3 }).at(-1.2, 0, 0));
    const bracket = P.rbox(1.2, 10.5, 0.6, 0.2, 0x9aa4b2, { metalness: 0.85, roughness: 0.3 });
    bracket.position.set(0.2, 0, -13.4); g.add(bracket);
    const conn = P.rbox(0.55, 1.0, 12.6, 0.15, 0xc9a45c, { metalness: 0.9, roughness: 0.25 });
    conn.position.set(-0.4, -5.9, 0); g.add(conn);
    const f1 = fan(P, 6.8, 1.7, 0x3a4658, 0x232c39);
    f1.group.position.set(1.55, 1.4, -6.5); g.add(f1.group);
    const f2 = fan(P, 6.8, 1.7, 0x3a4658, 0x232c39);
    f2.group.position.set(1.55, 1.4, 6.5); g.add(f2.group);
    return { group: g, spin: [f1.spin, f2.spin] };
  }

  function buildDrive(P, kind) {
    const g = P.grp();
    if (kind === "hdd") {
      g.add(P.rbox(2.6, 10.2, 14.2, 0.35, 0x232833, { roughness: 0.4, metalness: 0.5 }).at(0, 0, 0));
      g.add(P.rbox(2.75, 9.6, 13.6, 0.3, 0x39424f, { metalness: 0.7, roughness: 0.3 }).at(1.25, 0, 0));
      const label = new THREE.Mesh(new THREE.BoxGeometry(0.3, 4.4, 5.6),
        new THREE.MeshStandardMaterial({ map: PC.Tex.label("HDD 2 TB", 256, 128, "#2b323d", "#aeb8c6", 30), roughness: 0.5 }));
      label.position.set(1.42, 0.6, -3); g.add(label);
    } else {
      g.add(P.rbox(1.25, 7.2, 9.6, 0.3, 0x1d232d, { roughness: 0.4, metalness: 0.5 }).at(0, 0, 0));
      const label = new THREE.Mesh(new THREE.BoxGeometry(0.3, 4.6, 6.2),
        new THREE.MeshStandardMaterial({ map: PC.Tex.label(kind === "storage" ? "STORAGE" : "SSD 1 TB", 256, 128, "#20262f", "#aeb8c6", 34), roughness: 0.5 }));
      label.position.set(0.74, 0.2, -0.4); g.add(label);
      const conn = P.box(0.5, 0.9, 3.2, 0x0c0e13); conn.position.set(0.55, 0, 4.6); g.add(conn);
    }
    return { group: g };
  }

  function cable(P, pts, r, color, connA, connB) {
    const g = P.grp();
    g.add(P.tube(pts, r, color, { roughness: 0.6, metalness: 0.1 }));
    if (connA) { const c = P.rbox(connA[0], connA[1], connA[2], 0.2, 0x0c0e13, { roughness: 0.6 }); c.position.set(...pts[0]); g.add(c); }
    if (connB) { const c = P.rbox(connB[0], connB[1], connB[2], 0.2, 0x0c0e13, { roughness: 0.6 }); c.position.set(...pts[pts.length - 1]); g.add(c); }
    return g;
  }

  function buildCablesH(P) { /* high school: 24-pin + EPS in one part */
    const g = P.grp();
    /* group origin = mobo 24-pin conn local (12.0, -9.5, 0) */
    g.add(cable(P, [[0, 0, 0], [4, -2, 3], [8, -6, 0], [11, -9, -5], [13.1, -14.65, -8]], 0.62, 0x171a20, [2.9, 1.5, 6.4], [2.3, 1.4, 5.4]));
    /* EPS conn at mobo local (-7.2, 15.1, 0) → offset from group origin */
    const eps = [-7.2 - 12.0, 15.1 + 9.5, 0];
    g.add(cable(P, [eps, [eps[0] + 5, eps[1] - 8, eps[2]], [eps[0] + 10, eps[1] - 18, -2], [20.3 - 12.0, -29.75 + 9.5, -5]], 0.5, 0x2a2f38, [1.6, 1.3, 4.6], [1.6, 1.3, 4.0]));
    return { group: g };
  }

  function buildCables24(P) {
    const g = P.grp();
    g.add(cable(P, [[0, 0, 0], [4, -2, 3], [8, -6, 0], [11, -9, -5], [13.1, -14.65, -8]], 0.62, 0x171a20, [2.9, 1.5, 6.4], [2.3, 1.4, 5.4]));
    return { group: g };
  }

  function buildCables8(P) {
    const g = P.grp();
    g.add(cable(P, [[0, 0, 0], [5, -8, 0], [12, -20, -3], [20.3, -29.75, -5]], 0.5, 0xc9a227, [1.6, 1.3, 4.6], [1.6, 1.3, 4.0]));
    return { group: g };
  }

  function buildPcieCable(P) {
    const g = P.grp();
    g.add(cable(P, [[0, 0, 0], [3, -6, 0], [6, -12, -1], [8.5, -19.85, -2]], 0.5, 0x2f3540, [1.7, 1.2, 4.2], [1.7, 1.2, 4.0]));
    return { group: g };
  }

  function buildSataCable(P) {
    const g = P.grp();
    g.add(cable(P, [[0, 0, 0], [0.4, -2, 5], [-1.6, -1.25, 11.3]], 0.28, 0xb3302a, [1.2, 0.6, 2.0], [1.0, 0.6, 1.8]));
    return { group: g };
  }

  function buildFpanel(P) {
    const g = P.grp();
    g.add(P.rbox(1.5, 1.0, 1.0, 0.2, 0x0c0e13, { roughness: 0.6 }).at(0, 0, 0));
    const cols = [0xd33, 0xddd, 0x2a2, 0x111];
    for (let i = 0; i < 4; i++) {
      g.add(P.tube([[0, 0, 0], [2 + i, 1, 5 + i * 2], [5, 0, 10 + i * 2], [11.6, -9.25, 18 + i * 0.6]], 0.07, cols[i], { roughness: 0.7 }));
    }
    return { group: g };
  }

  function buildAio(P) {
    const g = P.grp();
    /* block (anchor on mobo), shifted in front of the board */
    g.add(P.rbox(5.6, 1.6, 5.6, 0.4, 0x161b24, { roughness: 0.35 }).at(2.8, 0.8, 0));
    const pump = P.cyl(2.2, 2.2, 0.5, 26, 0x39424f, { metalness: 0.7, roughness: 0.3 });
    pump.rotation.z = Math.PI / 2; pump.position.set(3.0, 0.95, 0); g.add(pump);
    const f1 = P.cyl(0.5, 0.5, 1.0, 14, 0x0c0e13, { roughness: 0.5 });
    f1.rotation.z = Math.PI / 2; f1.position.set(3.4, 1.3, 2.0); g.add(f1);
    const f2 = f1.clone(); f2.position.set(3.4, 1.3, -2.0); g.add(f2);
    /* tubes from block top to radiator (radiator bottom at world (0,42.3,0)) */
    g.add(P.tube([[3.2, 1.7, 2.0], [5, 8, 5.5], [9, 12, 3.5], [11.6, 10.7, 0.3]], 0.5, 0x0d0f14, { roughness: 0.4 }));
    g.add(P.tube([[3.2, 1.7, -2.0], [5, 8, -5.5], [9, 12, -3.5], [11.6, 10.7, -0.3]], 0.5, 0x0d0f14, { roughness: 0.4 }));
    return { group: g };
  }

  function buildAioRad(P) {
    const g = P.grp();
    g.add(P.rbox(28, 3.2, 12, 0.5, 0x39424f, { metalness: 0.8, roughness: 0.35 }).at(0, 0, 0));
    const f1 = fan(P, 11, 1.7, 0x232a35, 0x161b24);
    f1.group.rotation.z = Math.PI / 2; f1.group.position.set(-5.8, -2.6, 0);
    g.add(f1.group);
    const f2 = fan(P, 11, 1.7, 0x232a35, 0x161b24);
    f2.group.rotation.z = Math.PI / 2; f2.group.position.set(5.8, -2.6, 0);
    g.add(f2.group);
    return { group: g, spin: [f1.spin, f2.spin] };
  }

  function buildWifi(P) {
    const g = P.grp();
    g.add(P.rbox(1.9, 6.8, 6.4, 0.3, 0x1d2836, { roughness: 0.4 }).at(0, 0, 0));
    g.add(P.rbox(1.0, 6.8, 1.4, 0.2, 0x39424f, { metalness: 0.7, roughness: 0.3 }).at(0.9, 0, -2.4));
    for (const z of [-2, 2]) {
      const a = P.cyl(0.26, 0.26, 4.4, 12, 0x0c0e13, { roughness: 0.5 });
      a.position.set(0.4, 5.6, z); g.add(a);
      const tip = P.sphere(0.42, 0x39424f, { roughness: 0.4 }); tip.position.set(0.4, 7.9, z); g.add(tip);
    }
    return { group: g };
  }

  function buildCaseFan(P) {
    const g = P.grp();
    const f = fan(P, 11, 2.0, 0x232a35, 0x161b24);
    f.group.rotation.y = -Math.PI / 2; /* face +z */
    g.add(f.group);
    return { group: g, spin: [f.spin] };
  }
  function buildCaseFanRear(P) {
    const g = P.grp();
    const f = fan(P, 11, 2.0, 0x232a35, 0x161b24);
    f.group.rotation.y = Math.PI / 2; /* face -z */
    g.add(f.group);
    return { group: g, spin: [f.spin] };
  }

  /* ---- peripherals ---- */

  function buildMonitor(P) {
    const g = P.grp();
    g.add(P.rbox(24, 1.2, 14, 0.5, 0x232833, { roughness: 0.4 }).at(0, 0.6, 0));
    const neck = P.rbox(3.6, 13, 2.6, 0.3, 0x2b323d, { metalness: 0.5, roughness: 0.35 });
    neck.position.set(0, 7.6, 0); g.add(neck);
    const screenGeo = new THREE.BoxGeometry(2.4, 30, 50);
    const bezelMat = P.mat(0x0d1016, { roughness: 0.35 });
    const screen = new THREE.Mesh(screenGeo, [PC.Tex.screen.mat, bezelMat, bezelMat, bezelMat, bezelMat, bezelMat]);
    screen.position.set(0, 27.2, 0);
    g.add(screen);
    return { group: g, screen: screen };
  }

  function buildKeyboard(P) {
    const g = P.grp();
    const geo = new THREE.BoxGeometry(44, 1.6, 15);
    const side = P.mat(0x232833, { roughness: 0.5 });
    const kb = new THREE.Mesh(geo, [side, side, PC.Tex.keysMat, side, side, side]);
    g.add(kb);
    return { group: g };
  }

  function buildMouse(P) {
    const g = P.grp();
    const body = P.sphere(2.3, 0x232833, { roughness: 0.35 });
    body.scale.set(1.1, 0.72, 1.5);
    body.position.set(0, 0.9, 0); g.add(body);
    const wheel = P.cyl(0.65, 0.65, 0.5, 18, 0x39424f, { roughness: 0.4 });
    wheel.rotation.z = Math.PI / 2; wheel.position.set(0, 2.5, 1.6); g.add(wheel);
    const btn = P.box(1.5, 0.14, 2.2, 0x2b323d); btn.position.set(-0.9, 2.5, 1.4); g.add(btn);
    const btn2 = btn.clone(); btn2.position.set(0.9, 2.5, 1.4); g.add(btn2);
    return { group: g };
  }

  function buildSpeaker(P) {
    const g = P.grp();
    g.add(P.rbox(9, 18, 9, 0.6, 0x1d232d, { roughness: 0.5 }).at(0, 9, 0));
    const driver = P.cyl(3.1, 3.1, 1.2, 28, 0x0a0d12, { roughness: 0.85 });
    driver.rotation.x = Math.PI / 2; driver.position.set(0, 11, 4.6); g.add(driver);
    const cone = P.cyl(1.7, 1.1, 1.3, 24, 0x141922, { roughness: 0.8 });
    cone.rotation.x = Math.PI / 2; cone.position.set(0, 11, 5.1); g.add(cone);
    const tweeter = P.cyl(1.0, 1.0, 1.1, 20, 0x0a0d12, { roughness: 0.85 });
    tweeter.rotation.x = Math.PI / 2; tweeter.position.set(0, 15.5, 4.6); g.add(tweeter);
    return { group: g };
  }

  function buildWebcam(P) {
    const g = P.grp();
    g.add(P.rbox(4.6, 1.5, 2.6, 0.4, 0x1d232d, { roughness: 0.4 }).at(0, 0, 0));
    const lens = P.cyl(1.15, 1.15, 0.9, 20, 0x0a0d12, { roughness: 0.2 });
    lens.rotation.z = Math.PI / 2; lens.position.set(2.2, 0, 0); g.add(lens);
    const glass = P.cyl(0.7, 0.7, 1.0, 18, 0x1d4ed8, { roughness: 0.1, metalness: 0.3 });
    glass.rotation.z = Math.PI / 2; glass.position.set(2.6, 0, 0); g.add(glass);
    const led = P.sphere(0.22, 0xffffff, { emissive: 0xff3333, emissiveIntensity: 0.5, roughness: 0.3 });
    led.position.set(2.5, 0.4, 0.9); g.add(led);
    return { group: g, leds: [{ mat: led.material, color: 0xff3333, intensity: 1.6 }] };
  }

  function buildPaste(P) {
    const g = P.grp();
    g.add(P.rbox(3.4, 0.12, 3.4, 0.05, 0x9aa4b2, { metalness: 0.6, roughness: 0.3 }).at(0, 0, 0));
    return { group: g };
  }

  /* ============================ Tinkerer builders ============================ */

  function buildPcb(P) {
    const g = P.grp();
    /* board lying flat: plane XZ, top face (+y) gets the PCB texture */
    const geo = new THREE.BoxGeometry(44, 0.7, 36);
    const board = new THREE.Mesh(geo, [PC.Tex.pcbEdgeMat, PC.Tex.pcbEdgeMat, PC.Tex.pcbFaceMat, PC.Tex.pcbEdgeMat, PC.Tex.pcbEdgeMat, PC.Tex.pcbEdgeMat]);
    g.add(board);
    /* 24-pin power socket deco */
    g.add(P.rbox(2.2, 1.1, 5.6, 0.2, 0x0c0e13).at(21, 1.0, 5));
    /* debug LED (3 segments) */
    const segMat = P.mat(0x220000, { emissive: 0x000000, emissiveIntensity: 0, roughness: 0.3 });
    const segs = [];
    for (let i = 0; i < 3; i++) {
      const s = new THREE.Mesh(rboxGeo(1.2, 0.35, 0.6, 0.1), segMat.clone());
      s.position.set(10.5 + i * 1.6, 0.65, -15.5); g.add(s); segs.push(s);
    }
    /* power connector pads */
    for (let i = 0; i < 4; i++) g.add(P.box(0.5, 0.08, 0.5, 0xc9a45c, { metalness: 0.9, roughness: 0.25 }).at(-16, 0.4, -12 + i * 1.2));
    return { group: g, leds: segs.map(m => ({ mat: m.material, color: 0xff3b30, intensity: 2.2 })) };
  }

  function buildIos(P) {
    const g = P.grp();
    g.add(P.rbox(13, 3.4, 0.6, 0.2, 0x9aa4b2, { metalness: 0.8, roughness: 0.3 }).at(0, 1.7, 0));
    const ports = [
      [-5.2, 1.3, 0x1d4ed8, 1.3, 1.2], [-3.6, 1.3, 0x1d4ed8, 1.3, 1.2],
      [-1.6, 1.6, 0xb9c2cf, 2.0, 0.7], [0.6, 1.3, 0x0c0e13, 1.5, 1.3],
      [2.6, 1.3, 0x34d399, 1.0, 1.0], [4.0, 1.3, 0xec4899, 1.0, 1.0], [5.2, 1.3, 0x0c0e13, 1.0, 1.0]
    ];
    for (const [px, py, c, w, h] of ports) {
      g.add(P.box(w, h, 0.7, c, { roughness: 0.35 }).at(px, py, -0.35));
    }
    return { group: g };
  }

  function buildSocket(P) {
    const g = P.grp();
    g.add(P.rbox(9.6, 1.0, 9.6, 0.4, 0x0c0e13, { roughness: 0.5 }).at(0, 0.5, 0));
    const inner = P.rbox(8.0, 0.25, 8.0, 0.3, 0xc9a45c, { metalness: 0.85, roughness: 0.3 });
    inner.position.set(0, 0.28, 0); g.add(inner);
    const lever = P.rbox(9.0, 0.3, 0.7, 0.12, 0x9aa4b2, { metalness: 0.8, roughness: 0.3 });
    lever.position.set(0, 0.55, 4.8); g.add(lever);
    return { group: g };
  }

  function buildVrmMos(P) {
    const g = P.grp();
    for (let i = 0; i < 4; i++) {
      g.add(P.rbox(1.7, 0.6, 1.7, 0.15, 0x3a4454, { roughness: 0.4 }).at(-3.6 + i * 2.4, 0.3, 0));
      g.add(P.rbox(1.5, 0.12, 1.5, 0.1, 0x9aa4b2, { metalness: 0.7, roughness: 0.3 }).at(-3.6 + i * 2.4, 0.62, 0));
    }
    return { group: g };
  }

  function buildVrmChoke(P) {
    const g = P.grp();
    for (let i = 0; i < 4; i++) {
      g.add(P.rbox(2.0, 1.6, 2.0, 0.25, 0x454f61, { roughness: 0.4 }).at(-3.6 + i * 2.4, 0.8, 0));
      g.add(P.rbox(2.0, 0.3, 2.0, 0.15, 0x9aa4b2, { metalness: 0.8, roughness: 0.3 }).at(-3.6 + i * 2.4, 1.62, 0));
    }
    return { group: g };
  }

  function buildVrmCap(P) {
    const g = P.grp();
    for (let i = 0; i < 8; i++) {
      g.add(P.cyl(0.7, 0.7, 1.5, 18, 0x33415c, { roughness: 0.35 }).at(-7.7 + i * 2.2, 0.75, 0));
      g.add(P.cyl(0.62, 0.62, 0.12, 18, 0x9aa4b2, { metalness: 0.85, roughness: 0.25 }).at(-7.7 + i * 2.2, 1.52, 0));
    }
    return { group: g };
  }

  function buildDimm(P) {
    const g = P.grp();
    for (let i = 0; i < 4; i++) {
      const sx = -2.25 + i * 1.5;
      g.add(P.rbox(0.9, 0.8, 13.6, 0.15, 0x0b0e13, { roughness: 0.7 }).at(sx, 0.4, 0));
      g.add(P.box(0.4, 1.1, 1.0, 0x232833, { roughness: 0.5 }).at(sx, 0.9, -6.2));
      g.add(P.box(0.4, 1.1, 1.0, 0x232833, { roughness: 0.5 }).at(sx, 0.9, 6.2));
    }
    return { group: g };
  }

  function buildChipset(P) {
    const g = P.grp();
    g.add(P.rbox(5.8, 0.5, 5.8, 0.2, 0x11151d, { roughness: 0.45 }).at(0, 0.25, 0));
    g.add(P.rbox(6.6, 1.4, 6.6, 0.3, 0x4a5362, { metalness: 0.75, roughness: 0.35 }).at(0, 1.2, 0));
    for (let i = 0; i < 5; i++) {
      g.add(P.box(6.2, 0.18, 0.5, 0x39424f, { metalness: 0.7, roughness: 0.4 }).at(0, 1.55 + i * 0.24, 0));
    }
    return { group: g };
  }

  function buildBios(P) {
    const g = P.grp();
    g.add(P.rbox(1.7, 0.42, 1.2, 0.1, 0x0c0e13, { roughness: 0.5 }).at(0, 0.21, 0));
    for (const dx of [-0.55, 0.55]) for (const dz of [-0.32, 0.32]) {
      g.add(P.box(0.1, 0.16, 0.1, 0x9aa4b2, { metalness: 0.8, roughness: 0.3 }).at(dx, 0.06, dz));
    }
    const dot = P.cyl(0.3, 0.3, 0.06, 12, 0x39424f);
    dot.position.set(0, 0.46, 0); g.add(dot);
    return { group: g };
  }

  function buildCrystal(P) {
    const g = P.grp();
    g.add(P.rbox(2.4, 0.18, 1.5, 0.1, 0x9aa4b2, { metalness: 0.8, roughness: 0.3 }).at(0, 0.09, 0));
    g.add(P.cyl(1.05, 1.05, 0.8, 20, 0xd9dee6, { metalness: 0.9, roughness: 0.15 }).at(0, 0.55, 0));
    return { group: g };
  }

  function buildCmos(P) {
    const g = P.grp();
    g.add(P.cyl(2.1, 2.1, 0.3, 26, 0xb9c2cf, { metalness: 0.9, roughness: 0.2 }).at(0, 0.15, 0));
    const ring = P.torus(2.1, 0.16, 0x39424f, { metalness: 0.7, roughness: 0.4 });
    ring.rotation.x = Math.PI / 2; ring.position.set(0, 0.3, 0);
    g.add(ring);
    return { group: g };
  }

  function buildM2slot(P) {
    const g = P.grp();
    g.add(P.rbox(1.0, 0.4, 9.6, 0.12, 0x0b0e13, { roughness: 0.6 }).at(0, 0.2, 0));
    g.add(P.rbox(0.9, 0.1, 0.6, 0.05, 0xc9a45c, { metalness: 0.85, roughness: 0.3 }).at(0, 0.42, 4.6));
    const screw = P.cyl(0.25, 0.25, 0.5, 12, 0x8d97a5, { metalness: 0.8, roughness: 0.3 });
    screw.position.set(0, 0.65, -4.6); g.add(screw);
    return { group: g };
  }

  function buildNvme(P, tinker) {
    const g = P.grp();
    if (tinker) {
      g.add(P.rbox(2.2, 0.18, 8.0, 0.08, 0x1d2836, { roughness: 0.4 }).at(0, 0.1, 0));
      const chip = P.rbox(1.4, 0.24, 1.3, 0.08, 0x39424f, { metalness: 0.6, roughness: 0.3 });
      chip.position.set(-0.3, 0.32, -1.6); g.add(chip);
      const lbl = new THREE.Mesh(new THREE.BoxGeometry(2.0, 0.02, 3.4),
        new THREE.MeshStandardMaterial({ map: PC.Tex.label("NVMe", 256, 96, "#20262f", "#aeb8c6", 40), roughness: 0.5 }));
      lbl.position.set(0, 0.2, 1.6); g.add(lbl);
    } else {
      g.add(P.rbox(0.3, 0.3, 8.4, 0.1, 0x1d2836, { roughness: 0.4 }).at(0, 0.15, 0));
      const chip = P.rbox(0.45, 0.5, 1.4, 0.08, 0x39424f, { metalness: 0.6, roughness: 0.3 });
      chip.position.set(-0.15, 0.55, -1.8); g.add(chip);
    }
    return { group: g };
  }

  function buildSataPorts(P, tinker) {
    const g = P.grp();
    if (tinker) {
      g.add(P.rbox(2.6, 1.7, 3.0, 0.25, 0x11151d, { roughness: 0.5 }).at(0, 0.85, 0));
      for (let i = 0; i < 4; i++) {
        g.add(P.rbox(1.7, 0.8, 0.6, 0.15, 0x0c0e13, { roughness: 0.6 }).at(1.5, 0.75, -1.05 + i * 0.7));
      }
    } else {
      g.add(P.rbox(1.4, 1.5, 2.2, 0.2, 0x11151d, { roughness: 0.5 }).at(0, 0, 0));
      for (let i = 0; i < 4; i++) {
        g.add(P.rbox(1.1, 0.7, 0.5, 0.1, 0x0c0e13).at(0.9, -0.45 + i * 0.35, -0.3));
      }
    }
    return { group: g };
  }

  function buildHeaders(P) {
    const g = P.grp();
    g.add(P.rbox(2.6, 0.9, 1.7, 0.12, 0x0c1428, { roughness: 0.5 }).at(0, 0.45, 0));
    g.add(P.rbox(1.3, 0.5, 1.0, 0.1, 0x11151d).at(1.7, 0.25, -0.8));
    g.add(P.rbox(0.8, 0.5, 0.5, 0.1, 0x11151d).at(-1.2, 0.25, 1.3));
    g.add(P.rbox(1.5, 0.5, 1.0, 0.1, 0x11151d).at(0.4, 0.25, 1.3));
    for (let i = 0; i < 8; i++) {
      g.add(P.box(0.14, 0.6, 0.14, 0x9aa4b2, { metalness: 0.8, roughness: 0.3 }).at(-1.0 + i * 0.28, 0.75, 0.55));
    }
    return { group: g };
  }

  function buildAudioChip(P) {
    const g = P.grp();
    g.add(P.rbox(2.3, 0.45, 2.3, 0.12, 0x0c0e13, { roughness: 0.5 }).at(0, 0.23, 0));
    const lbl = new THREE.Mesh(new THREE.BoxGeometry(1.9, 0.02, 1.9),
      new THREE.MeshStandardMaterial({ map: PC.Tex.label("AUDIO", 128, 128, "#11151d", "#8b93a7", 34), roughness: 0.5 }));
    lbl.position.set(0, 0.47, 0); g.add(lbl);
    for (const [dx, dz] of [[-0.9, -0.9], [0.9, -0.9], [-0.9, 0.9], [0.9, 0.9]]) {
      g.add(P.box(0.12, 0.18, 0.12, 0x9aa4b2, { metalness: 0.8, roughness: 0.3 }).at(dx, 0.1, dz));
    }
    return { group: g };
  }

  function buildLanChip(P) {
    const g = P.grp();
    g.add(P.rbox(2.3, 0.45, 2.3, 0.12, 0x0c0e13, { roughness: 0.5 }).at(0, 0.23, 0));
    g.add(P.rbox(2.6, 1.0, 2.6, 0.15, 0x4a5362, { metalness: 0.75, roughness: 0.35 }).at(0, 1.0, 0));
    const lbl = new THREE.Mesh(new THREE.BoxGeometry(2.2, 0.02, 2.2),
      new THREE.MeshStandardMaterial({ map: PC.Tex.label("LAN", 128, 128, "#11151d", "#8b93a7", 40), roughness: 0.5 }));
    lbl.position.set(0, 0.47, 0); g.add(lbl);
    return { group: g };
  }

  function buildPcie(P) {
    const g = P.grp();
    g.add(P.rbox(1.2, 0.6, 14.6, 0.15, 0x0b0e13, { roughness: 0.6 }).at(0, 0.3, 0));
    g.add(P.rbox(0.5, 0.9, 1.5, 0.1, 0x232833).at(0, 0.75, 6.8));
    for (const sx of [-4.5, 4.5]) {
      g.add(P.rbox(1.2, 0.6, 3.6, 0.15, 0x0b0e13, { roughness: 0.6 }).at(sx, 0.3, 4.9));
      g.add(P.rbox(0.5, 0.9, 1.0, 0.1, 0x232833).at(sx, 0.75, 6.5));
    }
    return { group: g };
  }

  /* ============================ Registry ============================ */
  const DEFS = {

    case: {
      id: "case", label: "Case", emoji: "🧰", cat: "core", modes: ["e", "h", "c"],
      requires: [], build: buildCase,
      slots: [{ parent: "world", pos: [0, 0, 0], explodeDir: [0, 1, 0], factor: 0.25 }],
      focus: [0, 24, 0]
    },
    panel: {
      id: "panel", label: "Side Panel", emoji: "🪟", cat: "core", modes: ["e", "h", "c"],
      requires: ["case"], build: buildPanel,
      slots: [{ parent: "case", pos: [12.5, 24, 0], explodeDir: [1, 0, 0], factor: 1 }],
      focus: [12.5, 24, 0]
    },
    psu: {
      id: "psu", label: "Power Supply", emoji: "🔌", cat: "core", modes: ["e", "h", "c"],
      requires: ["case"], build: buildPsu,
      slots: [{ parent: "case", pos: [0, 4.3, -13], explodeDir: [1, 0, 0], factor: 1 }],
      focus: [0, 4.3, -13]
    },
    mobo: {
      id: "mobo", label: "Motherboard", emoji: "🧩", cat: "core", modes: ["e", "h", "c"],
      requires: ["case"], build: buildMobo,
      slots: [{ parent: "case", pos: TOWER.mobo, explodeDir: [1, 0, 0], factor: 1 }],
      focus: moboW(0, 0, 0)
    },
    cpu: {
      id: "cpu", label: "CPU", emoji: "🧠", cat: "core", modes: ["e", "h", "c", "t"],
      requires: m => m === "t" ? ["socket"] : ["mobo"],
      build: (P, m) => m === "t" ? buildCpu(P, 1.55) : buildCpu(P),
      slots: m => m === "t"
        ? [{ parent: "socket", pos: [0, 0.85, 0], explodeDir: [0, 1, 0], factor: 1.5 }]
        : [{ parent: "mobo", pos: [0.6, 8.5, 0], explodeDir: [1, 0, 0], factor: 1 }],
      focus: m => m === "t" ? boardW(0, 2, -8) : moboW(0.6, 8.5, 0)
    },
    paste: {
      id: "paste", label: "Thermal Paste", emoji: "🫧", cat: "core", modes: ["h", "c"],
      requires: ["cpu"], build: buildPaste,
      slots: [{ parent: "mobo", pos: [0.87, 8.5, 0], explodeDir: [1, 0, 0], factor: 1 }],
      focus: moboW(0.87, 8.5, 0)
    },
    cooler: {
      id: "cooler", label: "CPU Cooler", emoji: "🌬️", cat: "core", modes: ["e", "h"],
      requires: ["cpu"], build: buildCooler,
      slots: [{ parent: "mobo", pos: [0.86, 8.5, 0], explodeDir: [1, 0, 0], factor: 1 }],
      focus: moboW(3, 10, 0)
    },
    ram0: {
      id: "ram0", label: "RAM Stick 1", emoji: "📏", base: "ram", cat: "core", modes: ["e", "h", "c", "t"],
      requires: m => m === "t" ? ["dimm"] : ["mobo"],
      build: (P, m) => m === "t" ? buildRam(P, false, 1.0, "y") : buildRam(P, true, 1.0, "x"),
      slots: m => m === "t"
        ? [{ parent: "dimm", pos: [-0.75, 0.8, 0], explodeDir: [0, 1, 0], factor: 1.9 }]
        : [{ parent: "mobo", pos: [0.2, 8.3, -4.5], explodeDir: [1, 0, 0], factor: 1 }],
      focus: m => m === "t" ? boardW(7.2, 3, -8) : moboW(2, 10, -4.5)
    },
    ram1: {
      id: "ram1", label: "RAM Stick 2", emoji: "📏", base: "ram", cat: "core", modes: ["h", "c", "t"],
      requires: m => m === "t" ? ["dimm"] : ["mobo"],
      build: (P, m) => m === "t" ? buildRam(P, false, 1.0, "y") : buildRam(P, true, 1.0, "x"),
      slots: m => m === "t"
        ? [{ parent: "dimm", pos: [0.75, 0.8, 0], explodeDir: [0, 1, 0], factor: 1.9 }]
        : [{ parent: "mobo", pos: [0.2, 8.3, 1.5], explodeDir: [1, 0, 0], factor: 1 }],
      focus: m => m === "t" ? boardW(8.8, 3, -8) : moboW(2, 10, 1.5)
    },
    storage: {
      id: "storage", label: "Storage Drive", emoji: "💾", cat: "core", modes: ["e"],
      requires: ["case"], build: P => buildDrive(P, "storage"),
      slots: [{ parent: "case", pos: [-5.2, 12, 14.3], explodeDir: [1, 0, 0], factor: 1 }],
      focus: [-5.2, 12, 14.3]
    },
    ssd: {
      id: "ssd", label: "SSD", emoji: "💾", cat: "core", modes: ["h", "c"],
      requires: ["case"], build: P => buildDrive(P, "ssd"),
      slots: [{ parent: "case", pos: [-5.2, 8.5, 14.3], explodeDir: [1, 0, 0], factor: 1 }],
      focus: [-5.2, 8.5, 14.3]
    },
    hdd: {
      id: "hdd", label: "Hard Drive (HDD)", emoji: "📀", cat: "core", modes: ["h", "c"],
      requires: ["case"], build: P => buildDrive(P, "hdd"),
      slots: [{ parent: "case", pos: [-5.2, 16, 14.3], explodeDir: [1, 0, 0], factor: 1 }],
      focus: [-5.2, 16, 14.3]
    },
    gpu: {
      id: "gpu", label: "Graphics Card", emoji: "🎮", cat: "core", modes: ["e", "h", "c"],
      requires: ["mobo"], build: buildGpu,
      slots: [{ parent: "mobo", pos: [2.6, -6.8, 0], explodeDir: [1, 0, 0], factor: 1 }],
      focus: moboW(4, -3, 0)
    },
    cables: {
      id: "cables", label: "Power Cables", emoji: "🔗", cat: "cable", modes: ["h"],
      requires: ["psu", "mobo"], build: buildCablesH,
      slots: [{ parent: "mobo", pos: [12.0, -9.5, 0], explodeDir: [1, 0, 0], factor: 0.9 }],
      focus: moboW(10, -7, 2)
    },
    cables24: {
      id: "cables24", label: "24-pin ATX Cable", emoji: "🔗", cat: "cable", modes: ["c"],
      requires: ["psu", "mobo"], build: buildCables24,
      slots: [{ parent: "mobo", pos: [12.0, -9.5, 0], explodeDir: [1, 0, 0], factor: 0.9 }],
      focus: moboW(10, -7, 2)
    },
    cables8: {
      id: "cables8", label: "8-pin CPU Cable", emoji: "🔗", cat: "cable", modes: ["c"],
      requires: ["psu", "mobo"], build: buildCables8,
      slots: [{ parent: "mobo", pos: [-7.2, 15.1, 0], explodeDir: [1, 0, 0], factor: 0.9 }],
      focus: moboW(-7.2, 15.1, 0)
    },
    pciecable: {
      id: "pciecable", label: "PCIe Power Cable", emoji: "🔗", cat: "cable", modes: ["c"],
      requires: ["psu", "gpu"], build: buildPcieCable,
      slots: [{ parent: "mobo", pos: [4.6, 5.2, 0], explodeDir: [1, 0, 0], factor: 0.9 }],
      focus: moboW(4.6, 5.2, 0)
    },
    sata: {
      id: "sata", label: "SATA Cable", emoji: "🔌", cat: "cable", modes: ["c", "t"],
      requires: m => m === "t" ? ["pcb"] : ["mobo", "ssd"],
      build: (P, m) => m === "t" ? buildSataPorts(P, true) : buildSataCable(P),
      slots: m => m === "t"
        ? [{ parent: "pcb", pos: [14, 0.75, 4], explodeDir: [0, 1, 0], factor: 1.6 }]
        : [{ parent: "mobo", pos: [8, -13.5, 3], explodeDir: [1, 0, 0], factor: 0.9 }],
      focus: m => m === "t" ? boardW(14, 2, 4) : moboW(8, -13.5, 3)
    },
    aio: {
      id: "aio", label: "Liquid Cooler", emoji: "💧", cat: "core", modes: ["c"],
      requires: ["cpu"], build: buildAio,
      slots: [
        { parent: "mobo", pos: [0.86, 8.5, 0], explodeDir: [1, 0, 0], factor: 1 },
        { parent: "case", pos: [0, 43.9, 0], explodeDir: [0, 1, 0], factor: 0.6, buildRad: true }
      ],
      focus: moboW(0.86, 8.5, 0)
    },
    wifi: {
      id: "wifi", label: "Wi-Fi Card", emoji: "📡", cat: "core", modes: ["c"],
      requires: ["mobo"], build: buildWifi,
      slots: [{ parent: "mobo", pos: [-6.5, -6.5, 0], explodeDir: [1, 0, 0], factor: 1 }],
      focus: moboW(-6.5, -6.5, 0)
    },
    fans: {
      id: "fans", label: "Case Fans", emoji: "🌀", cat: "core", modes: ["c"],
      requires: ["case"], build: buildCaseFan,
      slots: [
        { parent: "case", pos: [0, 10, 21.4], explodeDir: [0, 0, 1], factor: 0.7 },
        { parent: "case", pos: [0, 32, 21.4], explodeDir: [0, 0, 1], factor: 0.7 },
        { parent: "case", pos: [0, 38, -21.6], explodeDir: [0, 0, -1], factor: 0.7, rear: true }
      ],
      focus: [0, 10, 21.4]
    },
    fpanel: {
      id: "fpanel", label: "Front Panel Wires", emoji: "🧵", cat: "cable", modes: ["c"],
      requires: ["mobo", "case"], build: buildFpanel,
      slots: [{ parent: "mobo", pos: [3.5, -14.5, 3.5], explodeDir: [1, 0, 0], factor: 0.9 }],
      focus: moboW(3.5, -14.5, 3.5)
    },
    nvme: {
      id: "nvme", label: "M.2 NVMe SSD", emoji: "💾", cat: "core", modes: ["c", "t"],
      requires: m => m === "t" ? ["m2slot"] : ["mobo"],
      build: (P, m) => buildNvme(P, m === "t"),
      slots: m => m === "t"
        ? [{ parent: "m2slot", pos: [0, 0.4, -0.8], explodeDir: [0, 1, 0], factor: 2.0 }]
        : [{ parent: "mobo", pos: [-5, -2.5, 0], explodeDir: [1, 0, 0], factor: 1 }],
      focus: m => m === "t" ? boardW(-13, 1.5, -4.8) : moboW(-5, -2.5, 0)
    },
    monitor: {
      id: "monitor", label: "Monitor", emoji: "🖥️", cat: "peripheral", modes: ["e", "h", "c"],
      requires: [], build: buildMonitor,
      slots: [{ parent: "world", pos: [34, 0, 8], explodeDir: [0, 1, 0], factor: 0.5 }],
      focus: [34, 27, 8]
    },
    keyboard: {
      id: "keyboard", label: "Keyboard", emoji: "⌨️", cat: "peripheral", modes: ["c"],
      requires: [], build: buildKeyboard,
      slots: [{ parent: "world", pos: [2, 0, -16], explodeDir: [0, 1, 0], factor: 0.45 }],
      focus: [2, 3, -16]
    },
    mouse: {
      id: "mouse", label: "Mouse", emoji: "🖱️", cat: "peripheral", modes: ["c"],
      requires: [], build: buildMouse,
      slots: [{ parent: "world", pos: [24, 0, -14], explodeDir: [0, 1, 0], factor: 0.45 }],
      focus: [24, 3, -14]
    },
    speakers: {
      id: "speakers", label: "Speakers", emoji: "🔊", cat: "peripheral", modes: ["c"],
      requires: [], build: buildSpeaker,
      slots: [
        { parent: "world", pos: [10, 0, 17], explodeDir: [0, 1, 0], factor: 0.4 },
        { parent: "world", pos: [56, 0, 17], explodeDir: [0, 1, 0], factor: 0.4 }
      ],
      focus: [10, 9, 17]
    },
    webcam: {
      id: "webcam", label: "Webcam", emoji: "📷", cat: "peripheral", modes: ["c"],
      requires: ["monitor"], build: buildWebcam,
      slots: [{ parent: "monitor", pos: [0, 42.4, 0], explodeDir: [0, 1, 0], factor: 0.6 }],
      focus: [34, 42.4, 8]
    },

    /* ---- tinkerer ---- */
    pcb: {
      id: "pcb", label: "PCB", emoji: "🟩", cat: "board", modes: ["t"],
      requires: [], build: buildPcb,
      slots: [{ parent: "world", pos: TINK.pcb, explodeDir: [0, 1, 0], factor: 0.25 }],
      focus: boardW(0, 0, 0)
    },
    ios: {
      id: "ios", label: "I/O Shield", emoji: "🚪", cat: "board", modes: ["t"],
      requires: ["pcb"], build: buildIos,
      slots: [{ parent: "pcb", pos: [0, 0.75, -16.8], explodeDir: [0, 1, 0], factor: 1.0 }],
      focus: boardW(0, 3, -16.8)
    },
    socket: {
      id: "socket", label: "CPU Socket", emoji: "🕳️", cat: "board", modes: ["t"],
      requires: ["pcb"], build: buildSocket,
      slots: [{ parent: "pcb", pos: [0, 0.75, -8], explodeDir: [0, 1, 0], factor: 1.2 }],
      focus: boardW(0, 1.5, -8)
    },
    "vrm-mos": {
      id: "vrm-mos", label: "VRM MOSFETs", emoji: "🎛️", base: "vrm-mos", cat: "board", modes: ["t"],
      requires: ["pcb"], build: buildVrmMos,
      slots: [{ parent: "pcb", pos: [-10, 0.75, -12.8], explodeDir: [0, 1, 0], factor: 1.8 }],
      focus: boardW(-10, 1.5, -12.8)
    },
    "vrm-choke": {
      id: "vrm-choke", label: "VRM Chokes", emoji: "🧲", base: "vrm-choke", cat: "board", modes: ["t"],
      requires: ["pcb"], build: buildVrmChoke,
      slots: [{ parent: "pcb", pos: [-10, 0.75, -10.8], explodeDir: [0, 1, 0], factor: 1.8 }],
      focus: boardW(-10, 1.5, -10.8)
    },
    "vrm-cap": {
      id: "vrm-cap", label: "VRM Capacitors", emoji: "🔋", base: "vrm-cap", cat: "board", modes: ["t"],
      requires: ["pcb"], build: buildVrmCap,
      slots: [{ parent: "pcb", pos: [-10, 0.75, -9.2], explodeDir: [0, 1, 0], factor: 1.8 }],
      focus: boardW(-10, 1.5, -9.2)
    },
    dimm: {
      id: "dimm", label: "DIMM Slots", emoji: "🎚️", cat: "board", modes: ["t"],
      requires: ["pcb"], build: buildDimm,
      slots: [{ parent: "pcb", pos: [8, 0.75, -8], explodeDir: [0, 1, 0], factor: 1.4 }],
      focus: boardW(8, 1, -8)
    },
    chipset: {
      id: "chipset", label: "Chipset", emoji: "🛣️", cat: "board", modes: ["t"],
      requires: ["pcb"], build: buildChipset,
      slots: [{ parent: "pcb", pos: [5, 0.75, 6], explodeDir: [0, 1, 0], factor: 2.2 }],
      focus: boardW(5, 2, 6)
    },
    bios: {
      id: "bios", label: "BIOS Chip", emoji: "💾", cat: "board", modes: ["t"],
      requires: ["pcb"], build: buildBios,
      slots: [{ parent: "pcb", pos: [10.5, 0.75, 3.5], explodeDir: [0, 1, 0], factor: 3.0 }],
      focus: boardW(10.5, 1.5, 3.5)
    },
    crystal: {
      id: "crystal", label: "Crystal Oscillator", emoji: "💎", cat: "board", modes: ["t"],
      requires: ["pcb"], build: buildCrystal,
      slots: [{ parent: "pcb", pos: [3, 0.75, 1.8], explodeDir: [0, 1, 0], factor: 2.8 }],
      focus: boardW(3, 1.5, 1.8)
    },
    cmos: {
      id: "cmos", label: "CMOS Battery", emoji: "🪙", cat: "board", modes: ["t"],
      requires: ["pcb"], build: buildCmos,
      slots: [{ parent: "pcb", pos: [15.5, 0.75, -14.5], explodeDir: [0, 1, 0], factor: 2.8 }],
      focus: boardW(15.5, 1, -14.5)
    },
    m2slot: {
      id: "m2slot", label: "M.2 Slot", emoji: "🎚️", cat: "board", modes: ["t"],
      requires: ["pcb"], build: buildM2slot,
      slots: [{ parent: "pcb", pos: [-13, 0.75, -4], explodeDir: [0, 1, 0], factor: 1.4 }],
      focus: boardW(-13, 1, -4)
    },
    headers: {
      id: "headers", label: "Headers", emoji: "📌", cat: "board", modes: ["t"],
      requires: ["pcb"], build: buildHeaders,
      slots: [{ parent: "pcb", pos: [-14, 0.75, 10], explodeDir: [0, 1, 0], factor: 2.0 }],
      focus: boardW(-14, 1.5, 10)
    },
    audio: {
      id: "audio", label: "Audio Codec", emoji: "🎵", cat: "board", modes: ["t"],
      requires: ["pcb"], build: buildAudioChip,
      slots: [{ parent: "pcb", pos: [-15, 0.75, 2], explodeDir: [0, 1, 0], factor: 2.4 }],
      focus: boardW(-15, 1, 2)
    },
    lan: {
      id: "lan", label: "LAN Controller", emoji: "🌐", cat: "board", modes: ["t"],
      requires: ["pcb"], build: buildLanChip,
      slots: [{ parent: "pcb", pos: [-14, 0.75, 14], explodeDir: [0, 1, 0], factor: 2.4 }],
      focus: boardW(-14, 1.5, 14)
    },
    pcie: {
      id: "pcie", label: "PCIe Slots", emoji: "🎚️", cat: "board", modes: ["t"],
      requires: ["pcb"], build: buildPcie,
      slots: [{ parent: "pcb", pos: [0, 0.75, 8], explodeDir: [0, 1, 0], factor: 1.2 }],
      focus: boardW(0, 1, 8)
    }
  };

  /* aio radiator + rear fan need distinct builds per anchor — main uses these */
  DEFS.aio.anchorBuild = (P, idx) => idx === 1 ? buildAioRad(P) : null;
  DEFS.fans.anchorBuild = (P, idx) => idx === 2 ? buildCaseFanRear(P) : null;

  return {
    DEFS,
    fan, rboxGeo, makeP,
    moboWorld: moboW,
    boardWorld: boardW
  };
})();
