#!/usr/bin/env python3
"""Import the author's TTS HTML data and render reproducible comparison figures."""
from __future__ import annotations

import argparse
from bisect import bisect_right
from collections import Counter
import hashlib
from html.parser import HTMLParser
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/tts_runs.json"
MANIFEST = ROOT / "data/tts_figures.json"
ASSETS = ROOT / "site/assets/img/tts"
MODELS = {"gpt-6-astra": "GPT-6 Astra", "claude-opus-5-5": "Claude Opus 5.5"}
TASKS = ("flux", "orpo", "sd35m", "lmcache", "kvzip", "llada")
LEVELS = ("Operator", "Module", "System")
TITLES = {"flux": "Flux/Comet MoE", "orpo": "Qwen3 ORPO", "sd35m": "SD3.5-M OPD",
          "lmcache": "LMCache", "kvzip": "KVzip", "llada": "LLaDA decoding"}
COLORS = {1: "#F2545B", 2: "#78AD00", 4: "#2F80ED"}
LABELS = {1: "Long horizon (1 × T)", 2: "Best-of-2 (2 × T/2)", 4: "Best-of-4 (4 × T/4)"}


def digest(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


class ReportData(HTMLParser):
    def __init__(self):
        super().__init__()
        self.active = False
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag == "script":
            attributes = dict(attrs)
            self.active = attributes.get("id") == "data" and attributes.get("type") == "application/json"

    def handle_data(self, data):
        if self.active:
            self.parts.append(data)

    def handle_endtag(self, tag):
        if tag == "script":
            self.active = False


def summarize(data: dict) -> dict:
    """Validate run budgets and grouped curves before computing score ratios."""
    panels = data["panels"]
    expected = {(model, task) for model in MODELS for task in TASKS}
    if len(panels) != 12 or {(p["model"], p["task"]) for p in panels} != expected:
        raise ValueError("Expected both models on all six tasks")
    rows = []
    all_ids = set()
    for panel in panels:
        curves = panel["curves"]
        if Counter(c["allocation"] for c in curves) != {1: 1, 2: 2, 4: 4}:
            raise ValueError(f"Incorrect allocations: {panel['id']}")
        if panel["budget"] != (12 if panel["level"] == "Operator" else 24):
            raise ValueError("Unexpected task budget")
        for curve in curves:
            run_id = curve["run_id"]
            if run_id in all_ids:
                raise ValueError(f"Duplicate run: {run_id}")
            all_ids.add(run_id)
            if curve["direction"] != "maximize" or not curve["points"]:
                raise ValueError(f"Unsupported or empty run: {run_id}")
            if not math.isclose(curve["budget_hours"] * curve["allocation"], panel["budget"]):
                raise ValueError(f"Unequal allocated budget: {run_id}")
            previous_time, best = -1, -math.inf
            for point in curve["points"]:
                time, score = point["elapsed_h"], point["score"]
                if not all(math.isfinite(v) for v in (time, score, point["best_score"])):
                    raise ValueError(f"Non-finite submission: {run_id}")
                if time < previous_time or time < 0 or time > curve["budget_hours"] + 1e-9:
                    raise ValueError(f"Submission outside ordered budget: {run_id}")
                best = max(best, score)
                if not math.isclose(best, point["best_score"], rel_tol=1e-10):
                    raise ValueError(f"Incorrect best-so-far score: {run_id}")
                previous_time = time
        if Counter(g["allocation"] for g in panel["groups"]) != {1: 1, 2: 1, 4: 1}:
            raise ValueError("Expected three grouped curves per panel")
        scores = {}
        for group in panel["groups"]:
            allocation = group["allocation"]
            runs = [c for c in curves if c["allocation"] == allocation]
            if set(group["run_ids"]) != {c["run_id"] for c in runs}:
                raise ValueError("Grouped curve refers to different runs")
            events = sorted((p["elapsed_h"], p["score"]) for c in runs for p in c["points"])
            times, bests, best = [], [], -math.inf
            for time, score in events:
                best = max(best, score)
                times.append(time)
                bests.append(best)
            plotted_times, plotted_scores = group["plotted_times"], group["plotted_best_scores"]
            budget = panel["budget"] / allocation
            if not math.isclose(group["budget_hours"], budget) or not math.isclose(plotted_times[-1], budget):
                raise ValueError("Grouped curve has an incorrect budget endpoint")
            if len(plotted_times) != len(plotted_scores) or plotted_times != sorted(plotted_times):
                raise ValueError("Invalid plotted coordinates")
            for time, score in zip(plotted_times, plotted_scores):
                index = bisect_right(times, time + 1e-10) - 1
                if index < 0 or time > budget + 1e-9 or not math.isclose(score, bests[index], rel_tol=1e-10):
                    raise ValueError("Grouped curve differs from the original submissions")
            if best <= 0:
                raise ValueError("Relative performance requires positive final scores")
            scores[str(allocation)] = best
        rows.append({
            "model": panel["model"], "task": panel["task"], "level": panel["level"],
            "scores": scores,
            "ratios": {str(n): scores[str(n)] / scores["1"] for n in (2, 4)},
            "long_wins": scores["1"] > max(scores["2"], scores["4"]),
        })
    geometric_means = {}
    for level in LEVELS:
        group = [r for r in rows if r["level"] == level]
        if len(group) != 4:
            raise ValueError("Each level must contain two tasks for both models")
        geometric_means[level] = {
            str(n): 100 * math.exp(sum(math.log(r["ratios"][str(n)]) for r in group) / len(group))
            for n in (2, 4)
        }
    return {
        "n_runs": len(all_ids), "n_comparisons": len(rows),
        "long_wins": sum(r["long_wins"] for r in rows),
        "system_long_wins": sum(r["long_wins"] for r in rows if r["level"] == "System"),
        "model_long_wins": {m: sum(r["long_wins"] for r in rows if r["model"] == m) for m in MODELS},
        "geometric_means_pct": geometric_means, "comparisons": rows,
    }


def browser_data(data: dict) -> dict:
    panels = []
    for panel in data["panels"]:
        groups = []
        for group in panel["groups"]:
            n = group["allocation"]
            groups.append({"n": n, "hours": group["budget_hours"],
                           "times": group["plotted_times"], "best": group["plotted_best_scores"]})
        panels.append({**{key: panel[key] for key in ("id", "model", "modelLabel", "task", "title", "stage", "level", "unit", "budget", "limits")}, "groups": groups})
    return {"source": data["source"], "panels": panels}


def render(data: dict, summary: dict) -> list[dict]:
    # Imports are local so --check and the data regression tests need only Python.
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from matplotlib.ticker import MaxNLocator

    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 11, "text.color": "#111111",
        "axes.labelcolor": "#111111", "xtick.color": "#111111", "ytick.color": "#111111",
        "axes.edgecolor": "#CCD3DF", "axes.spines.top": False, "axes.spines.right": False,
        "grid.color": "#E7EBF2", "grid.linewidth": .8, "axes.axisbelow": True,
        "svg.fonttype": "path", "svg.hashsalt": "infrathon-tts-v19", "pdf.fonttype": 42,
    })
    ASSETS.mkdir(parents=True, exist_ok=True)
    assets = []

    def save(fig, name):
        record = {"name": name, "width_pt": fig.get_figwidth() * 72, "height_pt": fig.get_figheight() * 72}
        for extension in ("svg", "pdf", "png"):
            destination = ASSETS / f"{name}.{extension}"
            metadata = {"Date": None} if extension == "svg" else {"CreationDate": None, "ModDate": None} if extension == "pdf" else None
            fig.savefig(destination, dpi=220, facecolor="white", metadata=metadata)
            if extension == "svg":
                destination.write_text("\n".join(line.rstrip() for line in destination.read_text().splitlines()) + "\n")
            record[extension] = f"assets/img/tts/{destination.name}"
            record[f"{extension}_sha256"] = digest(destination.read_bytes())
        assets.append(record)
        plt.close(fig)

    for model, label in MODELS.items():
        fig, axes = plt.subplots(2, 3, figsize=(14, 7.2))
        fig.subplots_adjust(left=.075, right=.98, bottom=.09, top=.80, hspace=.65, wspace=.30)
        fig.suptitle(label, y=.98, fontsize=18, fontweight="bold")
        legend = [Line2D([0], [0], color=COLORS[n], lw=2,
                         linestyle={1: "--", 2: "-", 4: "-."}[n], label=LABELS[n]) for n in (1, 2, 4)]
        fig.legend(handles=legend, loc="upper center", bbox_to_anchor=(.52, .935), ncol=3,
                   frameon=False, fontsize=11)
        for ax, task in zip(axes.flat, TASKS):
            panel = next(p for p in data["panels"] if p["model"] == model and p["task"] == task)
            for group in panel["groups"]:
                n = group["allocation"]
                times, scores = group["plotted_times"], group["plotted_best_scores"]
                warp = lambda time: time if time <= panel["budget"] / 2 else panel["budget"] / 2 + (time - panel["budget"] / 2) / 3
                ax.step([warp(time) for time in times], scores, where="post", lw=1.8, color=COLORS[n], linestyle={1: "--", 2: "-", 4: "-."}[n])
            ax.set_title(f"{TITLES[task]}\n{panel['stage']} · {panel['level']}", loc="left", fontsize=11, fontweight="bold", pad=12)
            ax.set_xlim(0, warp(panel["budget"]))
            ax.axvspan(panel["budget"] / 2, warp(panel["budget"]), color="#F2F5F8", zorder=0)
            ax.set_ylim(panel["limits"])
            ticks = [0, panel["budget"] / 6, panel["budget"] / 3, panel["budget"] / 2, panel["budget"]]
            ax.set_xticks([warp(tick) for tick in ticks], [f"{tick:g}" for tick in ticks])
            ax.set_xlabel("Time (hours)", fontsize=10)
            ax.set_ylabel(panel["unit"].replace(" ↑", ""), fontsize=10)
            ax.yaxis.set_major_locator(MaxNLocator(4))
            ax.tick_params(axis="both", labelsize=10, length=0, pad=7)
            ax.grid(axis="y")
        save(fig, "astra" if model == "gpt-6-astra" else "claude")
    return assets


def build(source: Path | None) -> None:
    if source:
        content = source.read_bytes()
        parser = ReportData()
        parser.feed(content.decode("utf-8"))
        data = json.loads("".join(parser.parts))
        data["source"] = {"file": source.name, "sha256": digest(content)}
        summary = summarize(data)
        DATA.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n")
    else:
        data = json.loads(DATA.read_text())
        summary = summarize(data)
    bundle = ROOT / "site/data/tts.js"
    bundle.write_text("window.INFRATHON_TTS=" + json.dumps(browser_data(data), ensure_ascii=False, separators=(",", ":")) + ";\n")
    manifest = {"source": data["source"], "source_version": data["sourceVersion"],
                "data_sha256": digest(DATA.read_bytes()), "summary": summary,
                "time_axis": "Paper layout: the first half occupies 75% of the axis, the shaded second half 25%. Tick labels are actual hours; short curves end at T/n.",
                "aggregation": "Geometric mean of short/long final-score ratios over four task–model comparisons per level.",
                "figures": render(data, summary)}
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")


def check() -> None:
    data = json.loads(DATA.read_text())
    manifest = json.loads(MANIFEST.read_text())
    assert manifest["source"] == data["source"]
    assert manifest["data_sha256"] == digest(DATA.read_bytes())
    assert manifest["summary"] == summarize(data)
    assert {f["name"] for f in manifest["figures"]} == {"astra", "claude"}
    bundle = (ROOT / "site/data/tts.js").read_text()
    assert bundle == "window.INFRATHON_TTS=" + json.dumps(browser_data(data), ensure_ascii=False, separators=(",", ":")) + ";\n"
    for figure in manifest["figures"]:
        for extension in ("svg", "pdf", "png"):
            assert digest((ROOT / "site" / figure[extension]).read_bytes()) == figure[f"{extension}_sha256"]
    print("Verified TTS: 84 runs, 12 comparisons, 36 grouped curves, the browser bundle, and two trajectory SVG/PDF/PNG figure sets.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", nargs="?", type=Path, help="Author-supplied TTS.html")
    parser.add_argument("--check", action="store_true", help="Verify data and assets without plotting dependencies")
    arguments = parser.parse_args()
    if not arguments.check:
        build(arguments.source)
    elif arguments.source:
        parser.error("--check does not import or modify source data")
    check()
