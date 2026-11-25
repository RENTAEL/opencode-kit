---
name: learn-with-docs
description: "Turn one solved problem into one learning under `docs/solutions/`, checked against the current tree and findable by the next agent."
---
# Learn With Docs

Turn one solved problem into one learning under `docs/solutions/`, checked against the current tree and findable by the next agent.

## The bar

Write a learning only when it holds reasoning a future engineer could not recover from the final code, tests, types, comments, or existing docs ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â and losing it would plausibly cause the mistake to recur, real risk, or a substantial re-investigation. Test it with a counterfactual: if this doc vanished, would someone reading the final implementation still likely repeat the mistake or redo the digging? Effort spent and diff size do not count.

The problem must also be solved and verified. If either test fails, write nothing and say why. Judge from the session; do not ask. An explicit invocation asks for the judgment now ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â it does not lower the bar.

An existing learning that became wrong or incomplete qualifies: update it instead of adding a duplicate.

**One learning per run.** Overlap detection and claim checks assume a single problem; batching several into one run leaks drafting labels ("Learning 3") into the docs. For several learnings, run the skill several times.

## Paths

| Path | Holds |
| --- | --- |
| `docs/solutions/<category>/` | One learning per file, kebab-case slug, no date in name |
| `CONCEPTS.md` (repo root) | Project glossary ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â see `references/concepts-vocabulary.md` |
| `AGENTS.md` / `CLAUDE.md` | Edited only to make the store discoverable, with consent |

These are the only files this skill writes. Edits to other learnings belong to `learn-with-docs-refresh`.

## Modes

- **Interactive** (default) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â asks only at the discoverability edit and when several stale docs need a refresh decision.
- **Non-interactive** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â triggered by `mode:non-interactive` or an unmistakable "run unattended / without questions". Asks nothing, never edits instruction files, and ends on `Documentation complete` or `Documentation skipped ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â <reason>` so a calling workflow can parse it.
- **Depth** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Full by default. Use Lightweight when context is nearly exhausted, or when `depth:lightweight` is passed. Strip `mode:` and `depth:` tokens before reading the rest as context.

## Full workflow

### 1. Classify and draft

Do this in the main context ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â only it holds the conversation.

- Read `references/schema.md`. Sample the frontmatter and directory names already under `docs/solutions/`; the corpus vocabulary wins over the defaults.
- Pick the track (bug or knowledge), category directory, `component`, `root_cause`, and a slug filename.
- Draft the body with the section order from `assets/resolution-template.md`. The failed attempts and the reasoning behind the fix are the point ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â a later reader cannot get them from the diff.
- Ground claims as you write. Read the defining source before stating how code behaves and cite `file:line`; soften anything you cannot verify ("per this session's conclusionÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦"). Cite PR numbers, not commit SHAs (rebases rewrite them). Phrase unmerged fixes as pending.
- If `CONCEPTS.md` exists, use its terms.
- If the host injects persistent memory notes, use relevant ones as supporting evidence only, and tag any that reach the doc "(from agent memory)".

### 2. Find related docs (subagent, in parallel with step 1)

Dispatch one read-only subagent so its corpus reading stays out of your context. Give it a few lines on the problem (what broke, module and file names, error text, the fix) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â it cannot see this conversation. Ask it to:

- Search `docs/solutions/` for related learnings: grep frontmatter (`title`, `tags`, `module`, `component`) first, read only strong candidates in full.
- Search related GitHub issues with `gh issue list --search "<keywords>" --state all --limit 5` when `gh` is available.
- Score overlap with the new learning across five dimensions ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â problem, root cause, solution, referenced files, prevention: **high** 4ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“5, **moderate** 2ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“3, **low** 0ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“1.
- Flag related learnings the new one makes stale, contradicted, or too broad.
- Return links, overlap score with matched dimensions, and stale candidates.

### 3. Write

| Overlap | Action |
| --- | --- |
| **High** | Update the existing doc in place: keep its path, title, and frontmatter shape; add `last_updated: YYYY-MM-DD`. |
| **Moderate** | Write a new doc; flag the pair for the refresh check (step 6). |
| **Low/none** | Write a new doc. |

Two docs on the same problem drift apart, so fold fresher context into the existing one rather than adding a second.

Write to `docs/solutions/<category>/<slug>.md`, creating the directory if needed.

### 4. Vocabulary

Read `references/concepts-vocabulary.md` first ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â its bar is not obvious, and qualifying terms often sit in the conversation, not the doc. Then scan both.

- **`CONCEPTS.md` exists** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â add, refine, fold, or scrub entries. Retiring and deleting belong to the refresh skill.
- **Missing, and a term qualifies** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â create it with the preamble, seeding the core domain nouns of this learning's area only. Hold borderline terms back.
- **Every run** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â check the coherence neighborhood of the area you touched: scrub implementation details, fix entries this learning shows have drifted, fold redundant ones. Flag anything that needs investigation you did not do.

Verify any behavior an entry asserts against source before writing it. Apply edits without asking.

### 5. Verify

Read `references/verify-claims.md` and check the written doc and any glossary entries you touched against the code ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â reading the source, and `git blame` / `git log` / commit messages where the code alone does not explain it. Fix or soften what does not hold.

### 6. Refresh check

Decide whether the new learning makes older docs stale. Recommend or run `learn-with-docs-refresh` with the narrowest scope (a file, module, or category) only when: a related doc now contradicts the new fix, the new fix supersedes one, a rename/migration/upgrade likely broke references, or overlap was moderate. Skip it when nothing related was found or related docs still agree.

- One clear stale candidate ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ invoke the refresh skill with that scope (interactive) or recommend it.
- Several candidates in one area ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ ask whether to refresh that area.
- Non-interactive or Lightweight ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ recommend only, in the report.

### 7. Discoverability

Read `references/discoverability.md` and follow it. It checks that `AGENTS.md` / `CLAUDE.md` point agents at `docs/solutions/` (and `CONCEPTS.md`), and proposes the smallest addition when they do not.

### 8. Report

End with the report; do not offer a follow-up menu.

```text
ÃƒÂ¢Ã…â€œÃ¢â‚¬Å“ Documentation complete            (or: ÃƒÂ¢Ã…â€œÃ¢â‚¬Å“ Documentation updated ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â high overlap with <path>)

File: docs/solutions/<category>/<slug>.md  (created | updated)
Track: bug | knowledge ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â category <category>, component <value> (corpus | default)
Related: <N docs linked, overlap low | moderate ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â <path> | high>
Verified: <N claims checked; N fixed, N softened, N unverified>
CONCEPTS.md: <scanned, no qualifying terms | created with N entries | updated ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â N added, N refined, N folded, N scrubbed>
Instruction file: <no gap | edited <file> | gap ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â proposed text below>
Refresh: <none | learn-with-docs-refresh <scope>>
```

"Scanned, no qualifying terms" is correct only when `CONCEPTS.md` is byte-for-byte unchanged. Non-interactive runs end with a last line of `Documentation complete`, or emit `ÃƒÂ¢Ã…â€œÃ¢â‚¬â€ Documentation skipped` with a reason and end with `Documentation skipped`.

## Lightweight workflow

One pass in the main context, no subagents:

1. Classify and draft as in step 1, shorter: Problem, Solution with key snippets, one Prevention tip (bug track); Context, Guidance, one When to Apply note (knowledge track).
2. Skip related-doc search. If the exact target path already exists and covers the same problem, update it; otherwise pick a distinct slug.
3. Write as in step 3.
4. Vocabulary is update-only: edit an existing `CONCEPTS.md`; never create one.
5. Verify claims as in step 5, limited to cited paths and the behavior claims at the heart of the fix.
6. Discoverability: assess and report only, never edit.
7. Report with `(lightweight)` in the header and a note that a Full run adds overlap detection and a full claim check.
