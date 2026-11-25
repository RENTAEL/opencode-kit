---
name: yolobox-orchestrator
description: "Use this skill for host-side orchestration of yolobox sessions."
---
# Yolobox Orchestrator

Use this skill for host-side orchestration of yolobox sessions.

Do not use it for questions about the current environment from inside a running box. Inside the container, use `yolobox` instead.

1. Start from the user's intent, then choose the smallest `yolobox` command or flag set that accomplishes it.
2. Check `yolobox config` when defaults, merged config, or flag precedence matter.
3. Prefer explicit isolation and safety flags:
   - `--scratch` for disposable or concurrent sessions that must not share `/home/yolo`.
   - `--readonly-project` when the agent only needs read access to the project tree.
   - `--docker` only when the agent needs Docker access or sibling containers.
4. When you need exact command patterns or edge-case reminders, read [references/commands.md](references/commands.md).
5. If you launch a box for another agent, point it at `yolobox` and `YOLOBOX_CONTEXT_FILE` for inside-the-box introspection.
6. When discussing concurrency, distinguish isolated per-run manifests from shared persistent state: manifests are per-run, but `/home/yolo` and `/var/cache` are shared unless `--scratch` is used.