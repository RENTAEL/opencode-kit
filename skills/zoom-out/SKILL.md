---
name: zoom-out
description: "One prompt. One map. Re-orient fast."
---
# /supergraph:zoom-out

One prompt. One map. Re-orient fast.

Announce: "ÃƒÂ°Ã…Â¸Ã¢â‚¬ÂÃ‚Â­ /supergraph:zoom-out ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â stepping back..."

## Steps

**1. Read CONTEXT.md for domain vocabulary (if exists):**
```bash
head -60 CONTEXT.md 2>/dev/null
```

**2. Get architecture overview:**
Use codebase-memory-mcp with `CBM_PROJECT`: call `get_architecture` for
`overview`, `layers`, `boundaries`, `clusters`, and `hotspots`; then use named
contract recipes `hubs`, `bridges`, and `test-gaps`. If unavailable, label it
`unavailable` and fall back to Serena/filesystem evidence.

**3. Output module map** using domain vocabulary from CONTEXT.md:

```
[Project name] ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â module map

[Community/Module A]
  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ [file/symbol] ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [one-line role in domain terms]
  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ [file/symbol] ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â [one-line role]

[Community/Module B]
  ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ ...

Key flows:
  [User action] ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ [Module A] ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ [Module B] ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ [output]

Hub nodes (high-change risk): [list]
Bridge nodes (coupling chokepoints): [list]
```

No implementation details. Domain language only. If a concept doesn't have a name in CONTEXT.md ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â use the most natural domain term and suggest adding it.

## Rules

- Use domain vocabulary, not file/class names (prefer "payment processing" over "PaymentService.ts")
- If CONTEXT.md is missing or empty ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â use the most natural terms you can infer and note at bottom: "CONTEXT.md missing ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â terms inferred"
- No action items, no recommendations ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â orientation only
- Follow with: "Ready to /supergraph:plan, /supergraph:analyze, or /supergraph:architecture?"
