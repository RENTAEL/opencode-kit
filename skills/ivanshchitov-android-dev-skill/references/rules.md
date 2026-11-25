# Skill rules

You are an agent creating a complete Android app feature slice.

You create all feature layers:
- `domain/` — models, DTOs, UseCase, Repository, custom errors
- `data/` — LocalDataSource, RemoteDataSource, DTO → Domain mapping
- `presentation/` — Screens, Views, ViewModel, ViewState, Events, side-effect channel
- `di/` — feature DI module
- `ui/` — Android platform UI (Compose)

You work strictly according to the rules below. Violating any invariant is an error.

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
- `domain/repository/` depends only on: `data/datasource/`, `domain/model/`.

PROHIBITED: domain → presentation, domain → data directly (UseCase doesn't know about DataSource), domain → other feature/.

### 2.2 Data layer

- `data/dto/` depends only on: Kotlinx Serialization annotations.
- `data/mapper/` depends only on: data/dto/, domain/model/.
- `data/datasource/` depends only on: `core/network/` (Remote), `core/database/` (Local), `data/dto/`.

**Principles**:
- **Offline-first**: Local database is the source of truth
- **Repository pattern**: Single public API for data access
- **Reactive streams**: All data exposed as `Flow<T>`

PROHIBITED: DataSource → UseCase, DataSource → ViewModel, DataSource → other feature/, DataSource → other DataSource.

### 2.3 Presentation layer

- `presentation/viewmodel/` depends only on: `domain/usecase/`, `domain/error/`, `presentation/mvi/`, `navigation/`

PROHIBITED: ViewModel → Repository, ViewModel → DataSource, ViewModel → other feature/ (navigation is only possible via sealed Config in `navigation/`).

===============================================================================

## 3. MODULE STRUCTURE (STRICT)

```
app/src/main/java/<basePackage>/
├── App.kt                       # DI setup (Koin startup or @HiltAndroidApp)
├── MainActivity.kt              # Entry point
├── navigation/                  # COMMON NAVIGATION
│   │   ├── NavigationConfig.kt  # Type-Safe Navigation config
│   │   └── AppNavHost.kt        # The central NavHost graph definition
├── core/                        # SHARED CODE
│   ├── di/                      # core DI modules (Koin or Hilt; e.g. Database, Network, Preferences)
│   ├── network/                 # Retrofit setup + ApiConfig
│   ├── database/                # Room AppDatabase, DAOs, entities
│   ├── preferences/             # DataStore Preferences
│   └── ui/                      # Material 3 theme, shared composable
└── feature/                     # BUSINESS FEATURES
    └── <featureName>/           # e.g. feature 'history'
        ├── data/
        │   ├── dto/             # DTO-classes (@Serializable)
        │   ├── datasource/      # LocalDataSource, RemoteDataSource
        │   ├── mapper/          # Entity/DTO <-> Domain mapping
        │   └── repository/      # <FeatureName>RepositoryImpl.kt — domain repository implementation
        ├── domain/
        │   ├── model/           # Data classes, value objects
        │   ├── error/           # <Feature>Error.kt (sealed class)
        │   ├── repository/      # <FeatureName>Repository.kt (interface)
        │   └── usecase/         # UseCase-classes
        ├── presentation/
        │   ├── mvi/             # <FeatureName>State.kt, <FeatureName>Intent.kt, <FeatureName>SideEffect.kt
        │   ├── viewmodel/       # <FeatureName>ViewModel.kt
        │   └── ui/              # <FeatureName>Screen.kt, <FeatureName>View.kt, Composable-components
        └── di/
            └── <FeatureName>Module.kt       # Feature DI module (Koin or Hilt)
```

- Project contains only one module `:app`.
- All features are generated inside `app/src/main/java/<basePackage>/feature/<featureName>/`.
- Code that shared between features is genarated inside `app/src/main/java/<basePackage>/core/`.

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
- `core/` never depend on `features.

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

File: `domain/error/<Feature>Error.kt`

```kotlin
sealed class AuthError : Exception() {
    data object InvalidCredentials : AuthError()
    data object AccountBlocked : AuthError()
    data class NetworkError(val cause: Throwable) : AuthError()
    data class UnknownError(val cause: Throwable) : AuthError()
}
```

### 5.2 UseCase maps exceptions to domain errors

```kotlin
class LoginUseCase(private val authRepository: AuthRepository) {
    suspend fun execute(params: LoginParams): Result<AuthToken> = try {
        Result.success(authRepository.login(params.email, params.password))
    } catch (e: UnauthorizedException) {
        Result.failure(AuthError.InvalidCredentials)
    } catch (e: NetworkException) {
        Result.failure(AuthError.NetworkError(e))
    } catch (e: Exception) {
        Result.failure(AuthError.UnknownError(e))
    }
}
```

### 5.3 ViewModel handles the typed errors

```kotlin
result.onFailure { error ->
    val message = when (error) {
        is AuthError.InvalidCredentials -> "Неверный логин или пароль"
        is AuthError.AccountBlocked -> "Аккаунт заблокирован"
        is AuthError.NetworkError -> "Проверьте интернет-соединение"
        else -> "Неизвестная ошибка"
    }
    _viewState.update { it.copy(error = message) }
}
```

===============================================================================

### 6. UseCase RULES (STRICT)

```kotlin
class LoginUseCase(private val authRepository: AuthRepository) {
    suspend fun execute(params: LoginParams): Result<AuthToken> = try {
        Result.success(authRepository.login(params.email, params.password))
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
- Returns `Result<T>` or `Result<Flow<T>>`.
- Whole `try/catch` is inside `invoke()` — exceptions don't fly out.
- Maps network/DB exceptions to `<Feature>Error`.

===============================================================================

## 7. DTO AND MAPPING

### 7.1 DTO is only in data/dto

DTOs are network/database models. They don't extend beyond `data/`.

```kotlin
// data/dto/AuthResponseDto.kt
@Serializable
data class AuthResponseDto(
    @SerialName("access_token") val accessToken: String,
    @SerialName("refresh_token") val refreshToken: String,
    @SerialName("expires_in") val expiresIn: Long
)

@Serializable
data class LoginRequestDto(
    @SerialName("email") val email: String,
    @SerialName("password") val password: String
)
```

### 7.2 Mapper is inside data/mapper/

Mapping DTO → Domain and Domain → DTO — only in `data/mapper/`:

```kotlin
// data/mapper/AuthMapper.kt
fun AuthResponseDto.toDomain(): AuthToken = AuthToken(
    accessToken = accessToken,
    refreshToken = refreshToken,
    expiresAt = Clock.System.now().plus(expiresIn, DateTimeUnit.SECOND, TimeZone.UTC)
)

fun LoginParams.toDto(): LoginRequestDto = LoginRequestDto(
    email = email,
    password = password
)
```

### 7.3 Who does mapping

- RemoteDataSource receives DTO from Retrofit and returns DTO
- Repository calls the mapper and returns the domain model
- LocalDataSource receives the Room entity and returns the entity
- Repository maps Room entity to domain model

```kotlin
// Correct flow:
// Retrofit → DTO → (mapper in Repository) → Domain model → UseCase → ViewModel
class AuthRepository(
    private val remoteDataSource: AuthRemoteDataSource,
    private val localDataSource: AuthLocalDataSource
) {
    suspend fun login(email: String, password: String): AuthToken {
        val dto = remoteDataSource.login(LoginRequestDto(email, password))
        val token = dto.toDomain()
        localDataSource.saveToken(token)
        return token
    }
}
```

### 7.4 Rules of DTO

- `@Serializable` for all DTO
- `@SerialName("snake_case")` if the API uses snake_case
- DTO is data class, only `val` fields
- DTOs do NOT contain business logic
- Nullable DTO field: If the field may not be present in the JSON, `val field: String? = null`

===============================================================================

### 8. Room RULES

- One `AppDatabase` for whole project — via DI (singletone)
- DAOs methods to receive something should return only `Flow<T>` or `Flow<List<T>>`
- Implement migrations with `Migration(from, to)` and `addMigrations` to builder
- Each Migration in separate file 
- `Entity → Domain` mapping — in Repository via mapper (not in LocalDataSource)
- DB table should be named as snake_case. Entity class should be named as PascalCase + Entity
- `AppDatabase` is inside `core/database/`.
- Enitites is inside `core/database/entity/`.
- Daos is inside `core/database/dao/`.

```kotlin
// core/database/entity/UserEntity.kt
@Entity(tableName = "user")
data class UserEntity(
    @PrimaryKey val id: String,
    @ColumnInfo(name = "first_name") val firstName: String,
    @ColumnInfo(name = "last_name") val lastName: String?,
    @ColumnInfo(name = "age") val age: Int = 0,
    @ColumnInfo(name = "height") val height: Double
)
```

```kotlin
// core/database/dao/UserDao.kt
@Dao
interface UserDao {
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertUser(user: UserEntity)

    @Query("SELECT * FROM users")
    fun observeUsers(): Flow<List<UserEntity>>
}
```

===============================================================================

## 9. ViewModel RULES

### 9.1 ViewModel structure

```kotlin
class HistoryViewModel(
    private val getHistoryRecordsUseCase: GetHistoryRecordsUseCase,
    private val onNavigateToEdit: (recordId: Int) -> Unit
) : ViewModel() {

    private val _state = MutableStateFlow(HistoryState())
    val state: StateFlow<HistoryState> = _state.asStateFlow()

    // Side Effects — via Channel (not StateFlow)
    private val _effects = Channel<HistorySideEffect>(Channel.BUFFERED)
    val effects: Flow<HistorySideEffect> = _effects.receiveAsFlow()

    fun onEvent(event: HistoryEvent) {
        when (event) {
            is HistoryEvent.Load -> load()
            is HistoryEvent.RecordClicked -> onNavigateToEdit(event.id)
        }
    }

    private fun load() {
        viewModelScope.launch {
            _state.update { it.copy(isLoading = true, errorMessage = null) }
            
            val result = getHistoryRecordsUseCase()
            result.onSuccess {
                _state.update { it.copy(isLoading = false, records = records) }
            }
            result.onFailure { error ->
                val message = when (error) {
                    is HistoryError.NetworkError -> "Check internet connection"
                    else -> "Unknown error"
                }
                _state.update { it.copy(isLoading = false, errorMessage = e.message) }
            }
        }
    }
}
```

### 9.2 ViewModel rules

- ViewModel should only have access to business logic through UseCases.
- PROHIBITED: Repositories, DataSources and DAO dependencies
- ViewModel is provided by DI per [Section 13](#13-di-rules): Koin `viewModel { }` + `koinViewModel()`, or Hilt `@HiltViewModel` + `@Inject constructor` + `hiltViewModel()`.

### 9.3 Coroutines rules

- `Dispatchers.IO` — DO NOT use directly in ViewModel (UseCase manages dispatchers automatically if needed)
- Coroutines Scope is cancelled automatically when ViewModel is destroyed.
- Use `SupervisorJob()` to not fall all corountines when one is failed.

### 9.4 Side-Effect rules

For events that cannot be repeated when `resubscribe` (navigation, toast, snackbar), use `Channel`, NOT `StateFlow`:

```kotlin
// mvi/AuthSideEffect.kt
sealed class AuthSideEffect {
    data object NavigateToMain : AuthSideEffect()
    data class ShowToast(val message: String) : AuthSideEffect()
}
```

```kotlin
// Inside ViewModel:
private val _effects = Channel<AuthSideEffect>(Channel.BUFFERED)
val effects: Flow<AuthSideEffect> = _effects.receiveAsFlow()
```

```kotlin
// Inside Screen (observe side effects):
LaunchedEffect(viewModel) {
    viewModel.effects.collect { effect ->
        when (effect) {
            is AuthSideEffect.NavigateToMain -> { /* навигация */ }
            is AuthSideEffect.ShowToast -> { /* показ тоста */ }
        }
    }
}
```

SideEffect is only created if there are truly one-time events. Don't create them just for the sake of it.

### 9.5 Strict rules

- ViewModel — the only source of state
- All public functions returns `Unit`
- All functions that return values ​​are private.
- View HAS NO `remember` for logic

===============================================================================

## 10. TESTING

### 10.1 UseCase testing

Tests for UseCase are the most important. Mock Repository:

```kotlin
// test/feature/auth/domain/usecase/LoginUseCaseTest.kt
class LoginUseCaseTest {
    private val authRepository = mockk<AuthRepository>()
    private val useCase = LoginUseCase(authRepository)

    @Test
    fun `execute returns success when login succeeds`() = runTest {
        // Given
        val token = AuthToken("access", "refresh", /* expiresAt */)
        coEvery { authRepository.login(any(), any()) } returns token

        // When
        val result = useCase.execute(LoginParams("user@test.com", "password"))

        // Then
        assertTrue(result.isSuccess)
        assertEquals(token, result.getOrNull())
    }

    @Test
    fun `execute returns InvalidCredentials on 401`() = runTest {
        // Given
        coEvery { authRepository.login(any(), any()) } throws
            ClientRequestException(mockk { every { status } returns HttpStatusCode.Unauthorized }, "")

        // When
        val result = useCase.execute(LoginParams("user@test.com", "wrong"))

        // Then
        assertTrue(result.isFailure)
        assertIs<AuthError.InvalidCredentials>(result.exceptionOrNull())
    }
}
```

### 10.2 ViewModel testing

```kotlin
// test/feature/auth/presentation/AuthViewModelTest.kt
class AuthViewModelTest {
    private val loginUseCase = mockk<LoginUseCase>()
    private val lifecycle = LifecycleRegistry()
    private val viewModel = AuthViewModel(
        loginUseCase = loginUseCase,
        onNavigateToMain = {}
    )

    @Test
    fun `obtainEvent EmailChanged updates viewState`() = runTest {
        viewModel.obtainEvent(AuthViewEvent.EmailChanged("test@test.com"))
        assertEquals("test@test.com", viewModel.viewState.value.email)
    }

    @Test
    fun `login success sends NavigateToMain effect`() = runTest {
        coEvery { loginUseCase.execute(any()) } returns Result.success(mockk())
        viewModel.obtainEvent(AuthViewEvent.EmailChanged("u@test.com"))
        viewModel.obtainEvent(AuthViewEvent.PasswordChanged("pass"))
        viewModel.obtainEvent(AuthViewEvent.Login)

        val effect = viewModel.effects.first()
        assertIs<AuthSideEffect.NavigateToMain>(effect)
    }
}
```

### 10.3 Testing rules

- UseCase tests are required
- ViewModel tests are required for complex logic
- Repository tests are optional (if there is non-trivial mapping logic)
- DataSource tests are not required (tested via Repository)
- Use `kotlinx-coroutines-test` (`runTest`, `TestScope`)
- Use `mockk` for mocking
- Test file: `test/feature/<featureName>/.../<Class>Test.kt`
- Test name: backtick string describing the scenario

===============================================================================

## 11. FILES RULES (HARD)

- Each class in a separate file
- Enum, Sealed, ViewState, Events, SideEffect — each in a separate file
- No nested classes (except sealed subclasses in a sealed file)
- The file cannot be more than 1000 lines (red zone)
- Preferably less than 600 lines (yellow zone)

===============================================================================

## 12. NAMING CONVENTIONS

| Artifact         | Pattern                           | Example                      |
|------------------|-----------------------------------|------------------------------|
| UseCase          | `<Action>UseCase.kt`              | `LoginUseCase.kt`            |
| Repository       | `<Feature>Repository.kt`          | `AuthRepository.kt`          |
| LocalDataSource  | `<Feature>LocalDataSource.kt`     | `AuthLocalDataSource.kt`     |
| RemoteDataSource | `<Feature>RemoteDataSource.kt`    | `AuthRemoteDataSource.kt`    |
| DTO              | `<Model>Dto.kt`                   | `RecordDto.kt`               |
| Mapper           | `<Feature>Mapper.kt`              | `AuthMapper.kt`              |
| Error            | `<Feature>Error.kt`               | `AuthError.kt`               |
| ViewModel        | `<Feature>ViewModel.kt`           | `AuthComponent.kt`           |
| ViewState        | `<Feature>ViewState.kt`           | `AuthViewState.kt`           |
| Events           | `<Feature>ViewEvent.kt`           | `AuthViewEvent.kt`           |
| SideEffect       | `<Feature>SideEffect.kt`          | `AuthSideEffect.kt`          |
| DI module (Koin) | `<featureName>Module`             | `val authModule = module {}` |
| DI module (Hilt) | `<Feature>Module`                 | `@Module @InstallIn(SingletonComponent::class) object AuthModule` |
| DI file          | `<FeatureName>Module.kt`          | `AuthModule.kt`              |
| Room entity      | `<Model>Entity`                   | `RecordEntity`               |
| Package          | lowercase                         | `feature.auth.domain`        |

===============================================================================

## 13. DI RULES

### 13.1 Framework selection (MANDATORY)

The project uses exactly one DI framework — **Koin** or **Hilt**. Before generating any DI code:

1. **Detect** the framework already used by the project (see [di-framework-selection.md](di-framework-selection.md)).
2. **If the project has NO DI** → **ask the user** which framework to use: **Koin** or **Hilt**. Never guess.
3. Follow the chosen framework consistently in every layer and every feature. Never mix frameworks.

### 13.2 One DI-file for one feature

```
feature/auth/di/AuthModule.kt
```

### 13.3 Module examples

#### 13.3.1 Koin module example

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

#### 13.3.2 Hilt module example

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

### 13.4 Application entry

#### 13.4.1 Koin application entry

**Koin** — register every feature module manually in `App.kt`:

```kotlin
class App : Application() {
    override fun onCreate() {
        super.onCreate()
        startKoin {
            androidContext(this@App)
            modules(
                // core-modules
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

#### 13.4.2 Hilt application entry

**Hilt** — no manual registration: `@HiltAndroidApp` on `Application`, `@AndroidEntryPoint` on `Activity`; `@InstallIn(...)` modules are discovered automatically by the root component.

### 13.5 ViewModel wiring

- **Koin**: `viewModel { }` in the module; the Screen retrieves it via `koinViewModel()`.
- **Hilt**: `@HiltViewModel` + `@Inject constructor` on the class; the Screen retrieves it via `hiltViewModel()`. Navigation callbacks cannot be constructor parameters with `@Inject` — use the SideEffect pattern ([Section 9.4](#94-side-effect-rules)) or `@AssistedInject` + `SavedStateHandle`.

### 13.6 DI DSL rules

#### 13.6.1 Koin DSL rules

- `single { }` - one instance for the app (repositories, DAOs, Retrofit services) — singletone
- `viewModel { }` - scoped to a ViewModel lifecycle (from `org.koin.androidx.viewmodel.dsl.viewModel`)
- `get()` resolves dependencies by type inside a definition

#### 13.6.2 Hilt DSL rules

- `@Singleton` — one instance per app (repositories, DAOs, Retrofit services)
- `@Provides` — factory method for third-party types (Room database, Retrofit, DataStore); parameters are resolved from the graph
- `@Binds` — binds an interface to its implementation (abstract function, no body)
- `@InstallIn(SingletonComponent::class)` — component scope for app-wide definitions
- Requires the KSP plugin (`com.google.devtools.ksp`) and `ksp(hilt-android-compiler)`

===============================================================================

## 14. UI RULES (COMPOSE)

Screen is a thin adapter:

```kotlin
@Composable
fun AuthScreen(viewModel: AuthViewModel = koinViewModel(),) { // Koin; for Hilt — hiltViewModel()
    val viewState by viewModel.viewState.collectAsState()

    // subscription for side effects
    LaunchedEffect(viewModel) {
        viewModel.effects.collect { effect ->
            when (effect) {
                is AuthSideEffect.ShowToast -> { /* показ тоста */ }
                AuthSideEffect.NavigateToMain -> { /* навигация */ }
            }
        }
    }

    AuthView(viewState, viewModel::obtainEvent)
}
```

View is layout only:
- Should contain previews with `@Preview`
- Accepts `viewState` and `eventHandler`
- No logic, no `remember` state logic
- No DI framework access (no `koinViewModel()` / `hiltViewModel()` in View)
- No side effects (only in Screen via `LaunchedEffect`)
- Margins are multiples of 4/8/16/24

**STRICT:** The agent generates **full working UI code** for each selected platform. Business logic is contained solely in the ViewModel. The UI only displays state and dispatches events. No // TODOs, // ..., or stubs. Only working code for a specific feature. **Exception** — user requests a stub.

===============================================================================

## 15. Android — Jetpack Compose (always)

The agent generates `<Feature>Screen.kt` and `<Feature>View.kt`.

**Screen** is a thin adapter (see [Section 14](#14-ui-rules-compose)).

**View** is full UI with real elements according to the feature description:

```kotlin
@Composable
fun AuthView(
    viewState: AuthViewState,
    onEvent: (AuthViewEvent) -> Unit
) {
    Column(
        modifier = Modifier.fillMaxSize().padding(16.dp),
        verticalArrangement = Arrangement.Center
    ) {
        TextField(
            value = viewState.email,
            onValueChange = { onEvent(AuthViewEvent.EmailChanged(it)) },
            label = { Text("Email") },
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Email),
            modifier = Modifier.fillMaxWidth()
        )
        Spacer(Modifier.height(8.dp))
        TextField(
            value = viewState.password,
            onValueChange = { onEvent(AuthViewEvent.PasswordChanged(it)) },
            label = { Text("Пароль") },
            visualTransformation = PasswordVisualTransformation(),
            modifier = Modifier.fillMaxWidth()
        )
        Spacer(Modifier.height(16.dp))
        Button(
            onClick = { onEvent(AuthViewEvent.Login) },
            enabled = !viewState.isLoading,
            modifier = Modifier.fillMaxWidth()
        ) {
            if (viewState.isLoading) CircularProgressIndicator(Modifier.size(16.dp))
            else Text("Войти")
        }
        viewState.error?.let {
            Spacer(Modifier.height(8.dp))
            Text(it, color = MaterialTheme.colorScheme.error)
        }
    }
}
```

- If a Composable component is used in 2+ places in multiple features → it is moved to: `core/ui/common/<ComponentName>.kt`.
- If a Composable component is used in 2+ places inside the feature (not between them) → it is moved to: `feature/ui/component/<ComponentName>.kt`.

```kotlin
@Composable
fun RecordList(
    records: List<Record>,
    onRecordClick: (Long) -> Unit,
    modifier: Modifier = Modifier,
) {
    LazyColumn(
        modifier = modifier,
        contentPadding = PaddingValues(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp),
    ) {
        items(
            items = records,
            key = { it.id },
        ) { record ->
            RecordCard(
                record = record,
                onClick = { onRecordClick(record.id) },
            )
        }
    }
}
```

- LazyColumn items should set key as item id: `key = { it.id }`

===============================================================================

## 16. NAVIGATION RULES (STRICT)

### 16.1 Type-Safe Navigation Config

```kotlin
// core/navigation/NavigationConfig.kt
// Sealed interface acts as the entry point for compile-time safety
sealed interface NavigationConfig {
    
    // Static screens without arguments
    @Serializable
    object Home : NavigationConfig
    
    @Serializable
    object Settings : NavigationConfig
    
    // Screens that require specific arguments
    @Serializable
    data class Profile(val userId: String) : NavigationConfig
}
```

- `NavigationConfig.kt` — separate file inside `navigation/`

### 16.2 AppNagGraph rules

```kotlin
// navigation/AppNavGraph.kt
@Composable
fun AppNavGraph(navController: NavHostController) {
    NavHost(
        navController = navController,
        startDestination = NavigationConfig.Home // Strict type reference
    ) {
        composable<NavigationConfig.Home> {
            HomeScreen(
                onProfileClick = { id -> 
                    navController.navigate(NavigationConfig.Profile(id)) 
                },
                onSettingsClick = { 
                    navController.navigate(NavigationConfig.Settings) 
                }
            )
        }
        
        composable<NavigationConfig.Settings> {
            SettingsScreen()
        }
        
        composable<NavigationConfig.Profile> { backStackEntry ->
            // Extract type-safe arguments safely
            val profileArgs = backStackEntry.toRoute<NavigationConfig.Profile>()
            ProfileScreen(userId = profileArgs.userId)
        }
    }
}
```

- `AppNavGraph.kt` — separate file inside `navigation/`

### 16.3 AppNavGraph inside MainActivity

```kotlin
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            val navController = rememberNavController()
            // The entire app UI points directly to central navigation file
            AppNavGraph(navController = navController)
        }
    }
}
```

===============================================================================

## 17. DEPENDENCIES VERSIONS

Set up dependencies version ONLY via `gradle/libs.versions.toml`.

Template of `gradle/libs.versions.toml` — include only the DI group of the framework chosen per [di-framework-selection.md](di-framework-selection.md) (Koin or Hilt):

```toml
[versions]
kotlin = "2.2.0"
agp = "9.0.0"
room = "2.8.4"
coroutines = "1.11.0"

# --- Koin (if Koin is the project's DI) ---
koin = "4.2.2"

# --- Hilt (if Hilt is the project's DI) ---
hilt = "2.56.2"
androidx-hilt = "1.2.0"
ksp = "2.2.0-2.0.4"          # tied to the Kotlin version

[libraries]
# Koin
koin-android = { group = "io.insert-koin", name = "koin-android", version.ref = "koin" }
koin-androidx-compose = { group = "io.insert-koin", name = "koin-androidx-compose", version.ref = "koin" }

# Hilt
hilt-android = { group = "com.google.dagger", name = "hilt-android", version.ref = "hilt" }
hilt-android-compiler = { group = "com.google.dagger", name = "hilt-android-compiler", version.ref = "hilt" }
hilt-navigation-compose = { group = "androidx.hilt", name = "hilt-navigation-compose", version.ref = "androidx-hilt" }

# Shared
room-runtime = { group = "androidx.room", name = "room-runtime", version.ref = "room" }

[plugins]
hilt = { id = "com.google.dagger.hilt.android", version.ref = "hilt" }
ksp = { id = "com.google.devtools.ksp", version.ref = "ksp" }
```

There are only aliases inside `build.gradle.kts`.

```kotlin
// ✅ Correct
implementation(libs.koin.android)
// ❌ Incorrect
implementation("io.insert-koin:koin-android:4.2.0")
```

===============================================================================

Follow these rules at all times. You're building a production-ready Android feature slice.
