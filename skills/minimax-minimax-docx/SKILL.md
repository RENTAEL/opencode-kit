---
name: minimax-minimax-docx
description: "Create, edit, and format DOCX documents via CLI tools or direct C# scripts built on OpenXML SDK (.NET)."
---
# minimax-docx

Create, edit, and format DOCX documents via CLI tools or direct C# scripts built on OpenXML SDK (.NET).

## Setup

**First time:** `bash scripts/setup.sh` (or `powershell scripts/setup.ps1` on Windows, `--minimal` to skip optional deps).

**First operation in session:** `scripts/env_check.sh` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â do not proceed if `NOT READY`. (Skip on subsequent operations within the same session.)

## Quick Start: Direct C# Path

When the task requires structural document manipulation (custom styles, complex tables, multi-section layouts, headers/footers, TOC, images), write C# directly instead of wrestling with CLI limitations. Use this scaffold:

```csharp
// File: scripts/dotnet/task.csx  (or a new .cs in a Console project)
// dotnet run --project scripts/dotnet/MiniMaxAIDocx.Cli -- run-script task.csx
#r "nuget: DocumentFormat.OpenXml, 3.2.0"

using DocumentFormat.OpenXml;
using DocumentFormat.OpenXml.Packaging;
using DocumentFormat.OpenXml.Wordprocessing;

using var doc = WordprocessingDocument.Create("output.docx", WordprocessingDocumentType.Document);
var mainPart = doc.AddMainDocumentPart();
mainPart.Document = new Document(new Body());

// --- Your logic here ---
// Read the relevant Samples/*.cs file FIRST for tested patterns.
// See Samples/ table in References section below.
```

**Before writing any C#, read the relevant `Samples/*.cs` file** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â they contain compilable, SDK-version-verified patterns. The Samples table in the References section below maps topics to files.

## CLI shorthand

All CLI commands below use `$CLI` as shorthand for:
```bash
dotnet run --project scripts/dotnet/MiniMaxAIDocx.Cli --
```

## Pipeline routing

Route by checking: does the user have an input .docx file?

```
User task
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ No input file ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Pipeline A: CREATE
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   signals: "write", "create", "draft", "generate", "new", "make a report/proposal/memo"
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Read references/scenario_a_create.md
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Has input .docx
    ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Replace/fill/modify content ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Pipeline B: FILL-EDIT
    ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   signals: "fill in", "replace", "update", "change text", "add section", "edit"
    ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Read references/scenario_b_edit_content.md
    ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
    ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Reformat/apply style/template ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Pipeline C: FORMAT-APPLY
        signals: "reformat", "apply template", "restyle", "match this format", "ÃƒÂ¥Ã‚Â¥Ã¢â‚¬â€ÃƒÂ¦Ã‚Â¨Ã‚Â¡ÃƒÂ¦Ã‚ÂÃ‚Â¿", "ÃƒÂ¦Ã…Â½Ã¢â‚¬â„¢ÃƒÂ§Ã¢â‚¬Â°Ã‹â€ "
        ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Template is pure style (no content) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ C-1: OVERLAY (apply styles to source)
        ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Template has structure (cover/TOC/example sections) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ C-2: BASE-REPLACE
            (use template as base, replace example content with user content)
        ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Read references/scenario_c_apply_template.md
```

If the request spans multiple pipelines, run them sequentially (e.g., Create then Format-Apply).

## Pre-processing

Convert `.doc` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `.docx` if needed: `scripts/doc_to_docx.sh input.doc output_dir/`

Preview before editing (avoids reading raw XML): `scripts/docx_preview.sh document.docx`

Analyze structure for editing scenarios: `$CLI analyze --input document.docx`

## Scenario A: Create

Read `references/scenario_a_create.md`, `references/typography_guide.md`, and `references/design_principles.md` first. Pick an aesthetic recipe from `Samples/AestheticRecipeSamples.cs` that matches the document type ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â do not invent formatting values. For CJK, also read `references/cjk_typography.md`.

**Choose your path:**
- **Simple** (plain text, minimal formatting): use CLI ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `$CLI create --type report --output out.docx --config content.json`
- **Structural** (custom styles, multi-section, TOC, images, complex tables): write C# directly. Read the relevant `Samples/*.cs` first.

CLI options: `--type` (report|letter|memo|academic), `--title`, `--author`, `--page-size` (letter|a4|legal|a3), `--margins` (standard|narrow|wide), `--header`, `--footer`, `--page-numbers`, `--toc`, `--content-json`.

Then run the **validation pipeline** (below).

## Scenario B: Edit / Fill

Read `references/scenario_b_edit_content.md` first. Preview ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ analyze ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ edit ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ validate.

**Choose your path:**
- **Simple** (text replacement, placeholder fill): use CLI subcommands.
- **Structural** (add/reorganize sections, modify styles, manipulate tables, insert images): write C# directly. Read `references/openxml_element_order.md` and the relevant `Samples/*.cs`.

Available CLI edit subcommands:
- `replace-text --find "X" --replace "Y"`
- `fill-placeholders --data '{"key":"value"}'`
- `fill-table --data table.json`
- `insert-section`, `remove-section`, `update-header-footer`

```bash
$CLI edit replace-text --input in.docx --output out.docx --find "OLD" --replace "NEW"
$CLI edit fill-placeholders --input in.docx --output out.docx --data '{"name":"John"}'
```

Then run the **validation pipeline**. Also run diff to verify minimal changes:
```bash
$CLI diff --before in.docx --after out.docx
```

## Scenario C: Apply Template

Read `references/scenario_c_apply_template.md` first. Preview and analyze both source and template.

```bash
$CLI apply-template --input source.docx --template template.docx --output out.docx
```

For complex template operations (multi-template merge, per-section headers/footers, style merging), write C# directly ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â see Critical Rules below for required patterns.

Run the **validation pipeline**, then the **hard gate-check**:
```bash
$CLI validate --input out.docx --gate-check assets/xsd/business-rules.xsd
```
Gate-check is a **hard requirement**. Do NOT deliver until it passes. If it fails: diagnose, fix, re-run.

Also diff to verify content preservation: `$CLI diff --before source.docx --after out.docx`

## Validation pipeline

Run after every write operation. For Scenario C the full pipeline is **mandatory**; for A/B it is **recommended** (skip only if the operation was trivially simple).

```bash
$CLI merge-runs --input doc.docx                                    # 1. consolidate runs
$CLI validate --input doc.docx --xsd assets/xsd/wml-subset.xsd     # 2. XSD structure
$CLI validate --input doc.docx --business                           # 3. business rules
```

If XSD fails, auto-repair and retry:
```bash
$CLI fix-order --input doc.docx
$CLI validate --input doc.docx --xsd assets/xsd/wml-subset.xsd
```

If XSD still fails, fall back to business rules + preview:
```bash
$CLI validate --input doc.docx --business
scripts/docx_preview.sh doc.docx
# Verify: font contamination=0, table count correct, drawing count correct, sectPr count correct
```

Final preview: `scripts/docx_preview.sh doc.docx`

## Critical rules

These prevent file corruption ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â OpenXML is strict about element ordering.

**Element order** (properties always first):

| Parent | Order |
|--------|-------|
| `w:p`  | `pPr` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ runs |
| `w:r`  | `rPr` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `t`/`br`/`tab` |
| `w:tbl`| `tblPr` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `tblGrid` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `tr` |
| `w:tr` | `trPr` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `tc` |
| `w:tc` | `tcPr` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `p` (min 1 `<w:p/>`) |
| `w:body` | block content ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `sectPr` (LAST child) |

**Direct format contamination:** When copying content from a source document, inline `rPr` (fonts, color) and `pPr` (borders, shading, spacing) override template styles. Always strip direct formatting ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â keep only `pStyle` reference and `t` text. Clean tables too (including `pPr/rPr` inside cells).

**Track changes:** `<w:del>` uses `<w:delText>`, never `<w:t>`. `<w:ins>` uses `<w:t>`, never `<w:delText>`.

**Font size:** `w:sz` = points ÃƒÆ’Ã¢â‚¬â€ 2 (12pt ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `sz="24"`). Margins/spacing in DXA (1 inch = 1440, 1cm ÃƒÂ¢Ã¢â‚¬Â°Ã‹â€  567).

**Heading styles MUST have OutlineLevel:** When defining heading styles (Heading1, ThesisH1, etc.), always include `new OutlineLevel { Val = N }` in `StyleParagraphProperties` (H1ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢0, H2ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢1, H3ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢2). Without this, Word sees them as plain styled text ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â TOC and navigation pane won't work.

**Multi-template merge:** When given multiple template files (font, heading, breaks), read `references/scenario_c_apply_template.md` section "Multi-Template Merge" FIRST. Key rules:
- Merge styles from all templates into one styles.xml. Structure (sections/breaks) comes from the breaks template.
- Each content paragraph must appear exactly ONCE ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â never duplicate when inserting section breaks.
- NEVER insert empty/blank paragraphs as padding or section separators. Output paragraph count must equal input. Use section break properties (`w:sectPr` inside `w:pPr`) and style spacing (`w:spacing` before/after) for visual separation.
- Insert oddPage section breaks before EVERY chapter heading, not just the first. Even if a chapter has dual-column content, it MUST start with oddPage; use a second continuous break after the heading for column switching.
- Dual-column chapters need THREE section breaks: (1) oddPage in preceding para's pPr, (2) continuous+cols=2 in the chapter HEADING's pPr, (3) continuous+cols=1 in the last body para's pPr to revert.
- Copy `titlePg` settings from the breaks template for EACH section. Abstract and TOC sections typically need `titlePg=true`.

**Multi-section headers/footers:** Templates with 10+ sections (e.g., Chinese thesis) have DIFFERENT headers/footers per section (Roman vs Arabic page numbers, different header text per zone). Rules:
- Use C-2 Base-Replace: copy the TEMPLATE as output base, then replace body content. This preserves all sections, headers, footers, and titlePg settings automatically.
- NEVER recreate headers/footers from scratch ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â copy template header/footer XML byte-for-byte.
- NEVER add formatting (borders, alignment, font size) not present in the template header XML.
- Non-cover sections MUST have header/footer XML files (at least empty header + page number footer).
- See `references/scenario_c_apply_template.md` section "Multi-Section Header/Footer Transfer".

## References

Load as needed ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â don't load all at once. Pick the most relevant files for the task.

**The C# samples and design references below are the project's knowledge base ("encyclopedia").** When writing OpenXML code, ALWAYS read the relevant sample file first ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â it contains compilable, SDK-version-verified patterns that prevent common errors. When making aesthetic decisions, read the design principles and recipe files ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â they encode tested, harmonious parameter sets from authoritative sources (IEEE, ACM, APA, Nature, etc.), not guesses.

### Scenario guides (read first for each pipeline)

| File | When |
|------|------|
| `references/scenario_a_create.md` | Pipeline A: creating from scratch |
| `references/scenario_b_edit_content.md` | Pipeline B: editing existing content |
| `references/scenario_c_apply_template.md` | Pipeline C: applying template formatting |

### C# code samples (compilable, heavily commented ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â read when writing code)

| File | Topic |
|------|-------|
| `Samples/DocumentCreationSamples.cs` | Document lifecycle: create, open, save, streams, doc defaults, settings, properties, page setup, multi-section |
| `Samples/StyleSystemSamples.cs` | Styles: Normal/Heading chain, character/table/list styles, DocDefaults, latentStyles, CJK ÃƒÂ¥Ã¢â‚¬Â¦Ã‚Â¬ÃƒÂ¦Ã¢â‚¬â€œÃ¢â‚¬Â¡, APA 7th, import, resolve inheritance |
| `Samples/CharacterFormattingSamples.cs` | RunProperties: fonts, size, bold/italic, all underlines, color, highlight, strike, sub/super, caps, spacing, shading, border, emphasis marks |
| `Samples/ParagraphFormattingSamples.cs` | ParagraphProperties: justification, indentation, line/paragraph spacing, keep/widow, outline level, borders, tabs, numbering, bidi, frame |
| `Samples/TableSamples.cs` | Tables: borders, grid, cell props, margins, row height, header repeat, merge (H+V), nested, floating, three-line ÃƒÂ¤Ã‚Â¸Ã¢â‚¬Â°ÃƒÂ§Ã‚ÂºÃ‚Â¿ÃƒÂ¨Ã‚Â¡Ã‚Â¨, zebra striping |
| `Samples/HeaderFooterSamples.cs` | Headers/footers: page numbers, "Page X of Y", first/even/odd, logo image, table layout, ÃƒÂ¥Ã¢â‚¬Â¦Ã‚Â¬ÃƒÂ¦Ã¢â‚¬â€œÃ¢â‚¬Â¡ "-X-", per-section |
| `Samples/ImageSamples.cs` | Images: inline, floating, text wrapping, border, alt text, in header/table, replace, SVG fallback, dimension calc |
| `Samples/ListAndNumberingSamples.cs` | Numbering: bullets, multi-level decimal, custom symbols, outlineÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢headings, legal, Chinese ÃƒÂ¤Ã‚Â¸Ã¢â€šÂ¬/ÃƒÂ¯Ã‚Â¼Ã‹â€ ÃƒÂ¤Ã‚Â¸Ã¢â€šÂ¬ÃƒÂ¯Ã‚Â¼Ã¢â‚¬Â°/1./(1), restart/continue |
| `Samples/FieldAndTocSamples.cs` | Fields: TOC, SimpleField vs complex field, DATE/PAGE/REF/SEQ/MERGEFIELD/IF/STYLEREF, TOC styles |
| `Samples/FootnoteAndCommentSamples.cs` | Footnotes, endnotes, comments (4-file system), bookmarks, hyperlinks (internal + external) |
| `Samples/TrackChangesSamples.cs` | Revisions: insertions (w:t), deletions (w:delText!), formatting changes, accept/reject all, move tracking |
| `Samples/AestheticRecipeSamples.cs` | 13 aesthetic recipes from authoritative sources: ModernCorporate, AcademicThesis, ExecutiveBrief, ChineseGovernment (GB/T 9704), MinimalModern, IEEE Conference, ACM sigconf, APA 7th, MLA 9th, Chicago/Turabian, Springer LNCS, Nature, HBR ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â each with exact values from official style guides |

Note: `Samples/` path is relative to `scripts/dotnet/MiniMaxAIDocx.Core/`.

### Markdown references (read when you need specifications or design rules)

| File | When |
|------|------|
| `references/openxml_element_order.md` | XML element ordering rules (prevents corruption) |
| `references/openxml_units.md` | Unit conversion: DXA, EMU, half-points, eighth-points |
| `references/openxml_encyclopedia_part1.md` | Detailed C# encyclopedia: document creation, styles, character & paragraph formatting |
| `references/openxml_encyclopedia_part2.md` | Detailed C# encyclopedia: page setup, tables, headers/footers, sections, doc properties |
| `references/openxml_encyclopedia_part3.md` | Detailed C# encyclopedia: TOC, footnotes, fields, track changes, comments, images, math, numbering, protection |
| `references/typography_guide.md` | Font pairing, sizes, spacing, page layout, table design, color schemes |
| `references/cjk_typography.md` | CJK fonts, ÃƒÂ¥Ã‚Â­Ã¢â‚¬â€ÃƒÂ¥Ã‚ÂÃ‚Â· sizes, RunFonts mapping, GB/T 9704 ÃƒÂ¥Ã¢â‚¬Â¦Ã‚Â¬ÃƒÂ¦Ã¢â‚¬â€œÃ¢â‚¬Â¡ standard |
| `references/cjk_university_template_guide.md` | Chinese university thesis templates: numeric styleIds (1/2/3 vs Heading1), document zone structure (coverÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢abstractÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢TOCÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢bodyÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢references), font expectations, common mistakes |
| `references/design_principles.md` | **Aesthetic foundations**: 6 design principles (white space, contrast/scale, proximity, alignment, repetition, hierarchy) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â teaches WHY, not just WHAT |
| `references/design_good_bad_examples.md` | **Good vs Bad comparisons**: 10 categories of typography mistakes with OpenXML values, ASCII mockups, and fixes |
| `references/track_changes_guide.md` | Revision marks deep dive |
| `references/troubleshooting.md` | **Symptom-driven fixes**: 13 common problems indexed by what you SEE (headings wrong, images missing, TOC broken, etc.) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â search by symptom, find the fix |
