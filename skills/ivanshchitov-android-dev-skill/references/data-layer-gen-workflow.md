# Data Layer Generation Workflow

You are an agent creating the Data layer of the Android app feature slice.

You work strictly according to the rules from [rules-core.md](rules-core.md). Violating any invariant is an error.

===============================================================================

## 1. DATA LAYER GENERATION DIALOG

Before starting the generation, you MUST ask the following questions in order if the user prompt has not answers:

1. **Feature name** where the Data layer should be added (if not stated explicitly). Offer the user to choose from existing ones (directories inside `<basePackage>/feature/`) or create a new one.
2. Is the LocalDataSource needed (the feature has local storage or not)?
3. Is the RemoteDataSource needed (the feature has network layer or not)?
4. Is the data list paginated (does the API return pages)? If yes, Paging 3 is mandatory.
5. If you need any clarifying questions, ask them.

Remember the answers and use them when generating all layers.

===============================================================================

## 2. DATA LAYER GENERATION WORKFLOW

1. Run Data Layer Generation Dialog ([Section 1](#1-data-layer-generation-dialog)) if needed.
2. Determine FeatureName (PascalCase).
3. Choose the repository contract from the answers using [Section 2.4](rules-core.md#24-repository-sync-contract-strict) of [rules-core.md](rules-core.md).
4. Create directories according to the structure from [Section 3](rules-core.md#3-module-structure-strict) of [rules-core.md](rules-core.md). ONLY for Data layer (ask the user if you need to create more dirs).
5. Generate files in the following order:
   - `core/database/`
      - `entity/<Model>Entity.kt` (if needed)
      - `dao/<Model>Dao.kt` (if needed)
      - `converter/<Model>Converter.kt` (if needed)
      - `migration/Migration<V1>To<V2>.kt` (if the schema changes)
      - `dao/<Model>PagingSource.kt` (if paginated)
   - `feature/<featureName>/`
      - `data/dto/<Model>Dto.kt`
      - `data/mapper/<FeatureName>Mapper.kt`
      - `data/datasource/<FeatureName>RemoteDataSource.kt` (if needed)
      - `data/datasource/<FeatureName>LocalDataSource.kt` (if needed)
      - `data/datasource/<FeatureName>Api.kt` (if needed)
      - `data/repository/<FeatureName>RepositoryImpl.kt`
      - `di/<FeatureName>Module.kt` (or modify the file if it already exists)
6. Add the `<FeatureName>Module.kt` to `App.kt` into `startKoin { modules(...) }` (if needed).
7. Generate tests for non-trivial mapping or queries:
   - `app/src/test/java/<basePackage>/feature/<featureName>/data/<FeatureName>RepositoryTest.kt`
8. Print result as specified: [output-format.md](output-format.md).
