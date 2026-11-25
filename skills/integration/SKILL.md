---
name: integration
description: "Integration + e2e tests. Validates modules work together. Run AFTER unit tests pass."
---
# /supergraph:integration

Integration + e2e tests. Validates modules work together. Run AFTER unit tests pass.

## Usage

`/supergraph:integration` | `plan auth-login` | `plan auth-login task 3`

## Prerequisites

- Unit tests passing (`$TEST_CMD` green)
- `/supergraph:fix` completed

## Steps

### 0. Announce
"ÃƒÂ°Ã…Â¸Ã¢â‚¬ÂÃ¢â‚¬â€ /supergraph:integration ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â running integration and e2e tests..."

### 1. Get Commands
Read from plan `## Environment Context` or `.supergraph-env`. Missing ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ STOP, run `/supergraph:scan` first.

### 2. Verify Unit Tests Pass
```bash
$TEST_CMD
```
If unit tests FAIL ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ STOP: "Unit tests must pass before integration. Run `/supergraph:fix` first."

### 3. Detect Integration Setup
Check for integration configuration:

| Config | Command |
|---|---|
| `jest.integration.config.js` | `npx jest --config jest.integration.config.js` |
| `vitest.integration.config.ts` | `npx vitest --config vitest.integration.config.ts` |
| `pytest.ini` with `[integration]` or `-m integration` | `pytest -m integration` |
| `cypress.config.js` / `cypress.config.ts` | `npx cypress run` |
| `docker-compose.test.yml` | `docker compose -f docker-compose.test.yml up --abort-on-container-exit` |
| `*.integration.test.ts` / `*.integration.spec.ts` pattern | `npx jest --testPathPattern="integration"` |

If none found ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ skip: "No integration/e2e config found ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â skipping."

### 4. Run Integration Tests
Max 3 retries. On failure:

**4b. Serena (optional):** See `serena/SKILL.md:Setup` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `find_referencing_symbols`/`get_diagnostics_for_file` per failing module to surface mismatches. Skip if unavailable.

Trace failure to source module, fix, re-run.

### 5. Run E2E & Full-Stack QA Automation
- **QA Matrix Generation**: Generate or verify ISTQB QA matrix coverage (`docs/qa/test-matrix-<feature>.md`) covering Happy path, Sad path, Boundary, Network 500 error injection, Auth/RBAC, and IDOR (scaffold via `bash plugins/supergraph/skills/browser-agent/scripts/init-qa.sh matrix <feature> [ui|api|fullstack]`).
- **Web/Frontend Projects**: ALWAYS automatically invoke `/supergraph:browser-agent` to run autonomous user-flow tests via native Rust CDP (anti-bot bypass, zero Playwright).
- **Backend / API Services**: Verify API endpoint schemas, response codes, DB state integrity, and error sanitization.
- **Execution**: Run automated test cases via `agent-browser` or project e2e test script. Max 2 retries (e2e is inherently flaky). Annotate flaky tests ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â do not block merge on known-flaky external network tests.

### 6. Graph Validation
For `CBM_PROJECT` via `codebase-memory-mcp` (see `references/codebase-memory-contract.md`) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `search_graph`/`trace_path` + recipes `dependencies/cross-boundary/test-gaps`; fall back to Serena/filesystem if empty.

### 7. Update Plan Status
Pass ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ mark in-progress tasks `Status: completed`.
Fail after 3 retries ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ mark `stuck`, append failure log.

### 8. Report
```
ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ /supergraph:integration complete
- Unit: PASS | Integration: PASS|FAIL|SKIP | E2E: PASS|FAIL|SKIP
- Cross-module flows: N/M covered | Surprising connections: [list/none]
- Plan status: updated|none
- Next: /supergraph:verify ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ /supergraph:review
```

## Rules
- Unit tests MUST pass BEFORE running integration
- Integration failures take priority over e2e (fix foundation first)
- Max 3 retries integration, 2 retries e2e
- Never block merge on `@flaky`-annotated e2e tests
- Always update plan status after completion
- After integration pass ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `/supergraph:verify` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `/supergraph:review`
