#!/bin/bash

# Django Dev Pro Skill - Global Entry Point
# Script to make the skill globally accessible

SKILL_DIR="$HOME/.config/opencode/skills/django-dev-pro"
PYTHON_BIN=$(which python3)

# Ejecutar la skill
cd "$SKILL_DIR" && $PYTHON_BIN lib/main.py "$@"
