---
name: architecture-review
description: "Read the implementation plan (typically `implementation_plan.md` or the artifact from `writing-plans`)."
---
<!--
  TÃƒÆ’Ã…â€œRKÃƒÆ’Ã¢â‚¬Â¡E AÃƒÆ’Ã¢â‚¬Â¡IKLAMA
  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬
  Bu skill, bir implementasyon planÃƒâ€žÃ‚Â± kod yazÃƒâ€žÃ‚Â±lmadan ÃƒÆ’Ã‚Â¶nce "ikinci gÃƒÆ’Ã‚Â¶z" olarak
  stres testine tabi tutar. AÃƒâ€¦Ã…Â¸Ãƒâ€žÃ‚Â±rÃƒâ€žÃ‚Â± mÃƒÆ’Ã‚Â¼hendislik, dÃƒÆ’Ã‚Â¶ngÃƒÆ’Ã‚Â¼sel baÃƒâ€žÃ…Â¸Ãƒâ€žÃ‚Â±mlÃƒâ€žÃ‚Â±lÃƒâ€žÃ‚Â±klar, eksik
  hata senaryolarÃƒâ€žÃ‚Â±, gÃƒÆ’Ã‚Â¼venlik aÃƒÆ’Ã‚Â§Ãƒâ€žÃ‚Â±klarÃƒâ€žÃ‚Â± ve ÃƒÆ’Ã‚Â¶lÃƒÆ’Ã‚Â§eklenebilirlik sorunlarÃƒâ€žÃ‚Â±nÃƒâ€žÃ‚Â± erken tespit eder.
  YanlÃƒâ€žÃ‚Â±Ãƒâ€¦Ã…Â¸ temele inÃƒâ€¦Ã…Â¸a etmenin maliyeti ÃƒÆ’Ã‚Â§ok yÃƒÆ’Ã‚Â¼ksektir ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â bu skill o maliyeti sÃƒâ€žÃ‚Â±fÃƒâ€žÃ‚Â±ra indirir.

  NE ZAMAN: Plan hazÃƒâ€žÃ‚Â±rlandÃƒâ€žÃ‚Â±ktan SONRA, kod yazmaya baÃƒâ€¦Ã…Â¸lamadan ÃƒÆ’Ã¢â‚¬â€œNCE. Zorunludur.
  ÃƒÆ’Ã¢â‚¬Â¡IKTI:    ÃƒÂ°Ã…Â¸Ã¢â‚¬ÂÃ‚Â´ Blocker / ÃƒÂ°Ã…Â¸Ã…Â¸Ã‚Â¡ Warning / ÃƒÂ°Ã…Â¸Ã¢â‚¬ÂÃ‚Âµ Note listesi + Approved/Revisions Required kararÃƒâ€žÃ‚Â±.
-->

# Architecture Review Skill

## When to Trigger

- After `writing-plans` produces an implementation plan, *before* `executing-plans`
- When a significant refactor is proposed
- When adding a new external service or integration
- When the team is debating between two approaches
- When something "feels off" about a design but you can't articulate why

## Step-by-Step Process

### 1. Load the Plan

Read the implementation plan (typically `implementation_plan.md` or the artifact from `writing-plans`).

Extract:
- Components being built
- Data flow between components
- External dependencies
- Assumptions the plan makes

### 2. Run the Checklists

Work through each checklist section. For every "No" or "Unclear" answer, flag it as a finding.

---

#### A. Complexity Check
- [ ] Is this the simplest solution that could work?
- [ ] Are there off-the-shelf solutions (libraries, services) that cover 80%+ of this?
- [ ] Does each component have a single, clear responsibility?
- [ ] Would a junior developer understand this in 30 minutes?

#### B. Coupling & Cohesion
- [ ] Can each module be tested in isolation?
- [ ] Are there circular dependencies? (A needs B needs A)
- [ ] Is data ownership clear? (only one place writes to each piece of state)
- [ ] Is the public API surface minimal? (don't expose what doesn't need to be exposed)

#### C. Data & State
- [ ] Is the source of truth for each piece of data clearly defined?
- [ ] What happens if the datastore goes down?
- [ ] Is there any global mutable state? If so, is it justified?
- [ ] Are database migrations planned for any schema changes?

#### D. Failure Modes
- [ ] What happens when each external service is unavailable?
- [ ] Are there retry mechanisms with backoff for network calls?
- [ ] Are there timeouts on all I/O operations?
- [ ] Is there a circuit breaker if a downstream dependency degrades?
- [ ] What does a partial failure look like to the user?

#### E. Security
- [ ] Is all user input validated and sanitized?
- [ ] Are secrets managed via env vars / secrets manager (not hardcoded)?
- [ ] Is authentication and authorization clearly separated?
- [ ] Are there any SQL injection / XSS / CSRF vectors?
- [ ] Does the principle of least privilege apply to service accounts?

#### F. Scalability
- [ ] What is the expected load in 6 months? Does the design handle it?
- [ ] Are there any obvious N+1 query problems?
- [ ] Is any caching planned? Is the invalidation strategy defined?
- [ ] Are background jobs used for anything that could block the request cycle?

#### G. Observability
- [ ] Is structured logging planned?
- [ ] Are there metrics/health endpoints?
- [ ] Will errors surface in a monitoring tool (not just logs)?
- [ ] Is there a way to trace a request end-to-end?

#### H. Operability
- [ ] Can this be deployed without downtime?
- [ ] Is there a rollback plan if the deployment goes wrong?
- [ ] Are environment differences (dev/staging/prod) documented?

---

### 3. Classify Findings

For each "No" or "Unclear" found above, classify it:

| Class | Meaning | Action |
|-------|---------|--------|
| ÃƒÂ°Ã…Â¸Ã¢â‚¬ÂÃ‚Â´ Blocker | Must fix before implementation | Revise plan |
| ÃƒÂ°Ã…Â¸Ã…Â¸Ã‚Â¡ Warning | Should address, can proceed carefully | Add a task to backlog |
| ÃƒÂ°Ã…Â¸Ã¢â‚¬ÂÃ‚Âµ Note | Nice to have, low risk | Document and move on |

### 4. Produce the Review Report

Her zaman ayrÃƒâ€žÃ‚Â± bir dosyaya yaz ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â **plan dosyasÃƒâ€žÃ‚Â±nÃƒâ€žÃ‚Â± kirletme**:
```
.agent/reviews/architecture-review-<plan-slug>.md
```

EÃƒâ€žÃ…Â¸er bu review'dan ÃƒÆ’Ã‚Â¶nemli bir mimari karar ÃƒÆ’Ã‚Â§Ãƒâ€žÃ‚Â±ktÃƒâ€žÃ‚Â±ysa, ek olarak `knowledge-base-update` skill'ini kullanarak `decision` tipiyle knowledge base'e de ekle ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `project-context-primer` oradan okuyacak.

```markdown
# Architecture Review ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â <plan name>
**Date:** <YYYY-MM-DD>
**Reviewer:** Agent

## Verdict
<Approved | Approved with conditions | Revisions required>

## ÃƒÂ°Ã…Â¸Ã¢â‚¬ÂÃ‚Â´ Blockers
### 1. <Finding title>
**Checklist item:** Failure Modes ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â timeout on I/O
**Issue:** The email service call has no timeout. If SendGrid hangs, the entire request thread blocks.
**Recommendation:** Wrap in a 5-second timeout; use a background job queue for non-critical emails.

## ÃƒÂ°Ã…Â¸Ã…Â¸Ã‚Â¡ Warnings
### 1. <Finding title>
...

## ÃƒÂ°Ã…Â¸Ã¢â‚¬ÂÃ‚Âµ Notes
### 1. <Finding title>
...

## Summary
<Overall health of the architecture in 2-3 sentences.>
```

### 5. Gate: Proceed or Revise?

- If there are any ÃƒÂ°Ã…Â¸Ã¢â‚¬ÂÃ‚Â´ **Blockers**: stop. Share the report with the user and revise the plan before any code is written.
- If there are only ÃƒÂ°Ã…Â¸Ã…Â¸Ã‚Â¡/**ÃƒÂ°Ã…Â¸Ã¢â‚¬ÂÃ‚Âµ**: proceed, but ensure warnings are tracked as tasks.

## Rules

- **Be specific, not generic.** "You should add error handling" is useless. "The `fetchUser()` call on line 42 of the plan has no 404 handling" is a review.
- **Don't block on stylistic preferences.** Blockers are objective risks, not taste.
- **Never approve a plan with an undefined failure mode for a critical path.**
- **If you can't understand part of the plan, that is itself a finding** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â clarity is a requirement.
