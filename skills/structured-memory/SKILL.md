---
name: structured-memory
description: "Up to three memory roles are available in this environment ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â local file-based memory, a long-term memory service, and a task-tracking store ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â each with its own scope and reliability profile (see `references/memory-backends.md` for the full mec..."
---
# Structured Memory

Up to three memory roles are available in this environment ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â local file-based memory, a long-term memory service, and a task-tracking store ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â each with its own scope and reliability profile (see `references/memory-backends.md` for the full mechanics of each). This skill is the decision layer on top of them: what's actually worth persisting, which type it is, which store it belongs in, how to write it so it survives intact, and when to prune or reinforce what's already there.

The recommendations below are grounded in current research on LLM agent memory ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â see `references/research-summary.md` for the full citation trail. That file exists so this one doesn't have to carry citations inline; read it when you want the "why" behind a rule here, or when deciding how much weight to give a judgment call that isn't clear-cut.

## The core loop

For any candidate memory, work through these in order. Don't skip straight to "where do I write this" ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â most low-value memories get caught at step 1.

### 1. Is this actually worth persisting?

Apply the test that already governs project-scoped memory, and hold cross-store additions to the same bar: **if the user starts a genuinely different, unrelated project next month, would this fact still save them time?** If the value is purely in retracing one ticket's or one incident's specific history, it belongs in project-scoped memory at most, not a durable store.

Never persist what's cheaply re-derivable from the current state of the world: code patterns, architecture, file:line facts (re-read the code), git history or blame (`git log`), debugging fix recipes (the fix is in the diff, the why is in the commit message), or anything already written down in a project's standing instructions doc. A memory that just restates the code is a liability, not an asset ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â it will silently go stale the moment the code changes, and nothing will tell you when that happens.

Selectivity on writes is the single highest-leverage decision in the research on this topic: agents that write everything measurably perform worse than ones that write only what earns it, because irrelevant accumulated records dilute retrieval and can degrade behavior even with no adversary involved. Err toward not writing when a candidate memory feels marginal.

### 2. What type is it?

Research converges on a functional taxonomy ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â working, episodic, semantic, procedural ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â that doesn't use the same names as this environment's actual stores, but maps onto them cleanly enough to reason with:

| Research category | What it means | Where it lives here |
|---|---|---|
| Semantic | Abstracted, de-contextualized facts (preferences, tool behaviors, standing knowledge) | Project notes' user/reference-style entries; a durable store's semantic-fact entries |
| Episodic | Concrete individual experiences (a specific incident, a specific investigation) | Project notes' project-scoped entries; a durable store's episodic entries |
| Procedural | Reusable rules, corrections, and "how to act" instructions | Project notes' feedback-style entries; a durable store's procedural entries |
| Working | Current task/session state, not meant to outlive the task | Task-tracking state ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â not really durable memory at all |

Coding agents lean procedural more than other agent domains do ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â verified patterns, corrections to approach, and architecture decisions tend to be the highest-value thing worth keeping. Weight your judgment accordingly: a correction about *how to work* is usually worth more than a fact about *what currently exists*.

Some durable stores also auto-classify content into extra categories beyond this four-way split, assigned automatically by content rather than chosen by you. Don't fight a store's own classifier by trying to force a memory into one of those categories ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â write the fact plainly and let the store sort it.

### 3. Where does it belong?

Route by scope, not convenience ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â see the full decision table in `references/memory-backends.md`:

- **Project-scoped notes** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â anything tied to one specific project's ongoing work, incidents, or decisions. This is the default for episodic content; it decays in relevance as the project evolves, which is fine and expected.
- **Durable cross-project memory** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â facts that hold regardless of which project surfaces them: tool behavior quirks, environment gotchas, methodology lessons validated across more than one occasion. This includes internal-company-tool facts if the user's work spans multiple projects that share that tool's blast radius ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â "cross-project" doesn't have to mean "universally applicable to any codebase on Earth," it means "applicable beyond the one project that surfaced it."
- **Task-tracking state** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â live task/subtask state for whatever you're currently doing, and the first place to check before fetching any external documentation (then durable memory, then a live fetch, only if nothing recent is already recorded).

When a fact could plausibly go in more than one place, prefer the narrowest scope that's still true. A fact that's actually project-specific but gets written to durable memory "just in case" pollutes a store meant to stay durable and cross-cutting.

## Writing memory so it survives

### One atomic proposition per write, verified immediately

This is the sharpest, most costly-to-forget rule in this skill. Some memory backends have a confirmed, empirically-verified defect: content spanning more than one clause or sentence gets silently corrupted ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â dropped clauses, spliced fragments, or emptied outright ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â with no relationship to simple length limits (one observed backend preserved a 130-character run-on sentence intact while losing half of a 90-character two-sentence input). The write call reports success either way, so there is no error to catch. Treat this as a standing risk with any backend you haven't personally verified handles compound writes correctly ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â not a defect specific to one named tool.

The only pattern that reliably survives: decompose the memory into one short, single-fact sentence per write, and immediately read it back to confirm the content matches byte-for-byte what you sent. If it's corrupted, discard it and retry as a smaller atomic claim rather than re-sending the same multi-clause content ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â retrying identical long content tends to fail the same way. Never write a compound memory to any backend and assume it landed correctly just because the call didn't error.

This isn't just a defensive habit ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â it's independently the direction the research points anyway: structured, atomic notes with explicit links between them outperform raw free-text blobs, and updating by small delta beats periodic full rewrites (full rewrites drift toward generic content over time and lose the specific detail that made the memory worth keeping in the first place).

### Carry provenance, and supersede rather than silently erase

Every memory should make clear *why* it exists ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â for project-scoped feedback/project entries this is the existing **Why:** / **How to apply:** structure; for backends that only accept one flat fact per write, a plain factual sentence with tags is usually enough given the one-proposition-per-write constraint. Link related memories (`[[name]]` locally) rather than duplicating context across files.

When a memory turns out to be wrong or stale, the strongest single finding across independent industry systems (arrived at from opposite architectural choices) is: don't just make it vanish. For project-scoped notes, edit the file in place and note what changed and why, rather than deleting outright ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â that keeps a record of what was previously believed and corrected, which matters if anything else still references the old version. For a durable store with no built-in versioning to lean on, the practical equivalent is: don't delete an outdated entry until its replacement is written *and* verified ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â never leave a window where the fact is simply gone from the store.

## Verify before you persist

This is the one rule in this skill that exists because of direct experience, not just literature: **a claim sourced from a subagent's research, a web search, or another session's summary is not yet a fact just because it reads confidently.** Before writing anything as a reference-type memory, or as a durable-store entry citing a specific source, number, or quote, check it against the primary source if the stakes of being wrong are more than trivial ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â especially for anything with suspiciously precise statistics or a verbatim-sounding quote attributed to a specific document. Hallucinated citations are a named failure mode in the literature on this exact topic; don't let one become a permanent memory that a future session cites as settled fact.

This doesn't mean verifying everything ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â a user's direct statement about their own preferences doesn't need a citation check. It means treating externally-sourced claims with the same skepticism before persisting them that you'd want a future session to apply when reading them back.

## Consolidate, reinforce, and let go

Memory quality degrades through accumulation, not just through individual bad entries ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â this is worth treating as a periodic maintenance task, not a one-time setup:

- **Promote durable lessons.** When a project-scoped memory turns out to generalize (the same tool quirk bites twice, in two different projects), promote the generalized version to durable memory rather than letting the same lesson exist only where it happened to first surface.
- **Consolidate repeated episodic facts into one semantic fact.** Three separate incidents where the user corrected the same kind of thing are worth one clear procedural/feedback memory, not three overlapping episodic ones.
- **Prune what's stale**, especially project-scoped memories referencing project state that has since changed or dangling `[[links]]` to memories that were never written and never will be.
- **Reinforce durable-memory entries that keep proving useful** with the store's reinforcement or salience-boost mechanism, if it has one ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â not all backends support this ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â rather than leaving salience to passive decay. Decay without reinforcement treats every memory as equally disposable over time, which isn't true of the ones that keep mattering.
- **Resolve dangling links** you find during an audit rather than leaving them as permanent gaps ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â a `[[link]]` to something that doesn't exist is a flag that a piece of context was never captured, not a cosmetic issue. `main.py check-links` (see below) automates finding these.

## Retrieve before you assume

Check what's already known before starting new work or re-fetching something live: task-tracking state first, then durable memory, then a live fetch only if nothing recent is already recorded ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â this ordering exists because both memory stores are cheaper and faster than a live fetch. At the start of any memory-heavy task, actually look at what's there rather than assuming the store is empty or that you already know its contents from earlier in the conversation.

## Security and hygiene boundaries

Judging what's worth remembering is this skill's job; enforcing safety limits is not, and shouldn't be improvised here. Never write secrets, credentials, or PII into any memory store, regardless of type ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â that's a hard line, not a judgment call, and no amount of "but it seemed relevant" changes that. Path safety, size limits, and sensitive-data stripping are the harness's and the tool's job to enforce; this skill's contribution is simply never attempting to write something that shouldn't be persisted in the first place.

## Further reading

- `references/research-summary.md` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the full academic and industry citation trail behind every claim above, corrected against primary sources.
- `references/memory-backends.md` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â exact mechanics, formats, and constraints for each memory-backend role, plus the full information-to-store decision table.
- `main.py check-links --memory-dir <path>` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â read-only scan for dangling `[[links]]`, malformed frontmatter identity, and orphaned files across a directory of markdown memory notes. Run this during any audit/cleanup pass instead of relying on manual read-through to catch broken links.
