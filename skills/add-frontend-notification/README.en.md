# Frontend Notification Integration / add-frontend-notification

---

## Introduction

This Skill integrates lightweight Butterup toast notifications into frontend or fullstack projects, creating non-blocking Toasters wherever browser-side logic needs user feedback.

**Feature Overview**

Use it to integrate Butterup into interactions that need notifications, such as successful saves, completed clipboard actions, or failed requests. When the scenario is explicit, the Skill implements the integration directly; when it is unclear, it provides project-specific instructions and code snippets.

**Core Value**

- Detects the project's frontend structure and styling pipeline to choose a suitable integration method.
- Replaces simple native prompts or hand-built notifications with Butterup Toasts when behavior and intent are clearly equivalent.
- Keeps the decision to modify the project with the user and does not subjectively replace confirmations, inputs, or business modals with Toasts.

**Who It's For**

- `💻` Frontend developers — quickly add consistent success, error, warning, or informational feedback to page interactions.
- `🧩` Fullstack developers — integrate notification assets, styles, and business calls into an existing project.

---

## Features

### Core Features

- Supports browser-facing projects using Vanilla JavaScript, Vite, Webpack, Rollup, React, Vue, Next.js, and similar setups.
- Supports basic Toasts, six locations, success/error/warning/info types, icons, buttons, themes, and Promise-state notifications.
- Modifies the project and completes the integration when the user provides a concrete notification scenario.
- Asks for the target scenario when it is unclear; if it remains undetermined, outputs instructions and copyable code without editing the project.
- Identifies simple `alert` calls or notification-only hand-built modals that can be replaced while preserving interactions that require user decisions or input.

---

## Usage Guide

Describe the project and the exact interaction that needs a notification. More specific context makes direct implementation easier.

### Common Phrases

| Intent | Example Prompt | Result |
| --- | --- | --- |
| Integrate a specific notification | `$add-frontend-notification show a Toast after settings are saved` | Integrates Butterup and adds a notification to the explicit save-success flow |
| Replace a simple native prompt | `$add-frontend-notification replace the alert after copying with a Toast` | Preserves the message and trigger timing while replacing the equivalent non-blocking notification |
| Scan for replaceable prompts | `$add-frontend-notification inspect this frontend and replace suitable simple notifications with Butterup` | Scans existing prompts and changes only scenarios that are clearly notification-only |
| Request guidance only | `$add-frontend-notification explain how to integrate it into this Vue project without changing files` | Outputs project-specific steps and code snippets without writing to the project |
| Explore an unspecified scenario | `$add-frontend-notification I want to use Butterup in this project` | Asks where notifications should appear; if still unclear, provides guidance and examples only |

### Output Example

```js
butterup.toast({
  title: 'Settings saved',
  location: 'top-right',
  dismissable: false,
  type: 'success',
  duration: 2500,
  icon: true,
})
```

---

## Use Cases

| Scenario | Role | Example Prompt | Benefit |
| --- | --- | --- | --- |
| Form save feedback | Frontend developer | `Use Butterup when saving succeeds or fails` | Gives asynchronous operations clear, non-blocking result feedback |
| Clipboard action feedback | Browser extension author | `Replace the post-copy alert with a Toast` | Avoids interrupting the user's flow with a native prompt |
| Unified notifications in an existing project | Fullstack developer | `Scan for simple prompts that can be replaced and integrate Butterup` | Unifies notification styling while preserving business behavior |
| Framework integration reference | Project maintainer | `Show me a Next.js Client Component integration example` | Provides instructions and snippets that fit the current project structure |

---

## Credit

Butterup was created by [dgtlss](https://github.com/dgtlss). Original project: [dgtlss/butterup](https://github.com/dgtlss/butterup).

---
