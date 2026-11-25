# Custom Task Generation Workflow

You are an agent creating a task of the Android dev.

You work strictly according to the rules from [rules-core.md](rules-core.md). Violating any invariant is an error.

===============================================================================

## 1. CUSTOM TASK GENERATION DIALOG

Before starting the generation, you MUST ask the following questions in order if the user prompt has not answers:

1. **Feature name** or **Feature names** that should be modified for the task (if not stated explicitly). Offer the user to choose from existing ones (directories inside `<basePackage>/feature/`) or create new ones (comma-separated names). The user does not have to enter a feature name, so continue to the next step.
2. If you need any clarifying questions, ask them.

Remember the answers and use them when generating all layers.

===============================================================================

## 2. CUSTOM TASK GENERATION WORKFLOW

1. Run Custom Task Generation Dialog ([Section 1](#1-custom-task-generation-dialog)).
2. Determine FeatureName or several FeatureNames (PascalCase) (if needed).
3. Inspect the affected feature: existing layers, repository contract, UiState naming, tests.
4. Prepare the plan to solve the task and ask the user to apply or input changes.
5. When the user approves the plan — generate code that resolves the task:
    - Module structure: [Section 3](rules-core.md#3-module-structure-strict) of [rules-core.md](rules-core.md)
    - New files and dirs generation order: [Section 2](full-feature-gen-workflow.md#2-full-feature-generation-workflow) of [full-feature-gen-workflow.md](full-feature-gen-workflow.md)
    - Presentation artifacts: `<FeatureName>UiState`, `<FeatureName>UiEvent`, `<FeatureName>UiEffect`
6. Generate or update tests:
    - `app/src/test/java/<basePackage>/feature/<featureName>/domain/usecase/<Action>UseCaseTest.kt` (if needed)
    - `app/src/test/java/<basePackage>/feature/<featureName>/presentation/<FeatureName>ViewModelTest.kt` (if needed)
    - `app/src/androidTest/java/<basePackage>/feature/<featureName>/presentation/<FeatureName>ViewTest.kt` (if needed)
7. Add new navigation config and new AppNavGraph destination (if needed).
8. Run the validation checklist before printing the result.
9. Print result as specified: [output-format.md](output-format.md).
