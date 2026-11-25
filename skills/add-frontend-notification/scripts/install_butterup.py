#!/usr/bin/env python3
"""Copy the bundled Butterup assets into a project directory."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


ASSET_NAMES = ("butterup.js", "butterup.css")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Copy add-frontend-notification's exact bundled Butterup assets."
    )
    parser.add_argument("target", type=Path, help="Destination directory in the project")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files with the same names",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    assets_dir = Path(__file__).resolve().parent.parent / "assets"
    target_dir = args.target.resolve()

    missing = [name for name in ASSET_NAMES if not (assets_dir / name).is_file()]
    if missing:
        raise SystemExit(f"Missing bundled assets: {', '.join(missing)}")

    existing = [name for name in ASSET_NAMES if (target_dir / name).exists()]
    if existing and not args.force:
        raise SystemExit(
            "Refusing to overwrite existing files: "
            f"{', '.join(existing)}. Re-run with --force after confirming replacement."
        )

    target_dir.mkdir(parents=True, exist_ok=True)
    for name in ASSET_NAMES:
        shutil.copy2(assets_dir / name, target_dir / name)
        print(f"Copied {name} -> {target_dir / name}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
