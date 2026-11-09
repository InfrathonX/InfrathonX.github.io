/* Use the light theme on every page, including previously dark-mode visits. */
(() => {
  "use strict";
  document.documentElement.dataset.theme = "light";
  try { localStorage.removeItem("infrathon-theme"); } catch (_) { /* Storage may be disabled. */ }
})();
