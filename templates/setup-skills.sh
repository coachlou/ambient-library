#!/bin/bash
set -e
PROJECT_DIR="${1:-.}"
MANIFEST="$PROJECT_DIR/skills-manifest.yaml"
SUBMODULE_PATH="$PROJECT_DIR/skills"
TARGET_DIR="$PROJECT_DIR/.agents/skills"
echo "🔄 Setting up magical skill system..."
if [ ! -d "$SUBMODULE_PATH" ]; then
  echo "Error: Submodule not found. Run: git submodule update --init --recursive"
  exit 1
fi
mkdir -p "$TARGET_DIR"
rm -rf "$TARGET_DIR"/*
while IFS= read -r skill || [ -n "$skill" ]; do
  skill=$(echo "$skill" | xargs)
  [[ -z "$skill" || "$skill" == \#* ]] && continue
  SOURCE="$SUBMODULE_PATH/$skill"
  TARGET="$TARGET_DIR/$skill"
  if [ -f "$SOURCE/SKILL.md" ]; then
    mkdir -p "$TARGET"
    cp "$SOURCE/SKILL.md" "$TARGET/SKILL.md"
    echo "  ✓ Installed pointer: $skill"
  else
    echo "  ✗ Warning: Skill $skill not found"
  fi
done < <(grep -E '^\s*-\s+' "$MANIFEST" | sed 's/^[[:space:]]*-[[:space:]]*//' | sed 's/[[:space:]]*#.*//' | sed '/^$/d' || true)
echo "✅ Skill system is ready."
