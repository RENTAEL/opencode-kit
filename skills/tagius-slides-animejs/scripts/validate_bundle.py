#!/usr/bin/env python3
"""
Post-build validator for a slides-animejs bundle.

Checks (all blocking unless noted):
  1. `index.html`, `run.py`, `assets/`, and `slides/` exist.
  2. `assets/anime.esm.min.js` exists and is non-empty.
  3. `assets/overlay.js`, `assets/overlay.css`, `assets/slides.css` exist.
  4. `index.html` contains a `window.__SLIDES__ = [...]` array whose length
     matches the number of `slides/slide-XX.html` files.
  5. Every `slide-XX.html`:
       - resolves all `<img src="...">` paths under `presentation/`
         (or against `assets/visuals/`);
       - uses only allowed `data-anim-from` values: up, down, left, right,
         scale, fade. Slides without `data-anim-from` are fine (default: up).
       - if it declares `window.__slideTL[N] = ...`, N matches the slide
         index (1-based file number minus 1).
  6. (Warning) `backup.pdf` is present (phase-10 PDF).

Exit 0 on success. Non-zero with a structured issue list on failure.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ALLOWED_ANIM_FROM = {"up", "down", "left", "right", "scale", "fade"}

SLIDES_RE = re.compile(r"window\.__SLIDES__\s*=\s*(\[.*?\])\s*;", re.DOTALL)
ANIM_FROM_RE = re.compile(r'data-anim-from\s*=\s*"([^"]+)"')
IMG_SRC_RE = re.compile(r'<img\b[^>]*\bsrc\s*=\s*"([^"]+)"', re.IGNORECASE)
SLIDE_TL_RE = re.compile(r"window\.__slideTL\s*\[\s*(\d+)\s*\]\s*=")


def issue(issues: list[str], slide: Path | None, msg: str) -> None:
    where = f"{slide.name}: " if slide is not None else ""
    issues.append(f"{where}{msg}")


def resolves(bundle: Path, slide: Path, src: str) -> bool:
    if src.startswith(("http://", "https://", "data:")):
        return True  # external; not our problem
    # Resolve relative to the slide file first, then relative to bundle root.
    candidates = [
        (slide.parent / src).resolve(),
        (bundle / src.lstrip("/")).resolve(),
    ]
    return any(c.exists() for c in candidates)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Validate the slides-animejs bundle.")
    parser.add_argument("--bundle", default="presentation", help="Path to the bundle directory.")
    args = parser.parse_args(argv)

    bundle = Path(args.bundle).resolve()
    issues: list[str] = []
    warnings: list[str] = []

    if not bundle.exists():
        print(f"error: bundle directory {bundle} does not exist", file=sys.stderr)
        return 2

    must_have = [
        bundle / "index.html",
        bundle / "run.py",
        bundle / "assets" / "anime.esm.min.js",
        bundle / "assets" / "overlay.js",
        bundle / "assets" / "overlay.css",
        bundle / "assets" / "slides.css",
        bundle / "slides",
    ]
    for path in must_have:
        if not path.exists():
            issue(issues, None, f"missing: {path.relative_to(bundle)}")

    anime_bundle = bundle / "assets" / "anime.esm.min.js"
    if anime_bundle.exists() and anime_bundle.stat().st_size < 1024:
        issue(issues, None, f"{anime_bundle.relative_to(bundle)} suspiciously small")

    if not (bundle / "backup.pdf").exists():
        warnings.append("backup.pdf missing (phase-10 PDF backup not produced)")

    # Read slide manifest from index.html.
    slide_files = sorted((bundle / "slides").glob("slide-*.html")) if (bundle / "slides").exists() else []
    expected = len(slide_files)

    if (bundle / "index.html").exists():
        idx_html = (bundle / "index.html").read_text(encoding="utf-8")
        m = SLIDES_RE.search(idx_html)
        if not m:
            issue(issues, None, "index.html missing window.__SLIDES__ = [...] declaration")
        else:
            try:
                manifest = json.loads(m.group(1))
            except json.JSONDecodeError as e:
                issue(issues, None, f"window.__SLIDES__ is not valid JSON: {e}")
                manifest = []
            if len(manifest) != expected:
                issue(
                    issues,
                    None,
                    f"manifest length {len(manifest)} != slide-file count {expected}",
                )

    # Per-slide checks.
    for i, slide in enumerate(slide_files):
        text = slide.read_text(encoding="utf-8")
        for variant in ANIM_FROM_RE.findall(text):
            if variant not in ALLOWED_ANIM_FROM:
                issue(issues, slide, f"data-anim-from='{variant}' not in {sorted(ALLOWED_ANIM_FROM)}")
        for src in IMG_SRC_RE.findall(text):
            if not resolves(bundle, slide, src):
                issue(issues, slide, f"<img src> does not resolve: {src}")
        for n_str in SLIDE_TL_RE.findall(text):
            n = int(n_str)
            if n != i:
                issue(issues, slide, f"window.__slideTL[{n}] declared in slide-{i+1:02d} (expected index {i})")

    # Report.
    if warnings:
        print("warnings:")
        for w in warnings:
            print(f"  - {w}")
    if issues:
        print(f"validation failed with {len(issues)} issue(s):", file=sys.stderr)
        for it in issues:
            print(f"  - {it}", file=sys.stderr)
        return 1

    print(f"validation OK ({expected} slides).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
