# Butterup Integration Guide

## Contents

- [Choose a loading pattern](#choose-a-loading-pattern)
- [Wire notification calls](#wire-notification-calls)
- [Replace existing UI safely](#replace-existing-ui-safely)
- [Use the API](#use-the-api)
- [Troubleshoot](#troubleshoot)
- [Source and credit](#source-and-credit)

## Choose a loading pattern

Copy `butterup.js` and `butterup.css` from the Skill's `assets/` directory into a project-owned location. Keep the two files together when practical.

### Bundler-managed frontend

Use this pattern for Vite, Webpack, Parcel, and bundlers that support CSS imports:

```js
import butterup from './vendor/butterup/butterup.js'
import './vendor/butterup/butterup.css'
```

Load the CSS once from the global application entry. Import the JavaScript wherever the notification calls are centralized, or directly at a small number of call sites.

### Vanilla HTML with ES modules

```html
<link rel="stylesheet" href="/vendor/butterup/butterup.css">

<script type="module">
  import butterup from '/vendor/butterup/butterup.js'

  document.querySelector('#save').addEventListener('click', () => {
    butterup.toast({
      title: 'Saved successfully',
      type: 'success',
      icon: true,
    })
  })
</script>
```

Do not load the bundled JavaScript as a classic `<script>` because it uses an ES module default export.

### React and Vue

Import the CSS once from the application's global client entry. Import `butterup` into the component, composable, hook, or notification service that owns the browser event.

Call Butterup from event handlers or client lifecycle code, not during render:

```js
async function handleSave() {
  await saveChanges()
  butterup.toast({
    title: 'Changes saved',
    type: 'success',
    icon: true,
    duration: 2500,
  })
}
```

### SSR frameworks

Place notification calls behind a client boundary. In Next.js App Router, call Butterup from a Client Component event handler. In other SSR systems, ensure calls only run when `document` is available. The module can be imported without creating DOM nodes; `toast()` itself requires a browser document and body.

### CSS-as-string pipelines

The source Bangumi userscript uses `rollup-plugin-import-css`, which returns CSS as a string, then injects it:

```js
import butterupStyles from './butterup.css'

const style = document.createElement('style')
style.textContent = butterupStyles
document.head.append(style)
```

Use this only when the project's CSS loader deliberately exports text. Prefer a normal CSS import or `<link>` in conventional applications.

## Wire notification calls

### Basic status notification

```js
butterup.toast({
  title: 'Copied to clipboard',
  location: 'top-right',
  dismissable: false,
  type: 'success',
  duration: 2500,
  icon: true,
})
```

### Title and supporting message

```js
butterup.toast({
  title: 'Upload failed',
  message: 'Try again after checking your connection.',
  type: 'error',
  icon: true,
  dismissable: true,
})
```

### Action buttons

```js
butterup.toast({
  title: 'Draft archived',
  type: 'info',
  icon: true,
  primaryButton: {
    text: 'Undo',
    onClick: () => restoreDraft(),
  },
  secondaryButton: {
    text: 'View archive',
    onClick: () => openArchive(),
  },
})
```

### Promise state

```js
await butterup.promise({
  promise: saveChanges(),
  loadingMessage: 'Saving changes...',
  successMessage: 'Changes saved',
  errorMessage: 'Could not save changes',
  location: 'top-right',
  theme: 'glass',
})
```

The returned Promise preserves the original result and rethrows the original rejection.

## Replace existing UI safely

Good candidates:

- `alert('Copied')` after a successful clipboard write
- transient save, upload, sync, or submit results
- non-blocking API success or failure feedback
- temporary custom notification banners that require no decision

Do not replace:

- `confirm(...)` or `prompt(...)`
- destructive action confirmation
- dialogs containing forms or authentication
- validation placed next to the invalid field
- persistent outage, billing, legal, or security notices
- modals whose close action advances or cancels a workflow

When replacing an `alert`, preserve the control flow. An alert blocks JavaScript until dismissed; a toast does not. If later statements depend on that pause, restructure only with user approval.

## Use the API

### `butterup.toast(options)`

| Option | Meaning |
| --- | --- |
| `title` | Main toast content. Inserted as HTML by this fork. |
| `message` | Supporting content. Inserted as HTML by this fork. |
| `type` | Visual type: `success`, `error`, `warning`, or `info`. |
| `location` | `top-right`, `top-center`, `top-left`, `bottom-right`, `bottom-center`, or `bottom-left`. Defaults to `top-right`. |
| `icon` | Show the built-in type icon or the supplied custom icon. |
| `theme` | Optional `glass` or `brutalist` theme class. |
| `customIcon` | Custom icon markup. Inserted as HTML. |
| `dismissable` | Allow clicking the toast to dismiss it. |
| `onClick` | Run a callback when the toast is clicked. |
| `onRender` | Run a callback with the created toast element. |
| `onTimeout` | Run a callback with the toast element when its lifetime expires. |
| `customHTML` | Additional message markup. Inserted as HTML. |
| `primaryButton` | `{ text, onClick }` action button. |
| `secondaryButton` | `{ text, onClick }` secondary action button. |
| `maxToasts` | Set the maximum simultaneous toast count. |
| `duration` | Set the toast lifetime in milliseconds. |

The fork also exposes:

- `butterup.despawnToast(toastId, onClosed)`
- `butterup.promise({ promise, loadingMessage, successMessage, errorMessage, location, theme })`

### Content safety

Treat `title`, `message`, `customHTML`, and `customIcon` as HTML sinks. Use only fixed application-controlled markup or content processed by a sanitizer already approved by the host project. Do not interpolate raw query parameters, user profiles, API error bodies, uploaded content, or other untrusted strings.

## Troubleshoot

- No styling: verify `butterup.css` is loaded exactly once and is not being treated as a CSS module.
- `Unexpected token 'export'`: load `butterup.js` through a bundler import or `<script type="module">`.
- `document is not defined`: move the call to a browser-only event or client lifecycle boundary.
- Toast appears behind UI: inspect the host stacking contexts; the toaster itself uses a high `z-index`.
- Host element collision: the unmodified fork uses `#toaster` and `#butterupRack`. Report the conflict instead of silently changing the bundled asset.
- Dynamic content is required: use an approved sanitizer or choose a notification component that renders text safely.

## Source and credit

The bundled files are copied unchanged from the Butterup fork used by `bangumi-plugin-boilerplate`, which identifies the original project as [dgtlss/butterup](https://github.com/dgtlss/butterup). The original project states that Butterup is distributed under the MIT License.
