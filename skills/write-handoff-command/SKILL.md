---
name: write-handoff-command
description: "A handoff command transfers an **in-progress work stream** from the agent that did the work to the future sessions that will continue it. It is written at a milestone - a large migration finished, a phase closed, a deployment deferred - by the agent whose context is about to b..."
---
# Handoff Command Writing

## Purpose

A handoff command transfers an **in-progress work stream** from the agent that did the work to the future sessions that will continue it. It is written at a milestone - a large migration finished, a phase closed, a deployment deferred - by the agent whose context is about to be lost, for its own future self.

This is a specialization of `write-command`: all base command conventions apply (frontmatter, no H1 title, `## Step N -` structure, constraints before steps, report ending in `DONE`/`BLOCKED`, fixed closing line). It is a **sibling** of `write-onboarding-command`, not a variant of it: an onboarding command orients an agent to a repository and optimizes for context frugality; a handoff command preserves session knowledge and optimizes for completeness. The two genres share surface structure (repo tables, anchors, dev loops - defer to `write-onboarding-command` for those parts) but obey **inverted length rules**. Mislabeling a handoff as a "light" onboarding command causes the exact failure the genre exists to prevent: the light framing pressures the author into trimming the nuances that were the entire point of writing it down.

## The Core Inversion: the payload is what cannot be rediscovered

An onboarding command asks of every fact: _"can the agent fetch this in one obvious tool call when needed?"_ - and if yes, anchors a pointer instead of inlining. A handoff command asks the opposite question:

> Will a fresh agent, with the full repo and all its docs in front of it, ever **rediscover** this? If not, inline it completely - there is no arbitrary length limit on a handoff command.

State that explicitly near the top of the command, and mark the payload sections as the reason the command exists (e.g. _"the 'Facts You Will Not Rediscover' and 'Techniques' sections are the payload - read them fully"_). An eager-to-skim future agent needs the instruction that these sections are not optional context.

What repeatedly qualifies as non-rediscoverable (use as a generation checklist, not an exhaustive taxonomy):

- **Decisions and their why.** The diff shows _what_ changed; the rationale, the alternatives rejected, and the review findings that shaped it live only in the session. ("The envelope interceptor is registered inside CommonModule, NOT in the root module's providers, so it lands after the serializer - Nest scans root providers first; moving it reintroduces a reviewed-and-fixed bug.")
- **Deliberate non-fixes.** Bugs preserved on purpose (behavior parity, frozen contracts) look like ordinary bugs to a fresh agent, which will "helpfully" fix them. Name each one, why it is preserved, what pins it (test/snapshot), and what a conscious fix must update.
- **Load-bearing arrangements that look arbitrary.** Import order, env-file precedence (dotenv first-wins vs last-wins), registration order, ignore patterns protecting byte-parity zones. These survive only as "it works, don't know why" unless the why is written down.
- **Failures that only surface at a distance.** Anything that passes every local gate and fails at deploy time, in CI, or under a rare condition - with the symptom described the way it will actually present ("crashes at config validation before the logger exists - CloudWatch shows nothing").
- **Deleted or absent-by-design surface.** What a fresh agent would otherwise hunt for or recreate: removed packages, a deliberately missing prod config, a dormant code path nothing calls.
- **Trap symptoms and their recoveries.** "If X 400s, check Y first" knowledge bought with debugging time.
- **Techniques rebuilt repeatedly during the work.** A verification script, a normalization recipe for diffing, a delegation/review pattern with its exact parameters. Inline the skeleton (~30 lines is fine); the future agent should paste-and-adapt, not reinvent.

And what does NOT belong: anything a maintained document already records. If a ledger, ADR file, or README carries a fact, the handoff **anchors** it and states the relationship ("`docs/migration/MIGRATION.md` is the compact authority; this command is its expanded runbook - if they disagree, investigate before acting"). The handoff inlines only the layer _above_ the written record: the context, ordering, and reasoning the record omits.

## Required Shape

1. **Frontmatter** - `description` in imperative mood naming the project, the work stream, and that this is a handoff.
2. **Opening paragraph** - declares it is a handoff from a specific effort, states the no-arbitrary-length-limit rule, names the payload sections, and points to any sibling handoff commands with a "do not duplicate its content from memory" guard.
3. **Repo/branch table** - as in onboarding commands, but include work-stream-specific rows a plain onboarding would not need (a reference branch read via `git show`, a superseded working copy that must not be edited by mistake).
4. **What the project is** - one dense paragraph (onboarding convention).
5. **History section** - one compact paragraph on what was done and why, anchored to the full written record. History is orientation, not payload: resist re-narrating what the ledger already tells.
6. **Operational spine** - dev loop, verification gate, and any always-relevant check (each with its own heading, per onboarding conventions). Include the exact commands; a handoff reader has even less patience for discovery than an onboarding reader.
7. **`## Facts You Will Not Rediscover From the Tree`** - the primary payload. One bullet per fact; each bullet carries the fact, the why, and the consequence of violating it. Order by damage potential, most dangerous first.
8. **`## Techniques Worth Reusing`** - reusable procedures with inline skeletons and exact tool parameters.
9. **Constraints** - lazy skill map, durable conventions, hard boundaries (onboarding conventions apply).
10. **Steps** - see below; always beginning with a verify-current-state step and ending with the work menu, report, and fixed closing line ("<project> <stream> handoff loaded. What would you like to work on?" or similar).

## Steps: verify first, menu last

- **Step 1 - Verify Current State.** Handoffs decay faster than onboarding commands: they describe a moment in a work stream, and the stream may have moved (by the user, by another session, by an external actor). The first step checks the assumptions the handoff depends on - branch positions, whether listed gaps already landed, whether referenced files still exist - and explicitly instructs: _skip any change below that already landed._
- **Anchor step** - the entry-point table, with work-stream anchors (ledger, contract snapshot, reference branch) alongside the usual ones, each with the "read on demand, not now" guard.
- **Final work step - Present the Work Menu.** A handoff serves a user who directs the continuation; the agent must not assume which thread to pull. Present a numbered menu, ask, and wait. Menu conventions:
  - Each item carries enough context to be chosen from the menu alone (one to three sentences: what, why it matters, the honest trade-off if there is one).
  - Where a demo/walkthrough item will hit a known-broken-by-design behavior, say so in the item ("expect the 422 in local mode - explain it, don't debug it") so the agent does not burn the session debugging a preserved bug.
  - Include an **agent's-own-backlog item**: the next steps the departing agent believes matter but the user has not asked for. Offer, let the user pick.
  - Items that belong to a sibling handoff route there by name instead of duplicating its runbook.

## The Ordered-Runbook Variant

When the handed-off work is a **future task with ordering constraints** (a deployment, a cutover, a multi-system rollout) rather than an open-ended continuation, add these on top of the base shape:

- **A `Verified Facts the Ordering Depends On` section** before the changes: everything checked against live systems, with the verification date stated and re-greppable anchors ("`modules/common/main.tf`, the `iam_github_oidc_role_cicd` block") instead of line numbers - line numbers rot fastest. Say explicitly: _spot-check if stale, do not re-derive._
- **Changes as an ordered list where the ordering is explained**, not just stated: which change gates which ("1 gates everything - workflows never fire without it; 4 gates only staging promotion"). For each change: what, where exactly, **why**, and the _consequence of skipping it_ described as the failure the future agent would actually observe ("dev deploys work; staging promotion fails at its final step and produces no semver, which then blocks prod").
- **Classify each change**: hard gate vs quality-of-life vs optional-skip-recommended. The future session may be short; it must know what it can defer.
- **Mark user-decision points.** Changes that are the user's call (a branch cutover, a first prod deploy) get flagged as decisions to confirm, never actions to take.
- **A first-run runbook** for the moment everything is in place: the expected happy path _including expected no-ops_ ("the first migration task run is a no-op - the journal already matches"), where to watch (exact tool names), and what self-heals vs what needs intervention.
- **A drift clause and self-update duty**: if reality disagrees with the handoff, investigate before acting, and update both the written record and the handoff command when drift is found.

## Verify Before Writing, Date What You Verified

The onboarding rule (verify every inlined fact against the live repo) applies with more force here, because handoff facts include _live external state_ (cloud resources, GitHub settings, branch layout) that the author checked once. Re-check each fact with tools while writing - the author's memory of "how it was mid-migration" is exactly the kind of stale knowledge that sinks the future session. Then date the verification in the command ("read from the live Terraform on 2026-08-06") so the future agent can calibrate trust by age.

## Anti-Patterns

- Framing a handoff as a "light" onboarding command - the light framing pressures the author into trimming the payload, which defeats the purpose
- Trimming non-rediscoverable facts for brevity - the length rules are inverted here; completeness of the payload is the success criterion
- Re-narrating history the ledger/ADR already records instead of anchoring it and carrying only the layer above
- Duplicating a sibling handoff's runbook from memory instead of routing to it by name
- Stating a load-bearing arrangement without its why and its consequence - "don't move this" without "because X scans Y first and moving it reintroduces Z"
- Listing a preserved bug without what pins it and what a conscious fix must update - the fresh agent will either re-fix it silently or fear touching it forever
- Line-number anchors into files the work stream does not own - they rot; use grep-able identifiers
- Undated verified facts about live external state - the future agent cannot calibrate trust
- No verify-current-state step - the handoff asserts a moment in time and the stream moves on without it
- A work menu that assumes the continuation instead of presenting options and asking
- Missing the consequence-of-skipping on ordered changes - ordering without stakes gets reordered by a future agent that cannot see why it matters

## Rules

- Name the file so "handoff" appears in it: `<project>-<stream>-handoff.md` (e.g. `my-app-mono-handoff.md`, `my-app-infra-handoff.md`)
- Declare the genre and the no-arbitrary-length-limit rule in the opening paragraph; name the payload sections as must-read
- The payload test is "will a fresh agent ever rediscover this?" - inline fully when no, anchor when a maintained document already records it
- Every payload fact carries its why and its consequence; order by damage potential
- Techniques include inline skeletons and exact tool parameters, ready to paste-and-adapt
- Anchor the written record (ledger/ADR) and state the authority relationship plus a disagreement clause
- Step 1 verifies current state and instructs skipping already-landed changes; the final step presents a work menu and asks
- Ordered-runbook variant: dated verified-facts section, ordering with why + consequence-of-skipping, gate/quality-of-life classification, user-decision flags, first-run runbook, drift + self-update clause
- Verify every fact with tools while writing; date verifications of live external state; prefer re-greppable anchors over line numbers
- All `write-command` conventions apply; defer to `write-onboarding-command` for the shared orientation parts (repo table, project paragraph, dev loop, anchor guards, closing line)
