#!/usr/bin/env python3
"""Django Dev Pro - OpenCode skill helper for Django / Django REST Framework.

This module uses only the Python standard library at runtime.  It generates
Django/DRF code from templates and runs configured project commands via
subprocess.  It does **not** import Django directly.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

CONFIG_DIR = Path.home() / ".django-dev-pro"
CONFIG_FILE = CONFIG_DIR / "commands.json"
TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"


class DjangoDevPro:
    """Helper class that detects a Django project, loads per-project config and
    performs code-generation / test tasks.
    """

    def __init__(
        self,
        project_path: str | Path | None = None,
        config_path: str | Path | None = None,
    ) -> None:
        self.config_path = Path(config_path) if config_path else CONFIG_FILE
        self.project: Path | None = None
        self.config: dict[str, Any] = {}

        if project_path:
            candidate = Path(project_path).resolve()
            if self._is_django_project(candidate):
                self.project = candidate
        else:
            self.project = self._detect_project(Path.cwd())

        self.load_config()

    # ------------------------------------------------------------------
    # Project detection
    # ------------------------------------------------------------------
    @staticmethod
    def _is_django_project(path: Path) -> bool:
        if not path.is_dir():
            return False
        return (
            (path / "manage.py").exists()
            or (path / "apps").is_dir()
            or (path / "core").is_dir()
        )

    def _detect_project(self, cwd: Path) -> Path | None:
        cur = cwd
        for _ in range(10):
            if self._is_django_project(cur):
                return cur
            parent = cur.parent
            if parent == cur:
                break
            cur = parent
        return None

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------
    def load_config(self) -> dict[str, Any]:
        if self.config_path.exists():
            try:
                self.config = json.loads(
                    self.config_path.read_text(encoding="utf-8")
                )
            except json.JSONDecodeError as exc:
                print(
                    f"⚠️  Warning: {self.config_path} contains invalid JSON ({exc}). "
                    "Starting with an empty configuration."
                )
                self.config = {}
        else:
            self.config = {}

        if self.project:
            key = self.project.name
            if key not in self.config:
                self.config[key] = {
                    "project_path": str(self.project),
                    "pyenv_env_name": "",
                    "env_file": ".env",
                    "load_env_before_commands": False,
                    "commands": {
                        "test": "python3 manage.py test",
                        "migrate": "python3 manage.py migrate",
                        "makemigrations": "python3 manage.py makemigrations",
                        "runserver": "python3 manage.py runserver",
                    },
                }
                self.save_config()
                print(
                    f"ℹ️  Created default configuration for '{key}' in {self.config_path}. "
                    "Edit it manually if you need pyenv, .env loading or custom commands."
                )

        return self.config

    def save_config(self) -> None:
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self.config_path.write_text(
            json.dumps(self.config, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def _project_key(self) -> str | None:
        if not self.project:
            return None
        key = self.project.name
        if key in self.config:
            return key
        for k, v in self.config.items():
            if v.get("project_path") == str(self.project):
                return k
        return key

    def _project_config(self) -> dict[str, Any]:
        key = self._project_key()
        if not key:
            return {}
        return self.config.get(key, {})

    def _command(self, name: str) -> str:
        cfg = self._project_config()
        return cfg.get("commands", {}).get(name, f"python manage.py {name}")

    # ------------------------------------------------------------------
    # Environment loading
    # ------------------------------------------------------------------
    @staticmethod
    def _load_env_file(path: Path) -> dict[str, str]:
        """Load KEY=VALUE pairs from an .env-style file.

        Uses python-dotenv when available; otherwise falls back to a simple
        stdlib parser that skips comments and empty lines.
        """
        values: dict[str, str] = {}
        try:
            from dotenv import dotenv_values  # type: ignore[import-not-found]

            raw = dotenv_values(str(path))
            for k, v in raw.items():
                if k is not None and v is not None:
                    values[k] = v
            return values
        except ImportError:
            pass

        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip("'\"")
            values[key] = value
        return values

    # ------------------------------------------------------------------
    # Command execution
    # ------------------------------------------------------------------
    def _run(
        self, cmd: str, cwd: Path | None = None
    ) -> subprocess.CompletedProcess[str]:
        target = cwd or self.project
        cfg = self._project_config()
        env = os.environ.copy()

        # Load .env file when configured
        env_file = cfg.get("env_file")
        if cfg.get("load_env_before_commands") and env_file:
            env_path = self.project / env_file if self.project else Path(env_file)
            if env_path.exists():
                try:
                    env_vars = self._load_env_file(env_path)
                    env.update(env_vars)
                    print(f"  Loading environment variables from {env_path}")
                except OSError as exc:
                    print(f"  Warning: could not read {env_path}: {exc}")
            else:
                print(f"  Warning: env file not found: {env_path}")

        # Optional pyenv activation
        pyenv_env = cfg.get("pyenv_env_name", "")
        if pyenv_env:
            full_cmd = (
                f'if command -v pyenv >/dev/null 2>&1; then '
                f'eval "$(pyenv init -)" && pyenv shell {pyenv_env} && {cmd}; '
                f'else echo "pyenv not found, running without activation" >&2 && {cmd}; fi'
            )
        else:
            full_cmd = cmd

        print(f"$ {full_cmd}")
        return subprocess.run(
            full_cmd,
            shell=True,
            cwd=target,
            capture_output=True,
            text=True,
            env=env,
        )

    # ------------------------------------------------------------------
    # --status
    # ------------------------------------------------------------------
    def status(self) -> str:
        if not self.project:
            return (
                "No Django project detected.\n\n"
                "A project is detected when any of the following exists\n"
                "in the current directory or an ancestor:\n"
                "  - manage.py\n"
                "  - apps/ directory\n"
                "  - core/ directory\n\n"
                "Navigate to the project root and try again."
            )

        key = self._project_key()
        cfg = self.config.get(key, {})
        lines = [
            f"Project: {self.project.name}",
            f"Path: {self.project}",
            f"Configured: {'yes' if cfg else 'no'}",
        ]

        if cfg:
            lines.append(
                f"Test command: {cfg.get('commands', {}).get('test', 'python manage.py test')}"
            )
            lines.append(f"Env file: {cfg.get('env_file', '-')}")
            lines.append(
                f"Load env before commands: {cfg.get('load_env_before_commands', False)}"
            )
            if cfg.get("pyenv_env_name"):
                lines.append(f"pyenv env: {cfg['pyenv_env_name']}")

        apps: list[str] = []
        apps_dir = self.project / "apps"
        if apps_dir.is_dir():
            apps = [
                d.name
                for d in apps_dir.iterdir()
                if d.is_dir() and not d.name.startswith((".", "_"))
            ]
        elif (self.project / "core").is_dir():
            apps = ["core"]

        lines.append(f"Apps found: {', '.join(apps) if apps else 'none'}")
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # --test [--auto-fix]
    # ------------------------------------------------------------------
    def test(self, auto_fix: bool = False) -> int:
        if not self.project:
            print(
                "No Django project detected. Look for manage.py, apps/ or core/ "
                "in the current directory or an ancestor."
            )
            return 1

        cmd = self._command("test")
        result = self._run(cmd)
        self._print_result(result)

        if result.returncode != 0 and auto_fix:
            print("\n🔧 Auto-fix enabled (simple): attempting common fixes...")
            if self._simple_auto_fix():
                print("\n🚀 Re-running tests after auto-fix...")
                result = self._run(cmd)
                self._print_result(result)

        return result.returncode

    def _print_result(self, result: subprocess.CompletedProcess[str]) -> None:
        if result.stdout:
            print("--- stdout ---")
            print(result.stdout)
        if result.stderr:
            print("--- stderr ---")
            print(result.stderr)
        if result.returncode != 0:
            print(f"--- exit code: {result.returncode} ---")

    def _simple_auto_fix(self) -> bool:
        """Apply very simple fixes such as missing __init__.py files."""
        fixed = False
        apps_dir = self.project / "apps"
        if apps_dir.is_dir():
            for app in apps_dir.iterdir():
                init = app / "__init__.py"
                if app.is_dir() and not init.exists():
                    init.touch()
                    print(f"  Created missing {init}")
                    fixed = True
        if not fixed:
            print("  No obvious simple fixes were applied.")
        return fixed

    # ------------------------------------------------------------------
    # Code generation helpers
    # ------------------------------------------------------------------
    def _render(self, template_name: str, context: dict[str, str]) -> str:
        path = TEMPLATES_DIR / template_name
        if not path.exists():
            raise FileNotFoundError(f"Template not found: {path}")
        text = path.read_text(encoding="utf-8")
        for key, value in context.items():
            text = text.replace(f"{{{{ {key} }}}}", str(value))
        return text

    @staticmethod
    def _is_numeric(value: str) -> bool:
        return bool(re.fullmatch(r"-?\d+(\.\d+)?", value))

    @staticmethod
    def _parse_fields(
        fields: list[str],
    ) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
        model_fields: list[dict[str, str]] = []
        serializer_fields: list[dict[str, str]] = []

        for raw in fields:
            parts = raw.split(":", 2)
            name = parts[0].strip()
            ftype = parts[1].strip() if len(parts) > 1 else "CharField"
            extra = parts[2].strip() if len(parts) > 2 else ""

            field_args: list[str] = []

            # Default value: explicit "default=..." or raw third part
            default_value: str | None = None
            default_match = re.search(r"default=([^,]+)", extra)
            if default_match:
                default_value = default_match.group(1).strip()
            elif extra:
                default_value = extra

            if default_value is not None:
                if ftype in ("IntegerField", "DecimalField", "FloatField"):
                    field_args.append(f"default={default_value}")
                elif ftype == "BooleanField":
                    field_args.append(f"default={default_value}")
                else:
                    field_args.append(f"default='{default_value}'")

            if ftype == "CharField":
                field_args.append("max_length=255")
            elif ftype == "TextField":
                pass
            elif ftype == "DecimalField":
                if "decimal_places" not in extra and "max_digits" not in extra:
                    field_args.append("max_digits=10, decimal_places=2")
            elif ftype == "BooleanField":
                pass
            elif ftype == "DateTimeField":
                pass
            elif ftype == "ForeignKey":
                field_args.append("to='auth.User', on_delete=models.CASCADE")
            elif ftype == "EmailField":
                field_args.append("max_length=255")
            elif ftype == "URLField":
                field_args.append("max_length=500")

            arg_str = ", ".join(field_args)
            model_fields.append({"name": name, "type": ftype, "args": arg_str})
            serializer_fields.append({"name": name})

        return model_fields, serializer_fields

    def _write(self, target: Path, content: str) -> None:
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            backup = target.with_suffix(target.suffix + ".bak")
            shutil.copy2(target, backup)
            print(f"  Backed up existing file to {backup}")
        target.write_text(content, encoding="utf-8")
        print(f"  Generated {target}")

    def _modify_file(self, target: Path, new_content: str) -> None:
        """Modify an existing file, keeping a backup."""
        if not target.exists():
            return
        backup = target.with_suffix(target.suffix + ".bak")
        shutil.copy2(target, backup)
        print(f"  Backed up existing file to {backup}")
        target.write_text(new_content, encoding="utf-8")
        print(f"  Updated {target}")

    def _app_dir(self, app_name: str) -> Path:
        apps_dir = self.project / "apps" / app_name
        if apps_dir.is_dir() or (self.project / "apps").is_dir():
            return apps_dir
        return self.project / app_name

    # ------------------------------------------------------------------
    # --generate-crud
    # ------------------------------------------------------------------
    def generate_crud(
        self, model_name: str, app_name: str, fields: list[str]
    ) -> int:
        if not self.project:
            print(
                "No Django project detected. Look for manage.py, apps/ or core/ "
                "in the current directory or an ancestor."
            )
            return 1

        app_dir = self._app_dir(app_name)
        app_dir.mkdir(parents=True, exist_ok=True)

        model_fields, serializer_fields = self._parse_fields(fields)

        model_snake = re.sub(r"(?<!^)(?=[A-Z])", "_", model_name).lower()
        model_plural = model_snake + "s"

        if model_fields:
            fields_model = "\n    ".join(
                f"{f['name']} = models.{f['type']}({f['args']})"
                for f in model_fields
            )
            fields_serializer = ", ".join(
                ['"id"'] + [f'"{f["name"]}"' for f in serializer_fields]
            )
        else:
            fields_model = "pass"
            fields_serializer = '"id"'

        context = {
            "app_name": app_name,
            "model_name": model_name,
            "model_snake": model_snake,
            "model_plural": model_plural,
            "fields_model": fields_model,
            "fields_serializer": fields_serializer,
            "url_basename": model_snake,
        }

        self._write(app_dir / "models.py", self._render("model.py.tpl", context))
        self._write(
            app_dir / "serializers.py", self._render("serializer.py.tpl", context)
        )
        self._write(app_dir / "views.py", self._render("viewset.py.tpl", context))
        self._write(app_dir / "tests.py", self._render("test.py.tpl", context))
        self._write(app_dir / "urls.py", self._render("url.py.tpl", context))

        self._register_project_urls(app_name)

        print(f"\n✅ CRUD generated for {model_name} in app '{app_name}'")
        return 0

    # ------------------------------------------------------------------
    # URL registration
    # ------------------------------------------------------------------
    def _detect_project_urls(self) -> Path | None:
        """Find the main project urls.py file."""
        if not self.project:
            return None

        root = self.project
        candidates: list[Path] = [
            root / "config" / "urls.py",
            root / "urls.py",
            root / root.name / "urls.py",
        ]

        for subdir in root.iterdir():
            if (
                subdir.is_dir()
                and subdir.name not in ("apps", "templates", "static", "__pycache__", ".git")
                and not subdir.name.startswith(".")
            ):
                cand = subdir / "urls.py"
                if cand not in candidates:
                    candidates.append(cand)

        for cand in candidates:
            if cand.exists() and "urlpatterns" in cand.read_text(encoding="utf-8"):
                return cand
        return None

    def _register_project_urls(self, app_name: str) -> None:
        urls_file = self._detect_project_urls()
        if not urls_file:
            print(
                f"\n⚠️  Could not find the main project urls.py. "
                f"Add the following line manually to your project URLs:\n"
                f"    path('{app_name}/', include('{app_name}.urls')),"
            )
            return

        content = urls_file.read_text(encoding="utf-8")
        include_path = f"{app_name}.urls"
        if include_path in content:
            print(f"\nℹ️  {urls_file} already includes '{include_path}'")
            return

        # Ensure include is imported
        if "from django.urls import" in content:
            if "include" not in content.split("from django.urls import", 1)[1].split("\n", 1)[0]:
                content = re.sub(
                    r"(from django\.urls import\s+)([^\n]+)",
                    r"\1include, \2",
                    content,
                    count=1,
                )
        else:
            content = f"from django.urls import path, include\n{content}"

        # Insert the new path into urlpatterns
        new_path_line = f"    path('{app_name}/', include('{app_name}.urls')),"
        content = re.sub(
            r"(urlpatterns\s*=\s*\[)",
            rf"\1\n{new_path_line}\n",
            content,
            count=1,
        )

        self._modify_file(urls_file, content)
        print(f"\n✅ Registered {app_name} URLs in {urls_file}")

    # ------------------------------------------------------------------
    # --add-field
    # ------------------------------------------------------------------
    def add_field(self, model_name: str, app_name: str, field: str) -> int:
        if not self.project:
            print(
                "No Django project detected. Look for manage.py, apps/ or core/ "
                "in the current directory or an ancestor."
            )
            return 1

        app_dir = self._app_dir(app_name)
        model_file = app_dir / "models.py"
        if not model_file.exists():
            print(f"Model file not found: {model_file}")
            return 1

        model_fields, _ = self._parse_fields([field])
        if not model_fields:
            print(f"Could not parse field: {field}")
            return 1

        f = model_fields[0]
        field_name = f["name"]
        line = f"    {field_name} = models.{f['type']}({f['args']})\n"
        content = model_file.read_text(encoding="utf-8").rstrip()
        content += f"\n\n    # Added by django-dev-pro\n{line}"
        model_file.write_text(content, encoding="utf-8")
        print(f"✅ Added field '{field_name}' to {model_name} in {model_file}")

        # Try to update the WriteSerializer fields
        serializers_file = app_dir / "serializers.py"
        if serializers_file.exists():
            self._add_field_to_serializer(serializers_file, field_name)

        # Optionally append a minimal test
        tests_file = app_dir / "tests.py"
        if tests_file.exists():
            self._add_field_test(tests_file, model_name, field_name)

        return 0

    def _add_field_to_serializer(self, serializers_file: Path, field_name: str) -> None:
        content = serializers_file.read_text(encoding="utf-8")

        write_block_re = re.compile(
            r"(class\s+\w+WriteSerializer\s*\([^)]*\):)(.*?)(?=^class\s|\Z)",
            re.DOTALL | re.MULTILINE,
        )

        def repl(match: re.Match[str]) -> str:
            block = match.group(2)
            new_block = re.sub(
                r"(fields\s*=\s*\[)([^\]]*?)(\])",
                lambda m: (
                    f"{m.group(1)}"
                    f"{m.group(2)}{(', ' if m.group(2).strip() else '')}\"{field_name}\""
                    f"{m.group(3)}"
                ),
                block,
                count=1,
            )
            return match.group(1) + new_block

        new_content = write_block_re.sub(repl, content)
        if new_content == content:
            print(
                f"  Could not locate WriteSerializer fields in {serializers_file}"
            )
            return

        self._modify_file(serializers_file, new_content)
        print(f"  Updated WriteSerializer fields in {serializers_file}")

    def _add_field_test(self, tests_file: Path, model_name: str, field_name: str) -> None:
        model_snake = re.sub(r"(?<!^)(?=[A-Z])", "_", model_name).lower()
        test_method = (
            f"\n\n    def test_{model_snake}_{field_name}_field(self):\n"
            f"        self.assertTrue(hasattr({model_name}, '{field_name}'))\n"
        )
        content = tests_file.read_text(encoding="utf-8").rstrip() + test_method
        self._modify_file(tests_file, content)
        print(f"  Added minimal test for '{field_name}' in {tests_file}")


# ----------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="django-dev-pro",
        description=(
            "OpenCode skill helper for Django and Django REST Framework projects."
        ),
    )
    parser.add_argument(
        "--project", "-p", help="Root path of the Django project"
    )
    parser.add_argument(
        "--config", "-c", help="Path to commands.json config file"
    )
    parser.add_argument(
        "--status", action="store_true", help="Show detected project status"
    )
    parser.add_argument(
        "--test", action="store_true", help="Run the project test suite"
    )
    parser.add_argument(
        "--auto-fix",
        action="store_true",
        help="Enable simple auto-fix when running tests",
    )
    parser.add_argument(
        "--generate-crud", metavar="MODEL", help="Generate a CRUD for MODEL"
    )
    parser.add_argument(
        "--model", "-m", metavar="MODEL", help="Model name for --add-field"
    )
    parser.add_argument(
        "--app", "-a", metavar="APP", help="App name (default: derived from model)"
    )
    parser.add_argument(
        "--fields",
        nargs="+",
        default=[],
        metavar="FIELD",
        help="Fields as name:type[:args] (e.g. name:CharField price:DecimalField priority:IntegerField:0)",
    )
    parser.add_argument(
        "--add-field",
        metavar="FIELD",
        dest="add_field",
        help="Add a field to an existing model (format: name:type[:args])",
    )

    args = parser.parse_args(argv)

    skill = DjangoDevPro(project_path=args.project, config_path=args.config)

    if args.status:
        print(skill.status())
        return 0

    if args.test:
        return skill.test(auto_fix=args.auto_fix)

    if args.generate_crud:
        app = args.app or (args.generate_crud.lower() + "s")
        return skill.generate_crud(args.generate_crud, app, args.fields)

    if args.add_field:
        if not args.model:
            parser.error("--add-field requires --model")
        app = args.app or "core"
        return skill.add_field(args.model, app, args.add_field)

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
