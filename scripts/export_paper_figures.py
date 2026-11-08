#!/usr/bin/env python3
"""Export the latest manuscript figures and verify the committed assets."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import xml.etree.ElementTree as element_tree
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "site/assets/img/paper"
MANIFEST = ROOT / "data/paper_figures.json"
FIGURES = {
    "framework": "ultrainfrabench_framework",
    "taskstat": "taskstat",
    "task_trajectories": "task_trajectories",
    "rank_performance": "rank_performance",
    "qvg_submission_comparison": "qvg_submission_comparison",
    "analysis_summary": "analysis_summary",
    "long_vs_short_runs": "long_vs_short_runs",
    "behavior_task_fidelity": "behavior_task_fidelity",
    "appendix_task_trajectories_1": "appendix_task_trajectories_1",
    "appendix_task_trajectories_2": "appendix_task_trajectories_2",
}
PREVIEWS = {
    "opcd": (326, 24, 160, 129),
    "sageattention": (0, 279, 164, 127),
    "qvg": (164, 405, 161, 135),
    "legend": (0, 0, 486, 24),
}


def digest(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def export(source: Path) -> None:
    manuscript = (source / "main.tex").read_bytes()
    ASSETS.mkdir(parents=True, exist_ok=True)
    manifest = {
        "source_tex": "main.tex",
        "source_tex_sha256": digest(manuscript),
        "method": "Original one-page manuscript PDFs, converted with pdftocairo -svg. Text remains vector outlines; embedded image content, colors, and geometry are retained.",
        "figures": [],
        "previews": [],
    }
    for name, member in FIGURES.items():
        original = source / "images" / f"{member}.pdf"
        pdf = ASSETS / f"{name}.pdf"
        svg = ASSETS / f"{name}.svg"
        pdf.write_bytes(original.read_bytes())
        subprocess.run(["pdftocairo", "-svg", str(pdf), str(svg)], check=True)
        attributes = element_tree.parse(svg).getroot().attrib
        manifest["figures"].append({
            "name": name, "source_member": f"images/{member}.pdf",
            "pdf": f"assets/img/paper/{name}.pdf",
            "svg": f"assets/img/paper/{name}.svg",
            "pdf_sha256": digest(pdf.read_bytes()),
            "svg_sha256": digest(svg.read_bytes()),
            "width_pt": float(attributes["viewBox"].split()[2]),
            "height_pt": float(attributes["viewBox"].split()[3]),
        })
    element_tree.register_namespace("", "http://www.w3.org/2000/svg")
    element_tree.register_namespace("xlink", "http://www.w3.org/1999/xlink")
    for task, rectangle in PREVIEWS.items():
        document = element_tree.parse(ASSETS / "task_trajectories.svg")
        artwork = document.getroot()
        artwork.set("viewBox", " ".join(str(value) for value in rectangle))
        artwork.set("width", f"{rectangle[2]}pt")
        artwork.set("height", f"{rectangle[3]}pt")
        destination = ASSETS / f"preview-{task}.svg"
        document.write(destination, encoding="utf-8", xml_declaration=True)
        manifest["previews"].append({
            "task": task, "source": "assets/img/paper/task_trajectories.svg",
            "view_box": list(rectangle),
            "svg": f"assets/img/paper/preview-{task}.svg",
            "svg_sha256": digest(destination.read_bytes()),
        })
    if digest((source / "main.tex").read_bytes()) != manifest["source_tex_sha256"]:
        raise RuntimeError("The manuscript changed during export; rerun with the current source.")
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n")


def check() -> None:
    manifest = json.loads(MANIFEST.read_text())
    assert {figure["name"] for figure in manifest["figures"]} == set(FIGURES)
    assert {preview["task"] for preview in manifest["previews"]} == set(PREVIEWS)
    for figure in manifest["figures"]:
        for extension in ("pdf", "svg"):
            content = (ROOT / "site" / figure[extension]).read_bytes()
            assert digest(content) == figure[f"{extension}_sha256"], figure[extension]
    for preview in manifest["previews"]:
        content = (ROOT / "site" / preview["svg"]).read_bytes()
        assert digest(content) == preview["svg_sha256"], preview["svg"]
        attributes = element_tree.fromstring(content).attrib
        assert [float(value) for value in attributes["viewBox"].split()] == preview["view_box"]
    print("Verified latest manuscript figures: 10 original PDFs, 10 SVGs, and four vector preview crops.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", nargs="?", type=Path)
    parser.add_argument("--check", action="store_true")
    arguments = parser.parse_args()
    if arguments.source:
        export(arguments.source)
    elif not arguments.check:
        parser.error("provide the Overleaf directory or --check")
    check()
