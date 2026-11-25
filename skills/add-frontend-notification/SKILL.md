---
name: add-frontend-notification
description: "Integrate the bundled Butterup fork while preserving the user's intended notification behavior."
---
# Add Frontend Notification

Integrate the bundled Butterup fork while preserving the user's intended notification behavior.

## Workflow

1. Inspect the project framework, entry points, styling pipeline, and existing notification code.
2. Determine whether the request identifies a concrete notification scenario.
3. If the scenario is unclear, ask which user action should trigger a notification and whether the user wants implementation or guidance.
4. If the user does not clarify, do not modify application code. Provide a project-specific guide and copyable snippets instead.
5. If the scenario is explicit, select an integration pattern from [references/integration-guide.md](references/integration-guide.md).
6. Copy `assets/butterup.js` and `assets/butterup.css` into an appropriate project-owned directory. Use `scripts/install_butterup.py` when a destination is known.
7. Import both assets once at the application's browser entry point or equivalent global client boundary.
8. Add or replace notification calls only where behavior is clearly equivalent.
9. Run the project's relevant formatter, lint, build, and tests. Verify the toast in a browser when practical.
10. Report the files changed, notification scenarios wired, and any remaining manual steps.

## Decide Whether to Modify Code

Proceed directly when the user names the interaction, target file, component, or notification to integrate. Also proceed when the user explicitly asks to replace existing simple alerts and inspection finds unambiguous fire-and-forget notifications such as saved, copied, submitted, failed, or loaded messages.

Ask for the scenario before editing when the request only says to add Butterup without identifying where notifications should appear. Ask at most the smallest set of questions needed, typically:

- Which user actions or outcomes should display a toast?
- Should existing alerts be replaced, or should only new notification calls be added?
- Is direct implementation wanted, or only an example for the project's framework?

If answers are unavailable, copy nothing and edit nothing. Explain where the two assets would go, show the appropriate imports, and give a representative `butterup.toast(...)` snippet.

## Preserve Behavior

- Replace `alert(...)` only when it communicates non-blocking status and its return timing is irrelevant.
- Do not replace `confirm(...)`, `prompt(...)`, form dialogs, destructive confirmations, authentication gates, or workflow-blocking modals with a toast.
- Do not remove accessible inline validation or persistent error summaries merely because a toast is added.
- Treat custom modals as equivalent only when they contain notification-only content and require no user decision or input.
- Keep message wording, event timing, error handling, and localization conventions consistent with the host project.
- Avoid introducing framework wrappers or state abstractions unless the project already uses that pattern or the user requests it.

## Use the Bundled Fork

Copy the assets without modifying their implementation:

- `assets/butterup.js`
- `assets/butterup.css`

The library creates `#toaster` and `#butterupRack` dynamically on the first `butterup.toast(...)` call. Do not add a static Toaster template unless a concrete host constraint requires one.

Run the copier from the Skill directory after confirming the destination:

```bash
python scripts/install_butterup.py <project-asset-directory>
```

Use `--force` only when the user has authorized replacement of existing copied assets. The script copies assets only; update imports and notification calls in the project separately.

## Apply Safety Boundaries

The bundled fork assigns `title`, `message`, `customHTML`, and `customIcon` through `innerHTML`. Preserve the asset as requested, but never pass untrusted or unsanitized external content into those fields. Prefer fixed application copy or values controlled by the project. If dynamic user/server content is required, explain the risk and request an approved sanitizer or render the dynamic content outside Butterup.

Do not claim that a toast is equivalent to an accessible live region. Preserve or add the host project's established accessibility mechanism when notification content must be announced reliably.

## Use a Basic Toast

```js
butterup.toast({
  title: 'Saved successfully',
  location: 'top-right',
  dismissable: false,
  type: 'success',
  duration: 2500,
  icon: true,
})
```

Read [references/integration-guide.md](references/integration-guide.md) for framework-specific loading patterns, the complete option surface, Promise usage, buttons, themes, and troubleshooting.
