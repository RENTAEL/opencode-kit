# slides-animejs

Turn a topic, an outline, some notes, or an existing `.pptx` into a **browser-served, full-screen, animated slide deck** — powered by [anime.js v4](https://animejs.com/). You run it locally with one command and present from any browser, no internet required.

It's a [skill](https://docs.claude.com/en/docs/agents-and-tools/agent-skills) for AI coding agents like **Claude Code** and **OpenCode**. You talk to your agent in plain language ("make me an animated slideshow about X"), and the skill walks you through building the deck step by step.

---

## What you get

- **A 16:9 full-screen deck** — the browser window *is* the slide. No tiny "slide on a webpage" look.
- **Smooth animations** — elements fly/fade in on entrance, and slides have subtle "idle" motion so they never feel static.
- **PowerPoint-style click-advance** — reveal points one click at a time.
- **A presenter overlay** — previous/next buttons, a slide counter, a progress bar, a grid overview, fullscreen, and speaker notes.
- **Works offline** — the animation library is bundled in; nothing phones home.
- **Runs with one command** — `python3 run.py` opens it in your browser.

The result is a self-contained `presentation/` folder you can zip, share, or present from anywhere.

---

## Requirements

- **Python 3** (only the standard library — no `pip install` needed). Check with `python3 --version`.
- **An AI coding agent** that supports skills — [Claude Code](https://docs.claude.com/en/docs/claude-code/overview) or [OpenCode](https://opencode.ai/).
- A modern web browser (Chrome, Firefox, Safari, or Edge).

> **Heads-up:** This skill *orchestrates* several companion skills (for content, design, static slides, and animation tips). The first time you run it, it tells you which ones are missing and how to add them. The core deck still builds without the optional ones.

---

## Installation

### Claude Code

Clone directly into Claude Code's skills directory:

```sh
mkdir -p ~/.claude/skills
git clone https://github.com/YOUR-USERNAME/slides-animejs.git ~/.claude/skills/slides-animejs
```

Or copy the files manually if you already have this repo cloned:

```sh
mkdir -p ~/.claude/skills/slides-animejs
cp -R . ~/.claude/skills/slides-animejs/
```

### OpenCode

Clone directly into OpenCode's skills directory:

```sh
mkdir -p ~/.config/opencode/skills
git clone https://github.com/YOUR-USERNAME/slides-animejs.git ~/.config/opencode/skills/slides-animejs
```

Or copy the files manually if you already have this repo cloned:

```sh
mkdir -p ~/.config/opencode/skills/slides-animejs
cp -R . ~/.config/opencode/skills/slides-animejs/
```

> **Note:** OpenCode also scans `~/.claude/skills/` for compatibility, so if you use both tools, a single clone into `~/.claude/skills/slides-animejs/` is enough.

> Replace `YOUR-USERNAME` with your GitHub username (or use this repo's actual URL). Unlike a single-file skill, slides-animejs ships folders (`assets/`, `references/`, `scripts/`, `examples/`) — so clone or copy the **whole repo**, not just `SKILL.md`.

---

## How to use it

Just ask your agent, in plain language. The skill triggers on requests like:

- *"Make an animated web slideshow about photosynthesis for high-schoolers."*
- *"Turn this `.pptx` into an interactive HTML deck with animations."*
- *"Build me a fullscreen browser presentation from these notes."*

From there it runs an **interactive, step-by-step workflow** and checks in with you at each stage — you stay in control the whole time:

1. **Setup** — grabs the latest anime.js reference and checks dependencies.
2. **Intake** — reads your input and asks about your audience, length, tone, and look.
3. **Content** — drafts the slides with you, one section at a time.
4. **Design** — picks colours, fonts, and a visual style (you approve it).
5. **Visuals** — you drop any images you want into a `visuals/` folder.
6. **Draft** — builds static slides for you to review.
7. **Animate** — adds the motion (only after you say go).
8. **Done** — hands you the run command.

When it's finished, run:

```sh
cd presentation
python3 run.py
```

Your browser opens at `http://localhost:8000` with the finished deck.

### Presenting

| Key | Action |
|-----|--------|
| `→` / `Space` | Next step / slide |
| `←` | Previous step / slide |
| `F` | Fullscreen |
| `G` | Grid overview of all slides |
| `S` | Speaker notes |
| `Esc` | Close panels / exit fullscreen |

---

## See a working example

This repo includes a ready-to-run sample deck under [`examples/minimal/`](examples/minimal/). It's five slides, each showing one core pattern (title, section divider, two-column content, click-advance steps, and a closing). To try it:

```sh
cd examples/minimal/presentation
python3 run.py
```

Open `examples/minimal/slides-draft/` to see how each slide is written.

---

## How it's organized

```
slides-animejs/
├── SKILL.md          ← the instructions your agent reads
├── references/       ← detailed playbooks (workflow, design rules, animation patterns)
├── assets/           ← the runtime: slide loader, overlay, server, templates
├── scripts/          ← build + helper scripts (Python, stdlib only)
└── examples/minimal/ ← a runnable sample deck
```

You don't need to read any of this to use the skill — your agent does. It's here if you want to peek under the hood.

---

## Frequently asked

**Do I need to know JavaScript or anime.js?**
No. You describe what you want; the skill writes the slides and animations.

**Does it need an internet connection to present?**
No. The finished deck is fully offline — anime.js is bundled into the `presentation/` folder.

**Can I edit the slides afterwards?**
Yes. Slides are plain HTML files in `presentation/slides/`. Edit them, or ask your agent to.

**Can I change the colours?**
Yes — the palette is fully customizable. Tell your agent your colours (or a brand), and it themes the deck for you.

**Can it read my existing PowerPoint?**
Yes. Point it at a `.pptx` and it pulls in the text, notes, and images as a starting point.
