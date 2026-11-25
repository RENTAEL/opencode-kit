# Django Dev Pro - Installation & Registration Guide

## 📦 Installation

The Django Dev Pro Skill is installed as an OpenCode skill at:

```
~/.config/opencode/skills/django-dev-pro/
```

### Prerequisites

- **OpenCode** installed and working (`opencode --version`)
- **Python 3.10+** (`python3 --version`)
- **Django** and **Django REST Framework** (for using the skill)

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/djcrespo/django-skill.git
cd django-skill
```

### 2. Run the Installer

```bash
chmod +x install.sh
./install.sh
```

Or copy the files manually:

```bash
mkdir -p ~/.config/opencode/skills
cp -r /path/to/cloned/django-skill ~/.config/opencode/skills/django-dev-pro
```

### 3. Enable the Skill in OpenCode

Edit or create `~/.config/opencode/opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "permission": {
    "skill": {
      "django-dev-pro": "allow"
    }
  }
}
```

### 4. Restart OpenCode

Close and reopen your terminal, or restart the OpenCode service.

---

## 📝 First Time Setup

Navigate to your Django project:

```bash
cd /path/to/your/django/project
```

Then invoke the skill in natural language:

```
Usa el skill django-dev-pro
```

The skill will prompt for:
- **Pyenv environment name** (e.g., `api-v2`)
- **Django commands** (`test`, `migrate`, `runserver`, etc.)
- **`.env` file** (usually `.env.local`)

Configuration is saved to `~/.django-dev-pro/commands.json`.

---

## 📂 Directory Structure

```
~/.config/opencode/
└── skills/
    └── django-dev-pro/          ← Main skill directory
        ├── SKILL.md             ← Required skill definition
        ├── skill.yml            ← Metadata
        ├── README.md            ← Full documentation
        ├── SKILL_INSTALL.md     ← Installation guide
        ├── lib/                 ← Skill helper source
        │   ├── __init__.py
        │   └── main.py
        ├── configs/             ← Configuration examples
        ├── templates/           ← Code generation templates
        └── examples/            ← Usage examples

~/.django-dev-pro/
└── commands.json                ← User configuration
```

---

## 🔧 Integration with OpenCode

The skill is invoked through OpenCode in natural language:

```
Usa el skill django-dev-pro
```

Examples:

```
Crea un CRUD para Product con name, description y price
```

```
Ejecuta los tests y corrige los errores
```

```
Agrega un campo priority al modelo Task
```

---

## 📖 Usage Examples

### Initialize Project (First Time)

```bash
cd /path/to/django/project
```

```
Usa el skill django-dev-pro
```

### Run Tests

```
Ejecuta los tests del proyecto
```

### Auto-Fix Failed Tests

```
Ejecuta los tests y corrige los errores
```

### Generate Complete CRUD

```
Crea un CRUD para Product con name, description y price
```

### Add Field to Model

```
Agrega un campo priority al modelo Task
```

### View Project Status

```
Muestra el estado del proyecto
```

---

## 🛠️ Advanced Features

### Multi-Project Support

The skill automatically detects and manages multiple Django projects. Change to the project directory and invoke the skill:

```bash
cd /path/to/your/first-project
```

```
Ejecuta los tests
```

```bash
cd /path/to/your/second-project
```

```
Ejecuta los tests
```

### Environment Variable Loading

Automatically loads `.env.local` before running commands when configured:

```bash
source .env.local && python manage.py test
```

### Pattern Learning

The skill learns from your project structure and replicates patterns:

- UUID vs INT primary keys
- Soft deletes (`is_active`)
- Timestamps (`created_at`, `updated_at`)
- Dual serializers (Write + Read)
- Naming conventions

---

## 🔍 Troubleshooting

### Skill Not Found

```bash
# Verify installation
ls -la ~/.config/opencode/skills/django-dev-pro/

# Verify SKILL.md exists
ls -la ~/.config/opencode/skills/django-dev-pro/SKILL.md
```

### Permission Denied

Ensure the skill is allowed in `~/.config/opencode/opencode.json`:

```json
{
  "permission": {
    "skill": {
      "django-dev-pro": "allow"
    }
  }
}
```

### Project Not Detected

```bash
# Ensure manage.py exists
ls -la manage.py

# Ensure you're in project root
pwd
```

### Configuration Lost

```bash
# Check configuration file
cat ~/.django-dev-pro/commands.json
```

Then reconfigure with:

```
Configura este proyecto Django
```

---

## 📚 Documentation

- **Full Guide**: `~/.config/opencode/skills/django-dev-pro/README.md`
- **Skill Definition**: `~/.config/opencode/skills/django-dev-pro/SKILL.md`
- **Examples**: `~/.config/opencode/skills/django-dev-pro/examples/usage_examples.md`
- **Metadata**: `~/.config/opencode/skills/django-dev-pro/skill.yml`
- **Skill Definition**: `~/.config/opencode/skills/django-dev-pro/SKILL.md`

---

## 📞 Support

For issues or suggestions:
https://github.com/djcrespo/django-skill/issues

---

## ✅ Verification

To verify the skill is properly installed:

```bash
python3 << 'EOF'
from pathlib import Path
skill_dir = Path.home() / ".config/opencode/skills/django-dev-pro"
assert skill_dir.exists(), f"Skill directory not found: {skill_dir}"
assert (skill_dir / "SKILL.md").exists(), "SKILL.md is missing"
print("✅ Django Dev Pro Skill is properly installed")
EOF
```

---

**Installation Complete!** 🎉

Your Django Dev Pro Skill is now ready to use with OpenCode.
