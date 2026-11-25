---
name: develop-code-quality
description: "This skill owns the code-quality rules that hold in every language: how code is named, structured, deduplicated and commented, and which code should not exist at all. Language skills (such as `language-typescript`) own the mechanics of their language and point here for these r..."
---
# Code Quality

## Purpose

This skill owns the code-quality rules that hold in every language: how code is named, structured, deduplicated and commented, and which code should not exist at all. Language skills (such as `language-typescript`) own the mechanics of their language and point here for these rules; their examples show the language-specific form.

It defers to:

- `AGENTS.md` for the decision rules that come before any code: tracing data flow end to end, naming the tradeoff, classifying the axis a change moves, validating at boundaries, and refusing fallbacks.
- `develop-code-spacing` for blank lines and paragraphing.
- `write-documentation` for persistent prose (READMEs, docs sites, guides) and its accuracy against the code.
- `develop-refactoring` for how to run a refactor or cleanup and prove it preserved behavior.

Examples are TypeScript or C++; the rules are language-neutral.

## Source of Truth Hierarchy

When rules conflict, apply in this order:

1. Enforced rules and published contracts: lint and compiler rules, the published API, a hard rule in `AGENTS.md`
2. The owner's explicit rulings for the work at hand
3. The measured local convention (the majority in the repository, or in the nearest module or package)
4. This skill's defaults

The rules in this skill are defaults unless they restate a hard rule. Do not invent a new local style when one is already established.

## Principles

1. Behavior-preserving by default: a change that alters observable behavior says so and is reviewed as a behavior change.
2. YAGNI: do not add features, parameters, hooks or layers that nothing needs now.
3. Prefer WET over unnecessary abstraction (Rule of Three: write it once - just write it; write it twice - notice but resist abstracting; write it a third time - now evaluate whether the cases share the same reason to change; if yes abstract, if no keep separate).
4. Keep implementations smaller by reducing real logic surface, not with cosmetic one-liners or comment removal.
5. Treat functions with many seemingly unrelated parameters as a smell: investigate whether responsibilities should be clarified or split by concern, without splitting for the sake of splitting.
6. Wrap multi-write operations in one transaction.
7. Remove dead code aggressively: unused methods, types, exports, tests, config keys and dependencies (see Dead Code and Unread State).
8. No compatibility shims or backwards-compatibility layers unless the human explicitly asks for them; with strong reasoning for one, ask first.

## Naming by Intent

Name operations by the domain action they perform, not by the mechanics: `connectToServer`, not `createServerConnection`; `valueFromConfig`, not `ConfigurationManager::instance.getValue`. Drop class-name suffixes that carry no meaning (`Manager`, `Handler`, `Proxy`, `Factory`, `Abstract`) unless they distinguish two genuinely different variants. A class named `ThingControllerManagerProxy` signals abstraction without providing any, and padding names to sound enterprise increases the surface readers must navigate without adding information.

Keep domain terms consistent across route, DTO, service, repository, entity, tests and docs, and prefer the canonical domain name over a legacy or vendor name.

## Structure

- Appropriate separation of concerns: no god functions, no mixed layers.
- No unnecessary coupling between modules.
- No premature abstraction: abstraction is earned by real duplication.
- No 3-layer call chains where the intermediate layer adds no branching logic or state; collapse to orchestrator plus specialized.
- No standalone helper files with functions used in exactly one place; inline them where they are used.

## Indirection and Extraction

Every layer of wrapping (trivial methods, single-use wrapper types, barrel files, parameter objects used at one call site) adds navigation cost. Remove wrappers that do not reduce real complexity.

### One-off extraction policy

- default to inline code when extracted helpers would be called only once
- extract only when one of these is true: complexity/size reduction (including lint constraints), clearly better readability with a well-defined responsibility, or likely near-term reuse
- rationale: avoid deep one-time call chains that force readers to jump across multiple functions and reduce navigability

### Algorithm preservation when extracting pure functions

When extracting a pure function whose output is observable downstream (deterministic shuffle seeds, hash-derived bucket assignments, ID-encoding schemes, ordering tiebreakers, anything backed by a fixed-seed PRNG), copy the body byte-for-byte. The function looks tidyable, but its output is part of an implicit contract: tests pin a specific permutation, users have a stable per-day card order, downstream caches key off the encoded value.

Things that look like cleanup but silently flip the contract:

- swapping a hand-rolled LCG for `Math.random()` or `crypto.randomBytes()`
- replacing bitwise twiddling (`| 0`, `& 0xff`) with arithmetic equivalents - they look identical until a 32-bit overflow case differs
- replacing a manual djb2 hash with `crypto.createHash('sha256')`
- swapping `Math.abs((x * 1664525 + 1013904223) | 0)` with `Math.floor(...)` because the bitwise OR "looks odd"
- changing the loop direction or the index used to compute the swap partner

If any of these would change the output for a given input, the extraction is no longer behaviour-preserving and the test suite that pins downstream order has to change with it. That is acceptable but it is no longer a refactor - it is a behavioural change in disguise.

Rule: copy the body, keep the `// eslint-disable` comments that flagged the intentional-bit-twiddling, do not "tidy." If a cleaner algorithm is genuinely better, propose it as a separate behavioural-change commit with the test suite updated to match the new permutation.

### Inline one-call wrappers

```typescript
// ÃƒÂ¢Ã‚ÂÃ…â€™
const getUsers = async () => fetchData('/api/users')
const users = await getUsers()

// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦
const users = await fetchData('/api/users')
```

### Trivial wrapper methods - inline the delegation

```typescript
// ÃƒÂ¢Ã‚ÂÃ…â€™ wrapper that only hardcodes one argument
private async cleanupTempFile(key: string): Promise<void> {
  await this.cleanupFile(key, 'temp file')
}
await this.cleanupTempFile(tempKey)

// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ call the real method directly
await this.cleanupFile(tempKey, 'temp file')
```

### Single-use parameter wrapper interfaces - use direct params

```typescript
// ÃƒÂ¢Ã‚ÂÃ…â€™ interface used at exactly one call site for a private method
interface IProcessInput {
  buffer: Buffer
  entityId: string
  config: IConfig
}
private async process(input: IProcessInput): Promise<void> {
  const { buffer, entityId, config } = input
  // ...
}

// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ direct parameters (consistent with sibling methods)
private async process(
  buffer: Buffer,
  entityId: string,
  config: IConfig,
): Promise<void> {
  // ...
}
```

**Allowed (and recommended): typed input objects at module boundaries.** The
anti-pattern above targets _private passthrough wrappers_ whose only job is to
forward args to another internal method. It does NOT cover the legitimate use
of a typed input where the method is a real contract boundary.

A typed input is the right call when ALL of these hold:

1. The method is a boundary crossing (repository query, service entry point,
   queue consumer entry, webhook handler) - not an internal helper.
2. The parameter list is heterogeneous: a mix of IDs, dates, arrays, numeric
   thresholds, and option flags. Same-typed positional args (e.g. three `string`
   IDs) are the trap a typed input prevents.
3. The internal positional binding is non-obvious. The worked example: two sibling
   ranking queries take the same TypeScript argument list, but each binds those
   args to _different_ SQL `$N` placeholder positions internally. A renamed
   positional call site silently passes the wrong value; a named input cannot.

```typescript
// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ typed input at a repository boundary - heterogeneous params,
//    same shape feeds two methods that bind positions differently
export interface IRankedCandidatesInput {
  currentUserId: string
  expandedCategoryIds: string[]
  lookbackDate: Date
  seenToday: string[]
  excludeIds: string[]
  minCount: number
  limit: number
}

public findTopRankedCandidates(
  input: IRankedCandidatesInput,
): Promise<IRankedCandidateProjection[]> {
  // SQL keeps positional $N; the public boundary is named.
}
```

The rule of thumb: if dropping the wrapper would force you to add
`// eslint-disable-next-line max-params` to call sites, the typed input is
not a wrapper - it is the contract. Keep it.

### Passthrough methods - merge when public only packs params for a private method

```typescript
// ÃƒÂ¢Ã‚ÂÃ…â€™ public method does nothing except pack params into an object and forward
interface ITranscodeOptions {
  inputPath: string
  outputDir: string
  probeResult: IProbeResult
  presets: string[]
}
public transcode(
  inputPath: string,
  outputDir: string,
  probeResult: IProbeResult,
  presets: string[],
): Promise<IResult> {
  return this.transcodeVariants({ inputPath, outputDir, probeResult, presets })
}
private async transcodeVariants(options: ITranscodeOptions): Promise<IResult> {
  const { inputPath, outputDir, probeResult, presets } = options
  // actual logic here
}

// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ merge into one method; delete the wrapper interface
public async transcode(
  inputPath: string,
  outputDir: string,
  probeResult: IProbeResult,
  presets: string[],
): Promise<IResult> {
  // actual logic here (no forwarding, no wrapper interface)
}
```

## Data Transformations

### Verbose field-by-field copy - assign directly when shapes match

```typescript
// ÃƒÂ¢Ã‚ÂÃ…â€™ manual copy when source already matches target type
this.configs = new Map(
  Object.entries(raw.entities).map(([name, cfg]) => [
    name,
    {
      tableName: cfg.tableName,
      s3Prefix: cfg.s3Prefix,
      outputFormat: cfg.outputFormat,
      sizes: Object.fromEntries(
        Object.entries(cfg.sizes).map(([k, v]) => [
          k,
          {
            maxWidth: v.maxWidth,
            maxHeight: v.maxHeight,
          },
        ])
      ),
    },
  ])
)

// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ direct assignment - source shape matches IEntityImageSchema
this.configs = new Map(Object.entries(raw.entities).map(([name, cfg]) => [name, cfg]))
```

### When direct assignment is not safe

Direct assignment (a spread, `Object.assign`, passing the source object through) copies the source's key set and its value semantics exactly. That is only safe when both match the target's contract. Write the fields out, or merge with explicit "keep the current value" semantics, when any of these hold:

- **Sparse updates.** A patch where an absent field means "no change" must not overwrite the target with `undefined`.
- **Absent, `undefined` and `null` mean different things.** In a NestJS API a `copyWith` rewritten from `props.locale ?? this.locale` to `{ ...this, ...props }` let a `PATCH { "locale": null }` through validation (`@IsOptional()` accepts `null`) and write `null` into a NOT NULL column: the endpoint went from 200 to 500, and the OpenAPI contract check could not see it.
- **The source has getters or non-enumerable properties** the target needs; a spread drops them.
- **The source carries extra enumerable fields** that would leak into the target, for example into a response body.

The direct form is right only when the source is an exact projection of the target: same keys, same null semantics.

## Redundant Work

### Redundant expensive calls - pass results down

```typescript
// ÃƒÂ¢Ã‚ÂÃ…â€™ metadata fetched in outer method, then re-fetched on same buffer in inner
const metadata = await this.getMetadata(buffer) // outer
// ... later:
private async processOriginal(buffer: Buffer): Promise<void> {
  const metadata = await this.getMetadata(buffer) // duplicate call
}

// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ pass the already-computed metadata
private async processOriginal(buffer: Buffer, metadata: IMetadata): Promise<void> {
  // uses metadata directly - no duplicate IO
}
```

## Magic Values

No magic strings or numbers: extract them into named constants (or the repository's config mechanism, when the value is environment-tunable).

```typescript
// ÃƒÂ¢Ã‚ÂÃ…â€™
if (retries > 3) { ... }
const key = `cache:user:${id}`

// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦
const MAX_RETRIES = 3
const CACHE_PREFIX_USER = 'cache:user'

if (retries > MAX_RETRIES) { ... }
const key = `${CACHE_PREFIX_USER}:${id}`
```

## Dead Code and Unread State

Everything the code declares must have a reader. Unread state is worse than missing state: it implies behavior that does not exist, and reviewers, tests, and future changes get built on the implication. Delete on sight - version control remembers.

Delete:

- **Struct fields written but never read.** A candidate carrying a `phaseId` the solver never consults, or an output row carrying `exerciseName` nothing prints, documents a data flow that isn't there.
- **Constructor parameters stored into members nothing reads.** Storing `goalName_` next to a `goal_` that already contains the name is two ways to hold one fact, one of them dead.
- **Request/DTO fields parsed into structs no code consumes.** Parse what you use. Extra wire fields the contract requires you to _accept_ are tolerated and ignored at the JSON boundary - not carried through the program as dead members.
- **Locals built and abandoned** (a `symptomIdSet` assembled and never queried).
- **Error enum values no code path produces**, and **function parameters no caller passes.** A defaulted `detail` argument that every call site leaves at its default is not flexibility; it is dead code plus a misleading signature, and every `detail.empty() ? fallback : detail` ternary behind it is unreachable.
- **No-op / null-object classes the composition root never instantiates.** A `NoOpSubsegment` with no construction site is not a pattern, it is a fossil.
- **Dead conditionals**: `(goalName == "Relief" ? 10 : 10)` compiles, reviews, and lies.
- **Protocol fields parsed but never honored.** A `Sampled` flag that never gates emission means either honor the flag or stop parsing it - parsing implies a promise.

### Defensive checks that cannot fire

Do not re-validate what an upstream layer guarantees. Common shapes:

- `conn->is_open()` immediately after a constructor documented to throw on failure.
- A null check on a pointer the only caller always sets.
- A second lookup that cannot miss because a membership check over the same key set just passed.
- An `empty()` early-return in front of a loop that handles empty naturally.

Replace the check with a comment stating the guarantee ("filter runs after `passesEquipment`; all equipment here is owned"), or better, restructure so the guarantee is a type-level fact - a reference instead of a pointer, a validated wrapper instead of a raw value. Unfireable checks train readers to distrust real invariants.

### The bar for speculative structure

Keeping a field, parameter, hook, or class "for later" requires a concrete consumer in the same change. "We might need it" fails the bar; when the need arrives, the addition is a small diff against a smaller codebase.

## Single Source of Truth

Each derived domain fact is computed in exactly one place - the boundary where its inputs first exist - and flows downstream as data. Duplicated derivations do not merely waste lines; they diverge, and the divergence is silent because each copy looks locally correct.

Symptoms and cures:

- **The same classification computed in multiple layers** (a filter, a builder, and a solver each re-deriving "is this a device exercise?") ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ classify once where the inputs live, carry the result as a flag or enum on the item. Bonus: downstream layers stop needing the lookup maps used to classify, which unwinds include dependencies (a solver header including database models is this smell made visible).
- **The same traversal implemented twice back-to-back producing the same key set** (one hierarchy walk to build a set, an adjacent walk to build a map over identical keys) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ one pass building one structure. If a map's key set _is_ the set, pass the map and use `contains` for membership.
- **The same index rebuilt per consumer** (`id ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ position` reconstructed in three sibling loaders) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ build once, pass down.
- **Two parallel containers coupled only by index**, one copied element-wise from the other so a downstream API can take "its" type ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ one struct, one vector. Index-coupled parallel structures are a refactor away from a silent misalignment.

### Defaults exist in exactly one place

For configuration, that place is the config definition itself (a config class field default, a config struct's default member initializer); the language skill names the mechanism. Constants files, builder initializers, and call-site literals restating the same `"localhost"` are three places to update and two places to forget.

### Identity from data, not fingerprints

Never classify an entity by matching a characteristic value it happens to carry:

```cpp
// Bad - "the device whose bonus happens to be 20 minutes must be the Halo"
bool isHalo() const {
  for (const auto minutes : timeRules | std::views::values) {
    if (minutes == kHaloAdditionalMinutes) return true;
  }
  return false;
}
// Breaks the day two devices share a value, a value changes in the DB,
// or a JSON number arrives as 20.0 instead of 20 - and every failure is silent.

// Good - identity is a column
enum class DeviceKind { None, Halo, Contour };  // from equipment.kind
```

If the schema lacks a kind, add the column; do not fingerprint. Corollary: when a parameter table exists in data (per-goal bonus minutes, per-tier caps), code **reads the table** - it never re-encodes the table as constants and demotes the data to a recognition key. A table that lives in both the database and a switch statement will disagree eventually, and the code's copy wins silently.

## Determinism and Tie-Breaks

Hash-container iteration order must never leak into output: sort before assigning indices, generating names or IDs, or writing anything persisted. The language skill names the containers and sorting idioms.

A max/argmax scan over an unordered container resolves ties by hash-bucket order - stable within one binary, arbitrary across stdlib versions, rebuilds, and dataset changes. When the winner is a business decision (which symptom dominates, which item is named), the tie-break must be explicit and stable:

```cpp
// Bad - on ties, the winner depends on hash order
std::unordered_map<std::string, int> severityBySymptom = ...;
for (const auto& [name, severity] : severityBySymptom) {
  if (severity > maxSeverity) { dominant = name; maxSeverity = severity; }
}

// Good - aggregate in encounter order; '>' resolves ties to the first submitted
std::vector<std::pair<std::string, int>> severityBySymptom;  // built in request order
```

Choose the tie-break key deliberately - request order, sorted ID - and document it. "Whatever the container yields" is not a tie-break, it is a latent flake.

## Comments

- Keep code mostly self-documenting through naming and structure.
- A comment explains why, never what the next statements do. Delete narration that restates the code ("loop over the users", "return the result"). Keep constraints, invariants, ordering reasons, side-effect ordering, external-contract explanations and non-obvious tradeoffs. Comments that document a non-obvious role, contract or lifecycle position of a type or module (a class comment stating which pipeline step populates it) are not narration.
- Complex logic gets an explanatory comment or is broken into named steps.
- A comment, file name or class name that contradicts the code is a bug with a longer half-life than most code bugs, because readers trust prose over implementation. When behavior changes, the comments and names that describe it change in the same commit. A `ConnectionPool` whose comment explains there is no pool needs a rename. Persistent docs follow the same rule and are owned by `write-documentation`.
- A TODO carries enough context to be actionable, including why the current approximation is acceptable for now:

```cpp
// TODO: Rough approximation. Real throughput depends on pickup/drop distance,
// stack size bonuses, and rotation-extension interaction.
```

- No stale TODOs after the work they describe is done.
- No comments that suppress tooling (lint disables, type-checker escapes) without a documented, unavoidable reason inline.

## Anti-Patterns

- Unnecessary indirection: trivial wrapper methods that only delegate with a hardcoded argument, single-use parameter wrapper types for private methods, barrel files with no consumers, adapter layers that pass data through unchanged
- Passthrough methods whose only job is to pack parameters into a single-use type and forward them
- Inconsistent parameter style across sibling methods of one class
- Verbose field-by-field mapping when the source is an exact projection of the target; and the reverse, a spread or `Object.assign` over a sparse or nullable source
- Redundant expensive operations on the same input when the result could be passed down
- 3-layer call chains whose middle layer adds no logic; standalone helper files used in one place
- Exported symbols with zero consumers; speculative fields, parameters and options that nothing reads
- Struct fields written but never read; request fields parsed but never consumed; error values no code path produces
- Defensive checks against conditions upstream code guarantees cannot occur
- The same default defined in more than one place; the same derived fact computed in more than one layer
- Identity inferred by matching characteristic values instead of an ID or kind column; parameter tables re-encoded as code constants
- Business tie-breaks resolved by hash-container iteration order
- Magic strings or numbers
- Partial domain renames; stale names, routes or docs after a rename
- Comments that narrate the code, contradict it, or carry a TODO with no context
- Hidden behavior changes inside a change presented as a refactor

## Rules

- Load this skill with the language skill for every code change and every review
- Name by domain intent; drop meaningless suffixes
- Remove indirection that does not reduce real complexity; extract only for real complexity reduction, a well-defined responsibility, or near-term reuse
- Copy an extracted algorithm byte for byte when its output is observable
- Assign directly only from an exact projection; write the fields out for sparse or nullable sources
- Pass computed results down instead of recomputing them
- Every declared field, parameter, enum value and branch has a reader or producer; delete unread state on sight
- Every derived fact is computed once, at the boundary where its inputs exist; every default is defined once
- Identity comes from data, never from fingerprint-matching values
- Business tie-breaks use an explicit, stable key
- Comments say why; narration goes, constraints and invariants stay; prose and names change in the same commit as the behavior they describe
