# Django Dev Pro Skill

**Automatiza el flujo completo de desarrollo con Django REST Framework**

---

## 🚀 Instalación

Para instalar este skill en opencode, sigue estos pasos resumidos o consulta la guía completa en [SKILL_INSTALL.md](SKILL_INSTALL.md).

### Requisitos Previos

- **opencode** instalado (`opencode --version`)
- **Python 3.8+** (`python3 --version`)
- **Django** y **Django REST Framework** (`pip install django djangorestframework`)

### Instalación Rápida

```bash
# 1. Crear directorio de skills (si no existe)
mkdir -p ~/.config/opencode/skills

# 2. Copiar el skill
cp -r /ruta/al/clon/django-skill ~/.config/opencode/skills/django-dev-pro

# 3. Verificar estructura
ls ~/.config/opencode/skills/django-dev-pro/

# 4. Habilitar permiso
# Edita ~/.config/opencode/opencode.json y añade:
# {
#   "permission": { "skill": { "django-dev-pro": "allow" } }
# }

# 5. Reiniciar opencode
```

---

## 📋 Características

### ✅ Code Generation
- Modelos Django con UUID, soft deletes, timestamps
- Serializers duales (Write + Read)
- ViewSets REST con permisos
- Tests unitarios automáticos
- Documentación en Google format

### ✅ Environment Management
- Detección automática de pyenv
- Carga de variables `.env`
- Configuración por proyecto
- Persistencia en `~/.django-dev-pro/commands.json`

### ✅ Testing
- Ejecución automática de tests
- Análisis de fallos
- Auto-corrección moderada
- Reportes detallados

### ✅ Pattern Learning
Detecta y replica automáticamente:
- Tipo de IDs (UUID vs INT)
- Soft deletes (`is_active`)
- Timestamps (`created_at`, `updated_at`)
- Estructura de serializers
- Convenciones de naming

---

## 📚 Ejemplos de Uso

Este skill se activa automáticamente cuando opencode detecta que trabajas en un proyecto Django. Puedes interactuar con él mediante lenguaje natural.

### Ejemplo 1: Crear un CRUD Completo

```
Crea un CRUD para Product con name, description y price
```

**Genera automáticamente:**
- ✅ Modelo `Product`
- ✅ `ProductWriteSerializer` + `ProductReadSerializer`
- ✅ `ProductViewSet`
- ✅ Tests
- ✅ URLs registradas
- ✅ Documentación

### Ejemplo 2: Ejecutar y Corregir Tests

```
Ejecuta los tests y corrige los errores
```

**Flujo:**
1. Ejecuta `python manage.py test`
2. Detecta fallos
3. Auto-corrige (nivel moderado)
4. Re-ejecuta
5. Reporte final

### Ejemplo 3: Agregar un Campo

```
Agrega un campo priority al modelo Task
```

**Actualiza automáticamente:**
- ✅ Modelo `Task`
- ✅ Serializers
- ✅ Tests
- ✅ Genera migración

### Ejemplo 4: Mostrar Estado del Proyecto

```
Muestra el estado del proyecto
```

---

## 🔧 Configuración

### Archivo: `~/.django-dev-pro/commands.json`

Se crea automáticamente en la primera interacción:

```json
{
  "mi-proyecto": {
    "project_path": "/ruta/a/tu/proyecto",
    "pyenv_env_name": "mi-entorno",
    "env_file": ".env",
    "load_env_before_commands": true,
    "commands": {
      "setup": "pip install -r requirements.txt",
      "test": "python manage.py test",
      "migrate": "python manage.py migrate",
      "runserver": "python manage.py runserver"
    }
  }
}
```

---

## 🎯 Validaciones Pre-Entrega

Toda tarea pasa estas validaciones antes de completarse:

- ✅ Código Python válido (sintaxis correcta)
- ✅ Imports correctos
- ✅ Sigue patrones del proyecto
- ✅ Sin secrets hardcoded
- ✅ Tests 100% pasando
- ✅ Documentación presente
- ✅ Migraciones aplicables

---

## 🔒 Seguridad

- ✅ Nunca guarda secrets o credenciales
- ✅ Valida archivos `.env` antes de cargar
- ✅ Backups automáticos antes de cambios
- ✅ Rollback disponible si falla

---

## 🐛 Troubleshooting

### Error: "No se detectó un proyecto Django"
```bash
# Asegúrate de que manage.py existe en el directorio actual
ls -la manage.py
```

### Error: "Entorno pyenv no encontrado"
```bash
# Verifica que el entorno existe
pyenv versions | grep mi-entorno

# O créalo:
pyenv virtualenv 3.10.0 mi-entorno
```

### Error: "Archivo .env no encontrado"
```bash
# Cópialo desde .env.example
cp .env.example .env

# Llena los valores necesarios
nano .env
```

---

## 📖 Documentación Adicional

- **[SKILL_INSTALL.md](SKILL_INSTALL.md)** - Guía completa de instalación paso a paso
- **SKILL.md** - Documentación interna del skill

---

## 📞 Support

Para reportar issues o sugerencias:
https://github.com/djcrespo/django-skill/issues

---

## 📄 Licencia

MIT
