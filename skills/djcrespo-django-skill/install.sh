#!/bin/bash

###############################################################################
#                                                                             #
#  Django Dev Pro Skill - Installation Script for OpenCode                    #
#  Installs the skill into ~/.config/opencode/skills/django-dev-pro           #
#                                                                             #
###############################################################################

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
INSTALL_DIR="$HOME/.config/opencode/skills"
SKILL_DIR="$INSTALL_DIR/django-dev-pro"
CONFIG_DIR="$HOME/.django-dev-pro"
OPENCODE_CONFIG="$HOME/.config/opencode/opencode.json"

# Determine the source directory (directory where this script is located)
SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║     Django Dev Pro Skill - Installation Script             ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Create directories
echo -e "${YELLOW}[1/4]${NC} Creating target directories..."
mkdir -p "$INSTALL_DIR"
mkdir -p "$CONFIG_DIR"
echo -e "${GREEN}✅ Directories created${NC}"

# Install / update skill
echo -e "${YELLOW}[2/4]${NC} Installing skill into $SKILL_DIR..."

if [ -d "$SKILL_DIR" ]; then
    echo -e "${YELLOW}   ⚠️  Skill already exists at $SKILL_DIR${NC}"
    read -p "   Do you want to update? (Y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$SKILL_DIR"
        cp -R "$SOURCE_DIR" "$SKILL_DIR"
        echo -e "${GREEN}✅ Skill updated${NC}"
    else
        echo -e "${YELLOW}ℹ️  Installation cancelled by user${NC}"
        exit 0
    fi
else
    cp -R "$SOURCE_DIR" "$SKILL_DIR"
    echo -e "${GREEN}✅ Skill installed${NC}"
fi

# Remove artifacts that should not be shipped inside the skill directory
rm -rf "$SKILL_DIR/.git"
find "$SKILL_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# Make scripts and entry points executable
echo -e "${YELLOW}[3/4]${NC} Setting permissions..."
find "$SKILL_DIR" -type f \( -name "*.sh" -o -name "*.py" \) -exec chmod +x {} +
echo -e "${GREEN}✅ Permissions configured${NC}"

# Ensure OpenCode permission is set
echo -e "${YELLOW}[4/4]${NC} Enabling skill in OpenCode config..."
mkdir -p "$(dirname "$OPENCODE_CONFIG")"
python3 - "$OPENCODE_CONFIG" <<'PY'
import json
import sys
from pathlib import Path

config_path = Path(sys.argv[1])
config = {}
if config_path.exists():
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        config = {}

config.setdefault("permission", {})
config["permission"].setdefault("skill", {})
config["permission"]["skill"]["django-dev-pro"] = "allow"

config_path.parent.mkdir(parents=True, exist_ok=True)
config_path.write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("✅ Permission added to OpenCode config")
PY

# Verification
echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ INSTALLATION COMPLETED SUCCESSFULLY${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"

echo ""
echo -e "${YELLOW}📁 Installation location:${NC}"
echo "   $SKILL_DIR"

echo ""
echo -e "${YELLOW}📚 Documentation:${NC}"
echo "   SKILL.md:      $SKILL_DIR/SKILL.md"
echo "   README:        $SKILL_DIR/README.md"
echo "   Installation:  $SKILL_DIR/SKILL_INSTALL.md"

echo ""
echo -e "${YELLOW}⚙️  Per-project configuration:${NC}"
echo "   ~/.django-dev-pro/commands.json"

echo ""
echo -e "${YELLOW}🎯 Next steps:${NC}"
echo "   1. Restart OpenCode."
echo "   2. Navigate to a Django project and run:"
echo "      Usa el skill django-dev-pro"
echo ""

echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Ready to use! Enjoy Django Dev Pro Skill 🎉${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
