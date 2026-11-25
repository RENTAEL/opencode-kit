# Rules — core (always read)

This is one part of the rule set. Section numbers are local to this file; cross-file
references name the file. The file map is in
`../SKILL.md`. Read `rules-core.md` first, then the file for the layer you generate.

===============================================================================

## 1. ARCHITECTURE OVERVIEW

```
┌────────────────────────────────────────────────────┐
│               Presentation Layer                   │
│  ┌──────────────┐    ┌─────────────────────────┐   │
│  │   Screen     │◄───│      ViewModel          │   │
│  │  (Compose)   │    │  (StateFlow<State>)     │   │
│  │  Event -->   │───►│  onEvent(Event)         │   │
│  └──────────────┘    └───────────┬─────────────┘   │
├──────────────────────────────────┼─────────────────┤
│                  Domain Layer    │                 │
│              ┌───────────────────▼──────┐          │
│              │       Use Cases          │          │
│              │  (combine/transform)     │          │
│              └───────────┬──────────────┘          │
├──────────────────────────┼─────────────────────────┤
│                  Data Layer                        │
│  ┌───────────────────────▼──────────────────────┐  │
│  │              Repository                      │  │
│  │    (offline-first, single source of truth)   │  │
│  └─────────┬─────────────────────┬──────────────┘  │
│            │                     │                 │
│  ┌─────────▼─────────┐  ┌───────▼──────────────┐   │
│  │  Local DataSource │  │  Remote DataSource   │   │
│  │   (Room + DAO)    │  │     (Retrofit)       │   │
│  └───────────────────┘  └──────────────────────┘   │
└────────────────────────────────────────────────────┘
```

Three-layer architecture with unidirectional data flow (UDF):
- **Intents flow DOWN** (`Presentation → ViewModel → Domain → Data`)
- **State flows UP** (`Data → Domain → ViewModel → Presentation`)
- **Local storage is source of truth**

## 2. LAYERS RULES (STRICT)

### 2.1 Domain layer

- `domain/model/` depends only on: Kotlin primitives, other domain models of this feature, `core/` shared entities.
- `domain/usecase/` depends only on: `domain/repository/`, `domain/error/`, `core/` utilities, other UseCase of the same feature.
- `domain/repository/` depends only on: `domain/model/`. It declares an interface and never mentions DataSources, DTOs or Room entities.

PROHIBITED: domain → presentation, domain → data directly (UseCase doesn't know about DataSource), domain → other feature/.

### 2.2 Data layer

- `data/dto/` depends only on: Kotlinx Serialization annotations.
- `data/mapper/` depends only on: data/dto/, domain/model/.
- `data/datasource/` depends only on: `core/network/` (Remote), `core/database/` (Local), `data/dto/`.
- `data/repository/` depends on: `domain/repository/`, `domain/model/`, `data/datasource/`, `data/mapper/`. This is the only place where DTO/Entity → Domain mapping happens.

**Principles**:
- **Offline-first** (when both DataSources exist): Local database is the source of truth
- **Repository pattern**: Single public API for data access
- **Reactive streams**: Persisted data is exposed as `Flow<T>`; one-shot operations are `suspend`

PROHIBITED: DataSource → UseCase, DataSource → ViewModel, DataSource → other feature/, DataSource → other DataSource.

### 2.3 Presentation layer

- `presentation/viewmodel/` depends only on: `domain/usecase/`, `domain/error/`, `presentation/mvi/`, `presentation/mapper/`, `core/ui/` (`UiText`), `navigation/`

PROHIBITED: ViewModel → Repository, ViewModel → DataSource, ViewModel → other feature/ (navigation is only possible via sealed Config in `navigation/`).

### 2.4 Repository sync contract (STRICT)

The repository contract is derived from the DataSources that actually exist. Never generate a
method without a DataSource behind it.

| Local | Remote | Contract | Source of truth |
|---|---|---|---|
| yes | yes | `observe(): Flow<T>` + `suspend refresh()` | Room |
| yes | no | `observe(): Flow<T>` + write methods (`save`, `delete`); no `refresh()` | Room |
| no | yes | `suspend fun get(): List<T>` (`Flow` only for push channels) | network |
| no | no | do not generate a repository — stop and ask the user | — |

- Offline-first is only the Local + Remote case: `observe()` reads Room, `refresh()` writes network data into Room. The UI never waits for the network.
- `refresh()` is not part of the interface when there is no RemoteDataSource, and `observe()` is not part of it without LocalDataSource.
- Repositories throw on failure. UseCases catch exceptions and convert them into `Result<T>` / `Flow<Result<T>>` with `<FeatureName>Error`. A repository never returns `Result`.
- The UseCase set follows the contract: observation UseCases require Local, refresh UseCases require Remote. Never generate a UseCase for a method that does not exist.

```kotlin
// Local + Remote (offline-first)
interface HistoryRepository {
    fun observeRecords(): Flow<List<Record>>
    suspend fun refresh()
}
```

```kotlin
// Local only
interface HistoryRepository {
    fun observeRecords(): Flow<List<Record>>
    suspend fun save(record: Record)
}
```

```kotlin
// Remote only
interface HistoryRepository {
    suspend fun getRecords(): List<Record>
}
```

===============================================================================

## 3. MODULE STRUCTURE (STRICT)

```
app/src/main/java/<basePackage>/
├── App.kt                       # Koin startup - loads all DI modules
├── MainActivity.kt              # Entry point
├── navigation/                  # COMMON NAVIGATION
│   │   ├── NavigationConfig.kt  # Type-Safe Navigation config
│   │   └── AppNavGraph.kt       # The central NavHost graph definition
├── core/                        # SHARED CODE
│   ├── di/                      # Koin modules (Dispatcher, Database, Network, Preferences)
│   ├── network/                 # Retrofit setup + ApiConfig
│   ├── database/                # Room AppDatabase
│   │   ├── dao/                 # DAOs
│   │   ├── entity/              # Entities
│   │   ├── converter/           # TypeConverters
│   │   └── migration/           # Manual migrations, one file per migration
│   ├── preferences/             # DataStore Preferences
│   └── ui/                      # Material 3 theme, Spacing, UiText, shared composable
└── feature/                     # BUSINESS FEATURES
    └── <featureName>/           # e.g. feature 'history'
        ├── data/
        │   ├── dto/             # DTO-classes (@Serializable)
        │   ├── datasource/      # LocalDataSource, RemoteDataSource, Retrofit API
        │   ├── mapper/          # Entity/DTO <-> Domain mapping
        │   └── repository/      # <FeatureName>RepositoryImpl.kt — domain repository implementation
        ├── domain/
        │   ├── model/           # Data classes, value objects
        │   ├── error/           # <FeatureName>Error.kt (sealed class)
        │   ├── repository/      # <FeatureName>Repository.kt (interface)
        │   └── usecase/         # UseCase-classes
        ├── presentation/
        │   ├── mvi/             # <FeatureName>UiState.kt, <FeatureName>UiEvent.kt, <FeatureName>UiEffect.kt
        │   ├── model/           # <Model>Ui.kt — presentation models with pre-formatted values
        │   ├── mapper/          # <FeatureName>UiMapper.kt — domain error → UiText
        │   ├── viewmodel/       # <FeatureName>ViewModel.kt
        │   └── ui/              # <FeatureName>Screen.kt, <FeatureName>View.kt, Composable-components
        └── di/
            └── <FeatureName>Module.kt       # Feature Koin module
```

- Project contains only one module `:app`.
- All features are generated inside `app/src/main/java/<basePackage>/feature/<featureName>/`.
- Code shared between features is generated inside `app/src/main/java/<basePackage>/core/`.

### 3.1 Generation order (STRICT)

This is the only place where the file generation order is defined. Workflows reference this
section instead of repeating it.

1. `core/ui/UiText.kt` (if missing) and `core/di/DispatcherModule.kt` (only if the feature has blocking or CPU-bound work).
2. `core/database/`: `entity/`, `dao/`, `converter/`, `migration/`, paging source.
3. `feature/<featureName>/domain/`: `error/`, `model/`, `repository/`, `usecase/`.
4. `feature/<featureName>/data/`: `dto/`, `mapper/`, `datasource/` (DataSource interfaces, implementations and the Retrofit API), `repository/`.
5. `feature/<featureName>/presentation/`: `mvi/`, `model/` (if the ViewModel pre-formats values), `mapper/`, `viewmodel/`, `ui/`.
6. `feature/<featureName>/di/<FeatureName>Module.kt`.
7. `res/values/strings.xml` and `res/values-ru/strings.xml`.
8. Register the module in `App.kt`.
9. Tests and `androidTest`.
10. Navigation config and destination (if needed).

The shape of every directory is defined in Section 3 above. The repository contract from
Section 2.4 determines which DataSources, UseCases and methods are generated.

===============================================================================

## 4. RULES OF LAYER DEPENDENCIES (CRITICAL)

### No horizontal dependencies between layers

```
❌ feature/auth → feature/profile
❌ core/ → feature/
✅ feature/auth → core/
✅ feature/profile → core/
```

- Shared data between features is only available through `core/`.
- `core/` never depends on `feature/`.

### No horizontal dependencies in the infrastructure

```
❌ AuthRepository → ProfileRepository
❌ AuthLocalDataSource → UserLocalDataSource
✅ AuthRepository → AuthLocalDataSource + AuthRemoteDataSource
```

- UseCase may use another UseCase — the only allowed exception.

### Rules inside feature

```
❌ domain/ → data/
❌ domain/ → presentation/
✅ presentation/ → domain/  # UI knows its own domain
✅ data/ → domain/          # Data implements domain contracts
```

- Domain is the innermost layer only.

===============================================================================

## 5. RULES OF ERRORS (STRICT)

### 5.1 Custom sealed class of errors for each feature

File: `domain/error/<FeatureName>Error.kt`

```kotlin
sealed class AuthError : Exception() {
    data object InvalidCredentials : AuthError()
    data object AccountBlocked : AuthError()
    data class NetworkError(val throwable: Throwable) : AuthError()
    data class UnknownError(val throwable: Throwable) : AuthError()
}
```

`AuthError` extends `Exception` only because `Result.failure()` requires a `Throwable`. Errors are
values: never throw `AuthError`, never catch it.

### 5.2 UseCase maps exceptions to domain errors

```kotlin
class LoginUseCase(private val authRepository: AuthRepository) {
    suspend operator fun invoke(params: LoginParams): Result<AuthToken> = try {
        Result.success(authRepository.login(params.email, params.password))
    } catch (e: CancellationException) {
        throw e
    } catch (e: UnauthorizedException) {
        Result.failure(AuthError.InvalidCredentials)
    } catch (e: NetworkException) {
        Result.failure(AuthError.NetworkError(e))
    } catch (e: Exception) {
        Result.failure(AuthError.UnknownError(e))
    }
}
```

### 5.3 ViewModel maps typed errors to `UiText`

ViewModel never builds user-facing strings itself. Mapping lives in `presentation/mapper/`:

```kotlin
result.onFailure { error ->
    _state.update { it.copy(error = error.toUiText()) }
}
```

```kotlin
// presentation/mapper/AuthUiMapper.kt
fun AuthError.toUiText(): UiText = when (this) {
    AuthError.InvalidCredentials -> UiText.Resource(R.string.error_invalid_credentials)
    AuthError.AccountBlocked -> UiText.Resource(R.string.error_account_blocked)
    AuthError.NetworkError -> UiText.Resource(R.string.error_network)
    AuthError.UnknownError -> UiText.Resource(R.string.error_unknown)
}
```

### 5.4 Error handling contract (STRICT)

- One-shot operations return `Result<T>`. Streams return `Flow<Result<T>>`.
- `Result<Flow<T>>` is PROHIBITED: a `try/catch` around `invoke()` cannot catch errors that happen during collection, so `Result.success` would lie.
- Errors inside a Flow are mapped with the `catch` operator:

```kotlin
operator fun invoke(): Flow<Result<List<Record>>> =
    repository.observeRecords()
        .map<List<Record>, Result<List<Record>>> { Result.success(it) }
        .catch { error ->
            if (error is CancellationException) throw error
            emit(Result.failure(error.toHistoryError()))
        }
```

- PROHIBITED: `Result.getOrThrow()`, `throw` outside DataSources and Repositories, `runCatching { }` around suspend calls (it swallows `CancellationException`).
- `CancellationException` is always rethrown before mapping any other error.
- `Result.exceptionOrNull()` is used only for assertions in tests; production code uses `onSuccess`/`onFailure`.
- Domain errors never reach the UI as exceptions: they are mapped to `UiText` (see 5.3).

===============================================================================

## 6. UseCase RULES (STRICT)

```kotlin
class LoginUseCase(private val authRepository: AuthRepository) {
    suspend operator fun invoke(params: LoginParams): Result<AuthToken> = try {
        Result.success(authRepository.login(params.email, params.password))
    } catch (e: CancellationException) {
        throw e
    } catch (e: ClientRequestException) {
        if (e.response.status == HttpStatusCode.Unauthorized)
            Result.failure(AuthError.InvalidCredentials)
        else
            Result.failure(AuthError.NetworkError(e))
    } catch (e: Exception) {
        Result.failure(AuthError.UnknownError(e))
    }
}
```

**Rules**:
- One public method: `suspend operator fun invoke()`.
- One-shot operation returns `Result<T>`; a stream returns `Flow<Result<T>>`. `Result<Flow<T>>` is prohibited.
- The `try/catch` covers only the suspend call. Errors emitted by a Flow are mapped with `.catch { }`.
- `CancellationException` is rethrown before any other `catch`.
- Maps network/DB exceptions to `<FeatureName>Error`; never rethrows raw exceptions.
- No `runCatching` around suspend calls.
- No `!!` in production code; use nullable-safe calls. For OkHttp media types use `"application/json".toMediaType()`.
- Dispatchers are injected, never referenced as `Dispatchers.*` (see `rules-presentation.md` 1.3). Only blocking or CPU-bound work needs a dispatcher; Room/Retrofit `suspend` calls are already main-safe.

### 6.1 Never do this

| ❌ Wrong | ✅ Correct |
|---|---|
| `Result<Flow<T>>` | `Flow<Result<T>>` |
| `result.getOrThrow()` in production | `result.onSuccess` / `result.onFailure` |
| `runCatching { suspendCall() }` | explicit `try/catch` with `CancellationException` rethrow |
| `repository.refresh(): Result<Unit>` | `suspend fun refresh()` — the UseCase maps errors |
| `class AuthRepository(...)` with body in `domain/` | `interface AuthRepository` + `AuthRepositoryImpl` in `data/` |
| `Dispatchers.IO` inside a UseCase | injected dispatcher qualifier, or no dispatcher for Room/Retrofit |
| `SupervisorJob()` or a custom scope in a ViewModel | `viewModelScope` only |
| `collectAsState()` in a Screen | `collectAsStateWithLifecycle()` |
| `MutableList` in `UiState` | `ImmutableList` / `persistentListOf()` |
| User-visible string in a View or ViewModel | `stringResource` / `UiText.Resource` |
| `@AutoMigration` or `fallbackToDestructiveMigration()` | manual `Migration(from, to)` + migration test |
| `SELECT *` for a complex query | explicit columns and a projection |
| `!!` in production code | nullable-safe calls; for OkHttp use `"application/json".toMediaType()` |
| `refresh()` without a RemoteDataSource | contract from Section 2.4 |

===============================================================================

## 7. FILES RULES (HARD)

- Each class in a separate file
- Enum, Sealed, UiState, UiEvent, UiEffect — each in a separate file
- No nested classes (except sealed subclasses in a sealed file)
- The file cannot be more than 1000 lines (red zone)
- Preferably less than 600 lines (yellow zone)

===============================================================================

## 8. NAMING CONVENTIONS

| Artifact         | Pattern                           | Example                      |
|------------------|-----------------------------------|------------------------------|
| UseCase          | `<Action>UseCase.kt`              | `LoginUseCase.kt`            |
| Repository       | `<FeatureName>Repository.kt`      | `AuthRepository.kt`          |
| Repository impl  | `<FeatureName>RepositoryImpl.kt`  | `AuthRepositoryImpl.kt`      |
| LocalDataSource  | `<FeatureName>LocalDataSource.kt` | `AuthLocalDataSource.kt`     |
| RemoteDataSource | `<FeatureName>RemoteDataSource.kt`| `AuthRemoteDataSource.kt`    |
| DTO              | `<Model>Dto.kt`                   | `RecordDto.kt`               |
| Mapper           | `<FeatureName>Mapper.kt`          | `AuthMapper.kt`              |
| Error            | `<FeatureName>Error.kt`           | `AuthError.kt`               |
| ViewModel        | `<FeatureName>ViewModel.kt`       | `AuthViewModel.kt`           |
| UiState          | `<FeatureName>UiState.kt`         | `AuthUiState.kt`             |
| UiEvent          | `<FeatureName>UiEvent.kt`         | `AuthUiEvent.kt`             |
| UiEffect         | `<FeatureName>UiEffect.kt`        | `AuthUiEffect.kt`            |
| Ui model         | `<Model>Ui.kt` (in `presentation/model/`) | `HistoryRecordUi.kt` |
| UiMapper         | `<FeatureName>UiMapper.kt`        | `AuthUiMapper.kt`            |
| UiText           | `UiText.kt` (in `core/ui/`)       | `UiText.kt`                  |
| Dispatcher module| `DispatcherModule.kt` (in `core/di/`) | `DispatcherModule.kt`    |
| Paging source    | `<Model>PagingSource.kt` (in `core/database/dao/`) | `RecordPagingSource.kt` |
| Room migration   | `Migration<V1>To<V2>.kt`          | `Migration2To3.kt`           |
| DI module val    | `<featureName>Module`             | `val authModule = module {}` |
| DI file          | `<FeatureName>Module.kt`          | `AuthModule.kt`              |
| Room entity      | `<Model>Entity`                   | `RecordEntity`               |
| Package          | lowercase                         | `feature.auth.domain`        |

===============================================================================

## 9. DI RULES

### 9.1 One DI-file for one feature

```
feature/auth/di/AuthModule.kt
```

### 9.2 DI-module example

```kotlin
val authModule = module {
    single { AuthRemoteDataSource(get(), get()) }
    single { AuthLocalDataSource(get()) }
    single<AuthRepository> { AuthRepositoryImpl(get(), get()) }
    factory { LoginUseCase(get()) }
    viewModel { AuthViewModel(get()) }
}
```

### 9.3 App.kt with Koin-modules

```kotlin
class App : Application() {
    override fun onCreate() {
        super.onCreate()
        startKoin {
            androidContext(this@App)
            modules(
                // core-modules
                dispatcherModule,
                databaseModule,
                networkModule,
                preferencesModule,
                // feature-modules
                authModule,
                profileModule
            )
        }
    }
}
```

### 9.4 Koin DSL rules

- `single { }` - one instance for the app (repositories, DAOs, Retrofit services) — singletone
- `viewModel { }` - scoped to a ViewModel lifecycle (from `org.koin.androidx.viewmodel.dsl.viewModel`)
- `viewModelOf(::FeatureViewModel)` is an allowed alternative to `viewModel { FeatureViewModel(get()) }` (import `org.koin.core.module.dsl.viewModelOf`)
- `get()` resolves dependencies by type inside a definition

### 9.5 Dispatcher qualifiers

```kotlin
// core/di/DispatcherModule.kt
import org.koin.core.qualifier.named

val dispatcherModule = module {
    single(named("ioDispatcher")) { Dispatchers.IO }
    single(named("defaultDispatcher")) { Dispatchers.Default }
}

// feature/auth/di/AuthModule.kt (inside module { })
factory { ImportCsvUseCase(get(), get(named("ioDispatcher"))) }
```

- Dispatchers are injected by qualifier, never referenced as `Dispatchers.*` in ViewModel, UseCase or Repository.
- Use a dispatcher only for blocking or CPU-bound work; Room/Retrofit `suspend` calls do not need one.
- Register `dispatcherModule` in `App.kt` next to the other core modules.

===============================================================================
