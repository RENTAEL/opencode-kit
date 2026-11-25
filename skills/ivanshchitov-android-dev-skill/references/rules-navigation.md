# Rules — navigation

This is one part of the rule set. Section numbers are local to this file; cross-file
references name the file. The file map is in
`../SKILL.md`. Read `rules-core.md` first, then the file for the layer you generate.

===============================================================================

## 1. NAVIGATION RULES (STRICT)

### 1.1 Type-Safe Navigation Config

```kotlin
// navigation/NavigationConfig.kt
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

### 1.2 AppNavGraph rules

```kotlin
// navigation/AppNavGraph.kt
@Composable
fun AppNavGraph(modifier: Modifier = Modifier) {
    val navController = rememberNavController()

    NavHost(
        navController = navController,
        startDestination = NavigationConfig.Home, // Strict type reference
        modifier = modifier,
    ) {
        composable<NavigationConfig.Home> {
            HomeScreen(
                onProfileClick = { id ->
                    navController.navigate(NavigationConfig.Profile(id))
                },
                onSettingsClick = {
                    navController.navigate(NavigationConfig.Settings)
                },
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

- `AppNavGraph.kt` — separate file inside `navigation/`.
- `AppNavGraph` owns the `NavHostController`: it creates it with `rememberNavController()` and never accepts it as a parameter.

### 1.3 AppNavGraph inside MainActivity

```kotlin
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            AppTheme {
                AppNavGraph(modifier = Modifier.fillMaxSize())
            }
        }
    }
}
```

- `MainActivity` does not create or pass a `NavController`; the graph is the single entry point.

===============================================================================
