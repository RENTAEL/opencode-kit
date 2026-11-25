---
name: simple-english-opencode
description: "Rewrite the given text into simple English."
---
# Simple English for OpenCode

Rewrite the given text into simple English.

Rule: every word must earn its place. If you can cut it without losing meaning, cut it.

Write for a tired reader who will read each sentence once. Prefer short sentences, plain words, active voice, and one meaning per word. AI padding dies as a side effect.

Use this for marketing copy, technical docs, blog posts, specs, and AI-generated text. It is not a full ASD-STE100 compliance tool. It takes the useful parts of Simplified Technical English (short sentences, active voice, fixed vocabulary, self-check) and applies them to broader prose, including marketing and blogs.

## Your task

1. Classify each passage as procedural (instructions) or descriptive (explanations). Do not mix the two in one paragraph.
2. Pick vocabulary before drafting: one verb for check/verify/confirm/validate; one noun for config/settings/options. Keep those choices for the whole piece.
3. Rewrite under the rules below. Do not explain while drafting. Rewrite first.
4. Run the self-check. Mandatory.
5. Deliver in the fixed output format. No other sections unless the user asked for Check mode.

Never invent facts, metrics, product claims, or citations the source did not contain. If a claim is empty ("enterprise-grade", "blazingly fast"), cut it or replace it with a concrete fact already in the source. If none exists, cut it.

## Modes

| Mode              | Trigger                                   | Output                                                          |
| ----------------- | ----------------------------------------- | --------------------------------------------------------------- |
| Rewrite (default) | rewrite, simplify, de-slop, plain English | Fixed format below                                              |
| Check             | check, audit, review only, just findings  | Findings table only. No full rewrite.                           |
| Shorter           | make it shorter, cut hard                 | Same as Rewrite, with hard cuts (aim for about 30% fewer words) |

Genre hints (optional): `marketing`, `docs`, `blog`, `spec`. Apply the matching notes in `references/genres.md`. Default genre = match the source.

## Rules

### Sentences

| Passage type | Limit    | Shape                                                                                                   |
| ------------ | -------- | ------------------------------------------------------------------------------------------------------- |
| Procedural   | 20 words | Imperative. One instruction per sentence. Condition before command: "If the build fails, read the log." |
| Descriptive  | 25 words | Simple present / past / future. One topic per paragraph. Max six sentences per paragraph.               |

- No semicolons. Split into two sentences.
- No contractions in technical docs/specs (`you'll` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `you will`). Marketing and blogs may keep contractions if they fit the voice.
- Keep articles and "that" when they prevent misreading: "Make sure that the file exists."
- Prefer two short sentences over one clever long one.

### Verbs and voice

- Active voice. Passive is allowed only when the actor is unknown, or the genre is a formal spec and the object matters more than the actor.
- Prefer simple tenses. Avoid present perfect padding ("has been completed" ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ "completed" / "is complete").
- Do not hang meaning on `-ing` clauses after a comma (", making it easy" ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ new sentence with a real subject).
- Approved modals for requirements and facts: can, will, must. Treat should / would / may / might / could as soft AI hedges. Replace with must/can, state the fact, or delete.
- Prefer verbs over nouns: "decide", not "make a decision"; "compress the file", not "perform compression of the file".

### Words

- One word, one meaning, for the whole document. No synonym rotation.
- Noun chains of three words or fewer. Break longer chains with prepositions: "the timeout value for the connection pool".
- Delete words that carry no fact. Replace AI/corporate filler using `references/substitutions.md`.
- Prefer concrete nouns and strong verbs over adjectives and adverbs. "Ran quickly" ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ "sprinted". "Very large" ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ give the number or cut "very".
- American English spelling unless the source is clearly British and the user wants to keep it.

### Untouchables

Leave these exact (each counts as one word toward sentence limits when backticked or quoted):

- Code, identifiers, CLI commands, flags, file paths
- Quoted errors and log lines
- Product names, API routes, config keys
- Numbers with units already in the source

### AI-slop kills (always)

Delete or rewrite every instance of:

| Pattern                                                                               | Fix                                      |
| ------------------------------------------------------------------------------------- | ---------------------------------------- |
| Enthusiasm padding ("Great question!", "Absolutely!")                                 | Delete                                   |
| Filler transitions ("Let's dive in", "In this article we will")                       | Delete or state the point                |
| Fake structure ("In conclusionÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦") that restates                                       | Delete                                   |
| Empty intensifiers (truly, incredibly, remarkably, seamlessly, robust, comprehensive) | Delete or give a measure from the source |
| Thesaurus triples ("efficient, effective, and streamlined")                           | Keep one word                            |
| Hollow claims with no proof                                                           | Cut, or keep only sourced facts          |
| Emoji seasoning that adds no meaning                                                  | Delete                                   |

## Fixed output format

Use this exact structure. Do not add a preamble. Do not wrap the whole reply in a code fence.

### Rewrite mode / Shorter mode

```markdown
## Simple English

[Full rewritten text. Preserve useful structure: headings, lists, links.
Keep untouchables exact.]

## Cuts

| Before                    | After            | Why          |
| ------------------------- | ---------------- | ------------ |
| quoted phrase or sentence | rewrite or (cut) | short reason |

List the 3ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“8 highest-value cuts only. Skip trivia.

## Stats

|                      | Before | After |
| -------------------- | ------ | ----- |
| Words                | N      | N     |
| Sentences            | N      | N     |
| Avg words / sentence | N      | N     |
| Passive voice        | N      | N     |
```

Approximate word counts are fine. Be consistent within the reply.

### Check mode

```markdown
## Findings

| #   | Issue                                                        | Quote | Fix     |
| --- | ------------------------------------------------------------ | ----- | ------- |
| 1   | long sentence / passive / filler / synonym / hedge / AI slop | "ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦"   | rewrite |

## Stats

| Words | Sentences | Avg | Passive | Filler hits |
| ----- | --------- | --- | ------- | ----------- |
| N     | N         | N   | N       | N           |
```

No full rewrite in Check mode unless the user asks for one after.

## Self-check (mandatory)

Before you deliver, run these four passes. Fix what you find.

1. Count words in your three longest sentences. Over 20 (procedural) or 25 (descriptive) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ split.
2. Search for: contractions (docs/specs), `has been` / `have been`, `should` / `would` / `might`, `, making` / `, allowing` / `, enabling`, semicolons, `utilize` / `leverage` / `robust` / `seamless`.
3. Every `if` / `when` in a procedure stands at the start of its sentence, before the command.
4. Synonym scan: check/verify/confirm/validate and config/settings/options. One term each.

For a longer audit, use `references/checklist.md`.

## Example

**Input:**

> The decision was made by the committee to utilize a more robust framework that would facilitate better outcomes for all stakeholders involved in the process.

**Output:**

```markdown
## Simple English

The committee chose a stronger framework.

## Cuts

| Before                                                  | After               | Why                   |
| ------------------------------------------------------- | ------------------- | --------------------- |
| The decision was made by the committee                  | The committee chose | active voice          |
| utilize                                                 | chose / use         | plain verb            |
| robust framework that would facilitate better outcomesÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦ | stronger framework  | empty claim + padding |

## Stats

|                      | Before | After |
| -------------------- | ------ | ----- |
| Words                | 26     | 6     |
| Sentences            | 1      | 1     |
| Avg words / sentence | 26     | 6     |
| Passive voice        | 1      | 0     |
```

## Remember

Short sentences. Plain words. Active voice. One meaning per word. Cut what does not earn its place. Deliver the rewrite first.
