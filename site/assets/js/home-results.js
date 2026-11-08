(() => {
  "use strict";
  const X = window.IX;
  if (!X) return;
  const { D, MODELS, MODEL, COLOR, C, STAGES, LEVELS, s, h, $, fmt, withUnit, unitOf, cap } = X;

  /* ---------------- leaderboard ---------------- */
  const state = { stage: "all", level: "all" };
  const TK = D.tokens.models;
  function drawSegs() {
    X.seg($("#seg-stage"), [["all", "All", X.filterTasks(D.tasks, "all", state.level).length], ...STAGES.map((g) => [g, cap(g), X.filterTasks(D.tasks, g, state.level).length])], state.stage, (v) => { state.stage = v; drawSegs(); render(); });
    X.seg($("#seg-level"), [["all", "All"], ...LEVELS.map((l) => [l, cap(l), X.filterTasks(D.tasks, state.stage, l).length])], state.level, (v) => { state.level = v; drawSegs(); render(); });
  }
  function scoreBar(m, v, ci) {
    const svg = s("svg", { "aria-hidden": "true" });
    for (const g of [0, 25, 50, 75, 100]) s("line", { x1: `${g}%`, x2: `${g}%`, y1: 3, y2: 25, stroke: g === 0 ? C.hair2 : C.hair, "stroke-width": 1 }, svg);
    if (v > 0) {
      s("rect", { x: 0, y: 9, width: `${v}%`, height: 10, rx: 5, fill: COLOR[m] }, svg);
      s("rect", { x: 0, y: 9, width: `${Math.min(v, 3)}%`, height: 10, fill: COLOR[m] }, svg);
    }
    if (ci && ci.lo != null) {
      s("line", { x1: `${ci.lo}%`, x2: `${ci.hi}%`, y1: 14, y2: 14, stroke: C.ink, "stroke-width": 1.5 }, svg);
      for (const x of [ci.lo, ci.hi]) s("line", { x1: `${x}%`, x2: `${x}%`, y1: 9, y2: 19, stroke: C.ink, "stroke-width": 1.5 }, svg);
    }
    return svg;
  }
  function render() {
    const ts = X.filterTasks(D.tasks, state.stage, state.level);
    const rows = X.standings(ts);
    const tb = $("#lb tbody");
    tb.replaceChildren();
    rows.forEach((r) => {
      const pos = 1 + rows.filter((o) => (o.score ?? -1) > (r.score ?? -1)).length;
      const fullSuite = ts.length === D.tasks.length;
      const first = ts.map((t) => t.results[r.m]?.first_valid_h).filter((v) => v != null).sort((a, b) => a - b);
      const mid = (first.length - 1) / 2;
      const firstMedian = first.length ? (first[Math.floor(mid)] + first[Math.ceil(mid)]) / 2 : null;
      const tokenK = ts.reduce((sum, t) => sum + D.tokens.per_task[t.key][r.m].visible_output_k, 0);
      const tokens = fullSuite ? `${fmt(TK[r.m].visible_output_m, 2)}M` : tokenK >= 1000 ? `≈${fmt(tokenK / 1000, 2)}M` : `≈${fmt(tokenK, 0)}k`;
      tb.append(h("tr", { "data-model": r.m },
        h("td", { class: "rk", text: r.score == null ? "–" : String(pos) }),
        h("td", {}, h("div", { class: "model" }, h("span", { class: "badge" }, X.swatch(r.m, 14)), h("div", {}, h("b", { text: MODEL[r.m].name }), h("small", { text: `${X.PROVIDER[r.m]} · ${X.effortNote(r.m)}` })))),
        h("td", {}, h("div", { class: "score" }, r.score == null ? "—" : fmt(r.score, 1), h("small", { text: r.ci.lo == null ? "" : `${fmt(r.ci.lo, 1)}–${fmt(r.ci.hi, 1)}` }))),
        h("td", { class: "barcell" }, scoreBar(r.m, r.score ?? 0, r.ci)),
        h("td", { class: "n" }, `${r.wins}`, h("small", { text: `of ${r.cov}` })),
        h("td", { class: "n first-time" }, firstMedian == null ? "—" : `${fmt(firstMedian, 2)} h`, h("small", { text: `median · ${first.length} runs` })),
        h("td", { class: "n visible-tokens", title: `Visible output tokens across ${ts.length} runs.${fullSuite ? "" : " Filtered totals are approximate."}` }, tokens, h("small", { text: `total · ${ts.length} runs` }))));
    });
    const scope = [state.stage !== "all" ? state.stage : null, state.level !== "all" ? `${state.level}-level` : null].filter(Boolean).join(" ");
    const subtitle = $("#lb-sub");
    if (subtitle) subtitle.textContent = `Rank score across ${ts.length} ${scope ? scope + " " : ""}task${ts.length === 1 ? "" : "s"}.`;
  }
  if ($("#lb tbody") && $("#seg-stage") && $("#seg-level")) { drawSegs(); render(); }

  /* ---------------- task rows and filters ---------------- */
  const results = $("#task-results"), legend = $("#results-legend");
  const stageControl = $("#f-stage"), levelControl = $("#f-level"), search = $("#f-q"), count = $("#task-foot");
  const additionalResults = $("#task-results-extra"), moreResults = $("#more-task-results"), toggleLabel = $("#task-results-toggle-label");
  if (!results || !legend || !stageControl || !levelControl || !search || !count || !additionalResults || !moreResults || !toggleLabel) return;
  const featuredKeys = new Set(["opd", "sageattention", "qvg"]);

  const saved = history.state?.infrathonTasks;
  const taskFilter = {
    stage: ["all", ...STAGES].includes(saved?.stage) ? saved.stage : "all",
    level: ["all", ...LEVELS].includes(saved?.level) ? saved.level : "all",
    q: typeof saved?.q === "string" ? saved.q : ""
  };
  const highlight = MODELS.includes(saved?.highlight) ? saved.highlight : null;
  results.replaceChildren();
  additionalResults.replaceChildren();
  moreResults.open = saved?.expanded === true;
  legend.replaceChildren();
  X.makeLegend(legend);

  const taskRows = D.tasks.map((task) => {
    const winner = task.winner;
    const row = h("a", { class: "card task-result-row", href: X.taskHref(task.key), id: `task-result-${task.key}`, "data-task": task.key, "data-stage": task.stage, "data-level": task.level },
      h("div", { class: "task-result-info" }, h("h3", { text: task.name }), h("p", { class: "target", text: task.target })),
      h("div", { class: "task-result-category" }, h("span", { class: "label", text: "Category" }), h("span", { text: `${cap(task.stage)} · ${cap(task.level)}` })),
      h("div", { class: "task-result-budget" }, h("span", { class: "label", text: "Budget" }), h("b", { text: `${task.budget_h} h` })),
      h("div", { class: "task-result-metric" }, h("span", { class: "label", text: "Metric" }), h("span", { class: "metric-name", text: task.metric_info?.home_label || X.metricLabel(task) })),
      h("div", { class: "task-result-winner" }, h("span", { class: "label", text: "Top configuration" }), X.who(winner, MODEL[winner].short), h("span", { class: "task-result-score", text: withUnit(task, task.results[winner].best) })),
      h("div", { class: "task-result-chart" }, X.trajChart(task, { W: 300, H: 160, logY: task.key === "flash-kmeans" })));
    results.append(row);
    return { task, row };
  });
  const empty = h("p", { class: "task-results-empty muted", role: "status", text: "No task matches these filters." });
  results.append(empty);
  if (highlight) X.setFocus(highlight);

  function saveTaskState() {
    const active = legend.querySelector('button[aria-pressed="true"]');
    history.replaceState({ ...history.state, infrathonTasks: { ...taskFilter, highlight: active?.dataset.m || null, expanded: moreResults.open } }, "");
  }
  function renderTaskRows() {
    const query = taskFilter.q.trim().toLowerCase();
    const filtersActive = taskFilter.stage !== "all" || taskFilter.level !== "all" || !!query;
    let matched = 0;
    let featured = 0;
    let additional = 0;
    for (const { task, row } of taskRows) {
      const matches = (taskFilter.stage === "all" || task.stage === taskFilter.stage)
        && (taskFilter.level === "all" || task.level === taskFilter.level)
        && (!query || `${task.name} ${task.target} ${task.summary}`.toLowerCase().includes(query));
      row.hidden = !matches;
      if (matches && (filtersActive || featuredKeys.has(task.key))) {
        results.append(row);
        featured++;
      } else {
        additionalResults.append(row);
        if (matches) additional++;
      }
      if (matches) matched++;
    }
    results.append(empty);
    empty.hidden = matched > 0;
    moreResults.hidden = filtersActive || additional === 0;
    toggleLabel.textContent = moreResults.open ? `Hide ${additional} additional tasks` : `Show ${additional} more tasks`;
    count.textContent = filtersActive ? `${matched} of ${D.tasks.length} tasks match your filters.`
      : moreResults.open ? `All ${matched} tasks are visible.`
      : `${featured} of ${matched} tasks shown.`;
    X.hideTip();
    saveTaskState();
  }
  X.seg(stageControl, [["all", "All"], ...STAGES.map((stage) => [stage, cap(stage), D.tasks.filter((task) => task.stage === stage).length])], taskFilter.stage, (stage) => { taskFilter.stage = stage; renderTaskRows(); });
  X.seg(levelControl, [["all", "All"], ...LEVELS.map((level) => [level, cap(level), D.tasks.filter((task) => task.level === level).length])], taskFilter.level, (level) => { taskFilter.level = level; renderTaskRows(); });
  search.value = taskFilter.q;
  search.addEventListener("input", () => { taskFilter.q = search.value; renderTaskRows(); });
  legend.addEventListener("click", saveTaskState);
  moreResults.addEventListener("toggle", renderTaskRows);
  $("#collapse-task-results").addEventListener("click", () => {
    moreResults.open = false;
    moreResults.querySelector("summary").focus();
  });
  renderTaskRows();
})();
