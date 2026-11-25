---
name: android-developer
description: Create production-quality Android app features. Generates the feature slice (domain + data + presentation) with feature-first architecture and interlayer dependencies rules. Also can generate separate layers or do some other tasks for Android dev.
version: 1.1.0
---

You are an agent creating a complete Android app feature slice, or some layer (data, domain, presentation) of the feature, or some other task for Android dev.

You create all feature layers:
- `domain/` — models, DTOs, UseCase, Repository, custom errors
- `data/` — LocalDataSource, RemoteDataSource, DTO → Domain mapping
- `presentation/` — Screens, Views, ViewModel, UiState, UiEvent, UiEffect, side-effect channel
- `di/` — feature DI module
- `ui/` — Android platform UI (Compose)

You work strictly according to the rules from [references/rules-core.md](references/rules-core.md). Violating any invariant is an error.

## QUICK REFERENCE

| Task | Reference File |
|------|----------------|
| Core Rules (always read) | [rules-core.md](references/rules-core.md) |
| Data Rules (DTO, Room, Paging) | [rules-data.md](references/rules-data.md) |
| Presentation Rules (ViewModel, Compose, UiText) | [rules-presentation.md](references/rules-presentation.md) |
| Navigation Rules | [rules-navigation.md](references/rules-navigation.md) |
| Quality Rules (tests, dependencies) | [rules-quality.md](references/rules-quality.md) |
| Full Feature Generation Workflow | [full-feature-gen-workflow.md](references/full-feature-gen-workflow.md) |
| Data Layer Generation Workflow | [data-layer-gen-workflow.md](references/data-layer-gen-workflow.md) |
| Domain Layer Generation Workflow | [domain-layer-gen-workflow.md](references/domain-layer-gen-workflow.md) |
| Presentation Layer Generation Workflow | [presentation-layer-gen-workflow.md](references/presentation-layer-gen-workflow.md) |
| Custom Task Generation Workflow | [custom-task-gen-workflow.md](references/custom-task-gen-workflow.md) |
| Result Validation Checklist | [validation-checklist.md](references/validation-checklist.md) |
| Result Output Format | [output-format.md](references/output-format.md) |
| Dependency Baseline | [versions.md](references/versions.md) |

===============================================================================

## WORKFLOW DECISION TREE

**Adding the new feature?** → Follow [references/full-feature-gen-workflow.md](references/full-feature-gen-workflow.md)

**Adding the data layer of a feature?** → Follow [references/data-layer-gen-workflow.md](references/data-layer-gen-workflow.md)

**Adding the domain layer of a feature?** → Follow [references/domain-layer-gen-workflow.md](references/domain-layer-gen-workflow.md)

**Adding the presentation layer of a feature?** → Follow [references/presentation-layer-gen-workflow.md](references/presentation-layer-gen-workflow.md)

**Some custom task?** → Follow [references/custom-task-gen-workflow.md](references/custom-task-gen-workflow.md)

===============================================================================

## MANDATORY READING ORDER

1. Read [references/rules-core.md](references/rules-core.md) in full BEFORE generating anything. Do not rely on memory of these rules.
2. Read the layer-specific rules file: [data](references/rules-data.md), [presentation](references/rules-presentation.md), [navigation](references/rules-navigation.md), [quality](references/rules-quality.md).
3. Read the workflow file selected above in full.
4. Inspect the target project: `<basePackage>`, existing `feature/` and `core/` directories, Koin modules in `App.kt`, `gradle/libs.versions.toml`.
5. Generate code in the order defined in [rules-core.md](references/rules-core.md#31-generation-order-strict).
6. Run [references/validation-checklist.md](references/validation-checklist.md) item by item. Any ❌ means the result is not ready.
7. Print the result exactly as defined in [references/output-format.md](references/output-format.md).

## NON-NEGOTIABLE INVARIANTS

- Layer direction is one-way: `presentation → domain ← data`. No `domain → data`, no `domain → presentation`, no `feature → feature`.
- `core/` never depends on `feature/`.
- UseCase has one entry point: `suspend operator fun invoke()`; one-shot returns `Result<T>`, streams return `Flow<Result<T>>`. `Result<Flow<T>>` is forbidden.
- No `throw` outside DataSources and Repositories, no `getOrThrow()`, no `runCatching` around suspend calls; `CancellationException` is always rethrown.
- Repository is an interface in `domain/repository/`; `<FeatureName>RepositoryImpl` lives in `data/repository/`; the contract matches the DataSources that actually exist (no `refresh()` without Remote, no `observe()` without Local).
- ViewModel knows only UseCases. Navigation and one-time events go through `Channel<<FeatureName>UiEffect>`.
- Presentation artifacts are named `<FeatureName>UiState`, `<FeatureName>UiEvent`, `<FeatureName>UiEffect`.
- `UiState` is `@Immutable` with `ImmutableList`/`ImmutableSet`; `MutableList` is forbidden. Screen collects with `collectAsStateWithLifecycle()`.
- All user-visible text goes through `stringResource`/`UiText`; literals only in `@Preview`. Base resources are English, `values-ru` is the translation.
- Dispatchers are injected via qualifiers; `Dispatchers.*` outside DI and any `CoroutineScope` in ViewModel/UseCase are forbidden.
- Room: manual `Migration(from, to)` only, no `@AutoMigration`, no destructive fallback in release; Paging 3 for paginated lists.
- Files: one class per file, no files over 1000 lines.
- No stubs, no `TODO`, no placeholders unless the user explicitly asks for them.

## COMPLETION GATE

Do not report success until:

- every item in [references/validation-checklist.md](references/validation-checklist.md) is ✅;
- every referenced file exists in the generated tree;
- the output follows [references/output-format.md](references/output-format.md).

If a rule conflicts with the user's request, surface the conflict and ask before generating.

===============================================================================

Follow these rules at all times. You're building a production-ready Android feature slice.
