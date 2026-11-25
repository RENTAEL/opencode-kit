---
name: dead-code-audit
description: "Find code that nothing actually uses, without lying about certainty. The output is always a report with confidence tiers, never silent deletion."
---
# Dead Code Audit

Find code that nothing actually uses, without lying about certainty. The output is
always a report with confidence tiers, never silent deletion.

## The one rule that matters

Static analysis cannot prove code is dead. It can only prove nothing *statically*
references it. Reflection, dependency injection, string-based imports, plugin
registries, ORM magic, and template engines all call code that looks unreferenced.
So every finding gets a confidence tier, and deletion only happens if the user asks
for it after seeing the report.

## Step 1: Size the repo and pick a strategy

Run the sizing script first. It counts files and lines per language, flags vendored
and generated directories, and recommends a strategy.

```bash
python scripts/size_repo.py /path/to/repo
```

Strategy thresholds (the script applies these for you):

| Tier | Repo size | Strategy |
|------|-----------|----------|
| SMALL | under 50k source lines | Full scan: run every relevant tool across the whole repo in one pass, then manually verify each finding |
| MEDIUM | 50k to 500k lines | Tool scan: run language tools repo-wide, but only do deep cross-reference verification on the highest-value candidates (largest files, whole modules, exported symbols) |
| LARGE | over 500k lines or over 5,000 source files | Chunked scan: see "Large repo protocol" below. Do not attempt a single-pass grep-everything approach, it will blow the time budget and the context window |

Always exclude before scanning, regardless of tier: `node_modules`, `vendor`,
`dist`, `build`, `.git`, `target`, `venv`/`.venv`, `__pycache__`, generated code
(protobuf `_pb2` files, `*.generated.*`, migration folders unless asked), and
test fixtures. The sizing script prints an exclusion list; confirm it looks right
before proceeding.

## Step 2: Run language-appropriate tools

Read the reference file for each language the sizing script found. Each one lists
the tools, install commands, invocation, and known false-positive patterns:

- `references/python.md` - vulture, pyflakes, coverage-assisted checks
- `references/javascript.md` - knip, ts-prune, depcheck, ESLint (covers TS too)
- `references/go-rust-java.md` - staticcheck/deadcode, cargo machinery, compiler flags
- `references/configs-ci-hygiene.md` - temp/junk files, stale CI, orphaned configs.
  ALWAYS read this one regardless of language; run `python scripts/hygiene_scan.py <repo>`
  alongside the source-level tools, since source tools cannot see this category at all.
- `references/safe-removal.md` - test-only-alive detection, tombstone runtime
  verification for Tier 2, the deletion workflow, and prevention (CI ratchets).
  Read before reporting and always before deleting anything.

If a tool is unavailable and cannot be installed (no network, unsupported), fall
back to the manual method in `references/manual-analysis.md`: build a symbol
definition list with grep/AST parsing, then search for references to each symbol.

## Step 3: Verify candidates before reporting

For each candidate the tools flag, check the dynamic-usage traps before assigning
a tier:

1. Grep for the symbol name as a **string** (`"symbol_name"`, `'symbol_name'`) -
   catches reflection, `getattr`, dynamic imports, config-driven dispatch.
2. Check decorators/annotations that register things implicitly (route handlers,
   event listeners, pytest fixtures, DI containers, serializers).
3. Check whether the symbol is part of a **public API surface**: exported from a
   package `__init__.py` or `index.ts`, listed in `__all__`, mentioned in docs or
   README, or the package is published. Public API that is internally unused is
   "unused internally", not dead.
4. Check templates and non-code files (HTML templates, YAML configs, SQL) for the
   name.
5. Check git history: `git log --oneline -3 -- <file>`. Code touched in the last
   30 days deserves extra suspicion of the tools, not of the code.
6. Check whether the only references are from **test files** (paths matching
   test/, tests/, spec/, __tests__/, *_test.*, *.test.*, *.spec.*). Production
   code kept alive solely by its own tests is dead; label it "test-only" in
   Tier 1 and remove code and tests together. See `references/safe-removal.md`.
   Exception: published-library code may legitimately have only test references
   internally; that stays Tier 3.

## Step 4: Report format

ALWAYS use this exact structure:

```
# Dead Code Audit: <repo name>
Scanned: <N files, N lines> | Strategy: <SMALL/MEDIUM/LARGE> | Coverage: <full or which modules>

## Tier 1 - Safe to remove (high confidence)
Nothing references these statically OR dynamically. Private symbols, unreferenced
files, unreachable branches after return/raise, unused imports.
<table: location | symbol | why it is dead | evidence>

## Tier 2 - Probably dead (verify with owner)
Statically unreferenced but matches a dynamic-usage risk pattern, or is old code
in a rarely-touched module. For each item, offer the tombstone technique from
`references/safe-removal.md` (a logged marker shipped for 30-90 days) as the way
to settle it with runtime evidence instead of leaving it in limbo.
<table: location | symbol | risk that it is actually used | suggested verification>

## Tier 3 - Unused but intentional (do not remove without discussion)
Public API surface, feature-flagged code, platform-specific branches.

## Unused dependencies
Packages in the manifest that no source file imports.

## Stale CI, configs, and junk files
Temp/backup files, CI files for retired systems or nonexistent branches, and
configs for tools no longer in the dependency set.

## Not scanned
Anything excluded or skipped due to size limits, so the user knows the blind spots.
```

Estimate deletable line counts per tier. Note the standing blind spots when
relevant: dead API endpoints need traffic logs and dead database objects need
query logs, both outside a source-only audit; name them as follow-ups rather
than staying silent.

If the user then asks to delete, follow the workflow in
`references/safe-removal.md`: Tier 1 only, one branch per audit and one commit
per module, tests deleted with the code they tested, a post-delete grep per
symbol, full test suite and build, and a diff summary. After a cleanup, offer
the prevention step from the same file (compiler/linter flags plus a baselined
ratchet job) so dead code stops accumulating between audits.

## Large repo protocol

For LARGE repos, work like a search party sweeping a forest grid by grid rather
than one person wandering everywhere:

1. **Budget first.** Tell the user roughly how long a full audit takes and offer
   scoping options: whole repo chunked, top N largest modules, or a specific
   directory they care about. Default to whole-repo chunked if they do not choose.
2. **Build a cheap global symbol index once** (script provided):
   `python scripts/symbol_index.py /path/to/repo --out index.json`
   This is a flat map of defined symbols to files, built with lightweight parsing,
   cheap enough to run on millions of lines.
3. **Chunk by top-level module/package**, not by arbitrary file count, so import
   relationships mostly stay inside a chunk.
4. **Per chunk:** run the language tools scoped to that chunk, then verify each
   candidate against the *global* index, not just the chunk. This is what prevents
   the classic false positive where module A's helper is only called from module B.
5. **Checkpoint after each chunk** by appending findings to a running report file.
   If the audit gets interrupted, resume from the last chunk instead of restarting.
6. **Time budget:** if a chunk takes more than ~10 minutes of tool time, note it,
   scan its largest files only, and mark the rest under "Not scanned". Partial
   honest coverage beats fake complete coverage.
7. Entire-file dead checks scale best, so on the first pass through a LARGE repo,
   prioritize finding whole dead files and dead modules (biggest wins), then only
   descend to function-level analysis in modules the user cares about.

## What counts as dead code

- Unreferenced functions, classes, methods, variables, constants
- Production code whose only references come from its own tests ("test-only")
- Unreachable code (after return/raise/break, conditions that are always false)
- Unused imports and unused manifest dependencies
- Orphaned files nothing imports
- Commented-out code blocks larger than ~10 lines (report, never auto-delete)
- Feature-flag branches for flags that are hardcoded off (Tier 2)
- Exported symbols with zero internal references (Tier 3 unless clearly internal)
- Committed temp/backup/junk files (`*.log`, `*.bak`, `.DS_Store`, editor swaps)
- CI files for retired systems, disabled workflows, workflows triggering on
  deleted branches, and CI helper scripts nothing references
- Config files whose consuming tool is absent from every manifest, CI file, and
  Makefile (see `references/configs-ci-hygiene.md`)
