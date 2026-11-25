---
name: djcrespo-django-skill
description: "ActÃƒÆ’Ã‚Â­vate ÃƒÆ’Ã‚Âºnicamente cuando el usuario estÃƒÆ’Ã‚Â© trabajando en un proyecto Django o Django REST Framework. No actives este skill para proyectos de otros frameworks."
---
# Django Dev Pro

## CuÃƒÆ’Ã‚Â¡ndo activarse

ActÃƒÆ’Ã‚Â­vate ÃƒÆ’Ã‚Âºnicamente cuando el usuario estÃƒÆ’Ã‚Â© trabajando en un proyecto Django o Django REST Framework. No actives este skill para proyectos de otros frameworks.

## DetecciÃƒÆ’Ã‚Â³n de proyectos Django

El skill detecta un proyecto Django cuando encuentra, en el directorio de trabajo o en algÃƒÆ’Ã‚Âºn directorio ascendente:

- `manage.py`
- Carpeta `apps/`
- Carpeta `core/`

Si no se detecta ninguno de estos elementos, pide al usuario que navegue a la raÃƒÆ’Ã‚Â­z del proyecto Django antes de continuar.

## ConfiguraciÃƒÆ’Ã‚Â³n inicial

La primera vez que se usa el helper sobre un proyecto, se crea automÃƒÆ’Ã‚Â¡ticamente una entrada por defecto en `~/.django-dev-pro/commands.json` con comandos Django estÃƒÆ’Ã‚Â¡ndar. El usuario debe editar ese archivo manualmente para:

- Activar la carga de variables de entorno (`load_env_before_commands` + `env_file`).
- Configurar un entorno pyenv (`pyenv_env_name`).
- Personalizar los comandos del proyecto.

El helper **no** realiza una configuraciÃƒÆ’Ã‚Â³n interactiva; solo genera el esqueleto y lo persiste.

## Uso mediante lenguaje natural

Ejemplos de instrucciones que el skill entiende:

- `Crea un CRUD para Product con name, description y price`
- `Agrega un campo priority al modelo Task`
- `Ejecuta los tests del proyecto`
- `Ejecuta los tests y corrige los errores`
- `Muestra el estado del proyecto`
- `Configura este proyecto Django`

## Estructura esperada de `~/.django-dev-pro/commands.json`

```json
{
  "nombre-proyecto": {
    "project_path": "/path/to/project",
    "pyenv_env_name": "mi-entorno",
    "env_file": ".env",
    "load_env_before_commands": true,
    "commands": {
      "test": "python manage.py test",
      "migrate": "python manage.py migrate",
      "makemigrations": "python manage.py makemigrations",
      "runserver": "python manage.py runserver"
    }
  }
}
```

Ver ejemplo completo en `configs/project_commands.example.json`.

## Comportamiento de ejecuciÃƒÆ’Ã‚Â³n de comandos

Antes de ejecutar cualquier comando configurado (`test`, `migrate`, etc.), el helper:

1. Carga el archivo `.env` indicado en `env_file` si `load_env_before_commands` es `true`. Usa `python-dotenv` si estÃƒÆ’Ã‚Â¡ instalado; de lo contrario usa un parser simple de la librerÃƒÆ’Ã‚Â­a estÃƒÆ’Ã‚Â¡ndar. Los valores nunca se escriben en logs.
2. Si `pyenv_env_name` estÃƒÆ’Ã‚Â¡ configurado, antepone la activaciÃƒÆ’Ã‚Â³n de pyenv al comando. Si pyenv no estÃƒÆ’Ã‚Â¡ disponible, muestra una advertencia y continÃƒÆ’Ã‚Âºa sin activar.

## Validaciones pre-entrega

Antes de dar una tarea por terminada, el skill verifica:

- CÃƒÆ’Ã‚Â³digo Python con sintaxis vÃƒÆ’Ã‚Â¡lida
- Imports resolvibles
- Ausencia de secrets hardcodeados
- Tests pasando (o fallos documentados)
- Migraciones generadas cuando corresponde
- DocumentaciÃƒÆ’Ã‚Â³n bÃƒÆ’Ã‚Â¡sica generada

## Nivel de auto-correcciÃƒÆ’Ã‚Â³n

Moderado y conservador: el auto-fix actual solo crea archivos `__init__.py` faltantes en las apps y vuelve a ejecutar los tests. No reescribe mÃƒÆ’Ã‚Â³dulos enteros ni realiza cambios semÃƒÆ’Ã‚Â¡nticos sin confirmaciÃƒÆ’Ã‚Â³n del usuario. Si no puede aplicar una correcciÃƒÆ’Ã‚Â³n obvia, documenta el fallo y pide intervenciÃƒÆ’Ã‚Â³n manual.
