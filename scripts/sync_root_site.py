#!/usr/bin/env python3
"""Mirror the site/ frontend at the repository root for branch-based Pages."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = Path("data/root_site_files.json")


def sync(root: Path, *, check: bool = False) -> list[str]:
    source = root / "site"
    files = sorted(path.relative_to(source).as_posix()
                   for path in source.rglob("*") if path.is_file())
    if "index.html" not in files:
        raise ValueError("site/index.html is required.")
    manifest = root / MANIFEST
    previous = json.loads(manifest.read_text()) if manifest.exists() else []
    if not isinstance(previous, list) or any(
        not isinstance(name, str) or Path(name).is_absolute() or ".." in Path(name).parts
        or name.startswith("site/") or name == MANIFEST.as_posix() for name in previous
    ):
        raise ValueError("Invalid managed-file manifest.")
    errors = []
    if check:
        if previous != files:
            errors.append("The published-file manifest is out of date.")
        for name in files:
            target = root / name
            if not target.is_file() or target.read_bytes() != (source / name).read_bytes():
                errors.append(f"Root publication is out of date: {name}")
        return errors
    for name in files:
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source / name, target)
    for name in set(previous) - set(files):
        target = root / name
        if target.is_file():
            target.unlink()
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(json.dumps(files, indent=2) + "\n")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify committed root files without changing them.")
    args = parser.parse_args()
    errors = sync(ROOT, check=args.check)
    if errors:
        raise SystemExit("\n".join(errors) + "\nRun python3 scripts/sync_root_site.py after editing site/.")
    print("Root homepage and legacy /site/ content are synchronized.")


if __name__ == "__main__":
    main()
