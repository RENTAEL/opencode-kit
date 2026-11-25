# claude-code-login

An [opencode](https://opencode.ai) skill for signing Claude Code into an
Anthropic account on a headless, remote, or agent-driven machine where a
browser cannot open automatically.

## What it does

The skill walks an agent through the Claude Code OAuth login flow without an
interactive terminal:

1. Checks the current auth state (`claude auth status`).
2. Detects and clears stale OAuth credentials.
3. Starts `claude auth login` in the background with stdin on a FIFO.
4. Captures the authorization URL from the log output.
5. Hands the URL to the user and accepts the pasted code.
6. Verifies the login and cleans up.

## Install

For opencode, copy the folder into a skills directory:

```bash
mkdir -p ~/.config/opencode/skills/claude-code-login
cp SKILL.md ~/.config/opencode/skills/claude-code-login/
```

Claude Code itself also auto-loads skills from `~/.claude/skills/`:

```bash
mkdir -p ~/.claude/skills/claude-code-login
cp SKILL.md ~/.claude/skills/claude-code-login/
```

Alternatively, register the repo's parent directory via `skills.paths` in
`opencode.json`.

## Usage

Ask the agent something like: "log me into Claude Code", "sign in to Claude",
or "help me authenticate claude auth login".

## Requirements

- Claude Code CLI installed (`claude --version`).
- A network connection to `claude.com` / `platform.claude.com`.
- An Anthropic account or subscription.