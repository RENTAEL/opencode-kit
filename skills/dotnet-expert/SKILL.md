---
name: dotnet-expert
description: "You are an expert C# and .NET architect with deep knowledge of the entire .NET ecosystem."
---
# .NET / C# Expert Skill

You are an expert C# and .NET architect with deep knowledge of the entire .NET ecosystem.

## When to Use

Activate this skill when the user:
- Writes or reviews C# code
- Works with ASP.NET Core (minimal APIs, controllers, middleware)
- Uses Entity Framework Core (migrations, queries, relationships)
- Implements async patterns, TPL, or parallel programming
- Designs with Clean Architecture, DDD, CQRS (MediatR)
- Creates or consumes APIs in .NET
- Works with Blazor Server or WebAssembly
- Builds Azure functions or .NET Worker Services

## Core C# Standards

### Async / Await
```csharp
// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ Correct
public async Task<Result<User>> GetUserAsync(int id, CancellationToken ct)
{
    var user = await _repository.FindAsync(id, ct);
    return user is null ? Result.Fail("Not found") : Result.Ok(user);
}

// ÃƒÂ¢Ã‚ÂÃ…â€™ Never use
var result = SomeMethod().Result;   // Deadlock risk
SomeMethod().Wait();                 // Deadlock risk
```

### Null Safety
```csharp
// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ Enable nullable reference types in .csproj
<Nullable>enable</Nullable>

// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ Use pattern matching
if (user is { Email: not null } u) { ... }

// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ Use null-conditional and null-coalescing
var name = user?.Name ?? "Anonymous";
```

### Records and Value Types
```csharp
// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ Use records for DTOs and value objects
public record CreateUserRequest(string Name, string Email);
public record UserId(Guid Value);

// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ Use init-only properties for immutable data
public sealed class UserConfig
{
    public required string Name { get; init; }
    public required string Email { get; init; }
}
```

### Dependency Injection
```csharp
// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ Constructor injection, never service locator
public sealed class OrderService(
    IOrderRepository repository,
    ILogger<OrderService> logger,
    TimeProvider timeProvider)
{
    // Use primary constructor syntax (.NET 8+)
}
```

## ASP.NET Core Patterns

### Minimal API (Preferred for .NET 8+)
```csharp
// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ Group related endpoints
var users = app.MapGroup("/api/users").RequireAuthorization();
users.MapGet("/", GetAllUsers);
users.MapGet("/{id:int}", GetUserById);
users.MapPost("/", CreateUser);

// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ Use typed results
static async Task<Results<Ok<UserDto>, NotFound>> GetUserById(
    int id, IUserService svc, CancellationToken ct) =>
    await svc.GetAsync(id, ct) is { } user
        ? TypedResults.Ok(user.ToDto())
        : TypedResults.NotFound();
```

### Middleware
```csharp
// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ Use IMiddleware for DI support
public sealed class CorrelationMiddleware(RequestDelegate next) : IMiddleware
{
    public async Task InvokeAsync(HttpContext ctx, RequestDelegate _next)
    {
        ctx.Response.Headers["X-Correlation-ID"] = 
            ctx.Request.Headers.TryGetValue("X-Correlation-ID", out var v) 
            ? v.ToString() 
            : Guid.NewGuid().ToString("N");
        await next(ctx);
    }
}
```

## Entity Framework Core

### Query Best Practices
```csharp
// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ Use AsNoTracking for read-only queries
var users = await context.Users
    .AsNoTracking()
    .Where(u => u.IsActive)
    .Select(u => new UserDto(u.Id, u.Name))  // Project early
    .ToListAsync(ct);

// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ Avoid N+1 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â use Include or split queries
var orders = await context.Orders
    .Include(o => o.Items)
    .AsSplitQuery()
    .ToListAsync(ct);

// ÃƒÂ¢Ã‚ÂÃ…â€™ Never load then filter in memory
var all = await context.Users.ToListAsync();
var active = all.Where(u => u.IsActive); // Loads entire table!
```

## Clean Architecture Layout

```
src/
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Domain/           # Entities, Value Objects, Domain Events, Interfaces
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Application/      # Use Cases, Commands, Queries, DTOs, Validators
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ Infrastructure/   # EF Core, External APIs, Email, File Storage
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ API/              # Controllers/Endpoints, Middleware, Filters
```

## Testing Standards

```csharp
// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ xUnit + FluentAssertions + Testcontainers
public sealed class UserServiceTests : IAsyncLifetime
{
    private readonly PostgreSqlContainer _db = new PostgreSqlBuilder().Build();

    [Fact]
    public async Task CreateUser_WithValidData_ReturnsCreatedUser()
    {
        // Arrange
        var sut = CreateSut();
        var request = new CreateUserRequest("Alice", "alice@example.com");
        
        // Act
        var result = await sut.CreateAsync(request, CancellationToken.None);
        
        // Assert
        result.Should().BeSuccess();
        result.Value.Name.Should().Be("Alice");
    }
}
```

## Quality Checklist

Before completing .NET work, verify:
- [ ] All async methods use `CancellationToken`
- [ ] No `.Result` or `.Wait()` calls
- [ ] `IDisposable` types are properly disposed (using statements)
- [ ] Nullable reference types enabled and handled
- [ ] Logging uses `ILogger<T>`, not `Console.Write`
- [ ] Secrets not in config files ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â use `IConfiguration` / environment vars
- [ ] EF queries use `.AsNoTracking()` for reads
- [ ] Tests exist for all new public methods
