# Full Feature Generation Workflow

You are an agent creating a complete Android app feature slice.

You create a complete feature slice. The canonical list of layers is in [SKILL.md](../SKILL.md); do not duplicate it here.

You work strictly according to the rules from [rules-core.md](rules-core.md). Violating any invariant is an error.

===============================================================================

## 1. FULL FEATURE GENERATION DIALOG

Before starting the generation, you MUST ask the following questions in order if the user prompt has not answers:

1. **Feature name** (if not stated explicitly). If a feature with such name already exists (`feature/<featureName>`) tell about it and ask for another feature name.
2. Is the LocalDataSource needed (the feature has local storage or not)?
3. Is the RemoteDataSource needed (the feature has network layer or not)?
4. Is the data list paginated (does the API return pages)? If yes, Paging 3 is mandatory.
5. If you need any clarifying questions, ask them.

Remember the answers and use them when generating all layers.

===============================================================================

## 2. FULL FEATURE GENERATION WORKFLOW

1. Run Feature Generation Dialog ([Section 1](#1-full-feature-generation-dialog)).
2. Determine FeatureName (PascalCase).
3. Choose the repository contract from the answers using [Section 2.4](rules-core.md#24-repository-sync-contract-strict) of [rules-core.md](rules-core.md). Do not generate UseCases for methods the contract does not have.
4. Create directories according to the structure from [Section 3](rules-core.md#3-module-structure-strict) of [rules-core.md](rules-core.md).
5. Generate files, resources and DI wiring in the order defined in [Section 3.1](rules-core.md#31-generation-order-strict) of [rules-core.md](rules-core.md).
6. Generate tests:
   - `app/src/test/java/<basePackage>/feature/<featureName>/domain/usecase/<Action>UseCaseTest.kt`
   - `app/src/test/java/<basePackage>/feature/<featureName>/presentation/<FeatureName>ViewModelTest.kt`
   - `app/src/androidTest/java/<basePackage>/feature/<featureName>/presentation/<FeatureName>ViewTest.kt`
7. Add new navigation config and new AppNavGraph destination (if needed).
8. Print result as specified: [output-format.md](output-format.md).
