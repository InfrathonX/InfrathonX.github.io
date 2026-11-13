#!/usr/bin/env python3
"""Extract the author's Twitter figures, export uploadable PNGs, and write Markdown."""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import math
from pathlib import Path
import struct
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
ASSETS = SITE / "assets/img/twitter"
MANIFEST = ROOT / "data/twitter_assets.json"
SOCIAL_AUTHORS = ROOT / "data/author_social_accounts.json"
ORIGINAL_THANKS = "Huge thanks to all our collaborators and the human experts who helped build Infrathon!"
OLD_SUPPORT_REQUEST = " If you find this work useful, please consider starring the repository and citing our paper."
HUGGING_FACE_SUPPORT = (
    "If you find Infrathon interesting, we’d appreciate an upvote on Hugging Face Daily Papers "
    "to help more people discover the work!\n\n"
    "<https://huggingface.co/papers/2611.11995>"
)
RAW = "https://raw.githubusercontent.com/InfrathonX/InfrathonX.github.io/main/"
FIGURES = [
    ("task-categories", "[2/7]", "Task categories"),
    ("framework", "[3/7]", "Infrathon framework"),
    ("model-rankings", "[4/7]", "Model rankings"),
    ("knowledge-discovery", "[5/7]", "Codec comparison and optimization trajectory"),
    ("long-vs-short", "[6/7]", "Long vs. short horizons"),
]
TABLES = [("knowledge-discovery-metrics", "[5/7]", "Compression and video quality"),
          ("horizon-comparison", "[6/7]", "Long- vs. short-run performance ratios")]


def digest(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def author_acknowledgment(platform: str) -> str:
    """Render all paper authors, adding only verified platform-specific accounts."""
    if platform not in ("x", "linkedin"):
        raise ValueError(f"Unknown social platform: {platform}")
    authors = json.loads(SOCIAL_AUTHORS.read_text())["authors"]
    labels = []
    for author in authors:
        name, account = author["name"], author[platform]
        if account is None:
            labels.append(name)
        elif platform == "x":
            labels.append(f'{name} ([@{account["handle"]}]({account["url"]}))')
        else:
            labels.append(f'[@{name}]({account["url"]})')
    names = ", ".join(labels[:-1]) + ", and " + labels[-1]
    return ("Huge thanks to the entire Infrathon author team: " + names + "!\n\n"
            "Thanks also to the human experts who helped build Infrathon!")


def png_info(path: Path) -> dict:
    content = path.read_bytes()
    if content[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"Not a PNG: {path}")
    width, height = struct.unpack(">II", content[16:24])
    if len(content) >= 5_000_000:
        raise ValueError(f"PNG exceeds the 5 MB upload target: {path}")
    return {"file": path.relative_to(SITE).as_posix(), "width": width, "height": height,
            "bytes": len(content), "sha256": digest(content)}


def export(source: Path) -> None:
    from bs4 import BeautifulSoup
    from markdownify import markdownify
    from PIL import Image
    from playwright.sync_api import sync_playwright

    content = source.read_bytes()
    soup = BeautifulSoup(content.decode("utf-8"), "html.parser")
    figures = soup.main.find_all("figure", recursive=False)
    tables = soup.main.select(".table-wrap table")
    headings = soup.main.find_all("h2", recursive=False)
    if len(figures) != 5 or len(tables) != 2 or len(headings) != 8:
        raise ValueError("Expected five figures, two tables, and eight posts in the author HTML.")
    original_directory = ASSETS / "sources"
    original_directory.mkdir(parents=True, exist_ok=True)
    manifest = {"source_file": source.name, "source_sha256": digest(content),
                "method": "Original embedded figures extracted without modification; SVGs rendered at 4x with Chromium on white, WebP decoded losslessly to PNG; original HTML tables captured at 2x.",
                "assets": [], "posts": []}

    def optimize(path: Path) -> None:
        with Image.open(path) as image:
            rgba = image.convert("RGBA")
            white = Image.new("RGBA", rgba.size, "white")
            white.alpha_composite(rgba)
            white.convert("RGB").save(path, optimize=True, compress_level=9)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_page()
        for figure, (name, post, alt) in zip(figures, FIGURES):
            image = figure.find("img")
            uri = image["src"]
            header, encoded = uri.split(",", 1)
            original = base64.b64decode(encoded, validate=True)
            extension = "svg" if header == "data:image/svg+xml;base64" else "webp"
            if header not in ("data:image/svg+xml;base64", "data:image/webp;base64"):
                raise ValueError(f"Unexpected image type: {header}")
            original_path = original_directory / f"{name}.{extension}"
            original_path.write_bytes(original)
            png_path = ASSETS / f"{name}.png"
            if extension == "svg":
                box = [float(number) for number in ET.fromstring(original).attrib["viewBox"].split()]
                width, height = math.ceil(box[2] * 4), math.ceil(box[3] * 4)
                page.set_viewport_size({"width": width, "height": height})
                page.set_content('<style>html,body{margin:0;width:100%;height:100%;background:white}img{display:block;width:100%;height:100%;object-fit:contain}</style><img src="' + uri + '">')
                page.locator("img").evaluate("(image) => image.decode()")
                page.screenshot(path=str(png_path))
            else:
                with Image.open(original_path) as image_data:
                    image_data.save(png_path)
            optimize(png_path)
            manifest["assets"].append({"key": name, "post": post, "kind": "original-figure",
                                       "alt": alt, "png": png_info(png_path),
                                       "original": {"file": original_path.relative_to(SITE).as_posix(),
                                                    "sha256": digest(original)}})
        page.close()
        table_page = browser.new_page(viewport={"width": 1200, "height": 1000}, device_scale_factor=2)
        table_page.goto(source.resolve().as_uri(), wait_until="load")
        table_page.evaluate("document.fonts.ready")
        for index, (name, post, alt) in enumerate(TABLES):
            png_path = ASSETS / f"{name}.png"
            table_page.locator(".table-wrap table").nth(index).screenshot(path=str(png_path))
            optimize(png_path)
            cells = [[cell.get_text(" ", strip=True) for cell in row.find_all(["th", "td"])]
                     for row in tables[index].find_all("tr")]
            manifest["assets"].append({"key": name, "post": post, "kind": "table-screenshot",
                                       "alt": alt, "png": png_info(png_path), "cells": cells})
        browser.close()

    def url(asset: dict) -> str:
        return RAW + asset["png"]["file"]

    archive = ASSETS / "infrathon-twitter-images.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
        for item in manifest["assets"]:
            image_path = SITE / item["png"]["file"]
            member = zipfile.ZipInfo(image_path.name, date_time=(2000, 1, 1, 0, 0, 0))
            member.compress_type = zipfile.ZIP_DEFLATED
            bundle.writestr(member, image_path.read_bytes())
    manifest["archive"] = {"file": archive.relative_to(SITE).as_posix(),
                           "sha256": digest(archive.read_bytes())}
    lines = ["# Infrathon Twitter Thread", "",
             "This file preserves the opening post and seven replies from `twitter.html`, including the original research wording, lists, and tables. The closing post adds all 21 authors and their verified X handles; see [author accounts](author-social-accounts.md).",
             "Attachment notes and download links after each post are publishing instructions. Download the PNGs and attach them as media when posting on X.",
             "Most posts exceed the standard 280-character limit. This file preserves the complete long-form draft without splitting posts. [Posting on X](https://help.x.com/en/using-x/how-to-post).", "",
             "## Image downloads", "", f'[Download all PNGs (ZIP)]({RAW}{manifest["archive"]["file"]})', "",
             "| Post | Attachment | PNG |", "| --- | --- | --- |"]
    for item in manifest["assets"]:
        lines.append(f'| {item["post"]} | {item["alt"]} | [Download]({url(item)}) |')
    lines += ["", "Posts [5/7] and [6/7] each include a table PNG that can replace the Markdown table when posting.",
              "All PNGs are smaller than 5 MB. [X image upload guidance](https://help.x.com/en/using-x/posting-gifs-and-pictures).", "", "---", ""]
    for index, heading in enumerate(headings):
        post = "Opening post" if index == 0 else heading.get_text(" ", strip=True)
        nodes = []
        for sibling in heading.next_siblings:
            if getattr(sibling, "name", None) in ("hr", "h2"):
                break
            if getattr(sibling, "name", None) and sibling.name != "figure":
                nodes.append(sibling)
        article = "\n\n".join(markdownify(str(node), heading_style="ATX", bullets="-", escape_underscores=False).strip()
                               for node in nodes)
        if index == len(headings) - 1:
            if ORIGINAL_THANKS not in article:
                raise ValueError("The source closing acknowledgment changed; review the author credits before exporting.")
            article = article.replace(ORIGINAL_THANKS, author_acknowledgment("x"))
            article = article.replace(OLD_SUPPORT_REQUEST, "") + "\n\n" + HUGGING_FACE_SUPPORT
        lines += [f"## {post}", "", article, ""]
        attached = [item for item in manifest["assets"] if item["post"] == post]
        if attached:
            lines.append("> Media attachments (not part of the post text): " + " · ".join(f'[{item["alt"]} PNG]({url(item)})' for item in attached))
            lines.append("")
            for item in attached:
                if item["kind"] == "original-figure":
                    lines += [f'![{item["alt"]}]({url(item)})', ""]
        lines += ["---", ""]
        plain = "\n\n".join(node.get_text(" ", strip=True) for node in nodes)
        manifest["posts"].append({"heading": post, "source_text_sha256": digest(plain.encode()),
                                  "unicode_characters": len(plain), "attachment_keys": [item["key"] for item in attached]})
    markdown = "\n".join(lines).rstrip() + "\n"
    if "data:image" in markdown:
        raise ValueError("Markdown still contains an embedded data URL.")
    destination = SITE / "twitter-thread.md"
    destination.write_text(markdown, encoding="utf-8")
    manifest["markdown"] = {"file": "twitter-thread.md", "sha256": digest(markdown.encode())}
    manifest["acknowledgments"] = {"authors_file": SOCIAL_AUTHORS.relative_to(ROOT).as_posix(),
                                    "sha256": digest(SOCIAL_AUTHORS.read_bytes())}
    if digest(source.read_bytes()) != manifest["source_sha256"]:
        raise ValueError("The source HTML changed during export; rerun with the latest file.")
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    check()


def check() -> None:
    manifest = json.loads(MANIFEST.read_text())
    assert len(manifest["assets"]) == 7
    assert [post["heading"] for post in manifest["posts"]] == ["Opening post"] + [f"[{i}/7]" for i in range(1, 8)]
    for item in manifest["assets"]:
        assert png_info(SITE / item["png"]["file"]) == item["png"], item["key"]
        if "original" in item:
            assert digest((SITE / item["original"]["file"]).read_bytes()) == item["original"]["sha256"]
    markdown = (SITE / manifest["markdown"]["file"]).read_bytes()
    assert digest(markdown) == manifest["markdown"]["sha256"]
    assert manifest["acknowledgments"]["sha256"] == digest(SOCIAL_AUTHORS.read_bytes())
    assert author_acknowledgment("x") in markdown.decode("utf-8")
    assert HUGGING_FACE_SUPPORT in markdown.decode("utf-8")
    assert b"data:image" not in markdown
    assert not any("\u3400" <= char <= "\u9fff" or "\uf900" <= char <= "\ufaff" for char in markdown.decode("utf-8")), "Markdown must be in English."
    for item in manifest["assets"]:
        assert (RAW + item["png"]["file"]).encode() in markdown
    archive = SITE / manifest["archive"]["file"]
    assert digest(archive.read_bytes()) == manifest["archive"]["sha256"]
    with zipfile.ZipFile(archive) as bundle:
        assert sorted(bundle.namelist()) == sorted(Path(item["png"]["file"]).name for item in manifest["assets"])
        for item in manifest["assets"]:
            assert digest(bundle.read(Path(item["png"]["file"]).name)) == item["png"]["sha256"]
    print("Verified Twitter package: 5 original figures, 2 table PNGs, and 8 Markdown posts.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", nargs="?", type=Path, help="The author's standalone twitter.html.")
    parser.add_argument("--check", action="store_true", help="Verify committed assets without the source HTML or rendering dependencies.")
    args = parser.parse_args()
    if args.source:
        export(args.source)
    elif args.check:
        check()
    else:
        parser.error("provide the source HTML or --check")
