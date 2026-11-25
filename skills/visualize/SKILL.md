---
name: visualize
description: "Generate plots/charts/graphs from CSV or JSON via `vl2svg` (Vega-Lite), with column-type detection and chart-type recommendation."
---
# Data Visualization Creator

Generate plots/charts/graphs from CSV or JSON via `vl2svg` (Vega-Lite), with
column-type detection and chart-type recommendation.

## When to use

- User wants a **chart/plot/graph** from tabular data (file or pasted table).
- Do **not** use for architecture/sequence diagrams ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `diagram`.
- Do **not** use for generative art, posters, or non-data images.

## Prerequisites

- `python3` and this skill's `main.py` (path: skill directory next to this file).
- `vl2svg` on PATH: `npm install -g vega-cli vega-lite`.
- Files ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â¥10MB also need `duckdb` on PATH.

## Procedure

Work phases in order. Do not skip. Do not invent column names ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â only use
fields from `analyze` output (or exact user overrides that exist in that output).

### Phase 1 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Materialize data

1. If data is already a file path the user gave, use it as `--data_path`.
2. If the user pasted a table / inline JSON/CSV, write it to a file in the
   **session scratch directory** (temp). Do not write into the project working
   directory unless the user explicitly asks to save there.
3. Completion: a real filesystem path exists and is readable.

### Phase 2 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Analyze

1. Run (from skill dir or with absolute path to `main.py`):

   ```bash
   python3 <skill-dir>/main.py analyze --data_path <path>
   ```

2. Read the JSON stdout. On `"status": "error"`, report `reason` and STOP
   (or fix path/format and re-run once).
3. Note `recommended_chart_type`, `recommended_x`, `recommended_y`, column
   `type` / `cardinality` / `null_count`. For large files note `"engine":
   "duckdb"` and `size_mb`.
4. Completion: you have recommended chart + axes (or a clear error reported).

### Phase 3 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Choose encoding

1. Default to recommended chart/x/y from analyze.
2. If the user named a chart type or axes, prefer their choice **only if**
   those fields appear in `columns`. If not, re-check analyze and ask once.
3. Chart intents: bar = category vs measure; line = temporal vs measure;
   scatter = two numerics; pie = few categories (ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â¤6) + measure.
4. Completion: concrete `chart_type`, `x_axis`, `y_axis` (y may be null only
   if analyze allowed it and user wants category counts ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â otherwise require y).

### Phase 4 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Render

1. Pick `--output_path` in scratch (or user-requested path). Prefer `.svg`.

   ```bash
   python3 <skill-dir>/main.py render \
     --data_path <path> \
     --chart_type <bar|scatter|line|pie> \
     --x_axis <field> \
     --y_axis <field> \
     --output_path <out.svg>
   ```

2. On success JSON: keep `output_path`. On error JSON: report `reason` /
   `stage`; if invalid field, re-run Phase 2 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â do not blind-retry.
3. If `"aggregated": true`, you **must** tell the user what was aggregated
   or sampled (`aggregation` field). Never imply every row was plotted.
4. Completion: SVG exists at `output_path`, or structured error reported.

### Phase 5 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Respond

1. Report chart type, axes, and SVG path.
2. Mention aggregation/sampling when present.
3. PNG only if user asked: rasterize SVG separately (`rsvg-convert` or
   `vl2png`); this skill does not emit PNG by default.
4. Completion: user has path + one-line interpretation of the chart.

## Edge cases (summary)

- Empty file / no rows ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ analyze error; stop and say so.
- Missing `vl2svg` / `duckdb` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ report install hint from error JSON; stop.
- Unknown columns ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ list columns from analyze; do not guess.
- Wide tables: recommend using analyze picks; do not plot all columns at once.
- Details and decision table: load `references/chart-selection.md` only if
  recommendation is ambiguous or user asks why a type was chosen.

## Examples

### Happy path

- User: "Make a bar chart of revenue by region from `sales.csv`"
- You: analyze ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ render bar with region/revenue ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ return SVG path.

### Inline data

- User pastes a markdown table ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ write temp CSV ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ analyze ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ render ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ SVG.

### Non-trigger

- User: "Draw the checkout service architecture" ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ do **not** use this skill
  (use `diagram`).
