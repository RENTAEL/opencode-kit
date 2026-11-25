---
name: docs-latex-expert
description: "This skill helps you write clean, modern LaTeX code. It can **review existing code** for anti-patterns and obsolete commands, and **help generate new LaTeX** following best practices."
---
# LaTeX Expert Skill

This skill helps you write clean, modern LaTeX code. It can **review existing code** for anti-patterns and obsolete commands, and **help generate new LaTeX** following best practices.

## How to Use

### Review LaTeX Code
Share your `.tex` code and ask for a review:

```
Can you review this LaTeX code for issues?

\documentclass{article}
\begin{document}
{\bf This is bold} and {\it this is italic}.
$$E = mc^2$$
\def\reals{\mathbb{R}}
\end{document}
```

The skill will identify obsolete commands, suggest modern replacements, and explain why.

### Generate LaTeX
Ask for help writing LaTeX:

```
Write a section about the Schrodinger equation with proper math formatting
```

The skill will produce well-structured LaTeX using modern commands and appropriate packages.

## Key Best Practices

- **Commands**: Use `\textbf{}` not `{\bf}`, `\newcommand` not `\def`, `\[...\]` not `$$...$$`
- **Math**: Use `align` from `amsmath` (never `eqnarray`), `\eqref` for equation refs, `\text{}` for text in math mode
- **Packages**: `amsmath`, `siunitx` for units, `cleveref` for smart refs, `physics` for QM notation
- **Style**: One sentence per line, label prefixes (`eq:`, `fig:`, `sec:`, `tab:`), BibTeX for references

See the `references/` directory for detailed cheat-sheets:
- [latex-commands.md](references/latex-commands.md) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Obsolete vs modern commands
- [latex-math.md](references/latex-math.md) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Math typesetting rules
- [latex-packages.md](references/latex-packages.md) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Package recommendations
- [latex-style.md](references/latex-style.md) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Source code conventions

## Gotchas

- **`$$...$$`** breaks vertical spacing and `fleqn`; always use `\[...\]`
- **`eqnarray`** produces inconsistent spacing; use `align` from `amsmath`
- **`{\bf}`** resets all font attributes; `\textbf{\textit{x}}` works, `{\it {\bf x}}` doesn't
- **`\def`** silently overwrites existing macros; use `\newcommand` (errors on conflict)
- **`\sloppy`** produces loose text; try rewording or `setspace` first
- **Manual bibliography** invites errors; always use BibTeX/BibLaTeX
- **`\mbox`** in math mode ignores font size; use `\text{}` instead

## Output Format

When reviewing LaTeX code, the skill will:

1. **List issues found** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â each with the line/context and why it's problematic
2. **Provide corrected code** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the same snippet rewritten with modern commands
3. **Explain improvements** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â why each change matters
4. **Suggest packages** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â if the document could benefit from specific packages

When generating LaTeX, the skill will:

1. **Produce clean source** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â one sentence per line, prefixed labels, proper environments
2. **Include recommended packages** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â in the preamble when needed
3. **Explain choices** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â why specific commands or environments were used

## Evaluation

Test prompts are in `evals/evals.json`. Run evaluations with:

```bash
python scripts/run_evaluation.py
```

---
*Following Agent Skills specification for proper progressive disclosure and best practices*
