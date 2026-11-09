/* Homepage outline, scoring notes, and links from previous layouts. */
(() => {
  "use strict";
  const legacy = {
    architecture: "framework.html#overview", framework: "framework.html#overview", "framework-overview": "framework.html#overview",
    protocol: "framework.html#protocol", execution: "framework.html#execution",
    "task-definition": "framework.html#definition", "task-execution": "framework.html#execution"
  };
  function followHomeHash() {
    const hash = location.hash.slice(1);
    const target = legacy[hash];
    if (target) {
      const url = new URL(target, location.href);
      url.search = location.search;
      location.replace(url.href);
      return;
    }
    if (hash === "score-notes") document.getElementById("score-notes").open = true;
    const alias = { cite: "overview", introduction: "overview", abstract: "overview", map: "results", "figure-2": "leaderboard", "figure-3": "results" }[hash] || (/^results-/.test(hash) ? "results" : null);
    if (alias) {
      history.replaceState(history.state, "", `${location.pathname}${location.search}#${alias}`);
      document.getElementById(alias).scrollIntoView();
    }
  }
  followHomeHash();
  window.addEventListener("hashchange", followHomeHash);
})();

(() => {
  "use strict";
  if (document.body.dataset.page !== "index" || !window.IX) return;
  const { h } = window.IX;
  const sidebar = document.querySelector(".nav .wrap");
  if (!sidebar) return;
  const entries = [
    ["overview", "Overview"],
    ["leaderboard", "Leaderboard"],
    ["results", "All Results"],
    ["knowledge-discovery", "Knowledge Discovery"],
    ["long-vs-short", "Long Horizon vs. Short Horizon"]
  ];
  const list = (items) => h("ul", {}, items.map(([id, label, children]) =>
    h("li", {}, h("a", { href: `#${id}`, text: label }), children ? list(children) : null)));
  const outline = h("nav", { class: "home-outline", "aria-label": "Page contents" },
    h("p", { class: "home-outline-title", text: "Contents" }), list(entries));
  sidebar.insertBefore(outline, sidebar.querySelector(".nav-right"));
  const sections = Array.from(outline.querySelectorAll("a"), (link) => ({
    link, target: document.getElementById(link.hash.slice(1))
  })).filter(({ target }) => target);
  function highlightSection() {
    const threshold = (parseFloat(getComputedStyle(document.documentElement).getPropertyValue("--nav-height")) || 0) + 48;
    let current = sections[0];
    for (const section of sections) if (section.target.getBoundingClientRect().top <= threshold) current = section;
    if (scrollY > 0 && scrollY + innerHeight >= document.documentElement.scrollHeight - 2) current = sections.at(-1);
    for (const section of sections) {
      if (section === current) section.link.setAttribute("aria-current", "location");
      else section.link.removeAttribute("aria-current");
    }
  }
  let pending = false;
  function queueHighlight() {
    if (pending) return;
    pending = true;
    requestAnimationFrame(() => { pending = false; highlightSection(); });
  }
  window.addEventListener("scroll", queueHighlight, { passive: true });
  window.addEventListener("resize", queueHighlight);
  window.addEventListener("hashchange", queueHighlight);
  highlightSection();
})();
