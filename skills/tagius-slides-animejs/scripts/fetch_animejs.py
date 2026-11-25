#!/usr/bin/env python3
"""
Vendor anime.js v4 into the skill's `assets/vendor/` so the build output
is fully offline.

Default source: jsDelivr's `animejs@4` ESM bundle. Cached to
`<skill>/assets/vendor/anime.esm.min.js` with a `version.json` sidecar.
`scripts/build.py` copies this file into every built `presentation/` bundle.

The script is idempotent — repeat runs are no-ops unless --force is given.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import sys
import urllib.request
from pathlib import Path

# Pin to the v4 major. jsDelivr resolves the tag at fetch time; we record the
# resolved URL and SHA-256 into version.json for reproducibility.
DEFAULT_URL = "https://cdn.jsdelivr.net/npm/animejs@4/lib/anime.esm.min.js"
DEFAULT_FALLBACK_URLS = [
    "https://esm.sh/animejs@4?bundle",
    "https://unpkg.com/animejs@4/lib/anime.esm.min.js",
]

SKILL_ROOT = Path(__file__).resolve().parent.parent
VENDOR_DIR = SKILL_ROOT / "assets" / "vendor"
BUNDLE_PATH = VENDOR_DIR / "anime.esm.min.js"
VERSION_PATH = VENDOR_DIR / "version.json"


def fetch(url: str, timeout: int = 30) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "slides-animejs/0.1"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def try_sources(urls: list[str]) -> tuple[str, bytes]:
    last_err: Exception | None = None
    for url in urls:
        try:
            data = fetch(url)
            if data:
                return url, data
        except Exception as exc:
            last_err = exc
            print(f"  fetch failed: {url} ({exc})", file=sys.stderr)
    raise RuntimeError(f"all sources failed; last error: {last_err}")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Vendor anime.js v4 for slides-animejs.")
    parser.add_argument("--force", action="store_true", help="Re-download even if vendored already.")
    parser.add_argument(
        "--url",
        default=DEFAULT_URL,
        help=f"Primary source URL (default: {DEFAULT_URL}).",
    )
    args = parser.parse_args(argv)

    VENDOR_DIR.mkdir(parents=True, exist_ok=True)

    if BUNDLE_PATH.exists() and not args.force:
        size = BUNDLE_PATH.stat().st_size
        print(f"  already vendored: {BUNDLE_PATH} ({size} bytes). Use --force to refresh.")
        return 0

    sources = [args.url] + [u for u in DEFAULT_FALLBACK_URLS if u != args.url]
    print(f"  fetching anime.js v4 from {sources[0]} …")
    resolved_url, data = try_sources(sources)

    BUNDLE_PATH.write_bytes(data)
    sha = hashlib.sha256(data).hexdigest()
    VERSION_PATH.write_text(
        json.dumps(
            {
                "source": resolved_url,
                "bytes": len(data),
                "sha256": sha,
                "fetched_at": dt.datetime.utcnow().isoformat() + "Z",
                "package": "animejs@4",
            },
            indent=2,
        )
        + "\n"
    )
    print(f"  wrote {BUNDLE_PATH} ({len(data)} bytes, sha256 {sha[:12]}…)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
