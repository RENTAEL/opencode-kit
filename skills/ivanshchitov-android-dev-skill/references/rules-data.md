# Rules — data layer

This is one part of the rule set. Section numbers are local to this file; cross-file
references name the file. The file map is in
`../SKILL.md`. Read `rules-core.md` first, then the file for the layer you generate.

===============================================================================

## 1. DTO AND MAPPING

### 1.1 DTO is only in data/dto

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

### 1.2 Mapper is inside data/mapper/

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

### 1.3 Who does mapping

- RemoteDataSource receives DTO from Retrofit and returns DTO
- `<FeatureName>RepositoryImpl` calls the mapper and returns the domain model
- LocalDataSource receives the Room entity and returns the entity
- `<FeatureName>RepositoryImpl` maps Room entity to domain model

```kotlin
// Correct flow:
// Retrofit → DTO → (mapper in RepositoryImpl) → Domain model → UseCase → ViewModel

// domain/repository/AuthRepository.kt — contract only, no data/ imports
interface AuthRepository {
    suspend fun login(email: String, password: String): AuthToken
}

// data/repository/AuthRepositoryImpl.kt — mapping lives here
class AuthRepositoryImpl(
    private val remoteDataSource: AuthRemoteDataSource,
    private val localDataSource: AuthLocalDataSource
) : AuthRepository {
    override suspend fun login(email: String, password: String): AuthToken {
        val dto = remoteDataSource.login(LoginRequestDto(email, password))
        val token = dto.toDomain()
        localDataSource.saveToken(token)
        return token
    }
}
```

### 1.4 Rules of DTO

- `@Serializable` for all DTO
- `@SerialName("snake_case")` if the API uses snake_case
- DTO is data class, only `val` fields
- DTOs do NOT contain business logic
- Nullable DTO field: If the field may not be present in the JSON, `val field: String? = null`

===============================================================================

## 2. Room RULES

### 2.1 Database and locations

- One `AppDatabase` for the whole project — via DI (singleton).
- `AppDatabase` → `core/database/`.
- Entities → `core/database/entity/`.
- DAOs → `core/database/dao/`.
- Converters → `core/database/converter/`.
- Migrations → `core/database/migration/`, one file per migration.
- `@Database(..., exportSchema = true)`; set `room.schemaLocation` in KSP and commit the JSON schemas.

### 2.2 Entities, indices, relations

- Table name: `snake_case`, plural (`users`, `history_records`). Entity: `PascalCase` + `Entity`.
- Columns: `snake_case` via `@ColumnInfo`.
- `@Index` is REQUIRED on every `@ForeignKey` child column and on columns used in real filters or sorting.
- Uniqueness is enforced by `@Index(unique = true)`, not by a check in code.
- `onDelete` is chosen deliberately: `CASCADE` for dependent data, `RESTRICT`/`NO_ACTION` for reference data.
- Many-to-many goes through a junction entity.
- `@Relation` only for small result sets; large sets use a JOIN with a projection to avoid N+1.

```kotlin
@Entity(
    tableName = "records",
    indices = [Index("user_id"), Index(value = ["external_id"], unique = true)],
    foreignKeys = [
        ForeignKey(
            entity = UserEntity::class,
            parentColumns = ["id"],
            childColumns = ["user_id"],
            onDelete = ForeignKey.CASCADE,
        ),
    ],
)
data class RecordEntity(
    @PrimaryKey val id: String,
    @ColumnInfo(name = "user_id") val userId: String,
    @ColumnInfo(name = "external_id") val externalId: String,
    @ColumnInfo(name = "created_at") val createdAt: Long,
)
```

### 2.3 DAO and transactions

- Read methods return `Flow<T>`/`Flow<List<T>>`; one-shot reads are `suspend`.
- Insert/update/delete return `Unit`, `Long` or a row count — never a Flow.
- `@Transaction` is required for read-modify-write and for any operation that changes several tables consistently.
- Multi-DAO consistency uses `db.withTransaction { }` in the repository.
- No network calls inside a transaction.
- DAOs contain no business logic and no mapping.

```kotlin
@Dao
interface RecordDao {
    @Query("SELECT id, user_id, external_id, created_at FROM records WHERE user_id = :userId ORDER BY created_at DESC")
    fun observeByUser(userId: String): Flow<List<RecordEntity>>

    @Upsert
    suspend fun upsert(records: List<RecordEntity>)

    @Query("DELETE FROM records WHERE user_id = :userId")
    suspend fun deleteByUser(userId: String)

    @Transaction
    suspend fun replaceForUser(userId: String, records: List<RecordEntity>) {
        deleteByUser(userId)
        upsert(records)
    }
}
```

### 2.4 Conflict strategy

- `onConflict` is specified explicitly on every `@Insert`.
- `OnConflictStrategy.REPLACE` is allowed only for a full row overwrite: it deletes and reinserts, which breaks foreign keys and confuses observers.
- Prefer `@Upsert`; for "insert if absent" use `@Insert(onConflict = OnConflictStrategy.ABORT)`.

### 2.5 Queries and converters

- `SELECT *` only for simple entities; otherwise list the columns.
- Projections are separate data classes, never entities.
- TypeConverters are explicit and registered via `@TypeConverters`.
- Enums are stored as `String` through a converter, never as `ordinal`.
- Dates are epoch millis (`Long`); `BigDecimal` is stored as `String`.

### 2.6 Paging (MUST for paginated lists)

- Paginated lists use Paging 3: `PagingSource` for a local source, `RemoteMediator` for offline-first (network → Room → `PagingSource`).
- `PagingData` is cached in the ViewModel with `cachedIn(viewModelScope)`.
- UI consumes it with `collectAsLazyPagingItems()`.
- `Flow<List<T>>` is allowed only for short, non-paginated lists.

```kotlin
@Dao
interface RecordDao {
    @Query("SELECT * FROM records ORDER BY created_at DESC")
    fun pagingSource(): PagingSource<Int, RecordEntity>
}
```

### 2.7 Schema and migrations

- `exportSchema = true` on `@Database`; schemas are committed to the repository.
- Every migration is a manual `Migration(from, to)` in its own file and is added to `addMigrations(...)`.
- `@AutoMigration` is PROHIBITED: every schema change must be explicit.
- `fallbackToDestructiveMigration()` is PROHIBITED in release.
- Every migration is covered by a `MigrationTestHelper` test against the previous schema.
- `Entity → Domain` mapping happens in the Repository via a mapper, never in the LocalDataSource.

```kotlin
@Database(
    entities = [UserEntity::class, RecordEntity::class],
    version = 3,
    exportSchema = true,
)
abstract class AppDatabase : RoomDatabase() {
    abstract fun recordDao(): RecordDao
}

class Migration2To3 : Migration(2, 3) {
    override fun migrate(db: SupportSQLiteDatabase) {
        db.execSQL("ALTER TABLE records ADD COLUMN note TEXT")
    }
}

val database = Room.databaseBuilder(context, AppDatabase::class.java, "app.db")
    .addMigrations(Migration2To3())
    .build()
```

===============================================================================
