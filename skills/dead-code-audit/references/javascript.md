# Dead code detection: JavaScript / TypeScript

## Primary tool: knip

Knip is the most complete option: finds unused files, unused exports, unused
dependencies, and unused class members in one run. It understands most frameworks
(Next.js, Remix, Astro, workspaces/monorepos) via built-in plugins.

```bash
npm install -D knip
npx knip                       # full report
npx knip --include files       # only orphaned files (fastest big win)
npx knip --production          # stricter: dev-only usage doesn't count
```

Monorepos: knip reads workspace config automatically; run it at the repo root.
If it misidentifies entry points, add a `knip.json`:

```json
{ "entry": ["src/index.ts", "src/cli.ts"], "project": ["src/**/*.ts"] }
```

Getting entry points right is the single most important knob. Wrong entries make
half the repo look dead.

## TypeScript-only alternatives

```bash
npx ts-prune                   # unused exports (noisy on re-exports, fast)
npx tsc --noUnusedLocals --noUnusedParameters --noEmit   # compiler-level check
```

## Unused dependencies

```bash
npx depcheck                   # if knip unavailable; otherwise knip covers it
```

## JS/TS-specific false-positive traps

Tier 2 or 3, never Tier 1 without verification:

- **Dynamic imports**: `import(variable)`, `require(path + name)`. Grep for
  `import(` and `require(` with non-literal arguments near the candidate.
- **Framework file conventions**: Next.js `pages/`/`app/` routes, config files
  (`*.config.js`), Storybook stories, test setup files. Nothing imports them; the
  framework loads them by path.
- **Barrel files** (`index.ts` re-exports): an export can be "unused" internally
  but be the published package surface. Check `package.json` `exports`/`main`.
- **JSX component usage**: `<MyComponent />` references `MyComponent`; make sure
  the tool run included `.jsx`/`.tsx` parsing before trusting a "unused" flag.
- **Window/global assignments**: `window.foo = foo` means external scripts may
  call it.
- **String-keyed dispatch**: event names, redux action types, template strings in
  Angular/Vue templates. Grep the symbol as a string.
- **Type-only usage**: a type may only appear in `.d.ts` files or JSDoc comments.
