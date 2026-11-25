---
name: self-review
description: "Read the actual change as a skeptical maintainer, not from memory."
---
# Self Review

Read the actual change as a skeptical maintainer, not from memory.

## Select the Mode

- **Author mode:** Review work produced within the current approved implementation. Fix in-scope findings, rerun affected checks, and review the resulting diff again.
- **Review-only mode:** Report findings and evidence without modifying files, formatting, snapshots, dependencies, git state, or external systems. Implement fixes only when separately requested.

## Review Process

1. Inspect repository instructions, status, the complete diff, untracked files, and the original request. Preserve unrelated work.
2. Trace each changed input through callers, state transitions, outputs, and failure paths. Check empty, boundary, large, Unicode, concurrent, retry, and partial-failure cases where relevant.
3. Follow changed trust boundaries beyond literal changed lines. Inspect authorization, secrets, injection, filesystem and process execution, unsafe rendering, deserialization, dependency risk, and data exposure.
4. Check errors and cleanup: failures must surface; resources, transactions, locks, and temporary files must be released.
5. Check scope and consistency: no debug leftovers, dead code, accidental generated files, unsupported API changes, or unrelated formatting churn.
6. Check tests: new behavior has meaningful coverage, assertions can fail, and boundary behavior is exercised.
7. Validate each potential finding against callers, guards, tests, and framework guarantees. Omit speculation.

## Report

Lead with independently actionable findings ordered by severity, each with a precise location, trigger, impact, evidence, and remediation direction. Then list material assumptions and verification gaps. If no finding survives validation, say so explicitly.
