#!/bin/bash

###############################################################################
#                                                                             #
#  Django Dev Pro - GitHub Repository Setup Script                          #
#  Crea un repositorio en GitHub desde la línea de comando                  #
#                                                                             #
###############################################################################

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  Django Dev Pro - GitHub Repository Setup                 ║"
echo "╚════════════════════════════════════════════════════════════╝"

# Verificar que estamos en el directorio correcto
if [ ! -f "skill.yml" ]; then
    echo "❌ Error: Este script debe ejecutarse desde la raíz de django-skill"
    exit 1
fi

echo ""
echo "Este script te ayudará a crear un repositorio en GitHub"
echo ""

# Solicitar información
read -p "¿Nombre de usuario de GitHub? " GITHUB_USER
read -p "¿Nombre del repositorio? (django-skill por defecto) " REPO_NAME
REPO_NAME=${REPO_NAME:-django-skill}

echo ""
echo "Configurando repositorio..."

# Inicializar git si no existe
if [ ! -d ".git" ]; then
    git init
    echo "✅ Repositorio git inicializado"
fi

# Agregar remote
git remote remove origin 2>/dev/null || true
git remote add origin "https://github.com/$GITHUB_USER/$REPO_NAME.git"
echo "✅ Remote agregado: https://github.com/$GITHUB_USER/$REPO_NAME.git"

# Crear rama main si es necesario
if ! git rev-parse --verify main > /dev/null 2>&1; then
    git checkout -b main
    echo "✅ Rama 'main' creada"
fi

# Agregar todos los archivos
git add .
echo "✅ Archivos agregados"

# Hacer commit inicial
if [ -z "$(git status --porcelain)" ]; then
    echo "ℹ️  No hay cambios para hacer commit"
else
    git commit -m "Initial commit: Django Dev Pro Skill" || true
    echo "✅ Commit inicial realizado"
fi

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  ¡Casi listo!                                             ║"
echo "╠════════════════════════════════════════════════════════════╣"
echo "║ Pasos finales:                                             ║"
echo "║                                                            ║"
echo "║ 1. Crea el repositorio en GitHub:                         ║"
echo "║    https://github.com/new                                 ║"
echo "║                                                            ║"
echo "║ 2. Nombre: $REPO_NAME"
echo "║    Usuario: $GITHUB_USER                                  ║"
echo "║                                                            ║"
echo "║ 3. NO inicialices con README, .gitignore, etc.            ║"
echo "║                                                            ║"
echo "║ 4. Luego, pushea con:                                      ║"
echo "║    git push -u origin main                                ║"
echo "║                                                            ║"
echo "║ 5. Opcionalmente, crea una rama develop:                  ║"
echo "║    git checkout -b develop                                ║"
echo "║    git push -u origin develop                             ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"

echo ""
echo "✅ Configuración completada"
