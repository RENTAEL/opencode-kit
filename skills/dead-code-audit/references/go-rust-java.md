# Dead code detection: Go, Rust, Java/Kotlin

## Go

```bash
go install golang.org/x/tools/cmd/deadcode@latest
deadcode ./...                       # whole-program reachability from main/tests
deadcode -test ./...                 # count test usage as alive

go install honnef.co/go/tools/cmd/staticcheck@latest
staticcheck ./...                    # U1000 = unused code checks
```

`deadcode` does true reachability analysis from entry points, so it is the most
trustworthy tool in this whole skill. Caveats:

- Library packages (no `main`) make everything exported look "dead" to a
  reachability tool; scope claims to unexported symbols there.
- Reflection (`reflect.Value.Call`, struct tags feeding encoders) can hide usage.
- Build tags: run once per meaningful tag combination (`GOOS`, `//go:build`) or
  platform-specific code will be falsely flagged.

## Rust

The compiler already does most of the work:

```bash
cargo build 2>&1 | grep -A2 "warning: .* never used"
# or force it loud:
RUSTFLAGS="-W dead_code -W unused" cargo check
```

Unused dependencies:

```bash
cargo install cargo-machete && cargo machete     # fast, regex-based
# or (needs nightly, precise): cargo +nightly udeps
```

Traps: `#[allow(dead_code)]` hides findings (grep for it and report those blocks
separately); trait impls and FFI (`#[no_mangle]`, `extern "C"`) look unused;
feature-gated code needs `cargo check --all-features` too.

## Java / Kotlin

No single great CLI tool. Layered approach:

```bash
# unused imports and simple issues
# PMD with the "unusedcode" ruleset:
pmd check -d src -R category/java/bestpractices.xml -f text | grep -i unused
```

- IntelliJ inspections ("Unused declaration") are the gold standard; if the user
  works locally, recommend running them there for the definitive pass.
- For unused public methods across modules, use the manual method from
  `manual-analysis.md` with the symbol index: Java's reflection, Spring DI,
  `@Autowired`, JPA entities, and serialization make automated Tier 1 claims
  unsafe. Anything with a Spring/JPA/Jackson annotation is Tier 2 minimum.
- Unused Maven/Gradle dependencies: `mvn dependency:analyze` or the Gradle
  `dependency-analysis` plugin.
