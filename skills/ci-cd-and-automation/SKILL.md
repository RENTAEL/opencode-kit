---
name: ci-cd-and-automation
description: "Automate quality gates so that no change reaches production without passing tests, lint, type checking, and build. CI/CD is the enforcement mechanism for every other skill ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â it catches what humans and agents miss, and it does so consistently on every single ch..."
---
> Adapted copy of addyosmani/agent-skills (MIT) for local use; changes are listed in `UPSTREAM.md`.
> Ground rules that override anything below: use only tools that are already installed in the project
> (project scripts, `npx --no-install ...`); never let npx/pip/brew download or install anything and never add
> MCP servers on your own; do not fetch web pages or online docs and do not upload or post data anywhere;
> never push, deploy, run migrations, flip feature flags or change shared systems without the user's explicit
> instruction. Commands inside CI/workflow examples are file content to write, not commands to run now.

# CI/CD and Automation

## Overview

Automate quality gates so that no change reaches production without passing tests, lint, type checking, and build. CI/CD is the enforcement mechanism for every other skill ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â it catches what humans and agents miss, and it does so consistently on every single change.

**Shift Left:** Catch problems as early in the pipeline as possible. A bug caught in linting costs minutes; the same bug caught in production costs hours. Move checks upstream ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â static analysis before tests, tests before staging, staging before production.

**Faster is Safer:** Smaller batches and more frequent releases reduce risk, not increase it. A deployment with 3 changes is easier to debug than one with 30. Frequent releases build confidence in the release process itself.

## When to Use

- Setting up a new project's CI pipeline
- Adding or modifying automated checks
- Configuring deployment pipelines
- When a change should trigger automated verification
- Debugging CI failures

## The Quality Gate Pipeline

Every change goes through these gates before merge:

```
Pull Request Opened
    ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
    ÃƒÂ¢Ã¢â‚¬â€œÃ‚Â¼
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€™ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ‚Â
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   LINT CHECK     ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  eslint, prettier
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬Å“ pass         ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   TYPE CHECK     ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  tsc --noEmit
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬Å“ pass         ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   UNIT TESTS     ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  jest/vitest
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬Å“ pass         ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   BUILD          ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  npm run build
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬Å“ pass         ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   INTEGRATION    ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  API/DB tests
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬Å“ pass         ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   E2E (optional) ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  Playwright/Cypress
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬Å“ pass         ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   SECURITY AUDIT ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  npm audit
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬Å“ pass         ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   BUNDLE SIZE    ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  bundlesize check
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ‹Å“
    ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
    ÃƒÂ¢Ã¢â‚¬â€œÃ‚Â¼
  Ready for review
```

**No gate can be skipped.** If lint fails, fix lint ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â don't disable the rule. If a test fails, fix the code ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â don't skip the test.

## GitHub Actions Configuration

### Basic CI Pipeline

```yaml
# .github/workflows/ci.yml
name: CI

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Lint
        run: npm run lint

      - name: Type check
        run: npx tsc --noEmit

      - name: Test
        run: npm test -- --coverage

      - name: Build
        run: npm run build

      - name: Security audit
        run: npm audit --audit-level=high
```

### With Database Integration Tests

```yaml
  integration:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: testdb
          POSTGRES_USER: ci_user
          POSTGRES_PASSWORD: ${{ secrets.CI_DB_PASSWORD }}
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'npm'
      - run: npm ci
      - name: Run migrations
        run: npx prisma migrate deploy
        env:
          DATABASE_URL: postgresql://ci_user:${{ secrets.CI_DB_PASSWORD }}@localhost:5432/testdb
      - name: Integration tests
        run: npm run test:integration
        env:
          DATABASE_URL: postgresql://ci_user:${{ secrets.CI_DB_PASSWORD }}@localhost:5432/testdb
```

> **Note:** Even for CI-only test databases, use GitHub Secrets for credentials rather than hardcoding values. This builds good habits and prevents accidental reuse of test credentials in other contexts.

### E2E Tests

```yaml
  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'npm'
      - run: npm ci
      - name: Install Playwright
        run: npx playwright install --with-deps chromium
      - name: Build
        run: npm run build
      - name: Run E2E tests
        run: npx playwright test
      - uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: playwright-report
          path: playwright-report/
```

## Feeding CI Failures Back to Agents

The power of CI with AI agents is the feedback loop. When CI fails:

```
CI fails
    ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
    ÃƒÂ¢Ã¢â‚¬â€œÃ‚Â¼
Copy the failure output
    ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
    ÃƒÂ¢Ã¢â‚¬â€œÃ‚Â¼
Feed it to the agent:
"The CI pipeline failed with this error:
[paste specific error]
Fix the issue and verify locally before pushing again."
    ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
    ÃƒÂ¢Ã¢â‚¬â€œÃ‚Â¼
Agent fixes ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ user confirms the push ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ CI runs again
```

**Key patterns:**

```
Lint failure ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Agent runs `npm run lint --fix` and commits locally (push only when the user confirms)
Type error  ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Agent reads the error location and fixes the type
Test failure ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Agent follows debugging-and-error-recovery skill
Build error ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Agent checks config and dependencies
```

## Deployment Strategies

### Preview Deployments

Every PR gets a preview deployment for manual testing:

```yaml
# Deploy preview on PR (Vercel/Netlify/etc.)
deploy-preview:
  runs-on: ubuntu-latest
  if: github.event_name == 'pull_request'
  steps:
    - uses: actions/checkout@v4
    - name: Deploy preview
      run: npx vercel --token=${{ secrets.VERCEL_TOKEN }}
```

### Feature Flags

Feature flags decouple deployment from release. Deploy incomplete or risky features behind flags so you can:

- **Ship code without enabling it.** Merge to main early, enable when ready.
- **Roll back without redeploying.** Disable the flag instead of reverting code.
- **Canary new features.** Enable for 1% of users, then 10%, then 100%.
- **Run A/B tests.** Compare behavior with and without the feature.

```typescript
// Simple feature flag pattern
if (featureFlags.isEnabled('new-checkout-flow', { userId })) {
  return renderNewCheckout();
}
return renderLegacyCheckout();
```

**Flag lifecycle:** Create ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Enable for testing ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Canary ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Full rollout ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Remove the flag and dead code. Flags that live forever become technical debt ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â set a cleanup date when you create them.

### Staged Rollouts

```
PR merged to main
    ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
    ÃƒÂ¢Ã¢â‚¬â€œÃ‚Â¼
  Staging deployment (auto)
    ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡ Manual verification
    ÃƒÂ¢Ã¢â‚¬â€œÃ‚Â¼
  Production deployment (manual trigger or auto after staging)
    ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
    ÃƒÂ¢Ã¢â‚¬â€œÃ‚Â¼
  Monitor for errors (15-minute window)
    ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
    ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Errors detected ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Rollback
    ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Clean ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Done
```

### Rollback Plan

Every deployment should be reversible:

```yaml
# Manual rollback workflow
name: Rollback
on:
  workflow_dispatch:
    inputs:
      version:
        description: 'Version to rollback to'
        required: true

jobs:
  rollback:
    runs-on: ubuntu-latest
    steps:
      - name: Rollback deployment
        run: |
          # Deploy the specified previous version
          npx vercel rollback ${{ inputs.version }}
```

## Environment Management

```
.env.example       ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Committed (template for developers)
.env                ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ NOT committed (local development)
.env.test           ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Committed (test environment, no real secrets)
CI secrets          ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Stored in GitHub Secrets / vault
Production secrets  ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Stored in deployment platform / vault
```

CI should never have production secrets. Use separate secrets for CI testing.

## Automation Beyond CI

### Dependabot / Renovate

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: npm
    directory: /
    schedule:
      interval: weekly
    open-pull-requests-limit: 5
```

### Build Cop Role

Designate someone responsible for keeping CI green. When the build breaks, the Build Cop's job is to fix or revert ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â not the person whose change caused the break. This prevents broken builds from accumulating while everyone assumes someone else will fix it.

### PR Checks

- **Required reviews:** At least 1 approval before merge
- **Required status checks:** CI must pass before merge
- **Branch protection:** No force-pushes to main
- **Auto-merge:** Only if the team has decided to enable it; the agent does not enable or trigger merges on its own

## CI Optimization

When the pipeline exceeds 10 minutes, apply these strategies in order of impact:

```
Slow CI pipeline?
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Cache dependencies
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Use actions/cache or setup-node cache option for node_modules
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Run jobs in parallel
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Split lint, typecheck, test, build into separate parallel jobs
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Only run what changed
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Use path filters to skip unrelated jobs (e.g., skip e2e for docs-only PRs)
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Use matrix builds
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Shard test suites across multiple runners
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Optimize the test suite
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Remove slow tests from the critical path, run them on a schedule instead
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Use larger runners
    ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ GitHub-hosted larger runners or self-hosted for CPU-heavy builds
```

**Example: caching and parallelism**
```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '22', cache: 'npm' }
      - run: npm ci
      - run: npm run lint

  typecheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '22', cache: 'npm' }
      - run: npm ci
      - run: npx tsc --noEmit

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '22', cache: 'npm' }
      - run: npm ci
      - run: npm test -- --coverage
```

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "CI is too slow" | Optimize the pipeline (see CI Optimization below), don't skip it. A 5-minute pipeline prevents hours of debugging. |
| "This change is trivial, skip CI" | Trivial changes break builds. CI is fast for trivial changes anyway. |
| "The test is flaky, just re-run" | Flaky tests mask real bugs and waste everyone's time. Fix the flakiness. |
| "We'll add CI later" | Projects without CI accumulate broken states. Set it up on day one. |
| "Manual testing is enough" | Manual testing doesn't scale and isn't repeatable. Automate what you can. |

## Red Flags

- No CI pipeline in the project
- CI failures ignored or silenced
- Tests disabled in CI to make the pipeline pass
- Production deploys without staging verification
- No rollback mechanism
- Secrets stored in code or CI config files (not secrets manager)
- Long CI times with no optimization effort

## Verification

After setting up or modifying CI:

- [ ] All quality gates are present (lint, types, tests, build, audit)
- [ ] Pipeline runs on every PR and push to main
- [ ] Failures block merge (branch protection configured)
- [ ] CI results feed back into the development loop
- [ ] Secrets are stored in the secrets manager, not in code
- [ ] Deployment has a rollback mechanism
- [ ] Pipeline runs in under 10 minutes for the test suite
