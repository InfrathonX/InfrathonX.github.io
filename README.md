# Infrathon website

Paper website for **Infrathon: Benchmarking Language Agents for Real-World, Long-Horizon AI Infra Optimization**. Plain HTML, CSS, and JavaScript, with committed measurements and original figure assets from the author-supplied Overleaf archive.

## Deployment

Live website: https://infrathonx.github.io/

GitHub Pages publishes the `main` branch from the repository root. The root
homepage and frontend files mirror `site/`, so both `/` and the existing
`/site/` URLs show the website. `.nojekyll` preserves the static files.
The `Site checks` workflow validates data, JavaScript, links, figures, and
the root mirror. GitHub's built-in Pages workflow handles deployment.

Edit the source files in `site/`, then run `python3 scripts/sync_root_site.py`
before committing. The script synchronizes only the frontend files listed in
`data/root_site_files.json`, preserving the repository's research data.
CI rejects stale root copies. To preview the published root layout, serve
the repository directory with `python3 -m http.server 8000`.

```
site/
  index.html                 paper identity, figures, interactive leaderboard, finding summaries, expandable task trajectories
  blog.html                  author-provided standalone blog, embedded figures, model tabs, and image expansion
  framework.html             task definition, task inventory, Work/Controller/Judge execution
  main-results.html          current manuscript setup, trajectories, plateaus, and rankings
  knowledge-discovery.html   Quant-VideoGen discovery, two-dataset comparison, submission evidence
  analysis.html              equal-budget comparisons, horizon-dependent rankings, tokens and actions
  agent-behavior.html        current manuscript requirements, testing, and premature completion
  experimental-results.html compatibility redirect to Main Results or the relevant Analysis section
  archived-results.html      standalone interactive explorer using the same data as Home
  tasks.html                 task documentation directory, grouped by stage and level
  trajectories.html#<task>/<model>  run log reached from task details
  docs.html                  installation, assets, Docker, launchers, outputs
  task.html#<key>/<section>   unified task goal, metric, results, settings, running details
  task-results.html#<key>     compatibility redirect → task.html#<key>
  architecture.html         compatibility redirect → framework.html#overview
  method.html                compatibility redirect → framework.html#overview
  results.html               compatibility redirect → experimental-results.html
  behavior.html              compatibility redirect → agent-behavior.html
  runs.html                  compatibility redirect → trajectories.html
  assets/css/site.css        shared layout and themes
  assets/css/home.css        sidebar, paper identity, leaderboard, and task rows
  assets/css/paper.css       research articles, original figures, tables, and finding cards
  assets/css/framework.css   framework definitions and task inventory
  assets/css/experimental-results.css  experimental figures and expansion dialog
  assets/css/agent-behavior.css  behavior figure components
  assets/css/docs.css        documentation sidebar, article, contents, code blocks
  assets/css/tasks.css       task documentation directory
  assets/css/task-results.css  individual task result layout
  assets/js/core.js          shared data access, rank math, charts, navigation
  assets/js/section-tabs.js  single-section views, deep links, keyboard navigation
  assets/js/home.js          homepage outline, scoring notes, and legacy anchors
  assets/js/home-results.js  leaderboard, featured tasks, expandable and filterable trajectories
  assets/js/paper.js         original-figure expansion and legacy paper anchors
  assets/js/experimental-results.js  figure expansion and section navigation
  assets/js/docs.js          task search, shared documentation navigation, command copying
  assets/js/task-results.js  task charts and per-model results
  assets/js/<page>.js        page rendering
  assets/img/institutions/   institution artwork extracted from the paper
  assets/img/homepage/       latest paper optimization example and framework SVGs
  assets/img/paper/          current manuscript original PDFs and vector SVGs
  assets/img/experimental-results/  original figure PDFs and vector SVG conversions
  data/infrathon.js          generated results and cost bundle
  data/docs.js               generated guides for all 25 tasks
  data/behavior.js           archived digitized Section 5 figure bundle
data/
  tasks.json                 task and model registry
  task_metrics.json          short metric explanations, formulas, conditions, source provenance
  task_guides.json           task settings, interfaces, metric summaries, source hashes
  setup_sources.json         setup documentation sources and public resource URLs
  raw/runs.json              selected dashboard submissions
  qvg_scores.json            quality-weighted QVG scores and source report hash
  tokens.json                paper cost totals and 150 per-task cost records
  behavior_figures.json      Section 5 measurements and source provenance
  behavior_original_figures.json  original PDFs, display SVGs, source hashes, section mapping
  experimental_figures.json  Figures 2–8 source archive, hashes, and display assets
  author_links.json          verified author homepage links; null when unconfirmed
  institution_logos.json     paper logo extraction provenance
  resource_icons.json        official arXiv, GitHub, Docker, and Hugging Face SVG sources and hashes
  framework_figure.json      original Overleaf framework figure provenance
  home_figures.json          latest homepage figure sources, dimensions, and hashes
  paper_figures.json         current manuscript source hash and original figure provenance
  tts_runs.json              author-supplied TTS report data: 84 runs and 36 grouped curves
  tts_figures.json           validated TTS comparisons, geometric means, and plot hashes
scripts/
  extract_dashboard.py      dashboard ZIP → selected runs
  build_data.py             results, ranks, summaries → infrathon.js
  import_qvg_scores.py       QVG HTML report → checked score update; preserves raw archive
  build_docs.py             task guides → docs.js
  extract_behavior_figures.py  archived figure JSON → behavior.js; optional PDF extraction
  export_behavior_figures.py   original Section 5 PDFs → SVG assets and manifest
  extract_experimental_figures.py  Overleaf figure PDFs → SVG assets and manifest
  extract_paper_distributions.py  archived 41-page manuscript Figure 5 extraction
  export_paper_figures.py    current Overleaf directory → original PDFs, SVGs, and source manifest
  build_tts_figures.py       author TTS HTML → validated data and SVG/PDF/PNG comparisons
  sync_root_site.py          site/ → committed domain-root frontend, with a CI freshness check
  check_site.py              local links, anchors, bundle structure, leaked local paths
  check_documentation_sources.py  task and setup sources against the public repository and paper
```

## Updating results

```bash
python3 scripts/extract_dashboard.py /path/to/dashboard-results.zip
python3 scripts/build_data.py
python3 scripts/build_docs.py
python3 scripts/extract_behavior_figures.py
python3 -m unittest discover -s tests -v
python3 scripts/check_site.py
```

The selected run source is `dashboard-latest-results-20261025.zip`: one selected page per task, with Astra OPD included and Qwen Concurrent agent-22 restored (best score 154.3333). The importer excludes Gemini, the voided LLaDA DeepSeek attempt, and Sol’s local Mamba-2 rerun. It supplements missing Astra OPD from the latest earlier run when needed. Independent final-artifact evaluations remain in raw records and do not determine the leaderboard.

The earlier dashboard and figure checks use `_AI_Infra____New_Template_Version___Zhengyu_Hu (1).zip` (SHA-256 `732678e3d954a4c605b1961abcdf994ebb22c1cd90b1a49683cd5caf2cd49cf5`). Historical experimental assets use `scripts/extract_experimental_figures.py`; archived behavior assets use `scripts/export_behavior_figures.py`. Their `--check` modes verify committed assets without extracting them.

Current research pages and homepage findings follow the author-supplied `../overleaf/main.tex`. Run `python3 scripts/export_paper_figures.py ../overleaf` with `pdftocairo` installed to export its original figures; `--check` validates committed PDFs, SVGs, and hashes. The figure manifest is `data/paper_figures.json`. The interactive results retain the original dashboard runs, with the author's quality-weighted QVG scores applied from `data/qvg_scores.json`. This changes overall Sol/GLM scores from 53.6/8.8 to the current manuscript's 54.4/8.0. Other tasks, submission timestamps, validity statuses, and archived raw records are unchanged.

Preview with `python3 -m http.server -d site 8000`.

The Long Horizon vs. Short Horizon section uses the author-supplied `TTS.html` data, version 19. Run `python3 scripts/build_tts_figures.py /path/to/TTS.html` to import it and render the two six-task trajectory figures and build the compact browser data bundle; Matplotlib is required only for rendering. Run the script without a source to redraw from `data/tts_runs.json`, or use `--check` to validate the committed data and assets using only the standard library. The importer checks all 84 run budgets, submission order, best-so-far values, and grouped curves. Final long-run scores match the 12 main-experiment runs. Geometric means reproduce 102.6% / 96.9% / 77.3% for best-of-four and 101.3% / 96.5% / 79.4% for best-of-two. Summary ratios use one long run as 100%; the interactive viewer shows all 12 task–model trajectories in two model groups. Charts show the best score as step lines, without submission dots or endpoint markers. Allocation legends toggle curves; each plot opens in a larger interactive dialog. The default paper time axis assigns 75% of the width to the first half and 25% to the shaded second half, with an option for linear hours. Short curves stop at T/n. The same viewer appears on Home and Analysis, with the key findings below. The model-specific comparison paragraph and the expanded setup/scoring block are removed; the visible T/TTS allocation definitions remain above Astra. SVG, PDF, and PNG files are in `site/assets/img/tts/`; the original manuscript figure remains archived unchanged.

To refresh QVG, run `python3 scripts/import_qvg_scores.py '/path/to/QVG Agent Leaderboard(1).html'`, then rebuild both data and documentation bundles. The importer matches all 108 submissions to the original six runs and verifies elapsed times, compression-only scores, and validity before accepting the update. It retains the report's two-decimal score precision and the dashboard's original timestamps. Invalid submissions never become valid through rescoring.

## Scoring and interaction costs

Every task has a source-checked metric description in `data/task_metrics.json`, based on the latest Overleaf paper's task appendix and the matching release task specifications. The file records the paper archive hash, documentation revision, and source-document hashes. The bundle includes the display content as `task.metric_info`; provenance stays in the source file. Homepage rows use compact `home_label` units or expressions (for example, `TFLOPS` or `Accuracy gain / training hour`); task details explain the full metric, formula, aggregation, baseline, and scoring conditions. Descriptions do not change any measured score, submission, trajectory, or ranking calculation.

The site follows paper Eq. 5. Each model is ranked by its best finite, valid score within each task's time budget; exact ties share the average rank. A run without a valid scored submission receives zero. Its rank score is the mean of `100 × (K − rank) / (K − 1)` over selected tasks, with fixed `K = 6`. All six models cover all 25 tasks. Flash-KMeans latency is converted to equivalent throughput, preserving the ordering. Budget and finiteness checks apply to performance summaries; submission records and status counts retain the original observations.

Regression checks cover 144 scores from the earlier manuscript table plus six quality-weighted QVG scores from the current manuscript and author-supplied report. The fixture retains the historical filename `tests/paper_table4.json`. `tests/test_paper_audit.py` checks category and overall rank scores, exact ties, and the independently sourced token/action totals. The website adds 95% task-bootstrap confidence intervals: 10,000 resamples for the full suite and 3,000 for filtered subsets.

Visible tokens follow Appendix B.4’s `o200k_base` definition: recorded agent text and tool-call content, excluding tool responses, repeated code-diff displays, and hidden reasoning. Full-suite totals match current Figure 8. Filtered totals sum current Figure 15’s per-task values, which are rounded to thousands and displayed with `≈`. Summing these rounded cells does not reproduce the unrounded suite total exactly. Agent actions are integers and sum to 203,266. First-score medians are computed from the selected tasks’ scored runs. These statistics cover the 150 main-experiment runs and exclude the short-budget ablations.

Cost values were originally transcribed from Figures 7 and 14 of earlier manuscript revisions. All 12 model totals and all 300 per-task token/action cells were checked against Figures 8 and 15 in the latest archive and are unchanged. `data/tokens.json` preserves original extraction references, earlier PDF verification, and the latest archive/member hashes. The dashboard ZIP does not contain the message trajectories needed to rerun tokenization.

The retained first-score distributions come from the October 25, 41-page manuscript’s Figure 5. These archived coordinates are not current Figure 6 data; the Experimental Results page uses the latest original figure asset. `scripts/extract_paper_distributions.py` remains specific to the 41-page layout and rejects other page counts. Printed completion and repetition statistics retain their original Figure 11 provenance and have been checked against current Figure 12. The main-experiment totals exclude the 72 additional short Astra/Claude runs in Section 4.3, which add 2,016 GPU-hours and reuse 12 primary runs to form 84 ablation trajectories.

## Paper layout and figures

Published charts and tables use descriptive titles without paper numbering. Source manifests and legacy anchors retain their original identifiers; figure expansion uses the displayed title.

Research pages lead with findings. Experiment settings, statistical definitions, and interaction-counting details are available in expandable sections. `copywriting-review.md` records the 52 reviewed copy items and 13 additional edits, including the method and task rules retained for reference.

Research pages follow the current manuscript in this order: Main Results, Knowledge Discovery with Infrathon, Analysis, and Agent Behavior Analysis. Each page has section links, original figures, and a figure-expansion dialog. The standalone Framework article explains task construction and execution.

The homepage (`index.html`) follows the paper title and author order, with 21 names in three desktop rows (7 / 8 / 6), numbered affiliations, and eight unlinked logos. Each author group can wrap on narrower screens. Author names, superscripts, and role notes follow the author-supplied `main.tex`: † marks the project leader and * marks corresponding authors. `data/author_links.json` records all 21 author links in paper order. Affiliation numbers and logo order follow the latest author-supplied reference: Washington, Ai2, Penn, Pyromind Dynamics, Stanford, RadixArk, UT Austin, Northwestern. Zheyuan Xiao is affiliated with Washington. Seven logos preserve the PDF’s vector paths; Pyromind Dynamics uses its original transparent image. `data/institution_logos.json` records the original PDF hash and extraction positions, not the display order. Resource buttons use the author-provided GitHub, Docker Hub, and Hugging Face URLs; the arXiv entry links to the paper at `https://arxiv.org/abs/2611.11995`.

The brand opens Home; primary navigation contains Task List, Docs, and Blog, with Discord in the sidebar footer. Blog opens `blog.html`, imported from the author-provided HTML (SHA-256 `2882886cc8cf584436806b7487272040b4abd83c65654a09dcf6b5c65041d95f`). The standalone article retains its text, tables, embedded images and licensed font, model tabs, and figure dialog; it adds a return-home link, the site favicon, and a canonical URL. Research articles remain available through the homepage finding links and article links. Task descriptions and results share `task.html#<key>` with `/<section>` anchors. Homepage task rows and the task directory open this unified page; per-model Run log links open `trajectories.html#<task>/<model>`.

Home uses a 280px fixed left navigation on wide screens, with Task List, Docs, Blog, and Discord. An always-expanded Contents outline below the page links jumps to Overview, Leaderboard, All Results, Knowledge Discovery, and Long Horizon vs. Short Horizon. All five entries appear at the same level. The main content uses a centered maximum width of 1720px, with equal left/right gutters in the space beside the sidebar. It highlights the current section while scrolling and is hidden when the navigation becomes a top bar on smaller screens. A horizontal row of institution logos sits above the single-line paper title. The authors and affiliations are centered in a readable column, with four benchmark-scale statistics below. A Blog button links to `blog.html` at the start of the compact, centered resource row beneath the hero card, followed by arXiv, GitHub, Docker Hub, and Hugging Face. All five buttons are 40px tall; the four external resources retain their unmodified official SVG artwork. Source URLs and hashes are recorded in `data/resource_icons.json`. Author names use the same blue as their hover state. A Contact section at the bottom of the homepage lists named mail links for Zhengyu Hu (`zhu7@uw.edu`) and Teng Xiao (`tengxiao01@gmail.com`). Smaller screens return to a top navigation and let the title and institution logos wrap; resource buttons use two columns.

The homepage and research pages use DM Sans, a light-gray canvas, white panels, black text, and blue accents. Author and affiliation text uses gray. Section headings sit outside panels. After the paper header, Home presents three parts: Leaderboard with Claude's performance finding between its heading and table, followed by scoring definitions and expandable task results; Infrathon can support knowledge discovery with the original optimization example below its conclusion; and Long Horizon vs. Short Horizon. The task results belong to the first part and appear immediately after Scoring and token definitions. The Main Results kicker, leaderboard subtitle, separate Key findings grid, homepage Abstract and Framework sections are removed. Finding summaries use a horizontal layout on desktop and stack on mobile. Detailed research analysis remains on the article pages. Interactive results include the quality-weighted QVG scores.

The homepage optimization example links to its full-size SVG and keeps a white artwork background. `data/home_figures.json` records its source and the earlier homepage framework asset. Original Framework artwork remains available in the framework article. Homepage artwork can be regenerated from the author-supplied figure PDFs with `pdftocairo -svg`.

Task results initially show Miles Qwen3 OPD, SageAttention, and Quant-VideoGen KV Codec, covering system, operator, and module levels and both application stages. A native disclosure expands the remaining 22 tasks. Stage, level, and search filters show all matching tasks directly; clearing filters restores the featured or previously expanded view. A red, bold hint below All Results invites readers to click a task for its details; the earlier trajectory subtitle is removed. Each row pairs the task name and optimization target with its category, budget, metric, best configuration, and a compact trajectory chart. Rows omit Start and All six columns, open individual task results, and stack their content on small screens. Filters, the selected model highlight, and expansion state are saved in history. Filtering and expansion reuse the existing chart nodes and listeners. The leaderboard omits mean-relative performance and bootstrap first-place probability; visible output tokens are totals across the selected main runs, explicitly excluding hidden reasoning. Scoring and token definitions remain collapsed at `#score-notes`. The homepage citation block and shared site footer are removed.

Framework follows the current task-definition and task-execution sections: the latest original framework figure; W/P/E/R/T definitions; the public/private KVzip example; separate Work, Controller, and Judge roles; submission review; and the complete 25-task inventory. Inventory rows link to task details.

Main Results covers the current six-model, 150-run experiment, H100 80 GB hardware, 10,512 GPU-hours, progress after long plateaus, final rank scores, task-specific strengths, and original task trajectories. Knowledge Discovery with Infrathon presents the latest Quant-VideoGen compression and quality table on both datasets and the original submission comparison. Analysis covers equal GPU-hour long/short runs, model rankings over time, second-half improvements, and token/action usage. Current original figures are tracked in `data/paper_figures.json`.

Old Architecture/Method URLs route to Framework; Results/Experimental Results URLs route to Main Results or the relevant Analysis section; Behavior URLs route to Agent Behavior Analysis; Runs URLs route to task/model logs. Queries are preserved. Old `#score-notes` and `#map` links open homepage components. Legacy citation anchors open the homepage overview; task-key links continue to open unified task pages.

Task pages have a visible Back button. Visits from Home or the task directory return through browser history; direct or external arrivals fall back to `tasks.html`. Search, stage, level, and highlighted model are saved on the homepage history entry. Adjacent-task, sidebar-task, and contents navigation replace the current task entry, preserving the original return destination.

Agent Behavior Analysis follows the current manuscript's three issues: task-requirement violations, tests that do not execute the changed code, and premature completion. It uses the current original task-fidelity figure and the three selected continuation examples: GLM/SageAttention +24.8%, Astra/Flux +7.3%, and DeepSeek/SD3.5-M +14.0%. Historical figure and digitized-data manifests remain for archive integrity checks and do not render this page.

The site uses one light theme. Charts use shared theme variables and responsive dimensions.

## Documentation

The setup guide follows the `Infrathon` repository at `https://github.com/InfrathonX/Infrathon`, revision `ad760e7d033028857d5c77e118a4829027934548`. The local source checkout is `../Infrathon`. Its task READMEs, Work contracts, public tests, Judge code, task configurations, and launchers are the current code references; the former `ultrainfrabench-release/docs/tasks` directory is not the release documentation source. The guide covers host requirements, repository installation, Codex and Claude Code runtime downloads, agent login and CLI version selection, a complete first-run configuration including submission-review credentials, asset fetching and Hugging Face authentication, direct Docker pulls using recorded hardware-specific tags, local image preparation, candidate history, launching a kernel task, and submission outputs. Public Code, Docker, and Dataset links use the author-provided resource URLs, also recorded in `data/setup_sources.json`.

Docs shows one setup section at a time, selected from its sidebar, with shareable section links and browser history. Tasks has its own searchable directory and 25 unified task pages. Each page presents the task introduction and metric summary once, followed by best scores, optimization trajectories, submission history, and the per-model results table. Task setup follows the results and explains the model and data or synthetic workload, workload settings, starting point, editable scope, and hardware. Detailed metric calculations and validity checks, then environment setup and launch commands, appear in disclosures. Document sidebars and contents collapse on mobile.

`data/task_guides.json` records each task's source files, launcher, source hashes, reader-oriented descriptions, and result-page summaries. Metric explanations follow the paper and `data/task_metrics.json`. `data/setup_sources.json` records the setup sources and code revision. The audit found unchanged task interfaces and scoring code across the former and current repositories, but changed launcher defaults and flags. Task hardware follows the paper's independent Worker and Judge allocations, recorded in `gpu_allocation_source`; examples explicitly use 12- or 24-hour experiment budgets. Launchers that default to one shared GPU select their `--legacy-dual-gpu` path with separate `WORK_GPU` and `JUDGE_GPU` values. All 25 task pages include Launch commands. The nine two-GPU workloads expose a shared-pair launcher in the public checkout; their commands and configuration steps are displayed with a brief shared-GPU note, as authorized by the author. The hardware description above them records the paper experiment allocation. Concurrent serving uses CPU Worker/Judge containers and a dedicated two-GPU backend, as in the paper. `scripts/build_docs.py` checks registry coverage and required content fields and emits display fields into `site/data/docs.js`; archived code-interface and public-test descriptions remain in the source data.

Run `python3 scripts/check_documentation_sources.py` with the sibling source checkout and paper archive present to verify source paths, hashes, task IDs, launchers, and example budgets. Use `--repo` and `--paper` for other locations. This check also parses the documented shell commands without executing them. A source revision update requires reviewing changed files and refreshing their recorded hashes.

Setup commands were checked against the release code and launcher help. The candidate-history example was exercised in temporary stores. Docker pulls, image builds, and GPU runs have not been executed as part of the website update.

## Deployment

`.github/workflows/pages.yml` rebuilds results, documentation, and archived behavior bundles; validates committed bundles; runs data tests, original-figure integrity checks, JavaScript checks, and local-reference checks. GitHub's Pages publishing configuration serves the repository-root redirect and `site/` content.
