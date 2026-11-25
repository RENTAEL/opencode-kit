---
name: skill_init_workspace
description: "**ADVERTENCIA DE INVOCACIÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œN:** Esta skill solo debe ser invocada desde `NEW_PROJECT.md` como parte del flujo de instanciaciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n de un proyecto nuevo. Nunca debe invocarse de forma directa o aislada. Si estÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡s ejecutando es..."
---
# SKILL: CREACIÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œN DE ARQUITECTURA Y GIT (FASE 0 - PASO 1)

**ADVERTENCIA DE INVOCACIÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œN:** Esta skill solo debe ser invocada desde `NEW_PROJECT.md` como parte del flujo de instanciaciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n de un proyecto nuevo. Nunca debe invocarse de forma directa o aislada. Si estÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡s ejecutando esta skill sin haber pasado por `NEW_PROJECT.md` primero, detente y consulta al Supervisor antes de continuar.

## DESCRIPCIÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œN
Esta habilidad genera la estructura base de directorios e inicializa Git dentro del directorio del proyecto ya creado por NEW_PROJECT.md.

## INSTRUCCIONES PARA EL AGENTE
1. Detente y lanza esta pregunta exacta al Supervisor: **"ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¿Deseas inicializar la arquitectura de carpetas y el repositorio Git para este proyecto? (S/N)"**.
2. Si la respuesta es "S", ejecuta estrictamente los siguientes comandos:

```bash
mkdir -p .github/workflows data/raw data/processed data/production notebooks src
touch .env Makefile
# Guard: solo inicializar Git si no existe ya un repositorio
if [ -d ".git" ]; then
  echo ".git/ ya existe. Saltando git init."
else
  git init
  git branch -M main
fi

# Configurar VS Code para usar el .venv del proyecto como kernel por defecto
mkdir -p .vscode
cat > .vscode/settings.json << 'EOF'
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "jupyter.kernelPickerType": "mru"
}
EOF
```

3. Al finalizar, confirma al usuario que las carpetas y Git han sido inicializados correctamente y continÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âºa con skill_setup_environment.

**Nota:** La carpeta `dbt_project/` no se crea en este paso ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â la genera automÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¡ticamente el comando `dbt init` en el paso siguiente (`skill_config_dbt`). No es necesario crearla manualmente.