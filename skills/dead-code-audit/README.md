# dead-code-audit

A Claude skill that hunts down dead code in a repository and hands back a
confidence-ranked report instead of a reckless delete list.

## Why the tiered report

Static analysis can only prove that nothing *statically* points at a piece of
code. Reflection, dependency injection, and string-based dispatch all call code
that looks orphaned on paper. So findings land in three tiers: safe to remove,
probably dead (check with an owner), and unused but intentional (public API,
feature flags). Nothing gets deleted unless you ask after seeing the report.

## How it handles big repos

The skill measures the repo first (`scripts/size_repo.py`) and picks a strategy:

- **SMALL**, under 50k lines: one full pass, every finding verified
- **MEDIUM**, 50k to 500k lines: repo-wide tool scan, deep verification only on
  the candidates worth the effort
- **LARGE**, 500k+ lines or 5k+ files: chunked module-by-module sweep. It builds
  a cheap global symbol index once (`scripts/symbol_index.py`), audits one
  module at a time, and checks every candidate against the global index so a
  helper used only by a distant module never gets flagged. Findings checkpoint
  after each chunk, so an interrupted audit resumes instead of restarting.

Vendored, generated, and build directories are excluded up front.

## Running the scripts yourself

Both scripts are plain Python 3, standard library only.

```bash
# size a repo and get the recommended strategy
python scripts/size_repo.py ~/code/my-repo
python scripts/size_repo.py ~/code/my-repo --json   # machine-readable

# build the global symbol index (large repos)
python scripts/symbol_index.py ~/code/my-repo --out index.json

# quick reference count for one symbol
python scripts/symbol_index.py ~/code/my-repo --lookup process_payment
```

## Layout

```
dead-code-audit/
├── SKILL.md                     # the workflow Claude follows
├── scripts/
│   ├── size_repo.py             # repo measurement + strategy pick
│   └── symbol_index.py          # global symbol index + reference lookup
└── references/
    ├── python.md                # vulture, pyflakes, deptry, Python traps
    ├── javascript.md            # knip, ts-prune, depcheck, JS/TS traps
    ├── go-rust-java.md          # deadcode, staticcheck, cargo-machete, PMD
    └── manual-analysis.md       # grep-and-git fallback when tools are missing
```

## Supported languages

First-class: Python, JavaScript/TypeScript, Go, Rust. Covered with caveats:
Java/Kotlin (reflection and Spring DI make automated certainty impossible, so
the skill leans on the manual method plus IDE inspections there). Anything else
falls back to the manual analysis method, which works on any text-based language.
