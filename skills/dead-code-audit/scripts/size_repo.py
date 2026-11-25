#!/usr/bin/env python3
"""Measure a repository and recommend a dead-code audit strategy.

Usage:
    python size_repo.py /path/to/repo [--json]

Counts source files and lines per language, skipping vendored/generated
directories, then prints a strategy recommendation:
    SMALL  (< 50k lines)             -> full one-pass scan
    MEDIUM (50k - 500k lines)        -> tool scan, targeted verification
    LARGE  (> 500k lines or > 5k files) -> chunked module-by-module scan
"""

import argparse
import json
import os
import sys

EXCLUDE_DIRS = {
    ".git", "node_modules", "vendor", "dist", "build", "out", "target",
    "venv", ".venv", "env", ".env", "__pycache__", ".mypy_cache",
    ".pytest_cache", ".tox", "coverage", ".next", ".nuxt", "bower_components",
    "third_party", "thirdparty", "externals", ".gradle", "Pods",
}

GENERATED_MARKERS = ("_pb2.py", "_pb2_grpc.py", ".generated.", ".min.js", ".min.css")

LANG_EXTS = {
    "python": {".py"},
    "javascript": {".js", ".jsx", ".mjs", ".cjs"},
    "typescript": {".ts", ".tsx"},
    "go": {".go"},
    "rust": {".rs"},
    "java": {".java"},
    "kotlin": {".kt", ".kts"},
    "ruby": {".rb"},
    "php": {".php"},
    "csharp": {".cs"},
    "c_cpp": {".c", ".h", ".cc", ".cpp", ".hpp", ".cxx"},
    "swift": {".swift"},
}

EXT_TO_LANG = {ext: lang for lang, exts in LANG_EXTS.items() for ext in exts}

SMALL_MAX_LINES = 50_000
MEDIUM_MAX_LINES = 500_000
LARGE_FILE_COUNT = 5_000


def count_lines(path):
    try:
        with open(path, "rb") as f:
            return sum(1 for _ in f)
    except OSError:
        return 0


def scan(repo):
    stats = {}          # lang -> {"files": n, "lines": n}
    top_modules = {}    # first path segment -> lines
    skipped_dirs = set()
    generated_files = 0
    total_files = 0
    total_lines = 0

    for root, dirs, files in os.walk(repo):
        kept = []
        for d in dirs:
            if d in EXCLUDE_DIRS or d.startswith("."):
                skipped_dirs.add(os.path.relpath(os.path.join(root, d), repo))
            else:
                kept.append(d)
        dirs[:] = kept

        for name in files:
            ext = os.path.splitext(name)[1].lower()
            lang = EXT_TO_LANG.get(ext)
            if not lang:
                continue
            full = os.path.join(root, name)
            if any(m in name for m in GENERATED_MARKERS):
                generated_files += 1
                continue
            lines = count_lines(full)
            entry = stats.setdefault(lang, {"files": 0, "lines": 0})
            entry["files"] += 1
            entry["lines"] += lines
            total_files += 1
            total_lines += lines

            rel = os.path.relpath(full, repo)
            top = rel.split(os.sep)[0]
            top_modules[top] = top_modules.get(top, 0) + lines

    return {
        "repo": os.path.abspath(repo),
        "total_files": total_files,
        "total_lines": total_lines,
        "languages": dict(sorted(stats.items(), key=lambda kv: -kv[1]["lines"])),
        "top_modules_by_lines": dict(
            sorted(top_modules.items(), key=lambda kv: -kv[1])[:15]
        ),
        "generated_files_skipped": generated_files,
        "excluded_dirs_found": sorted(skipped_dirs)[:25],
    }


def strategy(report):
    lines, files = report["total_lines"], report["total_files"]
    if lines > MEDIUM_MAX_LINES or files > LARGE_FILE_COUNT:
        return "LARGE", "Chunk by top-level module. Build the global symbol index first (symbol_index.py). Checkpoint findings per chunk."
    if lines > SMALL_MAX_LINES:
        return "MEDIUM", "Run language tools repo-wide. Deep-verify only high-value candidates (whole files, large functions, exported symbols)."
    return "SMALL", "Full scan: run all relevant tools across the repo in one pass and verify every finding."


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args()

    if not os.path.isdir(args.repo):
        print(f"error: {args.repo} is not a directory", file=sys.stderr)
        sys.exit(1)

    report = scan(args.repo)
    tier, advice = strategy(report)
    report["strategy"] = tier
    report["advice"] = advice

    if args.json:
        print(json.dumps(report, indent=2))
        return

    print(f"Repo: {report['repo']}")
    print(f"Source files: {report['total_files']:,}   Source lines: {report['total_lines']:,}")
    print(f"Generated files skipped: {report['generated_files_skipped']}")
    print("\nLanguages:")
    for lang, s in report["languages"].items():
        print(f"  {lang:<12} {s['files']:>6,} files  {s['lines']:>10,} lines")
    print("\nLargest top-level modules:")
    for mod, ln in report["top_modules_by_lines"].items():
        print(f"  {mod:<30} {ln:>10,} lines")
    if report["excluded_dirs_found"]:
        print("\nExcluded (vendored/build/hidden):")
        for d in report["excluded_dirs_found"]:
            print(f"  {d}")
    print(f"\nSTRATEGY: {tier}")
    print(f"  {advice}")


if __name__ == "__main__":
    main()
