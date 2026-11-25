# Safe removal, runtime verification, and prevention

Finding dead code is half the job. This file covers the other half: proving the
ambiguous cases, deleting without incident, and keeping the repo from silting
back up.

## Test-only-alive code

A symbol whose only references come from test files is not alive; it is dead
code with a life-support machine. Check every candidate that "has references"
for this pattern before clearing it:

```bash
# where do the references actually live?
git grep -lw "symbol_name" | grep -vE "(^|/)(test|tests|spec|__tests__|.*_test\.|.*\.test\.|.*\.spec\.)"
```

Zero non-test hits means the only callers are tests. Report these in Tier 1
with the label "test-only", and when removing, delete the tests together with
the code in the same commit. Exception: code that exists *for* external
consumers (a published library) may legitimately have only test references
internally; that stays Tier 3.

## Runtime verification (tombstones) for Tier 2

When static analysis cannot settle whether something runs, stop guessing and
measure. Add a tombstone: a cheap, unique log line at the top of the suspect
function, ship it, and wait.

```python
import logging
def maybe_dead_handler(...):
    logging.info("TOMBSTONE:maybe_dead_handler")  # remove after verification window
    ...
```

- Use a greppable prefix (`TOMBSTONE:`) so findings are one log query away.
- Pick the window by the code's rhythm: 30 days for request-path code, 90+ days
  for anything that smells of quarterly reports, year-end jobs, or rare admin
  flows.
- Zero hits after the window: promote to Tier 1 and delete. Any hits: mark the
  code alive, record the caller, remove the tombstone.
- Batch tombstones into one commit per module so they are easy to find and
  easy to rip out later.

Where infrastructure allows, production coverage tools do this wholesale
(coverage.py under a sampling harness, JaCoCo in JVM services, V8 coverage in
Node). Suggest them when the user owns deploys; suggest tombstones when they
can only merge code.

## Deletion workflow

When the user confirms removal, never do one giant cleanup commit. Follow this
sequence:

1. **Branch per audit, commit per module.** A revert should un-delete one
   module's cleanup, not the whole month's work.
2. **Delete Tier 1 only.** Tests and their fixtures go in the same commit as
   the code they tested.
3. **Post-delete grep.** After removing a symbol, grep its name once more
   repo-wide. Leftover references in comments, docs, or config are either
   cleanup targets or, worse, evidence the thing was not dead.
4. **Run the full test suite and the build**, not just the tests near the
   change. Dead-code removal fails at a distance (a lazy import, a plugin
   registry) more often than locally.
5. **Summarize per commit**: files touched, lines removed, tier, and the
   evidence line from the report. Future archaeologists will thank you, and
   `git revert` becomes a one-liner if anything surfaces.
6. If the repo has CODEOWNERS, route each module's deletions to its owners
   rather than one mega-review nobody reads carefully.

## Prevention: make the next audit smaller

Dead code is a flow problem, not a stock problem; an audit drains the lake but
the river keeps running. After a cleanup, offer to turn on the cheap dams:

- **Python**: pyflakes/ruff (`F401` unused import, `F841` unused variable) in
  CI; vulture in a scheduled weekly job rather than per-PR (too noisy inline).
- **JS/TS**: `noUnusedLocals` and `noUnusedParameters` in tsconfig;
  `npx knip` as a scheduled job with its current findings baselined, failing
  only on *new* findings (a ratchet, so legacy debt does not block builds).
- **Go**: `staticcheck` (U1000) in CI; the compiler already rejects unused
  imports and locals.
- **Rust**: deny the warnings you have finished cleaning:
  `#![deny(dead_code)]` per cleaned crate, or `RUSTFLAGS="-D dead_code"` in CI.
- **Everywhere**: a `.gitignore` entry for every junk pattern found during the
  hygiene scan, so temp files stop getting committed.

The ratchet pattern matters: enforce "no new dead code" immediately, burn down
the existing baseline gradually. Teams abandon zero-tolerance gates on legacy
repos within a week; they keep ratchets for years.

## Honest limits worth stating in every report

- Dead **API endpoints** need access logs or gateway metrics to confirm; the
  audit can flag "no internal callers" but cannot see external traffic.
- Dead **database columns, tables, and stored procedures** need query logs;
  out of scope for a source-only audit. Mention them as a follow-up if ORM
  models with unused fields showed up in findings.
- Anything verified by tombstone is only as dead as the window was long. Say
  the window length in the report.
