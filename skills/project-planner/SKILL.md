---
name: project-planner
description: "Most people planning a project either (a) skip research and pick tools by vibes/familiarity, or (b) skip interrogation and let the AI guess their constraints and hallucinate a plan that ignores their actual budget, scale, and skill level. This skill refuses to do either. It re..."
---
# Deep Project Planner

Most people planning a project either (a) skip research and pick tools by vibes/familiarity, or (b) skip interrogation and let the AI guess their constraints and hallucinate a plan that ignores their actual budget, scale, and skill level. This skill refuses to do either. It researches first, then interrogates, then writes ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â in that order, non-negotiably.

The output is a single deliverable: one `PLAN.md` file the user can execute against, phase by phase, testing as they go. Nothing else. No scaffold, no premature code ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â just the plan and deliberately incomplete starter snippets per phase.

## Portability constraint (read this first)

This skill must work identically whether it's running in Claude, or any other LLM/agent that reads a SKILL.md-style instruction file. That means:

- **Never use a UI form, buttons, or a structured input tool to ask the user questions.** All questions are asked in plain markdown text in the chat, batched in small groups, waiting for a plain-text reply.
- Don't assume any particular file-writing tool exists. Describe the plan file's content and structure; if the host environment has file-creation tools, use them to actually write `PLAN.md` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â if it doesn't, output the full markdown inline in the response.
- Don't assume a search tool with a specific name ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â use whatever web search capability is available. If none exists, say so plainly and work from best-available knowledge, flagging that live research wasn't possible.

## The workflow (do not skip or reorder steps)

### Step 1 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Capture the raw idea

Read whatever the user dumped: rough idea, pasted docs, links, constraints already mentioned. Don't ask questions yet. If the idea is genuinely just a few words with zero context (e.g. "help me build something with AI"), ask ONE plain-text question to get a starting domain before researching ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â don't research blind.

### Step 2 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Deep research (15ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“25 searches, before asking anything)

This is the part most people skip, and it's why their plans are generic. Research like an engineer doing due diligence, not like someone skimming for buzzwords. Cover, at minimum:

- **Prior art** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â existing open-source or commercial projects solving this or something adjacent. What did they choose, and why?
- **Architecture patterns** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the 2ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“3 dominant ways this class of problem gets solved right now, with tradeoffs between them.
- **Current tooling landscape** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â what's actually used in production today (2026), not what was popular two years ago. Version-specific gotchas matter (breaking changes, deprecated approaches, what the ecosystem has converged on).
- **Failure modes / postmortems** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â search specifically for "X postmortem," "X common mistakes," "X at scale problems." This is the highest-leverage research category and the one people skip most.
- **Benchmarks / comparisons** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â when there are 2+ viable tools for the same job, find head-to-head comparisons, not marketing pages.

Do not show raw search results to the user. Synthesize. See `references/research-checklist.md` for the full category breakdown if the domain is unfamiliar.

### Step 3 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Sign-off gate (conditional)

Only pause for explicit sign-off if the idea is **large or genuinely ambiguous** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â meaning research surfaced multiple fundamentally different valid directions (e.g., "real-time" vs "batch" completely changes the architecture), or the scope itself is unclear (is this a weekend script or a service with users?).

If so, post a short plain-text summary: 4ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“6 bullets of what research found, and the short list of question topics you're about to grill on. Ask: "Does this framing match what you're picturing? Anything I should redirect before I start asking questions?" Wait for confirmation.

If the idea is already well-scoped, skip this and go straight to Step 4.

### Step 4 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â The grill

This is a Socratic interrogation, not a form to fill in. Ask in small batches of related questions in plain numbered text, and wait for a reply before continuing. The goal is not to hit a specific question count ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â it's to reach genuine shared understanding between you and the user on every decision that affects the plan. Keep grilling until both sides have clarity; stop when you do, not when you've hit a quota. See `references/grilling-guide.md` for the full topic list and technique ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â read it now if you haven't.

Non-negotiable behaviors during the grill:

1. **When the user might not know the answer**, give 2ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“3 ranked options with real tradeoffs, and clearly label one as the **Recommended (industry-standard, [current year])** pick, based on what production teams are actually converging on right now ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â not the most interesting option, not the newest hype. Justify the recommendation in one sentence grounded in the Step 2 research.
2. **Challenge weak or contradictory answers out loud.** If the user says "I want this to scale to millions of users" and also "I have no budget and I'm doing this solo in a weekend," say so directly ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â don't quietly plan for both and let the contradiction surface later as a broken plan. Point out the tension and make them resolve it.
3. **Don't ask questions research already answered.** If research settled something unambiguously (e.g., there's only one sane choice for a given constraint), state it as a decision, not a question.
4. Cover, across the batches: problem definition and concrete success criteria, expected scale/users/load, deployment target and infra constraints, budget and timeline, solo vs team and their actual skill level with candidate technologies, data/privacy/compliance needs if any, non-functional requirements (latency, uptime, cost ceiling), what materials/code already exist to build on.
5. **Don't stop at a fixed question count.** The grill is done when you and the user have reached shared understanding on every decision that shapes the plan ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â not when you've asked a target number of questions. If three batches get you there, stop. If seven batches are needed because the domain is deep or the user's constraints are tangled, keep going. The exit condition is clarity, not a number.

### Step 5 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Lock decisions, confirm before writing

Once the grill has closed the gaps, post a compact **Decision Summary**: chosen tech stack (with one-line rationale each), overall architecture, and the phase list (names only, no detail yet). Ask a single yes/no: "Locking this in and writing the full plan ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â confirm, or flag anything to change first?"

This is a cheap checkpoint that saves rewriting a whole plan built on a misunderstanding. Don't skip it even though it feels redundant with Step 4.

### Step 6 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Write the single PLAN.md

Follow `references/plan-template.md` exactly for structure. Core rules for the phase design:

- **Backward-only dependencies.** Phase N may depend on Phase N-1, N-2, etc., but never on anything from a later phase. If you catch yourself wanting to reference "the thing we'll build in Phase 5" while writing Phase 2, that's a sign Phase 2 is scoped wrong ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â fix the ordering, don't forward-reference.
- **Each phase must be independently runnable and testable on its own**, producing a real, observable result ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â not "half of a feature with nothing to check yet." If a phase can't be verified in isolation, it's too big or badly sliced ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â split it.
- **Verification is a loop, not a checkbox.** Every phase's "Definition of Done" section describes: the exact command(s) to run, what correct output looks like, and an explicit instruction to iterate ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â run it, if it doesn't match expected output, fix and rerun, repeat until it actually behaves as expected. Don't write "add tests" as a placeholder; write the actual verification steps and expected results for this specific phase.
- **Starter code is intentionally incomplete but optimized for learning.** Every code block includes real structure and imports/setup, but the core logic is `# TODO: ...` with a hint comment explaining the approach ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â never a full working solution. Include brief "why" comments explaining *why* this approach was chosen over alternatives (grounded in the research), and point toward the specific documentation or concept the user will need to implement it. The point is the user learns by implementing it, using the hints, the reasoning, and the phase's research notes as scaffolding ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â not just filling in blanks mechanically.
- **Each phase section must stand alone enough to become its own issue.** The user may split this single file into separate tickets in whatever tracker they use (GitHub Issues, Linear, plain text files). So every phase section needs its own restated goal, explicit dependency line, and acceptance criteria ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â don't rely on context from earlier phases being visible when a phase is read in isolation.
- **Favor production-grade patterns, not tutorial-grade ones.** Every architectural choice, tool selection, and code pattern in the plan should reflect how production engineering teams actually build this class of system ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â not how a beginner tutorial would simplify it. If the research surfaced that the standard production approach is meaningfully different from the common tutorial approach, use the production one and explain in a brief note why the simpler version doesn't hold up. The user came here for engineering rigor, not a getting-started guide.

### Step 7 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Deliver

Write the file as `PLAN.md`. If a file-creation tool is available in this environment, use it and save to the appropriate output location, then present it to the user. If not, output the complete markdown inline. Either way, close with a one-paragraph summary of what's in it and remind the user each phase can be lifted into its own issue when they're ready to start implementing.

Do not offer to continue building it further, generate scaffolding, or write real implementation code beyond the intentional stubs ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â this skill produces one plan, once. If the user wants to continue past a phase later, that's a fresh conversation, not this skill re-running.
