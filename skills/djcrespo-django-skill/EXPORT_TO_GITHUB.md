# Exportar Django Dev Pro Skill a GitHub

Esta guía te ayudará a exportar y compartir la skill en GitHub para que otros la usen con OpenCode.

## 📋 Pasos para Exportar

### Opción 1: Usando el Script (Recomendado)

```bash
cd /path/to/django-skill

# Dale permisos de ejecución
chmod +x setup_github.sh

# Ejecuta el script
./setup_github.sh
```

El script te pedirá:
1. Tu usuario de GitHub
2. Nombre del repositorio (`django-skill` por defecto)

Luego deberás:
1. Crear un repositorio en https://github.com/new
2. Hacer push: `git push -u origin main`

### Opción 2: Manual

```bash
cd /path/to/django-skill

# Inicializar git
git init

# Agregar remote (reemplaza usuario y repo)
git remote add origin https://github.com/tu-usuario/django-skill.git

# Crear rama main
git checkout -b main

# Agregar archivos
git add .

# Commit inicial
git commit -m "Initial commit: Django Dev Pro Skill"

# Crear repositorio en GitHub (https://github.com/new)
# SIN inicializarlo con archivos

# Push
git push -u origin main
```

---

## 📦 Archivos Incluidos en el Repositorio

```
django-skill/
├── SKILL.md                     ← Definición requerida por OpenCode
├── skill.yml                    ← Metadata
├── README.md                    ← Guía de uso
├── README_GITHUB.md             ← README principal para GitHub
├── INSTALLATION.md              ← Guía de instalación
├── SKILL_INSTALL.md             ← Instalación paso a paso
├── CONTRIBUTING.md              ← Guía de contribución
├── CHANGELOG.md                 ← Historial de cambios
├── LICENSE                      ← MIT License
├── requirements.txt             ← Dependencias
├── install.sh                   ← Script de instalación
├── setup_github.sh              ← Setup de GitHub
├── lib/                         ← Código fuente del helper
│   ├── __init__.py
│   └── main.py
├── configs/                     ← Ejemplos de configuración
│   └── project_commands.example.json
├── templates/                   ← Plantillas de generación de código
│   ├── model.py.tpl
│   ├── serializer.py.tpl
│   ├── viewset.py.tpl
│   ├── test.py.tpl
│   └── url.py.tpl
├── examples/                    ← Ejemplos de uso
├── legacy/                      ← Archivos deprecated de versiones anteriores
└── .gitignore                   ← Archivo gitignore
```

---

## 🔑 Configurar Archivos Importantes

### 1. Renombrar README

```bash
cd /path/to/django-skill

# El README principal para GitHub es README_GITHUB.md
# Si quieres usarlo como principal:
cp README_GITHUB.md README_GITHUB_bak.md
mv README.md README_LOCAL.md
mv README_GITHUB.md README.md
```

### 2. Actualizar skill.yml

```yaml
name: django-dev-pro
version: 1.0.0
author: tu-nombre                # ← Actualiza
repository: https://github.com/tu-usuario/django-skill  # ← Actualiza
```

---

## 🚀 Después de Subir a GitHub

### 1. Agregar Descripción en GitHub

En la página del repositorio, edita la descripción:

```
Use ONLY when working with Django or Django REST Framework projects to generate models, dual serializers, ViewSets, tests, fixtures, documentation, manage environments, and run/fix tests following project patterns.
```

### 2. Agregar Topics

En Settings → Repository details → Topics, agrega:
- `django`
- `django-rest-framework`
- `code-generation`
- `automation`
- `python`
- `opencode`
- `skill`

### 3. Crear Releases

```bash
# Tag de versión
git tag -a v1.0.0 -m "Initial release"
git push origin v1.0.0

# O desde GitHub:
# Releases → Create a new release → v1.0.0
```

### 4. Habilitar GitHub Pages (Opcional)

Si quieres documentación en web:
1. Settings → Pages
2. Source: main branch /docs folder
3. Crea carpeta `docs/` con HTML/Markdown

---

## 📝 Instalar desde GitHub (Para Otros)

Una vez subido, otros pueden instalar así:

### Opción 1: Clonar y Ejecutar Script

```bash
git clone https://github.com/tu-usuario/django-skill.git
cd django-skill
chmod +x install.sh
./install.sh
```

### Opción 2: Instalación Manual

```bash
mkdir -p ~/.config/opencode/skills
git clone https://github.com/tu-usuario/django-skill.git ~/.config/opencode/skills/django-dev-pro
```

Luego habilitar en `~/.config/opencode/opencode.json`:

```json
{
  "permission": {
    "skill": {
      "django-dev-pro": "allow"
    }
  }
}
```

Y reiniciar OpenCode.

---

## 🔄 Mantener Actualizado

### Hacer Cambios Localmente

```bash
# Edita archivos
nano SKILL.md

# Commit
git add .
git commit -m "feat: agregar nueva funcionalidad"

# Push
git push origin main
```

### Actualizar Versión

```bash
# Edita skill.yml
# version: 1.0.1

# Commit
git add skill.yml
git commit -m "chore: bump version to 1.0.1"

# Tag
git tag -a v1.0.1 -m "Version 1.0.1"

# Push
git push origin main
git push origin v1.0.1
```

---

## 🛠️ Integración con OpenCode

Para que otros usen la skill directamente en OpenCode:

1. Asegúrate de que `SKILL.md` exista en la raíz del repositorio
2. Verifica que el frontmatter de `SKILL.md` tenga `name: django-dev-pro`
3. Sube a GitHub
4. Los usuarios deben copiar el repo a `~/.config/opencode/skills/django-dev-pro/` y habilitar el permiso

---

## 📊 Badges de GitHub

Agrega a tu README:

```markdown
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/tu-usuario/django-skill?style=social)](https://github.com/tu-usuario/django-skill)
[![GitHub forks](https://img.shields.io/github/forks/tu-usuario/django-skill?style=social)](https://github.com/tu-usuario/django-skill)
```

---

## ⚠️ Importante

### .gitignore

Asegúrate de que `.gitignore` contiene:
- `~/.django-dev-pro/` (configuraciones de usuario)
- `__pycache__/`
- `.env.local`
- Credenciales y secrets

### No Subas

❌ Archivos de configuración de usuario (`~/.django-dev-pro/commands.json`)  
❌ Archivos `.env` con datos sensibles  
❌ Tokens o credenciales  
❌ Archivos grandes innecesarios

✅ Solo código fuente y documentación

---

## 🎉 ¡Listo!

Tu skill Django Dev Pro está lista para ser compartida. Otros pueden:

1. Clonarla desde GitHub
2. Instalarla automáticamente
3. Usarla en sus proyectos Django con OpenCode
4. Contribuir mejoras

---

## 📞 Soporte para Usuarios

Asegúrate de que en tu README dice:

```markdown
## Soporte

- 📖 [Documentación](README.md)
- 🐛 [Reportar Issues](https://github.com/tu-usuario/django-skill/issues)
- 💬 [Discussions](https://github.com/tu-usuario/django-skill/discussions)
- 📧 Email: tu@email.com
```

---

**¡Tu skill está lista para el mundo! 🚀**
