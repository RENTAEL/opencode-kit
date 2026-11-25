---
name: scala
description: "Two hard rules for working in Scala/Java projects, both aimed at the same problem: generic, language-agnostic tool defaults (a cold `sbt` invocation per command, `grep`) are slow or semantically blind compared to Scala-aware tools and usage patterns that already exist in this ..."
---
## What this skill enforces

Two hard rules for working in Scala/Java projects, both aimed at the same problem: generic,
language-agnostic tool defaults (a cold `sbt` invocation per command, `grep`) are slow or
semantically blind compared to Scala-aware tools and usage patterns that already exist in this
environment. Following the generic default "because it's obvious" silently produces slower
feedback loops or missed call sites ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â this skill exists so that doesn't happen by default.

1. **Compile and test through the build tool's own BSP server ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â prefer it over defaulting to
   Bloop.**
2. **Code search/navigation MUST follow this fallback order: scalex ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ ast-grep ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ semantic/LSP tool
   (if available) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ grep.** This order is unconditional ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â it applies even when you already know
   which file to look in.

This skill is agent-agnostic: it names capabilities (a Scala symbol-intelligence CLI, a structural
pattern-matching CLI, an optional semantic/LSP layer) rather than assuming one specific host's
plugin or MCP ecosystem. Use whichever concrete tool your environment provides for each role ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â
see the invocation notes under each tool below for how that resolves in Claude Code specifically.

## Compile and test: prefer the build tool's BSP server over Bloop

Use a long-running `sbt` shell session (or `sbt --client`) for `compile` and `test`. Prefer the
build tool's own BSP server over defaulting to Bloop ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â if your editor/agent integration drives
BSP, point it at sbt's BSP server rather than letting it fall back to Bloop.

**Precondition ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â check before running anything:**

```bash
which sbt
```

If this returns nothing, **stop and report it** rather than guessing at an install path.

## Search and navigate: ordered, unconditional fallback

Before any Scala/Java symbol lookup, usage search, "does this pattern appear elsewhere" check, or
"where is X defined" question ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â **even inside a single file whose location you already know** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â
work through these tools in order. Do not skip ahead to grep or a bare file read on the theory
that a lookup is "too simple" to need them; that shortcut has produced missed call sites before
(Scala's implicits, extension methods, and type hierarchies are exactly the things a plain text
search misses).

### 1. scalex ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â primary

`scalex` is a Scalameta-based Scala/Java code-intelligence CLI (find definition/implementations/
usages/imports/members) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â a real semantic parser, not regex or a generic grammar, and it needs no
compile step or build server. Reach for it first for:

- `scalex def <symbol>` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â find where something is defined
- `scalex impl <trait>` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â find implementations
- `scalex refs <symbol>` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â find all usages, categorized (extended-by, imported-by, used-as-type,
  usage, comment)
- `scalex imports <symbol>` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â dependency/import graph
- `scalex members <symbol>` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â list members of a class/trait/object

**Invocation:** in Claude Code, this is available as the `scalex:scalex` plugin skill ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â load it
for exact syntax (it resolves to a versioned bootstrap script, not a bare `scalex` binary on
PATH). In OpenCode or any other host, use whatever local `scalex` skill/plugin/CLI installation is
configured; if none is installed, say so explicitly rather than silently skipping to ast-grep.

**Do not `which scalex` as a precondition check.** Unlike `sbt`, scalex typically has no bare
PATH binary ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â it's resolved via a plugin/skill bootstrap, so a `which scalex` will often report
"not found" even when scalex is fully available. Treating that as "scalex unavailable, fall
through to ast-grep" is a false negative, not a legitimate fallback trigger. The only reliable
precondition is trying the actual scalex invocation for your host and seeing what happens.

**When scalex won't answer it:** it only indexes top-level declarations in git-tracked
`.scala`/`.java` files. If a symbol is local to a method body, a function parameter, a pattern
binding, in a file with parse errors, or not yet `git add`ed, scalex will report "not found" ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â
that's the signal to fall through to ast-grep, not a dead end.

### 2. ast-grep ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â structural fallback

Use the `ast-grep` skill (or the `sg`/`ast-grep` CLI directly if no skill wrapper exists in your
host) when the question is about a **code shape** rather than a **named symbol** (e.g. "find all
`Try { }` blocks", "find every `case class` with more than 5 fields"), or when scalex returned
"not found" for a reason listed above. ast-grep matches AST structure via tree-sitter, ignoring
formatting differences, and works without any indexing step.

### 3. Semantic/LSP tool ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â compiler-accurate confirmation (if available)

If your environment exposes `start_metals_mcp` (start_metals_mcp is a shell function), which is Metals-backed for Scala ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â `find_referencing_symbols`, `find_implementations`, `get_diagnostics_for_file`, you must **use it** because neither scalex nor ast-grep does real type-checking:

- Implicit/given resolution (which instance the compiler actually selects)
- Type alias resolution across files
- Cross-package ambiguous-name disambiguation (two packages both defining `Config`)
- Compiler diagnostics for a file

This tier is genuinely optional ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â if no such tool is configured in your host, skip straight to
step 4 rather than blocking on it. There is no separate standalone Metals CLI step to run; where
this capability exists, it's exposed through a broader tool (an MCP server, an LSP client), not a
dedicated Metals binary.

### 4. grep / ripgrep ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â last resort only

Use plain `grep`/`ripgrep` only when all the tools above have been exhausted or are unavailable,
or for files outside Scala/Java entirely (config, docs, build scripts). A plain file read is fine
once a location has already been confirmed by one of the tools above ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â it is not a substitute for
the confirmation step itself.

## Relationship to other codebase-search conventions

A host or project may already have its own general codebase-search rule (e.g. ast-grep ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ semantic
tool ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ ripgrep) for non-Scala languages. For Scala/Java specifically, this skill's order ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â
**scalex first** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â supersedes that default: scalex's Scalameta-based symbol resolution is more
precise than tree-sitter pattern matching for named-symbol questions, which are the majority of
Scala navigation asks. ast-grep remains the right tool the moment the question shifts from "where
is X" to "find code shaped like this."

## Scala style

- Don't use `.iterator` unless really necessary. Prefer working with higher-order functions, like
  `filter`, `map`, `flatMap`, directly on collections.
- Prefer for-loops over `map`/`flatMap`, unless they fit in one line (one, or at most two, calls).
- Don't call `.toList` unless it's necessary.
- After adding a dependency to `build.sbt`, ALWAYS run the `import-build` tool.
- Use `sbt --client` instead of `sbt` to connect to a running sbt server for faster execution.
- NEVER use non-local returns.
