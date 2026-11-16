#!/usr/bin/env python3
"""Render the native run-overview SVG animation as a social-post MP4."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "site/assets/img/homepage/run-overview.svg"
OUTPUT = ROOT / "site/assets/img/twitter/run-overview.mp4"
MANIFEST = ROOT / "data/run_overview_video.json"
WIDTH, HEIGHT, FPS, DURATION = 1920, 1052, 30, 15


def find_ffmpeg(explicit: str | None) -> str:
    if explicit:
        return explicit
    if executable := shutil.which("ffmpeg"):
        return executable
    try:
        import imageio_ffmpeg
    except ImportError as error:
        raise SystemExit("Install FFmpeg or imageio-ffmpeg, or pass --ffmpeg.") from error
    return imageio_ffmpeg.get_ffmpeg_exe()


def export(ffmpeg: str) -> None:
    from playwright.sync_api import sync_playwright

    source_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    arguments = [
        "-hide_banner", "-loglevel", "error", "-y",
        "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "png", "-i", "pipe:0",
        "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
        "-map", "0:v:0", "-map", "1:a:0", "-vf", "setsar=1",
        "-c:v", "libx264", "-preset", "slow", "-crf", "18",
        "-profile:v", "high", "-level:v", "4.1", "-pix_fmt", "yuv420p",
        "-maxrate", "8M", "-bufsize", "16M", "-g", "60",
        "-c:a", "aac", "-b:a", "64k", "-t", str(DURATION),
        "-movflags", "+faststart", str(OUTPUT),
    ]
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
        try:
            page = browser.new_page(
                viewport={"width": WIDTH, "height": HEIGHT}, device_scale_factor=1,
            )
            page.goto(SOURCE.as_uri(), wait_until="load")
            page.evaluate("document.fonts.ready")
            animation_count = page.evaluate("""({width, height, duration}) => {
                const svg = document.documentElement;
                svg.style.width = width + 'px';
                svg.style.height = height + 'px';
                window.exportAnimations = document.getAnimations();
                if (!window.exportAnimations.length || window.exportAnimations.some(
                    animation => animation.effect.getTiming().duration !== duration * 1000
                )) throw new Error('Review the source animation duration before exporting.');
                for (const animation of window.exportAnimations) {
                    animation.pause();
                    animation.currentTime = 0;
                }
                return window.exportAnimations.length;
            }""", {"width": WIDTH, "height": HEIGHT, "duration": DURATION})
            with subprocess.Popen([ffmpeg, *arguments], stdin=subprocess.PIPE) as encoder:
                assert encoder.stdin is not None
                for frame in range(FPS * DURATION):
                    page.evaluate("""time => {
                        for (const animation of window.exportAnimations)
                            animation.currentTime = time;
                    }""", frame * 1000 / FPS)
                    encoder.stdin.write(page.screenshot(type="png", animations="allow"))
                    if (frame + 1) % 60 == 0 or frame + 1 == FPS * DURATION:
                        print(f"Rendered {frame + 1}/{FPS * DURATION} frames.", flush=True)
            if encoder.returncode:
                raise RuntimeError(f"FFmpeg exited with status {encoder.returncode}.")
        finally:
            browser.close()
    if hashlib.sha256(SOURCE.read_bytes()).hexdigest() != source_hash:
        raise RuntimeError("Source SVG changed during export; rerun with the latest file.")
    manifest = {
        "file": OUTPUT.relative_to(ROOT / "site").as_posix(),
        "sha256": hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
        "bytes": OUTPUT.stat().st_size,
        "duration_seconds": DURATION,
        "width": WIDTH, "height": HEIGHT,
        "frames_per_second": FPS, "frames": FPS * DURATION,
        "video_codec": "H.264 High, yuv420p",
        "audio_codec": "AAC, 48 kHz stereo, silent",
        "source_file": SOURCE.relative_to(ROOT).as_posix(),
        "source_sha256": source_hash,
        "source_animation_count": animation_count,
        "export_script": Path(__file__).relative_to(ROOT).as_posix(),
        "method": "Pause the SVG's native CSS animations in Chromium and render each frame at its exact 30 fps timestamp. Encode one complete 15-second cycle without screen-recording frame drops or GIF conversion.",
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(f"Exported {OUTPUT.relative_to(ROOT)} ({OUTPUT.stat().st_size:,} bytes).")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ffmpeg", help="Path to FFmpeg; defaults to PATH or imageio-ffmpeg.")
    export(find_ffmpeg(parser.parse_args().ffmpeg))
