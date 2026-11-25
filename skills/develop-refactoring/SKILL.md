---
name: develop-refactoring
description: "This skill owns how refactor and cleanup work is run and proven. `develop-code-quality` owns what good code looks like; this skill owns the procedure for changing existing code toward it without changing what it does. A refactor holds the functional axis fixed and improves the..."
---
# Refactoring

## Purpose

This skill owns how refactor and cleanup work is run and proven. `develop-code-quality` owns what good code looks like; this skill owns the procedure for changing existing code toward it without changing what it does. A refactor holds the functional axis fixed and improves the developmental one (`AGENTS.md`, Decision-Making Discipline); everything here serves keeping that promise checkable.

It defers to:

- `develop-code-quality` for the target rules (indirection, dead state, single source of truth, comments).
- The language skill for mechanics, and `develop-code-spacing` for blank lines after a reduction pass.
- The language skill's schema-evolution rules: removing dead columns or tables is a two-release change.
- `workflow-git-worktree` for parallel agents in separate worktrees, and `workflow-agentic` for dispatching them.

## Refactor Rules

1. Rename completely across DTOs/imports/tests/docs.
2. Preserve contracts unless behavior change is explicit.
3. Remove dead types instead of keeping compatibility stubs.
4. Do not add backwards compatibility layers unless explicitly requested by the user.
5. If there is strong reasoning to add backwards compatibility, pause and ask user clarification before implementing.
6. Keep schema/entity alignment.
7. Keep required vs optional semantics truthful across layers.
8. Remove unnecessary indirection: inline trivial wrappers, replace single-use parameter objects with direct parameters, delete unused barrels.
9. Simplify data transformations: assign directly instead of copying field by field, but only from an exact projection of the target (see `develop-code-quality`, When direct assignment is not safe).
10. Eliminate redundant work: pass already-computed results (metadata, validation outcomes, parsed data) to callees instead of re-computing.
11. Separate behavior changes from refactors. A bug found during a refactor is fixed in its own commit with its own test; a refactor commit never smuggles one in.
12. Be bold on internals and strict on observable behavior: private structure, names and layering may change freely when the evidence below stays green; response bodies, status codes, error codes, persisted data, side effects and their ordering may not.

## Proving Behavior Did Not Change

No single check proves a refactor preserved behavior. Use the evidence class that matches what could break, and name which one a claim rests on:

| Evidence                                                                                    | What it proves                                                                    | What it cannot see                                                                          |
| ------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| Contract shape: a diff of the generated OpenAPI document, schema or type surface            | Paths, schemas, fields, declared response statuses and descriptions are unchanged | Runtime behavior. A `PATCH` that went from 200 to 500 passed a byte-identical OpenAPI check |
| Exact output: a golden-output diff over a fixed input corpus                                | The same inputs still produce the same bytes                                      | Inputs outside the corpus                                                                   |
| Observable behavior: the test suite asserting status, payload, persistence and side effects | The covered behavior still holds                                                  | Uncovered paths; add a test when the refactor touches one                                   |

Byte comparison is the right tool only when the bytes are the contract. When part of the artifact is allowed to change (description text, ordering that is not part of the contract), compare semantically by stripping that part first.

Run the contract check on every branch of a multi-branch refactor and again on the integrated result. Record the baseline once, from the base branch, and compare everything against that one file.

### OpenAPI contract check (NestJS)

Build the app, create the document the way `main.ts` does, and write it with a stable layout. Mirror the app's own bootstrap (its module, plugins and `DocumentBuilder` settings); the skeleton below is the shape:

```javascript
// Usage: node dump-openapi.cjs <repoRoot> <out.json>  (run from the app dir after its build)
const { createRequire } = require('node:module')
const path = require('node:path')
const app = path.resolve(process.argv[2], 'apps/api')
const requireFromApp = createRequire(app + '/package.json')
const { NestFactory } = requireFromApp('@nestjs/core')
const { DocumentBuilder, SwaggerModule } = requireFromApp('@nestjs/swagger')
const { AppModule } = requireFromApp(app + '/dist/app.module')

;(async () => {
  const nest = await NestFactory.create(AppModule, { logger: false })
  // Apply the same global prefix, versioning and pipes main.ts applies, or paths will differ.
  const config = new DocumentBuilder().setTitle('api').addBearerAuth().build()
  const document = SwaggerModule.createDocument(nest, config)
  require('node:fs').writeFileSync(process.argv[3], JSON.stringify(document, null, 1))
  process.exit(0)
})().catch((error) => {
  console.error(error)
  process.exit(1)
})
```

Compare with `cmp baseline.json candidate.json`. The app usually needs its untracked env file (`.env`) to boot; copy it into each worktree and never commit it.

When doc text is meant to change, prove the structure did not:

```python
# Usage: openapi-textdiff.py <base.json> <new.json>
# Exit 0 when the documents match after dropping description/summary text; prints the changed text paths.
import json, sys

def strip(node):
    if isinstance(node, dict):
        return {k: strip(v) for k, v in node.items() if k not in ('description', 'summary')}
    if isinstance(node, list):
        return [strip(v) for v in node]
    return node

def walk(a, b, path=''):
    if isinstance(a, dict) and isinstance(b, dict):
        for key in set(a) | set(b):
            walk(a.get(key), b.get(key), f'{path}/{key}')
    elif isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        for i, (x, y) in enumerate(zip(a, b)):
            walk(x, y, f'{path}/{i}')
    elif a != b:
        print(path)

base, new = (json.load(open(p)) for p in sys.argv[1:3])
walk(base, new)
same = strip(base) == strip(new)
print('STRUCTURE IDENTICAL' if same else 'STRUCTURE DIFFERS')
sys.exit(0 if same else 1)
```

## Before a Large Refactor: Owner Rulings

A request such as "cut complexity and lines without affecting functionality, security or readability" can leave real choices to the owner: tradeoffs between line count and structure, contract changes, or removing stored data. When the request, the repository and the owner's standing rules do not settle them, present them before any code moves; when they do, proceed:

1. Write an analysis report: where the size and complexity are, and numbered strategies, each with its estimated effect, its tradeoff and its risk.
   - Verify every fact the request states about the code against the current tree first; in one run three of the brief's claims (a type's location, TODOs to resolve, a spec name) were already out of date.
   - Measure where the lines are: by module, by layer (services, DTOs, repositories, controllers, models), and by line kind (code, lone closing brackets, blank, API decorators, imports, comments). Line kinds are a diagnosis of where structure costs lines, not targets: a reduction that only removes blank lines or folds brackets is not a simplification.
   - When several analysts propose the same saving, count it once, at the lower estimate, net of any lines the change adds.
   - For the largest or riskiest modules, produce two independent designs first (structure-first and line-by-line), then synthesize the plan from both.
2. Ask the owner to rule on each open strategy, and record the answers verbatim in a file the agents read. Paraphrase loses the reason, and the reason is what a reviewer checks against.
3. Treat the rulings as binding in every brief and every review. Reviewers report a ruling violation as an issue.

Rulings that came up and are worth asking about explicitly, because the line-count answer and the owner's answer differ:

- Configuration classes, config files and config-key constants stay even when inlining would save lines ("all configurable things are in the config file").
- Every module keeps the same structure even when a small module could be flatter ("every module should have same structure even if it costs us extra lines of code").
- No magic literals, even where a literal would be shorter (queue names stay constants).
- Whether the API contract may change. One owner answered "we can't break contract" but allowed additive changes: new correctly named fields alongside deprecated old ones.
- How aggressive comment removal may be (see `develop-code-quality`, Comments).
- Whether dead persistent state (columns, tables, enum values) is removed in this work, and in how many releases.

## Running a Large Refactor

For a refactor spanning many modules, run it as a pipeline of independent units:

1. **Group the work by module** (or another boundary with few shared files) and give each group its own worktree and branch.
2. **One implementer per group**, briefed with the report's findings for that group, the owner rulings, the evidence commands, and the rule that cross-module items are deferred, not done. Each implementer prepares its worktree the way the repository needs (installing dependencies, building shared packages, copying untracked env files) and runs typecheck, lint, the specs of the modules it touched and the contract check before it reports.
3. **An adversarial review per group** that reads the diff against the rulings and hunts for observable changes, contract drift, lost transactions or locks, loosened assertions and readability regressions, followed by a fix pass that verifies each issue before fixing it.
4. **A cross-module stage** afterwards for the deferred items, run serially, because those items touch shared files.
5. **Integrate in a fixed order** through the integration procedure of `workflow-git-worktree`. When integrating by cherry-pick instead, check after each resolved conflict what already landed before picking the next range: re-picking a range that partly applied produces empty commits that must be skipped.
6. **Verify the integrated result** with the full evidence set, not the per-branch results: the whole test suite (in CI after the push, or locally when the owner asks for a full run) and the contract check.
7. **A final holistic review** with two lenses in parallel (behavior and contract; readability and consistency) over the whole diff from the base, then one fix pass. The per-group reviews cannot see cross-module regressions; in one run this final pass found a `PATCH` that had started returning 500.

Report line counts and other measured results from the integrated branch only.

## Consistency Surveys

A consistency pass makes code that differs between modules for no reason uniform. Run it as a read-only survey first:

1. Give each survey agent one lens (file and folder layout; symbol naming; test structure; declaration style; comments, API doc text and log style).
2. A finding is a pattern with a measured majority convention and a countable set of outliers, with example paths. One-off nits are not findings.
3. Skip what the formatter or linter owns, and what an owner ruling covers.
4. An adversarial agent recounts each finding, reads the outliers for a deliberate reason, and drops or corrects what fails.
5. Decide each convention in this order of authority: an enforced rule or published contract (lint config, the published API, a hard rule in `AGENTS.md`), then the owner's rulings, then the measured local majority, then skill defaults (the same order as `develop-code-quality`). A majority alone can canonize accidental debt; when the majority contradicts an enforced rule, the rule wins.
6. Present the verified list ranked, with the items that change externally visible text (API docs, log messages) separated out, because those break a byte-identical contract check and need the owner's acceptance.

Apply the accepted findings in serial stages on one branch, each implemented, reviewed and fixed before the next starts: layout (moves and renames), symbols, tests and comments, then API doc and log text last, verified with the text-only diff above.

Write each confirmed convention into the skill that owns it, not into this one: project layout and naming in the project's own conventions skill, language mechanics in the language skill, documentation wording in `write-documentation`.

## Cleanup Playbooks

### Indirection reduction

- identify trivial wrapper methods that only delegate to another method with a hardcoded argument; inline the call at all call sites and remove the wrapper
- identify single-use parameter wrapper interfaces/types (an interface created only to bundle arguments for one private method call); replace with direct parameters, especially when parallel methods in the same class already use direct parameters (consistency matters)
- identify barrel files (`index.ts`) that merely re-export siblings without adding value; if all consumers already import directly from the source files, delete the barrel
- identify wrapper objects or adapter layers that pass data through without transformation; remove the layer and let consumers use the source directly
- identify passthrough methods where a public method's only job is to pack its parameters into a single-use interface and forward to a private method; merge into one method (the private method becomes the public one) and delete the wrapper interface

### Verbose transformation reduction

- when loading config, deserializing data, or mapping between layers, check whether the source shape already matches the target type
- if it does, assign directly instead of copying field-by-field; field-by-field mapping is only warranted when fields are renamed, transformed, validated, or subsetted
- watch for mapping code that expands as new fields are added but never actually transforms anything - this is a maintenance surface with no value

### Redundant work elimination

- when a method calls an expensive operation (IO, parsing, metadata extraction) and then passes the raw input to a sub-method that repeats the same operation, pass the result down instead
- common pattern: metadata/validation fetched in an outer method, then re-fetched in an inner method on the same input - add a parameter for the already-computed result

### Service chain collapse

When a service chain has 3+ layers (orchestrator ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ intermediate ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ specialized) and the intermediate service adds no branching logic or independent state:

1. Identify what the intermediate service actually contributes - if it only forwards calls and aggregates results, it's a passthrough layer.
2. Move the intermediate service's logic into the orchestrator.
3. Let the orchestrator call the specialized service directly.
4. Delete the intermediate service and update module providers.

Example: `ImageProcessingService` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `ImageProcessorService` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `ImageTransformerService` collapsed to `ProcessingService` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `TransformerService` - the orchestrator now owns the full pipeline (download, validate, blurhash, resize, upload).

### Re-export and type alias cleanup

- Identify `export type { X }` re-exports where the consuming files could import directly from the source.
- Identify type files that exist solely to hold 1-2 interfaces consumed by one other file - merge into the consumer's schema file.
- When config types (e.g., `IEntityConfig`) and runtime data types (e.g., `IMediaItemData`) are consumed by the same pipeline, co-locate them in one schema file.

### Dead code removal

- remove unused methods/types/exports/tests/config keys/dependencies
- do not keep compatibility shims unless explicitly requested

### Post-change dead code verification

After removing a dependency, import, or injection from a service/module, run `codebase_find_unused_symbols` scoped to the affected module to detect methods or symbols that became dead as a side effect. Either clean them up in the same PR or log a follow-up ticket. Do not leave newly-dead code unacknowledged.

### Refactor-session unused symbol sweep

At least once during every refactor session, run `codebase_find_unused_symbols` on the touched scope (module/package or whole project, depending on blast radius). For each candidate, determine whether it is truly dead code or an exported symbol potentially used externally. If the list is large or ambiguous, use `codebase_trace_calls` per candidate to classify before removal - exported symbols with zero in-tree callers are still potentially consumed externally and need a wider check.

## Removing Dead Persistent State

Columns, tables and enum values that nothing reads are dead code too, but removing them is a schema change with deploy-ordering consequences: the drop must not ship in the same release that stops using the column. The language skill's schema-evolution rules own the two-release procedure; follow them, or record the owner's explicit acceptance of the downtime and the lost rollback safety.

## Reporting the Result

- Count production and test lines separately, measured from git objects (`git show <ref>:<path>`) so the numbers are reproducible for any ref.
- Exclude generated files (migration snapshots, generated API clients) from added-line totals, and say so.
- A spacing pass after a reduction adds blank lines back; report counts after it, and say how many lines it added.
- List anything deferred or skipped, with the reason.

## Anti-Patterns

- Claiming "behavior unchanged" on the strength of a contract-shape diff alone
- Starting a large refactor without recorded owner rulings, or paraphrasing them
- Mixing a behavior change into a refactor commit
- Letting a group's implementer do cross-module items in parallel with other groups
- Trusting per-branch verification instead of verifying the integrated result
- Re-picking a cherry-pick range after a conflict without checking what already landed
- Treating a measured majority as the convention when a rule or contract says otherwise
- Writing a survey's conventions into this skill instead of the skill that owns the topic
- Dropping columns in the same release that stops using them, without the owner's explicit acceptance
- Reporting line counts that include generated files without saying so

## Rules

- A refactor holds behavior fixed; name the evidence class behind every "unchanged" claim
- Record owner rulings verbatim before a large refactor, and review against them
- One worktree and branch per group; cross-module work runs serially afterwards
- Every branch runs typecheck, lint, its touched modules' specs and the contract check; the integrated result runs the whole suite and the contract check
- Finish with a holistic two-lens review of the whole diff from the base
- Consistency findings need a counted majority and countable outliers, recounted adversarially; rules and rulings outrank the majority
- Externally visible text changes are separated out, verified with a text-only diff, and accepted by the owner
- Dead persistent state is removed in two releases unless the owner accepts the risk
