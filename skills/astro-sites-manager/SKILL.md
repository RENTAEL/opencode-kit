---
name: astro-sites-manager
description: "This skill works alongside the **Astro Docs MCP server**. Before answering Astro questions, check if the `astro-docs` MCP tool is available and query it for the latest documentation. The MCP server provides real-time access to docs.astro.build and is the single source of truth..."
---
# Astro Framework ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â v7

## MCP Documentation Access

This skill works alongside the **Astro Docs MCP server**. Before answering Astro questions, check if the `astro-docs` MCP tool is available and query it for the latest documentation. The MCP server provides real-time access to docs.astro.build and is the single source of truth for current APIs.

```
MCP Server: astro-docs
Tool: search_astro_docs
```

If the MCP server is unavailable, fall back to the reference material in this skill and https://docs.astro.build.

---

## Best Practices

### Component Design
- One `.astro` component per file. Keep components small and focused.
- Use frontmatter (`---`) for data fetching and logic; template below for markup only.
- Prefer Astro components over framework components unless client interactivity is needed.
- Use `client:*` directives sparingly ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â each adds JavaScript to the bundle.
- Directive hierarchy: `client:idle` > `client:visible` > `client:load` (prefer lazy).

### Routing & Pages
- Use file-based routing in `src/pages/`. Dynamic routes: `[slug].astro`, `[...path].astro`.
- Always export `getStaticPaths()` for prerendered dynamic routes.
- For SSR pages: `export const prerender = false` at the top.
- Use `src/fetch.ts` (v7) only when you need control beyond middleware ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â don't use it for simple auth.

### Content Collections
- Define schemas in `content.config.ts` with Zod ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â never trust untyped content.
- Use `getCollection()` for lists, `getEntry()` for single items.
- Prefer `glob()` loader for local files, custom loaders for CMS data.

### Performance
- Default to static (`prerender = true`). Use SSR only for personalized/dynamic content.
- Use `<Image />` from `astro:assets` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â never raw `<img>` for local images.
- Prefer SÃƒÆ’Ã‚Â¤tteri (default v7) over unified for Markdown ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â it's significantly faster.
- Use Server Islands (`server:defer`) for mixing static shells with dynamic fragments.

### Styling
- Scoped `<style>` in `.astro` files is default and preferred.
- Use `is:global` only when truly needed (third-party component styling).
- Tailwind: install with `astro add tailwind`, don't configure manually.

### TypeScript
- Run `astro sync` after changing content schemas or env variables.
- Run `astro check` before committing ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â catches template type errors other tools miss.
- Use `astro:env/server` and `astro:env/client` for typed env variables (never `process.env` directly).

### Development Workflow
- Use `astro dev` for HMR. Never use `python -m http.server` or other static servers.
- Use `astro add` for official integrations ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â don't manually edit config for them.
- Use `astro build && astro preview` to test production behavior locally.
- In AI agent workflows: use `astro dev --background` and validate via `/_astro/status`.

---

## CLI Commands

```bash
npx astro dev              # Dev server (foreground)
npx astro dev --background # Dev server (detached, for AI agents)
npx astro dev --json       # Dev server with JSON structured logs
npx astro build            # Production build
npx astro preview          # Serve production build locally
npx astro check            # Type checking and diagnostics
npx astro sync             # Generate TypeScript types
npx astro add <integration># Install and configure integration
```

### Background Dev Server (AI Agents)

When working as an AI agent, use background mode:

```bash
# Start (blocks until ready, then detaches)
astro dev --background
# ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Dev server running at http://localhost:4321 (pid 12345)

# Check status
astro dev status

# Read logs
astro dev logs

# Stop
astro dev stop

# Health check endpoint (JSON)
curl http://localhost:4321/_astro/status
# ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ {"ok": true}
```

**Key behaviors:**
- Lockfile prevents duplicate instances ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â starting again returns existing instance
- All commands are idempotent (stop when not running = silent success)
- Auto-detected when running inside an AI agent (no flag needed)
- Opt out: `ASTRO_DEV_BACKGROUND=0 astro dev`

---

## Project Structure

```
src/
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ pages/          # File-based routing (.astro, .md, .mdx)
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ layouts/        # Reusable page layouts
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ components/     # Astro & framework components
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ content/        # Content collections (type-safe)
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ middleware.ts   # Request middleware
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ fetch.ts        # Advanced routing (v7, optional)
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ styles/         # Global CSS
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ assets/         # Optimized assets (images, fonts)
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ actions/        # Server actions
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ env.d.ts        # Environment type declarations
astro.config.mjs    # Main configuration
content.config.ts   # Content collection schemas
tsconfig.json       # TypeScript config
```

---

## Configuration (v7)

```typescript
import { defineConfig, memoryCache, logHandlers } from 'astro/config';

export default defineConfig({
  // Output mode
  output: 'static', // or configure per-page with server adapter

  // Route caching (stable in v7)
  cache: {
    provider: memoryCache(),
  },
  routeRules: {
    '/blog/[...path]': { maxAge: 300, swr: 60 },
  },

  // Logger (stable in v7)
  logger: logHandlers.json(), // or .console(), or .compose(...)

  // Markdown (SÃƒÆ’Ã‚Â¤tteri is default in v7)
  markdown: {
    // No config needed for defaults (GFM, smartypants, heading IDs)
    // For extra features:
    // processor: satteri({ features: { directive: true, math: true } })
  },

  // Advanced routing file (default: src/fetch.ts)
  // fetchFile: null, // disable if src/fetch.ts is used for other purposes

  // Whitespace (v7 default: 'jsx')
  compressHTML: 'jsx', // or true (v6 behavior), or false (preserve all)
});
```

---

## Islands Architecture (client:* directives)

```astro
<!-- Load immediately (interactive above the fold) -->
<Counter client:load />

<!-- Load when browser is idle (non-critical interactivity) -->
<Newsletter client:idle />

<!-- Load when scrolled into viewport (below the fold) -->
<Comments client:visible />

<!-- Load on media query match (mobile-only widget) -->
<MobileMenu client:media="(max-width: 768px)" />

<!-- Client-only, skip SSR entirely (browser APIs needed) -->
<MapWidget client:only="react" />

<!-- Server Island: static shell, fetched at request time (v6+) -->
<UserGreeting server:defer />
```

**Decision guide:** No directive (default) = zero JS, static HTML. Add directive only when user interaction is required.

---

## Image Optimization

```astro
---
import { Image } from 'astro:assets';
import heroImage from '../assets/hero.jpg';
---
<!-- Local image (optimized, lazy-loaded, responsive) -->
<Image src={heroImage} alt="Hero" width={1200} />

<!-- Remote image (must allowlist domain in config) -->
<Image src="https://cdn.example.com/photo.jpg" alt="Photo" width={800} height={600} />
```

Config for remote images:
```typescript
// astro.config.mjs
image: {
  domains: ['cdn.example.com'],
  remotePatterns: [{ protocol: 'https', hostname: '**.cloudinary.com' }],
}
```

---

## Detailed References

- [Install MCP Server](references/install-mcp.md) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Setup Astro Docs MCP for any AI tool (Kiro, Claude, Cursor, VS Code, etc.)
- [Migration Guide v6ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢v7](references/migration-v6-to-v7.md) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Step-by-step upgrade plan with breaking changes checklist
- [Validation Checklist](references/validation-checklist.md) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Verify installation, detect breaking/deprecated patterns
- [AI Dev Server](references/ai-dev-server.md) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Background mode, JSON logging, agent detection
- [Astro v7 Features](references/v7-features.md) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Rust compiler, SÃƒÆ’Ã‚Â¤tteri, Advanced Routing, Route Caching, CDN providers
- [Astro v6 Features](references/v6-features.md) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Content Collections v2, Actions, Sessions, Server Islands, env module
- [Related Content](references/related-content.md) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Vector embeddings para posts relacionados, deploy leve no Coolify sem modelo
- [Testing](references/testing.md) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Vitest components, Playwright E2E, link checking, CI pipeline
- [SEO Full Stack](references/seo-full-stack.md) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â JSON-LD graph, agent discovery, IndexNow, OG images, build-time validation, performance
- [Starlight & Patterns](references/starlight-and-patterns.md) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Docs sites, Pagefind search, i18n, pagination, RSS
- [Deployment](references/deployment.md) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Cloudflare, Vercel, Netlify, Firebase, GitHub Pages, Docker/Coolify, Azure
- [Coolify Deploy](references/coolify-deploy.md) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Self-hosted deploy on Coolify (Dockerfile, API, gotchas, recommended stack)
