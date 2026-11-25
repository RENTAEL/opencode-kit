---
name: language-typescript
description: "This skill codifies preferred TypeScript practices based on:"
---
# TypeScript Skill

## Purpose

This skill codifies preferred TypeScript practices based on:

- repository-enforced conventions (ESLint, tsconfig, package structure)
- recurring refactor preferences
- architecture patterns across TypeScript services and modules

Use this as the default rulebook before writing, refactoring, or reviewing TypeScript code.

## Source of Truth Hierarchy

When rules conflict, apply in this order:

1. Repository lint + compiler rules
2. Existing local pattern in the nearest module/package
3. This skill's defaults

Do not invent a new local style when an existing style is already established.

## Repository-Specific vs Neutral (Read First)

Most of this skill is neutral TypeScript guidance that holds anywhere. A few sections pin to a stack that varies between the repos this skill serves - **discover the actual repo before applying a pinned name**, and read tagged guidance accordingly:

- **Illustrative domain names.** Concrete identifiers in examples (`RoutineService`, `GoalType`, `UserId`, `EquipmentId`, `GoalNotFoundError`, cache keys like `lookups:equipment`, app names like `lambda-image-processing`) are placeholders to make a pattern concrete - not a catalog of any one product. Substitute the repo's real names.
- **[TypeORM].** The `TypeORM Patterns` section and any rule naming entities, `QueryBuilder`, `EntityManager`, `dataSource.transaction`, `softDelete`, or `eager: true` applies to TypeORM repos. A Drizzle repo applies the same _principle_ (parameterized queries, N+1 avoidance, transactions, deterministic ordering) with `drizzle-orm`'s query builder, `db.transaction()`, and `onConflictDoNothing`.
- **Auth is explicit opt-in via a composite decorator; the decorator name varies.** These repos have no global auth guard and no `@Public()` opt-out - every protected controller/route carries an explicit composite decorator that wraps the auth guard + `@ApiBearerAuth()`. The name differs per repo (for example `@JwtAuth()`). Auth examples below use one repo's names as a concrete instance; the neutral rule (protect each route explicitly with the repo's composite decorator, keep controllers thin, read the authenticated user via the repo's user decorator) is what holds. Do not introduce `@Public()`/`IS_PUBLIC_KEY`/a global guard - that model is not used here.
- **[if present] capabilities.** Redis caching, `@nestjs/event-emitter`, an admin app, and specific vendor packages exist only in some repos. Their sections are tagged - apply only after confirming the repo has that capability. In particular, **the async-queue transport in these repos is AWS SQS, not BullMQ** - treat the BullMQ specifics as one concrete instantiation of transport-neutral worker principles.

## Language and Formatting Baseline

- TypeScript strict mode is expected (`strict` family enabled).
- 2-space indentation.
- single quotes.
- no semicolons.
- trailing commas where formatter applies.
- arrow functions only; do not use `function` declarations.
- Swagger decorators (`@ApiProperty`, `@ApiResponse`, `@ApiOperation` and the other `@Api*` decorators) are written with their options on one line when they fit the configured print width (often 120 columns). The formatter keeps an object literal expanded once it has been written multi-line, so this is authored by hand; when the formatter itself expands a decorator, leave it. The change is layout only: the generated OpenAPI document must stay identical.

### Vertical Paragraphing

Blank lines follow the `develop-code-spacing` skill, which owns vertical paragraphing: role-based paragraphs, multi-line statements, guards, terminal returns, test phase markers, and repository-wide spacing passes.

## Naming Conventions

### General

- Files: kebab-case with purpose suffix where applicable.
- Classes: PascalCase with role suffix (`Service`, `Controller`, `Module`, `Repository`).
- Methods/variables: camelCase.
- Private members: camelCase, no leading underscore.

### Interfaces and Type Parameters

- Interface names start with `I` and use PascalCase.
- Generic type parameters start with `T` and are descriptive (`TItem`, `TResponse`, `TData`).
- Type aliases (`type X = ...`) take no prefix, in production and test code alike (`LockedQuest`, `SeededQuestTask`): `I` is reserved for interfaces and `T` for generic parameters.

### Booleans

- Prefix booleans with intent-bearing verbs:
  - `is`, `has`, `can`, `should`, `did`, `will`, `does`, `expected`
- Prefer semantic names over ambiguous forms.

### Single-Purpose App Naming

When an app has a single domain (e.g., `lambda-image-processing`, `lambda-subscriptions`), drop the domain prefix from class names - the app scope already provides context:

- `ProcessingService` not `ImageProcessingService`
- `TransformerService` not `ImageTransformerService`
- `RepositoryService` not `ImageEntityRepository`

Keep action-descriptive words (`Processing`, `Transformer`, `Repository`) - only drop the redundant domain qualifier.

This rule does NOT apply to multi-domain apps like `apps/api/` where the domain prefix disambiguates between modules (e.g., `RoutineService` vs `ExerciseService`).

### Naming Operations and Classes by Intent

Name by domain intent and drop meaningless class suffixes; see `develop-code-quality`, Naming by Intent.

### Domain Terms

- Prefer canonical domain names over legacy/vendor names.
- Keep terms consistent across route, DTO, service, repository, entity, tests, and docs.

### Constants and Enums

- Use `SCREAMING_SNAKE_CASE` for module-level constants that represent fixed configuration or magic values (`MAX_RETRIES`, `CACHE_PREFIX_USER`, `DEFAULT_PAGE_SIZE`).
- Use PascalCase string enums for domain values visible in APIs and serialization (`UserRole.Admin`, `GoalType.Relief`).
- Keep enum members in a single canonical file per domain; do not scatter related enum values across multiple files.

## File and Module Organization

- Keep folders purpose-driven and predictable within the local project conventions.
- Match the nearest existing module layout before introducing new structure.
- Prefer direct imports over unnecessary local barrels.
- Delete barrel files (`index.ts`) when all consumers already import directly from source files; a barrel with zero consumers is dead code.
- Do not add wrapper interfaces, adapter layers, helper methods or passthrough methods that do not reduce real complexity (`develop-code-quality`, Indirection and Extraction).
- Co-locate related types: config schema types and runtime data types consumed by the same pipeline belong in one file, not split across multiple type files with re-exports between them.
- Do not split error classes across multiple files within the same app/module when they share a common base; one `errors.ts` is sufficient.
- Do not create 1-method wrapper services around single infrastructure calls (e.g., a service that only wraps `redis.del()` or `readFile()` + YAML parse); inline into the consuming service.
- Avoid creating new files unless there is a clear structural reason.
- Order class members: fields, the constructor, public methods, protected methods, private methods. Private helpers sit below the last public method, not between public ones.

### Import Organization

Imports within a file follow a consistent group order separated by blank lines:

1. Node built-ins (`node:fs`, `node:path`)
2. External packages (`@nestjs/*`, `class-validator`, `zod`, `bullmq`)
3. Workspace packages (`@workspace/auth`, `@workspace/database`)
4. Relative imports - parent first (`../`), then sibling (`./`)

Within each group, sort alphabetically. Never mix groups on a single line. Tooling (ESLint `import/order` or similar) enforces this; when adding imports manually, match the pattern.

Mark type-only imports inline (`import { type Quest, QuestService } from './quest'`, `import { type Quest } from './quest'`), not with a whole-statement `import type { ... }`, unless the repository's majority does otherwise.

## Types and Modeling

### interface vs type

- Use `interface` for object shapes and contracts.
- Use `type` for unions, intersections, mapped/utility aliases, and discriminators.

### Arrays

- Use `TItem[]`, not `Array<TItem>`.

### Inference

- Avoid redundant primitive annotations when inference is obvious.
- Keep explicit annotations where they improve cross-file readability.

### Return Types

- Explicit return types are preferred on public methods/functions and exported symbols.
- Keep service/controller/repository boundaries explicitly typed.

### Nullability and Optionality

- Model nullability intentionally (`T | null` when explicitly nullable).
- Use `?` for optional fields.
- In DTO Swagger metadata, reflect optional vs nullable precisely.

### `any` vs `unknown`

- Never use `any`; use `unknown` and narrow with type guards or validation (e.g., Zod `.parse()`).
- If an external API returns untyped data, receive it as `unknown` and validate before use.

### Derived Types

- Prefer `Pick`, `Omit`, `Partial`, and other utility types over manually redeclaring fields.
- When a subset of an existing type is needed, derive it: `type UserSummary = Pick<User, 'id' | 'name'>`.

### Non-null Assertions

- Acceptable for framework/ORM initialized fields (`id!`, entity fields).
- Acceptable in tests where fixture guarantees existence.
- Do not use `!` to bypass real uncertainty in application logic.

### Type Safety

- Do not widen existing domain enums or named type aliases to anonymous `string`/`number` types; use the exact existing type (e.g., `Gender`, `MeasurementSystem`, `DailyTimeCommitment`).
- Enforce interface alignment with the canonical source type (e.g., align response interface fields with `IProfile` enum-typed fields).

### TypeScript 5.x Features

Adopt these features where they add clarity; do not adopt them for novelty.

**`satisfies` operator** - Use to validate that a value conforms to a type while preserving the narrower inferred type. Preferred over `as` for config objects, lookup tables, and constant definitions where you want both type checking and literal inference:

```typescript
// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ satisfies - validates shape, preserves literal inference
const CACHE_KEYS = {
  equipment: 'lookups:equipment',
  phases: 'lookups:phases',
  bodyAreas: 'lookups:body-areas:all',
} satisfies Record<string, string>
// typeof CACHE_KEYS.equipment is 'lookups:equipment', not string

// ÃƒÂ¢Ã‚ÂÃ…â€™ as - widens to Record<string, string>, loses literal types
const CACHE_KEYS = {
  equipment: 'lookups:equipment',
} as Record<string, string>
```

**`const` type parameters** - Use on generic functions where callers need literal type inference without `as const` at call sites. Primarily useful in config builders, typed event emitters, and schema factories:

```typescript
const defineRoutes = <const TRoutes extends readonly string[]>(routes: TRoutes): TRoutes => routes

// Inferred as readonly ['generate', 'ping'] - not string[]
const routes = defineRoutes(['generate', 'ping'])
```

**`using` declarations (Explicit Resource Management)** - Adopt for deterministic cleanup of resources like file handles, database connections, temporary files, and locks. Requires `Symbol.dispose` / `Symbol.asyncDispose` implementation. Disposal happens in reverse declaration order (LIFO):

```typescript
const acquireLock = async (key: string): Promise<AsyncDisposable> => {
  await redis.set(`lock:${key}`, '1', 'EX', 30, 'NX')
  return {
    [Symbol.asyncDispose]: async () => {
      await redis.del(`lock:${key}`)
    },
  }
}

// Lock is automatically released when scope exits (including on throw)
await using lock = await acquireLock('cache-rebuild')
const data = await expensiveComputation()
await cache.set(key, data, ttl)
```

**Inferred type predicates (5.5+)** - `.filter()` now narrows types automatically when the predicate is obvious. Remove explicit type predicate helper functions (like `isNonNull`, `isDefined`) that only exist to satisfy the type system when the built-in inference covers the case:

```typescript
// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ 5.5+ infers the narrowing automatically
const valid = items.filter((item) => item !== null)
// type: NonNullable<TItem>[]

// ÃƒÂ¢Ã‚ÂÃ…â€™ Remove this utility if only used for .filter()
const isNonNull = <T>(item: T | null): item is T => item !== null
```

**`NoInfer<T>` (5.4+)** - Use to prevent TypeScript from using a parameter position for inference when that position should only receive an already-inferred type. Useful in fallback/default parameters:

```typescript
const getOrDefault = <T>(value: T | undefined, fallback: NoInfer<T>): T => value ?? fallback
```

**Features to avoid or defer:**

- **Decorator metadata (5.2)** - runtime support still requires polyfills outside NestJS. NestJS already handles its own decorator metadata via `reflect-metadata`. Do not adopt the TC39 decorator metadata API separately unless the runtime environment natively supports it.

### Branded Types for Domain Safety

Use branded types to prevent accidental interchange of structurally identical primitives that represent different domain concepts (e.g., `UserId` vs `EquipmentId` vs `GoalId`). This catches misuse at compile time with zero runtime overhead.

```typescript
declare const __brand: unique symbol
type Brand<TBase, TBrand extends string> = TBase & { readonly [__brand]: TBrand }

type UserId = Brand<string, 'UserId'>
type EquipmentId = Brand<string, 'EquipmentId'>
type GoalId = Brand<string, 'GoalId'>

// Creation via validated factory (pairs well with Zod)
const UserId = (id: string): UserId => id as UserId
```

When to use branded types:

- UUID-based entity IDs passed across service boundaries (prevents swapping `userId` and `goalId` arguments).
- Currency amounts that must not be mixed (cents vs dollars, different currencies).
- Validated strings (email addresses, URLs) where the brand signals "this has been validated".

When NOT to use:

- Module-internal types where only one ID type exists and confusion is unlikely.
- Types that are already discriminated by structure (different shapes are already distinct).

Combine with Zod for runtime validation at trust boundaries (API input, queue job payloads) and let the branded type propagate through the domain layer:

```typescript
const UserIdSchema = z
  .string()
  .uuid()
  .transform((id) => id as UserId)
```

### Discriminated Unions

Prefer discriminated unions with a `type` (or `kind`) string literal field for representing states, events, or polymorphic domain objects. The discriminant field must be a string literal, not a computed value:

```typescript
type JobResult =
  | { type: 'success'; data: IRoutineData }
  | { type: 'failure'; error: string; retryable: boolean }
  | { type: 'skipped'; reason: string }
```

Exhaustive `switch` on the discriminant; no `default` clause - let TypeScript enforce completeness via `never`:

```typescript
const handleResult = (result: JobResult): string => {
  switch (result.type) {
    case 'success':
      return result.data.name
    case 'failure':
      return result.error
    case 'skipped':
      return result.reason
  }
  // No default - adding a new variant forces a compile error here
  const _exhaustive: never = result
  return _exhaustive
}
```

### Template Literal Types

Use for type-safe string patterns in cache keys, route paths, event names, and configuration keys where the set of valid strings follows a pattern:

```typescript
type CacheKeyPrefix = 'lookups' | 'routine-builder'
type CacheKey = `${CacheKeyPrefix}:${string}`

const buildKey = (prefix: CacheKeyPrefix, suffix: string): CacheKey => `${prefix}:${suffix}`
```

Do not over-engineer template literal types for internal strings where a plain `string` or union is sufficient. The cost of type-level complexity must be justified by real bug-prevention value.

## Runtime Validation (Zod)

### Schema-First at Trust Boundaries

Validate with Zod at every trust boundary where data enters the system:

- API request bodies, query params, headers
- Queue/message payloads (e.g. SQS message bodies)
- Webhook payloads from external services
- Environment variables at startup
- YAML/JSON config files loaded from disk
- Deserialized Redis cache values (cache corruption happens)

Internal function calls between trusted modules do NOT need Zod validation - TypeScript's static types are sufficient within the trust boundary.

### Schema Organization

- Define Zod schemas in the same file as (or co-located with) the types they validate.
- Derive TypeScript types from Zod schemas with `z.infer<>` - do not duplicate the type definition manually.
- Name schemas with a `Schema` suffix: `GenerationRequestSchema`, `BodyAreaSymptomSchema`.
- For DTOs in NestJS, keep `class-validator` on the DTO classes (NestJS pipes require them). Use Zod for non-NestJS validation contexts (workers, webhooks, config loading).

### Patterns

```typescript
// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ Schema as single source of truth
const BodyAreaSymptomSchema = z.object({
  bodyAreaId: z.string().uuid(),
  symptomId: z.string().uuid(),
  severity: z.number().int().min(1).max(10),
})
type BodyAreaSymptom = z.infer<typeof BodyAreaSymptomSchema>

// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ Environment validation at startup - fail fast
const EnvSchema = z.object({
  PGHOST: z.string().default('localhost'),
  PGPORT: z.coerce.number().default(5432),
  PGDATABASE: z.string().default('api_<project>_db'),
  REDIS_ENABLED: z.coerce.boolean().default(true),
})
const env = EnvSchema.parse(process.env)

// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ safeParse for expected-failure paths (user input, webhooks)
const result = GenerationRequestSchema.safeParse(body)
if (!result.success) {
  return { error: 'Invalid request', details: result.error.flatten() }
}

// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ parse for programmer-error paths (config, env) - crash is correct behavior
const config = ConfigSchema.parse(rawConfig)
```

### Anti-Patterns

- Do not `.parse()` the same data twice in different layers - validate once at the boundary, then trust the typed result downstream.
- Do not define Zod schemas inside functions - define at module level and reuse.
- Do not use `.transform()` for complex business logic - keep transforms limited to coercion (string ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ number, ISO string ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Date). Business logic belongs in services.
- Do not mix Zod and `class-validator` on the same object - pick one per context.

## API Layer Conventions (NestJS)

### Controllers

- Keep controllers thin: parse/validate/route only.
- Delegate business logic to services.
- Keep explicit return types.
- Use route semantics intentionally (GET read-only, POST mutations, etc.).
- Private controller methods that implement non-trivial business logic are a hard review failure; extract that logic into a service.

### Authentication and Authorization

Protection is **explicit and opt-in**: every protected controller (or route) carries a composite auth decorator that wraps the auth guard + `@ApiBearerAuth()`. There is no global guard and no `@Public()` in these repos - an unprotected route is simply one with no auth decorator. The decorator's name is repo-specific; a common name is `@JwtAuth()`. Read a sibling controller and reuse whatever it uses - do not invent a new guard-stacking style.

```typescript
// Concrete instance (names illustrative). The decorator wraps
// applyDecorators(UseGuards(<AuthGuard>), ApiBearerAuth()).
@ApiTags('feature')
@Controller('feature')
@JwtAuth()
export class FeatureController {
  @Get()
  public async list(@UserId() userId: string): Promise<FeatureListResponse> {
    return this.featureService.list(userId)
  }
}
```

- Apply the composite decorator at the class level when every route shares the same protection, or per-method when a controller mixes protection levels (e.g. a public sign-in route beside protected routes) - follow the sibling controller's placement.
- Prefer the repo's **composite** decorator (`@JwtAuth()`) over hand-stacking `@UseGuards(...) @ApiBearerAuth()` on every controller - the composite is the single source of truth for the guard set.
- Read the authenticated user via the repo's user decorator (`@UserId()` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ the `userId` string, or the repo's equivalent). Never re-parse the token in a controller.

### Admin Endpoints

**[if present]** Admin exists only in repos that have an admin app/role, and its shape varies: a repo may keep admin in a **separate `apps/admin` app** whose modules register only admin controllers (guarded by an admin-only composite decorator), not a second controller inside the public module. Discover whether the repo has an admin app and follow its structure; do not add an admin controller to the public API app.

### DTOs

- Names should describe transport role (`*Query`, `*Params`, `*Request`, `*Response`). Whether they carry a `Dto` suffix (`*QueryDto`, `PaginationDto`) is a repository convention: count the existing transport classes and follow the majority. A class whose name already appears as an OpenAPI component keeps it: renaming it changes the contract. The file is named after its main class (`select-pace-request.dto.ts` holds `SelectPaceRequest`).
- A response DTO constructor may `Object.assign(this, source)` only when `source` is an exact projection of the response: the same key set and the same null semantics. Otherwise assign the fields explicitly.
- Use class-validator for request validation.
- Use class-transformer where conversion is needed.
- Swagger decorators must match runtime shape (`ApiPropertyOptional`, `nullable: true`, `isArray`, `enumName`, `type`).
- **Use named command/input types for service methods** - when a service method accepts 4+ parameters, introduce a named interface (e.g., `ICreateReportInput`) instead of positional args. This is different from the single-use-parameter anti-pattern: command types represent a domain concept (the "create" input) at a boundary crossing, not a forwarding wrapper for a private method. See "Single-use parameter wrapper interfaces" in `develop-code-quality` for the disambiguator and worked example.
- **No booleans over API boundaries.** Do not return bare `boolean` fields in response DTOs when a string enum would be clearer and more extensible. Instead of `{ eligible: true, reason: null }` use a single status enum: `{ status: 'AVAILABLE' }`. This avoids the boolean + nullable companion anti-pattern and makes the contract self-documenting. When a boolean seems needed, ask whether a discriminant enum with two or more named values would serve the consumer better.
- **Boolean query parameters require explicit `@Transform` + strict comparison.** HTTP query params arrive as strings. `"false"` is truthy in JavaScript, so `if (selectable)` passes when the client sends `selectable=false`. Always use `@Transform` with explicit `=== 'true'` / `=== 'false'` conversion on boolean query DTO fields, and guard conditionals with `!== undefined` instead of truthiness checks.

```typescript
// ÃƒÂ¢Ã‚ÂÃ…â€™ boolean + nullable reason - ambiguous, not extensible
export class EligibilityResponse {
  public eligible: boolean
  public reason: string | null
}

// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ single status enum - self-documenting, extensible
export enum EligibilityStatus {
  AVAILABLE = 'AVAILABLE',
  DAILY_LIMIT_REACHED = 'DAILY_LIMIT_REACHED',
  SUBSCRIPTION_REQUIRED = 'SUBSCRIPTION_REQUIRED',
}
export class EligibilityResponse {
  public status: EligibilityStatus
}
```

- **No client-computable fields in responses.** Do not include fields the client can derive from other fields already in the response. If the response contains a `date` field and the client knows what "today" is, do not add an `isToday` boolean - the client computes `date === today` trivially. Each redundant field adds serialization cost, contract surface, and a staleness risk if the derivation logic ever diverges between server and client.

### Module-Scoped Config

Do not use raw `ConfigService.get<T>('ENV_VAR')` in feature module services. The correct pattern is a validated config class registered via `ConfigModule.forFeature()` and injected with `@Inject(config.KEY)`.

Bad - raw access, no validation, duplicated across services:

```typescript
constructor(private readonly configService: ConfigService) {
  this.arn = this.configService.get<string>('LAMBDA_ARN', '')
}
```

Good - validated, typed, single source of truth:

```typescript
// config/feature.config.ts
export class FeatureConfig {
  @IsString()
  @IsOptional()
  public LAMBDA_ARN?: string
}
export const featureConfig = registerAs('featureConfig', () => load(FeatureConfig))

// feature.service.ts
constructor(@Inject(featureConfig.KEY) private readonly config: FeatureConfig) {}
```

Infrastructure-level configs from `@workspace/*` packages (e.g., `databaseConfig`, `storageConfig`, `redisConfig`) use the same `registerAs` + `load` pattern but are registered globally in the root module's `ConfigModule.forRoot({ load: [...] })`.

### NestJS Interceptors, Pipes, and Guards - Composition Rules

- Apply the repo's composite auth decorator at the controller class level when every route shares protection; apply per-method when a controller mixes protection levels.
- Use global pipes (`ValidationPipe`) via `app.useGlobalPipes()` for DTO validation - do not repeat `@UsePipes()` on individual endpoints.
- Use interceptors for cross-cutting concerns (logging, response transformation, timeout). Keep interceptor logic stateless; inject services if needed.
- When a repo composes multiple guards, order matters - authentication runs before authorization (an auth guard before a roles guard). The repo's composite decorator already encodes the correct order; reuse it rather than re-stacking guards by hand.
- Do not put business logic in interceptors or pipes. These are infrastructure concerns only.
- **Request context derived from the authenticated user is resolved after the guards, never in middleware.** Nest runs middleware before guards, so when middleware runs the auth guard has not yet put the user on the request. Resolve such context (the user's locale, settings read from their row) in a parameter decorator backed by a pipe, composed on the repo's user decorator. One repository's pattern:

  ```typescript
  export const UserLocale = () => UserId(undefined, UserLocalePipe)

  public async getCandidates(@UserLocale() locale: AppLocale): Promise<CandidatesResponse> { ... }
  ```

  This is the same shape as a request-header decorator such as `GetTimezone`. It replaces injecting the user service into every controller just to read one field.

- **Prefer explicit opt-in over global registration** for feature-level interceptors. Wrap in a composite decorator and apply at the controller class level. Global interceptor registration is appropriate only for true infrastructure (logging, error handling), not feature behavior.

## Service and Repository Boundaries

### Services

- Own business rules, orchestration, and response shaping.
- Use guard clauses to reduce nesting.
- Keep method names action-oriented.

### Service Decomposition

When a service grows beyond 5-6 constructor dependencies or mixes read/write/presentation concerns, split by responsibility:

| Pattern                    | When to use                                                                                                                           |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| **Command/Query split**    | Service mixes read-only queries with write mutations. Separate into a write service and a query service.                              |
| **Lifecycle split**        | Service handles multiple state transitions (create, complete, cancel) plus sub-entity management. Separate by state-transition scope. |
| **Side-effect extraction** | Service mixes core logic with side effects (analytics, notifications). Extract or decouple via events.                                |

Rules:

- Each split service should have a clear, non-overlapping responsibility.
- The orchestration service (if one remains) delegates to split services - it does not duplicate their logic.
- After splitting, verify constructor dependency count decreases. If it doesn't, the split wasn't the right boundary.

### Entity ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Response Mapping

The response DTO owns its own mapping. Give the response class a constructor (or a static `fromEntity` / `fromProjection` when entity-specific parsing must happen before assignment) that takes the entity/projection and assigns fields. The controller calls `new FeatureResponse(entity)`. Services return entities/projections, never response DTOs; repositories return entities/projections, never response DTOs.

Do not introduce presenter/mapper services or standalone mapper functions for ordinary entity-to-response mapping. The DTO constructor is the mapping; a separate service is indirection that earns its place only when the identical mapping is reused across very different outputs with injected dependencies (rare).

```typescript
// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ response DTO maps itself
export class FeatureResponse {
  public id: string
  public name: string
  constructor(entity: FeatureEntity) {
    this.id = entity.id
    this.name = entity.name
  }
}
// controller
return new FeatureResponse(entity)

// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ static factory when parsing is required before assignment
public static fromEntity(entity: PartEntity): PartResponse { /* parse, then new PartResponse({...}) */ }

// ÃƒÂ¢Ã‚ÂÃ…â€™ repository returning a response DTO - repositories return entities/projections
public findAll(): Promise<FeatureResponse[]> { ... }
```

Pick one construction convention and keep it: prefer `new X(entity)`; use `X.fromEntity(entity)` only when a transform is unavoidable, and do not mix both for the same DTO.

### Repository Boundaries

- Repositories return entities or typed projections - never API response DTOs.
- Repositories never inject services. If mapping logic requires a service, it belongs in the service layer.
- Repositories never cross aggregate boundaries (e.g., an XP repository should not query a profiles table directly).
- Two categories: **aggregate repositories** (writes + aggregate loading) and **query/projection repositories** (read models, list projections).

### Redis Caching Pattern

**[if present]** Only in repos with a Redis package/cache layer. Services that cache data follow a read-through pattern:

```typescript
public async getData(id: string): Promise<TData> {
  const cacheKey = CACHE_KEYS.RESOURCE(id)
  const cached = await this.redisService.get<TData>(cacheKey)

  if (cached !== null) {
    return cached
  }

  const data = await this.repository.findById(id)
  await this.redisService.set(cacheKey, data, CACHE_TTL_SECONDS)
  return data
}
```

Cache keys are defined in a single canonical constants file in the shared-domain contracts package (discover its actual path, e.g. a `cache/` subdir). Workers and webhooks invalidate these keys after writes.

### Cache Invalidation Strategies

For write-through invalidation (data changes in DB, cache must reflect it):

- Delete the cache key immediately after a successful write transaction commits - do not update the cached value (delete + let next read repopulate avoids stale partial updates).
- When a write affects multiple cache keys (e.g., updating a body area affects `lookups:body-areas:all`), enumerate all affected keys and delete them in a single pipeline call.
- Cache invalidation from workers/webhooks must reference the same key constants as the API to prevent key drift.

### Cache Stampede Prevention

For high-traffic cache keys with expensive regeneration (e.g., lookup tables fetched by every request):

- **Mutex lock pattern** - on cache miss, acquire a short-lived Redis lock (`SET lock:${key} 1 EX 5 NX`). If lock acquired, regenerate and cache. If lock not acquired, wait briefly and retry (or return stale data if available).
- **Stale-while-revalidate** - store data with a physical TTL longer than the logical TTL. On read, if logical TTL has expired but physical TTL has not, serve stale data and trigger async background refresh.
- Reserve stampede protection for keys that are both frequently accessed AND expensive to regenerate. Simple key-value lookups with fast DB queries do not need it.

### Repositories

- Keep persistence-focused and predictable.
- Prefer typed return shapes.
- Keep API response mapping in services unless repository contract is intentionally API-oriented.
- For paginated database-backed reads, apply filtering and pagination in the database query, never in memory.
- Ensure deterministic ordering at query level before pagination (`ORDER BY` + `LIMIT/OFFSET` or cursor predicate).

## Error Handling

- Prefer typed/domain-specific errors over generic `Error`.
- Convert low-level errors to stable application-facing errors at boundaries.
- Keep messages actionable and specific.

Exception and error messages that do not interpolate a value are quoted strings (`'Pace not found'`), never template literals; use a template literal only when the message interpolates.

### Domain Error Classes

Define a base error class per app/module with a `code` discriminant. Keep all related error classes in a single `errors.ts`:

```typescript
// errors.ts
export class AppError extends Error {
  constructor(
    public readonly code: string,
    message: string,
    public readonly statusCode: number = 500
  ) {
    super(message)
    this.name = this.constructor.name
  }
}

export class GoalNotFoundError extends AppError {
  constructor(goalId: string) {
    super('GOAL_NOT_FOUND', `Goal ${goalId} not found`, 404)
  }
}

export class NoExercisesPassedFilterError extends AppError {
  constructor() {
    super('NO_EXERCISES_PASSED_FILTER', 'No exercises passed the filter criteria', 422)
  }
}
```

### Error Handling at Boundaries

Controllers and queue processors are the error boundary - they catch domain errors and translate to HTTP status codes or queue retry decisions. Services should throw domain errors; they should not catch-and-rethrow without adding information.

### Result Types (Optional - Evaluate for New Projects)

> **Industry note:** The `neverthrow` library provides a `Result<T, E>` type that makes errors explicit in function signatures, preventing forgotten error handling. This is gaining traction in production TypeScript codebases (as of 2025). It aligns with the `std::expected<T, E>` pattern used in some sibling codebases in this org. Consider adopting for new services or modules where typed error propagation across service boundaries would reduce error-handling bugs. Do not retrofit into existing NestJS services that already use throw-based patterns - the migration cost is high and NestJS exception filters expect thrown errors.

If adopting `neverthrow`, wrap third-party calls (DB, Redis, HTTP) in `try/catch` at the infrastructure boundary and return `Result` from there:

```typescript
import { ok, err, Result } from 'neverthrow'

const findGoal = async (goalId: string): Promise<Result<IGoal, AppError>> => {
  try {
    const goal = await repository.findOne({ where: { id: goalId } })

    if (!goal) {
      return err(new GoalNotFoundError(goalId))
    }

    return ok(goal)
  } catch (e) {
    return err(new DatabaseError(e))
  }
}
```

## Async and Concurrency

- No floating promises.
- Use `void` for intentional fire-and-forget.
- Do not mark function `async` when it does not await.
- Use `Promise.all` for independent operations.
- Keep sequential `await` when order matters.

### `Promise.all` vs `Promise.allSettled`

- Use `Promise.all` when all operations must succeed for the overall operation to be valid (default choice).
- Use `Promise.allSettled` when partial success is acceptable and you need to inspect individual results (e.g., sending notifications to multiple users where some may fail).
- Never use `Promise.allSettled` as a lazy way to ignore errors - always inspect and handle the `rejected` entries.

### Parallelization across short-circuits

Before replacing sequential `await`s with `Promise.all`, check whether the second call is gated by a downstream early return on the first. Eager parallelization is correct only when both results are always needed.

When the first call's result can short-circuit the second, parallelizing pays for work the caller never needed AND converts a no-op path into a new failure point. The DB or network call that used to never run can now fail and propagate.

```typescript
// ÃƒÂ¢Ã‚ÂÃ…â€™ unsafe: when Tier 1 fills the result, Tier 2 was never needed,
// but it now runs unconditionally and any failure surfaces to the caller
const [tier1, tier2] = await Promise.all([
  this.repo.findPersonal(profileId),
  this.repo.findCommunityBodyAreas(profileId),
])
const result = personalize(tier1)
if (result.length >= max) {
  return result // tier2 work was wasted, and a tier2 failure would have killed this path
}

// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ keep sequential: tier2 only runs when tier1 did not fill the result
const tier1 = await this.repo.findPersonal(profileId)
const result = personalize(tier1)
if (result.length >= max) {
  return result
}
const tier2 = await this.repo.findCommunityBodyAreas(profileId)
```

Rule of thumb: if there is an `if (...) return` between the two `await`s in the sequential version, do not parallelize. The early return is communicating that tier 2 is conditional, and `Promise.all` erases that information.

### Avoiding Unnecessary `async`/`await`

When a function returns a single promise without needing to `await` intermediate results, return the promise directly instead of making the function `async`:

```typescript
// ÃƒÂ¢Ã‚ÂÃ…â€™ unnecessary async wrapper
const getData = async (id: string): Promise<IData> => {
  return await this.repository.findById(id)
}

// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ return promise directly
const getData = (id: string): Promise<IData> => {
  return this.repository.findById(id)
}
```

Exception: keep `async` when you need `try/catch` around the awaited call, or when the function has multiple `await` statements.

## Queue and Worker Patterns

The principles here (minimal payloads, idempotency, backoff, DLQ, graceful shutdown) are transport-neutral. **The async transport in these repos is AWS SQS** (standard queues, not FIFO); any BullMQ-style example is one concrete instantiation - map it to SQS (redrive-policy DLQ, visibility-timeout retries, per-record batch failures). Keep the underlying rules regardless of transport.

### Job Design

- Job payloads must be JSON-serializable - no class instances, no functions, no circular references.
- Keep payloads minimal - include IDs and metadata, not full entity objects. Let the worker fetch fresh data.
- Guarantee idempotency at the application layer so a redelivered message does not double-process (a DB unique key / events table, or a completion flag checked before side effects). Note: these repos use **standard** SQS queues, which do NOT deduplicate - native `MessageDeduplicationId` exists only on FIFO queues, which neither repo uses. Do not rely on transport-level dedup.

### Idempotency

Workers and webhook handlers must be idempotent. The same job or event processed twice must produce the same outcome:

- Check for completion before performing side effects (e.g., DB flag `emailSent` checked before sending).
- Use database transactions with unique constraints to guard against duplicate writes.
- Design external API calls to be idempotent (use idempotency keys where available).
- **The duplicate check must gate the entire processing pipeline.** If idempotency is enforced via `ON CONFLICT DO NOTHING` on an events table, that check must happen before any other writes in the same transaction. If the event is a duplicate, ALL side effects must be skipped - not just the event log insert. Partial idempotency (guarding one table but unconditionally upserting another) allows stale event replays to overwrite current state.
- **Webhook handlers must not reject unknown event types with 4xx.** Most webhook providers (Stripe, etc.) treat 4xx as permanent client errors and stop retrying. If the provider introduces new event types not yet in your enum, a 400 from DTO validation permanently drops those events with no recovery path. Instead: validate structure (auth header, JSON shape) strictly, but handle unknown `event.type` values gracefully - return 200, log to a failures/audit table, and skip processing.

### Retry and Backoff

- Use bounded retries with backoff - never infinite retries. On SQS this is the queue's `maxReceiveCount` + visibility timeout (a message reappears after the timeout and is retried until the receive count is exceeded); a BullMQ-style broker expresses the same idea as `{ attempts, backoff }`.
- Route permanently failed messages to a dead-letter queue after the retry limit. On SQS this is the source queue's redrive policy pointing at a DLQ; do not hand-roll a "give up" branch that silently drops the message.
- Report per-record success/failure so the transport only redelivers the records that actually failed (e.g. SQS partial-batch failure via `processSqsBatch`), rather than reprocessing an entire batch on one bad record.

### Graceful Shutdown

- Stop the consumer/worker from accepting new messages on shutdown, then let in-flight work finish. The call is transport-specific (`consumer.stop()` for an `sqs-consumer` loop; `worker.close()` for a BullMQ worker) - use the one the repo's queue package exposes, typically from an `onModuleDestroy` hook.
- Listen for `SIGINT` and `SIGTERM`; let in-flight work complete before exiting.
- Do not use `SIGKILL` in orchestration (Kubernetes, ECS, PM2) - give workers a grace period.

### Separation of Concerns

- API apps enqueue jobs only - no processing logic in the API process.
- Worker apps process jobs - they import queue definitions and register processors.
- Shared job types and queue names live in a shared location (e.g., `apps/<app>/src/shared/`) with cross-app duplication documented.

## Commenting and Documentation

Comment content (why, not what; narration vs constraints; TODO context; prose that contradicts code) follows `develop-code-quality`. TypeScript specifics:

- No `@ts-ignore` or `@ts-expect-error`; fix the underlying type issue instead.
- No `eslint-disable` unless there is a documented, unavoidable reason inline.

## Testing Alignment

- Use the project's shared setup helpers and factories when they exist.
- Keep assertions strict and aligned with contract.
- Keep tests deterministic and isolated.

## Architecture Principles

The general structure rules (separation of concerns, coupling, premature abstraction, pass-through chains, single-use helper files) live in `develop-code-quality`. TypeScript and NestJS specifics:

- Keep service/repository/controller boundaries clean.
- No over-modularization in single-purpose apps - lambdas/workers with one pipeline should use flat module structure, not `core/` + `feature/` hierarchies.
- No standalone helper files with functions used in exactly one place - inline as private methods.

### Module Boundaries in NestJS

- A module should represent a cohesive domain concept (users, routines, equipment), not a technical layer (all repositories in one module, all services in another).
- Cross-module imports are normal and expected - `FeatureModule` importing `MediaModule` is fine.
- Export only what other modules need. If a provider is only used internally, do not export it.
- When two modules develop tight bidirectional coupling (each importing from the other), merge them or extract a shared third module.
- Lazy-load modules (dynamic imports) only when startup time is measurably impacted - NestJS `LazyModuleLoader` adds complexity that is rarely justified.

### Event-Driven Patterns

Choose the right tool for the job:

- **Direct method call** (default) - for synchronous, in-process communication between services within the same module.
- **A durable message queue** - for async fire-and-forget work that needs retry, backoff, DLQ, or must survive process restarts (image processing, email, webhook delivery). In these repos that transport is **AWS SQS**; other stacks use BullMQ/Redis.
- **[if present] Redis Pub/Sub** - real-time fan-out where message loss is acceptable (e.g. cache-invalidation broadcasts). Only where a Redis layer exists.
- **[if present] NestJS `EventEmitter2`** (`@nestjs/event-emitter`) - in-process decoupling so multiple listeners react to one action without the producer knowing. Only where the event-emitter is registered.

#### In-Process Event Conventions

**[if present]** Applies only to repos that register `@nestjs/event-emitter`. A repo without it calls side-effect services directly (still keeping transactional side effects inline - see the constraint below). Domain events decouple core business logic from side effects (analytics, notifications, audit logging). The pattern:

1. **Define typed events** with `as const` event name constants and typed payload interfaces
2. **Emit from domain services** after core state transitions - emitting service does NOT import side-effect services
3. **Listen in side-effect modules** - `@OnEvent()` handlers react independently, using their own infrastructure (analytics APIs, Redis, etc.)
4. **Event-emitter is a decoupling mechanism**, not a replacement for existing infrastructure. Listeners still use the same services and databases.

```typescript
// Domain service - emits event, does NOT know about analytics
this.eventEmitter.emit(DOMAIN_EVENTS.ORDER_COMPLETED, { orderId, customerId, total })

// Analytics listener - reacts to event, uses real infrastructure
@OnEvent(DOMAIN_EVENTS.ORDER_COMPLETED)
public handleOrderCompleted(event: IOrderCompletedEvent): void {
  this.analyticsService.track(event.customerId, 'order_completed', { ... })
}
```

**Critical constraint: do NOT use events for transactional side effects.** If a side effect must be part of a DB transaction (e.g., awarding points, updating balances, creating linked records inside `dataSource.transaction()`), keep it as a direct method call. Events are fire-and-forget - they cannot participate in transaction rollback.

Avoid EventEmitter for anything that must survive a process crash - use queues instead.

### Graceful Shutdown

All long-lived Node.js processes (API servers, workers) must handle shutdown cleanly:

```typescript
// main.ts
app.enableShutdownHooks()
```

The shutdown sequence:

1. Stop accepting new requests/jobs.
2. Wait for in-flight requests/jobs to complete (with a timeout).
3. Close database connection pools.
4. Close other connections that are present (Redis, queue consumers, etc.).
5. Exit.

NestJS `OnModuleDestroy` and `BeforeApplicationShutdown` lifecycle hooks handle steps 2-4 when `enableShutdownHooks()` is called. Ensure every provider that holds a connection implements the appropriate hook.

### Health Checks

- Expose `/ping` (or `/health`) for load balancer probes - return 204 with no body.
- For richer health checks, verify connectivity to the critical dependencies the app actually has (database, and where present Redis / the queue) and return a structured response with per-dependency status.
- Keep health check handlers fast - they are called frequently. Do not run expensive queries.

## Code Quality

The language-neutral principles (behavior preservation, YAGNI, rule of three, indirection, safe direct assignment, redundant work, magic values, dead code, transactions, no compatibility shims) live in `develop-code-quality`; load it with this skill. TypeScript-specific additions:

1. No `any`; use `unknown` and narrow with type guards or validation.
2. Derive types from existing ones (`Pick`, `Omit`, `Partial`) instead of copy-pasting fields.
3. A request DTO, `Partial<T>` or patch object is a sparse source: never spread or `Object.assign` it into an entity, model or `copyWith` where an explicit `null` or `undefined` must not overwrite the stored value. Merge field by field with explicit keep-current semantics (`props.locale ?? this.locale`), or omit the key entirely. Normalizing `null` to `undefined` at the boundary (`locale ?? undefined`) is safe only when the receiver treats `undefined` as "no change" with an explicit early return; a spread still overwrites with `undefined`.

## Query and Data Access

- No SQL/ORM N+1 query patterns; verify query efficiency on touched paths.
- Fetch only needed columns; avoid over-fetching; paginate large result sets.
- HARD FAIL: for database-backed paginated results, perform both filtering and pagination in the database query layer; never filter/slice in memory.
- Define deterministic ordering for any user-visible list, pagination, queue, or time-sequenced processing.
- HARD FAIL: when `ORDER BY` is combined with `LIMIT`, the final sort key must be unique (typically a primary key like `id ASC`). Without it, equal-ranked rows can shuffle between calls, producing user-visible drift, flaky tests, and non-deterministic pagination. Worked example: `ORDER BY p.profile_count DESC, qo.text ASC LIMIT 5` is unsafe when `(profile_count, text)` can tie - add `qo.id ASC` as the last key. The same rule applies to in-memory `.sort()` followed by `.slice()` and to ORM `find({ order: {...}, take: N })`.
- Verify supporting indexes exist for new/changed query paths (including composites matching `WHERE` + `ORDER BY`); remove redundant indexes.
- No injection-prone patterns (SQL/NoSQL/command/template); use parameterization/safe APIs.
- No multi-write operations without a transaction boundary.

### TypeORM Patterns

**[TypeORM]** This entire subsection is TypeORM-specific (`QueryBuilder`, `EntityManager`, `softDelete`, `eager`, `dataSource.transaction`, PG error-code catches). In a **Drizzle** repo the same goals - parameterized queries, no N+1, explicit relation loading, transactional multi-writes, unique-violation handling - are achieved with `drizzle-orm`'s query builder, `db.transaction()`, and `.onConflictDoNothing()`/`.onConflictDoUpdate()`. Soft-delete is a convention, not a built-in: if (and only if) the Drizzle schema adopts a `deletedAt` column, filter it explicitly in every read and back uniqueness with a partial index `WHERE deleted_at IS NULL`. Read the principle, then use your ORM's idiom.

- Prefer QueryBuilder over raw SQL for type-safe, composable queries. Use raw SQL only for performance-critical queries where QueryBuilder overhead is measurable.
- Use `.select()` to fetch only needed columns in read-heavy paths.
- For relations, use explicit `leftJoinAndSelect` or `loadRelationCountAndMap` - do not rely on `eager: true` entity configuration (it causes implicit N+1 on every query).
- Wrap multi-entity writes in `queryRunner.startTransaction()` / `commitTransaction()` / `rollbackTransaction()`. Use `try/finally` to ensure `queryRunner.release()`.
- For migrations: one logical change per migration, write both `up` and `down`, keep migrations backward-compatible (add columns as nullable first, then backfill, then add NOT NULL in a follow-up migration).
- **Soft-delete cascading requires explicit ORM configuration.** DB-level `ON DELETE CASCADE` constraints only fire on hard deletes - TypeORM `softDelete(id)` does not trigger them. To cascade soft-deletes to child entities: (1) add `@DeleteDateColumn` to every child entity, (2) add `cascade: ['soft-remove', 'recover']` to the parent's `@OneToMany` relation, (3) load the parent with all relations via `findOne({ relations: [...] })`, then call `softRemove(entity)` instead of `softDelete(id)`.
- **Uniqueness with soft-deletes requires a partial unique index.** A plain `UNIQUE` constraint on a column prevents reuse of names/slugs after soft-delete because the deleted row still satisfies the constraint. Use a partial index `CREATE UNIQUE INDEX ... ON table (column) WHERE deleted_at IS NULL` so uniqueness is enforced only among active records. Enforce uniqueness at the application level too (query before write) for user-facing error messages - the DB index is a safety net, not a substitute for proper 409 responses.
- **Soft-delete bypasses DB-level FK constraints (`ON DELETE RESTRICT`).** TypeORM `softDelete`/`softRemove` sets `deleted_at` without triggering DB FK checks. An entity referenced by active children can be soft-deleted without error, leaving dangling references. The application layer must check for active references before soft-deleting and return 409 if any exist. Additionally, TypeORM's automatic `WHERE deleted_at IS NULL` filter does NOT apply to eagerly joined relations - a `leftJoinAndSelect` on a soft-deleted child will return `null`, causing DTO constructors that access `child.id` to throw TypeError ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ 500. Guard DTO constructors against null joined relations or filter soft-deleted rows in the query.
- **TOCTOU (Time-of-Check vs Time-of-Use) on unique constraints.** When a service checks for existence before inserting (e.g., `hasVotedToday()` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `save()`), a concurrent request can pass the check before the first request's insert commits. The application-level check provides a fast user-facing 409, but the DB unique index is the real safety net. Always handle both: (1) check first for a clean error message, (2) catch the unique constraint violation (`error.code === '23505'` in PostgreSQL) at the `save()` call and convert it to a `ConflictException`. Without the catch, the DB violation bubbles as a 500 instead of 409. This applies to any check-then-write pattern guarded by a unique index - dedup checks, idempotency keys, slug uniqueness, daily limits.

```typescript
// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ handle both the fast check and the DB constraint race
const hasVoted = await this.repository.hasVotedToday(profileId, label, today)
if (hasVoted) {
  throw new ConflictException('Already voted today')
}

try {
  await manager.save(VoteEntity, { profileId, label, votedDate: today })
} catch (error: unknown) {
  // Narrow instead of `as any` - QueryFailedError carries the driver error.
  if (error instanceof QueryFailedError && isUniqueViolation(error)) {
    throw new ConflictException('Already voted today')
  }
  throw error
}
```

- **Use `EntityManager` type for transaction manager parameters.** When a private method receives a manager from `dataSource.transaction()`, type the parameter as `EntityManager` - not a hand-rolled interface like `{ query: (sql: string, parameters: unknown[]) => Promise<unknown[]> }`. The custom interface masks eslint's `no-unsafe-assignment` checks and loses access to `EntityManager` methods like `findOne`, `save`, and `createQueryBuilder`.
- **Use `manager.query<T[]>(...)` generic instead of `as` cast.** `EntityManager.query()` returns `Promise<any>`. Always pass a generic type parameter to get typed results without `as` casts:

```typescript
// ÃƒÂ¢Ã‚ÂÃ…â€™ as cast - bypasses type safety, triggers no-unsafe-assignment
const rows = (await manager.query(`SELECT ...`, [id])) as { id: string }[]

// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ generic - typed at the call site
const rows = await manager.query<{ id: string }[]>(`SELECT ...`, [id])
```

- **Never catch unique constraint violations inside a transaction and continue.** When an `INSERT` fails with a unique violation (`23505`) inside a PostgreSQL transaction, the transaction enters an aborted state - all subsequent commands fail with `current transaction is aborted, commands ignored until end of transaction block`. The TOCTOU `try/catch` pattern above is safe because the catch re-throws or the transaction ends. But if you catch the violation and try to continue with more writes in the same transaction (e.g., catch a duplicate event insert and still commit the subscription upsert), the entire transaction rolls back silently. Use `ON CONFLICT DO NOTHING` (via QueryBuilder `.orIgnore()`) instead - it does not abort the transaction:

```typescript
// ÃƒÂ¢Ã‚ÂÃ…â€™ catch inside transaction - poisons the transaction, rolls back prior writes
try {
  await manager.save(EventEntity, { eventId, ... })
} catch (error: unknown) {
  if (isUniqueViolation(error)) {
    return true // transaction is already aborted - this "succeeds" but prior writes are lost
  }
  throw error
}

// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ orIgnore() - ON CONFLICT DO NOTHING, transaction stays healthy
const result = await manager.createQueryBuilder()
  .insert()
  .into(EventEntity)
  .values({ eventId, ... })
  .orIgnore()
  .execute()

return result.identifiers.length === 0 // true = duplicate (no insert happened)
```

## Preferred Patterns

The language-neutral patterns (one-off extraction, algorithm preservation, inline wrappers, trivial wrappers, single-use parameter wrappers and the typed-input disambiguator, passthrough methods, direct assignment and when it is unsafe, redundant expensive calls, magic values) live in `develop-code-quality` with TypeScript examples. TypeScript-specific patterns:

### No `any` - use `unknown` + narrowing

```typescript
// ÃƒÂ¢Ã‚ÂÃ…â€™
const data: any = await response.json()
data.name.toUpperCase()

// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦
const data: unknown = await response.json()
const parsed = UserSchema.parse(data)
parsed.name.toUpperCase()
```

### Derive types instead of copy-pasting fields

```typescript
// ÃƒÂ¢Ã‚ÂÃ…â€™
interface UserSummary {
  id: string
  name: string
}

// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦
type UserSummary = Pick<User, 'id' | 'name'>
```

### No barrel exports (except package entry files)

```typescript
// ÃƒÂ¢Ã‚ÂÃ…â€™ services/index.ts re-exporting siblings
export { UserService } from './user.service'
export { OrderService } from './order.service'

// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ import directly from source
import { UserService } from './services/user.service'
```

### Guard clause bracing (hard fail)

```typescript
// ÃƒÂ¢Ã‚ÂÃ…â€™ single-line return is not allowed
if (!user) return null

// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ always use braces + multiline
if (!user) {
  return null
}

if (!user.isActive) {
  return null
}

if (!hasPermission(user)) {
  return null
}
```

### No escape hatches

```typescript
// ÃƒÂ¢Ã‚ÂÃ…â€™
// @ts-ignore
// @ts-expect-error
// eslint-disable-next-line @typescript-eslint/no-unused-vars
const data: any = value

// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ fix the actual problem
const data: unknown = value
if (isUser(data)) { ... }
```

## Security Patterns

### Input Sanitization

- Validate and constrain all user input at the API boundary (Zod / class-validator).
- Use strict Zod schemas: prefer `.strict()` or default stripping behavior on object schemas to prevent unexpected fields from reaching business logic.
- Limit string lengths, array sizes, and numeric ranges in schemas to prevent resource exhaustion.

### Injection Prevention

- Never interpolate user input into SQL strings - use parameterized queries (both TypeORM and Drizzle parameterize by default; the risk is raw string-built SQL).
- Never interpolate user input into shell commands - use `child_process.execFile` (not `exec`) with argument arrays.
- Never interpolate user input into template strings that become HTML - use a templating engine with auto-escaping.

### JWT and Auth Token Handling

- Never log JWTs or auth tokens.
- Validate JWT expiry, issuer, and audience on every request (the repo's auth guard, e.g. a JWT guard, handles this).
- Do not store tokens in Redis or database unless absolutely necessary (and with encryption at rest).

### SSRF Prevention

- When accepting URLs from user input (webhooks, image URLs), validate against an allowlist of domains or reject private/internal IP ranges.
- Use a library or middleware that resolves DNS and checks the resulting IP before making the request.

### Rate Limiting

- Apply rate limiting at the API gateway or middleware layer (NestJS `@nestjs/throttler`).
- Use sliding window rate limiting per authenticated user ID (not just IP) to prevent abuse from authenticated users.

## Refactor Playbooks (TypeScript and NestJS)

How to run a refactor, prove it preserved behavior, and the language-neutral cleanup playbooks (indirection reduction, transformation reduction, redundant work, service chain collapse, re-export cleanup, dead code sweeps) live in `develop-refactoring`. The NestJS-specific playbook:

### Module flattening (single-purpose apps)

When a lambda or worker app has multiple NestJS modules (`core/`, `feature/`) but only one pipeline:

1. Identify whether the `core/` module contains any service with more than one consumer across modules.
2. If every `core/` service is consumed only by the feature module, merge all files into a single flat `module/` directory.
3. Inline standalone helper files (functions used in exactly one place) as private methods.
4. Merge thin wrapper services (1-method services around infrastructure calls like `redis.del()`, `readFile()`) into the consuming service.
5. Consolidate multiple type files into a single schema file when all types serve the same pipeline.
6. Merge multiple error files into a single `errors.ts`.
7. Drop redundant domain prefix from class names when the app scope already implies it (e.g., `ProcessingService` not `ImageProcessingService` inside `lambda-image-processing`).
8. Update the root module to a flat providers list - no sub-module imports.

## Validation Matrix

- module-local: targeted tests + typecheck + lint
- route/contract change: endpoint integration tests + status/payload verification
- quality gate: zero ESLint errors and zero TypeScript errors

## Deployment and Operations

### Database Schema Evolution

- One logical change per migration. Do not bundle unrelated schema changes.
- **[TypeORM]** write a `down` method that cleanly reverses the `up`. **[Drizzle]** migrations are generated forward-only `.sql` files with no `down` - reversal is a new forward migration; do not hand-add a down step.
- Backward-compatible changes: add nullable columns first, backfill data, then add constraints in a follow-up migration. This allows rollback without data loss. (ORM-neutral.)
- Never rename columns in a single migration - add new column, backfill, update application code, remove old column in a subsequent release. (ORM-neutral.)
- Dropping a column, table or enum value takes two releases. Release A stops reading and writing it while the schema still declares it (nullable, or with a default when a NOT NULL column is no longer written); release B, once A runs everywhere, drops it. Deploys run migrations before the new version takes traffic, and ORMs name every mapped column in their selects and inserts, so dropping in the same release makes the still-serving version fail with `column does not exist` until traffic shifts, and again after a rollback. Shipping both in one release is an owner decision that records the accepted downtime and lost rollback safety. (ORM-neutral.)
- Feature-flag schema changes when the new schema serves a feature that may be rolled back.

### Zero-Downtime Deploys

- Use rolling deployments (Kubernetes or ECS rolling update).
- Ensure database schema is backward-compatible with both old and new application versions during the rollout window.
- Drain connections before terminating old instances - NestJS `enableShutdownHooks()` combined with a readiness probe transition handles this.
- Queue workers: use `worker.close()` to stop accepting new jobs while finishing in-flight work, then exit.

## Anti-Patterns

Language-neutral anti-patterns (indirection, dead state, duplicated derivations, magic values, stale prose) are listed in `develop-code-quality`. TypeScript and NestJS ones:

- putting admin endpoints on the public controller (in repos with an admin split)
- leaving a controller's auth implicit - every controller must declare its protection with the repo's actual auth guard/decorator
- omitting the authenticated-user decorator (`@GetUser()` or the repo's equivalent) when the service needs the user's ID
- using `any` instead of `unknown` + narrowing
- `function` declarations instead of arrow functions
- `@ts-ignore` or `@ts-expect-error` instead of fixing the type issue
- copy-pasting type fields instead of deriving with `Pick`/`Omit`/`Partial`
- prefixing a type alias with `I` or `T` (the `I` prefix is for interfaces, `T` for generic parameters)
- unnecessary local barrels; orphan imports
- in-memory filtering/slicing for paginated results backed by database queries
- multi-module hierarchies (`core/` + `feature/`) in single-purpose apps (lambdas, workers) that have only one pipeline; use a flat module structure instead
- redundant domain prefix in class names when the app scope already implies the domain (e.g., `ImageProcessingService` inside `lambda-image-processing`)
- 1-method wrapper services around infrastructure calls (`CacheInvalidationService` wrapping `redis.del()`, `ConfigLoaderService` wrapping `readFile` + YAML parse)
- re-export type aliases that add no transformation (e.g., `export type { IBlurhashSchema }` from a file that imports it from another type file)
- split type files for one pipeline: config types, data types, and error types for the same domain scattered across 3+ files when they could be 1-2 files
- widening existing domain enums or named type aliases to anonymous `string`/`number` types
- no single-line `if` statements (including `return`, `throw`, `continue`, `break`); always use braces and multiline blocks
- no escape hatches: no `@ts-ignore`, no `@ts-expect-error`, no `eslint-disable`, no `any`
- no SQL/ORM N+1 query patterns
- no multi-write operations without a transaction boundary
- no injection-prone patterns (SQL/NoSQL/command/template)
- no API doc drift
- no unnecessary file splits
- no unsorted user-visible lists or paginated endpoints
- using `as` assertions to cast types when `satisfies` or proper narrowing would preserve safety
- defining Zod schemas inside functions instead of at module level
- validating the same data multiple times across different layers
- using `eager: true` on TypeORM relations (causes implicit N+1)
- logging sensitive data (tokens, passwords, PII)
- using `console.log` instead of structured logger in production code
- fire-and-forget queue jobs without idempotency guarantees
- using `Promise.allSettled` to silently swallow errors without inspecting results
- scattering shared constants (cache keys, time boundaries, event names) across module-local files instead of a single shared constants file
- duplicating time/date boundary logic inline instead of centralizing in shared helpers
- transactional side effects (point awards, balance updates, linked record creation) behind fire-and-forget event handlers - these must remain direct method calls inside transactions
- repositories that inject services or return API response DTOs - repositories are persistence-focused
- circular module dependencies - if Module A imports Module B and B imports A, restructure before adding features
- bare `boolean` fields in API response DTOs when a status/state enum is clearer and more extensible (e.g., `{ eligible: true, reason: null }` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `{ status: 'AVAILABLE' }`)
- client-computable fields in API responses - do not send data the client can trivially derive from other fields in the same response (e.g., `isToday` when `date` is already present)
- passing optional DTO fields directly to constructors or converters without handling `undefined` - `new Date(undefined)` produces `Invalid Date` (not a throw), which persists as a NaN timestamp and crashes the DB; always guard with `dto.field ? new Date(dto.field) : defaultValue`
- spreading a request DTO or `Partial<T>` into an entity, model or `copyWith` when an explicit `null` must not overwrite the stored value

## Monorepo-Only Addendum (Turbo/workspaces + `apps/`/`packages/`)

Apply this section only when all are true:

- the target repository is a Turbo/workspace monorepo
- the repository has an `apps/` and/or `packages/` folder at root
- TypeScript work targets code inside that monorepo repository

### Apps (Feature Modules)

Use predictable module layout (match the nearest existing module):

- `dto/`
- `repositories/`
- `services/`
- `<feature>.controller.ts`
- `<feature>-admin.controller.ts` **[if present]** (only when the repo has an admin app/role)
- `<feature>.module.ts`
- `<feature>.enums.ts` (or shared types)
- `_tests/`

An `entities/` folder appears **[TypeORM]** only; a Drizzle repo defines its model in the shared-domain schema package, not per-feature-module entities.

### Feature Module Wiring

```typescript
@Module({
  imports: [
    // [TypeORM] register entities; [Drizzle] omit - the DB handle is global:
    TypeOrmModule.forFeature([Entity1, Entity2]),
    ConfigModule.forFeature(featureConfig), // Module-scoped config (optional)
    // The next imports are [if present] - include only what this repo/module has:
    StorageModule.forRootAsync(), // [if present] object storage
    QueueModule.forRootAsync({ queues: [QUEUES.NAME] }), // [if present] async queue
    MediaModule, // shared utility module (example)
    PeerModule, // Cross-module imports are normal
  ],
  // FeatureAdminController / AdminFeatureService are [if present] - admin repos only:
  controllers: [FeatureController, FeatureAdminController],
  providers: [FeatureService, FeatureRepository, AdminFeatureService],
  exports: [FeatureService, FeatureRepository], // Only what others need
})
export class FeatureModule {}
```

### Shared Types Across Apps

A type needed by more than one app goes in the **shared-domain workspace package** so there is one definition and drift is caught at compile time. This is the default and what these repos do - do not create per-app copies under `apps/<app>/src/shared/`.

If you encounter a legacy manually-duplicated type (the same shape copied into two apps with a "keep identical" comment), treat it as debt: update every copy in the same change (grep the repo for the type name to find them all), and prefer migrating it into the shared-domain package rather than perpetuating the duplication.

### Cache Key Contracts

**[if present]** Only in repos with a cache layer. Cache keys defined in the shared-domain contracts cache module are referenced by every app that reads or invalidates them (workers via config, webhooks via invalidation code). When renaming a cache key, verify all surfaces that reference it (API constants, any worker/webhook config, invalidation code) so keys do not drift.

### Packages Exports and Imports

- Keep package public surface in `src/index.ts`.
- Barrel exports are banned everywhere else.
- Allowed exception: package entry file barrels (`packages/<n>/src/index.ts`) only.
- Prefer direct imports inside apps/modules over local barrels.

### Monorepo Build and Dependencies

- Keep `dependencies` in each app's `package.json` - do not hoist all dependencies to the root.
- Use `devDependencies` at the root only for shared tooling (ESLint, TypeScript, Prettier).
- When a shared package changes, run its own tests plus key downstream consumer tests before merging.
- Turborepo caching is based on file inputs - ensure `turbo.json` `inputs` patterns cover all relevant source files and configs to avoid stale caches.

### Additional Validation

- shared package touched: package tests + workspace typecheck/lint + key downstream tests
