---
name: dreamor-dingtalk-to-ai-skill
description: "This skill manages a bridge service that forwards messages from Dingtalk group chats to local AI CLI tools (OpenCode or Claude Code), allowing remote AI interaction from mobile devices via Dingtalk."
---
# Dingtalk Bridge Skill

This skill manages a bridge service that forwards messages from Dingtalk group chats to local AI CLI tools (OpenCode or Claude Code), allowing remote AI interaction from mobile devices via Dingtalk.

## Features

- **Chat Commands**: `/help`, `/status`, `/model`, `/history`, `/queue`, `/config`, `/reset`, `/remember`
- **Project Memory**: Auto-summarize conversations, inject context across sessions
- **Media Processing**: Voice transcription, image description (configurable)
- **Multi-Agent Routing**: Route messages to different AI providers by rules
- **Scheduler**: Cron-based scheduled message processing
- **Interactive Cards**: Dingtalk interactive card message support

## Quick Reference

| Command | Description |
|---------|-------------|
| `setup`, `ÃƒÂ©Ã¢â‚¬Â¦Ã‚ÂÃƒÂ§Ã‚Â½Ã‚Â®` | Interactive configuration wizard |
| `start`, `ÃƒÂ¥Ã‚ÂÃ‚Â¯ÃƒÂ¥Ã…Â Ã‚Â¨` | Start the bridge service |
| `stop`, `ÃƒÂ¥Ã‚ÂÃ…â€œÃƒÂ¦Ã‚Â­Ã‚Â¢` | Stop the bridge service |
| `status`, `ÃƒÂ§Ã…Â Ã‚Â¶ÃƒÂ¦Ã¢â€šÂ¬Ã‚Â` | Check if service is running |
| `logs [N]`, `ÃƒÂ¦Ã…Â¸Ã‚Â¥ÃƒÂ§Ã…â€œÃ¢â‚¬Â¹ÃƒÂ¦Ã¢â‚¬â€Ã‚Â¥ÃƒÂ¥Ã‚Â¿Ã¢â‚¬â€` | Show last N lines of logs (default: 50) |
| `doctor`, `ÃƒÂ¨Ã‚Â¯Ã…Â ÃƒÂ¦Ã¢â‚¬â€œÃ‚Â­` | Run diagnostics and troubleshoot issues |
| `rebuild`, `ÃƒÂ©Ã¢â‚¬Â¡Ã‚ÂÃƒÂ¦Ã¢â‚¬â€œÃ‚Â°ÃƒÂ¦Ã…Â¾Ã¢â‚¬Å¾ÃƒÂ¥Ã‚Â»Ã‚Âº` | Rebuild the TypeScript project |

## Workflow

### 1. Parse Command

Extract the subcommand from `$ARGUMENTS` based on user input (supports both English and Chinese keywords).

### 2. Configuration Check

For all commands except `setup`:
- Check if `.env` file exists in project root
- If missing: guide user to run `setup` first
- If present: proceed with command

### 3. Environment Detection

Detect which environment Claude is running in:
- **Claude Code**: Full features available including interactive prompts
- **Other/Codex**: Limited features, provide manual instructions instead

### 4. Execute Command

**setup**: Interactive wizard to configure Dingtalk credentials and AI provider preference

**start**: Build the project and start the bridge service via PM2

**stop**: Stop the PM2-managed bridge service

**status**: Report service health and connectivity

**logs**: Display service logs with optional line count

**doctor**: Run comprehensive diagnostics (env, deps, build, Dingtalk API connectivity)

**rebuild**: Compile TypeScript and verify build success

## Examples

### Interactive Configuration
User: "ÃƒÂ©Ã¢â‚¬Â¦Ã‚ÂÃƒÂ§Ã‚Â½Ã‚Â®ÃƒÂ©Ã¢â‚¬â„¢Ã¢â‚¬Â°ÃƒÂ©Ã¢â‚¬â„¢Ã¢â‚¬Â°"
AI: ÃƒÂ¦Ã¢â‚¬Â°Ã‚Â§ÃƒÂ¨Ã‚Â¡Ã…â€™ setup ÃƒÂ¥Ã¢â‚¬ËœÃ‚Â½ÃƒÂ¤Ã‚Â»Ã‚Â¤ÃƒÂ¯Ã‚Â¼Ã…â€™ÃƒÂ¥Ã‚ÂÃ‚Â¯ÃƒÂ¥Ã…Â Ã‚Â¨ÃƒÂ¤Ã‚ÂºÃ‚Â¤ÃƒÂ¤Ã‚ÂºÃ¢â‚¬â„¢ÃƒÂ¥Ã‚Â¼Ã‚ÂÃƒÂ©Ã¢â‚¬Â¦Ã‚ÂÃƒÂ§Ã‚Â½Ã‚Â®ÃƒÂ¥Ã‚ÂÃ¢â‚¬ËœÃƒÂ¥Ã‚Â¯Ã‚Â¼

### Start the Bridge
User: "ÃƒÂ¥Ã‚ÂÃ‚Â¯ÃƒÂ¥Ã…Â Ã‚Â¨ÃƒÂ©Ã¢â‚¬â„¢Ã¢â‚¬Â°ÃƒÂ©Ã¢â‚¬â„¢Ã¢â‚¬Â°ÃƒÂ¦Ã‚Â¡Ã‚Â¥ÃƒÂ¦Ã…Â½Ã‚Â¥ÃƒÂ¦Ã…â€œÃ‚ÂÃƒÂ¥Ã…Â Ã‚Â¡" / "start bridge"
AI: ÃƒÂ¦Ã¢â‚¬Â°Ã‚Â§ÃƒÂ¨Ã‚Â¡Ã…â€™ start ÃƒÂ¥Ã¢â‚¬ËœÃ‚Â½ÃƒÂ¤Ã‚Â»Ã‚Â¤ÃƒÂ¯Ã‚Â¼Ã…â€™ÃƒÂ¦Ã…Â¾Ã¢â‚¬Å¾ÃƒÂ¥Ã‚Â»Ã‚ÂºÃƒÂ©Ã‚Â¡Ã‚Â¹ÃƒÂ§Ã¢â‚¬ÂºÃ‚Â®ÃƒÂ¥Ã‚Â¹Ã‚Â¶ÃƒÂ©Ã¢â€šÂ¬Ã…Â¡ÃƒÂ¨Ã‚Â¿Ã¢â‚¬Â¡ PM2 ÃƒÂ¥Ã‚ÂÃ‚Â¯ÃƒÂ¥Ã…Â Ã‚Â¨ÃƒÂ¦Ã…â€œÃ‚ÂÃƒÂ¥Ã…Â Ã‚Â¡

### Check Service Status
User: "ÃƒÂ©Ã¢â‚¬â„¢Ã¢â‚¬Â°ÃƒÂ©Ã¢â‚¬â„¢Ã¢â‚¬Â°ÃƒÂ¦Ã‚Â¡Ã‚Â¥ÃƒÂ¦Ã…Â½Ã‚Â¥ÃƒÂ§Ã…Â Ã‚Â¶ÃƒÂ¦Ã¢â€šÂ¬Ã‚ÂÃƒÂ¥Ã‚Â¦Ã¢â‚¬Å¡ÃƒÂ¤Ã‚Â½Ã¢â‚¬Â¢"
AI: ÃƒÂ¦Ã¢â‚¬Â°Ã‚Â§ÃƒÂ¨Ã‚Â¡Ã…â€™ status ÃƒÂ¥Ã¢â‚¬ËœÃ‚Â½ÃƒÂ¤Ã‚Â»Ã‚Â¤ÃƒÂ¯Ã‚Â¼Ã…â€™ÃƒÂ¦Ã…Â Ã‚Â¥ÃƒÂ¥Ã¢â‚¬ËœÃ…Â ÃƒÂ¦Ã…â€œÃ‚ÂÃƒÂ¥Ã…Â Ã‚Â¡ÃƒÂ¥Ã‚ÂÃ‚Â¥ÃƒÂ¥Ã‚ÂºÃ‚Â·ÃƒÂ§Ã…Â Ã‚Â¶ÃƒÂ¦Ã¢â€šÂ¬Ã‚Â

### View Logs
User: "ÃƒÂ¦Ã…Â¸Ã‚Â¥ÃƒÂ§Ã…â€œÃ¢â‚¬Â¹ÃƒÂ¦Ã…â€œÃ¢â€šÂ¬ÃƒÂ¨Ã‚Â¿Ã¢â‚¬Ëœ100ÃƒÂ¨Ã‚Â¡Ã…â€™ÃƒÂ¦Ã¢â‚¬â€Ã‚Â¥ÃƒÂ¥Ã‚Â¿Ã¢â‚¬â€"
AI: ÃƒÂ¦Ã¢â‚¬Â°Ã‚Â§ÃƒÂ¨Ã‚Â¡Ã…â€™ logs 100 ÃƒÂ¥Ã¢â‚¬ËœÃ‚Â½ÃƒÂ¤Ã‚Â»Ã‚Â¤

### Run Diagnostics
User: "ÃƒÂ©Ã¢â‚¬â„¢Ã¢â‚¬Â°ÃƒÂ©Ã¢â‚¬â„¢Ã¢â‚¬Â°ÃƒÂ¦Ã‚Â¡Ã‚Â¥ÃƒÂ¦Ã…Â½Ã‚Â¥ÃƒÂ¦Ã…â€œÃ¢â‚¬Â°ÃƒÂ©Ã¢â‚¬â€Ã‚Â®ÃƒÂ©Ã‚Â¢Ã‹Å“"
AI: ÃƒÂ¦Ã¢â‚¬Â°Ã‚Â§ÃƒÂ¨Ã‚Â¡Ã…â€™ doctor ÃƒÂ¥Ã¢â‚¬ËœÃ‚Â½ÃƒÂ¤Ã‚Â»Ã‚Â¤ÃƒÂ¯Ã‚Â¼Ã…â€™ÃƒÂ¨Ã‚Â¿Ã¢â‚¬ÂºÃƒÂ¨Ã‚Â¡Ã…â€™ÃƒÂ¥Ã¢â‚¬Â¦Ã‚Â¨ÃƒÂ©Ã‚ÂÃ‚Â¢ÃƒÂ¨Ã‚Â¯Ã…Â ÃƒÂ¦Ã¢â‚¬â€œÃ‚Â­

## Edge Cases

- **Missing `.env` file**: Guide user to run `setup` first
- **PM2 service not found**: Provide rebuild instructions with `rebuild` command
- **Dingtalk API connection failed**: Show specific error and suggest `doctor` command
- **Service already running**: Inform user and suggest `stop` first
- **Build failed**: Display error messages and suggest checking dependencies

## Important Notes

- Always mask secrets in output (show only last 4 characters)
- The service defaults to Stream mode, falling back to Polling if needed
- Configuration persists in `.env` file with restricted permissions (600)
- Project memory is enabled by default, auto-summarizes after 20 messages
- Media processing (voice/image) is disabled by default, enable via `MEDIA_VOICE_TRANSCRIPTION=true` / `MEDIA_IMAGE_DESCRIPTION=true`
- Multi-agent routing is disabled by default, enable via `ROUTER_ENABLED=true`
- Scheduler is disabled by default, enable via `SCHEDULER_ENABLED=true`
- Project directory: `$PROJECT_DIR` (current working directory)