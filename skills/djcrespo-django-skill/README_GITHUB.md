# Django Dev Pro - Automatiza Django REST Framework

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/djcrespo/django-skill?style=social)](https://github.com/djcrespo/django-skill)

> **Django Dev Pro** es una skill para OpenCode que automatiza el flujo completo de desarrollo con Django REST Framework. Genera automáticamente Modelos, Serializers duales, ViewSets, Tests, Fixtures y Documentación siguiendo los patrones de tu proyecto.

## 🌟 Características Principales

- **🔍 Auto-Detección** - Detecta automáticamente proyectos Django
- **📚 Pattern Learning** - Aprende y replica tus patrones
- **⚙️ Code Generation** - Genera Modelo-Serializer-View-Tests automáticamente
- **🧪 Test Management** - Ejecuta y auto-corrige tests
- **📝 Auto-Documentation** - Genera docstrings automáticamente
- **🐍 Pyenv Integration** - Gestión de entornos virtuales
- **🔐 Env Variables** - Carga automática de `.env.local`
- **📦 Multi-Project** - Soporta múltiples proyectos simultáneamente
- **💾 Persistent Config** - Guarda configuración entre ejecuciones

## 📦 Instalación Rápida

```bash
# Clona el repositorio
git clone https://github.com/djcrespo/django-skill.git
cd django-skill

# Ejecuta el instalador
chmod +x install.sh
./install.sh
```

Luego habilita la skill en `~/.config/opencode/opencode.json`:

```json
{
  "permission": {
    "skill": {
      "django-dev-pro": "allow"
    }
  }
}
```

Y reinicia OpenCode.

## 🚀 Primeros Pasos

### 1. Inicializar (Primera Ejecución)

```bash
# Navega a tu proyecto Django
cd /path/to/your/django/project
```

```
Usa el skill django-dev-pro
```

Se te pedirá:
- Nombre del entorno pyenv (ej: `api-v2`)
- Comandos clave (`test`, `migrate`, `server`)
- Variables de configuración

### 2. Usar (Ejecuciones Posteriores)

```
Ejecuta los tests
```

```
Muestra el estado del proyecto
```

```
Ejecuta los tests y corrige los errores
```

## 📖 Documentación

| Documento | Descripción |
|-----------|-------------|
| [README.md](README.md) | Guía completa de uso |
| [SKILL_INSTALL.md](SKILL_INSTALL.md) | Instalación paso a paso |
| [INSTALLATION.md](INSTALLATION.md) | Guía de instalación en inglés |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Cómo contribuir |
| [examples/usage_examples.md](examples/usage_examples.md) | Ejemplos prácticos |

## 💻 Ejemplos de Uso

### Generar CRUD Completo

```
Crea un CRUD para Product con title, price y description
```

Genera automáticamente:
- ✅ Modelo con UUID, soft delete, timestamps
- ✅ Serializers duales (Write + Read)
- ✅ ViewSet REST con permisos
- ✅ Tests unitarios
- ✅ URLs registradas
- ✅ Documentación

### Agregar Campo a Modelo

```
Agrega un campo priority al modelo Task
```

Actualiza:
- ✅ Modelo
- ✅ Serializers
- ✅ Tests
- ✅ Genera migración

### Ejecutar y Corregir Tests

```
Ejecuta los tests y corrige los errores
```

Flujo automático:
1. Ejecuta tests
2. Detecta fallos
3. Auto-corrige errores
4. Re-ejecuta tests
5. Reporte final

## 🏗️ Estructura del Repositorio

```
django-skill/
├── SKILL.md                     ← Definición de la skill para OpenCode
├── skill.yml                    ← Metadata
├── README.md                    ← Guía de uso
├── README_GITHUB.md             ← README para GitHub
├── INSTALLATION.md              ← Guía de instalación
├── SKILL_INSTALL.md             ← Instalación paso a paso
├── CONTRIBUTING.md              ← Guía de contribución
├── CHANGELOG.md                 ← Historial de cambios
├── LICENSE                      ← MIT License
├── requirements.txt             ← Dependencias
├── install.sh                   ← Script de instalación
├── lib/                         ← Código fuente del helper
│   ├── __init__.py
│   └── main.py
├── configs/                     ← Ejemplos de configuración
├── templates/                   ← Plantillas de generación de código
│   ├── model.py.tpl
│   ├── serializer.py.tpl
│   ├── viewset.py.tpl
│   ├── test.py.tpl
│   └── url.py.tpl
├── examples/                    ← Ejemplos de uso
└── legacy/                      ← Archivos deprecated de versiones anteriores
```

## 🔧 Configuración

La skill crea un archivo de configuración en:

```
~/.django-dev-pro/commands.json
```

Ejemplo:

```json
{
  "wpd-api": {
    "project_path": "/path/to/project",
    "pyenv_env_name": "api-v2",
    "env_file": ".env.local",
    "load_env_before_commands": true,
    "commands": {
      "setup": "pyenv activate api-v2 && source .env.local && pip install -r requirements.txt",
      "test": "python manage.py test",
      "migrate": "python manage.py migrate"
    }
  }
}
```

Ver ejemplo completo en [`configs/project_commands.example.json`](configs/project_commands.example.json).

## 📋 Requisitos

- Python 3.10+
- Django 5.0+
- Django REST Framework 3.14+
- OpenCode
- Git (opcional, para instalación)

## 🐛 Troubleshooting

### Error: "No se detectó un proyecto Django"

```bash
# Asegúrate de que manage.py existe
ls -la manage.py

# Ejecuta desde la raíz del proyecto
cd /path/to/project
```

### Error: "Entorno pyenv no encontrado"

```bash
# Verifica que existe
pyenv versions | grep tu-entorno

# O créalo
pyenv virtualenv 3.10.0 tu-entorno
```

### Error: "Skill no encontrado"

```bash
# Verifica la instalación
ls -la ~/.config/opencode/skills/django-dev-pro/

# Verifica los permisos en ~/.config/opencode/opencode.json
```

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Lee [CONTRIBUTING.md](CONTRIBUTING.md) para detalles.

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Distribuido bajo la licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

## 🙏 Agradecimientos

- [Django](https://www.djangoproject.com/) - El framework web
- [Django REST Framework](https://www.django-rest-framework.org/) - API REST
- [OpenCode](https://opencode.ai/) - La plataforma de skills

## 📞 Soporte

- 📖 [Documentación](README.md)
- 🐛 [Reportar Issues](https://github.com/djcrespo/django-skill/issues)
- 💬 [Discussions](https://github.com/djcrespo/django-skill/discussions)

## ⭐ Si te Gusta, Dale una Estrella!

Ayuda a otros a descubrir este proyecto en GitHub.

---

**Hecho con ❤️ por [djcrespo](https://github.com/djcrespo)**

Transforma tu desarrollo Django. Automatiza todo. Enfócate en la lógica de negocio. 🚀
