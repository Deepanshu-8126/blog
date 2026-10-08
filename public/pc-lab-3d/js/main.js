/* ============================================================
   PC Lab 3D — application logic (state, assembly, tweens,
   power-on effects, boot screen, persistence)
   ============================================================ */
window.PC = window.PC || {};

(function () {
  if (!window.THREE) {
    window.addEventListener("DOMContentLoaded", () => {
      const err = document.getElementById("scene-error");
      if (err) err.hidden = false;
      const load = document.getElementById("loading");
      if (load) load.classList.add("hide");
    });
    return;
  }

  const App = {
    mode: "e",
    action: "build",
    powered: false,
    insts: [],            /* instances for current mode */
    assembled: new Set(),
    history: [],
    tweens: [],
    explodeAmt: 0,
    xray: false,
    labelsOn: true,
    guided: true,
    selected: null,
    hovered: null,
    boot: { running: false, line: 0, t: 0 },
    debugT: 0,
    seq: [],
    saved: null
  };

  /* ---- debug beacon (enabled via ?debug=1) ---- */
  const DEBUG = /[?&]debug=1/.test(location.search);
  let dbgEl = null;
  function dbg(msg) {
    if (!DEBUG) return;
    if (!dbgEl) {
      dbgEl = document.createElement("div");
      dbgEl.style.cssText = "position:fixed;left:8px;top:8px;z-index:9999;background:#000c;color:#0f0;font:28px monospace;padding:8px 12px;white-space:pre;pointer-events:none;max-width:96vw";
      document.body.appendChild(dbgEl);
    }
    dbgEl.textContent = msg;
  }
  window.addEventListener("error", e => {
    dbg("ERR: " + (e.message || e.type) + " @ " + (e.filename || "") + ":" + (e.lineno || ""));
  });

  const tmpV = new THREE.Vector3();

  /* ---------- persistence ---------- */
  function loadSaved() {
    try {
      App.saved = JSON.parse(localStorage.getItem("pclab3d.v1") || "{}");
    } catch (e) { App.saved = {}; }
    if (!App.saved.progress) App.saved.progress = {};
    if (App.saved.tutorialSeen === undefined) App.saved.tutorialSeen = false;
  }
  function saveProgress() {
    App.saved.progress[App.mode] = [...App.assembled];
    try { localStorage.setItem("pclab3d.v1", JSON.stringify(App.saved)); } catch (e) { /* ignore */ }
  }

  /* ---------- scene building ---------- */
  function parentWorldOf(partId) {
    const p = instOf(partId);
    if (!p) return tmpV.set(0, 0, 0);
    return p.anchors[0].obj.getWorldPosition(tmpV);
  }
  function instOf(id) {
    for (const i of App.insts) if (i.id === id) return i;
    return null;
  }

  function makeInstances(mode) {
    const seq = PC.MODES[mode].seq;
    App.seq = seq;
    App.insts = [];
    for (const id of seq) {
      const def = PC.Parts.DEFS[id];
      const P = PC.Parts.makeP();
      const res = def.build(P, mode);
      const slots = typeof def.slots === "function" ? def.slots(mode) : def.slots;
      const anchors = [];
      for (let i = 0; i < slots.length; i++) {
        let obj, spin = [], leds = [];
        if (i === 0) {
          obj = res.group; spin = res.spin || []; leds = res.leds || [];
        } else if (def.anchorBuild) {
          const alt = def.anchorBuild(P, i);
          if (alt) { obj = alt.group; spin = alt.spin || []; leds = alt.leds || []; }
          else { const r2 = def.build(P, mode); obj = r2.group; spin = r2.spin || []; leds = r2.leds || []; }
        } else {
          const r2 = def.build(P, mode);
          obj = r2.group; spin = r2.spin || []; leds = r2.leds || [];
        }
        obj.traverse(o => {
          if (o.isMesh) {
            o.userData.partId = id;
            o.userData.anchorIdx = i;
            o.castShadow = true;
            o.receiveShadow = true;
          }
        });
        anchors.push({ obj, slot: slots[i], spin, leds, state: "out", prog: 0 });
      }
      App.insts.push({
        id, def, anchors,
        focus: typeof def.focus === "function" ? def.focus(mode) : def.focus,
        labelText: PC.contentFor(def, mode).name,
        mats: collectMats(anchors),
        screen: res.screen || null
      });
      /* mark materials that are already transparent so X-ray skips them */
      const inst = App.insts[App.insts.length - 1];
      inst.mats.forEach(m => { if (m.transparent) m._skipXray = true; });
    }
  }

  function collectMats(anchors) {
    const set = new Set();
    anchors.forEach(a => a.obj.traverse(o => {
      if (o.isMesh && o.material) {
        /* multi-material meshes pass an array — expand it */
        if (Array.isArray(o.material)) o.material.forEach(m => set.add(m));
        else set.add(o.material);
      }
    }));
    return set;
  }

  function buildScene(mode) {
    const root = new THREE.Group();
    for (const inst of App.insts) {
      inst.anchors.forEach(a => { /* not added until assembled */ });
    }
    PC.Core.setModeGroup(root);
  }

  /* ---------- tweening ---------- */
  function addTween(anchor, fromWorld, toWorld, dur, onDone, outHide) {
    App.tweens.push({
      a: anchor,
      from: fromWorld.clone(),
      to: toWorld.clone(),
      t: 0, dur,
      done: onDone || null,
      outHide: !!outHide
    });
  }
  function updateTweens(dt) {
    for (let i = App.tweens.length - 1; i >= 0; i--) {
      const tw = App.tweens[i];
      tw.t += dt;
      const k = Math.min(1, tw.t / tw.dur);
      const e = 1 - Math.pow(1 - k, 3); /* easeOutCubic */
      tw.a.obj.position.lerpVectors(tw.from, tw.to, e);
      if (k >= 1) {
        App.tweens.splice(i, 1);
        if (tw.done) tw.done();
      }
    }
  }
  function cancelTweens() { App.tweens = []; }

  function entryPoint() {
    const e = PC.MODES[App.mode].entry;
    return new THREE.Vector3(
      e[0] + (Math.random() - 0.5) * 60,
      e[1] + (Math.random() - 0.5) * 40,
      e[2] + (Math.random() - 0.5) * 60
    );
  }

  /* ---------- assemble / disassemble ---------- */
  function assemble(id) {
    const inst = instOf(id);
    if (!inst) return;
    if (App.assembled.has(id)) return;
    const reqs = typeof inst.def.requires === "function" ? inst.def.requires(App.mode) : inst.def.requires;
    for (const r of reqs) {
      if (!App.assembled.has(r)) {
        const rdef = PC.Parts.DEFS[r];
        const rname = PC.contentFor(rdef, App.mode).name;
        PC.UI.toast("Install the " + rname + " first!", "err");
        PC.UI.setHint("⚠️ The " + rname + " needs to be installed first.", "err");
        return;
      }
    }
    let remaining = inst.anchors.length;
    inst.anchors.forEach(a => {
      const from = entryPoint();
      const pWorld = a.slot.parent === "world" ? tmpV.set(0, 0, 0) : parentWorldOf(a.slot.parent);
      const to = new THREE.Vector3(pWorld.x + a.slot.pos[0], pWorld.y + a.slot.pos[1], pWorld.z + a.slot.pos[2]);
      a.state = "moving";
      a.obj.position.copy(from);
      a.obj.quaternion.identity();
      PC.Core.getRoot().add(a.obj);
      applyXrayTo(inst);
      addTween(a, from, to, 0.95, () => {
        const pObj = a.slot.parent === "world" ? null : instOf(a.slot.parent).anchors[0].obj;
        PC.Core.getRoot().remove(a.obj);
        (pObj || PC.Core.getRoot()).add(a.obj);
        a.obj.position.set(a.slot.pos[0], a.slot.pos[1], a.slot.pos[2]);
        a.state = "in";
        if (--remaining === 0) finishAssemble(inst);
      });
    });
  }

  function finishAssemble(inst) {
    App.assembled.add(inst.id);
    App.history.push(inst.id);
    applyExplode(inst);
    if (App.labelsOn) PC.UI.labelAdd(inst.id, inst.labelText);
    saveProgress();
    refreshUI();
    PC.UI.setHint("✅ " + inst.labelText + " installed!", "ok");
    selectPart(inst.id, true);
    if (App.assembled.size === App.seq.length) {
      PC.UI.setHint("🎉 Everything is installed! Press ⏻ Power On to boot the system!", "ok");
    }
  }

  function disassemble(id, instant) {
    const inst = instOf(id);
    if (!inst || !App.assembled.has(inst.id)) return;
    if (App.powered) powerOff();
    App.assembled.delete(inst.id);
    App.history = App.history.filter(h => h !== id);
    PC.UI.labelRemove(inst.id);
    if (inst.id === App.selected) { App.selected = null; PC.UI.hideInfo(); PC.UI.labelSetSelected(null); }
    saveProgress();
    let remaining = inst.anchors.length;
    inst.anchors.forEach(a => {
      const to = entryPoint();
      if (instant) {
        a.obj.parent && a.obj.parent.remove(a.obj);
        a.state = "out";
        if (--remaining === 0) { refreshUI(); }
        return;
      }
      const from = a.obj.getWorldPosition(new THREE.Vector3());
      a.obj.parent && a.obj.parent.remove(a.obj);
      PC.Core.getRoot().add(a.obj);
      a.state = "moving";
      addTween(a, from, to, 0.7, () => {
        PC.Core.getRoot().remove(a.obj);
        a.state = "out";
        if (--remaining === 0) refreshUI();
      });
    });
    if (instant) refreshUI();
  }

  function resetMode() {
    cancelTweens();
    if (App.powered) powerOff();
    const ids = [...App.assembled];
    ids.forEach(id => disassemble(id, true));
    App.history = [];
    App.selected = null;
    PC.UI.hideInfo();
    PC.UI.labelSetSelected(null);
    PC.UI.setHint(App.guided && App.seq.length ? "Start building! Click the highlighted part in the tray." : "", "");
    PC.UI.toast("Level reset — start fresh!", "");
    refreshUI();
  }

  /* ---------- explode / xray ---------- */
  function applyExplode(inst) {
    inst.anchors.forEach(a => {
      if (a.state !== "in") return;
      const off = App.explodeAmt * a.slot.factor;
      a.obj.position.set(
        a.slot.pos[0] + a.slot.explodeDir[0] * off,
        a.slot.pos[1] + a.slot.explodeDir[1] * off,
        a.slot.pos[2] + a.slot.explodeDir[2] * off
      );
    });
  }
  function applyExplodeAll() {
    App.insts.forEach(applyExplode);
  }
  function applyXrayTo(inst) {
    inst.mats.forEach(m => {
      if (m._skipXray) return;
      m.transparent = App.xray;
      m.opacity = App.xray ? 0.3 : 1;
      m.depthWrite = !App.xray;
      m.needsUpdate = true;
    });
  }
  function applyXrayAll() {
    App.insts.forEach(i => {
      if (App.assembled.has(i.id)) applyXrayTo(i);
    });
  }

  /* ---------- selection & highlight ---------- */
  function highlight(inst, on, strong) {
    if (App.powered && !strong) return;
    const accent = new THREE.Color(PC.MODES[App.mode].color);
    inst.mats.forEach(m => {
      if (m._skipXray) return;
      if (on) { m.emissive.copy(accent); m.emissiveIntensity = strong ? 0.55 : 0.22; }
      else { m.emissive.setRGB(0, 0, 0); m.emissiveIntensity = 0; }
    });
  }
  function selectPart(id, showInfo) {
    if (App.selected) {
      const prev = instOf(App.selected);
      if (prev) highlight(prev, false);
    }
    App.selected = id;
    const inst = instOf(id);
    if (inst) {
      highlight(inst, true, true);
      PC.UI.labelSetSelected(id);
      if (showInfo) PC.UI.showInfo(id, App.mode);
      if (App.action === "explore") {
        const f = inst.focus;
        PC.Core.ctrl.focusOn(new THREE.Vector3(f[0], f[1], f[2]));
      }
    }
  }
  function clearHover() {
    if (App.hovered) {
      const inst = instOf(App.hovered);
      if (inst && App.hovered !== App.selected) highlight(inst, false);
      App.hovered = null;
    }
  }
  function setHover(id) {
    if (id === App.hovered) return;
    clearHover();
    if (id && id !== App.selected) {
      App.hovered = id;
      const inst = instOf(id);
      if (inst) highlight(inst, true, false);
    }
  }

  /* ---------- power ---------- */
  function canPower() { return App.assembled.size === App.seq.length; }
  function powerOn() {
    App.powered = true;
    PC.UI.setPower(true);
    PC.UI.status("System running");
    App.boot = { running: true, line: 0, t: 0 };
    drawBoot(true);
    App.insts.forEach(inst => {
      if (!App.assembled.has(inst.id)) return;
      inst.anchors.forEach(a => {
        a.leds.forEach(l => {
          l.mat.emissive.set(l.color);
          l.mat.emissiveIntensity = l.intensity;
        });
      });
    });
    PC.UI.toast("System powered on! 🎉", "ok");
  }
  function powerOff() {
    App.powered = false;
    PC.UI.setPower(false);
    PC.UI.status("");
    App.boot.running = false;
    drawBoot(false);
    App.insts.forEach(inst => {
      inst.anchors.forEach(a => {
        a.leds.forEach(l => {
          l.mat.emissive.setRGB(0, 0, 0);
          l.mat.emissiveIntensity = 0;
        });
      });
    });
  }

  function drawBoot(on) {
    const { canvas, ctx, texture } = PC.Tex.screen;
    ctx.fillStyle = "#02040a";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    if (!on) { texture.needsUpdate = true; return; }
    const lines = PC.MODES[App.mode].boot;
    ctx.fillStyle = "#cfe3ff";
    ctx.font = "600 17px 'Segoe UI', Arial, sans-serif";
    ctx.fillText("PC LAB 3D — SYSTEM CONSOLE", 30, 42);
    ctx.strokeStyle = "rgba(255,255,255,0.15)";
    ctx.beginPath(); ctx.moveTo(30, 58); ctx.lineTo(canvas.width - 30, 58); ctx.stroke();
    ctx.font = "15px 'Consolas', 'Courier New', monospace";
    const n = Math.min(App.boot.line + 1, lines.length);
    for (let i = 0; i < n; i++) {
      ctx.fillStyle = i === n - 1 && n < lines.length ? "#8be9fd" : "#7ce3a7";
      ctx.fillText(lines[i], 34, 90 + i * 30);
    }
    if (n >= lines.length) {
      ctx.fillStyle = "#7ce3a7";
      ctx.font = "700 20px 'Segoe UI', Arial, sans-serif";
      ctx.fillText("✔ SYSTEM READY", 34, 90 + lines.length * 30 + 14);
    }
    texture.needsUpdate = true;
  }

  /* ---------- UI refresh ---------- */
  function refreshUI() {
    const total = App.seq.length;
    const done = App.assembled.size;
    PC.UI.updateProgress(done, total);
    PC.UI.setPowerEnabled(canPower());
    PC.UI.setUndo(App.history.length > 0);
    let next = null;
    if (App.guided && done < total) {
      for (const id of App.seq) if (!App.assembled.has(id)) { next = id; break; }
    }
    const statusMap = new Map();
    App.insts.forEach(i => statusMap.set(i.id, App.assembled.has(i.id) ? "in" : "out"));
    PC.UI.renderTray(App.mode, App.seq, statusMap, next);
    if (App.guided && next) {
      const def = PC.Parts.DEFS[next];
      PC.UI.setHint("👉 Next step: " + PC.contentFor(def, App.mode).name + " — click it in the tray.", "");
    } else if (done === total) {
      PC.UI.setHint("🎉 Everything is installed! Press ⏻ Power On to boot the system!", "ok");
    } else {
      PC.UI.setHint("", "");
    }
  }

  /* ---------- mode switching ---------- */
  function switchMode(modeId) {
    cancelTweens();
    clearHover();
    if (App.powered) powerOff();
    App.mode = modeId;
    App.assembled.clear();
    App.history = [];
    App.selected = null;
    App.hovered = null;
    PC.UI.labelClear();
    PC.UI.hideInfo();
    App.explodeAmt = 0;
    document.getElementById("explode").value = 0;
    const m = PC.MODES[modeId];
    PC.Core.setAccent(m.color);
    PC.Core.setInterior(modeId);
    makeInstances(modeId);
    buildScene(modeId);
    /* restore saved progress for this mode */
    const savedSet = (App.saved.progress || {})[modeId] || [];
    savedSet.forEach(id => {
      const inst = instOf(id);
      if (!inst) return;
      inst.anchors.forEach(a => {
        const pObj = a.slot.parent === "world" ? null : instOf(a.slot.parent) && instOf(a.slot.parent).anchors[0].obj;
        (pObj || PC.Core.getRoot()).add(a.obj);
        a.obj.position.set(a.slot.pos[0], a.slot.pos[1], a.slot.pos[2]);
        a.state = "in";
      });
      App.assembled.add(id);
      if (App.labelsOn) PC.UI.labelAdd(id, inst.labelText);
    });
    /* camera */
    const pos = new THREE.Vector3(m.cam.pos[0], m.cam.pos[1], m.cam.pos[2]);
    const tgt = new THREE.Vector3(m.cam.tgt[0], m.cam.tgt[1], m.cam.tgt[2]);
    PC.Core.ctrl.set(pos, tgt);
    if (PC.Core.ctrl.sph) PC.Core.ctrl.sph.radius = PC.Core.ctrl.sph.radius * 1.9;
    PC.UI.setMode(modeId);
    PC.UI.setPower(false);
    PC.UI.status("");
    refreshUI();
    PC.UI.setHint(App.guided ? "Start building! Click the highlighted part in the tray." : "", "");
  }

  /* ---------- events ---------- */
  function onCanvasClick(e) {
    if (!PC.Core.isClickEvent()) return;
    const data = PC.Core.pick(e.clientX, e.clientY);
    const id = data ? data.partId : null;
    if (!id) {
      /* deselect on empty space */
      if (App.selected) {
        const prev = instOf(App.selected);
        if (prev) highlight(prev, false);
        App.selected = null;
        PC.UI.labelSetSelected(null);
        PC.UI.hideInfo();
      }
      return;
    }
    const inst = instOf(id);
    if (!inst) return;
    const assembled = App.assembled.has(id);
    if (App.action === "disassemble") {
      if (assembled) {
        disassemble(id);
        PC.UI.toast("Removed: " + inst.labelText, "");
      } else {
        PC.UI.toast("That part isn't installed yet.", "err");
      }
      return;
    }
    selectPart(id, true);
    if (App.action === "build" && !assembled) assemble(id);
  }

  function onTrayClick(id) {
    const inst = instOf(id);
    if (!inst) return;
    const assembled = App.assembled.has(id);
    if (App.action === "build") {
      if (assembled) { selectPart(id, true); }
      else { assemble(id); }
    } else if (App.action === "disassemble") {
      if (assembled) { disassemble(id); PC.UI.toast("Removed: " + inst.labelText, ""); }
      else { PC.UI.toast("That part isn't installed yet.", "err"); }
    } else {
      selectPart(id, true);
    }
  }

  /* ---------- modals ---------- */
  function showTutorial() {
    PC.UI.modal(`
      <h2>👋 Welcome to PC Lab 3D!</h2>
      <p>Build, take apart and explore a computer — right in your browser.</p>
      <ul>
        <li><b>🔧 Build</b> — click parts in the tray to install them.</li>
        <li><b>🧹 Disassemble</b> — click installed parts to remove them.</li>
        <li><b>🔍 Explore</b> — click any part to read about it.</li>
      </ul>
      <p>🖱️ <b>Drag</b> to rotate · <b>scroll</b> to zoom · <b>right-drag</b> to pan</p>
      <p>Choose a level: each one adds more parts and deeper explanations.</p>
      <div class="modal-actions">
        <button class="btn-primary" data-close>Start building! 🚀</button>
      </div>`);
  }
  function showHelp() {
    const modes = PC.MODE_ORDER.map(id => {
      const m = PC.MODES[id];
      return `<div class="mode-row"><span class="em">${m.emoji}</span><div><b>${m.name}</b><br>${m.tagline}</div></div>`;
    }).join("");
    PC.UI.modal(`
      <h2>❓ Help & Controls</h2>
      <p><kbd>Drag</kbd> rotate &nbsp; <kbd>Scroll</kbd> zoom &nbsp; <kbd>Right-drag</kbd> pan &nbsp; <kbd>Click part</kbd> select/learn</p>
      <h3 style="font-size:12px;text-transform:uppercase;letter-spacing:1px;color:var(--accent);margin:14px 0 8px">Difficulty levels</h3>
      ${modes}
      <p>💡 <b>Guided mode</b> highlights the next step. <b>Exploded view</b> spreads parts apart. <b>X-ray</b> sees through components.</p>
      <div class="modal-actions">
        <button class="btn-primary" data-close>Got it</button>
      </div>`);
  }

  /* ---------- update loop ---------- */
  function update(dt) {
    updateTweens(dt);
    App.insts.forEach(inst => {
      if (!App.assembled.has(inst.id)) return;
      if (App.powered) {
        inst.anchors.forEach(a => a.spin.forEach(s => {
          s.obj.rotation[s.axis] += s.speed * dt;
        }));
      }
    });
    /* boot screen */
    if (App.boot.running) {
      App.boot.t += dt;
      const total = PC.MODES[App.mode].boot.length;
      if (App.boot.line < total - 1 && App.boot.t > 0.72) {
        App.boot.t = 0;
        App.boot.line++;
        drawBoot(true);
      } else if (App.boot.line >= total - 1 && App.boot.t > 0.9) {
        drawBoot(true);
      }
    }
    /* tinkerer debug LED */
    if (App.powered && App.mode === "t") {
      App.debugT += dt;
      if (App.debugT > 0.35) {
        App.debugT = 0;
        const pcb = instOf("pcb");
        if (pcb) {
          const palette = [0xff3b30, 0xff9500, 0xffcc00, 0x34c759, 0x00c7be, 0x007aff, 0xaf52de];
          pcb.anchors[0].leds.forEach(l => {
            l.mat.emissive.set(palette[Math.floor(Math.random() * palette.length)]);
          });
        }
      }
    }
    /* labels */
    if (App.labelsOn) {
      App.insts.forEach(inst => {
        if (!App.assembled.has(inst.id)) return;
        const wp = inst.anchors[0].obj.getWorldPosition(tmpV);
        PC.UI.labelSetPos(inst.id, [wp.x, wp.y + 6.5, wp.z], true);
      });
      PC.UI.labelUpdate();
    }
    PC.Core.update(dt);
    PC.Core.render();
  }

  /* ---------- boot ---------- */
  function boot() {
    dbg("THREE=" + (window.THREE ? THREE.REVISION : "UNDEF") + " stage=main-js");
    try {
      PC.Core.init(document.getElementById("scene"), () => {
      dbg("THREE=" + (window.THREE ? THREE.REVISION : "UNDEF") + " stage=core-ready");
      PC.UI.setLoading(true);
      if (DEBUG) document.getElementById("loading").style.display = "none";
      loadSaved();
      PC.UI.init({
        onMode: switchMode,
        onAction: a => { App.action = a; PC.UI.setAction(a); },
        onTrayClick,
        onPower: () => { if (!canPower()) return; App.powered ? powerOff() : powerOn(); },
        onUndo: () => {
          if (!App.history.length) return;
          const id = App.history[App.history.length - 1];
          disassemble(id);
          PC.UI.toast("Undo: removed " + instOf(id).labelText, "");
        },
        onReset: resetMode,
        onLabels: () => {
          App.labelsOn = !App.labelsOn;
          PC.UI.setToggle("labels", App.labelsOn);
          if (App.labelsOn) {
            App.insts.forEach(i => { if (App.assembled.has(i.id)) PC.UI.labelAdd(i.id, i.labelText); });
          } else {
            PC.UI.labelClear();
          }
        },
        onXray: () => {
          App.xray = !App.xray;
          PC.UI.setToggle("xray", App.xray);
          applyXrayAll();
        },
        onExplode: v => {
          App.explodeAmt = (v / 100) * PC.MODES[App.mode].explodeScale;
          applyExplodeAll();
        },
        onGuided: g => { App.guided = g; refreshUI(); },
        onHelp: showHelp
      });
      const modeParam = /[?&]mode=([a-z])/.exec(location.search);
      let ASM_LOG = "";
      switchMode(modeParam ? modeParam[1] : "e");
      if (/[?&]view=(very)?close/.test(location.search)) {
        const m = PC.MODES[App.mode];
        const veryClose = /[?&]view=veryclose/.test(location.search);
        PC.Core.ctrl.sph.radius = App.mode === "t" ? (veryClose ? 44 : 62) : 78;
        PC.Core.ctrl.goalRadius = PC.Core.ctrl.sph.radius;
        PC.Core.ctrl.targetGoal.set(m.cam.tgt[0], m.cam.tgt[1], m.cam.tgt[2]);
      }
      if (/[?&]asm=all/.test(location.search)) {
        let growN = 0;
        [...App.seq].forEach(id => {
          const inst = instOf(id);
          let addN = 0;
          inst.anchors.forEach(a => {
            const pObj = a.slot.parent === "world" ? null : instOf(a.slot.parent) && instOf(a.slot.parent).anchors[0].obj;
            (pObj || PC.Core.getRoot()).add(a.obj);
            a.obj.position.set(a.slot.pos[0], a.slot.pos[1], a.slot.pos[2]);
            a.state = "in";
            let n = 0; a.obj.traverse(o => { if (o.isMesh) n++; }); addN += n;
          });
          growN += addN;
          ASM_LOG += id + "+" + addN + "=" + growN + " ";
          App.assembled.add(id);
          if (App.labelsOn) PC.UI.labelAdd(id, inst.labelText);
        });
        refreshUI();
        saveProgress();
        if (/[?&]power=1/.test(location.search)) powerOn();
      }
      dbg("THREE=" + (window.THREE ? THREE.REVISION : "UNDEF") + " stage=booted insts=" + App.insts.length + " asm=" + App.assembled.size);
      if (DEBUG) {
        let meshCount = 0, rootKids = 0;
        const root = PC.Core.getRoot();
        if (root) {
          rootKids = root.children.length;
          root.traverse(o => { if (o.isMesh) meshCount++; });
        }
        const inScene = App.insts.filter(i => i.anchors.length && i.anchors.every(a => a.obj.parent)).map(i => i.id).join(",");
        const seen = new Set();
        if (root) root.traverse(o => seen.add(o));
        const unreached = App.insts.filter(i => i.anchors.length && !seen.has(i.anchors[0].obj)).map(i => i.id).join("|");
        const childCount = c => { let n = 0; c.traverse(o => { if (o.isMesh) n++; }); return n; };
        const rootKidsInfo = root ? root.children.map(c => childCount(c)).join(",") : "-";
        const pcbInst = instOf("pcb");
        const pcbKids = pcbInst ? pcbInst.anchors[0].obj.children.map(c => childCount(c)).join(",") : "-";
        dbg("rootKids=" + rootKids + " children-mesh-counts=[" + rootKidsInfo + "]\npcb.children=[" + pcbKids + "] UNREACHED=[" + unreached + "]\nasm-log: " + ASM_LOG);
      }
      if (!App.saved.tutorialSeen && !DEBUG) {
        showTutorial();
        App.saved.tutorialSeen = true;
        try { localStorage.setItem("pclab3d.v1", JSON.stringify(App.saved)); } catch (e) { }
      }
      /* canvas events */
      const canvas = document.getElementById("scene");
      canvas.addEventListener("pointerdown", () => PC.Core.resetMoved());
      canvas.addEventListener("click", onCanvasClick);
      canvas.addEventListener("pointermove", e => {
        if (PC.Core.ctrl.pointers.size) return;
        const data = PC.Core.pick(e.clientX, e.clientY);
        setHover(data ? data.partId : null);
        canvas.style.cursor = data ? (App.action === "disassemble" ? "not-allowed" : "pointer") : "grab";
      });
      let last = performance.now();
      const loop = (now) => {
        const dt = Math.min(0.05, (now - last) / 1000);
        last = now;
        update(dt);
        requestAnimationFrame(loop);
      };
      requestAnimationFrame(loop);
    });
    } catch (e) {
      dbg("CORE-INIT-FAIL: " + (e && e.message ? e.message : e));
      PC.UI.showError();
    }
  }

  window.addEventListener("DOMContentLoaded", boot);
  PC.App = App;
})();
