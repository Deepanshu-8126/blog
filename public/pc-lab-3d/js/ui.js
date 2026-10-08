/* ============================================================
   PC Lab 3D — UI layer (DOM wiring, tray, info panel, labels,
   toasts, modals)
   ============================================================ */
window.PC = window.PC || {};

PC.UI = (function () {
  const $ = id => document.getElementById(id);
  let cb = {};
  const labels = new Map(); /* id -> {el, dot} */
  let currentAction = "build";

  const els = {
    modeTabs: $("mode-tabs"),
    actionTabs: $("action-tabs"),
    tray: $("tray"),
    hint: $("hint"),
    guided: $("guided"),
    progressNum: $("progress-num"),
    progressFill: $("progress-fill"),
    power: $("btn-power"),
    undo: $("btn-undo"),
    reset: $("btn-reset"),
    labelsBtn: $("btn-labels"),
    xrayBtn: $("btn-xray"),
    explode: $("explode"),
    status: $("status"),
    infoEmpty: $("info-empty"),
    infoCard: $("info-card"),
    modalRoot: $("modal-root"),
    loading: $("loading"),
    sceneError: $("scene-error"),
    labelsLayer: $("labels-layer"),
    toasts: null
  };

  function toastRoot() {
    if (!els.toasts) {
      els.toasts = document.createElement("div");
      els.toasts.id = "toasts";
      document.body.appendChild(els.toasts);
    }
    return els.toasts;
  }

  function init(callbacks) {
    cb = callbacks || {};
    /* mode tabs */
    for (const id of PC.MODE_ORDER) {
      const m = PC.MODES[id];
      const b = document.createElement("button");
      b.dataset.mode = id;
      b.innerHTML = `<span>${m.emoji}</span><span>${m.name}</span>`;
      b.title = m.tagline;
      b.addEventListener("click", () => cb.onMode && cb.onMode(id));
      els.modeTabs.appendChild(b);
    }
    /* action tabs */
    els.actionTabs.querySelectorAll("button").forEach(b => {
      b.addEventListener("click", () => cb.onAction && cb.onAction(b.dataset.action));
    });
    els.guided.addEventListener("change", () => cb.onGuided && cb.onGuided(els.guided.checked));
    els.power.addEventListener("click", () => cb.onPower && cb.onPower());
    $("btn-help").addEventListener("click", () => cb.onHelp && cb.onHelp());
    els.undo.addEventListener("click", () => cb.onUndo && cb.onUndo());
    els.reset.addEventListener("click", () => cb.onReset && cb.onReset());
    els.labelsBtn.addEventListener("click", () => cb.onLabels && cb.onLabels());
    els.xrayBtn.addEventListener("click", () => cb.onXray && cb.onXray());
    els.explode.addEventListener("input", () => cb.onExplode && cb.onExplode(parseInt(els.explode.value, 10)));
  }

  /* ---------- modes & actions ---------- */
  function setMode(modeId) {
    const m = PC.MODES[modeId];
    document.documentElement.style.setProperty("--accent", m.color);
    document.documentElement.style.setProperty("--accent-dim", m.color + "26");
    els.modeTabs.querySelectorAll("button").forEach(b => {
      b.classList.toggle("active", b.dataset.mode === modeId);
    });
  }
  function setAction(action) {
    currentAction = action;
    els.actionTabs.querySelectorAll("button").forEach(b => {
      b.classList.toggle("active", b.dataset.action === action);
    });
  }
  function getAction() { return currentAction; }

  /* ---------- tray ---------- */
  function renderTray(modeId, seq, statusMap, nextId) {
    els.tray.innerHTML = "";
    /* flat build-order checklist: matches the guided flow, one card per step */
    seq.forEach((id, idx) => {
      const def = PC.Parts.DEFS[id];
      const info = PC.contentFor(def, modeId);
      const card = document.createElement("button");
      card.className = "tray-card";
      card.dataset.part = id;
      const done = statusMap.get(id) === "in";
      if (done) card.classList.add("done");
      if (nextId === id) card.classList.add("next");
      card.innerHTML = `<span class="tray-num">${idx + 1}</span>
        <span class="tray-emoji">${def.emoji}</span>
        <span class="tray-name">${info.name}</span>
        <span class="tray-status ${done ? "in" : ""}"></span>`;
      card.addEventListener("click", () => cb.onTrayClick && cb.onTrayClick(id));
      els.tray.appendChild(card);
    });
  }

  function setHint(text, kind) {
    if (!text) { els.hint.classList.remove("show"); return; }
    els.hint.textContent = text;
    els.hint.className = "show " + (kind || "");
    els.hint.classList.add("show");
  }

  function updateProgress(done, total) {
    els.progressNum.textContent = done + " / " + total;
    els.progressFill.style.width = (total ? (done / total) * 100 : 0) + "%";
  }

  function setPower(on) {
    els.power.classList.toggle("on", on);
    els.power.textContent = on ? "⏻ Power Off" : "⏻ Power On";
  }
  function setPowerEnabled(en) { els.power.disabled = !en; }
  function setUndo(en) { els.undo.disabled = !en; }
  function setToggle(id, on) { els[id === "labels" ? "labelsBtn" : "xrayBtn"].classList.toggle("on", on); }
  function status(text) { els.status.textContent = text || ""; }

  /* ---------- info panel ---------- */
  function showInfo(partId, modeId) {
    const def = PC.Parts.DEFS[partId];
    const info = PC.contentFor(def, modeId);
    const m = PC.MODES[modeId];
    els.infoEmpty.hidden = true;
    els.infoCard.hidden = false;
    $("info-emoji").textContent = def.emoji;
    $("info-name").textContent = def.label;
    $("info-mode-line").textContent = m.emoji + " " + m.name + " · " + info.name;
    $("info-one").textContent = info.one;
    $("info-detail").textContent = info.detail;
    $("info-fun-text").textContent = info.fun;
    const specs = $("info-specs");
    specs.innerHTML = "";
    if (info.specs) info.specs.forEach(s => {
      const sp = document.createElement("span");
      sp.textContent = s;
      specs.appendChild(sp);
    });
    els.infoCard.scrollTop = 0;
  }
  function hideInfo() {
    els.infoEmpty.hidden = false;
    els.infoCard.hidden = true;
  }

  /* ---------- labels ---------- */
  function labelAdd(id, text) {
    if (labels.has(id)) return;
    const wrap = document.createElement("div");
    const chip = document.createElement("div");
    chip.className = "label-chip";
    chip.textContent = text;
    const dot = document.createElement("div");
    dot.className = "label-dot";
    wrap.appendChild(chip); wrap.appendChild(dot);
    wrap.style.display = "none";
    els.labelsLayer.appendChild(wrap);
    labels.set(id, { el: wrap, chip, dot, pos: null });
  }
  function labelRemove(id) {
    const l = labels.get(id);
    if (l) { l.el.remove(); labels.delete(id); }
  }
  function labelSetPos(id, worldPos, visible) {
    const l = labels.get(id);
    if (!l) return;
    l.pos = worldPos;
    l.visible = visible;
  }
  function labelSetSelected(id) {
    labels.forEach((l, key) => l.chip.classList.toggle("sel", key === id));
  }
  function labelClear() { labels.forEach(l => l.el.remove()); labels.clear(); }
  function labelUpdate() {
    const out = { x: 0, y: 0, visible: false };
    labels.forEach(l => {
      if (!l.pos || !l.visible) { l.el.style.display = "none"; return; }
      PC.Core.project(l.pos, out);
      if (!out.visible) { l.el.style.display = "none"; return; }
      l.el.style.display = "block";
      l.el.style.left = out.x + "px";
      l.el.style.top = out.y + "px";
    });
  }

  /* ---------- toasts ---------- */
  function toast(msg, kind) {
    const t = document.createElement("div");
    t.className = "toast " + (kind || "");
    t.textContent = msg;
    toastRoot().appendChild(t);
    setTimeout(() => t.remove(), 3000);
  }

  /* ---------- modals ---------- */
  function modal(html) {
    els.modalRoot.innerHTML =
      `<div class="modal-backdrop"><div class="modal">${html}</div></div>`;
    els.modalRoot.querySelector(".modal-backdrop").addEventListener("click", e => {
      if (e.target.classList.contains("modal-backdrop")) closeModal();
    });
    els.modalRoot.querySelectorAll("[data-close]").forEach(b =>
      b.addEventListener("click", closeModal));
  }
  function closeModal() { els.modalRoot.innerHTML = ""; }

  /* ---------- loading / error ---------- */
  function setLoading(hide) { els.loading.classList.toggle("hide", !!hide); }
  function showError() { els.sceneError.hidden = false; els.loading.classList.add("hide"); }

  return {
    init, setMode, setAction, getAction,
    renderTray, setHint, updateProgress,
    setPower, setPowerEnabled, setUndo, setToggle, status,
    showInfo, hideInfo,
    labelAdd, labelRemove, labelSetPos, labelSetSelected, labelClear, labelUpdate,
    toast, modal, closeModal,
    setLoading, showError
  };
})();

/* content lookup with fallback chain t → c → h → e */
PC.contentFor = function (def, modeId) {
  const id = def.base || def.id;
  const c = PC.CONTENT[id] || {};
  const chain = modeId === "t" ? ["t", "c", "h", "e"] : modeId === "c" ? ["c", "h", "e"] : modeId === "h" ? ["h", "e"] : ["e"];
  for (const k of chain) if (c[k]) return c[k];
  return { name: def.label, one: "A component of the computer.", detail: "Click around to learn about the other parts.", fun: "Every part has a job — together they make a working computer!" };
};
