#!/usr/bin/env python3
"""Scan a repo for temp/junk files, stale CI files, and orphaned tool configs.

Usage:
    python hygiene_scan.py /path/to/repo [--json]

Complements the source-level tools: these files are never imported by code, so
"unused" means the tool that would consume them is gone or misconfigured. This
script surfaces candidates; SKILL.md step 3 and references/configs-ci-hygiene.md
describe the verification before anything is called safe to remove.
"""

import argparse
import fnmatch
import json
import os
import re
import subprocess
import sys

EXCLUDE_DIRS = {
    ".git", "node_modules", "vendor", "dist", "build", "target",
    "venv", ".venv", "__pycache__", "third_party", "Pods",
}

JUNK_PATTERNS = [
    "*.log", "*.tmp", "*.temp", "*.bak", "*.orig", "*.rej", "*.swp", "*~",
    ".DS_Store", "Thumbs.db", "*.pyc", "core", "core.*", "npm-debug.log*",
    "yarn-error.log", "*.stackdump",
]

# config file -> markers that must appear in a manifest/CI/Makefile for it to be alive
CONFIG_TOOL_MARKERS = {
    ".babelrc": ["babel"],
    "babel.config.js": ["babel"],
    "babel.config.json": ["babel"],
    "tslint.json": ["tslint"],
    ".flowconfig": ["flow-bin", "flow"],
    "bower.json": ["bower"],
    ".bowerrc": ["bower"],
    "Gruntfile.js": ["grunt"],
    "gulpfile.js": ["gulp"],
    "webpack.config.js": ["webpack"],
    ".dockerignore": ["dockerfile"],
    "Procfile": ["heroku"],
    ".travis.yml": ["travis"],
    "appveyor.yml": ["appveyor"],
}

MANIFEST_NAMES = {
    "package.json", "pyproject.toml", "requirements.txt", "requirements-dev.txt",
    "setup.py", "setup.cfg", "gemfile", "go.mod", "cargo.toml", "makefile",
    "dockerfile", "composer.json",
}

CI_DIR_HINTS = (".github/workflows", ".circleci", "ci")


def walk(repo):
    for root, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for f in files:
            yield os.path.join(root, f)


def rel(repo, p):
    return os.path.relpath(p, repo)


def read(path, limit=200_000):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read(limit)
    except OSError:
        return ""


def git_lines(repo, *args):
    try:
        out = subprocess.run(["git", "-C", repo, *args],
                             capture_output=True, text=True, timeout=60)
        return out.stdout.splitlines() if out.returncode == 0 else []
    except (OSError, subprocess.TimeoutExpired):
        return []


def find_junk(repo, all_files):
    committed = set(git_lines(repo, "ls-files"))
    junk = []
    for path in all_files:
        name = os.path.basename(path)
        r = rel(repo, path)
        if any(fnmatch.fnmatch(name, pat) for pat in JUNK_PATTERNS):
            if "fixture" in r.lower() or "testdata" in r.lower():
                continue  # likely test input, not junk
            junk.append({
                "file": r,
                "committed": (r in committed) if committed else None,
            })
    return junk


def gather_haystack(repo, all_files):
    """Concatenate manifests + CI yaml + Makefiles: where live tools are named."""
    chunks = []
    for path in all_files:
        name = os.path.basename(path).lower()
        r = rel(repo, path).replace("\\", "/")
        if name in MANIFEST_NAMES or name.startswith("makefile") or \
           any(h in r for h in CI_DIR_HINTS) or name.endswith((".yml", ".yaml")):
            chunks.append(read(path).lower())
    return "\n".join(chunks)


def find_orphan_configs(repo, all_files, haystack):
    orphans = []
    for path in all_files:
        name = os.path.basename(path)
        markers = CONFIG_TOOL_MARKERS.get(name)
        if not markers:
            continue
        if not any(m in haystack for m in markers):
            orphans.append({
                "file": rel(repo, path),
                "expected_tool": markers[0],
                "reason": f"'{markers[0]}' not found in any manifest, CI file, or Makefile",
            })
    return orphans


def find_stale_ci(repo, all_files):
    findings = []
    ci_files = []
    for path in all_files:
        r = rel(repo, path).replace("\\", "/")
        name = os.path.basename(path)
        if name in (".travis.yml", "Jenkinsfile", "appveyor.yml", "azure-pipelines.yml") \
           or r.startswith(".circleci/") or r.startswith(".github/workflows/"):
            ci_files.append((r, path))
        if name.endswith((".yml.disabled", ".yml.bak", ".yaml.disabled", ".yaml.bak")):
            findings.append({"file": r, "reason": "disabled/backup CI file"})

    # multiple CI systems -> flag the ones with the oldest last commit
    systems = {}
    for r, path in ci_files:
        sys_name = ("github" if ".github/" in r else
                    "circleci" if ".circleci/" in r else
                    os.path.basename(r))
        date = git_lines(repo, "log", "-1", "--format=%cs", "--", r)
        systems.setdefault(sys_name, []).append((r, date[0] if date else "unknown"))

    if len(systems) > 1:
        for sys_name, files in systems.items():
            for r, date in files:
                findings.append({
                    "file": r,
                    "reason": f"multiple CI systems present ({', '.join(sorted(systems))}); last commit {date}",
                })

    # workflows referencing branches that no longer exist
    branches = {b.strip().split("/")[-1] for b in git_lines(repo, "branch", "-a")}
    branch_re = re.compile(r"branches:\s*\n(?:\s*-\s*([\w./-]+)\s*\n)+")
    for r, path in ci_files:
        text = read(path)
        for m in re.finditer(r"-\s*([\w./-]+)", branch_re.search(text).group(0)) if branch_re.search(text) else []:
            b = m.group(1)
            if branches and b not in branches and "*" not in b:
                findings.append({"file": r, "reason": f"triggers on branch '{b}' which does not exist"})
    return findings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if not os.path.isdir(args.repo):
        print(f"error: {args.repo} is not a directory", file=sys.stderr)
        sys.exit(1)

    all_files = list(walk(args.repo))
    haystack = gather_haystack(args.repo, all_files)
    result = {
        "junk_files": find_junk(args.repo, all_files),
        "orphan_configs": find_orphan_configs(args.repo, all_files, haystack),
        "stale_ci": find_stale_ci(args.repo, all_files),
    }

    if args.json:
        print(json.dumps(result, indent=2))
        return

    print("== Temp / junk files ==")
    if not result["junk_files"]:
        print("  none found")
    for j in result["junk_files"]:
        tag = "committed" if j["committed"] else "untracked/ignored"
        print(f"  {j['file']}  ({tag})")

    print("\n== Orphaned tool configs ==")
    if not result["orphan_configs"]:
        print("  none found")
    for c in result["orphan_configs"]:
        print(f"  {c['file']}  -> {c['reason']}")

    print("\n== Stale CI candidates ==")
    if not result["stale_ci"]:
        print("  none found")
    for s in result["stale_ci"]:
        print(f"  {s['file']}  -> {s['reason']}")

    print("\nVerify all candidates per references/configs-ci-hygiene.md before removal.")


if __name__ == "__main__":
    main()
