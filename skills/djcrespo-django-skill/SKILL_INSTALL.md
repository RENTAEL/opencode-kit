# django-dev-pro - Guía de Instalación para OpenCode

## Información General

| Campo | Valor |
|-------|-------|
| **Nombre del Skill** | django-dev-pro |
| **Descripción** | Automatiza desarrollo Django REST Framework. Genera Modelos, Serializers duales, ViewSets, Tests y Documentación siguiendo patrones del proyecto. |
| **Versión** | 1.0.0 |
| **Autor** | djcrespo |
| **Licencia** | MIT |

---

## Requisitos Previos

Antes de instalar el skill, asegúrate de tener:

1. **opencode** instalado y funcionando
   - Verifica con: `opencode --version`

2. **Python 3.10+** instalado
   - Verifica con: `python3 --version`

3. **Django y Django REST Framework** (para usar el skill)
   - `pip install django djangorestframework`

---

## Instalación Paso a Paso

### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/djcrespo/django-skill.git
cd django-skill
```

### Paso 2: Instalar la skill

Ejecuta el script de instalación incluido:

```bash
./install.sh
```

O copia manualmente el contenido del repositorio a la carpeta de skills de opencode:

```bash
mkdir -p ~/.config/opencode/skills
cp -r /ruta/al/clon/django-skill ~/.config/opencode/skills/django-dev-pro
```

### Paso 3: Verificar estructura

Confirma que la estructura sea correcta:

```bash
ls -la ~/.config/opencode/skills/django-dev-pro/
```

Deberías ver al menos:

```
django-dev-pro/
├── SKILL.md
├── configs/
├── templates/
└── ...
```

### Paso 4: Habilitar el skill en opencode

Edita o crea el archivo de configuración de opencode:

```bash
nano ~/.config/opencode/opencode.json
```

Agrega el permiso para el skill:

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

### Paso 5: Reiniciar opencode

Cierra y vuelve a abrir tu terminal, o reinicia el servicio de opencode.

---

## Configuración Inicial

### Primera vez que usas el skill

1. **Abre opencode** en tu terminal

2. **Activa el skill** escribiendo:
   ```
   Usa el skill django-dev-pro
   ```

3. **El skill detectará automáticamente** tu proyecto Django:
   - Buscará `manage.py` en el directorio actual
   - Buscará directorios `apps/` o `core/`

4. **Configura el proyecto** cuando se te solicite:
   - Nombre del entorno pyenv (opcional)
   - Archivo `.env` a usar (ej: `.env.local`)
   - Comandos principales del proyecto

### Guardado de configuración

La configuración se guarda en `~/.django-dev-pro/commands.json`:

```json
{
  "mi-proyecto": {
    "project_path": "/ruta/al/proyecto",
    "pyenv_env_name": "mi-entorno",
    "env_file": ".env.local",
    "load_env_before_commands": true,
    "commands": {
      "test": "python manage.py test",
      "migrate": "python manage.py migrate",
      "runserver": "python manage.py runserver"
    }
  }
}
```

Ver ejemplo completo en [`configs/project_commands.example.json`](configs/project_commands.example.json) y la definición del skill en [`SKILL.md`](SKILL.md).

---

## Uso Básico del Skill

Una vez instalado y configurado, puedes usar estos comandos en lenguaje natural:

### Crear un nuevo modelo

```
Crea un modelo Product con name, description, price
```

### Agregar campos a un modelo existente

```
Agrega campo priority a Task
```

### Ejecutar tests

```
Ejecuta los tests del proyecto
```

### Ver estado del proyecto

```
Muestra el estado del proyecto
```

### Configurar proyecto Django

```
Configura este proyecto Django
```

---

## Configuración por Proyecto

### Estructura del archivo commands.json

Cada proyecto puede tener su propia configuración:

```json
{
  "nombre-proyecto": {
    "project_path": "/ruta/completa/al/proyecto",
    "pyenv_env_name": "nombre-del-entorno-virtual",
    "env_file": ".env.local",
    "load_env_before_commands": true,
    "commands": {
      "setup": "pip install -r requirements.txt",
      "test": "python manage.py test",
      "migrate": "python manage.py migrate",
      "makemigrations": "python manage.py makemigrations",
      "runserver": "python manage.py runserver",
      "createsuperuser": "python manage.py createsuperuser"
    }
  }
}
```

### Comandos configurables

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| setup | Instalar dependencias | `pip install -r requirements.txt` |
| test | Ejecutar tests | `python manage.py test` |
| migrate | Aplicar migraciones | `python manage.py migrate` |
| makemigrations | Generar migraciones | `python manage.py makemigrations` |
| runserver | Iniciar servidor | `python manage.py runserver` |
| createsuperuser | Crear superusuario | `python manage.py createsuperuser` |

---

## Solución de Problemas

### Problema: "Skill no encontrado"

**Síntoma**: opencode no reconoce el skill

**Solución**:
1. Verifica que el directorio exista: `ls ~/.config/opencode/skills/django-dev-pro/`
2. Confirma que contiene `SKILL.md`
3. Revisa que `~/.config/opencode/opencode.json` tenga el permiso habilitado

### Problema: "Proyecto Django no detectado"

**Síntoma**: El skill no encuentra tu proyecto

**Solución**:
1. Asegúrate de estar en el directorio raíz del proyecto
2. Verifica que existe `manage.py`: `ls -la manage.py`
3. El skill busca en: `manage.py`, `apps/`, `core/`

### Problema: "Error al cargar variables de entorno"

**Síntoma**: No se cargan las variables del .env

**Solución**:
1. Verifica que el archivo `.env` exista en la raíz del proyecto
2. Confirma que `load_env_before_commands` esté en `true`
3. No incluyas secrets sensibles en el archivo de configuración

### Problema: "Tests fallan"

**Síntoma**: Los tests no pasan

**Solución**:
1. Ejecuta los tests manualmente: `python manage.py test`
2. Verifica que tienes todas las dependencias instaladas
3. Asegúrate de tener migraciones aplicadas: `python manage.py migrate`

### Problema: "Pyenv no encontrado"

**Síntoma**: No se activa el entorno virtual

**Solución**:
1. Verifica que pyenv esté instalado: `pyenv --version`
2. Lista tus entornos: `pyenv versions`
3. Configura el nombre exacto del entorno en `commands.json`

---

## Actualización del Skill

Para actualizar a una nueva versión:

```bash
# 1. Respaldar configuración actual
cp ~/.django-dev-pro/commands.json ~/.django-dev-pro/commands.json.backup

# 2. Volver a clonar/copiar los archivos del skill
cp -r /ruta/al/nuevo/django-skill ~/.config/opencode/skills/django-dev-pro

# 3. Reiniciar opencode
```

---

## Recursos Adicionales

- **Documentación del skill**: Disponible en `~/.config/opencode/skills/django-dev-pro/SKILL.md`
- **Repositorio del skill**: https://github.com/djcrespo/django-skill
- **Reportar issues**: https://github.com/djcrespo/django-skill/issues

---

## Notas de Seguridad

- **Nunca** guardes credenciales o secrets en `commands.json`
- **Siempre** usa archivos `.env` para variables sensibles
- El skill **nunca** hardcodea valores sensibles
- **Valida** tus archivos `.env` antes de cargarlos

---

## Changelog

### v1.0.0
- Lanzamiento inicial
- Detección automática de proyectos Django
- Generación de modelos, serializers y ViewSets
- Testing automático con auto-corrección
- Configuración persistente por proyecto
