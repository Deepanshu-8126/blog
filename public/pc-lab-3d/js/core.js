/* ============================================================
   PC Lab 3D — core 3D engine (renderer, camera, orbit controls,
   lights, environment, raycast, screen-space label projection)
   ============================================================ */
window.PC = window.PC || {};

PC.Core = (function () {
  const V = THREE.Vector3;

  let renderer, scene, camera, raycaster;
  let hemi, key, rim, ambient, accentLight, interiorLight;
  let container, canvas;
  let groupRoot = null;      /* per-mode scene content */
  let deskGroup = null;

  /* ---- custom orbit controls ---- */
  const ctrl = {
    target: new V(0, 24, 0),
    sph: null,             /* spherical around target */
    minDist: 30, maxDist: 320,
    minPolar: 0.15, maxPolar: Math.PI * 0.49,
    damping: 0.14,
    targetGoal: new V(0, 24, 0),
    enabled: true,
    pointers: new Map(),
    pinchDist: 0
  };
  ctrl.set = function (pos, tgt) {
    ctrl.targetGoal.copy(tgt);
    ctrl.target.copy(tgt);
    const off = new V().copy(pos).sub(tgt);
    ctrl.sph = new THREE.Spherical().setFromVector3(off);
    ctrl.goalRadius = ctrl.sph.radius;
  };
  ctrl.rotate = function (dx, dy) {
    if (!ctrl.sph) return;
    ctrl.sph.theta -= dx * 0.0055;
    ctrl.sph.phi -= dy * 0.0055;
    ctrl.sph.phi = Math.max(ctrl.minPolar, Math.min(ctrl.maxPolar, ctrl.sph.phi));
  };
  ctrl.zoom = function (f) {
    if (!ctrl.sph) return;
    ctrl.sph.radius = Math.max(ctrl.minDist, Math.min(ctrl.maxDist, ctrl.sph.radius * f));
    ctrl.goalRadius = ctrl.sph.radius;
  };
  ctrl.pan = function (dx, dy) {
    if (!ctrl.sph) return;
    const off = new V().setFromSpherical(ctrl.sph);
    const dist = off.length();
    const right = new V().crossVectors(off, new V(0, 1, 0)).normalize();
    const up = new V().crossVectors(right, off).normalize();
    const scale = dist * 0.0011;
    const move = right.multiplyScalar(-dx * scale).add(up.multiplyScalar(dy * scale));
    ctrl.target.add(move);
    ctrl.targetGoal.add(move);
  };
  ctrl.focusOn = function (pos, distKeep) {
    ctrl.targetGoal.copy(pos);
    if (distKeep) ctrl.sph.radius = distKeep;
  };
  ctrl.update = function (dt) {
    if (!ctrl.sph) return;
    ctrl.target.lerp(ctrl.targetGoal, Math.min(1, ctrl.damping * dt * 8));
    if (ctrl.goalRadius !== undefined) {
      ctrl.sph.radius += (ctrl.goalRadius - ctrl.sph.radius) * Math.min(1, dt * 1.7);
    }
    const off = new V().setFromSpherical(ctrl.sph);
    camera.position.copy(ctrl.target).add(off);
    camera.lookAt(ctrl.target);
  };

  function onPointerDown(e) {
    if (e.button === 2) ctrl.panning = true;
    else ctrl.pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
    canvas.setPointerCapture && canvas.setPointerCapture(e.pointerId);
  }
  function onPointerMove(e) {
    if (ctrl.pointers.has(e.pointerId)) {
      const p = ctrl.pointers.get(e.pointerId);
      const dx = e.clientX - p.x, dy = e.clientY - p.y;
      p.x = e.clientX; p.y = e.clientY;
      if (ctrl.pointers.size === 1) {
        ctrl.rotate(dx, dy);
        if (Math.abs(dx) > 3 || Math.abs(dy) > 3) moved = true;
      }
    }
    if (ctrl.pointers.size === 2) {
      const pts = [...ctrl.pointers.values()];
      const d = Math.hypot(pts[0].x - pts[1].x, pts[0].y - pts[1].y);
      if (ctrl.pinchDist > 0) ctrl.zoom(ctrl.pinchDist / d);
      ctrl.pinchDist = d;
    }
  }
  function onPointerUp(e) {
    ctrl.pointers.delete(e.pointerId);
    if (ctrl.pointers.size < 2) ctrl.pinchDist = 0;
    ctrl.panning = false;
  }
  function onWheel(e) {
    e.preventDefault();
    ctrl.zoom(e.deltaY > 0 ? 1.09 : 0.917);
  }
  function onContext(e) { e.preventDefault(); }

  let moved = false;
  function isClickEvent() { return !moved; }
  function resetMoved() { moved = false; }

  /* ---- init ---- */
  function init(canvasEl, onReady) {
    canvas = canvasEl;
    container = canvas.parentElement;
    renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.22;
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;

    scene = new THREE.Scene();
    scene.fog = new THREE.Fog(0x070a12, 260, 620);

    camera = new THREE.PerspectiveCamera(45, 1, 0.1, 2000);

    hemi = new THREE.HemisphereLight(0xa3b7e8, 0x1a1e28, 1.15);
    scene.add(hemi);
    ambient = new THREE.AmbientLight(0xffffff, 0.55);
    scene.add(ambient);
    key = new THREE.DirectionalLight(0xffffff, 2.3);
    key.position.set(70, 110, 50);
    key.castShadow = true;
    key.shadow.mapSize.set(2048, 2048);
    key.shadow.camera.left = -110; key.shadow.camera.right = 110;
    key.shadow.camera.top = 120; key.shadow.camera.bottom = -90;
    key.shadow.camera.near = 20; key.shadow.camera.far = 400;
    key.shadow.bias = -0.0004;
    key.shadow.normalBias = 0.02;
    scene.add(key);
    rim = new THREE.DirectionalLight(0x6f8cff, 1.0);
    rim.position.set(-60, 40, -80);
    scene.add(rim);
    accentLight = new THREE.PointLight(0x38bdf8, 60, 300, 1.8);
    accentLight.position.set(20, 40, 30);
    scene.add(accentLight);
    interiorLight = new THREE.PointLight(0x9fc4ff, 60, 120, 1.5);
    interiorLight.position.set(0, 24, 0);
    scene.add(interiorLight);

    raycaster = new THREE.Raycaster();
    raycaster.layers.enableAll();

    canvas.addEventListener("pointerdown", onPointerDown);
    canvas.addEventListener("pointermove", onPointerMove);
    canvas.addEventListener("pointerup", onPointerUp);
    canvas.addEventListener("pointercancel", onPointerUp);
    canvas.addEventListener("wheel", onWheel, { passive: false });
    canvas.addEventListener("contextmenu", onContext);

    buildEnvironment();
    resize();
    window.addEventListener("resize", resize);
    if (onReady) onReady();
  }

  function resize() {
    const w = container.clientWidth, h = container.clientHeight;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  }

  /* ---- desk + floor (shared environment) ---- */
  function buildEnvironment() {
    const P = {
      mat: (color, opts) => new THREE.MeshStandardMaterial(Object.assign({ color, roughness: 0.5, metalness: 0.2 }, opts || {})),
      rbox: (w, h, d, r, color, opts) => {
        const m = new THREE.Mesh(PC.Parts.rboxGeo(w, h, d, r), P.mat(color, opts));
        m.castShadow = true; m.receiveShadow = true; return m;
      },
      box: (w, h, d, color, opts) => {
        const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), P.mat(color, opts));
        m.castShadow = true; m.receiveShadow = true; return m;
      }
    };
    deskGroup = new THREE.Group();
    const top = P.rbox(104, 4, 72, 1.6, 0x54483a, { roughness: 0.5, metalness: 0.12 });
    top.position.set(8, -2, 0);
    deskGroup.add(top);
    const edge = P.rbox(105, 0.8, 73, 1.4, 0x6b5c49, { roughness: 0.45, metalness: 0.15 });
    edge.position.set(8, -2.6, 0);
    deskGroup.add(edge);
    for (const [dx, dz] of [[-40, -30], [56, -30], [-40, 30], [56, 30]]) {
      const leg = P.box(4, 66, 4, 0x241e18, { roughness: 0.6 });
      leg.position.set(8 + dx, -37, dz);
      deskGroup.add(leg);
    }
    /* floor */
    const fgeo = new THREE.CircleGeometry(420, 48);
    fgeo.rotateX(-Math.PI / 2);
    const fc = document.createElement("canvas");
    fc.width = fc.height = 512;
    const fx = fc.getContext("2d");
    const grad = fx.createRadialGradient(256, 256, 40, 256, 256, 256);
    grad.addColorStop(0, "#1a2030"); grad.addColorStop(0.6, "#10141f"); grad.addColorStop(1, "#070a12");
    fx.fillStyle = grad; fx.fillRect(0, 0, 512, 512);
    fx.strokeStyle = "rgba(120,150,255,0.05)";
    for (let i = -512; i <= 512; i += 32) {
      fx.beginPath(); fx.moveTo(i + 256, 0); fx.lineTo(i + 256, 512); fx.stroke();
      fx.beginPath(); fx.moveTo(0, i + 256); fx.lineTo(512, i + 256); fx.stroke();
    }
    const ftex = new THREE.CanvasTexture(fc);
    const floor = new THREE.Mesh(fgeo, new THREE.MeshStandardMaterial({ map: ftex, roughness: 0.95 }));
    floor.position.set(0, -70, 0);
    floor.receiveShadow = true;
    scene.add(floor);
    scene.add(deskGroup);
  }

  function setModeGroup(g) {
    if (groupRoot) {
      scene.remove(groupRoot);
      disposeGroup(groupRoot);
    }
    groupRoot = g;
    scene.add(g);
  }
  function getRoot() { return groupRoot; }

  function disposeGroup(g) {
    g.traverse(o => {
      if (o.geometry) o.geometry.dispose();
      if (o.material) {
        if (Array.isArray(o.material)) o.material.forEach(m => m.dispose());
        else o.material.dispose();
      }
    });
  }

  /* ---- raycast ---- */
  function pick(clientX, clientY) {
    const rect = canvas.getBoundingClientRect();
    const nx = ((clientX - rect.left) / rect.width) * 2 - 1;
    const ny = -((clientY - rect.top) / rect.height) * 2 + 1;
    raycaster.setFromCamera(new THREE.Vector2(nx, ny), camera);
    if (!groupRoot) return null;
    const hits = raycaster.intersectObjects(groupRoot.children, true);
    for (const h of hits) {
      let o = h.object;
      while (o) {
        if (o.userData && o.userData.partId) return o.userData;
        o = o.parent;
      }
    }
    return null;
  }

  /* ---- world → screen projection for labels ---- */
  const projV = new V();
  function project(worldPos, out) {
    projV.set(worldPos[0], worldPos[1], worldPos[2]).project(camera);
    const rect = canvas.getBoundingClientRect();
    out.x = (projV.x * 0.5 + 0.5) * rect.width;
    out.y = (-projV.y * 0.5 + 0.5) * rect.height;
    out.visible = projV.z < 1 && projV.z > -1;
  }

  function setAccent(hex) {
    if (!accentLight) return;
    accentLight.color.set(hex);
  }
  function setInterior(modeId) {
    if (!interiorLight) return;
    if (modeId === "t") interiorLight.position.set(0, 16, 0);
    else interiorLight.position.set(2, 26, 8);
  }

  function render() { renderer.render(scene, camera); }
  function update(dt) { ctrl.update(dt); }

  return {
    init, resize, render, update, pick, project, disposeGroup,
    setModeGroup, getRoot, setAccent, setInterior,
    ctrl, camera, scene,
    isClickEvent, resetMoved,
    onPointerDown: null
  };
})();
