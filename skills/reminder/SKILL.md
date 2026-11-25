---
name: reminder
description: "Set silence-reminder nudges in airc. NOTE: not available in the rust-rewrite yet — no airc reminder verb exists; report that instead of guessing."
---
# airc reminder

> ÃƒÂ¢Ã…Â¡Ã‚Â ÃƒÂ¯Ã‚Â¸Ã‚Â **Not available in rust-rewrite yet** (TODO: remove this skill or port the
> command). There is no `airc reminder` verb, and the silence-reminder nudge timer
> (`airc reminder 300 | off | pause`) does not exist in the rust-rewrite. There is **no
> CLI equivalent.**

Run this yourself ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â don't ask the user.

## What there is instead

Nothing maps directly. The rust-rewrite has no per-scope idle-nudge timer surfaced
through the CLI. The closest related verb is `airc monitor`, which only *formats*
monitor events for AI/runtime consumers ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â it does not arm a silence reminder.

## When this comes up

- "Remind me if the room goes quiet for N seconds" ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â explain that idle-reminder timing is not a CLI feature in the rust-rewrite. If you need idle awareness, the runtime's own loop (Claude Monitor / Codex poll) is where that lives, not an `airc` subcommand.

## Notes

- Do not invent `airc reminder` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â it does not exist in the rust-rewrite.
