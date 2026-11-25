---
name: yt-llm-translate
description: "Run the entry script using the full path to the skill's scripts directory. Do not change the current working directory ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â output files should land in the user's workspace, not the skill directory. All workflow steps (download, punctuator, translate) are handled..."
---
Run the entry script using the full path to the skill's scripts directory. Do not change the current working directory ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â output files should land in the user's workspace, not the skill directory.
All workflow steps (download, punctuator, translate) are handled by the scripts.

## Platform-specific Python command

Do NOT simply use `python` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â on Windows this often resolves to the Microsoft Store stub which fails silently. Follow the order below to find a working Python executable:

1. **macOS / Linux**: `python3` (preferred, most reliable)
2. **Windows**:
   - First try `py` (the Python launcher, bypasses Store stub)
   - If that fails, run `where.exe python` to locate the real Python path ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â pick a path NOT under `Microsoft\WindowsApps` (e.g., `C:\Users\<user>\AppData\Local\Python\bin\python.exe`)
   - Use the discovered full path directly in the command

```
py "<path-to-skill>/scripts/entry.py" "<youtube_url>"
```

If `py` is not available:
```
"C:\Users\<user>\AppData\Local\Python\bin\python.exe" "<path-to-skill>/scripts/entry.py" "<youtube_url>"
```
