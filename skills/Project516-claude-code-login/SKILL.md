---
name: Project516-claude-code-login
description: "Sign Claude Code into an Anthropic account when there is no interactive terminal or browser on the machine itself. Instead of letting `claude auth login` block on a prompt, run it in the background, hand the user the authorization URL, and feed the resulting code back."
---
# Claude Code OAuth Login (headless)

Sign Claude Code into an Anthropic account when there is no interactive
terminal or browser on the machine itself. Instead of letting `claude auth
login` block on a prompt, run it in the background, hand the user the
authorization URL, and feed the resulting code back.

## Prerequisites

- Claude Code installed and on PATH (`claude --version`).
- A network connection to `claude.com` / `platform.claude.com`.
- The user has an Anthropic account or subscription they can sign in with.

## Procedure

### 1. Check the current state

```bash
claude auth status
```

Expected states:

- `"loggedIn": true` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â already signed in, stop here.
- `"loggedIn": false` or `Please run /login` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â proceed.
- `Failed to authenticate: OAuth session expired and could not be refreshed` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â stale credentials; clear them first (step 2).

### 2. Clear stale credentials (only if auth fails or the session expired)

The OAuth session is stored in `~/.claude/.credentials.json`. Back it up
rather than deleting it outright:

```bash
mv ~/.claude/.credentials.json ~/.claude/.credentials.json.bak
```

Note: use `claude auth login`. The plain `claude login` command is legacy and
does not perform the browser flow.

### 3. Start the login in the background

`claude auth login` prints the authorization URL to stdout even without a
TTY, then waits on stdin for the pasted code. Run it in the background with
stdout redirected to a log file and stdin wired to a FIFO so it stays alive
while the user is away:

```bash
rm -f /tmp/claude_login_in /tmp/claude_login_out.txt
mkfifo /tmp/claude_login_in
setsid nohup claude auth login <> /tmp/claude_login_in > /tmp/claude_login_out.txt 2>&1 &
```

Key details:

- `<>` opens the FIFO read-write so nothing blocks at startup.
- stdout-to-file works because a TTY is not required.
- Do NOT wrap it in `script(1)`: the typescript file is buffered and stays
  empty until the process exits.

### 4. Capture the authorization URL

Wait a few seconds, then extract the URL:

```bash
sleep 3
grep -oa 'https://claude.com/cai/oauth/authorize[^ ]*' /tmp/claude_login_out.txt | head -1
```

### 5. Give the URL to the user

Present the URL. The user opens it in any browser, signs in, approves
consent, and is shown a code. The code may include a trailing `#<state>`
suffix ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â keep it when pasting back.

### 6. Submit the code

Write the code back into the FIFO (a trailing newline is required):

```bash
printf '%s\n' '<PASTE_CODE_HERE>' > /tmp/claude_login_in
```

The process completes the token exchange and prints `Login successful.`

### 7. Verify and clean up

```bash
claude auth status   # expect "loggedIn": true
rm -f /tmp/claude_login_in /tmp/claude_login_out.txt
```

The backup at `~/.claude/.credentials.json.bak` can be removed once login is
confirmed working.

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| `OAuth session expired and could not be refreshed` | Clear `~/.claude/.credentials.json` (step 2), then redo step 3. |
| `Not logged in Ãƒâ€šÃ‚Â· Please run /login` | Use `claude auth login`; the bare `claude login` command is legacy. |
| Log file stays empty | Give it 2-3 s. Confirm the background process is alive with `ps aux \| grep "claude auth login"`. |
| Process dies before the code is pasted | The OAuth state was bound to that run. Restart from step 3 to get a fresh URL. |
| Login succeeds but email looks wrong | Run `claude auth logout` and start over to sign in with a different account. |
