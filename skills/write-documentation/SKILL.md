---
name: write-documentation
description: "This skill applies when writing or reviewing project documentation - concept docs, architecture overviews, getting-started guides, API references, or pipeline/step docs. It defines how to read, assess, and improve documentation so it is accurate, useful to first-time readers, ..."
---
# Documentation Development

## Purpose

This skill applies when writing or reviewing project documentation - concept docs, architecture overviews, getting-started guides, API references, or pipeline/step docs. It defines how to read, assess, and improve documentation so it is accurate, useful to first-time readers, and consistent with the codebase.

## Prose voice (defer to workflow-human-like-writing)

This skill owns documentation accuracy, information architecture, examples, and page structure. It does not carry its own prose-voice rules. Load `workflow-human-like-writing` alongside it for human-sounding prose and AI-pattern removal (copula avoidance, significance inflation, superficial -ing analyses, vague attributions, hedge stacks, marketing language, diff-anchored narration). The two are meant to run together, and the skills in this repo compose rather than each restating the others.

Where they meet, documentation accuracy wins. These doc-specific concerns override the voice skill:

- **Keep meaningful technical qualifiers.** Anti-hedging must not turn accurate `may`, `can`, `typically`, or conditional language into false certainty. Cut empty hedges and disclaimers; keep qualifiers that encode a runtime condition, optional behaviour, or an unresolved guarantee.
- **Never rewrite syntax-bearing or source-derived spans** when improving prose: code blocks, commands, paths, identifiers, payloads, generated output, table data, URLs, and quotations. Fix the surrounding explanation instead. This extends the real-output rule below to all editing.
- **Neutral technical register is correct here.** Do not inject first person, stance, or personality into reference documentation.

## Core workflow

### 1. Read the doc first, cold

Read the doc before touching the source. Simulate a first-time reader: does the doc give enough conceptual grounding to understand what something is and why it exists? Does it tell you where to look in the code?

### 2. Verify every claim against the source

After reading the doc, read the relevant source files to verify:

- Type names, field names, function names
- Described behaviour (what a function does, what gets dropped, what gets set)
- File paths mentioned in the doc
- Example data (JSON, config snippets, fixtures) - compare against actual files, not memory
- Dependency and output listings - check the actual manifest, directory, or source that writes them

When possible, **run the system** to verify claims that cannot be confirmed by reading alone: CLI flags and their defaults, output file names, build steps, test counts, exact numeric values. Do not trust approximations in examples - replace them with values from actual output.

Never assume a doc is correct. Even well-written docs drift from the code.

**When a claim cannot be verified**, do not document it as fact and do not guess. First separate "cannot run it locally" from "cannot verify at all": source, tests, schemas, generated artifacts, or an authoritative spec may still confirm it. If nothing can, record it in the assessment as unverified and leave it out of the finished doc. Do not ship a permanent "unverified" label in the prose - it ages into a stale dev note; keep an uncertainty note only when the uncertainty is itself part of the documented contract.

An unsourced normative claim ("recommended", "best practice", "more secure", "industry standard") is not a verifiable fact either. Give it a concrete local reason, state the requirement plainly, or cut it.

### 3. Assess before editing

Produce an explicit assessment before making changes:

- What is accurate and should be left alone
- What is wrong or misleading and needs fixing
- What is missing that would help a first-time reader
- What is present but adds noise and should be cut

Do not silently fix things without explaining the reasoning.

### 4. Edit with restraint

Only change what needs changing. Do not rewrite sections that are accurate. Do not add content that doesn't help a first-time reader understand or navigate the codebase.

## Content principles

### "Why it exists" before "how it works"

Every concept page, service description, and architecture section should open with _why_ the thing exists before explaining _how_ it works. A reader who understands the problem being solved will absorb the implementation details faster and evaluate trade-offs correctly.

Do not invent the rationale. Code proves what the system does and how, but rarely why that design was chosen. Draw the "why" from ADRs, code comments, issue or commit history, specifications, or the user. If only the mechanism is observable and no source states the intent, document the mechanism and leave the rationale out rather than guessing. A plausible-sounding invented reason is worse than none, because a reader cannot tell it from a sourced one.

Pattern for concept pages:

```markdown
## Why it exists

<1-2 paragraphs explaining the problem this solves and why the alternative approaches don't work>

## What happens

<implementation details>
```

Pattern for service/component descriptions in architecture pages:

```markdown
### Schedule Builder Lambda

C++ binary using OR-Tools CP-SAT constraint solver to generate schedules.
Invoked synchronously by the API. It's written in C++ because OR-Tools CP-SAT is a native
library, and running it directly is simpler than bridging through Node.js. It runs as a
Lambda because schedule generation is CPU-intensive and variable in duration, so isolating
it keeps API response times predictable.
```

Weave the rationale into the description as natural prose. Do not use standalone "Why X:" question-and-answer lines - they read as FAQ entries rather than documentation. For concept pages with substantial rationale, use a dedicated "Why it exists" section.

### Name sections after concepts, not types

Section headings should reflect the domain concept, not the language-level type name. A reader looking at a section should understand the concept in domain terms first. Type names are secondary details within the section.

When a concept has multiple type-level representations (e.g. prototype + runtime instance, config + entry, interface + implementation), describe the concept once with the types as sub-bullets - not as separate top-level sections.

Good:

```markdown
### Widget

A widget exists at two levels:

- **Prototype** (`WidgetConfig`, `config/widget.ts`) - loaded from config at startup. Describes ...
- **Pipeline entry** (`WidgetEntry`, `core/widget.ts`) - wraps the prototype with runtime metadata ...
```

Bad:

```markdown
### WidgetConfig / WidgetEntry

A widget config... WidgetEntry bundles the config with...
```

### File path references in section headers

For technical reference docs (domain model, module reference, pipeline steps), add the primary source file path to the section header. This lets a reader jump directly to the code without searching.

```markdown
### Order Processor (`src/orders/order-processor.ts`)
```

Only do this for sections where a reader would plausibly want to open the file. Skip it for high-level concept sections where no single file is the right entry point.

### Verify data structure completeness

When documenting a struct, class, or data model, check the actual source definition to ensure all fields are documented. Pay particular attention to:

- Fields present in the code but missing from the doc
- Fields documented but removed from the code
- Fields that exist but are never written or read (dead fields - document why they exist or remove them)

Run `grep` or use codebase tools to trace whether a documented field is actually populated anywhere. A field that is defined but never set is documentation debt.

### Concepts that live in only one module belong in that module

If a type is only created in one module and consumed only by diagnostic output, it is an implementation detail of that module - not a domain concept. Do not promote it to the domain model doc.

Test: if removing the module would make the type unreachable, it belongs in the module, not in a shared concept doc.

### Scope annotations precisely

When a field, flag, or concept only applies in a narrow window (e.g. between two processing phases, or only during initialisation), say so explicitly. Do not let readers infer scope from context.

Good:

```markdown
`pendingFlag` - set during phase A to signal phase B. Cleared immediately after phase B
processes it. Never set in steady-state code.
```

Bad:

```markdown
`pendingFlag` - set during phase A processing.
```

### Keep implementation status out of concept docs

Implementation status sections ("working / not implemented") belong in issue trackers or dedicated status pages, not in concept documentation. They date quickly and distract first-time readers from understanding the design.

Exception: a single `> Note: X is not yet implemented.` callout is acceptable when the concept doc describes something a reader might try to use and find missing.

### Don't repeat what adjacent docs cover

If a concept is described in detail in another doc, reference it with a link rather than duplicating. One source of truth per concept.

When a set of docs has a parent overview that already contains a table of information (e.g. preconditions, output files, processing order), do not duplicate that table in the individual child docs. Link to the overview instead.

### Examples must match actual data

Any JSON example, config snippet, or code sample shown in the docs must match real files in the repository. Verify the example against the actual source - do not trim fields silently (a trimmed example implies those fields don't exist).

**Use real system output for examples.** If the system produces mermaid diagrams, console output, file listings, or numeric values, run it and use the actual output. Approximate or reconstructed examples mislead readers about what the system really does.

Good: a mermaid diagram copied directly from actual tool output after running the system.

Bad: a hand-crafted mermaid diagram with approximate values.

### Reference implementations over code templates in guides

How-to guides ("how to add a feature module", "how to create a package") should point readers to a real implementation in the codebase rather than pasting generic code templates. A template in a doc page drifts from the codebase the moment someone refactors the real code. A reference to the actual file is always current.

Pattern for how-to guides:

1. Name the reference implementation ("copy from `apps/admin/`" or "see `packages/amplitude/`")
2. List what files to create and what external files to update (the checklist)
3. Call out the decisions the reader needs to make (which pattern, which trigger, which config)
4. Include a comparison table of real examples showing how existing implementations vary

Do not paste multi-line code blocks that reconstruct what a file "should look like." If a reader needs the code, they open the reference file. The doc's job is to tell them which file to open and what to change.

### Examples should show the delta

When documenting a transformation (a pipeline step, a merge, a split), the example should show what changed, not just the final state. Before-and-after comparisons are more instructive than a single snapshot:

- Show which items were removed and which were added
- Show which relationships or references were changed
- State explicitly what the total count was before and after

### Choose fixtures that demonstrate what the step uniquely does

When selecting an example for a process or transformation, pick one that exercises the specific behaviour the step is responsible for - not just any input that produces output. An example that triggers the interesting case teaches more:

- For a step that handles error recovery, use an input that actually triggers recovery
- For a step that does batching, use an input that requires multiple batches
- For a step that applies transformations conditionally, use an input that triggers the condition

Think: "what is the most interesting thing this step can do, and which input triggers it?" Use that as the primary example.

### Worked examples should use non-trivial inputs

Use production-realistic inputs for examples, not the simplest possible case. An example that exercises more of the system's behaviour (multiple edge cases, conditional branches, concurrent operations) teaches the reader more and acts as a better regression anchor. Reserve simple examples for isolated concept explanations where complexity would distract.

## Page patterns

### Introduction page structure

The introduction page is the most important page in the doc site - it orients first-time readers (human and LLM) to the entire project. It should contain, in order:

1. **One-paragraph summary** - what the project is and what this repo contains. Write for a developer who needs to work on the codebase, not a customer evaluating the product: state facts (what the app does, what technology the backend uses, what it serves), not a product pitch. Stripping marketing language is the voice skill's job.
2. **What it does** - concrete capabilities, not abstract descriptions. Use a bulleted feature list or a short paragraph per major capability area.
3. **System boundaries** - which repositories exist, what each owns, how they relate. A table works well here.
4. **Service URLs and quick links** - deployed environment URLs (Swagger, API base URL, CDN), dashboard links, and any access credentials needed for testing. Readers should find every URL they need to interact with the system on the intro page, not buried in a deployment guide. Format as a table:

```markdown
## Quick links

| Environment | API                         | Swagger                                          | Webhooks                    |
| ----------- | --------------------------- | ------------------------------------------------ | --------------------------- |
| Dev         | `https://...cloudfront.net` | [Swagger UI](https://...cloudfront.net/api-docs) | -                           |
| Staging     | `https://...cloudfront.net` | [Swagger UI](https://...cloudfront.net/api-docs) | `https://...cloudfront.net` |
```

5. **Domain model at a glance** - a compact structural overview of core entities and their relationships. This is not a database schema - it shows domain concepts and how they relate to each other at a level that helps a reader navigate the codebase.
6. **Where to go next** - 2ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“4 links with one-line descriptions guiding the reader to the most important pages. Every reader path should start here.

### Domain model documentation

A domain model page explains the core entities, their relationships, and lifecycle - not just their database columns. Organize by conceptual layer or functional group, not alphabetically.

For each entity or entity group:

- **What it is** - one sentence defining the concept in domain terms
- **Why it exists** - what problem it solves or what behaviour it enables
- **Lifecycle** - how instances are created, modified, and consumed (which endpoints, which services, which async flows)
- **Key relationships** - cardinality, ownership, cascade behaviour where it matters
- **Source of truth** - where the entity definition lives in code (entity file path)

A domain model page is different from a database schema reference. The database page lists tables and columns for people who need to write queries. The domain model page explains what the entities mean, why they exist, and how they flow through the system for people who need to understand the architecture.

If the project has both a domain model page and a database page, the domain model page links to the database page for column-level details - it does not duplicate them.

### Diagrams: Mermaid vs ASCII vs text trees

Use Mermaid diagrams for flows, sequences, and deployment topologies - anything with edges/connections between components. Mermaid renders consistently across VitePress, GitHub, and LLM tool output.

Use text trees (indented `ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬` / `ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬` notation) for hierarchical structures where the relationships are parent-child ownership, not directional flows. Domain model entity trees and project directory layouts are clearer as text because they are compact, scannable, and don't need visual edge routing.

Use ASCII box diagrams for spatial/physical layouts where tile positions, coordinates, or spatial adjacency matter and Mermaid's graph layout would obscure the geometry.

**Decision shortcut:**

| Content type                                                  | Format                                   |
| ------------------------------------------------------------- | ---------------------------------------- |
| Deployment topology (services, data stores, external APIs)    | Mermaid `flowchart`                      |
| Request/data pipeline (step 1 ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ step 2 ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ step 3)              | Mermaid `flowchart` or `sequenceDiagram` |
| CI/CD workflow (build ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ test ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ deploy)                        | Mermaid `flowchart`                      |
| Entity ownership tree (Account ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Profile ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Session)           | Text tree                                |
| Directory layout                                              | Text tree                                |
| Physical/spatial layout (tile coordinates, machine positions) | ASCII box diagram                        |
| Layer stack (controller ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ service ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ repository)               | ASCII box diagram or text                |

Never use a Mermaid diagram when the text version is more compact and equally clear. A 5-line text tree is always better than a 20-node Mermaid graph that says the same thing.

### Cross-referencing

Every page should link outward to related pages. A reader should never hit a dead end where they need information that exists elsewhere in the docs but isn't linked.

Minimum cross-referencing requirements:

- **Concept pages** link to the pages that exercise the concept (user flows, pipeline steps, getting-started guides)
- **User flow pages** link to the concept pages that explain the underlying model (database, auth, subscriptions)
- **Getting-started pages** link to concept pages for deeper understanding
- **The intro page** links to every top-level entry point

When a concept is mentioned in passing (e.g., "feature limits" in a user flow doc), link to the concept page on first mention. Don't link every occurrence - just the first one per section.

### State and output documentation

When documenting a process, pipeline step, or API endpoint, explicitly state what it produces. Use a table for structured output:

```markdown
## State outputs

| Field            | Type                 | Description                           |
| ---------------- | -------------------- | ------------------------------------- |
| `group.slotPlan` | `optional<SlotPlan>` | Node order, resource slot assignments |
```

For API endpoints, include request and response examples with realistic data. For pipeline steps, show before-and-after state. For background processes, document what database rows, cache keys, or side effects are created.

### Avoid checklists in docs

Do not include task checklists (checkbox lists like `- [ ] verify X works`) in documentation pages. Checklists are ephemeral operational artifacts - they belong in runbooks, JIRA tickets, or CI scripts, not in persistent documentation. A checklist in a doc page either goes stale (items change but nobody updates the list) or creates false confidence (reader checks boxes without actually verifying).

If a process has verification steps, describe them as prose: "After deployment, verify the API's health route responds with 204 and the Swagger UI loads." This is more durable than a checkbox list and doesn't invite half-completed state. Take the real paths from the app's health controller and bootstrap, not from this example.

## Specific conventions

### Avoid step/phase numbers as primary identifiers in individual docs

Do not use internal sequencing identifiers (step numbers, phase numbers) as the primary way to refer to concepts within a step's own documentation. Prefer descriptive names.

Rationale: step numbers are implementation order, not domain concepts. They change when things are added or reordered. They also add no information inside the doc for the step they describe.

Acceptable: the overview table of all steps, where the number is the point.

Not acceptable (within an individual step doc):

- "Step 3 requires graph, input, resources, recipes" ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ "This step requires graph, input, resources, recipes"
- "After Step 2 completes..." ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ "After logic optimization completes..."
- "Steps 3ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“7 treat macro nodes identically" ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ "Downstream steps treat macro nodes identically"

Exception: step numbers are fine in cross-references where the number uniquely identifies which step is meant and the name alone would be ambiguous.

### Fix code issues discovered during the doc pass

Reading code to write documentation often reveals bugs or stale code that the doc would otherwise perpetuate:

- A comment describing one algorithm when the implementation uses a different one
- A config field defined but never read
- A dead code block that explains (incorrectly) what some other code does
- A fallback that silently produces wrong results

Fix these in the same commit as the doc change. A doc that accurately describes incorrect code is still wrong - the code is the ground truth.

### When removing a concept, audit all docs for references

When a type, step, or concept is removed, search all docs for every reference to it. References appear in:

- The step's own doc (delete it)
- The overview/parent doc (update the table row)
- Concept docs that reference it (update or remove the section)
- Getting-started docs that mention its output files
- The sidebar/nav config

Use grep across the docs directory for the type name, file name, and any terminology unique to the removed concept. Missing one reference leaves a broken link or a confusing orphan.

### Keep internal dev notes out of public docs

Notes written for developers actively working on a known bug or incomplete feature do not belong in public documentation. They confuse first-time readers who have no context for the note.

Examples of things to remove: "(known issue)", "(sorting bug)", "(alignment problem)", "(TODO: fix this)"

### Dash style

No em dashes (the U+2014 character) or double-hyphen substitutes in documentation prose. They are the most common AI writing tell and this repo bans them. Use commas, parentheses, a colon, or separate sentences for parenthetical clauses. Use a plain hyphen (`-`) for Markdown bullets and list-item separators, and keep hyphens in compound words. The prose-voice skill owns the rest.

### Output and file listings

When documenting output files, generated artifacts, or directory contents, verify the listing against the actual files and the source code that produces them. Do not document files that don't exist; do not omit files that do.

### Dependency and fixture tables

When listing dependencies, fixtures, or configuration entries, check the actual manifest or directory. Document everything present - don't silently omit entries.

### Explain the _why_ behind ignored or unused fields

When a field, flag, or feature is explicitly ignored or not yet implemented, say why - not just that it is ignored. This prevents readers from thinking the omission is a mistake and prevents future contributors from re-implementing something intentionally excluded.

Good:

```markdown
`auditLog`, `retentionPolicy` - present in the upstream API response but not consumed.
These relate to compliance tracking which this service does not handle.
```

Bad:

```markdown
> Note: We ignore `auditLog` and `retentionPolicy` for now.
```

### Precondition sections belong in the overview

If a pipeline or system has an overview doc with a consolidated table of preconditions, do not repeat those preconditions in each individual step doc. A "Preconditions" section in every step doc duplicates the overview table and goes stale independently.

## Anti-patterns

- Editing the doc without reading the source to verify claims
- Trusting approximate or reconstructed values when the system can be run to get exact values
- Documenting an unverifiable claim as fact instead of flagging it and leaving it out
- Inventing design rationale the code does not state - document the mechanism when no source gives the "why"
- Asserting a normative claim ("best practice", "more secure") with no source or concrete local reason
- Keeping internal dev notes in public docs
- Listing ignored/unused fields without explaining _why_ they are ignored
- Splitting one concept across multiple top-level sections because it has multiple type representations
- Using internal sequencing identifiers (step numbers) as primary identifiers within individual docs
- Showing trimmed examples that omit fields present in the real data
- Using hand-crafted example values instead of actual system output
- Documenting implementation status inline in concept docs (use a single callout note instead)
- Repeating content already covered in a linked doc instead of linking
- Duplicating overview-level tables (preconditions, output files) in individual child docs
- Making claims about coupling or dependencies without verifying the actual imports
- Adding `---` horizontal rules between sections - use headings alone for structure
- Using em dashes in documentation prose - they are a top AI tell and banned in this repo
- Promoting a type to the domain model when it is only created in one step and consumed only by diagnostic output
- Documenting a config field or struct field without checking whether it is actually read anywhere in the implementation
- Leaving stale code comments that contradict the implementation when they are discovered during a doc pass - fix both
- Changing behavior without updating, in the same commit, the docs, READMEs and file names that describe it - prose that contradicts the code is a bug readers trust over the code (code comments follow `develop-code-quality`)
- Deleting a concept without grepping all docs for references to it
- Choosing an example input that doesn't exercise the component's primary or most interesting behaviour
- Starting a concept page with "how it works" without first explaining "why it exists"
- Jumping straight to implementation ("how") before explaining purpose ("what" and "why")
- Burying service URLs and access information deep in deployment or setup pages instead of surfacing them on the intro page
- Using Mermaid for hierarchical structures (entity trees, directory layouts) where a text tree is more compact
- Using ASCII text for flow/topology diagrams where Mermaid renders better and is easier to maintain
- Writing a domain model page as a flat table list without explaining entity relationships, lifecycle, or why each entity exists
- Dead-end pages - concept pages that don't link to related user flows, and user flow pages that don't link back to concept pages
- Task checklists (`- [ ]`) in persistent documentation - these belong in runbooks or tickets, not in docs that should stay accurate over time
- An intro page that doesn't include deployed environment URLs, Swagger links, or repository links
- Using "Why X:" question-and-answer format for rationale in service descriptions - weave the reasoning into the paragraph as natural prose instead
- Pasting generic code templates in how-to guides when the codebase has a real reference implementation to point to - templates drift, reference files stay current
- Writing intro page summaries in marketing language ("personalized", "cutting-edge", "seamless") - the audience is a developer, not a customer
