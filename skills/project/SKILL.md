---
name: project
description: "Unified entry point for project operations. Each subcommand delegates to an existing command, skill, or agent, with shared behavior for argument parsing and state awareness."
---
# Project

Unified entry point for project operations. Each subcommand delegates to an existing command, skill, or agent, with shared behavior for argument parsing and state awareness.

## When to Use

- Creating tests for an agent
- Committing, staging, or managing git operations
- Creating or managing pull requests
- Reviewing code quality, security, and architecture
- Analyzing or optimizing code
- Refactoring, simplifying, and modernizing code
- Cleaning up AI-generated code slop
- Generating icon assets
- Organizing files and finding duplicates
- Generating changelogs
- Updating README files
- Tagging releases
- Auditing project health

## No-Argument Behavior

When invoked without arguments, list the subcommands as plain text and ask the user to choose. Do NOT call `hubMenu` or any other tool ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â just output the list directly. Available operations: create-tests, code-review, commit, git-stage-thread, pr, gh, optimize, refactor, simplify, simplify-code, cleanup, modernize, icon, organize, changelog, converge, scan, sandbox, retrospect, purge, release, review, audit, archive, git-cleanup, workspace, readme, extract-standards.

## With-Argument Behavior

Directly invoke the matching subcommand. Print the reminder, then delegate.

## Subcommand Routing

| Subcommand | Skill/Delegate | What It Does |
|------------|----------------|--------------|
| `create-tests` | `create-tests` command | Generate 8-type test suite for an OpenCode agent |
| `code-review` | `@code-reviewer` agent | Delegated review ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â pass instructions directly to the reviewer |
| `commit` | `conventional-commit` skill | Create a conventional commit with emoji prefixes |
| `git-stage-thread` | `git-stage-thread` command | Stage all files modified in the current conversation thread |
| `pr` | `github-ops` skill | Create, view, merge, manage GitHub pull requests |
| `gh` | `github-ops` skill | Full GitHub CLI operations ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â repos, issues, releases, workflows, search |
| `optimize` | inline | Analyze code for performance, security, and maintainability bottlenecks |
| `refactor` | `@refactoring` agent | Behavior-preserving restructuring ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â extract, split, reduce coupling |
| `simplify` | `@code-simplifier` agent | Reduce complexity ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â flatten nesting, clarify naming, remove abstractions |
| `simplify-code` | `code-simplification` skill | Process-driven clarity pass ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â preserve behavior, follow conventions, verify checklist |
| `cleanup` | `ai-slop-cleaner` skill | Regression-safe deletion-first cleanup of AI-generated code artifacts |
| `modernize` | `@refactoring` agent | Update code patterns to modern language/framework conventions |
| `icon` | `icon-generator` skill | Generate web/PWA/UE icon assets from a single source image |
| `organize` | `file-organizer` skill | Find duplicates, suggest structures, automate file cleanup |
| `changelog` | `changelog-generator` skill | Generate user-facing changelogs from git commits |
| `converge` | inline | Merge divergent branches and resolve conflicts |
| `scan` | inline | Scan for security vulnerabilities, secrets, and unsafe patterns |
| `sandbox` | inline | Run code in an isolated sandbox environment |
| `retrospect` | inline | Project retrospective ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â what went well, what didn't, action items |
| `purge` | inline | Remove unused dependencies, dead code, and stale artifacts |
| `release` | inline | Tag and release ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â bump version, generate changelog, create GitHub release |
| `review` | inline | Full code review round ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â analyze changes, scan security, check complexity |
| `audit` | inline | Comprehensive project health check ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â deps, security, quality, coverage, size |
| `archive` | inline | Move stale branches, old artifacts, unused config to timestamped archive |
| `git-cleanup` | inline | Repair CHANGELOG entries with orphaned commit hash references |
| `workspace` | inline | Manage `.opencode` across projects ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â list, sync, init, health check |
| `readme` | `readme-updater` skill | Update README to reflect current codebase state |
| `extract-standards` | `code-standards-extractor` skill | Extract coding standards from existing files ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â infer style guide from codebase syntax |

### Subcommand Behavior

Each subcommand follows the hub pattern:

1. **Print a terse reminder** (1-2 lines, see Terse Reminders table below)
2. **Parse arguments** ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â accept target paths, flags, or operation-specific args
3. **Delegate** to the appropriate skill, agent, or inline execution (see routing table above)
4. **Report results inline** with summary of what was done

### Terse Reminders

| Subcommand | Reminder on Invoke |
|------------|-------------------|
| `create-tests` | Tests: Generate an 8-type test suite for an agent. |
| `commit` | Commit: Analyze staged changes and create a conventional commit with emoji prefixes. |
| `git-stage-thread` | Stage: I'll identify all files modified in our conversation and stage them. |
| `review` | Review: Full code review round ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â analyze changes, scan security, check complexity. |
| `pr` | PR: Create, view, merge pull requests via GitHub CLI. |
| `gh` | GH: Full GitHub operations via the gh CLI ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â repos, issues, actions, releases, search. |
| `optimize` | Optimize: Analyze code for bottlenecks, vulnerabilities, and maintainability issues. |
| `refactor` | Refactor: Plan and implement behavior-preserving restructuring. |
| `simplify` | Simplify: Reduce complexity, flatten nesting, clarify naming, remove abstractions. |
| `simplify-code` | Simplify-code: Process-driven clarity pass ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â preserve behavior, follow conventions. |
| `cleanup` | Cleanup: Remove AI-generated slop ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â dead code, unused exports, redundant comments. |
| `modernize` | Modernize: Update code patterns to modern language/framework conventions. |
| `icon` | Icon: Generate web/PWA/UE icon assets from a source image. |
| `organize` | Organize: Scan directories, find duplicates, suggest structures, clean up files. |
| `changelog` | Changelog: Generate a user-facing changelog from git commits. |
| `release` | Release: Tag, bump version, generate changelog, create GitHub release in one flow. |
| `audit` | Audit: Comprehensive health check ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â deps, security, quality, coverage, bundle size. |
| `readme` | Readme: Scan codebase and update README with current state. |
| `extract-standards` | Extract-standards: Infer coding standards from existing file(s) syntax. |
| `git-cleanup` | Git-cleanup: Repair CHANGELOG entries with orphaned commit hash references. |

---

## Shared Lifecycle

`/project` is stateless ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â no checkpoints or resume. Each subcommand is a one-shot operation:

### Step 1: Parse Arguments

Accept target paths, flags, or operation-specific arguments. If no arguments provided, ask the user what to operate on (unless the subcommand is self-targeting like `audit` or `retrospect`).

### Step 2: Print Reminder

Show the static 1-2 line description for the selected subcommand (see Terse Reminders table above).

### Step 3: Execute

Delegate to the appropriate skill, agent, or inline execution per the Subcommand Routing table.

### Step 4: Report

Report results inline with a summary of what was done. For destructive operations (purge, archive, git-cleanup), confirm before applying changes.

## Related

- `/ideation` ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Plan before you build
- `/orchestrate` ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Execute with a pattern
- `/harvest-context` ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Capture and manage project knowledge
- `/init-project` ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â Set up or refresh project configuration