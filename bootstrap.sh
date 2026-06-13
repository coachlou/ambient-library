#!/bin/bash
# bootstrap.sh — One-command setup for a new project using ambient-library.
#
# Usage (run from your project root):
#   curl -fsSL https://raw.githubusercontent.com/coachlou/ambient-library/main/bootstrap.sh | bash
#   OR after cloning: bash skills/bootstrap.sh
#
# What it does:
#   1. Adds ambient-library as a git submodule (if not already present)
#   2. Copies all template files into your project root
#   3. Makes scripts executable
#   4. Runs setup-skills.sh to install skill pointers
#   5. Prints next steps

set -e

REPO="git@github-coachlou:coachlou/ambient-library.git"
SUBMODULE_DIR="skills"
TEMPLATE_DIR="$SUBMODULE_DIR/templates"

echo ""
echo "🚀 Bootstrapping Ambient Library skill system..."
echo ""

# Step 1: Add submodule if not already present
if [ ! -f ".gitmodules" ] || ! grep -q "ambient-library" .gitmodules 2>/dev/null; then
  if [ ! -d ".git" ]; then
    echo "  ℹ️  No git repo found. Initializing..."
    git init
  fi
  echo "  📦 Adding ambient-library submodule..."
  git submodule add "$REPO" "$SUBMODULE_DIR"
else
  echo "  ✓ Submodule already present — updating to latest..."
  git submodule update --remote "$SUBMODULE_DIR"
fi

# Step 2: Copy templates (skip if file already exists)
echo ""
echo "  📋 Copying template files..."

copy_template() {
  local src="$TEMPLATE_DIR/$1"
  local dest="$1"
  local destdir
  destdir=$(dirname "$dest")
  if [ -f "$dest" ]; then
    echo "     Skipped (already exists): $dest"
  else
    mkdir -p "$destdir"
    cp "$src" "$dest"
    echo "     ✓ $dest"
  fi
}

copy_template "setup-skills.sh"
copy_template "skills-manifest.yaml"
copy_template "CLAUDE.md"
copy_template ".gitignore"
copy_template ".claude/settings.json"
copy_template ".claude/hooks/session-start.sh"

# Step 3: Ensure scripts are executable
chmod +x setup-skills.sh
chmod +x .claude/hooks/session-start.sh

# Step 4: Install skill pointers
echo ""
./setup-skills.sh

# Step 5: Next steps
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Ambient Library is ready."
echo ""
echo "Next steps:"
echo "  1. Edit skills-manifest.yaml to choose which skills to activate"
echo "  2. Edit CLAUDE.md to add project-specific rules"
echo "  3. Commit everything:  git add . && git commit -m 'Add ambient-library skill system'"
echo "  4. Start a Claude session — skills are active automatically"
echo ""
echo "Docs: skills/docs/GETTING_STARTED.md"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
