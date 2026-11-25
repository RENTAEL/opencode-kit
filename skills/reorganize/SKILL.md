---
name: reorganize
description: "Operator-triggered clarity-shape pass over SPEC.md Ãƒâ€šÃ‚Â§V. Cadence ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â¤ once per major epoch (months) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â skill body documents intent; check skill does not enforce. Single atomic commit, rollback via `git revert`."
---
# reorganize ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Ãƒâ€šÃ‚Â§V cluster + renumber + cite-DAG sweep

Operator-triggered clarity-shape pass over SPEC.md Ãƒâ€šÃ‚Â§V. Cadence ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â¤ once per major epoch (months) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â skill body documents intent; check skill does not enforce. Single atomic commit, rollback via `git revert`.

## PREAMBLE

State-mutator scoped to SPEC.md + `.spec/spec-clusters.json` + `.spec/spec-renumber-map.json` + cite-DAG sweep targets (PUBLISHED + REPO-LOCAL + SPEC.md internal + `SPEC.archive.md` when exists). Operator invokes only per recipe-step-no-dispatch rule. Owns Ãƒâ€šÃ‚Â§V renumber permission carved out of monotonic-id invariant.

Distinct from the condense skill: condense = token reduction (folds, archives, trims); reorganize = clarity shape (cluster + renumber) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â not token drop, not row folds. Writes serialize main-thread per write-serialize invariant; classification reads delegable to sub-agents. Single commit per atomic-operation discipline, not partial application; cite-DAG sweep per cite-resolution invariant rides same commit.

## LOAD

1. Read `SPEC.md`. Missing ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ "no spec, nothing to reorganize." Stop.
2. Read `skills/spec/SPEC-FORMAT.md` (deployed to `~/.opencode/skills/spec/SPEC-FORMAT.md`) every row schema and section catalog.
3. Parse `$ARGUMENTS`: empty ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ full cluster + renumber + sweep propose; `--taxonomy-only` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ PROPOSE report only, not mutation.
4. Discovery probe ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â repo-agnostic skill pack scope per published-scope invariant:
   - (a) `skills/*/SKILL.md` exists ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ parse frontmatter `name` field; PUBLISHED = all skill dirs found. `name` field absent ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ directory name as fallback. Internal sub-skills identified by description starting with "Internal ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â not for direct invocation".
   - (b) else ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ empty map; sweep targets REPO-LOCAL + SPEC.md internal only.
5. Load `.spec/spec-clusters.json` if exists, else cold-start. Shape `[{cluster:<name>, rows:[{fingerprint:<hash>, current_id:V<n>}, ...]}, ...]`. Per-row key is Ãƒâ€šÃ‚Â§V body-text fingerprint (sha256 over row body w/o `V<n>:` prefix) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â stable across renumber; id-as-key invalidates persist every run.
6. Load `.spec/spec-renumber-map.json` if exists (chain-walk semantics on subsequent runs). Shape `[{run:<iso-date>, topic:<cluster>, old:V<n>, new:V<m>}, ...]` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â append-only; `new` admits sentinel `archive` (archived-terminus per archive-sibling schema). Provenance via `git log` on file, not in-file `run_sha`.

## ARCHIVE-RETIRED

Pre-CLUSTER. Ãƒâ€šÃ‚Â§V rows w/ body opening `retired YYYY-MM-DD` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ migrate to `SPEC.archive.md ## Ãƒâ€šÃ‚Â§V.retired` block per archive-sibling schema. Flagged rows skip cluster taxonomy, not consume new ids @ renumber.

1. Grep `^V[0-9]+:\s+retired\s+[0-9]{4}-[0-9]{2}-[0-9]{2}\b` in Ãƒâ€šÃ‚Â§V ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ flagged-set.
2. Citer-protection probe per flagged `V<n>` via cite-resolution cite-DAG: typed columns (Ãƒâ€šÃ‚Â§T.cites, Ãƒâ€šÃ‚Â§B.fix bare `V<n>`, incl. closed `x` rows) + free-text `Ãƒâ€šÃ‚Â§V.<n>` in Ãƒâ€šÃ‚Â§V/Ãƒâ€šÃ‚Â§C/Ãƒâ€šÃ‚Â§I bodies of active SPEC.md. Backtick pre-filter `` `[^`]*(Ãƒâ€šÃ‚Â§[VTB]\.[0-9]+|\b[VTB][0-9]+\b)[^`]*` `` (builtin Grep per tooling-preference invariant) excludes Ãƒâ€šÃ‚Â§B/Ãƒâ€šÃ‚Â§T narrative historical refs per verbatim-preservation invariant.
3. Live citer on any flagged row ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ bail `cannot archive Ãƒâ€šÃ‚Â§V.<n> ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â live citers: <list>`. Operator resolves pre-retry (fold cited content into surviving row, rewrite citer, or drop `retired` opener).
4. No live citers ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ flagged-set passes to PROPOSE (`## To archive` block) and EXECUTE (archive write + renumber-map sentinel per row).

## CLUSTER

LLM judgment over each non-archived Ãƒâ€šÃ‚Â§V row body ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ topic-coherent cluster. Two paths:

- **Cold-start** (no persist): propose full taxonomy from scratch. Default span 10 ids per cluster (`V<n>..V<n+9>`), operator-overridable @ PROPOSE.
- **Delta** (persist exists): fingerprint-match each current row; matched fingerprints retain cluster home, moved/new rows reassign. Emit delta-set (new, moved, dropped rows).

Cluster name = short topic-coherent noun phrase (e.g. `spec-mutator-contract`, `audit-mechanics`, `release-flow`, `cite-resolution`). Per-row assignment operator-overridable @ PROPOSE.

## PROPOSE

Render cluster diagram in steno register per github-facing-register invariant (operator-facing). Per cluster: `## <cluster-name> (V<a>..V<b>, <n> rows)` H2 w/ per-row line `- V<old> ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ V<new>: <one-line summary>`. Trailing summary `<m> clusters, <total> rows, renumber map writes <k> mappings`. Flagged-set not empty ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ sibling `## To archive` H2 w/ per-row `- V<old>: <one-line body summary>`, so subset-skip path informed @ CONFIRM.

Operator critiques boundaries, names, assignments; iterate until stable. Cold-start = full taxonomy under review; delta = changed rows + new clusters only.

`--taxonomy-only` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ emit report, stop. Not CONFIRM, not EXECUTE.

## CONFIRM

AskUserQuestion per decision-gate invariant ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â single bulk-confirm covers renumber + sweep (mid-flow re-prompt not allowed per atomic-operation discipline):

- **question**: `Reorganize SPEC.md: <m> clusters, <k> id renumbers, <a> archive-retired rows, cite-DAG sweep over <s> sites. Apply?`
- **header**: `Reorganize gate`
- **options** (3, mutually exclusive):
  - `apply renumber + cite-DAG sweep + archive-retired` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ EXECUTE w/ full map + flagged set.
  - `subset` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ operator-typed cluster list or `skip archive-retired` keyword (retains flagged rows in active Ãƒâ€šÃ‚Â§V this run); re-render PROPOSE w/ filter, re-emit CONFIRM.
  - `cancel` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ stop, no mutation.

## EXECUTE

Single atomic commit:

1. Archive-retired migration (flagged-set not empty, CONFIRM not `skip archive-retired`):
   - Append flagged rows verbatim to `SPEC.archive.md ## Ãƒâ€šÃ‚Â§V.retired` block; create if absent (sibling to `## Ãƒâ€šÃ‚Â§T TASKS` / `## Ãƒâ€šÃ‚Â§B BUGS` H2s). Preserve `V<orig-n>:` prefix + `retired YYYY-MM-DD ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â ...` body verbatim; sort ascending by orig id.
   - Drop archived rows from active Ãƒâ€šÃ‚Â§V.
   - Emit/update marker `## archived: Ãƒâ€šÃ‚Â§V.retired ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ SPEC.archive.md (<n> retired rows)` under Ãƒâ€šÃ‚Â§V heading ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â count form, not id-range (retired ids non-contiguous).
   - Per archived row append map entry `{run:<iso-date>, topic:'retired', old:V<n>, new:'archive'}`. No paired live-renumber entry (no new id consumed).
2. Append renumber entries to `.spec/spec-renumber-map.json` per surviving renumbered row (`{run:<iso-date>, topic:<cluster>, old:V<n>, new:V<m>}`). Append-only ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â never rewrite prior runs.
3. Rewrite Ãƒâ€šÃ‚Â§V in cluster order: body verbatim per verbatim-preservation invariant, only `V<n>:` prefix renumbered. Archived ids skipped.
4. Overwrite `.spec/spec-clusters.json` w/ post-run state; keyed by fingerprint, `current_id` = `V<new>`. Archived rows not persisted (terminus in archive sibling).
5. Cite-DAG sweep w/ renumber map: target set per PREAMBLE scope; backtick pre-filter as ARCHIVE-RETIRED step 2. Every surviving `Ãƒâ€šÃ‚Â§V.<old>` free-text or bare `V<old>` typed-column cite (Ãƒâ€šÃ‚Â§T.cites, Ãƒâ€šÃ‚Â§B.fix) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `Ãƒâ€šÃ‚Â§V.<new>` / `V<new>` per context. `new:'archive'` entries not substituted ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â citer-protection gate already excluded live citers.
6. Probe `.spec/.gitignore` if exists: both json files not gitignored (git-tracked per scope-set invariant); not guard add.
7. Stage owned paths `git add SPEC.md SPEC.archive.md .spec/spec-clusters.json .spec/spec-renumber-map.json` + touched sweep sites (add tracks new-file artifacts), then path-scoped commit `git commit -m <subject> -- <those same paths>` (write-ownership invariant ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â commit scopes to the owned set, pre-staged files never leak; `-m` flags ! precede `--`); auto-commit msg `reorganize SPEC.md Ãƒâ€šÃ‚Â§V: <m> clusters, <k> renumbers, <a> archive-retired`; not user prompt for commit step.

EXECUTE ends @ commit. Rollback `git revert <reorganize-sha>` per single-commit shape. Drift cascade surfaces as Next-block item per response-shape invariant ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â operator dispatches next turn.

## CHAIN-WALK SEMANTICS

Map is append-only history of all runs; stacked runs admit duplicate `old:` keys: run-1 `{old:V<a>, new:V<b>}`, run-2 `{old:V<b>, new:V<c>}` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `V<a>` resolves via newest-first walk `V<a> ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ V<b> ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ V<c>`, terminating when no further `old:` match. Walk landing on `archive` sentinel ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ emit `archived ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ SPEC.archive.md ## Ãƒâ€šÃ‚Â§V.retired V<n>`, not resolve to live row ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â distinct terminus from "no further mapping" (current live id). Consumers: reorganize re-runs + explain skill LOAD (historical-id resolution); both walk newest-first, read-only per cite-resolution invariant.

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

Heading `## Next`; 1ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“5 atomic items (one sentence each, no `Reply` prefix); positional dispatch (`run <int>` or `invoke the <skill-name> skill [args]`). Optional `## Hint` (ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â¤ 3 lines) precedes when item selection needs hidden state. State-mutator ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ post-EXECUTE prefer: invoke the check skill (confirm cite-DAG + format-layer clean post-renumber).

Example after EXECUTE (commit auto-fired):

```
## Next

1. invoke the check skill ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â cascade scan over reorganized SPEC.md
2. invoke the build skill --next ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â start the next pending Ãƒâ€šÃ‚Â§T row
3. git revert <reorganize-sha> ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â rollback if renumber breaks downstream
```

Variants: `--taxonomy-only` exit (not commit) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ swap item 1 for: invoke the reorganize skill (apply for real), drop item 3; CONFIRM cancel ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ swap item 1 for: invoke the reorganize skill --taxonomy-only (re-propose w/ filter), drop item 3.

## NON-GOALS

- not auto-fire ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â operator-triggered only per recipe-step-no-dispatch rule.
- not partial commit ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â single atomic commit per atomic-operation discipline.
- not token reduction ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â routes through the condense skill.
- not row folds ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â body content preserved (collapse belongs to the condense skill, prong 1); ARCHIVE-RETIRED drops row count via verbatim migration, not collapse.
- not cadence enforcement by the check skill ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â intent only.
- not hardcoded skill pack dir names ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â discovery probe drives PUBLISHED scope from `skills/*/SKILL.md` frontmatter.