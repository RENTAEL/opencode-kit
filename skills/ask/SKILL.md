---
name: ask
description: "The quick mode: one question in, one answer out, ~3 seconds on the default `gemini-3.8-flash-low`. Zero tools by design (restricted profile, question-only prompt), so it needs no setup and works on a fresh install ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â run it first as the smoke test: `ask --promp..."
---
# agy ask

The quick mode: one question in, one answer out, ~3 seconds on the default `gemini-3.8-flash-low`. Zero tools by design (restricted profile, question-only prompt), so it needs no setup and works on a fresh install ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â run it first as the smoke test: `ask --prompt "reply with OK"`.

ask is the only persona that runs in the foreground: the call blocks and the answer comes back on stdout. staffer, researcher, reviewer, and implementer instead return a background job id (see the jobs skill, `../jobs/SKILL.md`).

## Locating the companion

This skill file lives at `<plugin-root>/skills/ask/SKILL.md`; resolve the companion path relative to this skill directory:

```bash
node "<skill-dir>/../../companion/agy-companion.mjs" ask [flags] --prompt "question"
```

Pass the user's question verbatim via `--prompt`; use `--prompt-file <path>` or `--stdin` for a long question.

> [!IMPORTANT]
> Run this command **unsandboxed** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â agy needs a localhost port and its OAuth token file, which harness sandboxes hide. In Codex, request escalated permissions for the command. Details: `../jobs/references/troubleshooting.md`.

## Flags (all optional)

- `--prompt <text>` / `--prompt-file <path>` / `--stdin` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the question, from exactly one of these three sources. Use file/stdin for a long question.
- `--continue` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â reuse the last ask conversation; `--conversation <id>` targets a specific one.
- `--model <id>` or `--effort low|medium|high` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â default model is `gemini-3.8-flash-low`.
- `--timeout <dur>` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â default 2m.

ask is always restricted (it is tool-free, so there is nothing to unrestrict); `--unrestricted` is ignored with a note on stderr. That is fixed for ask alone ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the tool-using personas default to unrestricted, where `--restricted` is an opt-in hardening flag. Execution style is likewise fixed per mode and no flag changes it.

## Rules

- Pass the user's question through verbatim and return the answer verbatim. The `[agy-staff]` telemetry line arrives on stderr and is metadata for you, the calling agent ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â do not show it to the user; mention the follow-up ability in natural language when relevant, and give model/duration/token numbers only if asked.
- If the answer says "not sure", relay it as-is; do not silently substitute your own answer.
- Exit 5 means a resumable response timeout: explain it and ask whether the user wants to continue with the suggested timeout or stop. Continue only after explicit user confirmation, using the recorded conversation and configuration. For other companion errors, quote the error and add a concise diagnosis. Full failure protocol: `../jobs/SKILL.md`.
