# Dependency baseline

Reference values for a new project. **Not a source of truth**: verify every row before use.

- Last verified: 2026-11-02
- Check Google Maven: `https://maven.google.com/web/index.html`
- Check Maven Central: `https://search.maven.org`
- Check the Kotlin/AGP compatibility matrix: `https://developer.android.com/build/releases/gradle-plugin`

| Artifact | Baseline |
|---|---|
| Kotlin | 2.2.0 |
| Android Gradle Plugin | 9.0.0 |
| Koin | 4.2.2 |
| Room | 2.8.4 |
| Kotlin Coroutines | 1.11.0 |
| AndroidX Lifecycle | 2.9.0 |
| Paging | 3.3.6 |
| kotlinx-collections-immutable | 0.4.0 |
| Turbine | 1.2.0 |

## Rules

- An existing project always wins: read its `gradle/libs.versions.toml` and reuse the versions.
- Do not bump dependencies as part of a feature task.
- For a new project, verify the rows above and replace them with the current stable versions.
- If a version cannot be verified, ask the user instead of guessing.
