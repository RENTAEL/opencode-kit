#!/usr/bin/env python3
"""Deterministic scaffolding helpers for the Project Anchor skill.

Uses only the Python standard library.
Never overwrites existing files.
"""

from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = SKILL_ROOT / "assets" / "templates"
PROFILES = {"generic", "agent", "python", "java"}

BASE_TEMPLATES = {
    "AGENTS.md": "AGENTS.md.tpl",
    "docs/index.md": "index.md.tpl",
    "docs/product/overview.md": "product-overview.md.tpl",
    "docs/product/boundaries.md": "product-boundaries.md.tpl",
    "docs/specs/README.md": "specs-readme.md.tpl",
    "docs/architecture/overview.md": "architecture-overview.md.tpl",
    "docs/invariants/invariants.md": "invariants.md.tpl",
    "docs/decisions/README.md": "decisions-readme.md.tpl",
    "docs/changes/active/README.md": "active-readme.md.tpl",
    "docs/changes/archive/README.md": "archive-readme.md.tpl",
}
CHANGE_TEMPLATES = {
    "proposal.md": "change/proposal.md.tpl",
    "spec.md": "change/spec.md.tpl",
    "design.md": "change/design.md.tpl",
    "tasks.md": "change/tasks.md.tpl",
}

def render(template_path: Path, values: dict[str, str]) -> str:
    text = template_path.read_text(encoding="utf-8")
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text

def write_new(path: Path, content: str, dry_run: bool = False) -> str:
    if path.exists():
        return f"SKIP   {path} (exists)"
    if dry_run:
        return f"CREATE {path}"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    return f"CREATE {path}"

def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "change"

def title_from_slug(slug: str) -> str:
    return " ".join(w.capitalize() for w in slug.replace("_", "-").split("-") if w)

def cmd_init(args):
    root = Path(args.root).resolve()
    values = {"PROJECT_NAME": args.project_name or root.name, "PROFILE": args.profile}
    print(f"Repository: {root}")
    print(f"Profile:    {args.profile}")
    for rel, tpl in BASE_TEMPLATES.items():
        print(write_new(root / rel, render(TEMPLATES / tpl, values), args.dry_run))
    print("\nReview TBD placeholders against real code/tests/requirements.")
    return 0

def cmd_new_change(args):
    root = Path(args.root).resolve()
    slug = slugify(args.name)
    title = args.title or title_from_slug(slug)
    change_dir = root / "docs" / "changes" / "active" / slug
    for filename, tpl in CHANGE_TEMPLATES.items():
        print(write_new(change_dir / filename, render(TEMPLATES / tpl, {"CHANGE_TITLE": title}), args.dry_run))
    return 0

def next_adr_number(decisions: Path) -> int:
    nums = []
    if decisions.exists():
        for p in decisions.glob("ADR-*.md"):
            m = re.match(r"ADR-(\d+)", p.name, re.I)
            if m:
                nums.append(int(m.group(1)))
    return max(nums, default=0) + 1

def cmd_new_adr(args):
    root = Path(args.root).resolve()
    decisions = root / "docs" / "decisions"
    n = next_adr_number(decisions)
    num = f"{n:03d}"
    path = decisions / f"ADR-{num}-{slugify(args.title)}.md"
    content = render(TEMPLATES / "adr.md.tpl", {"ADR_NUMBER": num, "ADR_TITLE": args.title.strip()})
    print(write_new(path, content, args.dry_run))
    return 0

def validate_index_links(root: Path):
    problems = []
    index = root / "docs" / "index.md"
    if not index.exists():
        return problems
    text = index.read_text(encoding="utf-8")
    for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
        if "://" in target or target.startswith("#"):
            continue
        clean = target.split("#", 1)[0]
        if clean and not (index.parent / clean).resolve().exists():
            problems.append(f"Broken docs/index.md link: {target}")
    return problems

def validate_active_changes(root: Path):
    problems = []
    active = root / "docs" / "changes" / "active"
    if not active.exists():
        return problems
    for child in active.iterdir():
        if child.is_dir():
            missing = [x for x in CHANGE_TEMPLATES if not (child / x).exists()]
            if missing:
                problems.append(f"Active change {child.name} missing: {', '.join(missing)}")
    return problems

def validate_adr_numbers(root: Path):
    problems, seen = [], {}
    decisions = root / "docs" / "decisions"
    if not decisions.exists():
        return problems
    for p in decisions.glob("ADR-*.md"):
        m = re.match(r"ADR-(\d+)", p.name, re.I)
        if m:
            n = int(m.group(1))
            if n in seen:
                problems.append(f"Duplicate ADR number {n:03d}: {seen[n].name}, {p.name}")
            else:
                seen[n] = p
    return problems

def cmd_validate(args):
    root = Path(args.root).resolve()
    problems = [
        f"Missing governance file: {Path(rel)}"
        for rel in BASE_TEMPLATES
        if not (root / rel).exists()
    ]
    problems += validate_index_links(root)
    problems += validate_active_changes(root)
    problems += validate_adr_numbers(root)
    if problems:
        print("Governance validation found issues:")
        for p in problems:
            print(f"- {p}")
        return 1
    print("Governance structure looks consistent.")
    print("Structural validation does not prove semantic agreement between docs and code.")
    return 0

def build_parser():
    p = argparse.ArgumentParser(description="Project Anchor governance scaffolding helper")
    sub = p.add_subparsers(dest="command", required=True)

    x = sub.add_parser("init", help="Create missing governance files")
    x.add_argument("--root", default=".")
    x.add_argument("--profile", default="generic", choices=sorted(PROFILES))
    x.add_argument("--project-name")
    x.add_argument("--dry-run", action="store_true")
    x.set_defaults(func=cmd_init)

    x = sub.add_parser("new-change", help="Create an active significant-change workspace")
    x.add_argument("name")
    x.add_argument("--title")
    x.add_argument("--root", default=".")
    x.add_argument("--dry-run", action="store_true")
    x.set_defaults(func=cmd_new_change)

    x = sub.add_parser("new-adr", help="Create the next numbered ADR")
    x.add_argument("title")
    x.add_argument("--root", default=".")
    x.add_argument("--dry-run", action="store_true")
    x.set_defaults(func=cmd_new_adr)

    x = sub.add_parser("validate", help="Validate governance structure")
    x.add_argument("--root", default=".")
    x.set_defaults(func=cmd_validate)
    return p

def main():
    args = build_parser().parse_args()
    return args.func(args)

if __name__ == "__main__":
    sys.exit(main())
