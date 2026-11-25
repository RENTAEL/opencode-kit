---
name: build
description: "Build instructions for the typescript/none project."
---
# Build

Build instructions for the typescript/none project.

## Workflow

1. Install dependencies: `npm install`
2. Build: `npm run build`
3. Verify: Ensure build output exists in the expected output directory

## Common Commands

| Command | Description |
|---------|-------------|
| `npm install` | Install dependencies |
| `npm run build` | Production build |
| `npm run dev` | Development server |
| `npm run build -- --analyze` | Build with bundle analysis |

## Common Issues

- **Type errors during build**: Run `npx tsc --noEmit` first to check types
- **Missing dependencies**: Run `npm install` to sync
- **Build cache issues**: Delete `node_modules/.cache` and retry
