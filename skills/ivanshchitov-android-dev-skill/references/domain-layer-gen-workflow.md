# Domain Layer Generation Workflow

You are an agent creating the Domain layer of the Android app feature slice.

You work strictly according to the rules from [rules-core.md](rules-core.md). Violating any invariant is an error.

===============================================================================

## 1. DOMAIN LAYER GENERATION DIALOG

Before starting the generation, you MUST ask the following questions in order if the user prompt has not answers:

1. **Feature name** where the Domain layer should be added (if not stated explicitly). Offer the user to choose from existing ones (directories inside `<basePackage>/feature/`) or create a new one.
2. Which DataSources exist for this feature: Local, Remote, both, or none? The answer defines the repository contract (see `rules-core.md` 2.4).
3. If you need any clarifying questions, ask them.

Remember the answers and use them when generating all layers.

===============================================================================

## 2. DOMAIN LAYER GENERATION WORKFLOW

1. Run Domain Layer Generation Dialog ([Section 1](#1-domain-layer-generation-dialog)).
2. Determine FeatureName (PascalCase).
3. Choose the repository contract using [Section 2.4](rules-core.md#24-repository-sync-contract-strict) of [rules-core.md](rules-core.md). Do not declare methods that have no DataSource behind them.
4. Create directories according to the structure from [Section 3](rules-core.md#3-module-structure-strict) of [rules-core.md](rules-core.md). ONLY for Domain layer (ask the user if you need to create more dirs).
5. Generate files in the following order:
   - `feature/<featureName>/`
      - `domain/error/<FeatureName>Error.kt`
      - `domain/model/<Model>.kt`
      - `domain/repository/<FeatureName>Repository.kt`
      - `domain/usecase/<Action>UseCase.kt` (one UseCase for one action; the set follows the repository contract)
      - `di/<FeatureName>Module.kt` (or modify the file if it already exists)
6. Add the `<FeatureName>Module.kt` to `App.kt` into `startKoin { modules(...) }` (if needed).
7. Generate tests:
   - `app/src/test/java/<basePackage>/feature/<featureName>/domain/usecase/<Action>UseCaseTest.kt`
8. Print result as specified: [output-format.md](output-format.md).
