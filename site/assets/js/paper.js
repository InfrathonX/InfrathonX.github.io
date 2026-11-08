(() => {
  "use strict";
  const dialog = document.getElementById("figure-dialog");
  const artwork = document.getElementById("figure-dialog-image");
  if (dialog && artwork) {
    document.querySelectorAll("[data-expand-figure]").forEach((button) => {
      button.addEventListener("click", () => {
        const figure = button.closest("figure");
        const source = figure.querySelector("img");
        document.getElementById("figure-dialog-title").textContent = figure.querySelector("h3").textContent;
        artwork.src = source.src;
        artwork.alt = source.alt;
        dialog.showModal();
      });
    });
    document.getElementById("figure-dialog-close").addEventListener("click", () => dialog.close());
    dialog.addEventListener("click", (event) => { if (event.target === dialog) dialog.close(); });
  }
  document.querySelectorAll("[data-close-disclosure]").forEach((button) => {
    button.addEventListener("click", () => {
      const disclosure = button.closest("details");
      disclosure.open = false;
      disclosure.querySelector("summary").focus();
    });
  });
  const aliases = {
    "agent-behavior": {"figure-9": "requirements", "figure-9a": "requirements", "figure-9b": "requirements", "figure-10": "validation", "figure-10a": "validation", "figure-10b": "validation", "figure-11": "validation", "figure-12": "improvement", "figure-12a": "improvement", "figure-12b": "improvement", "overall-answer": "requirements", behavior: "improvement"},
    framework: {"task-definition": "definition", "task-execution": "execution"}
  };
  function followLegacyAnchor() {
    const target = aliases[document.body.dataset.page]?.[location.hash.slice(1)];
    if (!target) return;
    history.replaceState(history.state, "", `${location.pathname}${location.search}#${target}`);
    document.getElementById(target)?.scrollIntoView();
  }
  followLegacyAnchor();
  window.addEventListener("hashchange", followLegacyAnchor);
})();
