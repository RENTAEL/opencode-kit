---
name: dependency-audit
description: Scan dependencies for CVEs, outdated packages, license issues, and unused deps to produce a prioritized remediation list
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: general
---
<!--
  TÃƒÆ’Ã…â€œRKÃƒÆ’Ã¢â‚¬Â¡E AÃƒÆ’Ã¢â‚¬Â¡IKLAMA
  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬
  Bu skill, projenin baÃƒâ€žÃ…Â¸Ãƒâ€žÃ‚Â±mlÃƒâ€žÃ‚Â±lÃƒâ€žÃ‚Â±klarÃƒâ€žÃ‚Â±nÃƒâ€žÃ‚Â± (npm, pip, vb.) gÃƒÆ’Ã‚Â¼venlik aÃƒÆ’Ã‚Â§Ãƒâ€žÃ‚Â±klarÃƒâ€žÃ‚Â±, eski sÃƒÆ’Ã‚Â¼rÃƒÆ’Ã‚Â¼mler
  ve kullanÃƒâ€žÃ‚Â±lmayan paketler aÃƒÆ’Ã‚Â§Ãƒâ€žÃ‚Â±sÃƒâ€žÃ‚Â±ndan tarar. Bulunan sorunlarÃƒâ€žÃ‚Â± ÃƒÆ’Ã‚Â¶ncelik sÃƒâ€žÃ‚Â±rasÃƒâ€žÃ‚Â±na gÃƒÆ’Ã‚Â¶re
  listeler ve gÃƒÆ’Ã‚Â¼venli gÃƒÆ’Ã‚Â¼ncellemeleri otomatik uygular. Her major release ÃƒÆ’Ã‚Â¶ncesi ve
  ayda bir ÃƒÆ’Ã‚Â§alÃƒâ€žÃ‚Â±Ãƒâ€¦Ã…Â¸tÃƒâ€žÃ‚Â±rÃƒâ€žÃ‚Â±lmalÃƒâ€žÃ‚Â±dÃƒâ€žÃ‚Â±r.

  NE ZAMAN: Her production release ÃƒÆ’Ã‚Â¶ncesi. AylÃƒâ€žÃ‚Â±k rutin. Yeni CVE duyurulduÃƒâ€žÃ…Â¸unda.
  ÃƒÆ’Ã¢â‚¬Â¡IKTI:    .agent/audits/dependency-audit-YYYY-MM-DD.md ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â ÃƒÆ’Ã‚Â¶ncelikli aksiyon raporu.
-->

# Dependency Audit Skill

## When to Trigger

- Before any production release
- Monthly cadence (add to sprint planning)
- After a CVE is publicly announced that might affect your stack
- When a team member says "we should update our packages"
- Before onboarding a new contributor (known-safe baseline)

## Step-by-Step Process

### 1. Detect Package Ecosystem

Identify which package managers are in use:

```
package.json        ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ npm / yarn / pnpm  (Node.js)
requirements.txt    ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ pip                (Python)
pyproject.toml      ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ pip / poetry       (Python)
Gemfile             ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ bundler            (Ruby)
go.mod              ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ go modules         (Go)
Cargo.toml          ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ cargo              (Rust)
```

Run the audit steps for each ecosystem found.

---

### 2. Security Vulnerability Scan

#### Node.js
```bash
npm audit
# or
yarn audit
# or
pnpm audit
```

#### Python
```bash
pip install pip-audit
pip-audit
```

#### General (all ecosystems)
```bash
# If using GitHub: check Security tab ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Dependabot alerts
# If using Snyk:
snyk test
```

**Triage each finding:**

| Severity | Action |
|----------|--------|
| Critical | Fix immediately before any other work |
| High | Fix before next release |
| Medium | Schedule for current sprint |
| Low | Track, fix when touching related code |

---

### 3. Outdated Package Scan

#### Node.js
```bash
npm outdated
```

#### Python
```bash
pip list --outdated
```

For each outdated package, check:
1. **How many major versions behind?** (1 minor = low urgency, 2+ major = high urgency)
2. **Is it a direct or transitive dependency?**
3. **Does the changelog mention breaking changes?**

---

### 4. Unused Dependency Detection

#### Node.js
```bash
npx depcheck
```

#### Python
```bash
pip install deptry
deptry .
```

For each unused dependency flagged:
- Verify it's truly unused (some are peer deps or used at runtime via config)
- If confirmed unused, remove from `package.json` / `requirements.txt`
- Re-run the app and tests to confirm nothing breaks

---

### 5. License Compliance Check

Flag any dependencies with licenses that may be incompatible with your project:

```bash
# Node.js
npx license-checker --summary

# Python  
pip install pip-licenses
pip-licenses
```

**License risk tiers:**

| License | Risk |
|---------|------|
| MIT, Apache 2.0, BSD | Safe for most uses |
| LGPL | Generally OK, check linking requirements |
| GPL | Risk if distributing proprietary software |
| AGPL | High risk ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â requires open-sourcing if used via network |
| Unknown | Must investigate before use |

---

### 6. Produce the Audit Report

Write findings to `.agent/audits/dependency-audit-<YYYY-MM-DD>.md`:

```markdown
# Dependency Audit ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â <YYYY-MM-DD>

## Summary
- **Critical vulnerabilities:** <N>
- **High vulnerabilities:** <N>
- **Outdated packages:** <N>
- **Unused packages:** <N>
- **License issues:** <N>

## Critical / High ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Action Required

### <package-name> @ <version>
- **CVE:** CVE-XXXX-XXXXX
- **Severity:** Critical
- **Description:** <what the vulnerability is>
- **Fix:** Upgrade to <version>
- **Breaking changes:** Yes/No ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â <details>

## Outdated Packages

| Package | Current | Latest | Urgency | Notes |
|---------|---------|--------|---------|-------|
| express | 4.17.1 | 5.0.0 | High | Major version ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â review changelog |
| lodash | 4.17.20 | 4.17.21 | Low | Patch only |

## Unused Dependencies (safe to remove)
- `left-pad` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â not imported anywhere
- `moment` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â replaced by `date-fns` but not removed

## License Issues
- `<package>` uses GPL-3.0 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â review with team before next release

## Recommendations
1. <prioritized action>
2. <prioritized action>
```

---

### 7. Execute Safe Fixes

For packages with **patch or minor** updates and **no breaking changes**:

```bash
# Node.js ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â safe updates only
npm update

# Python
pip install --upgrade <package>
```

After upgrading:
1. Run the full test suite
2. Do a smoke test of the running app
3. Commit with message: `chore: dependency security updates <YYYY-MM-DD>`

For **major version** upgrades, create a separate branch and task.

## Rules

- **Never auto-upgrade major versions** in bulk ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â do them one at a time.
- **Always run tests after any upgrade** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â even patch versions can break things.
- **Keep the audit report** even after fixes ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â it's a compliance record.
- **Critical vulnerabilities block releases** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â no exceptions without explicit sign-off.
- **Unused packages must be removed**, not just ignored ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â they are attack surface.
