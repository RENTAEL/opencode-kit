#!/usr/bin/env python3
"""Build a cheap global symbol index for large-repo dead code audits.

Usage:
    python symbol_index.py /path/to/repo --out index.json
    python symbol_index.py /path/to/repo --lookup my_function

Definitions are extracted with lightweight regexes (fast, good enough for a
reference-existence check; the per-chunk tools do the precise work). The index
maps symbol name -> list of files that define it, plus a reverse helper to
count textual references across the repo.

Why this exists: when auditing a huge repo chunk by chunk, a symbol defined in
chunk A may only be used in chunk B. Verifying candidates against this global
index prevents that false positive without re-scanning the world per chunk.
"""

import argparse
import json
import os
import re
import subprocess
import sys

EXCLUDE_DIRS = {
    ".git", "node_modules", "vendor", "dist", "build", "out", "target",
    "venv", ".venv", "__pycache__", ".mypy_cache", ".pytest_cache",
    "third_party", "Pods",
}

# lang -> (extensions, definition regex)
DEF_PATTERNS = {
    "python": ({".py"}, re.compile(r"^\s*(?:def|class)\s+([A-Za-z_]\w*)", re.M)),
    "js_ts": (
        {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"},
        re.compile(
            r"^\s*(?:export\s+)?(?:default\s+)?(?:async\s+)?"
            r"(?:function|class)\s+([A-Za-z_$][\w$]*)"
            r"|^\s*(?:export\s+)?(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=",
            re.M,
        ),
    ),
    "go": ({".go"}, re.compile(r"^\s*func\s+(?:\([^)]*\)\s*)?([A-Za-z_]\w*)|^\s*type\s+([A-Za-z_]\w*)", re.M)),
    "rust": ({".rs"}, re.compile(r"^\s*(?:pub\s+)?(?:fn|struct|enum|trait)\s+([A-Za-z_]\w*)", re.M)),
    "java_kt": ({".java", ".kt"}, re.compile(r"^\s*(?:public|private|protected|internal)?\s*(?:static\s+)?(?:final\s+)?(?:class|interface|enum)\s+([A-Za-z_]\w*)", re.M)),
    "ruby": ({".rb"}, re.compile(r"^\s*(?:def|class|module)\s+([A-Za-z_]\w*[?!]?)", re.M)),
}

EXT_TO_PAT = {}
for lang, (exts, pat) in DEF_PATTERNS.items():
    for e in exts:
        EXT_TO_PAT[e] = pat


def walk_sources(repo):
    for root, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith(".")]
        for name in files:
            ext = os.path.splitext(name)[1].lower()
            if ext in EXT_TO_PAT:
                yield os.path.join(root, name), EXT_TO_PAT[ext]


def build(repo):
    index = {}
    nfiles = 0
    for path, pattern in walk_sources(repo):
        nfiles += 1
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
        except OSError:
            continue
        rel = os.path.relpath(path, repo)
        for m in pattern.finditer(text):
            name = next((g for g in m.groups() if g), None)
            if not name or len(name) < 2:
                continue
            index.setdefault(name, [])
            if rel not in index[name]:
                index[name].append(rel)
    return {"repo": os.path.abspath(repo), "files_indexed": nfiles, "symbols": index}


def count_references(repo, symbol):
    """Count textual references repo-wide with git grep (fast) or grep."""
    try:
        out = subprocess.run(
            ["git", "-C", repo, "grep", "-c", "--word-regexp", symbol],
            capture_output=True, text=True, timeout=120,
        )
        if out.returncode in (0, 1):
            hits = {}
            for line in out.stdout.strip().splitlines():
                f, _, n = line.rpartition(":")
                hits[f] = int(n)
            return hits
    except (OSError, subprocess.TimeoutExpired):
        pass
    # non-git fallback
    hits = {}
    word = re.compile(r"\b" + re.escape(symbol) + r"\b")
    for path, _ in walk_sources(repo):
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                n = len(word.findall(f.read()))
        except OSError:
            continue
        if n:
            hits[os.path.relpath(path, repo)] = n
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo")
    ap.add_argument("--out", help="write index JSON here")
    ap.add_argument("--lookup", help="count repo-wide references to a symbol")
    args = ap.parse_args()

    if args.lookup:
        hits = count_references(args.repo, args.lookup)
        total = sum(hits.values())
        print(f"'{args.lookup}': {total} textual reference(s) in {len(hits)} file(s)")
        for f, n in sorted(hits.items(), key=lambda kv: -kv[1])[:20]:
            print(f"  {n:>4}  {f}")
        if total <= 1:
            print("  -> only the definition itself (or nothing). Strong dead-code signal,")
            print("     but still run the string/dynamic-usage checks from SKILL.md step 3.")
        return

    idx = build(args.repo)
    print(f"Indexed {idx['files_indexed']:,} files, {len(idx['symbols']):,} symbols", file=sys.stderr)
    if args.out:
        with open(args.out, "w") as f:
            json.dump(idx, f)
        print(f"Wrote {args.out}", file=sys.stderr)
    else:
        json.dump(idx, sys.stdout)


if __name__ == "__main__":
    main()
