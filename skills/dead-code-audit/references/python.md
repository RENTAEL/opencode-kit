# Dead code detection: Python

## Primary tool: vulture

```bash
pip install vulture --break-system-packages
vulture <path> --min-confidence 60 --sort-by-size
```

- `--min-confidence 100` gives only certain findings (unreachable code, unused
  imports). Use 60 as the working default, then verify.
- `--sort-by-size` surfaces the biggest wins first, which matters on large repos.
- Whitelist known-dynamic names: `vulture <path> whitelist.py` where whitelist.py
  just references the symbols vulture should ignore.

## Secondary checks

```bash
pip install pyflakes --break-system-packages
pyflakes <path>          # unused imports and variables, very low false-positive rate
```

Unused dependencies: compare `requirements.txt` / `pyproject.toml` against actual
imports. `pip install deptry --break-system-packages && deptry <path>` does this well.

## Python-specific false-positive traps

Treat these as Tier 2 or 3, never Tier 1, even if vulture flags them:

- **Dunder methods** (`__enter__`, `__str__`, etc.) - called by the runtime.
- **`getattr`/`globals()`/`importlib` targets** - grep the symbol as a string first.
- **Decorated registrations** - Flask/FastAPI routes, Celery tasks, click commands,
  pytest fixtures, signal handlers, `@register` patterns. The decorator IS the caller.
- **Django/SQLAlchemy model fields and Meta classes** - referenced by the ORM.
- **`__all__` exports and package `__init__.py` re-exports** - public API surface.
- **Abstract method overrides** - a subclass method may look unused but be called
  through the base class interface. Check for the method name on the base.
- **Pickle/serialization targets** - classes only instantiated from stored data.

## Unreachable code

Vulture at confidence 100 catches code after `return`/`raise`/`continue`. Also
grep for `if False:` and `if 0:` blocks and always-false version gates like
`if sys.version_info < (3, 0):` in a py3-only project.
