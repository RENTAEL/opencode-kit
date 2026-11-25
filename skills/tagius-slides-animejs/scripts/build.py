#!/usr/bin/env python3
"""
Build the `./presentation/` bundle for slides-animejs.

Inputs (project-relative defaults):
  - presentation_plan.md   — canonical plan (front matter, design tokens, per-slide blocks).
  - slides-draft/          — slides-grab-style `slide-XX.html` files (or `--slides-dir`).
  - visuals/               — user-curated assets (also auto-extracted PPTX + memes).

Output: ./presentation/  (overwritten in place; idempotent).

What it does:
  1. Parse presentation_plan.md → front matter + design tokens (YAML block) + slide list.
  2. Read each `slide-XX.html` from --slides-dir, strip <html>/<head>/<body> wrappers,
     preserve inline <style> blocks at the top of the fragment.
  3. Render slides.css with the design tokens injected as CSS variables.
  4. Copy templated assets (overlay.js, overlay.css, index.html, run.py, README.md).
  5. Copy the vendored anime.esm.min.js (fetched separately by fetch_animejs.py).
  6. Mirror ./visuals/ into presentation/assets/visuals/.
  7. Emit slide manifest as `window.__SLIDES__ = [...]` inline in index.html.

The script never edits the plan or drafts; it only writes inside ./presentation/.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = SKILL_ROOT / "assets"
VENDOR_BUNDLE = ASSETS_DIR / "vendor" / "anime.esm.min.js"

# Slide canvas baseline — the final 720x405 viewport, matching assets/slides.css
# and overlay.js (SLIDE_W/SLIDE_H). Used only for sanity-check log output; the
# authoritative values live in slides.css and are runtime-scaled by overlay.js.
# The token override mechanism does NOT touch --slide-w/--slide-h.
DEFAULT_SLIDE_W = 720
DEFAULT_SLIDE_H = 405


# ---------- presentation_plan.md parser ----------

@dataclass
class Slide:
    index: int
    title: str
    purpose: str = ""
    key_message: str = ""
    content_lines: list[str] = field(default_factory=list)
    visuals: list[str] = field(default_factory=list)
    animation_hints: dict[str, str] = field(default_factory=dict)
    meme: str = ""
    notes: str = ""
    status: str = "draft"


@dataclass
class Plan:
    title: str = "Untitled"
    author: str = ""
    audience: str = ""
    length: str = ""
    tone: str = ""
    academic: str = ""
    memes_allowed: str = ""
    palette: str = ""
    style: str = ""
    fonts: str = ""
    tokens: dict[str, str] = field(default_factory=dict)
    slides: list[Slide] = field(default_factory=list)


SLIDE_HEADER_RE = re.compile(r"^###\s+Slide\s+(\d+)\s*(?:—|--|-)\s*(.*?)\s*$")
FIELD_RE = re.compile(r"^\s*-\s+\*\*([^*]+)\*\*\s*:\s*(.*)$")
SUB_RE = re.compile(r"^\s+-\s+(.*)$")
TOKEN_RE = re.compile(r"^([A-Za-z0-9_\-]+)\s*:\s*\"?([^\"]*)\"?\s*$")


def parse_plan(text: str) -> Plan:
    plan = Plan()
    lines = text.splitlines()
    i = 0
    n = len(lines)

    # 1. Title line ("# Presentation: ...")
    while i < n:
        line = lines[i]
        m = re.match(r"#\s+Presentation:\s*(.*)$", line)
        if m:
            plan.title = m.group(1).strip() or "Untitled"
            i += 1
            break
        i += 1

    # 2. Front matter (bullet list `- Key: value`) until first `## ` heading.
    while i < n and not lines[i].startswith("## "):
        line = lines[i].strip()
        if line.startswith("- "):
            kv = line[2:]
            if ":" in kv:
                key, value = kv.split(":", 1)
                key = key.strip().lower()
                value = value.strip()
                if key == "author":
                    plan.author = value
                elif key == "audience":
                    plan.audience = value
                elif key == "length":
                    plan.length = value
                elif key == "tone":
                    plan.tone = value
                elif key == "academic":
                    plan.academic = value
                elif key in ("memes allowed", "memes-allowed", "memes"):
                    plan.memes_allowed = value
                elif key == "palette":
                    plan.palette = value
                elif key == "style":
                    plan.style = value
                elif key in ("fonts", "font"):
                    plan.fonts = value
        i += 1

    # 3. Design tokens YAML block, then ## Slides.
    while i < n:
        line = lines[i]
        if line.startswith("## Design tokens"):
            i += 1
            # Expect a fenced ```yaml block.
            while i < n and not lines[i].lstrip().startswith("```"):
                i += 1
            if i < n:
                i += 1  # skip opening fence
                while i < n and not lines[i].lstrip().startswith("```"):
                    m = TOKEN_RE.match(lines[i])
                    if m:
                        plan.tokens[m.group(1).strip()] = m.group(2).strip()
                    i += 1
                if i < n:
                    i += 1  # skip closing fence
            continue
        if line.startswith("## Slides"):
            i += 1
            break
        i += 1

    # 4. Per-slide blocks.
    current: Slide | None = None
    current_field: str | None = None
    while i < n:
        line = lines[i]
        m_hdr = SLIDE_HEADER_RE.match(line)
        if m_hdr:
            if current is not None:
                plan.slides.append(current)
            current = Slide(index=int(m_hdr.group(1)), title=m_hdr.group(2))
            current_field = None
            i += 1
            continue
        if current is None:
            i += 1
            continue

        m_fld = FIELD_RE.match(line)
        if m_fld:
            key = m_fld.group(1).strip().lower()
            value = m_fld.group(2).strip()
            current_field = key
            if key == "purpose":
                current.purpose = value
            elif key in ("key message", "message"):
                current.key_message = value
            elif key == "content":
                # Body follows as nested sub-bullets; clear and accumulate.
                current.content_lines = []
            elif key == "visuals":
                current.visuals = parse_inline_paths(value)
            elif key in ("animation hints", "animation"):
                current.animation_hints = parse_kv_pairs(value)
            elif key == "meme":
                current.meme = "" if value.lower() == "none" else value
            elif key == "notes":
                current.notes = value
            elif key == "status":
                current.status = value.lower() or "draft"
            i += 1
            continue

        m_sub = SUB_RE.match(line)
        if m_sub and current_field == "content":
            current.content_lines.append(m_sub.group(1).strip())
            i += 1
            continue

        # Continuation lines for free-text fields (notes/purpose/key_message)
        # when the user uses multi-line indented blocks.
        if line.startswith("  ") and current_field in ("notes", "purpose", "key message"):
            if current_field == "notes":
                current.notes += " " + line.strip()
            elif current_field == "purpose":
                current.purpose += " " + line.strip()
            elif current_field == "key message":
                current.key_message += " " + line.strip()
            i += 1
            continue

        i += 1

    if current is not None:
        plan.slides.append(current)

    plan.slides.sort(key=lambda s: s.index)
    return plan


def parse_inline_paths(value: str) -> list[str]:
    # Backtick-delimited paths, or bare comma-separated paths.
    paths = re.findall(r"`([^`]+)`", value)
    if paths:
        return [p.strip() for p in paths]
    return [p.strip() for p in value.split(",") if p.strip()]


def parse_kv_pairs(value: str) -> dict[str, str]:
    out: dict[str, str] = {}
    fragments = re.findall(r"`([^`]+)`", value)
    items = fragments if fragments else [p.strip() for p in value.split(",")]
    for item in items:
        if ":" in item:
            k, v = item.split(":", 1)
            out[k.strip().lower()] = v.strip()
    return out


# ---------- slide HTML normalizer ----------

class _BodyExtractor(HTMLParser):
    """Extract <body> inner HTML plus any <style> tags from <head>."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.in_body = False
        self.in_head = False
        self.in_style = False
        self.depth_body = 0
        self.body_parts: list[str] = []
        self.head_styles: list[str] = []
        self._current_style: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag == "body":
            self.in_body = True
            self.depth_body = 0
            return
        if tag == "head":
            self.in_head = True
            return
        if tag == "style" and self.in_head:
            self.in_style = True
            self._current_style = []
            return
        if self.in_body:
            attr_str = "".join(f' {k}="{v}"' if v is not None else f" {k}" for k, v in attrs)
            self.body_parts.append(f"<{tag}{attr_str}>")
            if tag != "img" and tag != "br" and tag != "hr":
                self.depth_body += 1

    def handle_endtag(self, tag):
        if tag == "body":
            self.in_body = False
            return
        if tag == "head":
            self.in_head = False
            return
        if tag == "style" and self.in_style:
            self.head_styles.append("".join(self._current_style))
            self.in_style = False
            return
        if self.in_body:
            self.body_parts.append(f"</{tag}>")
            self.depth_body = max(0, self.depth_body - 1)

    def handle_startendtag(self, tag, attrs):
        if self.in_body:
            attr_str = "".join(f' {k}="{v}"' if v is not None else f" {k}" for k, v in attrs)
            self.body_parts.append(f"<{tag}{attr_str}/>")

    def handle_data(self, data):
        if self.in_style:
            self._current_style.append(data)
        elif self.in_body:
            self.body_parts.append(data)

    def handle_entityref(self, name):
        if self.in_body:
            self.body_parts.append(f"&{name};")

    def handle_charref(self, name):
        if self.in_body:
            self.body_parts.append(f"&#{name};")

    def handle_comment(self, data):
        if self.in_body:
            self.body_parts.append(f"<!--{data}-->")


def normalize_slide_html(raw: str) -> str:
    """Strip <html>/<head>/<body> wrappers. Hoist <head><style> to top of fragment."""
    if "<body" not in raw.lower() and "<html" not in raw.lower():
        return raw.strip()
    parser = _BodyExtractor()
    parser.feed(raw)
    parser.close()
    body = "".join(parser.body_parts).strip()
    head_styles = "\n".join(f"<style>{s}</style>" for s in parser.head_styles if s.strip())
    if head_styles:
        return f"{head_styles}\n{body}"
    return body


# ---------- token → CSS rendering ----------

def render_slides_css(template: str, tokens: dict[str, str]) -> str:
    """Override CSS variable defaults inside :root with token values."""
    if not tokens:
        return template

    def repl(match: re.Match[str]) -> str:
        body = match.group(2)
        new_lines = body.splitlines()
        out: list[str] = []
        seen: set[str] = set()
        for line in new_lines:
            m = re.match(r"(\s*)--([a-zA-Z0-9_\-]+)\s*:\s*[^;]+;", line)
            if m and m.group(2) in tokens:
                indent = m.group(1)
                key = m.group(2)
                out.append(f'{indent}--{key}: {tokens[key]};')
                seen.add(key)
            else:
                out.append(line)
        # Append any tokens not present in the template (kebab-case → --key).
        for key, value in tokens.items():
            if key not in seen:
                out.insert(-1, f"  --{key}: {value};")
        return f"{match.group(1)}{chr(10).join(out)}{match.group(3)}"

    return re.sub(r"(:root\s*\{)(.*?)(\})", repl, template, count=1, flags=re.DOTALL)


# ---------- build pipeline ----------

def copy_tree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Build the slides-animejs presentation bundle.")
    parser.add_argument("--plan", default="presentation_plan.md", help="Path to presentation_plan.md.")
    parser.add_argument("--slides-dir", default="slides-draft", help="Slides-grab workspace.")
    parser.add_argument("--visuals-dir", default="visuals", help="Project visuals directory.")
    parser.add_argument("--out", default="presentation", help="Output bundle directory.")
    args = parser.parse_args(argv)

    plan_path = Path(args.plan).resolve()
    if not plan_path.exists():
        print(f"error: {plan_path} not found", file=sys.stderr)
        return 1

    if not VENDOR_BUNDLE.exists():
        print(
            f"error: {VENDOR_BUNDLE} not found. Run scripts/fetch_animejs.py first.",
            file=sys.stderr,
        )
        return 1

    plan = parse_plan(plan_path.read_text(encoding="utf-8"))
    print(f"  plan: {plan.title} ({len(plan.slides)} slide(s))")

    slides_dir = Path(args.slides_dir).resolve()
    visuals_dir = Path(args.visuals_dir).resolve()
    out_dir = Path(args.out).resolve()
    out_assets = out_dir / "assets"
    out_slides = out_dir / "slides"

    # Fresh-out the bundle (idempotent rebuild).
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_assets.mkdir(parents=True, exist_ok=True)
    out_slides.mkdir(parents=True, exist_ok=True)

    # --- per-slide HTML ---
    manifest: list[dict] = []
    for slide in plan.slides:
        src_name = f"slide-{slide.index:02d}.html"
        src = slides_dir / src_name
        if not src.exists():
            print(f"  warning: {src_name} not found in {slides_dir}; emitting placeholder", file=sys.stderr)
            content_html = (
                f"<header class=\"slide-header\"><h1 data-anim>{slide.title}</h1></header>"
                "<section class=\"slide-body\"><p class=\"caption\">"
                "Draft missing — re-run slides-grab-design or drop the slide HTML in place."
                "</p></section>"
            )
        else:
            content_html = normalize_slide_html(src.read_text(encoding="utf-8"))

        (out_slides / src_name).write_text(content_html, encoding="utf-8")
        manifest.append(
            {
                "file": src_name,
                "title": slide.title,
                "notes": slide.notes,
                "status": slide.status,
            }
        )

    # --- assets: slides.css with tokens injected ---
    slides_css_template = (ASSETS_DIR / "slides.css").read_text(encoding="utf-8")
    slides_css = render_slides_css(slides_css_template, plan.tokens)
    (out_assets / "slides.css").write_text(slides_css, encoding="utf-8")

    # overlay.{js,css} as-is.
    shutil.copy2(ASSETS_DIR / "overlay.css", out_assets / "overlay.css")
    shutil.copy2(ASSETS_DIR / "overlay.js", out_assets / "overlay.js")

    # vendored anime.js.
    shutil.copy2(VENDOR_BUNDLE, out_assets / "anime.esm.min.js")

    # mirror visuals/.
    if visuals_dir.exists():
        copy_tree(visuals_dir, out_assets / "visuals")
    else:
        (out_assets / "visuals").mkdir(exist_ok=True)

    # --- index.html ---
    index_template = (ASSETS_DIR / "index.html").read_text(encoding="utf-8")
    slides_json = json.dumps(manifest, ensure_ascii=False)
    index_html = (
        index_template
        .replace("{{TITLE}}", plan.title)
        .replace("{{SLIDES_JSON}}", slides_json)
    )
    (out_dir / "index.html").write_text(index_html, encoding="utf-8")

    # --- run.py ---
    shutil.copy2(ASSETS_DIR / "run.py", out_dir / "run.py")
    (out_dir / "run.py").chmod(0o755)

    # --- README ---
    readme_template = (ASSETS_DIR / "README.template.md").read_text(encoding="utf-8")
    (out_dir / "README.md").write_text(readme_template.replace("{{TITLE}}", plan.title), encoding="utf-8")

    print(f"  built bundle: {out_dir}")
    print(f"  next: cd {out_dir.name} && python3 run.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
