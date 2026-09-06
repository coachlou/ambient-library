#!/usr/bin/env bash
# install.sh — make a folder a SoloFactory workspace.
#
#   bash install.sh [target-dir]      default: current directory
#   bash install.sh --check [target]  report what would happen, write nothing
#   bash install.sh --help
#
# Writes (owned, never overwritten if present):   <target>/.aai/{identity,instructions,context}.md
# Writes (vendored, always re-synced):            <target>/.ailib/solofactory/ + .ailib/manifest.yaml
# Creates:                                        <target>/projects/   (one subfolder per run id)
# Appends a discovery anchor to <target>/CLAUDE.md and AGENTS.md.
# Re-running is safe: it refreshes .ailib/ and leaves .aai/ and projects/ alone.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHECK=0; TARGET=""
while [ $# -gt 0 ]; do
  case "$1" in
    --check) CHECK=1; shift ;;
    --help|-h) sed -n '2,12p' "$0"; exit 0 ;;
    --*) echo "unknown flag: $1" >&2; exit 2 ;;
    *) TARGET="$1"; shift ;;
  esac
done
TARGET="${TARGET:-$PWD}"
mkdir -p "$TARGET"; TARGET="$(cd "$TARGET" && pwd)"
case "$TARGET" in
  "$HERE"|"$HERE"/*) echo "refusing: target is inside the capability itself" >&2; exit 2 ;;
esac
[ -f "$HERE/.claude-plugin/plugin.json" ] || { echo "refusing: $HERE is not the solofactory capability" >&2; exit 2; }
NAME="$(basename "$TARGET")"
VER=$(python3 -c "import json;print(json.load(open('$HERE/.claude-plugin/plugin.json'))['version'])")
APPVER=$(head -1 "$HERE/app/VERSION" 2>/dev/null || echo "unknown")
DATE=$(date -u +%F)

say() { printf '%s\n' "$*"; }
plan() { say "  $1  $2"; }

# ── plan ─────────────────────────────────────────────────────────────────────
say "target: $TARGET"
if [ -f "$TARGET/.aai/instructions.md" ]; then plan keep ".aai/ (exists — owned, untouched)"; else plan write ".aai/{identity,instructions,context}.md"; fi
plan sync ".ailib/solofactory/ ($APPVER)"
plan write ".ailib/manifest.yaml"
[ -d "$TARGET/projects" ] && plan keep "projects/" || plan create "projects/"
for f in CLAUDE.md AGENTS.md; do
  if [ -f "$TARGET/$f" ] && grep -q 'ambient folder' "$TARGET/$f"; then plan keep "$f (anchor present)"; else plan anchor "$f"; fi
done
NODE_OK=1; command -v node >/dev/null && [ "$(node -p 'process.versions.node.split(".")[0]')" -ge 22 ] || NODE_OK=0
[ $NODE_OK = 1 ] || say "  warn  node 22+ not found on PATH — SoloFactory will not start until it is installed"
[ $CHECK = 1 ] && { say "nothing written."; exit 0; }

# ── .aai (owned) ─────────────────────────────────────────────────────────────
if [ ! -f "$TARGET/.aai/instructions.md" ]; then
  mkdir -p "$TARGET/.aai"
  for t in identity instructions context; do
    sed "s/{{NAME}}/$NAME/g" "$HERE/templates/aai/$t.md" > "$TARGET/.aai/$t.md"
  done
fi

# ── .ailib (vendored) ────────────────────────────────────────────────────────
mkdir -p "$TARGET/.ailib/solofactory"
rsync -a --delete --exclude='.DS_Store' "$HERE/" "$TARGET/.ailib/solofactory/"
cat > "$TARGET/.ailib/manifest.yaml" <<YAML
# Vendored canonical capabilities — pristine, re-synced by install.sh; never edit here.
solofactory:
  source: ambient-library/library/solofactory
  version: "$VER"
  app: "$APPVER"
  installed: $DATE
YAML

# ── projects ─────────────────────────────────────────────────────────────────
mkdir -p "$TARGET/projects"

# ── anchors ──────────────────────────────────────────────────────────────────
for f in CLAUDE.md AGENTS.md; do
  if ! { [ -f "$TARGET/$f" ] && grep -q 'ambient folder' "$TARGET/$f"; }; then
    [ -f "$TARGET/$f" ] && printf '\n' >> "$TARGET/$f"
    cat >> "$TARGET/$f" <<MD
## Ambient folder

This folder is an ambient folder: SoloFactory is its agentic function.
**Read \`.aai/instructions.md\` and follow it before acting.** "Ambient folder"
means a folder with an \`.aai/\` behavior layer, not a Node project — do not
run \`npm init\` or scaffold anything.
MD
  fi
done

say "installed solofactory $VER into $TARGET"
say "start:  bash '$TARGET/.ailib/solofactory/run.sh'   → http://127.0.0.1:4173"
