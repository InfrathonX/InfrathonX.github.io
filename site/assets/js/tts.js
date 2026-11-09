/* Interactive long/short-horizon submission trajectories. */
(() => {
  "use strict";
  const X = window.IX, data = window.INFRATHON_TTS;
  if (!X || !data) return;
  const { h, s, st, fmt, showTip, hideTip } = X;
  const modes = [1, 2, 4];
  const color = { 1: "#F2545B", 2: "#78AD00", 4: "#2F80ED" };
  const dash = { 1: "7 3", 2: null, 4: "6 2 1.5 2" };
  const label = { 1: "T (1 run)", 2: "T/2 (best of 2)", 4: "T/4 (best of 4)" };

  document.querySelectorAll("[data-tts-viewer]").forEach((root) => {
    const state = { axis: "paper", visible: new Set(modes) };
    const charts = [], legendButtons = [];
    let views = [], modalPanel = null;
    const modalTitle = h("h3", { id: `${root.id}-dialog-title` });
    const modalMount = h("div", { class: "tts-chart tts-modal-chart" });
    const close = h("button", { type: "button", class: "figure-expand", text: "Close ×", "aria-label": "Close expanded trajectory" });
    const modal = h("dialog", { class: "tts-dialog", "aria-labelledby": modalTitle.id },
      h("div", { class: "tts-dialog-head" }, modalTitle, close));

    function legend() {
      return h("div", { class: "tts-legend", "aria-label": "Show or hide an allocation" }, modes.map((n) => {
        const icon = s("svg", { width: 25, height: 14, viewBox: "0 0 25 14", "aria-hidden": "true" });
        s("line", { x1: 0, x2: 25, y1: 7, y2: 7, stroke: color[n], "stroke-width": 2, "stroke-dasharray": dash[n] }, icon);
        const button = h("button", { type: "button", "data-allocation": n, "aria-pressed": "true", onclick: () => {
          if (state.visible.has(n)) state.visible.delete(n); else state.visible.add(n);
          for (const { button, allocation } of legendButtons) button.setAttribute("aria-pressed", String(state.visible.has(allocation)));
          for (const view of views) view.applyVisibility();
          hideTip();
        } }, icon, label[n]);
        legendButtons.push({ button, allocation: n });
        return button;
      }));
    }

    function chart(panel, mount, large = false) {
      const W = Math.max(280, mount.clientWidth || (large ? 900 : 380)), H = large ? 440 : 240;
      const left = large ? 76 : 62, right = W - 16, top = 16, bottom = H - 47;
      const svg = s("svg", { viewBox: `0 0 ${W} ${H}`, role: "img", "aria-label": `${panel.modelLabel}: ${panel.title}, one long run versus best-of-two and best-of-four short runs` });
      const warp = (time) => state.axis === "linear" || time <= panel.budget / 2 ? time : panel.budget / 2 + (time - panel.budget / 2) / 3;
      const x = (time) => left + warp(time) / warp(panel.budget) * (right - left);
      const [lo, hi] = panel.limits;
      const y = (value) => bottom - (value - lo) / (hi - lo) * (bottom - top);
      const ticks = X.niceTicks(lo, hi, 4).filter((tick) => tick >= lo && tick <= hi);
      s("rect", { x: x(panel.budget / 2), y: top, width: right - x(panel.budget / 2), height: bottom - top, fill: "#f2f5f8" }, svg);
      for (const value of ticks) {
        s("line", { x1: left, x2: right, y1: y(value), y2: y(value), stroke: "var(--hair)", "stroke-width": 1 }, svg);
        st(svg, left - 8, y(value) + 4, fmt(value, hi - lo < 5 ? 1 : 0), { "text-anchor": "end", "font-size": 12, fill: "var(--ink)" });
      }
      const times = state.axis === "paper" ? [0, panel.budget / 6, panel.budget / 3, panel.budget / 2, panel.budget] : [0, panel.budget / 4, panel.budget / 2, panel.budget * .75, panel.budget];
      for (const time of times) {
        s("line", { x1: x(time), x2: x(time), y1: top, y2: bottom, stroke: "var(--hair)", "stroke-width": 1 }, svg);
        st(svg, x(time), bottom + 19, String(time), { "text-anchor": "middle", "font-size": 12, fill: "var(--ink)" });
      }
      s("line", { x1: left, x2: right, y1: bottom, y2: bottom, stroke: "var(--hair-2)" }, svg);
      st(svg, (left + right) / 2, H - 6, "Time (hours)", { "text-anchor": "middle", "font-size": 12, fill: "var(--ink)", style: "font-family:var(--f-sans)" });
      st(svg, 14, (top + bottom) / 2, panel.unit, { "text-anchor": "middle", "font-size": 12, fill: "var(--ink)", transform: `rotate(-90 14 ${(top + bottom) / 2})`, style: "font-family:var(--f-sans)" });
      const clipId = `${root.id}-${panel.id}-${large ? "large" : "small"}`;
      const clip = s("clipPath", { id: clipId }, s("defs", {}, svg));
      s("rect", { x: left - 6, y: top - 6, width: right - left + 12, height: bottom - top + 12 }, clip);
      const layers = [];
      for (const group of panel.groups) {
        const n = group.n;
        const layer = s("g", { "data-allocation": n, "clip-path": `url(#${clipId})` }, svg);
        let path = `M${x(group.times[0])},${y(group.best[0])}`;
        for (let i = 1; i < group.times.length; i++) path += `H${x(group.times[i])}V${y(group.best[i])}`;
        s("path", { class: "tts-best", d: path, fill: "none", stroke: color[n], "stroke-width": large ? 2.3 : 1.8, "stroke-dasharray": dash[n], "stroke-linejoin": "round" }, layer);
        layers.push({ n, layer });
      }
      const applyVisibility = () => { for (const { n, layer } of layers) layer.style.display = state.visible.has(n) ? "" : "none"; };
      applyVisibility();
      const cursor = s("line", { x1: 0, x2: 0, y1: top, y2: bottom, stroke: "var(--hair-3)", "stroke-dasharray": "3 3", visibility: "hidden" }, svg);
      s("rect", { x: left, y: top, width: right - left, height: bottom - top, fill: "transparent" }, svg);
      svg.addEventListener("pointermove", (event) => {
        const bounds = svg.getBoundingClientRect(), position = (event.clientX - bounds.left) / bounds.width * W;
        if (position < left || position > right) { cursor.setAttribute("visibility", "hidden"); hideTip(); return; }
        const transformed = (position - left) / (right - left) * warp(panel.budget);
        const time = state.axis === "paper" && transformed > panel.budget / 2 ? panel.budget / 2 + 3 * (transformed - panel.budget / 2) : transformed;
        cursor.setAttribute("x1", position); cursor.setAttribute("x2", position); cursor.setAttribute("visibility", "visible");
        const rows = panel.groups.filter((group) => state.visible.has(group.n)).map((group) => {
          const elapsed = Math.min(time, group.hours);
          let value = null;
          for (let i = 0; i < group.times.length && group.times[i] <= elapsed + 1e-9; i++) value = group.best[i];
          return { color: color[group.n], value: value == null ? "—" : fmt(value, 2), label: label[group.n] + (time > group.hours ? " · final" : "") };
        });
        showTip(event.clientX, event.clientY, `${panel.modelLabel} · ${panel.title} · ${fmt(time, 2)} h`, rows, "Best score so far");
        const tip = document.getElementById("tip"), parent = modal.open ? modal : document.body;
        if (tip && tip.parentNode !== parent) parent.append(tip);
      });
      svg.addEventListener("pointerleave", () => { cursor.setAttribute("visibility", "hidden"); hideTip(); });
      mount.replaceChildren(svg);
      return { applyVisibility };
    }

    function redraw() {
      views = charts.map(({ panel, mount }) => chart(panel, mount));
      if (modal.open && modalPanel) views.push(chart(modalPanel, modalMount, true));
    }
    function expand(panel) {
      modalPanel = panel;
      modalTitle.textContent = `${panel.modelLabel} · ${panel.title}`;
      modal.showModal();
      redraw();
    }
    close.addEventListener("click", () => modal.close());
    modal.addEventListener("close", () => { modalPanel = null; hideTip(); const tip = document.getElementById("tip"); if (tip && modal.contains(tip)) document.body.append(tip); });
    modal.addEventListener("click", (event) => { if (event.target === modal) modal.close(); });
    modal.append(legend(), modalMount);
    root.replaceChildren();
    const axes = h("span", { class: "seg" });
    X.seg(axes, [["paper", "Paper axis"], ["linear", "Linear hours"]], state.axis, (axis) => { state.axis = axis; redraw(); });
    const axisControls = h("div", { class: "tts-axis" }, h("span", { text: "Time axis" }), axes);
    root.append(h("div", { class: "tts-setup-note" },
      h("p", {}, h("strong", { text: "T = 12 hours for operator tasks and 24 hours for module and system tasks." })),
      h("ul", {},
        h("li", {}, h("strong", { text: "T (1 run): " }), "one long-horizon run lasting T hours."),
        h("li", {}, h("strong", { text: "T/2 (best of 2): " }), "short-horizon TTS (test-time scaling) with 2 independent runs, each lasting T/2 hours; take the best score."),
        h("li", {}, h("strong", { text: "T/4 (best of 4): " }), "short-horizon TTS with 4 independent runs, each lasting T/4 hours; take the best score.")),
      h("p", {}, "All three settings use the ", h("strong", { text: "same total GPU-hour budget" }), ": 1 × T = 2 × (T/2) = 4 × (T/4).")));
    for (const model of ["gpt-6-astra", "claude-opus-5-5"]) {
      const panels = data.panels.filter((panel) => panel.model === model);
      const grid = h("div", { class: "tts-grid" });
      root.append(h("section", { class: "tts-model", "aria-label": panels[0].modelLabel },
        h("div", { class: "tts-model-head" }, h("h3", { text: panels[0].modelLabel }),
          h("div", { class: "tts-model-controls" }, model === "gpt-6-astra" ? axisControls : null, legend())), grid));
      for (const panel of panels) {
        const mount = h("div", { class: "tts-chart" });
        grid.append(h("article", { class: "tts-card", "data-panel": panel.id },
          h("div", { class: "tts-card-head" }, h("div", {}, h("h4", { text: panel.title }),
            h("p", { class: "tts-task-meta", "data-level": panel.level.toLowerCase(), text: `${panel.stage} / ${panel.level}` })),
          h("button", { class: "figure-expand", type: "button", text: "Expand ↗", "aria-label": `Expand ${panel.modelLabel}: ${panel.title}`, onclick: () => expand(panel) })),
          h("div", { class: "tts-card-body" }, mount)));
        charts.push({ panel, mount });
      }
    }
    root.append(modal);
    redraw();
    let previousWidth = root.clientWidth, pending = false;
    new ResizeObserver(() => {
      if (Math.abs(root.clientWidth - previousWidth) < 1 || pending) return;
      pending = true;
      requestAnimationFrame(() => { previousWidth = root.clientWidth; pending = false; redraw(); });
    }).observe(root);
  });
})();
