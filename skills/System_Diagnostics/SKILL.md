---
name: System_Diagnostics
description: "Use this skill for short local diagnostics that do not need OpenCode."
---
# System Diagnostics

Use this skill for short local diagnostics that do not need OpenCode.

## Main command

```powershell
powershell -File ".\skills\System_Diagnostics\Get-SystemSnapshot.ps1"
```

## Useful variants

Include top processes:

```powershell
powershell -File ".\skills\System_Diagnostics\Get-SystemSnapshot.ps1" -IncludeProcesses
```

Include listening ports too:

```powershell
powershell -File ".\skills\System_Diagnostics\Get-SystemSnapshot.ps1" -IncludeProcesses -IncludePorts
```

## Notes

- The output is JSON so the orchestrator can summarize it safely.
- Prefer this for local inspection. Escalate to OpenCode only if the issue requires a multi-step investigation or remediation.
