#!/usr/bin/env python3
"""Import quality-weighted QVG scores from the author-provided HTML report.

The report prints scores and elapsed hours to two decimal places. Keep the
original dashboard timestamps and statuses, and check every row against that
archive before exporting a separate score update. The archive is not rewritten.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ScoreTables(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tables = []
        self.heading = ""
        self.summary = None
        self.table = None
        self.row = None
        self.cell = None

    def handle_starttag(self, tag, attrs):
        if tag == "summary":
            self.summary = []
        elif tag == "table":
            self.table = []
            self.tables.append((self.heading, self.table))
        elif tag == "tr":
            self.row = []
        elif tag in ("td", "th"):
            self.cell = []

    def handle_data(self, text):
        if self.summary is not None:
            self.summary.append(text)
        if self.cell is not None:
            self.cell.append(text)

    def handle_endtag(self, tag):
        if tag == "summary" and self.summary is not None:
            self.heading = "".join(self.summary).strip()
            self.summary = None
        elif tag in ("td", "th") and self.cell is not None:
            self.row.append("".join(self.cell).strip())
            self.cell = None
        elif tag == "tr" and self.row is not None:
            self.table.append(self.row)
            self.row = None


def rescore_run(run: dict, update: dict) -> dict:
    """Match report rows to original submissions and replace only their scores."""
    if run["id"] != update["id"] or len(run["points"]) != len(update["rows"]):
        raise ValueError(f"QVG run identity or submission count changed: {run['model']}")
    points = []
    for index, (point, row) in enumerate(zip(run["points"], update["rows"]), 1):
        number, hour, old_score, new_score, valid = row
        if number != index or abs(hour - point[0]) > .0051:
            raise ValueError(f"QVG submission identity/time mismatch: {run['model']} agent-{index}")
        if valid != (point[2] == "valid") or abs(old_score - (point[1] or 0)) > .0051:
            raise ValueError(f"QVG original score/status mismatch: {run['model']} agent-{index}")
        if not math.isfinite(new_score) or new_score < 0 or (not valid and new_score != 0):
            raise ValueError(f"Invalid quality-weighted QVG score: {run['model']} agent-{index}")
        points.append([point[0], new_score if valid else None, point[2]])
    return {**run, "points": points}


def extract(source: Path) -> dict:
    html = source.read_text(encoding="utf-8")
    parser = ScoreTables()
    parser.feed(html)
    registry = json.loads((ROOT / "data/tasks.json").read_text())
    originals = json.loads((ROOT / "data/raw/runs.json").read_text())["tasks"]["qvg"]["runs"]
    runs = {}
    for heading, table in parser.tables:
        if not table or table[0][:5] != ["提交", "时刻 (h)", "结果", "现有分数", "新分数"]:
            continue
        matches = [model for model in registry["models"] if heading.startswith(model["name"])]
        if len(matches) != 1:
            raise ValueError(f"Unrecognized QVG model heading: {heading}")
        key = matches[0]["key"]
        if key in runs or originals[key]["id"] not in html:
            raise ValueError(f"Duplicate or unidentified QVG run: {key}")
        rows = []
        for row in table[1:]:
            if row[2] not in ("有效", "没过线", "崩溃或缺指标"):
                raise ValueError(f"Unrecognized QVG status: {row[2]}")
            rows.append([int(row[0].removeprefix("agent-")), float(row[1]),
                         float(row[3]), float(row[4]), row[2] == "有效"])
        runs[key] = {"id": originals[key]["id"], "rows": rows}
        rescore_run(originals[key], runs[key])
    if set(runs) != set(originals):
        raise ValueError("QVG score update must cover all six original runs")
    return {
        "source": {
            "file": source.name,
            "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "method": "Post-hoc quality-weighted scores from the author-provided HTML tables; original dashboard timestamps and validity statuses retained.",
            "score_decimals": 2,
            "reference_score": 6.82,
            "formula": "sqrt(R_LongCat * (1 + q_LongCat) * R_HY * (1 + q_HY))",
            "paper": "Quant-VideoGen KV Codec: eq:qvg_task_score and app:qvg_quality_score",
        },
        "columns": ["submission", "elapsed_h_rounded", "compression_score", "quality_weighted_score", "valid"],
        "runs": runs,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("-o", "--out", type=Path, default=ROOT / "data/qvg_scores.json")
    args = parser.parse_args()
    data = extract(args.source)
    args.out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    for model, run in data["runs"].items():
        print(f"{model}: {len(run['rows'])} submissions, best score {max(row[3] for row in run['rows']):.2f}")


if __name__ == "__main__":
    main()
