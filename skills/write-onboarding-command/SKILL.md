---
name: write-onboarding-command
description: "A \"light\" onboarding command bootstraps a development session in one repository. Its job is to make the agent know **where** to find every piece of information it might need - not to hand it the information. It front-loads only what is core, non-obvious, or slow to discover, a..."
---
# Onboarding Command Writing

## Purpose

A "light" onboarding command bootstraps a development session in one repository. Its job is to make the agent know **where** to find every piece of information it might need - not to hand it the information. It front-loads only what is core, non-obvious, or slow to discover, and leaves anchored references for everything else, to be pulled on demand.

This is a specialization of `write-command`: all command conventions still apply (frontmatter, no H1 title, `## Step N -` structure, constraints before steps, no `---` rules between sections, report ending in `DONE`/`BLOCKED`). Load `write-command` for the base rules; this skill adds only what makes an onboarding command different. Sibling genre: when the command's job is to hand off an in-progress WORK STREAM (carrying history, non-rediscoverable session knowledge, and a future-work menu), that is a handoff command - `write-handoff-command` owns it, with inverted length rules; do not force that content into the light-onboarding shape. Name the file so the `-light` suffix reads as the lightweight bootstrap for that project - `<project>-light.md`, optionally with the local taxonomy prefix the repo already uses (e.g. `backend-light.md` in my-backend-mono, `develop-factorio-vlsi-light.md`).

## The Core Principle: anchor, don't enumerate

The value of a light onboarding command is measured by context saved, not information delivered. Every fact you inline costs the agent's context window on every session, whether the task needs it or not. So the test for every candidate fact is:

> Is this **core** (needed on almost every task), **non-obvious** (the agent would guess wrong), or **slow to discover** (many tool calls / trial-and-error to learn)? If yes, inline it. If not, anchor a reference to where it lives and stop.

The single sentence that captures the whole pattern, and belongs near the top of every such command:

> After this command completes, the agent knows **where** to find every piece of information it might need, not the information itself. It pulls content on demand when a task requires it.

An onboarding command that reproduces the README, lists every module, or pastes the full doc tree has failed - it is the heavy version. If the agent could get a fact in one obvious tool call when a task needs it, do not inline it; anchor the entry point instead.

## What to inline vs what to anchor

| Inline it (core / non-obvious / slow)                                                                                  | Anchor a reference instead (cheap to fetch on demand) |
| ---------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| The one-paragraph "what the project is"                                                                                | Full architecture / design docs                       |
| The build-and-see-it-live loop (the command that makes a change real, e.g. `yarn symlink` + restart)                   | Step-by-step setup instructions                       |
| The repeated structural shape (module/app/step anatomy) that unlocks navigating everything                             | An enumeration of every module/app/step               |
| The 1-3 hard boundaries an agent will not discover (an off-limits path, a vendored submodule, a load-bearing ordering) | Per-file caveats                                      |
| A single load-bearing operational fact that can surface mid-task (a solver status code, a credential-refresh rule)     | The full operational reference (link the doc page)    |
| The verification gate commands (typecheck / lint / test) + the traps that waste time                                   | Expected outputs / full CI config                     |
| Where credentials/config live (the path), and which are auto-managed                                                   | The credential values themselves                      |
| The lazy skill-loading map (which skill before which kind of task)                                                     | The skills' contents                                  |

The right-hand column items each get **one line naming the entry point** ("READMEs are the canonical per-module entry point; read `apps/<app>/README.md` when a task touches that app"), then a firm "do not read it now."

## Required shape

An onboarding command has a recognizable skeleton. Order matters - reference data and boundaries come before the steps so the agent internalizes them first.

1. **Frontmatter** - `description` in imperative mood naming the project and "lightweight ... discovery entry points."
2. **Opening paragraph** (no heading) - the anchor-not-enumerate sentence, plus one line on when to use the light version vs a heavier one.
3. **Project path table** - the absolute repo root(s). State plainly whether it is single-repo or spans sibling repos, so the agent does not hunt for a monorepo that is not there.
4. **What the project is (one paragraph)** - a single dense paragraph. Domain, the shape of the work, the core abstraction. This is the one place you _do_ teach content, because it is the map everything else hangs on.
5. **The load-bearing operational fact(s)** - the dev loop and/or the one fact that can surface at any time. Give these their own short section with a heading; do not bury them in a bullet list. (See "The dev loop is the highest-value inline".)
6. **Constraints** - lazy skill-loading map + durable owner conventions + the hard boundaries. (See "Constraints carry the boundaries".)
7. **Numbered steps** - the discovery-anchoring workflow. (See "Steps anchor entry points".)
8. **Report step** - what to confirm, ending in `DONE`/`BLOCKED`, then a fixed closing line: **"<project> light context loaded. What would you like to work on?"**

## The dev loop is the highest-value inline

The most time-wasting gap for an agent new to a repo is the moment its change does not take effect and it does not know why. If the repo has a non-obvious build/activate loop - compiled output, a symlink/copy step, a required restart, a codegen step, a submodule sync - inline it with its own heading and the exact command. Name the failure it prevents ("editing a `.ts` file does not update the running tool until `yarn symlink` + restart"). This single fact often saves more agent time than the rest of the command combined. If the loop is trivial (`the change is live on save`), say so in one line and move on.

## Constraints carry the boundaries

The `## Constraints` section does triple duty in an onboarding command:

- **Lazy skill map** - a bullet list of "load `<skill>` before `<kind of task>`". This is the load-bearing substitute for pre-loading skills. Keep it to skills that genuinely gate a task type; do not list every skill in the repo.
- **Durable owner conventions** - the standing preferences that apply to every change (fallback policy, commit cadence, "prefer fewer lines", "keep docs in sync"). These are the things a contributor learns by being corrected; inline them so the agent is not corrected.
- **Hard boundaries** - the 1-3 things that are genuinely off-limits or load-bearing, each with the reason and, where it exists, a reference to the doc that explains why. Examples that recur: an untouchable module, a vendored submodule, a manually-maintained dependency manifest, an in-source ordering that feeds a downstream solver. State the boundary AND the consequence of crossing it.

Put constraints before the numbered steps (base command rule) so they are internalized before any action.

## Steps anchor entry points, they do not do work

Unlike a task command, an onboarding command's steps mostly _read one anchor file and stop_. The recurring, effective step sequence:

- **Step 1 - Load Minimum Skills (Blocking Gate)** - load only the 2-3 baseline orientation skills; explicitly defer the rest to the lazy map. Mark it a blocking gate.
- **Step 2 - Scan Top-Level Layout** - `codebase_project_structure` at the root with `maxDepth: 2`, and the canonical deeper scans written out as copy-pasteable calls for "when a task requires it". Do not drill now.
- **Anchor steps** - one per major information source (docs entry point / sidebar config, README index, build+run, tests+verification, credentials discovery). Each names the file(s), says what lives there, and ends with "read it only when a task needs it".
- **Optional standing-setup step** - if the command establishes something every session needs (e.g. warming thinking-partner models), make it an explicit step with the exact `oc_*` dispatch and how to use it well.
- **Report step** - confirmations, warnings, `DONE`/`BLOCKED`, then the fixed closing line.

Each anchor step is a pointer with a "do not read now" guard. The guard is what keeps the command light - without it, an eager agent reads every anchored file and the command stops being light.

## Keep it current, keep it honest

An onboarding command asserts concrete facts (paths, module counts, the dev-loop command, which module is off-limits). Those drift. Before writing or updating one, verify each inlined fact against the live repo with tools - read the actual `package.json` scripts, list the actual modules, read the actual build script - rather than trusting memory or a prior version of the repo. A stale onboarding command is worse than none: it sends the agent confidently to the wrong place. When a fact is inherently drift-prone (a count, a version), prefer a stable phrasing ("~19 modules", "the modules under `src/modules/`") over a brittle exact number, or anchor the live source instead of copying the value.

## Anti-Patterns

- Enumerating content the agent can fetch in one obvious tool call (every module, every doc page, every env var) - anchor the entry point instead
- Omitting the dev/activate loop when it is non-obvious - the single biggest time sink for a new agent
- Anchor steps without a "do not read it now" guard - an eager agent reads everything and the command is no longer light
- Pre-loading language/testing/authoring skills instead of providing a lazy load map in Constraints
- A "what the project is" section longer than one dense paragraph - that is the heavy version leaking in
- Stale inlined facts (wrong paths, dropped modules, outdated commands) from trusting memory over verifying against the live repo
- Brittle exact counts that drift - prefer "~N" or anchor the live source
- Burying the load-bearing operational fact (dev loop, solver status, credential rule) inside a bullet list instead of giving it a heading
- Missing the fixed closing handoff line, so the session does not clearly transition to "what would you like to work on?"
- Boundaries stated without their consequence ("do not touch X" without "because X does Y and breaking it does Z")

## Rules

- Name the file `<project>-light.md` (optionally with the repo's existing command-name prefix); description names the project and "lightweight ... discovery entry points"
- Lead with the anchor-not-enumerate sentence; state single-repo vs multi-repo explicitly in a path table
- Inline only core / non-obvious / slow-to-discover facts; anchor everything else with a one-line "read on demand" pointer
- Give the dev/activate loop and any always-relevant operational fact their own heading, not a buried bullet
- Constraints section carries the lazy skill-loading map, durable owner conventions, and the 1-3 hard boundaries (each with its consequence)
- Steps anchor entry points and stop; every anchor step has a "do not read it now" guard
- Verify every inlined fact against the live repo before writing; prefer stable phrasing for drift-prone values
- End with the report (`DONE`/`BLOCKED`) and the fixed closing line: "<project> light context loaded. What would you like to work on?"
- All base `write-command` conventions still apply
