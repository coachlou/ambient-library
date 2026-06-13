#!/bin/bash
# install-global.sh
# Installs the ambient skill globally so it's available in every Claude Code session.
# Run once per machine. Safe to re-run — updates to latest version.
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/coachlou/ambient-library/main/install-global.sh | bash

set -e

REPO="https://github.com/coachlou/ambient-library.git"
TARGET="$HOME/.claude/skills/ambient"
TMP_DIR=$(mktemp -d)

echo ""
echo "🌐 Installing ambient skill globally..."
echo ""

# Clone just the ambient/ folder from the repo
git clone --depth 1 --filter=blob:none --sparse "$REPO" "$TMP_DIR" 2>/dev/null
cd "$TMP_DIR"
git sparse-checkout set ambient 2>/dev/null

# Install to ~/.claude/skills/ambient/
mkdir -p "$TARGET"
cp -r "$TMP_DIR/ambient/." "$TARGET/"

# Clean up
rm -rf "$TMP_DIR"

echo "  ✓ Installed to: $TARGET"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Ambient skill is ready."
echo ""
echo "Open any project in Claude Code and say:"
echo "  \"Set up ambient-library in this project\""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
