---
name: verify-done
description: "Claim only what the available evidence demonstrates."
---
# Verify Done

Claim only what the available evidence demonstrates.

## Select the Mode

- **Implementation completion:** Run the gate, repair in-scope failures while implementation authority remains active, then rerun the failed and neighboring checks.
- **Verification only:** Run safe relevant checks, report failures or blocked gates, and stop without changing implementation or configuration.

## Evidence Gate

1. Inspect the repository's actual command definitions, worktree baseline, required services, cost, credentials, side effects, and expected runtime.
2. Build, compile, bundle, or import the changed code where applicable.
3. Run focused tests, the relevant suite, and any lint or type checks. Report exact pass, fail, and skip counts and distinguish pre-existing failures.
4. Exercise the assembled user-facing behavior on a safe realistic input. Prefer a dry run, sandbox, fixture, or disposable environment. Do not mutate production, incur charges, send messages, expose private data, or expand authority merely to satisfy this gate.
5. Audit status and the complete diff for unintended files, debug code, generated artifacts, secrets, and unrelated churn.
6. Confirm documentation, configuration, migrations, rollout, rollback, and monitoring remain consistent with changed behavior.
7. Record checks that could not run because of credentials, hardware, services, platform, or environment. Never turn an unavailable check into a pass.

## Report

State the command or action, observed result, and residual gap. If a gate fails during verification-only mode, report the task as not verified and stop. If repair is in scope, fix the cause and repeat the gate before claiming completion.
