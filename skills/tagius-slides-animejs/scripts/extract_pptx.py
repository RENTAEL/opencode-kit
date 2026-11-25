#!/usr/bin/env python3
"""
PPTX → slides-animejs intake shim.

Wraps the `pptx` skill's outputs into the per-slide shape we need:

  - per-slide text (extracted via `python -m markitdown <file>.pptx`)
  - per-slide speaker notes (parsed from the OOXML `ppt/notesSlides/`)
  - per-slide media references (resolved via `ppt/slides/_rels/slideN.xml.rels`)

Media land in `./visuals/from-pptx/slide-NN/<basename>.<ext>`. EMF / WMF
formats are converted to PNG via `soffice` if available; otherwise a
warning is recorded.

Output: a JSON manifest at the path given by `--manifest` with the shape:

    {
      "title": "<from core.xml or filename>",
      "slides": [
        {"index": 1, "text": "...", "notes": "...",
         "media": ["visuals/from-pptx/slide-01/image1.png", ...]},
        ...
      ],
      "warnings": [...]
    }
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

NS = {
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
    "cp": "http://schemas.openxmlformats.org/package/2006/metadata/core-properties",
    "dc": "http://purl.org/dc/elements/1.1/",
}

MEDIA_EXT_RASTER = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".svg"}
MEDIA_EXT_NEEDS_CONVERT = {".emf", ".wmf"}


def have_soffice() -> bool:
    return shutil.which("soffice") is not None or shutil.which("libreoffice") is not None


def convert_to_png(src: Path, dst_dir: Path) -> Path | None:
    binary = shutil.which("soffice") or shutil.which("libreoffice")
    if binary is None:
        return None
    proc = subprocess.run(
        [binary, "--headless", "--convert-to", "png", "--outdir", str(dst_dir), str(src)],
        capture_output=True,
        text=True,
        timeout=60,
    )
    if proc.returncode != 0:
        return None
    out = dst_dir / (src.stem + ".png")
    return out if out.exists() else None


def extract_text_via_markitdown(pptx: Path) -> list[str]:
    """Run `python -m markitdown` and split its output by slide markers."""
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "markitdown", str(pptx)],
            capture_output=True,
            text=True,
            timeout=120,
        )
    except FileNotFoundError:
        return []
    if proc.returncode != 0:
        return []
    md = proc.stdout
    # markitdown emits `<!-- Slide number: N -->` markers
    parts = re.split(r"<!--\s*Slide number:\s*\d+\s*-->", md)
    # Drop preamble (everything before the first marker)
    if parts and parts[0].strip() == "":
        parts = parts[1:]
    # Trim and return
    return [p.strip() for p in parts]


def list_slide_files(z: zipfile.ZipFile) -> list[str]:
    names = [n for n in z.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)]
    names.sort(key=lambda n: int(re.search(r"slide(\d+)\.xml", n).group(1)))
    return names


def parse_notes(z: zipfile.ZipFile, slide_xml_name: str) -> str:
    """Find the notesSlide for a given slideN.xml via the rels file."""
    rels_name = slide_xml_name.replace("slides/slide", "slides/_rels/slide") + ".rels"
    try:
        rels_data = z.read(rels_name)
    except KeyError:
        return ""
    rels_root = ET.fromstring(rels_data)
    notes_target = None
    for rel in rels_root.findall("rel:Relationship", NS):
        if rel.get("Type", "").endswith("/notesSlide"):
            notes_target = rel.get("Target")
            break
    if not notes_target:
        return ""
    # notes_target is relative to ppt/slides/, e.g. "../notesSlides/notesSlide1.xml"
    notes_path = (Path("ppt/slides") / notes_target).resolve().relative_to(Path("/").resolve()) if notes_target.startswith("/") else None
    if notes_path is None:
        # Manual resolution
        base = Path("ppt/slides")
        notes_path = (base / notes_target).as_posix()
        # normalize ../ segments
        parts: list[str] = []
        for seg in notes_path.split("/"):
            if seg == "..":
                if parts:
                    parts.pop()
            elif seg in ("", "."):
                continue
            else:
                parts.append(seg)
        notes_path = "/".join(parts)
    try:
        notes_xml = z.read(notes_path)
    except KeyError:
        return ""
    notes_root = ET.fromstring(notes_xml)
    texts = [t.text or "" for t in notes_root.findall(".//a:t", NS)]
    return "\n".join(t for t in texts if t.strip())


def parse_media_refs(z: zipfile.ZipFile, slide_xml_name: str) -> list[str]:
    rels_name = slide_xml_name.replace("slides/slide", "slides/_rels/slide") + ".rels"
    try:
        rels_data = z.read(rels_name)
    except KeyError:
        return []
    rels_root = ET.fromstring(rels_data)
    targets: list[str] = []
    for rel in rels_root.findall("rel:Relationship", NS):
        rel_type = rel.get("Type", "")
        if rel_type.endswith("/image") or rel_type.endswith("/media"):
            target = rel.get("Target", "")
            # Targets look like "../media/image3.png"
            parts: list[str] = []
            for seg in (Path("ppt/slides") / target).as_posix().split("/"):
                if seg == "..":
                    if parts:
                        parts.pop()
                elif seg in ("", "."):
                    continue
                else:
                    parts.append(seg)
            targets.append("/".join(parts))
    return targets


def parse_title(z: zipfile.ZipFile, default: str) -> str:
    try:
        core_xml = z.read("docProps/core.xml")
    except KeyError:
        return default
    try:
        root = ET.fromstring(core_xml)
    except ET.ParseError:
        return default
    el = root.find("dc:title", NS)
    if el is not None and (el.text or "").strip():
        return (el.text or "").strip()
    return default


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Extract a .pptx into the slides-animejs intake shape.")
    parser.add_argument("pptx", help="Path to the source .pptx file.")
    parser.add_argument("--visuals-dir", default="visuals", help="Project visuals directory.")
    parser.add_argument("--manifest", default="intake-manifest.json", help="Output manifest path.")
    args = parser.parse_args(argv)

    src = Path(args.pptx).resolve()
    if not src.exists():
        print(f"error: {src} not found", file=sys.stderr)
        return 1

    visuals_root = Path(args.visuals_dir).resolve() / "from-pptx"
    visuals_root.mkdir(parents=True, exist_ok=True)
    warnings: list[str] = []

    # --- text via markitdown ---
    texts = extract_text_via_markitdown(src)

    # --- structure via direct OOXML walk ---
    slides_out: list[dict] = []
    with zipfile.ZipFile(src) as z:
        title = parse_title(z, default=src.stem)
        slide_names = list_slide_files(z)
        if not slide_names:
            print("error: no slides found in pptx", file=sys.stderr)
            return 1

        for i, slide_name in enumerate(slide_names, start=1):
            slide_dir = visuals_root / f"slide-{i:02d}"
            slide_dir.mkdir(parents=True, exist_ok=True)
            media_refs = parse_media_refs(z, slide_name)
            media_paths: list[str] = []

            for ref in media_refs:
                try:
                    raw = z.read(ref)
                except KeyError:
                    warnings.append(f"slide {i}: media ref {ref} not found in pptx")
                    continue
                ext = Path(ref).suffix.lower()
                out_path = slide_dir / Path(ref).name

                if ext in MEDIA_EXT_NEEDS_CONVERT:
                    # Write the source temporarily, then attempt convert.
                    tmp = slide_dir / Path(ref).name
                    tmp.write_bytes(raw)
                    converted = convert_to_png(tmp, slide_dir)
                    if converted is not None:
                        out_path = converted
                        # Remove the EMF/WMF original since we have a PNG.
                        try:
                            tmp.unlink()
                        except FileNotFoundError:
                            pass
                    else:
                        warnings.append(
                            f"slide {i}: {Path(ref).name} is {ext.upper()[1:]}; "
                            "soffice not available — provide a replacement asset"
                        )
                        out_path = tmp  # keep the original so the user sees it
                elif ext in MEDIA_EXT_RASTER:
                    out_path.write_bytes(raw)
                else:
                    out_path.write_bytes(raw)
                    warnings.append(f"slide {i}: unknown media type {ext} kept as-is")

                # Record as a project-relative POSIX path.
                rel = out_path.resolve().relative_to(Path(args.visuals_dir).resolve().parent)
                media_paths.append(rel.as_posix())

            slides_out.append(
                {
                    "index": i,
                    "text": texts[i - 1] if i - 1 < len(texts) else "",
                    "notes": parse_notes(z, slide_name),
                    "media": media_paths,
                }
            )

    manifest = {"title": title, "slides": slides_out, "warnings": warnings}
    Path(args.manifest).write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    if warnings:
        print(f"  {len(warnings)} warning(s):")
        for w in warnings:
            print(f"   - {w}")

    print(f"  extracted {len(slides_out)} slide(s) → {args.manifest}")
    print(f"  media → {visuals_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
