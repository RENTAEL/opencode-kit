---
name: writer-memory
description: "Persistent memory system designed for creative writers, with first-class support for Korean storytelling workflows."
---
# Writer Memory - Agentic Memory System for Writers

Persistent memory system designed for creative writers, with first-class support for Korean storytelling workflows.

## Overview

Writer Memory maintains context across OpenCode sessions for fiction writers. It tracks:

- **Characters (ÃƒÂ¬Ã‚ÂºÃ‚ÂÃƒÂ«Ã‚Â¦Ã‚Â­ÃƒÂ­Ã¢â‚¬Å¾Ã‚Â°)**: Emotional arcs (ÃƒÂªÃ‚Â°Ã‚ÂÃƒÂ¬Ã‚Â Ã¢â‚¬Â¢ÃƒÂªÃ‚Â¶Ã‚Â¤ÃƒÂ«Ã‚ÂÃ¢â‚¬Å¾), attitudes (ÃƒÂ­Ã†â€™Ã…â€œÃƒÂ«Ã‚ÂÃ¢â‚¬Å¾), dialogue tone (ÃƒÂ«Ã…â€™Ã¢â€šÂ¬ÃƒÂ¬Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ­Ã¢â‚¬Â Ã‚Â¤), speech levels
- **World (ÃƒÂ¬Ã¢â‚¬Å¾Ã‚Â¸ÃƒÂªÃ‚Â³Ã¢â‚¬Å¾ÃƒÂªÃ‚Â´Ã¢â€šÂ¬)**: Settings, rules, atmosphere, constraints
- **Relationships (ÃƒÂªÃ‚Â´Ã¢â€šÂ¬ÃƒÂªÃ‚Â³Ã¢â‚¬Å¾)**: Character dynamics and evolution over time
- **Scenes (ÃƒÂ¬Ã…Â¾Ã‚Â¥ÃƒÂ«Ã‚Â©Ã‚Â´)**: Cut composition (ÃƒÂ¬Ã‚Â»Ã‚Â·ÃƒÂªÃ‚ÂµÃ‚Â¬ÃƒÂ¬Ã¢â‚¬Å¾Ã‚Â±), narration tone, emotional tags
- **Themes (ÃƒÂ­Ã¢â‚¬Â¦Ã…â€™ÃƒÂ«Ã‚Â§Ã‹â€ )**: Emotional themes (ÃƒÂ¬Ã‚Â Ã¢â‚¬Â¢ÃƒÂ¬Ã¢â‚¬Å¾Ã…â€œÃƒÂ­Ã¢â‚¬Â¦Ã…â€™ÃƒÂ«Ã‚Â§Ã‹â€ ), authorial intent

All data persists in `.writer-memory/memory.json` for git-friendly collaboration.

## Commands

| Command | Action |
|---------|--------|
| `/writer-memory init <project-name>` | Initialize new project memory |
| `/writer-memory status` | Show memory overview (character count, scene count, etc) |
| `/writer-memory char add <name>` | Add new character |
| `/writer-memory char <name>` | View character details |
| `/writer-memory char update <name> <field> <value>` | Update character field |
| `/writer-memory char list` | List all characters |
| `/writer-memory rel add <char1> <char2> <type>` | Add relationship |
| `/writer-memory rel <char1> <char2>` | View relationship |
| `/writer-memory rel update <char1> <char2> <event>` | Add relationship event |
| `/writer-memory scene add <title>` | Add new scene |
| `/writer-memory scene <id>` | View scene details |
| `/writer-memory scene list` | List all scenes |
| `/writer-memory theme add <name>` | Add theme |
| `/writer-memory world set <field> <value>` | Set world attribute |
| `/writer-memory query <question>` | Query memory naturally (Korean supported) |
| `/writer-memory validate <character> <dialogue>` | Check if dialogue matches character tone |
| `/writer-memory synopsis` | Generate emotion-focused synopsis |
| `/writer-memory export` | Export full memory as readable markdown |
| `/writer-memory backup` | Create manual backup |

## Memory Types

### ÃƒÂ¬Ã‚ÂºÃ‚ÂÃƒÂ«Ã‚Â¦Ã‚Â­ÃƒÂ­Ã¢â‚¬Å¾Ã‚Â° ÃƒÂ«Ã‚Â©Ã¢â‚¬ÂÃƒÂ«Ã‚ÂªÃ‚Â¨ÃƒÂ«Ã‚Â¦Ã‚Â¬ (Character Memory)

Tracks individual character attributes essential for consistent portrayal:

| Field | Korean | Description |
|-------|--------|-------------|
| `arc` | ÃƒÂªÃ‚Â°Ã‚ÂÃƒÂ¬Ã‚Â Ã¢â‚¬Â¢ÃƒÂªÃ‚Â¶Ã‚Â¤ÃƒÂ«Ã‚ÂÃ¢â‚¬Å¾ | Emotional journey (e.g., "ÃƒÂ¬Ã‚Â²Ã‚Â´ÃƒÂ«Ã¢â‚¬Â¦Ã‚Â -> ÃƒÂ¬Ã…Â¡Ã¢â‚¬Â¢ÃƒÂ«Ã‚Â§Ã‚ÂÃƒÂ¬Ã…Â¾Ã‚ÂÃƒÂªÃ‚Â°Ã‚Â -> ÃƒÂ¬Ã¢â‚¬Å¾Ã‚Â ÃƒÂ­Ã†â€™Ã‚Â") |
| `attitude` | ÃƒÂ­Ã†â€™Ã…â€œÃƒÂ«Ã‚ÂÃ¢â‚¬Å¾ | Current disposition toward life/others |
| `tone` | ÃƒÂ«Ã…â€™Ã¢â€šÂ¬ÃƒÂ¬Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ­Ã¢â‚¬Â Ã‚Â¤ | Dialogue style (e.g., "ÃƒÂ«Ã¢â‚¬Â¹Ã‚Â´ÃƒÂ«Ã‚Â°Ã‚Â±", "ÃƒÂ¬Ã‚Â§Ã‚ÂÃƒÂ¬Ã¢â‚¬Å¾Ã‚Â¤ÃƒÂ¬Ã‚Â Ã‚Â", "ÃƒÂ­Ã…Â¡Ã…â€™ÃƒÂ­Ã¢â‚¬ÂÃ‚Â¼ÃƒÂ¬Ã‚Â Ã‚Â") |
| `speechLevel` | ÃƒÂ«Ã‚Â§Ã‚ÂÃƒÂ­Ã‹â€ Ã‚Â¬ ÃƒÂ«Ã‚Â Ã‹â€ ÃƒÂ«Ã‚Â²Ã‚Â¨ | Formality: ÃƒÂ«Ã‚Â°Ã‹Å“ÃƒÂ«Ã‚Â§Ã‚Â, ÃƒÂ¬Ã‚Â¡Ã‚Â´ÃƒÂ«Ã…â€™Ã¢â‚¬Å“ÃƒÂ«Ã‚Â§Ã‚Â, ÃƒÂ­Ã¢â‚¬Â¢Ã‚Â´ÃƒÂ¬Ã‚Â²Ã‚Â´, ÃƒÂ­Ã‹Å“Ã‚Â¼ÃƒÂ­Ã¢â‚¬Â¢Ã‚Â© |
| `keywords` | ÃƒÂ­Ã¢â‚¬Â¢Ã‚ÂµÃƒÂ¬Ã¢â‚¬Â¹Ã‚Â¬ ÃƒÂ«Ã¢â‚¬Â¹Ã‚Â¨ÃƒÂ¬Ã¢â‚¬â€œÃ‚Â´ | Characteristic words/phrases they use |
| `taboo` | ÃƒÂªÃ‚Â¸Ã‹â€ ÃƒÂªÃ‚Â¸Ã‚Â°ÃƒÂ¬Ã¢â‚¬â€œÃ‚Â´ | Words/phrases they would never say |
| `emotional_baseline` | ÃƒÂªÃ‚Â°Ã‚ÂÃƒÂ¬Ã‚Â Ã¢â‚¬Â¢ ÃƒÂªÃ‚Â¸Ã‚Â°ÃƒÂ¬Ã‚Â¤Ã¢â€šÂ¬ÃƒÂ¬Ã¢â‚¬Å¾Ã‚Â  | Default emotional state |
| `triggers` | ÃƒÂ­Ã…Â Ã‚Â¸ÃƒÂ«Ã‚Â¦Ã‚Â¬ÃƒÂªÃ‚Â±Ã‚Â° | What provokes emotional reactions |

**Example:**
```
/writer-memory char add ÃƒÂ¬Ã†â€™Ã‹â€ ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ
/writer-memory char update ÃƒÂ¬Ã†â€™Ã‹â€ ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ arc "ÃƒÂ¬Ã‚Â²Ã‚Â´ÃƒÂ«Ã¢â‚¬Â¦Ã‚Â -> ÃƒÂ¬Ã…Â¡Ã¢â‚¬Â¢ÃƒÂ«Ã‚Â§Ã‚ÂÃƒÂ¬Ã…Â¾Ã‚ÂÃƒÂªÃ‚Â°Ã‚Â -> ÃƒÂ¬Ã¢â‚¬Å¾Ã‚Â ÃƒÂ­Ã†â€™Ã‚Â"
/writer-memory char update ÃƒÂ¬Ã†â€™Ã‹â€ ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ tone "ÃƒÂ«Ã¢â‚¬Â¹Ã‚Â´ÃƒÂ«Ã‚Â°Ã‚Â±, ÃƒÂ­Ã‹Å“Ã¢â‚¬Å¾ÃƒÂ¬Ã…Â¾Ã‚Â¬ÃƒÂ¬Ã‚Â¶Ã‚Â©ÃƒÂ¬Ã¢â‚¬Â¹Ã‚Â¤, ÃƒÂªÃ‚Â°Ã‚ÂÃƒÂ¬Ã‚Â Ã¢â‚¬Â¢ÃƒÂ¬Ã¢â‚¬â€œÃ‚ÂµÃƒÂ¬Ã‚Â Ã…â€œ"
/writer-memory char update ÃƒÂ¬Ã†â€™Ã‹â€ ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ speechLevel "ÃƒÂ­Ã¢â‚¬Â¢Ã‚Â´ÃƒÂ¬Ã‚Â²Ã‚Â´"
/writer-memory char update ÃƒÂ¬Ã†â€™Ã‹â€ ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ keywords "ÃƒÂªÃ‚Â·Ã‚Â¸ÃƒÂ«Ã†â€™Ã‚Â¥, ÃƒÂ«Ã‚Â­Ã‚Â, ÃƒÂªÃ‚Â´Ã…â€œÃƒÂ¬Ã‚Â°Ã‚Â®ÃƒÂ¬Ã¢â‚¬Â¢Ã¢â‚¬Å¾"
/writer-memory char update ÃƒÂ¬Ã†â€™Ã‹â€ ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ taboo "ÃƒÂ¬Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ«Ã…Â¾Ã¢â‚¬ËœÃƒÂ­Ã¢â‚¬Â¢Ã‚Â´, ÃƒÂ«Ã‚Â³Ã‚Â´ÃƒÂªÃ‚Â³Ã‚Â ÃƒÂ¬Ã¢â‚¬Â¹Ã‚Â¶ÃƒÂ¬Ã¢â‚¬â€œÃ‚Â´"
```

### ÃƒÂ¬Ã¢â‚¬Å¾Ã‚Â¸ÃƒÂªÃ‚Â³Ã¢â‚¬Å¾ÃƒÂªÃ‚Â´Ã¢â€šÂ¬ ÃƒÂ«Ã‚Â©Ã¢â‚¬ÂÃƒÂ«Ã‚ÂªÃ‚Â¨ÃƒÂ«Ã‚Â¦Ã‚Â¬ (World Memory)

Establishes the universe your story inhabits:

| Field | Korean | Description |
|-------|--------|-------------|
| `setting` | ÃƒÂ«Ã‚Â°Ã‚Â°ÃƒÂªÃ‚Â²Ã‚Â½ | Time, place, social context |
| `rules` | ÃƒÂªÃ‚Â·Ã…â€œÃƒÂ¬Ã‚Â¹Ã¢â€žÂ¢ | How the world operates (magic systems, social norms) |
| `atmosphere` | ÃƒÂ«Ã‚Â¶Ã¢â‚¬Å¾ÃƒÂ¬Ã…â€œÃ¢â‚¬Å¾ÃƒÂªÃ‚Â¸Ã‚Â° | Overall mood and tone |
| `constraints` | ÃƒÂ¬Ã‚Â Ã…â€œÃƒÂ¬Ã¢â‚¬Â¢Ã‚Â½ | What cannot happen in this world |
| `history` | ÃƒÂ¬Ã¢â‚¬â€Ã‚Â­ÃƒÂ¬Ã¢â‚¬Å¡Ã‚Â¬ | Relevant backstory |

### ÃƒÂªÃ‚Â´Ã¢â€šÂ¬ÃƒÂªÃ‚Â³Ã¢â‚¬Å¾ ÃƒÂ«Ã‚Â©Ã¢â‚¬ÂÃƒÂ«Ã‚ÂªÃ‚Â¨ÃƒÂ«Ã‚Â¦Ã‚Â¬ (Relationship Memory)

Captures the dynamic between characters over time:

| Field | Description |
|-------|-------------|
| `type` | Base relationship: romantic, familial, friendship, rivalry, professional |
| `status` | Current state: budding, stable, strained, broken, healing |
| `power_dynamic` | Who has the upper hand, if any |
| `events` | Timeline of relationship-changing moments |
| `tension` | Current unresolved conflicts |
| `intimacy_level` | Emotional closeness (1-10) |

**Example:**
```
/writer-memory rel add ÃƒÂ¬Ã†â€™Ã‹â€ ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ ÃƒÂ­Ã¢â‚¬Â¢Ã‚Â´ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ romantic
/writer-memory rel update ÃƒÂ¬Ã†â€™Ã‹â€ ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ ÃƒÂ­Ã¢â‚¬Â¢Ã‚Â´ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ "ÃƒÂ¬Ã‚Â²Ã‚Â« ÃƒÂ­Ã¢â‚¬Å¡Ã‚Â¤ÃƒÂ¬Ã…Â Ã‚Â¤ - ÃƒÂ¬Ã†â€™Ã‹â€ ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ ÃƒÂ­Ã…Â¡Ã…â€™ÃƒÂ­Ã¢â‚¬ÂÃ‚Â¼"
/writer-memory rel update ÃƒÂ¬Ã†â€™Ã‹â€ ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ ÃƒÂ­Ã¢â‚¬Â¢Ã‚Â´ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ "ÃƒÂ­Ã¢â‚¬Â¢Ã‚Â´ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ ÃƒÂªÃ‚Â³Ã‚Â ÃƒÂ«Ã‚Â°Ã‚Â± ÃƒÂªÃ‚Â±Ã‚Â°ÃƒÂ¬Ã‚Â Ã‹â€ ÃƒÂ«Ã¢â‚¬Â¹Ã‚Â¹ÃƒÂ­Ã¢â‚¬Â¢Ã‚Â¨"
/writer-memory rel update ÃƒÂ¬Ã†â€™Ã‹â€ ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ ÃƒÂ­Ã¢â‚¬Â¢Ã‚Â´ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ "ÃƒÂ¬Ã†â€™Ã‹â€ ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ ÃƒÂ«Ã‚Â¨Ã‚Â¼ÃƒÂ¬Ã‚Â Ã¢â€šÂ¬ ÃƒÂ¬Ã¢â‚¬Â Ã‚Â ÃƒÂ¬Ã…Â¾Ã‚Â¡ÃƒÂ¬Ã‚ÂÃ…â€™"
```

### ÃƒÂ¬Ã…Â¾Ã‚Â¥ÃƒÂ«Ã‚Â©Ã‚Â´ ÃƒÂ«Ã‚Â©Ã¢â‚¬ÂÃƒÂ«Ã‚ÂªÃ‚Â¨ÃƒÂ«Ã‚Â¦Ã‚Â¬ (Scene Memory)

Tracks individual scenes and their emotional architecture:

| Field | Korean | Description |
|-------|--------|-------------|
| `title` | ÃƒÂ¬Ã‚Â Ã…â€œÃƒÂ«Ã‚ÂªÃ‚Â© | Scene identifier |
| `characters` | ÃƒÂ«Ã¢â‚¬Å“Ã‚Â±ÃƒÂ¬Ã…Â¾Ã‚Â¥ÃƒÂ¬Ã‚ÂÃ‚Â¸ÃƒÂ«Ã‚Â¬Ã‚Â¼ | Who appears |
| `location` | ÃƒÂ¬Ã…Â¾Ã‚Â¥ÃƒÂ¬Ã¢â‚¬Â Ã…â€™ | Where it happens |
| `cuts` | ÃƒÂ¬Ã‚Â»Ã‚Â· ÃƒÂªÃ‚ÂµÃ‚Â¬ÃƒÂ¬Ã¢â‚¬Å¾Ã‚Â± | Shot-by-shot breakdown |
| `narration_tone` | ÃƒÂ«Ã¢â‚¬Å¡Ã‚Â´ÃƒÂ«Ã‚Â Ã‹â€ ÃƒÂ¬Ã‚ÂÃ‚Â´ÃƒÂ¬Ã¢â‚¬Â¦Ã‹Å“ ÃƒÂ­Ã¢â‚¬Â Ã‚Â¤ | Narrative voice style |
| `emotional_tag` | ÃƒÂªÃ‚Â°Ã‚ÂÃƒÂ¬Ã‚Â Ã¢â‚¬Â¢ ÃƒÂ­Ã†â€™Ã…â€œÃƒÂªÃ‚Â·Ã‚Â¸ | Primary emotions (e.g., "ÃƒÂ¬Ã¢â‚¬Å¾Ã‚Â¤ÃƒÂ«Ã‚Â Ã‹Å“+ÃƒÂ«Ã‚Â¶Ã‹â€ ÃƒÂ¬Ã¢â‚¬Â¢Ã‹â€ ") |
| `purpose` | ÃƒÂ«Ã‚ÂªÃ‚Â©ÃƒÂ¬Ã‚Â Ã‚Â | Why this scene exists in the story |
| `before_after` | ÃƒÂ¬Ã‚Â Ã¢â‚¬Å¾ÃƒÂ­Ã¢â‚¬ÂºÃ¢â‚¬Å¾ ÃƒÂ«Ã‚Â³Ã¢â€šÂ¬ÃƒÂ­Ã¢â€žÂ¢Ã¢â‚¬Â | What changes for characters |

### ÃƒÂ­Ã¢â‚¬Â¦Ã…â€™ÃƒÂ«Ã‚Â§Ã‹â€  ÃƒÂ«Ã‚Â©Ã¢â‚¬ÂÃƒÂ«Ã‚ÂªÃ‚Â¨ÃƒÂ«Ã‚Â¦Ã‚Â¬ (Theme Memory)

Captures the deeper meaning woven through your story:

| Field | Korean | Description |
|-------|--------|-------------|
| `name` | ÃƒÂ¬Ã‚ÂÃ‚Â´ÃƒÂ«Ã‚Â¦Ã¢â‚¬Å¾ | Theme identifier |
| `expression` | ÃƒÂ­Ã¢â‚¬ËœÃ…â€œÃƒÂ­Ã‹Å“Ã¢â‚¬Å¾ ÃƒÂ«Ã‚Â°Ã‚Â©ÃƒÂ¬Ã¢â‚¬Â¹Ã‚Â | How this theme manifests |
| `scenes` | ÃƒÂªÃ‚Â´Ã¢â€šÂ¬ÃƒÂ«Ã‚Â Ã‚Â¨ ÃƒÂ¬Ã…Â¾Ã‚Â¥ÃƒÂ«Ã‚Â©Ã‚Â´ | Scenes that embody this theme |
| `character_links` | ÃƒÂ¬Ã‚ÂºÃ‚ÂÃƒÂ«Ã‚Â¦Ã‚Â­ÃƒÂ­Ã¢â‚¬Å¾Ã‚Â° ÃƒÂ¬Ã¢â‚¬â€Ã‚Â°ÃƒÂªÃ‚Â²Ã‚Â° | Which characters carry this theme |
| `author_intent` | ÃƒÂ¬Ã…Â¾Ã¢â‚¬ËœÃƒÂªÃ‚Â°Ã¢â€šÂ¬ ÃƒÂ¬Ã‚ÂÃ‹Å“ÃƒÂ«Ã‚ÂÃ¢â‚¬Å¾ | What you want readers to feel |

## Synopsis Generation (ÃƒÂ¬Ã¢â‚¬Â¹Ã…â€œÃƒÂ«Ã¢â‚¬Â Ã¢â‚¬Â°ÃƒÂ¬Ã¢â‚¬Â¹Ã…â€œÃƒÂ¬Ã…Â Ã‚Â¤)

The `/synopsis` command generates an emotion-focused summary using 5 essential elements:

### 5 Essential Elements (ÃƒÂ¬Ã¢â‚¬Â¹Ã…â€œÃƒÂ«Ã¢â‚¬Â Ã¢â‚¬Â°ÃƒÂ¬Ã¢â‚¬Â¹Ã…â€œÃƒÂ¬Ã…Â Ã‚Â¤ 5ÃƒÂ¬Ã…Â¡Ã¢â‚¬ÂÃƒÂ¬Ã¢â‚¬Â Ã…â€™)

1. **ÃƒÂ¬Ã‚Â£Ã‚Â¼ÃƒÂ¬Ã‚ÂÃ‚Â¸ÃƒÂªÃ‚Â³Ã‚Âµ ÃƒÂ­Ã†â€™Ã…â€œÃƒÂ«Ã‚ÂÃ¢â‚¬Å¾ ÃƒÂ¬Ã…Â¡Ã¢â‚¬ÂÃƒÂ¬Ã¢â‚¬Â¢Ã‚Â½** (Protagonist Attitude Summary)
   - How the protagonist approaches life/love/conflict
   - Their core emotional stance
   - Example: "ÃƒÂ¬Ã†â€™Ã‹â€ ÃƒÂ«Ã…Â¾Ã¢â‚¬ËœÃƒÂ¬Ã‚ÂÃ¢â€šÂ¬ ÃƒÂ¬Ã†â€™Ã‚ÂÃƒÂ¬Ã¢â‚¬Â¹Ã‚Â¤ÃƒÂ¬Ã‚ÂÃ¢â‚¬Å¾ ÃƒÂ¬Ã‹Å“Ã‹â€ ÃƒÂ«Ã‚Â°Ã‚Â©ÃƒÂ­Ã¢â‚¬Â¢Ã‹Å“ÃƒÂªÃ‚Â¸Ã‚Â° ÃƒÂ¬Ã…â€œÃ¢â‚¬Å¾ÃƒÂ­Ã¢â‚¬Â¢Ã‚Â´ ÃƒÂ«Ã‚Â¨Ã‚Â¼ÃƒÂ¬Ã‚Â Ã¢â€šÂ¬ ÃƒÂ­Ã‚ÂÃ‚Â¬ÃƒÂªÃ‚Â¸Ã‚Â°ÃƒÂ­Ã¢â‚¬Â¢Ã‹Å“ÃƒÂ«Ã…Â Ã¢â‚¬Â ÃƒÂ¬Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ«Ã…Â¾Ã…â€™"

2. **ÃƒÂªÃ‚Â´Ã¢â€šÂ¬ÃƒÂªÃ‚Â³Ã¢â‚¬Å¾ ÃƒÂ­Ã¢â‚¬Â¢Ã‚ÂµÃƒÂ¬Ã¢â‚¬Â¹Ã‚Â¬ ÃƒÂªÃ‚ÂµÃ‚Â¬ÃƒÂ«Ã‚ÂÃ¢â‚¬Å¾** (Core Relationship Structure)
   - The central dynamic driving the story
   - Power imbalances and tensions
   - Example: "ÃƒÂ¬Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ«Ã…Â¾Ã¢â‚¬ËœÃƒÂ«Ã‚Â°Ã¢â‚¬ÂºÃƒÂ«Ã…Â Ã¢â‚¬Â ÃƒÂ¬Ã…Â¾Ã‚ÂÃƒÂ¬Ã¢â€žÂ¢Ã¢â€šÂ¬ ÃƒÂ¬Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ«Ã…Â¾Ã¢â‚¬ËœÃƒÂ­Ã¢â‚¬Â¢Ã‹Å“ÃƒÂ«Ã…Â Ã¢â‚¬Â ÃƒÂ¬Ã…Â¾Ã‚ÂÃƒÂ¬Ã‚ÂÃ‹Å“ ÃƒÂ«Ã‚Â¶Ã‹â€ ÃƒÂªÃ‚Â·Ã‚Â ÃƒÂ­Ã‹Å“Ã¢â‚¬Â¢"

3. **ÃƒÂ¬Ã‚Â Ã¢â‚¬Â¢ÃƒÂ¬Ã¢â‚¬Å¾Ã…â€œÃƒÂ¬Ã‚Â Ã‚Â ÃƒÂ­Ã¢â‚¬Â¦Ã…â€™ÃƒÂ«Ã‚Â§Ã‹â€ ** (Emotional Theme)
   - The feeling the story evokes
   - Not plot, but emotional truth
   - Example: "ÃƒÂ¬Ã¢â‚¬Â Ã‚ÂÃƒÂ¬Ã¢â‚¬â€Ã‚Â ÃƒÂ¬Ã‚Â¥Ã¢â‚¬Â ÃƒÂ­Ã¢â‚¬â€œÃ¢â‚¬Â°ÃƒÂ«Ã‚Â³Ã‚ÂµÃƒÂ¬Ã‚ÂÃ¢â‚¬Å¾ ÃƒÂ«Ã‚Â¯Ã‚Â¿ÃƒÂ¬Ã‚Â§Ã¢â€šÂ¬ ÃƒÂ«Ã‚ÂªÃ‚Â»ÃƒÂ­Ã¢â‚¬Â¢Ã‹Å“ÃƒÂ«Ã…Â Ã¢â‚¬Â ÃƒÂ«Ã‚Â¶Ã‹â€ ÃƒÂ¬Ã¢â‚¬Â¢Ã‹â€ "

4. **ÃƒÂ¬Ã…Â¾Ã‚Â¥ÃƒÂ«Ã‚Â¥Ã‚Â´ vs ÃƒÂ¬Ã¢â‚¬Â¹Ã‚Â¤ÃƒÂ¬Ã‚Â Ã…â€œÃƒÂªÃ‚Â°Ã‚ÂÃƒÂ¬Ã‚Â Ã¢â‚¬Â¢ ÃƒÂ«Ã…â€™Ã¢â€šÂ¬ÃƒÂ«Ã‚Â¹Ã¢â‚¬Å¾** (Genre vs Real Emotion Contrast)
   - Surface genre expectations vs. actual emotional content
   - Example: "ÃƒÂ«Ã‚Â¡Ã…â€œÃƒÂ«Ã‚Â§Ã‚Â¨ÃƒÂ¬Ã…Â Ã‚Â¤ÃƒÂ¬Ã‚Â§Ã¢â€šÂ¬ÃƒÂ«Ã‚Â§Ã…â€™ ÃƒÂ«Ã‚Â³Ã‚Â¸ÃƒÂ¬Ã‚Â§Ã‹â€ ÃƒÂ¬Ã‚ÂÃ¢â€šÂ¬ ÃƒÂ¬Ã…Â¾Ã‚ÂÃƒÂªÃ‚Â¸Ã‚Â°ÃƒÂ¬Ã‹â€ Ã‹Å“ÃƒÂ¬Ã…Â¡Ã‚Â© ÃƒÂ¬Ã¢â‚¬Å¾Ã…â€œÃƒÂ¬Ã¢â‚¬Å¡Ã‚Â¬"

5. **ÃƒÂ¬Ã¢â‚¬â€Ã¢â‚¬ÂÃƒÂ«Ã¢â‚¬ÂÃ‚Â© ÃƒÂ¬Ã‚Â Ã¢â‚¬Â¢ÃƒÂ¬Ã¢â‚¬Å¾Ã…â€œ ÃƒÂ¬Ã…Â¾Ã¢â‚¬ÂÃƒÂ¬Ã†â€™Ã‚Â** (Ending Emotional Aftertaste)
   - The lingering feeling after the story ends
   - Example: "ÃƒÂ¬Ã¢â‚¬ÂÃ‚ÂÃƒÂ¬Ã¢â‚¬Å“Ã‚Â¸ÃƒÂ­Ã¢â‚¬Â¢Ã…â€œ ÃƒÂ¬Ã¢â‚¬Â¢Ã‹â€ ÃƒÂ«Ã‚ÂÃ¢â‚¬Å¾, ÃƒÂ«Ã‚Â¶Ã‹â€ ÃƒÂ¬Ã¢â€žÂ¢Ã¢â‚¬Å¾ÃƒÂ¬Ã‚Â Ã¢â‚¬Å¾ÃƒÂ­Ã¢â‚¬Â¢Ã…â€œ ÃƒÂ­Ã¢â‚¬Â¢Ã‚Â´ÃƒÂ­Ã¢â‚¬ÂÃ‚Â¼ÃƒÂ¬Ã¢â‚¬â€Ã¢â‚¬ÂÃƒÂ«Ã¢â‚¬ÂÃ‚Â©ÃƒÂ¬Ã‚ÂÃ‹Å“ ÃƒÂ¬Ã¢â‚¬â€Ã‚Â¬ÃƒÂ¬Ã…Â¡Ã‚Â´"

## Character Validation (ÃƒÂ¬Ã‚ÂºÃ‚ÂÃƒÂ«Ã‚Â¦Ã‚Â­ÃƒÂ­Ã¢â‚¬Å¾Ã‚Â° ÃƒÂªÃ‚Â²Ã¢â€šÂ¬ÃƒÂ¬Ã‚Â¦Ã‚Â)

The `/validate` command checks if dialogue matches a character's established voice.

### What Gets Checked

| Check | Description |
|-------|-------------|
| **Speech Level** | Does formality match? (ÃƒÂ«Ã‚Â°Ã‹Å“ÃƒÂ«Ã‚Â§Ã‚Â/ÃƒÂ¬Ã‚Â¡Ã‚Â´ÃƒÂ«Ã…â€™Ã¢â‚¬Å“ÃƒÂ«Ã‚Â§Ã‚Â/ÃƒÂ­Ã¢â‚¬Â¢Ã‚Â´ÃƒÂ¬Ã‚Â²Ã‚Â´) |
| **Tone Match** | Does the emotional register fit? |
| **Keyword Usage** | Uses characteristic words? |
| **Taboo Violation** | Uses forbidden words? |
| **Emotional Range** | Within character's baseline? |
| **Context Fit** | Appropriate for relationship and scene? |

### Validation Results

- **PASS**: Dialogue is consistent with character
- **WARN**: Minor inconsistencies, may be intentional
- **FAIL**: Significant deviation from established voice

**Example:**
```
/writer-memory validate ÃƒÂ¬Ã†â€™Ã‹â€ ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ "ÃƒÂ¬Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ«Ã…Â¾Ã¢â‚¬ËœÃƒÂ­Ã¢â‚¬Â¢Ã‚Â´, ÃƒÂ­Ã¢â‚¬Â¢Ã‚Â´ÃƒÂ«Ã…Â¾Ã¢â‚¬ËœÃƒÂ¬Ã¢â‚¬Â¢Ã¢â‚¬Å¾. ÃƒÂ«Ã¢â‚¬Å¾Ã‹â€ ÃƒÂ«Ã‚Â¬Ã‚Â´ ÃƒÂ«Ã‚Â³Ã‚Â´ÃƒÂªÃ‚Â³Ã‚Â ÃƒÂ¬Ã¢â‚¬Â¹Ã‚Â¶ÃƒÂ¬Ã¢â‚¬â€Ã‹â€ ÃƒÂ¬Ã¢â‚¬â€œÃ‚Â´."
```
Output:
```
[FAIL] ÃƒÂ¬Ã†â€™Ã‹â€ ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ validation failed:
- TABOO: "ÃƒÂ¬Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ«Ã…Â¾Ã¢â‚¬ËœÃƒÂ­Ã¢â‚¬Â¢Ã‚Â´" - character avoids direct declarations
- TABOO: "ÃƒÂ«Ã‚Â³Ã‚Â´ÃƒÂªÃ‚Â³Ã‚Â ÃƒÂ¬Ã¢â‚¬Â¹Ã‚Â¶ÃƒÂ¬Ã¢â‚¬â€Ã‹â€ ÃƒÂ¬Ã¢â‚¬â€œÃ‚Â´" - character suppresses longing expressions
- TONE: Too emotionally direct for ÃƒÂ¬Ã†â€™Ã‹â€ ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ's ÃƒÂ«Ã¢â‚¬Â¹Ã‚Â´ÃƒÂ«Ã‚Â°Ã‚Â± style

Suggested alternatives:
- "...ÃƒÂ¬Ã¢â€žÂ¢Ã¢â‚¬ÂÃƒÂ«Ã¢â‚¬Å¾Ã‚Â¤." (minimal acknowledgment)
- "ÃƒÂ«Ã…Â Ã‚Â¦ÃƒÂ¬Ã¢â‚¬â€Ã‹â€ ÃƒÂ«Ã¢â‚¬Â¹Ã‚Â¤." (deflection to external fact)
- "ÃƒÂ«Ã‚Â°Ã‚Â¥ ÃƒÂ«Ã‚Â¨Ã‚Â¹ÃƒÂ¬Ã¢â‚¬â€Ã‹â€ ÃƒÂ¬Ã¢â‚¬â€œÃ‚Â´?" (care expressed through practical concern)
```

## Context Query (ÃƒÂ«Ã‚Â§Ã‚Â¥ÃƒÂ«Ã‚ÂÃ‚Â½ ÃƒÂ¬Ã‚Â§Ã‹â€ ÃƒÂ¬Ã‚ÂÃ‹Å“)

Natural language queries against memory, with full Korean support.

### Example Queries

```
/writer-memory query "ÃƒÂ¬Ã†â€™Ã‹â€ ÃƒÂ«Ã…Â¾Ã¢â‚¬ËœÃƒÂ¬Ã‚ÂÃ¢â€šÂ¬ ÃƒÂ¬Ã‚ÂÃ‚Â´ ÃƒÂ¬Ã†â€™Ã‚ÂÃƒÂ­Ã¢â€žÂ¢Ã‚Â©ÃƒÂ¬Ã¢â‚¬â€Ã‚ÂÃƒÂ¬Ã¢â‚¬Å¾Ã…â€œ ÃƒÂ«Ã‚Â­Ã‚ÂÃƒÂ«Ã‚ÂÃ‚Â¼ÃƒÂªÃ‚Â³Ã‚Â  ÃƒÂ­Ã¢â‚¬Â¢Ã‚Â ÃƒÂªÃ‚Â¹Ã…â€™?"
/writer-memory query "ÃƒÂªÃ‚Â·Ã…â€œÃƒÂ«Ã‚Â¦Ã‚Â¬ÃƒÂ¬Ã‚ÂÃ‹Å“ ÃƒÂ­Ã‹Å“Ã¢â‚¬Å¾ÃƒÂ¬Ã…Â¾Ã‚Â¬ ÃƒÂªÃ‚Â°Ã‚ÂÃƒÂ¬Ã‚Â Ã¢â‚¬Â¢ ÃƒÂ¬Ã†â€™Ã‚ÂÃƒÂ­Ã†â€™Ã…â€œÃƒÂ«Ã…Â Ã¢â‚¬Â?"
/writer-memory query "ÃƒÂ­Ã¢â‚¬Â¢Ã‚Â´ÃƒÂ«Ã…Â¾Ã¢â‚¬ËœÃƒÂªÃ‚Â³Ã‚Â¼ ÃƒÂ¬Ã†â€™Ã‹â€ ÃƒÂ«Ã…Â¾Ã¢â‚¬ËœÃƒÂ¬Ã‚ÂÃ‹Å“ ÃƒÂªÃ‚Â´Ã¢â€šÂ¬ÃƒÂªÃ‚Â³Ã¢â‚¬Å¾ÃƒÂ«Ã…Â Ã¢â‚¬Â ÃƒÂ¬Ã¢â‚¬â€œÃ‚Â´ÃƒÂ«Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂªÃ‚Â¹Ã…â€™ÃƒÂ¬Ã‚Â§Ã¢â€šÂ¬ ÃƒÂ¬Ã¢â€žÂ¢Ã¢â‚¬ÂÃƒÂ«Ã¢â‚¬Å¡Ã‹Å“?"
/writer-memory query "ÃƒÂ¬Ã‚ÂÃ‚Â´ ÃƒÂ¬Ã…Â¾Ã‚Â¥ÃƒÂ«Ã‚Â©Ã‚Â´ÃƒÂ¬Ã‚ÂÃ‹Å“ ÃƒÂ¬Ã‚Â Ã¢â‚¬Â¢ÃƒÂ¬Ã¢â‚¬Å¾Ã…â€œÃƒÂ¬Ã‚Â Ã‚Â ÃƒÂ«Ã‚Â¶Ã¢â‚¬Å¾ÃƒÂ¬Ã…â€œÃ¢â‚¬Å¾ÃƒÂªÃ‚Â¸Ã‚Â°ÃƒÂ«Ã…Â Ã¢â‚¬Â?"
/writer-memory query "ÃƒÂ¬Ã†â€™Ã‹â€ ÃƒÂ«Ã…Â¾Ã¢â‚¬ËœÃƒÂ¬Ã‚ÂÃ‚Â´ ÃƒÂ«Ã‚Â¨Ã‚Â¼ÃƒÂ¬Ã‚Â Ã¢â€šÂ¬ ÃƒÂ¬Ã¢â‚¬â€Ã‚Â°ÃƒÂ«Ã‚ÂÃ‚Â½ÃƒÂ­Ã¢â‚¬Â¢Ã‹Å“ÃƒÂ«Ã…Â Ã¢â‚¬Â ÃƒÂªÃ‚Â²Ã…â€™ ÃƒÂ«Ã‚Â§Ã…Â¾ÃƒÂ¬Ã¢â‚¬Â¢Ã¢â‚¬Å¾?"
/writer-memory query "ÃƒÂ­Ã¢â‚¬Â¢Ã‚Â´ÃƒÂ«Ã…Â¾Ã¢â‚¬ËœÃƒÂ¬Ã‚ÂÃ‚Â´ ÃƒÂ­Ã¢â€žÂ¢Ã¢â‚¬ÂÃƒÂ«Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¬Ã‚ÂÃ¢â‚¬Å¾ ÃƒÂ«Ã¢â‚¬Â¢Ã…â€™ ÃƒÂ«Ã‚Â§Ã‚ÂÃƒÂ­Ã‹â€ Ã‚Â¬ÃƒÂ«Ã…Â Ã¢â‚¬Â?"
```

The system synthesizes answers from all relevant memory types.

## Behavior

1. **On Init**: Creates `.writer-memory/memory.json` with project metadata and empty collections
2. **Auto-Backup**: Changes are backed up before modification to `.writer-memory/backups/`
3. **Korean-First**: Emotion vocabulary uses Korean terms throughout
4. **Session Loading**: Memory is loaded on session start for immediate context
5. **Git-Friendly**: JSON formatted for clean diffs and collaboration

## Integration

### With OMC Notepad System
Writer Memory integrates with `.opencode/state/notepad.md`:
- Scene ideas can be captured as notes
- Character insights from analysis sessions are preserved
- Cross-reference between notepad and memory

### With Architect Agent
For complex character analysis:
```
@architect(model="opus",
     prompt="Analyze ÃƒÂ¬Ã†â€™Ã‹â€ ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ's arc across all scenes...")
```

### Character Validation Pipeline
Validation pulls context from:
- Character memory (tone, keywords, taboo)
- Relationship memory (dynamics with dialogue partner)
- Scene memory (current emotional context)
- Theme memory (authorial intent)

### Synopsis Builder
Synopsis generation aggregates:
- All character arcs
- Key relationship events
- Scene emotional tags
- Theme expressions

## Examples

### Full Workflow

```
# Initialize project
/writer-memory init ÃƒÂ«Ã‚Â´Ã¢â‚¬Å¾ÃƒÂ¬Ã‚ÂÃ‹Å“ ÃƒÂ«Ã‚ÂÃ‚ÂÃƒÂ¬Ã…Â¾Ã‚ÂÃƒÂ«Ã‚ÂÃ‚Â½

# Add characters
/writer-memory char add ÃƒÂ¬Ã†â€™Ã‹â€ ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ
/writer-memory char update ÃƒÂ¬Ã†â€™Ã‹â€ ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ arc "ÃƒÂ¬Ã‚Â²Ã‚Â´ÃƒÂ«Ã¢â‚¬Â¦Ã‚Â -> ÃƒÂ¬Ã…Â¡Ã¢â‚¬Â¢ÃƒÂ«Ã‚Â§Ã‚ÂÃƒÂ¬Ã…Â¾Ã‚ÂÃƒÂªÃ‚Â°Ã‚Â -> ÃƒÂ¬Ã¢â‚¬Å¾Ã‚Â ÃƒÂ­Ã†â€™Ã‚Â"
/writer-memory char update ÃƒÂ¬Ã†â€™Ã‹â€ ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ tone "ÃƒÂ«Ã¢â‚¬Â¹Ã‚Â´ÃƒÂ«Ã‚Â°Ã‚Â±, ÃƒÂ­Ã‹Å“Ã¢â‚¬Å¾ÃƒÂ¬Ã…Â¾Ã‚Â¬ÃƒÂ¬Ã‚Â¶Ã‚Â©ÃƒÂ¬Ã¢â‚¬Â¹Ã‚Â¤"
/writer-memory char update ÃƒÂ¬Ã†â€™Ã‹â€ ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ speechLevel "ÃƒÂ­Ã¢â‚¬Â¢Ã‚Â´ÃƒÂ¬Ã‚Â²Ã‚Â´"

/writer-memory char add ÃƒÂ­Ã¢â‚¬Â¢Ã‚Â´ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ
/writer-memory char update ÃƒÂ­Ã¢â‚¬Â¢Ã‚Â´ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ arc "ÃƒÂ­Ã¢â€žÂ¢Ã¢â‚¬Â¢ÃƒÂ¬Ã¢â‚¬Â¹Ã‚Â  -> ÃƒÂ«Ã‚ÂÃ¢â€žÂ¢ÃƒÂ¬Ã…Â¡Ã¢â‚¬Â -> ÃƒÂªÃ‚Â¸Ã‚Â°ÃƒÂ«Ã¢â‚¬Â¹Ã‚Â¤ÃƒÂ«Ã‚Â¦Ã‚Â¼"
/writer-memory char update ÃƒÂ­Ã¢â‚¬Â¢Ã‚Â´ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ tone "ÃƒÂ¬Ã‚Â§Ã‚ÂÃƒÂ¬Ã‚Â§Ã¢â‚¬Å¾, ÃƒÂ¬Ã¢â‚¬Â Ã¢â‚¬ÂÃƒÂ¬Ã‚Â§Ã‚Â"
/writer-memory char update ÃƒÂ­Ã¢â‚¬Â¢Ã‚Â´ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ speechLevel "ÃƒÂ«Ã‚Â°Ã‹Å“ÃƒÂ«Ã‚Â§Ã‚Â"

# Establish relationship
/writer-memory rel add ÃƒÂ¬Ã†â€™Ã‹â€ ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ ÃƒÂ­Ã¢â‚¬Â¢Ã‚Â´ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ romantic
/writer-memory rel update ÃƒÂ¬Ã†â€™Ã‹â€ ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ ÃƒÂ­Ã¢â‚¬Â¢Ã‚Â´ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ "ÃƒÂ¬Ã‚Â²Ã‚Â« ÃƒÂ«Ã‚Â§Ã…â€™ÃƒÂ«Ã¢â‚¬Å¡Ã‚Â¨ - ÃƒÂ­Ã¢â‚¬Â¢Ã‚Â´ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ ÃƒÂ¬Ã‚ÂÃ‚Â¼ÃƒÂ«Ã‚Â°Ã‚Â©ÃƒÂ¬Ã‚Â Ã‚Â ÃƒÂ­Ã‹Å“Ã‚Â¸ÃƒÂªÃ‚Â°Ã‚Â"
/writer-memory rel update ÃƒÂ¬Ã†â€™Ã‹â€ ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ ÃƒÂ­Ã¢â‚¬Â¢Ã‚Â´ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ "ÃƒÂ¬Ã†â€™Ã‹â€ ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ ÃƒÂªÃ‚Â±Ã‚Â°ÃƒÂ¬Ã‚Â Ã‹â€ "
/writer-memory rel update ÃƒÂ¬Ã†â€™Ã‹â€ ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ ÃƒÂ­Ã¢â‚¬Â¢Ã‚Â´ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ "ÃƒÂ¬Ã…Â¾Ã‚Â¬ÃƒÂ­Ã…Â¡Ã…â€™ - ÃƒÂ¬Ã†â€™Ã‹â€ ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ ÃƒÂ«Ã¢â‚¬Å¡Ã‚Â´ÃƒÂ¬Ã‚Â Ã‚Â ÃƒÂ«Ã‚ÂÃ¢â€žÂ¢ÃƒÂ¬Ã…Â¡Ã¢â‚¬Â"

# Set world
/writer-memory world set setting "ÃƒÂ¬Ã¢â‚¬Å¾Ã…â€œÃƒÂ¬Ã…Â¡Ã‚Â¸, ÃƒÂ­Ã‹Å“Ã¢â‚¬Å¾ÃƒÂ«Ã…â€™Ã¢â€šÂ¬, 20ÃƒÂ«Ã…â€™Ã¢â€šÂ¬ ÃƒÂ­Ã¢â‚¬ÂºÃ¢â‚¬Å¾ÃƒÂ«Ã‚Â°Ã‹Å“ ÃƒÂ¬Ã‚Â§Ã‚ÂÃƒÂ¬Ã…Â¾Ã‚Â¥ÃƒÂ¬Ã‚ÂÃ‚Â¸"
/writer-memory world set atmosphere "ÃƒÂ«Ã‚ÂÃ¢â‚¬Å¾ÃƒÂ¬Ã¢â‚¬Â¹Ã…â€œÃƒÂ¬Ã‚ÂÃ‹Å“ ÃƒÂªÃ‚Â±Ã‚Â´ÃƒÂ¬Ã‚Â¡Ã‚Â°ÃƒÂ­Ã¢â‚¬Â¢Ã‚Â¨ ÃƒÂ¬Ã¢â‚¬Â Ã‚Â ÃƒÂ«Ã‚Â¯Ã‚Â¸ÃƒÂ«Ã‚Â¬Ã‹Å“ÃƒÂ­Ã¢â‚¬Â¢Ã…â€œ ÃƒÂ¬Ã‹Å“Ã‚Â¨ÃƒÂªÃ‚Â¸Ã‚Â°"

# Add themes
/writer-memory theme add "ÃƒÂ­Ã‚ÂÃ‚Â¬ÃƒÂªÃ‚Â¸Ã‚Â°ÃƒÂ­Ã¢â‚¬Â¢Ã‹Å“ÃƒÂ¬Ã‚Â§Ã¢â€šÂ¬ ÃƒÂ¬Ã¢â‚¬Â¢Ã…Â ÃƒÂ«Ã…Â Ã¢â‚¬Â ÃƒÂ¬Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ"
/writer-memory theme add "ÃƒÂ¬Ã…Â¾Ã‚ÂÃƒÂªÃ‚Â¸Ã‚Â° ÃƒÂ«Ã‚Â³Ã‚Â´ÃƒÂ­Ã‹Å“Ã‚Â¸ÃƒÂ¬Ã‚ÂÃ‹Å“ ÃƒÂ«Ã‚Â²Ã‚Â½"

# Add scene
/writer-memory scene add "ÃƒÂ¬Ã‹Å“Ã‚Â¥ÃƒÂ¬Ã†â€™Ã‚Â ÃƒÂ¬Ã…Â¾Ã‚Â¬ÃƒÂ­Ã…Â¡Ã…â€™"

# Query for writing
/writer-memory query "ÃƒÂ¬Ã†â€™Ã‹â€ ÃƒÂ«Ã…Â¾Ã¢â‚¬ËœÃƒÂ¬Ã‚ÂÃ¢â€šÂ¬ ÃƒÂ¬Ã‚ÂÃ‚Â´ÃƒÂ«Ã‚Â³Ã¢â‚¬Å¾ ÃƒÂ¬Ã…Â¾Ã‚Â¥ÃƒÂ«Ã‚Â©Ã‚Â´ÃƒÂ¬Ã¢â‚¬â€Ã‚ÂÃƒÂ¬Ã¢â‚¬Å¾Ã…â€œ ÃƒÂ¬Ã¢â‚¬â€œÃ‚Â´ÃƒÂ«Ã¢â‚¬â€œÃ‚Â¤ ÃƒÂ­Ã¢â‚¬Â Ã‚Â¤ÃƒÂ¬Ã…â€œÃ‚Â¼ÃƒÂ«Ã‚Â¡Ã…â€œ ÃƒÂ«Ã‚Â§Ã‚ÂÃƒÂ­Ã¢â‚¬Â¢Ã‚Â ÃƒÂªÃ‚Â¹Ã…â€™?"

# Validate dialogue
/writer-memory validate ÃƒÂ¬Ã†â€™Ã‹â€ ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ "ÃƒÂ­Ã¢â‚¬Â¢Ã‚Â´ÃƒÂ«Ã…Â¾Ã¢â‚¬ËœÃƒÂ¬Ã¢â‚¬Â¢Ã¢â‚¬Å¾, ÃƒÂªÃ‚Â·Ã‚Â¸ÃƒÂ«Ã‚Â§Ã…â€™ÃƒÂ­Ã¢â‚¬Â¢Ã‹Å“ÃƒÂ¬Ã…Â¾Ã‚Â."

# Generate synopsis
/writer-memory synopsis

# Export for reference
/writer-memory export
```

### Quick Character Check

```
/writer-memory char ÃƒÂ¬Ã†â€™Ã‹â€ ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ
```

Output:
```
## ÃƒÂ¬Ã†â€™Ã‹â€ ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ

**Arc (ÃƒÂªÃ‚Â°Ã‚ÂÃƒÂ¬Ã‚Â Ã¢â‚¬Â¢ÃƒÂªÃ‚Â¶Ã‚Â¤ÃƒÂ«Ã‚ÂÃ¢â‚¬Å¾):** ÃƒÂ¬Ã‚Â²Ã‚Â´ÃƒÂ«Ã¢â‚¬Â¦Ã‚Â -> ÃƒÂ¬Ã…Â¡Ã¢â‚¬Â¢ÃƒÂ«Ã‚Â§Ã‚ÂÃƒÂ¬Ã…Â¾Ã‚ÂÃƒÂªÃ‚Â°Ã‚Â -> ÃƒÂ¬Ã¢â‚¬Å¾Ã‚Â ÃƒÂ­Ã†â€™Ã‚Â
**Attitude (ÃƒÂ­Ã†â€™Ã…â€œÃƒÂ«Ã‚ÂÃ¢â‚¬Å¾):** ÃƒÂ«Ã‚Â°Ã‚Â©ÃƒÂ¬Ã¢â‚¬â€œÃ‚Â´ÃƒÂ¬Ã‚Â Ã‚Â, ÃƒÂ­Ã‹Å“Ã¢â‚¬Å¾ÃƒÂ¬Ã¢â‚¬Â¹Ã‚Â¤ÃƒÂ¬Ã‚Â£Ã‚Â¼ÃƒÂ¬Ã‚ÂÃ‹Å“
**Tone (ÃƒÂ«Ã…â€™Ã¢â€šÂ¬ÃƒÂ¬Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ­Ã¢â‚¬Â Ã‚Â¤):** ÃƒÂ«Ã¢â‚¬Â¹Ã‚Â´ÃƒÂ«Ã‚Â°Ã‚Â±, ÃƒÂ­Ã‹Å“Ã¢â‚¬Å¾ÃƒÂ¬Ã…Â¾Ã‚Â¬ÃƒÂ¬Ã‚Â¶Ã‚Â©ÃƒÂ¬Ã¢â‚¬Â¹Ã‚Â¤
**Speech Level (ÃƒÂ«Ã‚Â§Ã‚ÂÃƒÂ­Ã‹â€ Ã‚Â¬):** ÃƒÂ­Ã¢â‚¬Â¢Ã‚Â´ÃƒÂ¬Ã‚Â²Ã‚Â´
**Keywords (ÃƒÂ­Ã¢â‚¬Â¢Ã‚ÂµÃƒÂ¬Ã¢â‚¬Â¹Ã‚Â¬ÃƒÂ¬Ã¢â‚¬â€œÃ‚Â´):** ÃƒÂªÃ‚Â·Ã‚Â¸ÃƒÂ«Ã†â€™Ã‚Â¥, ÃƒÂ«Ã‚Â­Ã‚Â, ÃƒÂªÃ‚Â´Ã…â€œÃƒÂ¬Ã‚Â°Ã‚Â®ÃƒÂ¬Ã¢â‚¬Â¢Ã¢â‚¬Å¾
**Taboo (ÃƒÂªÃ‚Â¸Ã‹â€ ÃƒÂªÃ‚Â¸Ã‚Â°ÃƒÂ¬Ã¢â‚¬â€œÃ‚Â´):** ÃƒÂ¬Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ«Ã…Â¾Ã¢â‚¬ËœÃƒÂ­Ã¢â‚¬Â¢Ã‚Â´, ÃƒÂ«Ã‚Â³Ã‚Â´ÃƒÂªÃ‚Â³Ã‚Â ÃƒÂ¬Ã¢â‚¬Â¹Ã‚Â¶ÃƒÂ¬Ã¢â‚¬â€œÃ‚Â´

**Relationships:**
- ÃƒÂ­Ã¢â‚¬Â¢Ã‚Â´ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ: romantic (intimacy: 6/10, status: healing)

**Scenes Appeared:** ÃƒÂ¬Ã‹Å“Ã‚Â¥ÃƒÂ¬Ã†â€™Ã‚Â ÃƒÂ¬Ã…Â¾Ã‚Â¬ÃƒÂ­Ã…Â¡Ã…â€™, ÃƒÂ¬Ã‚Â¹Ã‚Â´ÃƒÂ­Ã…Â½Ã‹Å“ ÃƒÂ«Ã…â€™Ã¢â€šÂ¬ÃƒÂ­Ã¢â€žÂ¢Ã¢â‚¬Â, ÃƒÂ«Ã‚Â§Ã‹â€ ÃƒÂ¬Ã‚Â§Ã¢â€šÂ¬ÃƒÂ«Ã‚Â§Ã¢â‚¬Â° ÃƒÂ¬Ã¢â‚¬Å¾Ã‚Â ÃƒÂ­Ã†â€™Ã‚Â
```

## Storage Schema

```json
{
  "version": "1.0",
  "project": {
    "name": "ÃƒÂ«Ã‚Â´Ã¢â‚¬Å¾ÃƒÂ¬Ã‚ÂÃ‹Å“ ÃƒÂ«Ã‚ÂÃ‚ÂÃƒÂ¬Ã…Â¾Ã‚ÂÃƒÂ«Ã‚ÂÃ‚Â½",
    "genre": "ÃƒÂ«Ã‚Â¡Ã…â€œÃƒÂ«Ã‚Â§Ã‚Â¨ÃƒÂ¬Ã…Â Ã‚Â¤",
    "created": "2024-01-15T09:00:00Z",
    "lastModified": "2024-01-20T14:30:00Z"
  },
  "characters": {
    "ÃƒÂ¬Ã†â€™Ã‹â€ ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ": {
      "arc": "ÃƒÂ¬Ã‚Â²Ã‚Â´ÃƒÂ«Ã¢â‚¬Â¦Ã‚Â -> ÃƒÂ¬Ã…Â¡Ã¢â‚¬Â¢ÃƒÂ«Ã‚Â§Ã‚ÂÃƒÂ¬Ã…Â¾Ã‚ÂÃƒÂªÃ‚Â°Ã‚Â -> ÃƒÂ¬Ã¢â‚¬Å¾Ã‚Â ÃƒÂ­Ã†â€™Ã‚Â",
      "attitude": "ÃƒÂ«Ã‚Â°Ã‚Â©ÃƒÂ¬Ã¢â‚¬â€œÃ‚Â´ÃƒÂ¬Ã‚Â Ã‚Â, ÃƒÂ­Ã‹Å“Ã¢â‚¬Å¾ÃƒÂ¬Ã¢â‚¬Â¹Ã‚Â¤ÃƒÂ¬Ã‚Â£Ã‚Â¼ÃƒÂ¬Ã‚ÂÃ‹Å“",
      "tone": "ÃƒÂ«Ã¢â‚¬Â¹Ã‚Â´ÃƒÂ«Ã‚Â°Ã‚Â±, ÃƒÂ­Ã‹Å“Ã¢â‚¬Å¾ÃƒÂ¬Ã…Â¾Ã‚Â¬ÃƒÂ¬Ã‚Â¶Ã‚Â©ÃƒÂ¬Ã¢â‚¬Â¹Ã‚Â¤",
      "speechLevel": "ÃƒÂ­Ã¢â‚¬Â¢Ã‚Â´ÃƒÂ¬Ã‚Â²Ã‚Â´",
      "keywords": ["ÃƒÂªÃ‚Â·Ã‚Â¸ÃƒÂ«Ã†â€™Ã‚Â¥", "ÃƒÂ«Ã‚Â­Ã‚Â", "ÃƒÂªÃ‚Â´Ã…â€œÃƒÂ¬Ã‚Â°Ã‚Â®ÃƒÂ¬Ã¢â‚¬Â¢Ã¢â‚¬Å¾"],
      "taboo": ["ÃƒÂ¬Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ«Ã…Â¾Ã¢â‚¬ËœÃƒÂ­Ã¢â‚¬Â¢Ã‚Â´", "ÃƒÂ«Ã‚Â³Ã‚Â´ÃƒÂªÃ‚Â³Ã‚Â ÃƒÂ¬Ã¢â‚¬Â¹Ã‚Â¶ÃƒÂ¬Ã¢â‚¬â€œÃ‚Â´"],
      "emotional_baseline": "ÃƒÂ­Ã‚ÂÃ¢â‚¬Â°ÃƒÂ¬Ã‹Å“Ã‚Â¨ÃƒÂ­Ã¢â‚¬Â¢Ã…â€œ ÃƒÂ«Ã‚Â¬Ã‚Â´ÃƒÂªÃ‚Â´Ã¢â€šÂ¬ÃƒÂ¬Ã¢â‚¬Â¹Ã‚Â¬",
      "triggers": ["ÃƒÂªÃ‚Â³Ã‚Â¼ÃƒÂªÃ‚Â±Ã‚Â° ÃƒÂ¬Ã¢â‚¬â€œÃ‚Â¸ÃƒÂªÃ‚Â¸Ã¢â‚¬Â°", "ÃƒÂ«Ã‚Â¯Ã‚Â¸ÃƒÂ«Ã…Â¾Ã‹Å“ ÃƒÂ¬Ã¢â‚¬Â¢Ã‚Â½ÃƒÂ¬Ã¢â‚¬Â Ã‚Â"]
    }
  },
  "world": {
    "setting": "ÃƒÂ¬Ã¢â‚¬Å¾Ã…â€œÃƒÂ¬Ã…Â¡Ã‚Â¸, ÃƒÂ­Ã‹Å“Ã¢â‚¬Å¾ÃƒÂ«Ã…â€™Ã¢â€šÂ¬, 20ÃƒÂ«Ã…â€™Ã¢â€šÂ¬ ÃƒÂ­Ã¢â‚¬ÂºÃ¢â‚¬Å¾ÃƒÂ«Ã‚Â°Ã‹Å“ ÃƒÂ¬Ã‚Â§Ã‚ÂÃƒÂ¬Ã…Â¾Ã‚Â¥ÃƒÂ¬Ã‚ÂÃ‚Â¸",
    "rules": [],
    "atmosphere": "ÃƒÂ«Ã‚ÂÃ¢â‚¬Å¾ÃƒÂ¬Ã¢â‚¬Â¹Ã…â€œÃƒÂ¬Ã‚ÂÃ‹Å“ ÃƒÂªÃ‚Â±Ã‚Â´ÃƒÂ¬Ã‚Â¡Ã‚Â°ÃƒÂ­Ã¢â‚¬Â¢Ã‚Â¨ ÃƒÂ¬Ã¢â‚¬Â Ã‚Â ÃƒÂ«Ã‚Â¯Ã‚Â¸ÃƒÂ«Ã‚Â¬Ã‹Å“ÃƒÂ­Ã¢â‚¬Â¢Ã…â€œ ÃƒÂ¬Ã‹Å“Ã‚Â¨ÃƒÂªÃ‚Â¸Ã‚Â°",
    "constraints": [],
    "history": ""
  },
  "relationships": [
    {
      "id": "rel_001",
      "from": "ÃƒÂ¬Ã†â€™Ã‹â€ ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ",
      "to": "ÃƒÂ­Ã¢â‚¬Â¢Ã‚Â´ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ",
      "type": "romantic",
      "dynamic": "ÃƒÂ­Ã¢â‚¬Â¢Ã‚Â´ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ ÃƒÂ¬Ã‚Â£Ã‚Â¼ÃƒÂ«Ã‚ÂÃ¢â‚¬Å¾ ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ ÃƒÂªÃ‚Â·Ã‚Â ÃƒÂ­Ã‹Å“Ã¢â‚¬Â¢",
      "speechLevel": "ÃƒÂ«Ã‚Â°Ã‹Å“ÃƒÂ«Ã‚Â§Ã‚Â",
      "evolution": [
        { "timestamp": "...", "change": "ÃƒÂ¬Ã‚Â²Ã‚Â« ÃƒÂ«Ã‚Â§Ã…â€™ÃƒÂ«Ã¢â‚¬Å¡Ã‚Â¨ - ÃƒÂ­Ã¢â‚¬Â¢Ã‚Â´ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ ÃƒÂ¬Ã‚ÂÃ‚Â¼ÃƒÂ«Ã‚Â°Ã‚Â©ÃƒÂ¬Ã‚Â Ã‚Â ÃƒÂ­Ã‹Å“Ã‚Â¸ÃƒÂªÃ‚Â°Ã‚Â", "catalyst": "ÃƒÂ¬Ã…Â¡Ã‚Â°ÃƒÂ¬Ã¢â‚¬â€Ã‚Â°ÃƒÂ­Ã¢â‚¬Â¢Ã…â€œ ÃƒÂ«Ã‚Â§Ã…â€™ÃƒÂ«Ã¢â‚¬Å¡Ã‚Â¨" },
        { "timestamp": "...", "change": "ÃƒÂ¬Ã†â€™Ã‹â€ ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ ÃƒÂªÃ‚Â±Ã‚Â°ÃƒÂ¬Ã‚Â Ã‹â€ ", "catalyst": "ÃƒÂªÃ‚Â³Ã‚Â¼ÃƒÂªÃ‚Â±Ã‚Â° ÃƒÂ­Ã…Â Ã‚Â¸ÃƒÂ«Ã‚ÂÃ‚Â¼ÃƒÂ¬Ã…Â¡Ã‚Â°ÃƒÂ«Ã‚Â§Ã‹â€ " },
        { "timestamp": "...", "change": "ÃƒÂ¬Ã…Â¾Ã‚Â¬ÃƒÂ­Ã…Â¡Ã…â€™ - ÃƒÂ¬Ã†â€™Ã‹â€ ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ ÃƒÂ«Ã¢â‚¬Å¡Ã‚Â´ÃƒÂ¬Ã‚Â Ã‚Â ÃƒÂ«Ã‚ÂÃ¢â€žÂ¢ÃƒÂ¬Ã…Â¡Ã¢â‚¬Â", "catalyst": "ÃƒÂ¬Ã‹Å“Ã‚Â¥ÃƒÂ¬Ã†â€™Ã‚ÂÃƒÂ¬Ã¢â‚¬â€Ã‚ÂÃƒÂ¬Ã¢â‚¬Å¾Ã…â€œ ÃƒÂ¬Ã…Â¾Ã‚Â¬ÃƒÂ­Ã…Â¡Ã…â€™" }
      ],
      "notes": "ÃƒÂ¬Ã†â€™Ã‹â€ ÃƒÂ«Ã…Â¾Ã¢â‚¬ËœÃƒÂ¬Ã‚ÂÃ‹Å“ ÃƒÂ«Ã‚Â¶Ã‹â€ ÃƒÂ¬Ã¢â‚¬Â¹Ã‚Â  vs ÃƒÂ­Ã¢â‚¬Â¢Ã‚Â´ÃƒÂ«Ã…Â¾Ã¢â‚¬ËœÃƒÂ¬Ã‚ÂÃ‹Å“ ÃƒÂªÃ‚Â¸Ã‚Â°ÃƒÂ«Ã¢â‚¬Â¹Ã‚Â¤ÃƒÂ«Ã‚Â¦Ã‚Â¼",
      "created": "..."
    }
  ],
  "scenes": [
    {
      "id": "scene-001",
      "title": "ÃƒÂ¬Ã‹Å“Ã‚Â¥ÃƒÂ¬Ã†â€™Ã‚Â ÃƒÂ¬Ã…Â¾Ã‚Â¬ÃƒÂ­Ã…Â¡Ã…â€™",
      "characters": ["ÃƒÂ¬Ã†â€™Ã‹â€ ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ", "ÃƒÂ­Ã¢â‚¬Â¢Ã‚Â´ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ"],
      "location": "ÃƒÂ­Ã…Â¡Ã…â€™ÃƒÂ¬Ã¢â‚¬Å¡Ã‚Â¬ ÃƒÂ¬Ã‹Å“Ã‚Â¥ÃƒÂ¬Ã†â€™Ã‚Â",
      "cuts": ["ÃƒÂ­Ã¢â‚¬Â¢Ã‚Â´ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ ÃƒÂ«Ã‚Â¨Ã‚Â¼ÃƒÂ¬Ã‚Â Ã¢â€šÂ¬ ÃƒÂ«Ã‚Â°Ã…â€œÃƒÂªÃ‚Â²Ã‚Â¬", "ÃƒÂ¬Ã†â€™Ã‹â€ ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ ÃƒÂªÃ‚ÂµÃ‚Â³ÃƒÂ¬Ã‚ÂÃ¢â€šÂ¬ ÃƒÂ­Ã¢â‚¬ËœÃ…â€œÃƒÂ¬Ã‚Â Ã¢â‚¬Â¢", "ÃƒÂ¬Ã‚Â¹Ã‚Â¨ÃƒÂ«Ã‚Â¬Ã‚Âµ", "ÃƒÂ­Ã¢â‚¬Â¢Ã‚Â´ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ ÃƒÂ«Ã‚Â¨Ã‚Â¼ÃƒÂ¬Ã‚Â Ã¢â€šÂ¬ ÃƒÂ«Ã‚Â§Ã‚Â ÃƒÂªÃ‚Â±Ã‚Â¸ÃƒÂªÃ‚Â¸Ã‚Â°"],
      "narration_tone": "ÃƒÂªÃ‚Â±Ã‚Â´ÃƒÂ¬Ã‚Â¡Ã‚Â°ÃƒÂ¬Ã‚Â²Ã‚Â´",
      "emotional_tag": "ÃƒÂªÃ‚Â¸Ã‚Â´ÃƒÂ¬Ã…Â¾Ã‚Â¥+ÃƒÂªÃ‚Â·Ã‚Â¸ÃƒÂ«Ã‚Â¦Ã‚Â¬ÃƒÂ¬Ã¢â‚¬ÂºÃ¢â€šÂ¬",
      "purpose": "ÃƒÂ¬Ã…Â¾Ã‚Â¬ÃƒÂ­Ã…Â¡Ã…â€™ÃƒÂ¬Ã‚ÂÃ‹Å“ ÃƒÂ¬Ã¢â‚¬â€œÃ‚Â´ÃƒÂ¬Ã†â€™Ã¢â‚¬Â°ÃƒÂ­Ã¢â‚¬Â¢Ã‚Â¨ÃƒÂªÃ‚Â³Ã‚Â¼ ÃƒÂ«Ã¢â‚¬Å¡Ã‚Â¨ÃƒÂ¬Ã‚ÂÃ¢â€šÂ¬ ÃƒÂªÃ‚Â°Ã‚ÂÃƒÂ¬Ã‚Â Ã¢â‚¬Â¢ ÃƒÂ¬Ã¢â‚¬Â¢Ã¢â‚¬ÂÃƒÂ¬Ã¢â‚¬Â¹Ã…â€œ",
      "before_after": "ÃƒÂ¬Ã†â€™Ã‹â€ ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ: ÃƒÂ«Ã‚Â¬Ã‚Â´ÃƒÂªÃ‚Â´Ã¢â€šÂ¬ÃƒÂ¬Ã¢â‚¬Â¹Ã‚Â¬ -> ÃƒÂ«Ã‚ÂÃ¢â€žÂ¢ÃƒÂ¬Ã…Â¡Ã¢â‚¬Â"
    }
  ],
  "themes": [
    {
      "name": "ÃƒÂ­Ã‚ÂÃ‚Â¬ÃƒÂªÃ‚Â¸Ã‚Â°ÃƒÂ­Ã¢â‚¬Â¢Ã‹Å“ÃƒÂ¬Ã‚Â§Ã¢â€šÂ¬ ÃƒÂ¬Ã¢â‚¬Â¢Ã…Â ÃƒÂ«Ã…Â Ã¢â‚¬Â ÃƒÂ¬Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ",
      "expression": "ÃƒÂ­Ã¢â‚¬Â¢Ã‚Â´ÃƒÂ«Ã…Â¾Ã¢â‚¬ËœÃƒÂ¬Ã‚ÂÃ‹Å“ ÃƒÂ¬Ã‚ÂÃ‚Â¼ÃƒÂªÃ‚Â´Ã¢â€šÂ¬ÃƒÂ«Ã‚ÂÃ…â€œ ÃƒÂ­Ã†â€™Ã…â€œÃƒÂ«Ã‚ÂÃ¢â‚¬Å¾",
      "scenes": ["ÃƒÂ¬Ã‹Å“Ã‚Â¥ÃƒÂ¬Ã†â€™Ã‚Â ÃƒÂ¬Ã…Â¾Ã‚Â¬ÃƒÂ­Ã…Â¡Ã…â€™", "ÃƒÂ«Ã‚Â§Ã‹â€ ÃƒÂ¬Ã‚Â§Ã¢â€šÂ¬ÃƒÂ«Ã‚Â§Ã¢â‚¬Â° ÃƒÂªÃ‚Â³Ã‚Â ÃƒÂ«Ã‚Â°Ã‚Â±"],
      "character_links": ["ÃƒÂ­Ã¢â‚¬Â¢Ã‚Â´ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ"],
      "author_intent": "ÃƒÂ¬Ã‚Â§Ã¢â‚¬ËœÃƒÂ¬Ã‚Â°Ã‚Â©ÃƒÂ¬Ã‚ÂÃ‚Â´ ÃƒÂ¬Ã¢â‚¬Â¢Ã¢â‚¬Å¾ÃƒÂ«Ã¢â‚¬Â¹Ã…â€™ ÃƒÂ«Ã‚Â¯Ã‚Â¿ÃƒÂ¬Ã‚ÂÃ…â€™ÃƒÂ¬Ã‚ÂÃ‹Å“ ÃƒÂ¬Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ«Ã…Â¾Ã¢â‚¬Ëœ"
    }
  ],
  "synopsis": {
    "protagonist_attitude": "ÃƒÂ¬Ã†â€™Ã‹â€ ÃƒÂ«Ã…Â¾Ã¢â‚¬ËœÃƒÂ¬Ã‚ÂÃ¢â€šÂ¬ ÃƒÂ¬Ã†â€™Ã‚ÂÃƒÂ¬Ã¢â‚¬Â¹Ã‚Â¤ÃƒÂ¬Ã‚ÂÃ¢â‚¬Å¾ ÃƒÂ¬Ã‹Å“Ã‹â€ ÃƒÂ«Ã‚Â°Ã‚Â©ÃƒÂ­Ã¢â‚¬Â¢Ã‹Å“ÃƒÂªÃ‚Â¸Ã‚Â° ÃƒÂ¬Ã…â€œÃ¢â‚¬Å¾ÃƒÂ­Ã¢â‚¬Â¢Ã‚Â´ ÃƒÂ«Ã‚Â¨Ã‚Â¼ÃƒÂ¬Ã‚Â Ã¢â€šÂ¬ ÃƒÂ­Ã‚ÂÃ‚Â¬ÃƒÂªÃ‚Â¸Ã‚Â°ÃƒÂ­Ã¢â‚¬Â¢Ã‹Å“ÃƒÂ«Ã…Â Ã¢â‚¬Â ÃƒÂ¬Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ«Ã…Â¾Ã…â€™",
    "relationship_structure": "ÃƒÂªÃ‚Â¸Ã‚Â°ÃƒÂ«Ã¢â‚¬Â¹Ã‚Â¤ÃƒÂ«Ã‚Â¦Ã‚Â¬ÃƒÂ«Ã…Â Ã¢â‚¬Â ÃƒÂ¬Ã…Â¾Ã‚ÂÃƒÂ¬Ã¢â€žÂ¢Ã¢â€šÂ¬ ÃƒÂ«Ã‚ÂÃ¢â‚¬Å¾ÃƒÂ«Ã‚Â§Ã‚ÂÃƒÂ¬Ã‚Â¹Ã‹Å“ÃƒÂ«Ã…Â Ã¢â‚¬Â ÃƒÂ¬Ã…Â¾Ã‚ÂÃƒÂ¬Ã‚ÂÃ‹Å“ ÃƒÂ¬Ã‚Â¤Ã¢â‚¬Å¾ÃƒÂ«Ã¢â‚¬Â¹Ã‚Â¤ÃƒÂ«Ã‚Â¦Ã‚Â¬ÃƒÂªÃ‚Â¸Ã‚Â°",
    "emotional_theme": "ÃƒÂ¬Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ«Ã…Â¾Ã¢â‚¬ËœÃƒÂ«Ã‚Â°Ã¢â‚¬ÂºÃƒÂ¬Ã‚ÂÃ¢â‚¬Å¾ ÃƒÂ¬Ã…Â¾Ã‚ÂÃƒÂªÃ‚Â²Ã‚Â©ÃƒÂ¬Ã¢â‚¬â€Ã‚Â ÃƒÂ«Ã…â€™Ã¢â€šÂ¬ÃƒÂ­Ã¢â‚¬Â¢Ã…â€œ ÃƒÂ¬Ã‚ÂÃ‹Å“ÃƒÂ¬Ã¢â‚¬Â¹Ã‚Â¬",
    "genre_contrast": "ÃƒÂ«Ã‚Â¡Ã…â€œÃƒÂ«Ã‚Â§Ã‚Â¨ÃƒÂ¬Ã…Â Ã‚Â¤ÃƒÂ¬Ã‚Â§Ã¢â€šÂ¬ÃƒÂ«Ã‚Â§Ã…â€™ ÃƒÂ«Ã‚Â³Ã‚Â¸ÃƒÂ¬Ã‚Â§Ã‹â€ ÃƒÂ¬Ã‚ÂÃ¢â€šÂ¬ ÃƒÂ¬Ã…Â¾Ã‚ÂÃƒÂªÃ‚Â¸Ã‚Â°ÃƒÂ¬Ã‹â€ Ã‹Å“ÃƒÂ¬Ã…Â¡Ã‚Â© ÃƒÂ¬Ã¢â‚¬Å¾Ã…â€œÃƒÂ¬Ã¢â‚¬Å¡Ã‚Â¬",
    "ending_aftertaste": "ÃƒÂ«Ã‚Â¶Ã‹â€ ÃƒÂ¬Ã¢â€žÂ¢Ã¢â‚¬Å¾ÃƒÂ¬Ã‚Â Ã¢â‚¬Å¾ÃƒÂ­Ã¢â‚¬Â¢Ã‹Å“ÃƒÂ¬Ã‚Â§Ã¢â€šÂ¬ÃƒÂ«Ã‚Â§Ã…â€™ ÃƒÂ«Ã¢â‚¬ÂÃ‚Â°ÃƒÂ«Ã…â€œÃ‚Â»ÃƒÂ­Ã¢â‚¬Â¢Ã…â€œ ÃƒÂ¬Ã¢â‚¬Å¾Ã‚Â ÃƒÂ­Ã†â€™Ã‚ÂÃƒÂ¬Ã‚ÂÃ‹Å“ ÃƒÂ¬Ã¢â‚¬â€Ã‚Â¬ÃƒÂ¬Ã…Â¡Ã‚Â´"
  }
}
```

## File Structure

```
.writer-memory/
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ memory.json          # Main memory file
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ backups/             # Auto-backups before changes
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ memory-2024-01-15-090000.json
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ memory-2024-01-20-143000.json
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ exports/             # Markdown exports
    ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ export-2024-01-20.md
```

## Tips for Writers

1. **Start with Characters**: Build character memories before scenes
2. **Update Relationships After Key Scenes**: Track evolution actively
3. **Use Validation While Writing**: Catch voice inconsistencies early
4. **Query Before Difficult Scenes**: Let the system remind you of context
5. **Regular Synopsis**: Generate periodically to check thematic coherence
6. **Backup Before Major Changes**: Use `/backup` before significant story pivots

## Troubleshooting

**Memory not loading?**
- Check `.writer-memory/memory.json` exists
- Verify JSON syntax is valid
- Run `/writer-memory status` to diagnose

**Validation too strict?**
- Review taboo list for unintended entries
- Consider if character is growing (arc progression)
- Intentional breaks from pattern are valid for dramatic moments

**Query not finding context?**
- Ensure relevant data is in memory
- Try more specific queries
- Check character names match exactly
