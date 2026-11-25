# DI Framework Selection

The skill supports two DI frameworks — **Koin** and **Hilt**. Each project uses exactly one of them. Before generating any DI code (feature `di/` module, ViewModel wiring, `App.kt` entry), determine the framework for the project.

## 1. Detect the framework in the project

Inspect the existing project — version catalog (`gradle/libs.versions.toml`), `App.kt`/`Application`, `MainActivity.kt`, `build.gradle.kts`:

| Indicator | Koin | Hilt |
|---|---|---|
| Version catalog (`gradle/libs.versions.toml`) | `koin-android`, `koin-androidx-compose` | `hilt-android`, `hilt-navigation-compose` |
| Gradle plugin in `build.gradle.kts` | none (Koin needs no plugin) | `com.google.dagger.hilt.android` + KSP `com.google.devtools.ksp` |
| `Application` | `class App : Application()` with `startKoin { ... }` in `onCreate` | `@HiltAndroidApp class App : Application()` |
| `Activity` | plain | `@AndroidEntryPoint` |
| ViewModel in Compose | `koinViewModel()` | `hiltViewModel()` |
| Feature DI module | `val <feature>Module = module { ... }` | `@Module @InstallIn(SingletonComponent::class) object <Feature>Module` |

## 2. Decision rule

1. **Project already has DI** → detect the framework (table above) and **follow the existing choice**. Generate all DI code with that framework. Never switch frameworks mid-project and never mix them.
2. **Project has NO DI** → **ask the user** which framework to use: **Koin** or **Hilt**. Do not guess. Offer a recommendation only if asked:
   - **Hilt** — official Google solution over Dagger, graph validated at compile time, industrial standard.
   - **Koin** — lightweight runtime DSL, less ceremony, no annotation processing.
3. Remember the choice and reuse it for every feature of the project (consistent across the whole session).

## 3. Koin patterns

Feature module — `feature/<featureName>/di/<FeatureName>Module.kt`:

```kotlin
val authModule = module {
    single { AuthRemoteDataSource(get(), get()) }
    single { AuthLocalDataSource(get()) }
    single { AuthRepository(get(), get()) }
    factory { LoginUseCase(get()) }
    viewModel { (onNavigateToMain: () -> Unit) ->
        AuthViewModel(get(), onNavigateToMain)
    }
}
```

Register the module in the application entry — `App.kt`:

```kotlin
class App : Application() {
    override fun onCreate() {
        super.onCreate()
        startKoin {
            androidContext(this@App)
            modules(
                databaseModule,
                networkModule,
                preferencesModule,
                authModule,
                profileModule,
            )
        }
    }
}
```

ViewModel in Compose — `koinViewModel()`:

```kotlin
@Composable
fun AuthScreen(viewModel: AuthViewModel = koinViewModel()) { ... }
```

Koin DSL rules:

- `single { }` — one instance per app (repositories, DAOs, Retrofit services)
- `factory { }` — a new instance per request (UseCases)
- `viewModel { }` — scoped to the ViewModel lifecycle (from `org.koin.androidx.viewmodel.dsl.viewModel`)
- `get()` — resolves a dependency by type inside a definition

## 4. Hilt patterns

Feature module — `feature/<featureName>/di/<FeatureName>Module.kt`:

```kotlin
@Module
@InstallIn(SingletonComponent::class)
object AuthModule {

    @Provides
    @Singleton
    fun provideAuthRemoteDataSource(api: AuthApi): AuthRemoteDataSource =
        AuthRemoteDataSource(api)

    @Provides
    @Singleton
    fun provideAuthLocalDataSource(db: AuthDatabase): AuthLocalDataSource =
        AuthLocalDataSource(db)

    @Binds
    @Singleton
    abstract fun bindAuthRepository(impl: AuthRepositoryImpl): AuthRepository
}
```

Rules:

- `@Provides` — factory method for third-party types (Room database, Retrofit, DataStore); method parameters are resolved from the graph.
- `@Binds` — binds an interface to its implementation; the function is abstract, no body.
- `@Singleton` — one instance per app (repositories, DAOs, Retrofit services).
- **No manual registration**: `@InstallIn(SingletonComponent::class)` is discovered automatically by the `@HiltAndroidApp` root. Do not add Hilt modules to any `modules(...)` list.

Application entry:

```kotlin
@HiltAndroidApp
class App : Application()

@AndroidEntryPoint
class MainActivity : ComponentActivity()
```

ViewModel — `@HiltViewModel` + `@Inject constructor`:

```kotlin
@HiltViewModel
class AuthViewModel @Inject constructor(
    private val loginUseCase: LoginUseCase,
) : ViewModel() { ... }
```

ViewModel in Compose — `hiltViewModel()`:

```kotlin
@Composable
fun AuthScreen(viewModel: AuthViewModel = hiltViewModel()) { ... }
```

Hilt and navigation callbacks: `@Inject constructor` cannot inject lambda parameters (e.g. `onNavigateToMain`). Prefer the SideEffect pattern for navigation (Section 9.4 of `rules.md`). If an assisted parameter is truly required, use `@AssistedInject` + `SavedStateHandle`.

Hilt dependencies in `gradle/libs.versions.toml`:

```toml
[versions]
# Hilt version must be compatible with the Kotlin/AGP version of the project
hilt = "2.56.2"
androidx-hilt = "1.2.0"
# KSP version is tied to the Kotlin version, e.g. 2.2.0-2.0.4
ksp = "2.2.0-2.0.4"

[libraries]
hilt-android = { group = "com.google.dagger", name = "hilt-android", version.ref = "hilt" }
hilt-android-compiler = { group = "com.google.dagger", name = "hilt-android-compiler", version.ref = "hilt" }
hilt-navigation-compose = { group = "androidx.hilt", name = "hilt-navigation-compose", version.ref = "androidx-hilt" }

[plugins]
hilt = { id = "com.google.dagger.hilt.android", version.ref = "hilt" }
ksp = { id = "com.google.devtools.ksp", version.ref = "ksp" }
```

In `app/build.gradle.kts` the Hilt plugin and compiler must be wired:

```kotlin
plugins {
    alias(libs.plugins.hilt)
    alias(libs.plugins.ksp)
}

dependencies {
    implementation(libs.hilt.android)
    ksp(libs.hilt.android.compiler)
    implementation(libs.hilt.navigation.compose)
}
```