---
name: test-fix-loop
description: "1. Run the narrowest relevant test. 2. Read the exact failure and stack trace. 3. Map the failure to the owning code path. 4. Fix one root cause at a time. 5. Re-run the narrow test before expanding scope."
---
## When to use
- Tests are failing and the cause is not yet confirmed.

## Procedure
1. Run the narrowest relevant test.
2. Read the exact failure and stack trace.
3. Map the failure to the owning code path.
4. Fix one root cause at a time.
5. Re-run the narrow test before expanding scope.

## Rules
- Do not change multiple unrelated things at once.
- Prefer local fixes over broad rewrites.
