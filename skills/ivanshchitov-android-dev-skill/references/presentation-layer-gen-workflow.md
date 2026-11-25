# Presentation Layer Generation Workflow

You are an agent creating the Presentation layer of the Android app feature slice.

You work strictly according to the rules from [rules-core.md](rules-core.md). Violating any invariant is an error.

===============================================================================

## 1. PRESENTATION LAYER GENERATION DIALOG

Before starting the generation, you MUST ask the following questions in order if the user prompt has not answers:

1. **Feature name** where the Presentation layer should be added (if not stated explicitly). Offer the user to choose from existing ones (directories inside `<basePackage>/feature/`) or create a new one.
2. Do the UseCases already exist? If not, ask the user to generate the Domain layer first, or explicitly approve temporary stubs.
3. If you need any clarifying questions, ask them.

Remember the answers and use them when generating all layers.

===============================================================================

## 2. PRESENTATION LAYER GENERATION WORKFLOW

1. Run Presentation Layer Generation Dialog ([Section 1](#1-presentation-layer-generation-dialog)).
2. Determine FeatureName (PascalCase).
3. Create directories according to the structure from [Section 3](rules-core.md#3-module-structure-strict) of [rules-core.md](rules-core.md). ONLY for Presentation layer (ask the user if you need to create more dirs).
4. Generate files in the following order:
   - `core/ui/UiText.kt` (if missing)
   - `feature/<featureName>/`
      - `domain/error/<FeatureName>Error.kt` (if needed)
      - `domain/model/<Model>.kt` (if needed)
      - `presentation/mvi/<FeatureName>UiState.kt`
      - `presentation/mvi/<FeatureName>UiEvent.kt`
      - `presentation/mvi/<FeatureName>UiEffect.kt` (if needed)
      - `presentation/model/<Model>Ui.kt` (if the ViewModel pre-formats values)
      - `presentation/mapper/<FeatureName>UiMapper.kt` (domain error → UiText)
      - `presentation/viewmodel/<FeatureName>ViewModel.kt`
      - `presentation/ui/<FeatureName>Screen.kt`
      - `presentation/ui/<FeatureName>View.kt`
      - `di/<FeatureName>Module.kt` (or modify the file if it already exists)
5. Add strings to `res/values/strings.xml` (English) and `res/values-ru/strings.xml` (Russian).
6. Add the `<FeatureName>Module.kt` to `App.kt` into `startKoin { modules(...) }` (if needed).
7. Generate tests:
   - `app/src/test/java/<basePackage>/feature/<featureName>/presentation/<FeatureName>ViewModelTest.kt`
   - `app/src/androidTest/java/<basePackage>/feature/<featureName>/presentation/<FeatureName>ViewTest.kt`
8. Add new navigation config and new AppNavGraph destination (if needed).
9. Print result as specified: [output-format.md](output-format.md).
