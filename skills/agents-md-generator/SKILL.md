---
name: agents-md-generator
description: "Produce an `AGENTS.md` that serves as an onboarding document for AI coding agents in this repository. The file is short, specific to the repo, and structured so the most important rules appear first."
---
# AGENTS.md generator

Produce an `AGENTS.md` that serves as an onboarding document for AI coding agents in this repository. The file is short, specific to the repo, and structured so the most important rules appear first.

Gates follow the shared contract in [Gate Contract](../orchestrator-framework/references/gate-contract.md) (confirm-or-revise exception ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â see the [Confirm-or-Revise Exception](../orchestrator-framework/references/confirm-or-revise-exception.md)).

## Entry Gate

The input resolution below IS this skill's entry gate:

## Input resolution

`$ARGUMENTS` is optional. It may be:

- empty ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ write to `AGENTS.md` at the repo root.
- a directory path ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ write `AGENTS.md` inside that directory (useful for nested per-area guides, e.g. `src/api/AGENTS.md`).
- a full file path ending in `.md` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ write there verbatim.

If the target file already exists, do **not** silently overwrite. Switch to the update flow under "Procedure ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Update path". The default behavior is a surgical edit that preserves still-valid content, not a rewrite.

## Scope detection ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â repo-level vs. directory-level

The same skill can produce two materially different documents depending on **where** it's invoked from. Detect the scope before discovery so the draft targets the right altitude.

1. **Resolve the target directory.** If `$ARGUMENTS` names a path, that's the target. Otherwise it's the current working directory (`pwd`).
2. **Compare against the repo root.** Run `git rev-parse --show-toplevel`. If the target directory equals the repo root ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ **repo-level scope**. If it's a subdirectory (e.g. `src/components/`, `packages/api/src/routes/`, `app/api/`) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ **directory-level scope**.

**Repo-level scope.** Follow the procedure and "Output structure" below as written ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the document is a high-level onboarding guide (project structure, build commands, CI gate, commit conventions, etc.).

**Directory-level scope.** Drop the repository-onboarding framing entirely. The reader already knows the repo; they need the rules of _this_ directory. Reorient discovery and output:

- **Discover locally first.** Inspect the files actually living next to the target: sibling source files, the nearest `index.ts`/`Application.java`, co-located tests, the parent directory's README if any, and any nested config (e.g. `tsconfig.json`, `.eslintrc`, `application.yml`, route manifests) that overrides repo-level defaults. Only consult repo-root docs (`README.md`, `AGENTS.md`) to **resolve conflicts** or pull a single canonical `@`-reference ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â not as the primary source.
- **Infer the local pattern by reading siblings.** What shape do existing files in this directory take? Component file layout, naming (`PascalCase.tsx`, `camelCase.ts`, `*.handler.ts` for Node.js; `PascalCase.java`, `*Controller.java`, `*Service.java` for Spring), default vs. named exports (Node.js) or package-private vs. public visibility (Java), prop/argument conventions, where types/styles/tests live relative to the unit, error-handling idioms, what gets imported from where. The AGENTS.md captures the convention you observed, not generic advice.
- **Reframe sections around the local unit.** Replace repo-level sections with directory-relevant ones. Useful defaults (adapt to what's there):
  - _Adding a new \<unit\>_ ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â concrete steps for the dominant artifact in this directory (component, route handler, migration, hook, worker, etc.), citing one existing sibling as the reference shape via `@./<sibling-file>`.
  - _File layout & naming_ ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â naming pattern, co-location rules (test next to source? styles inline? types in a sibling file?), barrel-export policy if one exists.
  - _Local conventions_ ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â props/args shape, state/data-flow rules, allowed imports (and forbidden ones ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â e.g. "components in this directory must not import from `src/server/`"), accessibility or i18n rules visible in siblings.
  - _Testing this unit_ ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the test pattern used by neighbors, how to run just this directory's tests.
  - _Tripwires_ ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â directory-specific "never do X" rules visible in siblings or a nearby AGENTS.md fragment.
- **Skip the repo-level sections.** No top-level project structure map, no monorepo package list, no global build/CI overview, no commit-convention recap ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â those belong in the root `AGENTS.md`. If the reader needs them, link once: `See @AGENTS.md at the repo root for repo-wide rules.`
- **Length budget shrinks.** Aim for **120ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“250 words** of body for directory-level guides; the surface area is smaller, and padding here is worse than at the root.

The Quality guards still apply, with one substitution: guard 5 ("Critical rules first") becomes "Local rules first" ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the highest-leverage line is the one that prevents a wrong-shaped sibling from landing in this directory.

## Interactive prompts

Whenever the procedure says _"ask the user"_, use the `question` tool with labeled options. If a step requires free-form input, ask via a plain conversational message instead.

## Parallel research via subagents (optional)

If the repo is large enough to benefit (roughly >20 top-level files), use the `Task` tool to fan out independent reads in **one batched call** (multiple subagents in a single invocation, not sequentially):

- one subagent reads `README.md`, existing `AGENTS.md`, top-level `docs/` index
- one inspects the manifest + lint/format/type configs
- one inspects test config + CI workflows
- one runs the git-history queries via `Bash` (commit conventions, last-touch on AGENTS.md, diff range since `LAST_TOUCH`)

Each subagent should return a **short structured report** (ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â¤200 words: facts only, with `path:line` citations) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â not a full file dump. The main agent then synthesizes the AGENTS.md from those reports.

**Skip the fan-out if** the repo is small (under ~20 top-level files), or you've already loaded most of the relevant files in the current context.

**Do not delegate** the synthesis step (drafting and Quality-guard checks). Drafting requires holding the full picture in one context to enforce the 200ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“400 word budget, ordering, and `@`-reference policy.

## What this skill does NOT do

- Does not invent project facts. Every claim in the output must trace back to a file, command, or commit you actually inspected.
- Does not embed multi-line code or config snippets. Use `@`-references to canonical files instead (e.g. `@package.json`, `@tsconfig.json`, `@docs/architecture.md`).
- Does not write generic engineering advice ("write clean code", "follow best practices", "handle errors properly"). If a rule cannot be checked against a diff, drop it or rewrite it concretely.
- Does not restate framework defaults, language tutorials, or anything the AI assistant already knows from training. Only project-specific knowledge earns a line.
- Does not edit unrelated files. The skill writes one markdown file and stops.

## Procedure

**First, branch on existence.** Before discovering anything else, check whether the resolved target path already exists (use `Read` or `Glob`). If it does, follow the **Update path** below. If not, follow the **Create path**.

### Create path

1. **Discover.** Read in this order, skipping what doesn't exist:
   - `README.md`, existing `AGENTS.md`, top-level `docs/` index.
   - Manifest: `package.json` (scripts, workspaces, engines) for Node.js, or `pom.xml` / `build.gradle` (plugins, dependencies, profiles) for Spring Java.
   - Lint/format/type configs: `.eslintrc*`, `oxlint*`, `biome.json`, `tsconfig.json`, `.editorconfig` for Node.js; `checkstyle.xml`, `spotbugs-exclude.xml`, `.editorconfig` for Spring Java.
   - Test config: `vitest.config.*`, `jest.config.*`, `playwright.config.*`, `*.test.*` locations for Node.js; `src/test/`, `*Test.java`, `*IT.java`, Surefire/Failsafe plugin config in `pom.xml` for Spring Java.
   - CI: `.github/workflows/*` (one or two files; just enough to know the gate).
   - Layout: top two levels of the tree (use `Glob` or `Bash`), workspace package list if monorepo.
   - History: `git log --oneline -n 30` to learn commit-message conventions; `git config remote.origin.url` for PR target.
2. **Extract.** From discovery, write down for yourself:
   - The 1ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“3 commands an agent runs most often (build, test, lint, dev server).
   - The handful of conventions a reviewer would actually flag in PR review (naming patterns, file layout, commit prefix style).
   - Any hard "never do X" rule visible in `AGENTS.md`, README, or CI validators.
   - Where deeper docs live, so the AGENTS.md can point to them instead of duplicating.
3. **Draft.** Write the file per "Output structure" below.
4. **Self-check before writing.** Run the five guards in "Quality guards". If any fail, revise the draft, do not write yet.
5. **Write.** Use the `Write` tool to create the file at the resolved path. Confirm the path and word count back to the user.

### Update path

Triggered when the target file already exists. The default is a **surgical edit**: keep what's still true, fix what's stale, fill what's missing, and remove what's been deleted from the repo. Do not rewrite from scratch unless the user asks.

1. **Inventory the existing file.**
   - Read the full file.
   - List its current sections (H1/H2/H3 headings) and the rules/commands under each.
   - Extract every `@`-reference and every relative path or filename it cites.

2. **Date the file via git.**
   - `git log --follow --format="%h %ad %s" --date=short -- <path>` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â full edit history of the file.
   - Note the **last-touched commit hash** and date. Call this `LAST_TOUCH`.
   - If the file is untracked (`git ls-files --error-unmatch <path>` fails), treat it as freshly authored: skip git-diff steps and run the full Create path discovery, but still preserve any obviously project-specific content the user wrote.

3. **Diff repo state since `LAST_TOUCH`.** Use these checks (skip any whose target the file doesn't reference):
   - `git diff --stat LAST_TOUCH..HEAD -- README.md AGENTS.md docs/` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â has top-level documentation moved or changed?
   - `git diff LAST_TOUCH..HEAD -- package.json pom.xml build.gradle` (whichever exists) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â for **scripts**, **dependencies**, **engines**, **workspaces**. Pay closest attention to the `scripts` block (Node.js) or plugin/dependency changes (Maven/Gradle): renamed/added/removed scripts or build targets are the most common source of stale AGENTS.md content.
   - `git diff LAST_TOUCH..HEAD -- .eslintrc* oxlint* biome.json tsconfig.json .editorconfig checkstyle.xml spotbugs-exclude.xml` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â has the lint/format/type toolchain changed?
   - `git diff LAST_TOUCH..HEAD -- vitest.config.* jest.config.* playwright.config.*` (Node.js) or `pom.xml` Surefire/Failsafe sections (Spring Java) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â has the test stack or layout changed?
   - `git diff --stat LAST_TOUCH..HEAD -- .github/workflows/` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â has the CI gate changed?
   - `git log --oneline LAST_TOUCH..HEAD -- <commit-conventions-relevant-area>` and `git log --oneline -n 30` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â does the commit-style observation in the file still match recent history?
   - For each `@`-reference and path the file mentions: use `Read` or `Glob` to check whether the path still exists. If it no longer exists or has been renamed, that line is stale.

4. **Classify each line of the existing file** into one of four buckets:
   - **KEEP** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â still accurate; cited file/command/path still exists with the same shape.
   - **UPDATE** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â directionally right but a detail is stale (renamed script, moved path, changed tool, version bump). Note the exact replacement.
   - **REMOVE** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the underlying file/command/convention no longer exists, or the rule has been contradicted by a newer source (`AGENTS.md`, README) that you trust more.
   - **MISSING** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â not currently in the file but should be (new top-level package, new required script, new "never do X" rule landed via CI validator, new commit convention visible in `git log`).
     Keep this classification as a short table you can show the user. Cite `path:line` (in the existing AGENTS.md) for every UPDATE/REMOVE entry, and cite the source-of-truth path (e.g. `package.json:42`) for every UPDATE/MISSING entry.

5. **Confirm scope before editing.** Use the `question` tool with these options:
   - **Apply the proposed updates** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â execute the UPDATE/REMOVE/MISSING list as targeted edit operations; KEEP lines are not touched.
   - **Show me the change list first** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â print the classification table to chat, no edits, then ask again.
   - **Full regenerate** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â discard the existing file and run the Create path. Use only when the existing file is mostly stale or the user explicitly wants a clean slate.
   - **Cancel** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â no changes.

6. **Edit surgically.** For the "Apply" choice, prefer multiple targeted `Write` calls (one per UPDATE/REMOVE/MISSING entry) over a single full-file rewrite. This preserves authorial voice in KEEP sections and produces a reviewable diff. If section ordering violates the "critical rules first" guard from the Quality guards and the user approved updates, you may move whole sections ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â but only sections, never re-author rule wording silently.

7. **Re-run the Quality guards** on the updated file. The same five gates apply. If a guard now fails because of the update (e.g. body grew past 400 words after MISSING additions), trim KEEP content that has become low-leverage rather than dropping the new MISSING content.

8. **Report.** Confirm path, new word count, and a one-line summary of what changed in each bucket (e.g. _"3 updated, 1 removed, 2 added; section order unchanged"_).

## Output structure

The document title is `# Repository Guidelines`. Target length is **200ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“400 words** of body content. Use Markdown headings for structure. Adapt sections to what the repo actually has ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â omit any section that would be empty or speculative.

Order sections by **leverage to a fresh agent**, not by tradition. Critical rules and the most-used commands go first; nice-to-know context goes last. A useful default ordering, when in doubt:

1. **Hard rules / Agent-specific instructions** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the "never do X" list and any tripwires (only include if the repo actually has them; otherwise skip and let conventions carry the weight).
2. **Project Structure & Module Organization** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â top-level directory map, where source/tests/assets live, monorepo package list if relevant. Reference deeper docs with `@path/to/doc.md` instead of inlining them.
3. **Build, Test, and Development Commands** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the 3ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“6 commands an agent will actually run, each with a one-line purpose. Prefer `pnpm <script>` (Node.js) or `./mvnw <goal>` / `./gradlew <task>` (Spring Java) over raw tool invocations when the project wraps them.
4. **Coding Style & Naming Conventions** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â indentation, language version, naming patterns (with one short example pattern, not a code block), and the lint/format tools that enforce them.
5. **Testing Guidelines** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â framework, where tests live, naming pattern, how to run a single test, any coverage threshold the repo actually checks.
6. **Commit & Pull Request Guidelines** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the convention observed in `git log` (e.g. Conventional Commits prefixes seen), PR description expectations, required CI checks.
7. **Security & Configuration Tips** _(optional)_ ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â secrets handling, env-file location, validator scripts that fail CI.
8. **Architecture Overview** _(optional, only if not already covered by a `@`-reference)_ ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â 3ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“6 bullets max; otherwise link out.

Open the file with one short paragraph (1ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“2 sentences) naming what the project is and the primary stack ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â enough that an agent landing in the repo for the first time has a frame. No mission statements, team intros, or values.

## Quality guards (run before performing a file write operation)

Each guard is a hard gate. If any fails, revise the draft.

1. **Length.** Body is 200ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“400 words. Under 200 means you skipped specifics; over 400 means you padded or inlined what should be a reference.
2. **No multi-line snippets.** No fenced code blocks longer than a single command line. Replace example components / configs / migrations with `@path/to/file`. Short single-line command examples (`pnpm test`, `git rebase main`) are fine.
3. **Every rule is checkable.** Re-read each sentence and ask: _could a reviewer flag a diff against this?_ If not, rewrite it with a concrete pattern, threshold, or named tool. Strike phrases like "clean code", "best practices", "modern patterns", "be consistent", "handle errors properly", "keep it simple".
4. **No redundant knowledge.** Strike any line you could have written without opening the repo. Framework defaults, language tutorials, and definitions of common terms do not earn a slot. If a rule duplicates `README.md` / `package.json` / lint config, replace it with `@README.md` / `@package.json` / `@.eslintrc.json`.
5. **Critical rules first.** The first third of the file must contain the highest-stakes rules and the most-used commands. If the only "never do X" rule is at the bottom, move it up. If the top is welcome/mission/values, cut it.

## Tone

Professional, instructional, terse. Second person ("Run `npm test` before pushing" or "Run `./mvnw verify` before pushing") or imperative ("Place new handlers in `src/api/<feature>/`" or "Place new controllers in `src/main/java/<package>/controller/`"). No marketing voice, no emojis, no decorative dividers.

## After writing (Exit Gate ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â confirm-or-revise form)

Per the shared contract's exception for no-follow-up skills, present the results box, then ask only a confirm-or-revise question (no unsolicited follow-up suggestions):

**Results box**:

```markdown
## ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ AGENTS.MD COMPLETE ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â <path>

**Scope** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [repo-level / directory-level]
**Words** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [<word count> body words]
**Sections** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [<1-line section order summary>]

**Written** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `<path>`
```

Report to the user:

- the file path written,
- the body word count,
- a one-line summary of the section order chosen.

**Results-acceptance question** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â use `question` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â "Is the document correct?" with options:

- **Accept** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â keep it. Reminder (always print with or without acceptance): _test the file by running a real task with a fresh agent session ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â onboarding docs only prove themselves on the next run._
- **Adjust** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â user specifies changes (trim, reorder, re-shape a section); apply them surgically, re-run the Quality guards, re-present the results box.
- **Discuss** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â justify a specific rule or citation (its file source); then re-ask.
- **Stop here** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â keep the file as written; nothing further at this time.

After the user's response, stop. Do not propose further follow-ups unless the user asks.

## Edge cases

- **No `README.md` and no manifest detected.** Stop and tell the user the repo looks empty or unfamiliar; ask for a one-paragraph project description before drafting.
- **Monorepo with per-package READMEs.** Write a root `AGENTS.md` that lists packages and `@`-references each package's README, rather than duplicating per-package detail. Suggest nested `packages/<name>/AGENTS.md` for any package with rules that materially differ.
- **Existing rich `AGENTS.md` in the repo.** Treat it as authoritative source material. The new `AGENTS.md` should be a tighter distillation that points back to `@AGENTS.md` for depth, not a verbatim copy.
- **Existing `AGENTS.md` was edited by hand after its last commit.** `git diff HEAD -- <path>` will show uncommitted changes. Read those changes first and treat them as KEEP unless they directly contradict a CI-enforced rule ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the user is mid-edit and you must not clobber in-flight work.
- **`LAST_TOUCH` is the initial commit of the repo.** Diff range becomes `LAST_TOUCH..HEAD` with no useful signal. Fall back to inspecting current repo state vs. the file's claims, line by line, without the git-diff shortcut.
- **File exists but is empty or a stub.** Skip the Update path ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â run the Create path and overwrite, since there is no authorial content to preserve.
- **Repo with no commit history (`git log` empty).** Skip the commit-conventions section rather than guessing; note in the PR section that the convention is to be defined.
- **Polyglot repo (e.g. Node.js frontend + Spring Java backend).** Pick the dominant stack by file count for the "Build/Test/Dev" section; mention the secondary stack only if it has its own commands an agent will need. For a typical full-stack repo, cover both `package.json` scripts and Maven/Gradle goals.
