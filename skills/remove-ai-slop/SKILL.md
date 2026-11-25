---
name: remove-ai-slop
description: "Identify and remove AI-slop: the filler, hedging, marketing, and jargon phrases that AI text generators lean on, the structural tells they use to manufacture insight, plus em-dash overuse. Output is cleaner prose with the meaning, facts, and technical terms intact."
---
# Remove AI Slop

Identify and remove AI-slop: the filler, hedging, marketing, and jargon
phrases that AI text generators lean on, the structural tells they use to
manufacture insight, plus em-dash overuse. Output is cleaner prose with the
meaning, facts, and technical terms intact.

This skill is a reviewer/cleaner, not a writer. It edits what is there; it
does not invent content or restructure the document.

It covers two kinds of slop:

- **Word-level** (words and phrases) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â see
  [references/phrases.md](references/phrases.md).
- **Structural** (constructions and rhythm) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â see
  [references/structures.md](references/structures.md).

## Workflow

1. **Identify the setting.** Determine the input: a file on disk to edit in
   place, or inline prose to return cleaned. If you write to a `.md` file,
   never wrap the result in a code fence ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the file content IS markdown.
2. **Scan the text.** Flag every match of the categories below. Record the
   exact location (line or sentence), the current phrase, and a proposed
   replacement.
3. **Report before editing** (unless the user asked for auto-fix). Present
   findings as a numbered table where each entry gets a number starting at 1:

   | # | Location | Phrase | Suggested fix |
   |---|----------|--------|---------------|

   Let the user accept or reject findings before you apply changes.
4. **Apply the selected fixes.** The user picks which findings to fix by
   number. Keep the meaning, facts, and technical terms intact.

   **Selecting findings.** Selection is 1-based and can be a single number,
   a comma-separated list, a range, or any combination:

   - Single: `3`
   - List: `1,2,5`
   - Range: `1-3`
   - Combined: `1-3,5,7-8`

   Whitespace after commas is allowed and ignored (`1, 3` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ findings 1 and
   3). An out-of-range number is not an error in the whole selection ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â apply
   the valid findings and report the ones that don't exist. Apply only what
   the user selected; leave the rest untouched for a later pass.
5. **Re-verify** against the validation checklist at the bottom, fix any
   remaining violations, then present the result.

## AI-slop detector

Flag each pattern below and replace it with plain, direct language. Many are
omittable outright. Full detail is in the reference files.

### Word-level

- **Adverbs** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â cut all of them (the -ly blanket rule). This includes
  "simply", "just", "easily", "effortlessly", "seamless(ly)", "obviously",
  "actually", "literally", "truly", "really", and all -ly softeners,
  intensifiers, and hedges. See [references/phrases.md](references/phrases.md).
- **Filler and throat-clearing openers** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â cut: "Here's the thing/why/this/
  that", "It turns out", "The uncomfortable truth is", "Let me be clear",
  "In today's fast-paced world", "It is important to note", "In conclusion".
- **Emphasis crutches and generic filler** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â cut: "Full stop.", "Let that
  sink in.", "Make no mistake", "At its core", "At the end of the day",
  "When it comes to", "In a world where".
- **Jargon and leverage verbs** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â plain-language replacement: "utilize" ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢
  "use"; "leverage" ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ "use"; "streamline" ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ "simplify"; "delve" ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ "examine";
  "harness/unleash/empower/revolutionize/unlock" ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ concrete verb;
  "navigate/unpack/lean into/deep dive/circle back/moving forward/
  game-changer/double down/landscape" ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ plain synonym. See the jargon tables in
  [references/phrases.md](references/phrases.md).
- **Meta-commentary** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â cut self-referential asides ("The rest of this essay
  explainsÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦", "In this section, we'llÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦").
- **Vague declaratives** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â cut or name the specific thing ("The implications
  are significant", "The stakes are high").
- **Telling instead of showing** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â name the concrete thing ("This is genuinely
  hard", "this is what X actually looks like").
- **Future tense for current behavior** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â change to present tense:
  "the tool will create" ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ "the tool creates"; "this app will let you" ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢
  "this app lets you".

### Structural

- **Binary contrasts** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â cut "not X, it's Y", "isn't X, it's Y", "X isn't the
  problem, Y is". State Y directly.
- **Negative listing** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â cut "not a X... not a Y... a Z". State Z.
- **Dramatic fragmentation** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â cut "X. And Y. And Z.", "[Noun]. That's it."
  Use complete sentences.
- **Rhetorical setups** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â cut "What if [reframe]?", "Here's what I mean:",
  "Think about it:".
- **False agency** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â inanimate things doing human verbs ("the decision
  emerges", "the market rewards", "the data tells us"). Name the human.
- **Passive voice** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â "X was created", "It is believed that". Find and name
  the actor.
- **Starters to avoid** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Wh- openers, paragraphs starting "So", sentences
  starting "Look,".
- **Rhythm** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â two items beat three; vary paragraph endings; no stacked
  fragments; no metronomic cadence.
- **Lazy extremes** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â "every/always/never/everyone/nobody" as false authority;
  use specifics.

See [references/structures.md](references/structures.md) for the pattern tables.

## Wordiness and tone

- No exclamation marks, no rhetorical questions, no emojis.
- Sentences ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â¤ 25 words; split nested clauses.
- Prefer common words: "use" not "utilize", "start" not "commence".
- No marketing superlatives ("best", "unparalleled", "game-changing").

## Em-dash rule

Default = `true` (remove em-dashes). An em-dash (`ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â`) is a common AI-slop
tick; strip it unless the user explicitly opts out.

- Replace an em-dash with a comma, a parenthetical, or by splitting and
  restructuring the sentence ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â whichever reads most clearly.
- Treat more than one em-dash per paragraph as overuse even if the user
  opts to keep them.
- Preserve an em-dash only when it is technically necessary (rare) and the
  user asked to keep em-dash usage.

## Gotchas

- **Never change meaning.** Remove slop, but keep intent, facts, and
  technical terms. Ask if an ambiguous edit could change what the author
  meant.
- **Don't write what isn't slop.** This skill edits AI-slop only; it does
  not impose a new structure or voice on competent existing prose.
- **Don't invent an actor.** When fixing false agency or passive voice, name
  a real actor or use "you". Never fabricate who did something.
- **Don't strip legitimate dashes.** Em-dashes in favor of a comma are an
  edit; a hyphen in a compound word (`state-of-the-art`) is not an em-dash.
- **Don't invent replacements.** Prefer omission or a known substitution to
  guessing at a synonym the author didn't intend.
- **Don't wrap the output in a code fence** when editing a `.md` file.

## Validation checklist

Before delivering, verify:

- [ ] No filler, hedging, or marketing adverbs remain ("simply", "just",
      "easily", "seamless(ly)", "actually", "literally", "truly", "really",
      "-ly" softeners)
- [ ] No empty openers remain ("Here's the thing", "In today's fast-paced
      world", "It is important to note", "In conclusion")
- [ ] No jargon or leverage verbs remain ("leverage", "utilize",
      "streamline", "delve", "navigate", "lean into", "deep dive",
      "circle back", "robust", "cutting-edge", "best-in-class")
- [ ] No meta-commentary remains ("The rest of this essay explainsÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦")
- [ ] No vague declaratives remain ("The implications are significant") ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â
      the specific thing is named
- [ ] No false agency or passive voice remains ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â a real actor is named
- [ ] No binary contrasts, negative listing, or dramatic fragmentation remain
- [ ] No rhetorical setups or rhetorical questions remain
- [ ] No future tense for current behavior ("will create" ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ "creates")
- [ ] No em-dashes remain (unless the user opted to keep them)
- [ ] No exclamation marks, rhetorical questions, or emojis
- [ ] Every sentence ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â¤ 25 words
- [ ] Rhythm is varied ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â no metronomic cadence, no stacked fragments
- [ ] Meaning, facts, and technical terms unchanged