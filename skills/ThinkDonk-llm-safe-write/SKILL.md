---
name: ThinkDonk-llm-safe-write
description: "Use this skill when:"
---
## When to use me

Use this skill when:
- You need to write a file that is **longer than 50 lines**
- The file contains **CJK characters** (Chinese, Japanese, Korean) or special escape sequences
- A previous **Write tool call failed** with `Unterminated string` or JSON truncation errors
- You are about to write a Python/JS/TS file with more than a few functions
- You need to embed **CJK strings** in source code

Do NOT use this skill when:
- The file is short (< 50 lines) and ASCII-only ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â just use Write directly
- You are making small edits to an existing file ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â just use Edit directly

## Prerequisites: Understanding Write Tool JSON Truncation

The Write tool serializes file content as a JSON string for transport. CJK characters occupy 3-4 bytes each in UTF-8. When a multi-byte character happens to cross an internal buffer boundary, the JSON string gets truncated, causing `Unterminated string` errors. ASCII-only content avoids this because each character is exactly 1 byte.

**Key facts**:
- Truncation is **probabilistic** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â short files and pure ASCII rarely trigger it, but long files or CJK content trigger it frequently
- Bash tool also fails when passing multi-line Python code via PowerShell ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â PowerShell interprets quotes, backticks, curly braces, silently corrupting code
- You may try Write for files under 50 lines, but expect frequent failures above this threshold. For files > 50 lines or containing CJK, go directly to skeleton + Edit. The 50-line threshold is conservative ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â if your environment reliably handles longer ASCII files (e.g., 80 lines), you may adjust upward, but CJK content remains high-risk at any length.
- Truncation happens at the transport layer; it has nothing to do with whether your file content is syntactically valid

> **Scope clarification**: The Read and Edit tools are **not affected by this issue** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Read only reads (never writes), and Edit's `oldString`/`newString` are short strings (< 30 lines each) that never trigger truncation. **Only the Write tool has this limitation.**

## Subagent Dispatch: Same Truncation Applies to Task Tool Arguments

Passing the full target file content as arguments to a subagent-dispatch tool (e.g., `task`) goes through the
same JSON serialization as the Write tool. The task call itself truncates at roughly the same thresholds ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â
a payload over ~150 lines or ~6KB of CJK content fails with the same `Unterminated string` / JSON parse error,
and the subagent never receives the task.

**Rules**:
- Payload ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â¤ 120 lines: single task call, embed the full content in the instructions
- Payload > 120 lines: split into **multiple sequential** task calls (never parallel ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â each append depends on
  the previous chunk having been written), each carrying ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â¤ 120 lines, with explicit instructions like
  "append to the end of the file, do not touch existing content"
- **Empty/aborted task result**: the content may not have been written at all ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â grep or read the target file
  to verify what actually landed before re-dispatching; never blindly re-send the same payload
- Have the subagent report line counts and first/last lines of what it wrote, so the orchestrating agent can
  verify completeness without reading the whole file back

## Routing Priority (First Principles)

> **Evaluate the file first**: if any condition below is met, go directly to skeleton + Edit ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â do NOT try Write first:
>
> - File **> 50 lines** ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ skeleton + Edit
> - Content **contains CJK / special characters** ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ ASCII skeleton + Edit to fill CJK
> - **Write already failed** ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ switch immediately, never retry
>
> Only for files that are **short (< 50 lines) and pure ASCII** may you try Write directly ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â but if it fails, switch immediately.
>
> **Never retry a failed Write with the same content** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â this is the hard constraint of this Skill.

| Scenario | Strategy |
|---|---|
| < 50 lines + pure ASCII | You may try Write directly; for files > 50 lines or with CJK, go directly to skeleton + Edit |
| > 50 lines / contains CJK / Write failed | Skeleton + Edit |
| Small edit to existing file (< 30 lines change) | Edit tool directly |
| Large rewrite of existing file / CJK content | Read file ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Edit in small chunks with unique anchors |

## Strategy

When unsure, try the simpler approach first and fall back to skeleton+Edit if it fails. Never retry a failed Write.

### For new files

**Trigger condition**: Creating a new file expected to be > 50 lines, or containing CJK content.

**Steps**:
1. Construct an ASCII-only skeleton (< 50 lines), replacing all CJK with `PLACEHOLDER_xxx`
2. Use Write to create the skeleton
3. Use Edit to replace each PLACEHOLDER with actual content (< 30 lines per Edit)

**Example ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â writing a 200-line Python file**:

Step 1 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Write the skeleton:
```python
import argparse
import base64
import json

from paddleocr import PaddleOCR
from openai import OpenAI

API_BASE = "PLACEHOLDER_API_BASE"
API_KEY = "PLACEHOLDER_API_KEY"
PROMPT = "PLACEHOLDER_PROMPT"

def get_ocr():
    pass  # PLACEHOLDER_get_ocr

def detect_texts(image_path):
    pass  # PLACEHOLDER_detect_texts

def extract_json(text):
    pass  # PLACEHOLDER_extract_json

def main():
    pass  # PLACEHOLDER_main

if __name__ == "__main__":
    main()
```

Step 2 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Fill each function with Edit (one at a time):
```
Edit(filePath="/path/to/file.py",
     oldString="pass  # PLACEHOLDER_get_ocr",
     newString="ocr = PaddleOCR(use_angle_cls=True, lang='ch')\n    return ocr")

Edit(filePath="/path/to/file.py",
     oldString="pass  # PLACEHOLDER_detect_texts",
     newString="result = ocr.ocr(image_path, cls=True)\n    return result")
```

### For existing files

**Trigger condition**: Modifying an existing file that is already large or contains CJK.

1. **Always use Edit tool** for modifications. Never use Write to overwrite an existing large file.
2. If adding a large block, use Edit to replace a known marker/placeholder with the new content.
3. Break large edits into multiple smaller Edit calls.

### Appending content to existing files

**Trigger condition**: Need to add content at the end of an existing file.

The Edit tool can only replace, not append. To add content at the end of a file:
1. **Use the last line as an anchor** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â include it in `oldString`, then repeat it in `newString` after the new content.
2. Example: to add a new function before `if __name__ == "__main__":`, use that line as the anchor and replace it with `new_function_code\n\nif __name__ == "__main__":`.
3. **Always read the file first** to get the exact last-line content for a precise match.
4. When no stable anchor exists at file end, write a temporary marker line (e.g., `# END_OF_FILE`) via Edit, use it as anchor for subsequent appends, then remove it with a final Edit. ÃƒÂ¢Ã…Â¡Ã‚Â ÃƒÂ¯Ã‚Â¸Ã‚Â Prefer stable anchors (like `if __name__ == "__main__":`) whenever available ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â if the agent is interrupted before the final cleanup Edit, the marker will remain in the file as residue.

### For files with CJK content

**Trigger condition**: File content includes Chinese, Japanese, Korean, or other non-ASCII characters.

1. **Write skeleton with ASCII placeholders** for all CJK strings.
2. **Use Edit to insert CJK text** into the placeholders. Short CJK strings in Edit oldString/newString pairs work reliably.
3. Alternative: use Python unicode escape in source (e.g., `"\u8bc6\u522b"` instead of `"ÃƒÂ¨Ã‚Â¯Ã¢â‚¬Â ÃƒÂ¥Ã‹â€ Ã‚Â«"`) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â this keeps the file ASCII-safe but less readable.

**Example ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Python file with Chinese prompts**:

Step 1 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Skeleton with placeholders:
```python
PROMPT_SYSTEM = "PLACEHOLDER_prompt_system"
PROMPT_USER = "PLACEHOLDER_prompt_user"
ERROR_MSG = "PLACEHOLDER_error_msg"
```

Step 2 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Fill with Edit:
```
Edit(filePath="/path/to/file.py",
     oldString='PROMPT_SYSTEM = "PLACEHOLDER_prompt_system"',
     newString='PROMPT_SYSTEM = "ÃƒÂ¤Ã‚Â½Ã‚Â ÃƒÂ¦Ã‹Å“Ã‚Â¯ÃƒÂ¤Ã‚Â¸Ã¢â€šÂ¬ÃƒÂ¤Ã‚Â¸Ã‚ÂªÃƒÂ¤Ã‚Â¸Ã¢â‚¬Å“ÃƒÂ¤Ã‚Â¸Ã…Â¡ÃƒÂ§Ã…Â¡Ã¢â‚¬Å¾AIÃƒÂ¥Ã…Â Ã‚Â©ÃƒÂ¦Ã¢â‚¬Â°Ã¢â‚¬Â¹ÃƒÂ¯Ã‚Â¼Ã…â€™ÃƒÂ¨Ã‚Â¯Ã‚Â·ÃƒÂ§Ã¢â‚¬ÂÃ‚Â¨ÃƒÂ¤Ã‚Â¸Ã‚Â­ÃƒÂ¦Ã¢â‚¬â€œÃ¢â‚¬Â¡ÃƒÂ¥Ã¢â‚¬ÂºÃ…Â¾ÃƒÂ§Ã‚Â­Ã¢â‚¬ÂÃƒÂ©Ã¢â‚¬â€Ã‚Â®ÃƒÂ©Ã‚Â¢Ã‹Å“"')
```

### For non-code files (JSON, YAML, Markdown, etc.)

**Trigger condition**: Writing config/data files that lack code-style comment placeholders.

These files lack code-style comment placeholders. Strategy:
1. **JSON**: Write the full structure with ASCII placeholder strings, then Edit to replace them with CJK values. Ensure the skeleton is valid JSON (all keys present, placeholder values) so the file remains parseable between edits. For non-string fields (numbers, booleans, null), use a same-type placeholder (e.g., `0`, `false`, `null`) rather than a string ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â a string placeholder like `"PLACEHOLDER"` would break JSON type validity. Edit the field afterward with a short Edit call to replace the placeholder with the real value, or use a two-step Edit: first replace with a string, then fix the type.
2. **YAML**: Use `# PLACEHOLDER_key_name` comments as anchors on the line above the value to replace.
3. **Markdown**: Write section headers first as skeleton, then Edit to fill body content under each header.

### Skeleton structure template

A good skeleton should include:
1. **All imports** at the top (these rarely change)
2. **Constants and config** (with ASCII placeholders for CJK values)
3. **Function signatures with unique placeholder comments** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â one line per function, preserving correct indentation. **Never use bare `pass`** as multiple `pass` statements cause Edit tool `Found multiple matches` errors.
4. **A `main()` or entry point** at the bottom

For classes, use `# PLACEHOLDER_ClassName_method_name` format to ensure uniqueness across methods:

```python
class MyHandler:
    def __init__(self):
        pass  # PLACEHOLDER_MyHandler_init

    def process(self, data):
        pass  # PLACEHOLDER_MyHandler_process
```

For JS/TS, use `// PLACEHOLDER_funcName` comments instead.

### Edit failure recovery

If an Edit call fails with `oldString not found`:
1. **Read the file again** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the content may have changed from a previous edit
2. **Check whitespace** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â tabs vs spaces, trailing newlines, or line endings
3. **Use a shorter oldString** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â pick a smaller, unique substring to match
4. **Avoid partial-line matches** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â include the full line or use exact indentation

If an Edit call fails with `Found multiple matches`:
1. **Add more surrounding context** to make the oldString unique
2. **Or use `replaceAll: true`** if you genuinely want to replace every occurrence (e.g., renaming a variable)

## Common Error Handling

| Error | Cause | Fix |
|---|---|---|
| `Unterminated string` | Write content contains CJK or is too long; JSON truncated | Switch to skeleton + Edit immediately; do not retry Write |
| `oldString not found` | File content doesn't match oldString (stale after prior edit, whitespace differences) | Re-Read the file; construct oldString from actual content |
| `Found multiple matches` | oldString appears multiple times (e.g., bare `pass`) | Add more surrounding context to make oldString unique; or use `replaceAll: true` |
| `File not found` | Parent directory doesn't exist for new file | Create directory first with `mkdir -p`, then Write |
| Write succeeds but Read shows incomplete content | JSON truncation at end of file ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Write didn't error but content was cut off | Use Edit to fill in missing parts, or rewrite with skeleton + Edit |
| PowerShell corrupts multi-line code | PowerShell interprets quotes/backticks/curly braces in strings | Write code to a .py/.js file first, then execute the file |

## Hard Rules & Anti-patterns

### Hard Rules

1. **Never retry a failed Write** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the root cause is length/encoding; retrying wastes tokens and may leave a corrupt file. Switch to skeleton + Edit immediately.
2. **Never pass multi-line code through Bash/PowerShell** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â PowerShell interprets quotes, backticks, curly braces, silently corrupting code. Write to a .py/.js file first, then execute the file.
3. **Each Edit must change < 30 lines** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â split larger changes across multiple Edit calls.
4. **Always use unique placeholder comments** (e.g., `pass  # PLACEHOLDER_func_name`) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â bare `pass` triggers `Found multiple matches` on every subsequent Edit.
5. **Always Read the file before Edit on existing files** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â stale oldString causes `oldString not found`.
6. **Subagent dispatch payloads follow the same limits** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â embedding >120 lines (or ~6KB of CJK) in a single task call truncates the call's JSON arguments; split into sequential subagent calls and verify empty results before re-sending.

### Anti-patterns

- **Embedding CJK in Write content** ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ CJK becomes 3-4 byte UTF-8; crossing buffer boundaries truncates the JSON string, failing the entire Write
- **Using `python -c "..."` with multi-line code in PowerShell** ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ same string handling issues; code gets mangled before execution
- **Appending via Write to an existing large file** ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Write sends the full content through JSON again, risking truncation on the entire file
- **Write succeeds but Read shows incomplete content** ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ silent truncation at end of file; always spot-check after Write

## Post-write Behavior

After completing all file writes/edits:

- **Spot-check the file** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â use Read to verify the first 10 lines and last 5 lines; confirm key structure is intact
- **Report concisely** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â tell the user: "Written to `file.py` (120 lines, verified)" ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â no more detail needed
- **Do not output the full file content or large diffs** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the user doesn't need to see it
- **Do not expose tool call internals** (e.g., "Edit oldString='pass  # PLACEHOLDER_parse'") ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â this is infrastructure, not user-facing information
- **Do not say "edit successful" after every single Edit** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â confirm once after all edits are complete
