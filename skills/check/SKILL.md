---
name: check
description: "Pure diagnostic. Reports violations; writes nothing to SPEC or code except auto-commit of `.spec/check-state.json` on clean run per check-memo-commit (carve-out to read-only-diagnostic); user decides other remedies. Only sibling state: memo in REPO-LOCAL `.spec/` (cache, not s..."
---
# check ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â drift report

Pure diagnostic. Reports violations; writes nothing to SPEC or code except auto-commit of `.spec/check-state.json` on clean run per check-memo-commit (carve-out to read-only-diagnostic); user decides other remedies. Only sibling state: memo in REPO-LOCAL `.spec/` (cache, not source of truth ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â code + SPEC.md are truth). Mechanical audits owned by published script per mechanical-realization invariant ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â never re-derive its greps per run. Behavioral judgment stays LLM. Recipes parametric per parametric-recipe invariant ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â repo-specific extensions: `.opencode/scripts/check-extras.sh` hook (mechanical, run by script) + `.opencode/check-extras.md` (judgment-class, consulted by LLM). Read-only ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ sub-agent delegation safe throughout.

## LOAD

1. Load spec overview (SCOPE, not whole-file Read per single-load invariant) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `python3 ~/.opencode/scripts/check-mechanical.py emit-overview`. Prints Ãƒâ€šÃ‚Â§G/Ãƒâ€šÃ‚Â§C/Ãƒâ€šÃ‚Â§I/Ãƒâ€šÃ‚Â§T/Ãƒâ€šÃ‚Â§B bodies + Ãƒâ€šÃ‚Â§V id list (no Ãƒâ€šÃ‚Â§V bodies ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â those arrive via `emit-v-slices` step 4; whole-file Read here double-loads SPEC.md + re-hits the Read token cap). Script exits non-zero "no SPEC.md" ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ "no spec, nothing to check." Stop.
2. Parse `$ARGUMENTS` (two forms only, per dispatch invariant):
   - bare ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ memo-driven default sweep: invariants + interfaces + tasks. Memo absent or invalidated ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ full re-classify. Fresh memo written on clean.
   - `--full` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ delete `.spec/check-state.json` upfront, classify all rows, propagate `--full` to audit script (restores per-row history listing instead of aggregation). Interrupt mid-run ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ no memo ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ next run also full ("don't trust cache" fails safe).
   - other ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ bail w/ `unknown arg <arg> ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â accepted forms: bare invocation, --full`. Legacy section-name args and multi-flag forms retired.
3. Run audit script (MECHANICAL CORE). Its `memo|ADVISORY|ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦` rows report fired invalidation triggers + the `v_row_shas` dirty set that scopes Ãƒâ€šÃ‚Â§V re-classification.
4. Ãƒâ€šÃ‚Â§V row bodies come from the script's `emit-v-slices` mode (SCOPE), never whole-file Read ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â large SPEC paginates past the Read token cap. Script slice is canonical Ãƒâ€šÃ‚Â§V-body source for single-agent and sub-agent paths.

## MECHANICAL CORE ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â audit script

Deterministic audit set ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â SPEC-FORMAT structural rules (section catalog + order, row grammar, rightmost-`|` column extraction, archive markers + sibling shape), `Ãƒâ€šÃ‚Â§T` cite / `Ãƒâ€šÃ‚Â§B` fix grammar, monotonic-ID, cite-DAG resolution + edge-type, history-residue patterns + pre-filters + oversized-cell advisory, pinned-invariant-header grep, MECHANIZE-block byte-identity across the user-invocable SKILL.md set, auto-fire sub-skill invocation ban, token estimate ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â owned by `scripts/check-mechanical.py` (deployed to `~/.opencode/scripts/check-mechanical.py`). Script regex is single source of truth; per-run paraphrase not permitted (mirrors canonical-agent-block verbatim contract) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the MECHANIZE-block check supersedes any hand-run `awk|md5|uniq` block sweep, the dispatch-target check any hand-run skill-body invocation grep.

Run at audit start (git stays unused ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â all rev-parse/show/diff run inside the script):

```
python3 ~/.opencode/scripts/check-mechanical.py audit [--full]
```

Reads `SPEC.md` (+ `SPEC.archive.md` sibling if exists) from cwd; discovers PUBLISHED scope from `skills/*/SKILL.md` directory walk (`name` frontmatter = skill name; description starting with "Internal ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â not for direct invocation" = internal sub-skill); probes `.opencode/scripts/check-extras.sh` (exists + executable ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ run, append its `id|verdict|evidence` rows ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â language-agnostic contract). Emits pipe-table `id|verdict|evidence`:

- `format|VIOLATE|format: <detail>` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â SPEC-FORMAT breach.
- `cite|UNRESOLVED|<citer> <id> ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦` / `cite|TYPE-MISMATCH|ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â cite-DAG. `cite|ambiguous|ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦` = bare-form phase-label / gate-ID collision subset ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ LLM adjudicates per CHECK Ãƒâ€šÃ‚Â§-cite.
- `history|VIOLATE|<row> ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦ history: <pattern>` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â inlined-history residue. `history|ADVISORY|oversized cells ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦` = smell, not VIOLATE.
- `pinned-header|VIOLATE|<file:line> ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â PUBLISHED body pins invariant number in header.
- `mechanize|DRIFT|<path> ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦ md5 <a> != <b>` / `mechanize|MISSING|<path> ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â user-invocable `skills/*/SKILL.md` (minus internal sub-skills `backprop`, `socratic`, `steno`, `telegraph`, `monitor`) carries the byte-identical canonical MECHANIZE block per mechanize-scan invariant; DRIFT = divergent block, MISSING = absent sentinel. Script-owned byte-identity check ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â never hand-run `awk|md5|uniq` per run.
- `dispatch|VIOLATE|<path:line> ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦ names internal sub-skill for direct invocation <cmd>` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â a skill body names an internal sub-skill for direct invocation per response-shape invariant; direct invocation of internal skills is never a valid dispatch target (backtick-wrapped exempt). Sub-skill set derived from description convention ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â script-owned, never hand-grep skill bodies per run (closes Ãƒâ€šÃ‚Â§B.<n>).
- `grant|SKIP|<path> tool unused, no frontmatter grants exist in opencode>` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â opencode skills do not use `allowed-tools` frontmatter; tool access is managed globally in `opencode.jsonc` (deployed to `~/.config/opencode/opencode.jsonc`). This check is a no-op in opencode context (preserved for cross-format compatibility).
- `token|ADVISORY|SPEC.md ~<n>k tokens > budget ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â estimate `bytes/3.4` per token-budget invariant.
- `memo|ADVISORY|<trigger>` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â invalidation (`schema_version` mismatch or `last_clean_sha` unreachable ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ drop memo, full sweep) or scope feed `v_row_shas drift: V<n>,ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦`.
- `tasks|ADVISORY|flipped-since-clean: T<n>,ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Ãƒâ€šÃ‚Â§T rows flipped `.`ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢`x` since clean sha.
- `diff|ADVISORY|touched: <paths>` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â paths changed since clean sha.
- `batch|ADVISORY|recommended: <n> agents` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Ãƒâ€šÃ‚Â§V-classification sub-agent count from Ãƒâ€šÃ‚Â§V row count + PUBLISHED file census per batch invariant; consumed by Batch protocol step 1, never hand-computed.

Merge into REPORT verbatim: `format` / `history` / `cite` / `pinned-header` / `mechanize` / `dispatch` / `grant` rows ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ their REPORT blocks (`mechanize` DRIFT/MISSING + `dispatch` VIOLATE + `grant` SKIP ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ invariant drift); `token` + `memo`-invalidation ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `## advisory`. Scope-feed rows (`memo` drift, `tasks` flipped-set, `diff` touched-set) carry stable comma-joined fields consumed machine-side ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â chained into `emit-v-slices --dirty`, never surfaced in advisory, never hand-rolled via `git diff`. `batch|ADVISORY` likewise consumed machine-side (Batch protocol step 1), never surfaced in advisory.

## MEMO

`.spec/check-state.json`, schema v3:

```json
{
  "schema_version": 3,
  "last_clean_sha": "<git HEAD @ last clean run>",
  "v_row_shas": { "V<n>": "<sha256 of Ãƒâ€šÃ‚Â§V row body>" },
  "last_run_at": "<ISO-8601 timestamp>",
  "last_v_classifications": { "V<n>": "HOLD|HOLD-SINCE-CLEAN|SCOPE-EMPTY|VIOLATE-CAPTURED|LATENT" },
  "oversized_cell_ack": "<sha256 over sorted oversized cell-id set>"
}
```

Script owns both ends per memo invariant:

- **read** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `audit` mode emits `memo|ADVISORY|ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦` per fired trigger. Per-row `v_row_shas` drift ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ only edited Ãƒâ€šÃ‚Â§V rows re-classify; hash-stable rows carry forward HOLD-SINCE-CLEAN. `oversized_cell_ack` suppresses the oversized-cells advisory while the acknowledged set is unchanged; re-fires on new cell (acknowledged smell not re-nagged).
- **write** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `write-memo` mode (WRITE-MEMO) computes clean-set membership, per-row hashes, ack, idempotent `.opencode/.gitignore` guard. LLM never decides clean, never hand-writes memo.

Memo update = side-effect of every clean run, no user prompt. Ãƒâ€šÃ‚Â§V non-row content (archive-marker line) unhashed ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ no re-classify on edit; format audit covers marker shape.

## SCOPE ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â memo-driven default

Both scope dimensions script-emitted; LLM consumes the scope-feed rows, never hand-rolls `git diff`. Memo valid ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢

1. **Ãƒâ€šÃ‚Â§V dirty** = rows in `memo|ADVISORY|v_row_shas drift` + rows whose body path tokens (quoted/backticked path-like strings) intersect `diff|ADVISORY|touched`. Neither source ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ emit `V<n> HOLD-SINCE-CLEAN`, skip.
2. **Ãƒâ€šÃ‚Â§T** re-verify scoped to `tasks|ADVISORY|flipped-since-clean` rows. Historical `x` unchanged ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ HOLD-SINCE-CLEAN.
3. **Ãƒâ€šÃ‚Â§I + cite-DAG** full-sweep every run (cite-DAG owned by script; Ãƒâ€šÃ‚Â§I shape-diff cheap, no triage gain).

First-run, invalidated memo, or `--full` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ classify all Ãƒâ€šÃ‚Â§V rows.

Ãƒâ€šÃ‚Â§V bodies for the classified set:

```
python3 ~/.opencode/scripts/check-mechanical.py emit-v-slices [--dirty V<n>,...]
```

Prints each Ãƒâ€šÃ‚Â§V row body w/ source range ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â header `## V<n> SPEC.md:<start>-<end>` + verbatim row text. `--dirty` = comma-list from step 1; omit on first-run / `--full` (all rows). Sidesteps Read pagination, not bulk-load cost: single-agent path loads full slice set in-thread (may spill to persisted file past inline output cap); sub-agent batches distribute per spawn.

## CHECK invariants

Script never classifies behavior ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Ãƒâ€šÃ‚Â§V claim ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ verifiable-code-claim translation + verdict stays LLM. For each dirty `V<n>`:

1. Translate invariant ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ verifiable claim about code.
2. Recipe scope (invariant may reduce scope per scope-set invariant, e.g. PUBLISHED-only; default full repo). Touch set = script touched-set intersect scope; first-run / `--full` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ scope itself.
3. Touch set empty ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `V<n> SCOPE-EMPTY: <reason>`, evidence `scope-touch overlap empty`, skip grep. Silence differs verified-absence.
4. Row clean since `last_clean_sha` + scope untouched ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `V<n> HOLD-SINCE-CLEAN`, evidence `HOLD-since-clean @ <last_clean_sha>`, skip grep.
5. Else grep/read relevant files; verdict in {HOLD, VIOLATE, VIOLATE-CAPTURED, UNVERIFIABLE, SCOPE-EMPTY, HOLD-SINCE-CLEAN, LATENT} per drift-verdict-vocab invariant.
   - Surfaced {VIOLATE, VIOLATE-CAPTURED, UNVERIFIABLE} ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ REPORT body row + distinct remedy hint.
   - Silence {HOLD, HOLD-SINCE-CLEAN, SCOPE-EMPTY, LATENT} ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ no body row, no hint; collapse to summary `suppressed` count w/ per-reason breakdown. Verdicts still recorded in memo (`last_v_classifications`).
   - VIOLATE-CAPTURED = live violation, `Ãƒâ€šÃ‚Â§B`-recorded, remediation forward-only (e.g. historical commit body) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ emit `<row-id> VIOLATE-CAPTURED: <evidence>; see Ãƒâ€šÃ‚Â§B.<n>`; classify on `Ãƒâ€šÃ‚Â§B` cite presence (e.g. captured-sha list in REPO-LOCAL extension).
   - LATENT = trigger condition structurally absent from repo state ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ audit no-op until condition fires. Differs UNVERIFIABLE (missing audit infrastructure for an otherwise-verifiable claim).
6. Record file:line evidence.

Recipes never name repo-literal paths beyond `SPEC.md`. Repo-specific enforcement ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ extras hook + extras md per LOAD.

### Batch protocol (parallel invariant audit)

Invariant audit MAY parallelize via Explore sub-agents:

1. **Batch count** = the audit's `batch|ADVISORY|recommended: <n> agents` row ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â script-computed from Ãƒâ€šÃ‚Â§V row count + PUBLISHED file census; formula owned by the script per mechanical-realization invariant, never re-derived here. `n` = 1 ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ main-thread single-agent path. Narrow-scope collapse (PUBLISHED census small vs Ãƒâ€šÃ‚Â§V count ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ fewer agents amortize cross-cutting greps better) folds into the row already, closing the eyeballed-file-count proxy class (Ãƒâ€šÃ‚Â§B.<n>).
2. **Partition** = contiguous V<n> spans per batch (cite locality ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ shared file reads).
3. **Prompt** = canonical block below, copied verbatim per batch, fill only `{...}` placeholders ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â no paraphrase, no per-call schema improvisation. `{V_SLICE}` + `{LINE_START}`/`{LINE_END}` filled from `emit-v-slices` output (batch = contiguous span; line bounds from the `## V<n> SPEC.md:<start>-<end>` headers), never re-Read SPEC.md. Single-agent path sources same slice in-thread.
4. **Aggregate** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â main thread concatenates per-batch tables ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ REPORT invariant drift block.
5. **Failure** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â agent error or timeout ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ re-run that range serially (strict fallback, not retry); other batch results retained.

Cite-DAG, format, history, pinned-header, mechanize-block, dispatch-target, grant-use stay w/ the script ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â never delegated to Ãƒâ€šÃ‚Â§V batches.

#### Canonical agent prompt block

```
You are an invariants audit sub-agent. Read-only tools (Explore-class palette). No edits, no commits.

INPUT ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â SPEC.md invariants slice (lines {LINE_START}ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“{LINE_END}):

{V_SLICE}

INPUT ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â audit recipe (CHECK invariants step 5 behavioral-claim classification + judgment-class REPO-LOCAL extras from `.opencode/check-extras.md`, verbatim):

{RECIPE_EXCERPT}

INPUT ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â scope sets (per scope-set invariant in SPEC.md):

PUBLISHED = {PUBLISHED_PATHS}
REPO-LOCAL = {REPO_LOCAL_PATHS}
SPEC-ADJACENT = {SPEC_ADJACENT_PATHS}
GITHUB-FACING = {GITHUB_FACING_PATHS}

OUTPUT ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â pipe-table only. Columns: `id|verdict|evidence`.

- `id` is invariant row identifier (`V<n>`).
- `verdict` in {HOLD, VIOLATE, VIOLATE-CAPTURED, UNVERIFIABLE, SCOPE-EMPTY, HOLD-SINCE-CLEAN, LATENT}.
- `evidence` ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â¤ 1 line, one of `file:line` or `no test covers ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦` or `scope-touch overlap empty` or `HOLD-since-clean @ <sha>` or `<file:line>; see Ãƒâ€šÃ‚Â§B.<n>` (VIOLATE-CAPTURED form) or `<trigger-condition-absent reason>` (LATENT form).

No prose preamble before the table. No trailing summary after the table. No commentary between rows. Pipe-table only ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â first line is header `id|verdict|evidence`, subsequent lines one row per assigned V<n>.
```

Block = single source of truth for sub-agent input + output shape; verbatim-copy contract closes the dispatcher-improvisation class.

## CHECK Ãƒâ€šÃ‚Â§-cite ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â ambiguous adjudication

Mechanical cite-DAG resolution (typed-prefix cites ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ expected-section rows, archive-probe, backtick pre-filter) owned by script ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `cite|UNRESOLVED` + `cite|TYPE-MISMATCH` fold into REPORT cite drift. LLM adjudicates only `cite|ambiguous|ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦` (bare-form phase-label / gate-ID collisions) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â per-hit verdict in {spec-cite, phase-label, ambiguous}; clear cases auto-classify, residual ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ operator review. Never re-run mechanical resolution. Script's edge set = authoritative citer list for the spec skill renumber-sweep.

## CHECK interfaces

For each I item: locate implementation; classify

- **MATCH** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â code shape = spec shape.
- **DRIFT** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â impl exists, shape differs.
- **MISSING** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â impl absent.
- **EXTRA** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â code exposes surface not in interfaces section.

### List-shape sub-recipe

Interface field w/ enumerated list (verb set, cmd set, tool list, config keys, env vars) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ mechanical set-diff, not manual re-read: extract spec set; build code symbol set via grep or AST (CLI verb registry, exported cmd map, config-key constants); `spec - code` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ MISSING, `code - spec` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ EXTRA. Catches enumerated drift free-text re-read slips past.

## CHECK tasks

For each T<n>:

1. `x` + predates `last_clean_sha` per memo ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `T<n> HOLD-SINCE-CLEAN`, skip re-verify.
2. `x` flipped since memo (or first-run / `--full`) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ verify claimed work present; no evidence ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ flag **STALE**.
3. `.` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ note pending.

## REPORT

Telegraph register, grouped by severity. Mechanical rows from script merge into their blocks; behavioral `V<n>` from Ãƒâ€šÃ‚Â§V batches; `I.<key>` / `T<n>` from interface + task audits.

```
## invariant drift
V<n> VIOLATE: auth/mw.go:47 uses `<` not `ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â¤`. see Ãƒâ€šÃ‚Â§B.<n>.
V<n> VIOLATE-CAPTURED: <commit-sha> body contains heavy math operators; see Ãƒâ€šÃ‚Â§B.<n>.
V<n> UNVERIFIABLE: no test covers every req path.
Ãƒâ€šÃ‚Â§T.<n> VIOLATE: history: dated-retirement in task body ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â prune per freshness-contract invariant.
mechanize DRIFT: skills/explain/SKILL.md MECHANIZE block diverges from canonical.
dispatch VIOLATE: skills/build/SKILL.md:96 references internal sub-skill for direct invocation.
grant SKIP: opencode skills do not use allowed-tools frontmatter.

## cite drift
T<n>.cites V<m> UNRESOLVED: V<m> absent from invariants section.
Ãƒâ€šÃ‚Â§B.<n>.fix T<k> TYPE-MISMATCH: target is task row, expected invariant row.
AGENTS.md:<line> cite UNRESOLVED: row absent.

## interface drift
I.api DRIFT: POST /x returns `{result}` not `{id}`. route.go:112.
I.cmd MISSING: `foo bar` absent from cli/*.go.

## task drift
T<n> STALE: status `x`, no middleware file exists.

## summary
2 violate. 1 violate-captured. 1 missing. 1 stale. 1 unverifiable. 1 unresolved. 1 type-mismatch. 5 suppressed (1 scope-empty, 2 hold-since-clean, 2 latent).
```

Silence-class verdicts excluded from body ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â collapsed in summary `suppressed` count w/ per-reason breakdown. Rows roll forward run-to-run; HOLD re-verifies on next dirty-scope hit; LATENT re-classifies when trigger fires; HOLD-SINCE-CLEAN re-verifies on touch-set intersect; SCOPE-EMPTY re-verifies on scope expansion.

**Body-row aggregation** (mechanical core): `history`-class VIOLATE rows collapse per section (Ãƒâ€šÃ‚Â§V/Ãƒâ€šÃ‚Â§T/Ãƒâ€šÃ‚Â§B) when section count > threshold (script-owned) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ single summary row `Ãƒâ€šÃ‚Â§<S>: <n> rows (<count> <pattern>, ...) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ invoke the condense skill for body-trim` w/ breakdown across {amendment-counter, dated-retirement, supersession-narration}; below-threshold sections keep per-row form. `--full` restores per-row listing.

```
## invariant drift
Ãƒâ€šÃ‚Â§V: 49 rows (29 amendment-counter, 12 dated-retirement, 8 supersession-narration) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ invoke the condense skill for body-trim
Ãƒâ€šÃ‚Â§B.<n> VIOLATE: history: amendment-counter @ SPEC.md:<line>
```

**Checkpoint** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â clean-run REPORT ! contain `## checkpoint` H2 reflecting `write-memo` + `AUTO-COMMIT` outcome, single line before `## summary` (state mutation needs salient signal, not buried prose):

- memo advanced + auto-commit landed ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `clean ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ memo <old-sha> ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ <new-sha> ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ commit <commit-sha>`
- memo unchanged (no auto-commit needed) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `clean ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â memo @ <sha>`
- dirty run (any VIOLATE / DRIFT / MISSING / STALE / UNRESOLVED / TYPE-MISMATCH) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ omit section.

**Advisory** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â fired conditions ! emit `## advisory` H2 between `## checkpoint` and `## summary` (or leading output when no checkpoint). One line per fired `token|ADVISORY` / `memo|ADVISORY` / `history|ADVISORY` row. No line ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ omit heading.

```
## checkpoint
clean ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â memo @ 060a9d2

## advisory
memo schema_version mismatch ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â memo dropped, full sweep
SPEC.md ~30k tokens > 20k budget; consider invoking the condense skill

## summary
0 violate. 1 violate-captured. 39 suppressed (18 hold-since-clean, 2 latent, 19 hold).
```

## WRITE-MEMO

Source the live id-set skeleton from the script ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â never hand-enumerate (closes omitted-row silent-undercoverage class):

```
python3 ~/.opencode/scripts/check-mechanical.py emit-row-ids
```

Emits one blank-verdict row per live Ãƒâ€šÃ‚Â§V/Ãƒâ€šÃ‚Â§I/Ãƒâ€šÃ‚Â§T id (`id||`, header `id|verdict|evidence`). Fill verdicts + evidence from REPORT classification ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â behavioral rows only (Ãƒâ€šÃ‚Â§V/Ãƒâ€šÃ‚Â§I/Ãƒâ€šÃ‚Â§T); never hand-merge the `audit` mechanical rows (memo invariant). Feed the filled skeleton to stdin; `--from-audit` re-runs the mechanical audit internally + merges it:

```
python3 ~/.opencode/scripts/check-mechanical.py write-memo --from-audit < <filled-skeleton>
```

Script merges its internal mechanical audit w/ the behavioral rows, validates vocab per row type, computes clean-set membership (clean iff no VIOLATE / UNVERIFIABLE / UNRESOLVED / TYPE-MISMATCH / DRIFT / MISSING / STALE / EXTRA), writes memo only when clean (schema v3, per-row hashes, `last_clean_sha` = HEAD, oversized-cell ack, `.gitignore` guard). Exit `0` = clean (memo advanced); `1` = dirty (memo untouched, offenders on stderr ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â CI-gateable); `2` = invalid vocab. `## checkpoint` line reflects the outcome.

## AUTO-COMMIT (check-memo-commit)

On clean audit (`write-memo` exit 0) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ auto-commit `.spec/check-state.json` w/o operator prompt (check-memo-commit carve-out to read-only-diagnostic for this file only):

```bash
git add .spec/check-state.json
git commit -m "check: memo @ <short-sha>" \
           -m "auto-advance check memo on clean run (check-memo-commit)" \
           -- .spec/check-state.json
```

Path-scoped per write-ownership (`-m` flags precede `--`); pre-staged files never leak. Pre-flight: `git status --porcelain -- .spec/check-state.json` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ empty = no-op (tracked file clean vs HEAD, skip commit silently). `git add` is run unconditionally before the commit (idempotent ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â no-op if file already staged at HEAD content); for a previously-untracked file this transitions it to staged and the commit creates the tracking entry. On dirty run (`write-memo` exit 1) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ no auto-commit (check-memo-commit gate unsatisfied); checkpoint section omits commit line. No new operator `## Next` item ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â auto-commit is internal mutation, not a dispatch surface.

## REMEDY HINTS

Populate the Next block (not a separate section) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â map drift classes ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ candidate items, surface most acute:

- VIOLATE / DRIFT ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ invoke the spec skill with `<description citing Ãƒâ€šÃ‚Â§V.<n>>` (gate routes to BACKPROP).
- VIOLATE-CAPTURED ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ no action; baseline `Ãƒâ€šÃ‚Â§B`-recorded, remediation forward-only.
- `history:` VIOLATE ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ invoke the spec skill to `amend Ãƒâ€šÃ‚Â§<S>.<n>` to prune inlined history; task-row residue ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ invoke the condense skill for body-trim.
- `format:` VIOLATE ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ invoke the spec skill to `amend Ãƒâ€šÃ‚Â§<S>.<n>` (or invoke the condense skill when archive-marker / window split).
- SUPPRESSED ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ no action; rolls forward until trigger fires / touch intersects / scope expands.
- MISSING ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ invoke the build skill with `<task-cite>` if task exists; else invoke the spec skill to `amend task` to add row.
- STALE ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ invoke the spec skill to `amend <task-cite>` to uncheck status.
- EXTRA ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ invariant mandates the surface ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ invoke the spec skill to `amend interfaces` (cause known); invariant silent ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ invoke the spec skill with `<surface> missing from interfaces section` (cause TBD, `Ãƒâ€šÃ‚Â§B` row starts conversation).
- UNRESOLVED / TYPE-MISMATCH ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ invoke the spec skill to `amend Ãƒâ€šÃ‚Â§<S>.<n>` to repair stale or wrong-section cite.

Never invoke fixes. Report only.

## MECHANIZE ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â script-candidate scan

Recipe end ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ before the `## Next` block, scan this run for a mechanization candidate. Candidate = any of:

- ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â¥ 2 same-shape deterministic calls this run (identical command modulo args)
- LLM-side join / sort / count / dedup over script-emittable data
- multi-step parse collapsible to one script emit mode
- fresh regex paraphrase of an existing mechanical rule (mechanical-realization invariant class)

Hit ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ emit exactly one `## Next` item naming the observed pattern + proposed script mode; none ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ no item. Never self-implement the mechanization mid-run (recipe-step-no-dispatch + write-ownership invariants). Route by cwd:

- dev repo (this skill pack) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ invoke the spec skill ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ new Ãƒâ€šÃ‚Â§T row
- consumer repo ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ invoke the spec skill ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `.opencode/check-extras` row

## OUTPUT ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â "Next" block

Heading `## Next`; 1ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“5 atomic items (one sentence each, no `Reply` prefix); skill invocation dispatch. Items are skill invocations; before invoking the build skill with `--next` confirm ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â¥ 1 pending `.` task else suggest invoking the spec skill to seed. Optional `## Hint` (ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â¤ 3 lines) precedes when item selection needs hidden state (severity order VIOLATE > DRIFT > MISSING > STALE > EXTRA; record-vs-amend choice).

Example (drift found):

```
## summary
1 violate. 1 drift.

## Hint

VIOLATE outranks DRIFT ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â record the V<n> breach via item 1 before fixing the interface drift, so `Ãƒâ€šÃ‚Â§B` captures the cause not just the symptom.

## Next

1. invoke the spec skill: V<n> violated at auth/mw.go ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â record the drift
2. invoke the spec skill: I.api drifted at route.go ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â record interface drift
```

Variants: clean + pending `.` task ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ invoke the build skill with `--next` + invoke the check skill later; terminal (all closed, clean) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ invoke the spec skill to seed.

## NON-GOALS

- Zero writes to SPEC or code except `.spec/check-state.json` auto-commit on clean run per check-memo-commit. Memo written by the script's `write-memo` mode only.
- Mechanical audits stay in the script; behavioral Ãƒâ€šÃ‚Â§V classification, interface shape-diff, task STALE-verify stay LLM; reads delegable to Explore sub-agents.
- No scores, no grades. Binary per item: holds or drifts.
