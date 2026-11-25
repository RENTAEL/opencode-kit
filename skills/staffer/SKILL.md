---
name: staffer
description: "The general-purpose persona: a clean entry point for tasks that none of the specialists fit. Its prompt template is deliberately minimal ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the task text, the environment (cwd, branch, date), and the safety guardrails, nothing else. No role framing, no rules, n..."
---
# agy staffer

The general-purpose persona: a clean entry point for tasks that none of the specialists fit. Its prompt template is deliberately minimal ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the task text, the environment (cwd, branch, date), and the safety guardrails, nothing else. No role framing, no rules, no output format: the task defines its own output, and no unrelated template context can pull the run off course.

Prefer a specialist when one fits: `researcher` for surveys and deep dives, `reviewer` for second opinions on code or plans, `implementer` for edits to the working tree, `ask` for a cheap one-shot question.

staffer is also the route to agy-native tools no specialist covers ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â notably **image generation**: agy ships a `generate_image` tool (verified on v1.1.15; a 1024ÃƒÆ’Ã¢â‚¬â€1024 PNG in ~30s). Name the output path in the task, e.g. `staffer --prompt "generate a pixel-art robot mascot, save it as assets/mascot.png"`.

## Locating the companion

This skill file lives at `<plugin-root>/skills/staffer/SKILL.md`; resolve the companion path relative to this skill directory:

```bash
node "<skill-dir>/../../companion/agy-companion.mjs" staffer [flags] --prompt "task"
```

Pass the user's task text verbatim via `--prompt`; use `--prompt-file <path>` or `--stdin` for long text.

> [!IMPORTANT]
> Run this command **unsandboxed** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â agy needs a localhost port and its OAuth token file, which harness sandboxes hide. In Codex, request escalated permissions for the command. Details: `../jobs/references/troubleshooting.md`.

## Collecting the result

The command returns a job id. Read `../jobs/SKILL.md` for result collection and recovery: dispatch, wait for the final result, then validate as needed. Do not proactively observe progress, read logs or inspect intermediate artifacts while running. Observe only when the user explicitly asks for progress; diagnose a failure or a result requiring intervention under the jobs protocol.

## Flags (all optional)

- `--prompt <text>` / `--prompt-file <path>` / `--stdin` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the task, from exactly one of these three sources. Use file/stdin for long prompts instead of shell quoting.
- `--model <id>` or `--effort low|medium|high` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â default model is `gemini-3.8-flash-medium`.
- `--restricted` / `--unrestricted` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â permission profile; staffer defaults to unrestricted like the other tool-using personas, `--restricted` is the opt-in hardening path.
- `--continue` (or `--conversation <id>`), `--timeout <dur>` (default 60m, maximum 120m hard execution limit).

## Rules

- Pass the user's task through verbatim. Because the template imposes no output format, state the desired format in the task text when the caller needs a specific one.
- Pass the user's explicit authorizations through verbatim. The template default-denies costly or irreversible side effects (commits/pushes, deleting files outside the workspace, side-effectful network calls, paid-quota commands); that default opens only when the task itself asks for the operation.
- A general task may legitimately edit files. The companion reports any working-tree delta with the result ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â inspect it (`git diff`) and confirm it is what the task asked for before building on it.
- For errors and recovery, follow `../jobs/SKILL.md`.

For an existing conversation, `--continue` / `--conversation <id>` inherit its recorded model and permission profile unless explicitly overridden. The unrestricted defaults above apply to new tasks.
