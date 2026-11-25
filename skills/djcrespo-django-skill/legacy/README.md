# Legacy / Deprecated Files

Esta carpeta contiene archivos de versiones anteriores del proyecto que pretendían crear una herramienta CLI independiente (`django-dev-pro`) en lugar de una skill válida de OpenCode.

## Contenido

- `setup.py`: Configuración de setuptools para instalar un paquete pip y un comando global `django-dev-pro`.
- `django-dev-pro.sh`: Script bash que intentaba ejecutar `lib/main.py` (inexistente) desde `~/.opencode/skills/django-dev-pro`.

## Estado

⚠️ **DEPRECADO**: No se requieren para que OpenCode cargue la skill. OpenCode solo necesita `SKILL.md` en la carpeta del skill (`~/.config/opencode/skills/django-dev-pro/SKILL.md`).

Se mantienen aquí únicamente como referencia histórica. No forman parte de la instalación oficial de la skill.
