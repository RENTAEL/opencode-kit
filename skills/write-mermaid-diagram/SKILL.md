---
name: write-mermaid-diagram
description: "This skill owns the mechanics of Mermaid: which diagram type answers which question, what a label may contain before the parser rejects or silently mangles it, how to render a `.mmd` file to SVG or PNG, how to prove the render is real, and where the result can actually be pasted."
---
# Mermaid Diagrams

## Purpose

This skill owns the mechanics of Mermaid: which diagram type answers which question, what a label may contain before the parser rejects or silently mangles it, how to render a `.mmd` file to SVG or PNG, how to prove the render is real, and where the result can actually be pasted.

Everything here was verified against mermaid `11.17.2` through `@mermaid-js/mermaid-cli` `11.17.0`. Mermaid's parser rules are not guessable from the rendered output, and two of them fail silently, so the verified tables below are the point of the skill.

## Scope

This skill never states what a diagram should say about a domain. It states what the parser and the renderer will do.

## Choosing the Diagram Type

Pick from the question the reader arrives with, not from the shape of the data.

| The reader's question                          | Type              | Why this one                                                      |
| ---------------------------------------------- | ----------------- | ----------------------------------------------------------------- |
| What happens next, and where does it branch?   | `flowchart TD`    | Decision diamonds and labeled edges are the only native branching |
| Who calls whom, and in what order?             | `sequenceDiagram` | Participants plus ordering; lifelines show who is waiting         |
| When did each thing run, and what overlapped?  | `gantt`           | The only type with a real time axis and parallel rows             |
| What states exist and what moves between them? | `stateDiagram-v2` | Transitions are first class; terminal states are explicit         |
| What tables exist and how do they relate?      | `erDiagram`       | Cardinality notation is built in                                  |
| What types exist and what does each own?       | `classDiagram`    | Members and relationships in one node                             |
| How do these branches and merges relate?       | `gitGraph`        | Branch topology without hand-placed nodes                         |
| What share of a total?                         | `pie`             | One number per slice, nothing else                                |

All twelve of these render in this version: `flowchart`, `sequenceDiagram`, `gantt`, `stateDiagram-v2`, `erDiagram`, `classDiagram`, `gitGraph`, `pie`, `timeline`, `journey`, `mindmap`, `quadrantChart`. Two are easy to reach for wrongly:

- `timeline` orders events by label with no time axis. Spacing carries no duration and nothing can overlap. When elapsed time or concurrency matters, it is a `gantt`, whatever the word "timeline" in the request suggests.
- `journey` scores steps on a satisfaction axis. It is not a sequence diagram with nicer boxes.

A flowchart that has grown decision diamonds for ordering, or a sequence diagram with a participant per hour, is a sign the type was chosen before the question.

## File Layout

- One diagram per `.mmd` file. Mermaid has no include mechanism, so a file is the unit of both authoring and rendering.
- Name the file after what it shows, and keep a rendered `.svg` next to it when the diagram is a deliverable. Add a `.png` only when the destination cannot display SVG.
- Inside a Markdown document, use a fenced block tagged `mermaid`. The fence content is the same text as a `.mmd` file, with no extra indentation - leading indentation inside the fence is passed to the parser and breaks `gantt` and `pie`.

## Label Rules

This is where diagrams fail, and two of the three failure modes are silent. Verified per type:

| Type                         | Fatal in a label                              | Silently mangled | Safe                                                        |
| ---------------------------- | --------------------------------------------- | ---------------- | ----------------------------------------------------------- |
| `flowchart`, bare `A[...]`   | `(` `)` `[` `]` `{` `}` `"` and the pipe char | none             | `:` `,` `;` `#` `%` `&` `<` `>` `/` `-` `@`                 |
| `flowchart`, quoted `A["ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦"]` | `"`                                           | none             | everything else, brackets and pipe included                 |
| `sequenceDiagram` message    | `;`                                           | `#`              | `:` `(` `)` `[` `]` `{` `}` `,` `%` `&` `<` `>` `/` `-` `@` |
| `gantt` task label           | none                                          | `:`              | everything else                                             |
| `pie` slice label            | `"`                                           | none             | everything else                                             |

Three rules follow, and they cover nearly every real failure:

**Quote every flowchart label.** `A["step (x) done"]` parses; `A[step (x) done]` does not. Quoting costs two characters and removes five fatal characters at once. There is no case where a bare label is better.

**A colon in a gantt task label is a silent corruption, not an error.** The gantt parser splits a task line on `:` to separate the label from its metadata, so `plan: 4 tickets :2026-09-06 20:18, 2026-09-06 20:28` either fails outright or renders a bar with the wrong label and the wrong dates, depending on what follows the colon. Use `-` as the separator inside gantt labels, always. This one is worth checking for by grep before every gantt render:

```bash
grep -nE '^\s+[^:]*:[^:]*:' timeline.mmd   # a task line with two colons: the first one is in the label
```

**`#` starts a character entity.** `#35;` is a literal `#`, `#quot;` is a literal `"`. In a sequence message a bare `#` swallows the rest of the text; inside a quoted flowchart label it is safe. Write `PR #35;240 opened` in a sequence message and `A["say #quot;yes#quot;"]` in a flowchart, both verified to render the literal character.

Two more that are not character rules:

- **Line breaks inside a label** are `<br/>`, not a newline. A raw newline ends the statement.
- **Basic HTML renders inside labels** (`<b>`, `<i>`, `<br/>`, `<hr/>`) on flowchart and sequence nodes. Do not rely on it in `gantt`, whose labels are plain SVG text.

## Rendering

The CLI is not installed globally; `npx` resolves it from the npm cache, and Puppeteer's Chrome is already under `~/.cache/puppeteer`. A small diagram renders in about 1.5 seconds.

```bash
npx -y @mermaid-js/mermaid-cli -i diagram.mmd -o diagram.svg
npx -y @mermaid-js/mermaid-cli -i diagram.mmd -o diagram.png -s 2 -b white
```

- **Prefer SVG.** It is text, it diffs, it stays sharp at any zoom, and it is a fraction of the size. Render PNG only for a destination that cannot display SVG.
- **`-s 2`** doubles the raster scale. A wide diagram whose SVG viewBox is 3584 px renders as a 7168 px PNG, which is what makes small labels legible when someone zooms in. It does not change layout, only the raster resolution.
- **`-b white`** sets the background. Without it a PNG lands transparent, which reads as black text on black in any dark-mode viewer.
- **`-i` accepts a Markdown file**, in which case every fenced `mermaid` block in it is rendered and the block replaced with an image reference. Useful for a doc page, wrong for a single deliverable diagram.

## Verifying a Render

**The exit code does not tell you the diagram is valid.** A parse error inside an otherwise well-formed file makes mermaid-cli exit `0` and write an SVG whose entire content is the words "Syntax error in text". This is verified, and it is the single most expensive trap in this tooling: a build step that checks only `$?` will happily publish an error image.

Check the output, every time:

```bash
npx -y @mermaid-js/mermaid-cli -i diagram.mmd -o diagram.svg >/dev/null 2>&1
if [ ! -f diagram.svg ] || grep -q 'Syntax error' diagram.svg; then echo "render failed"; fi
```

For anything whose labels matter (a gantt especially, where a colon corrupts rather than fails), go one step further and read the text back out of the SVG:

```bash
grep -o '<text[^>]*>[^<]*' diagram.svg | sed 's/.*>//' | head -40
```

If a label you wrote is not in that list, the parser ate it. Comparing intended labels against rendered labels is the only check that catches silent mangling.

## Readability at Scale

Mermaid lays out automatically and will not warn when the result is unreadable.

- **Node count.** A flowchart past roughly 40 nodes stops being a diagram and becomes a wall. Split it, and name the sub-diagram at the node that leads to it.
- **Edge crossings** are the layout engine telling you the graph is not a tree. Reorder declarations so the main path is declared first and top to bottom; the engine follows declaration order.
- **Gantt row count** scales fine - 80 rows is readable - because each row is one line of text. Gantt fails on the time axis instead: set `tickInterval` so the chart has roughly 8 to 15 ticks, and set `axisFormat` to the smallest unit that distinguishes bars.
- **`todayMarker off`** on any gantt describing the past. Otherwise a vertical line for the current date lands somewhere arbitrary and readers try to interpret it.
- **Subgraphs add a box and a lot of vertical space.** Use them for genuinely parallel tracks, not for sequential grouping.

## Where Mermaid Renders

| Surface                                | Renders?                | What to send                                                                  |
| -------------------------------------- | ----------------------- | ----------------------------------------------------------------------------- |
| GitHub pull requests, issues, Markdown | Yes, natively           | The fenced `mermaid` block                                                    |
| Claude artifacts                       | Yes, natively           | A ```mermaid fence, or `<pre class="mermaid">` in HTML; do not load a library |
| VitePress and most static doc sites    | Yes, with the plugin on | The fenced block                                                              |
| Issue trackers (JIRA)                  | No                      | Attach the PNG; put the source in a code block below it                       |
| Chat apps                              | No                      | Upload the PNG; the source alone is unreadable there                          |

When the destination does not render Mermaid, send the image and keep the source next to it. The source is what makes the diagram editable later; the image is what makes it readable now.

## Debugging a Diagram That Will Not Parse

Mermaid's error messages point at the token it choked on, which is usually not where the mistake is. Bisect instead of reading the message:

1. Render the file. If the SVG says "Syntax error in text", the file parses as a diagram but a statement inside it is bad.
2. Cut the body in half, keeping the header lines (`gantt` plus `dateFormat`, or `flowchart TD`). Render again. The half that fails holds the bad statement; repeat.
3. Once it is one statement, apply the label rules above before looking anywhere else. In practice it is an unquoted flowchart label or a colon in a gantt label.
4. If a statement is clean and still fails, check for a tab character or trailing whitespace after a `<br/>`, and check that the fence or file has no leading indentation.

## Anti-Patterns

- Trusting the CLI exit code as proof a diagram rendered
- Bare flowchart labels; quote every one
- A colon inside a gantt task label, which corrupts silently rather than failing
- A bare `#` in a sequence message, which swallows the rest of the line
- Using `timeline` when durations or overlap matter; that is a `gantt`
- A PNG without `-b white`, invisible in dark mode
- PNG when the destination renders SVG
- Shipping a rendered image without keeping the `.mmd` source next to it
- Indenting a fenced `mermaid` block inside Markdown
- A raw newline instead of `<br/>` for a line break in a label
- `todayMarker` left on in a gantt describing the past
- Subgraphs used to group sequential steps
- Reading the parser's error message instead of bisecting the file

## Rules

- Pick the type from the reader's question; `gantt` is the only type with a real time axis
- One diagram per `.mmd` file; keep the source beside any rendered image
- Quote every flowchart label; escape a literal `"` as `#quot;`
- Never put `:` in a gantt task label; use `-` and grep for it before rendering
- Escape `#` as `#35;` in sequence messages
- `<br/>` for line breaks; never a raw newline
- Render with `npx -y @mermaid-js/mermaid-cli`; SVG by default, PNG only when required, with `-s 2 -b white`
- Verify every render by checking the file exists and does not contain "Syntax error", never by exit code alone
- Verify gantt labels by reading the text back out of the SVG
- `todayMarker off` on any gantt describing the past; tune `tickInterval` to 8 to 15 ticks
- Split a flowchart past roughly 40 nodes
- Send the image where Mermaid does not render (issue trackers, chat apps), the fence where it does (GitHub, Claude artifacts, doc sites)
- Bisect to find a parse error; do not trust the reported position
