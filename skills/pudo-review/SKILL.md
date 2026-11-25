---
name: pudo-review
description: "1. Run `git diff` (and `git diff --staged`). Read every changed hunk and the callers of changed functions. 2. Run the project's tests and checks. Report the exact command and result. A failure is reported, never hidden. 3. Call `pudo.runQualityGate` with `develop`, then `optim..."
---
# PUDO Review

1. Run `git diff` (and `git diff --staged`). Read every changed hunk and the callers of changed functions.
2. Run the project's tests and checks. Report the exact command and result. A failure is reported, never hidden.
3. Call `pudo.runQualityGate` with `develop`, then `optimize`, when the PUDO MCP server is connected.
4. Reply with:

```
Verdict:         ready / not ready (one line why)
Verified by:     commands run and their result
Findings:        numbered; each with file:line, the concrete failing case, the smallest fix
Scope creep:     changes the request did not ask for
Remaining risks: what is untested or assumed
```

No finding without a concrete case ("this input leads to this wrong result"). No style taste.
