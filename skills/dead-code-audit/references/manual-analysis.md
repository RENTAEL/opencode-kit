# Manual dead code analysis (no tools available)

Use this when the language tools cannot be installed, or the language has no
good tool. It is slower and needs more verification, but it works anywhere with
grep and git.

## The method

1. **Extract definitions.** Use `scripts/symbol_index.py` to build a symbol map,
   or for a single directory, grep definition keywords (`def `, `function `,
   `class `, `func `, `fn `) and collect names.

2. **Count references per symbol.**
   ```bash
   python scripts/symbol_index.py <repo> --lookup <symbol>
   # or directly:
   git grep -cw "<symbol>" | awk -F: '{s+=$2} END {print s}'
   ```
   A symbol with exactly 1 reference (its own definition) is a candidate.
   2 references where the second is an import/re-export line is also a candidate.

3. **Whole-file check first** (best value per minute): for each file, check
   whether anything imports it.
   ```bash
   git grep -l "filename_without_ext" -- ':!path/to/that/file'
   ```
   Zero importers plus not matching an entry-point convention = candidate dead file.

4. **Apply the SKILL.md step 3 verification** (string usage, decorators/
   annotations, public API, templates/configs, git history) before assigning a tier.

## Ranking candidates when time is limited

Prioritize in this order, since it maximizes deletable lines per unit of effort:

1. Whole files with zero importers
2. Whole classes with zero instantiations
3. Large functions (30+ lines) with only a definition reference
4. Everything else

## Honest limits

Name-based grep cannot distinguish two different functions that share a name in
different modules, and it over-counts symbols mentioned in comments or docs.
When a symbol name is generic (`run`, `get`, `handler`, `main`), skip textual
counting entirely and read the actual import graph for its module instead. Say
so in the report's "Not scanned" section if generic-named symbols were skipped.
