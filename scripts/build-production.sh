#!/bin/bash
# Build the production library from this dev workspace.
#
# Production is a BUILD OUTPUT, not a clone. It contains only the skills named
# in RELEASE.yaml, and none of the authoring machinery — so a skill cannot
# reach production by being committed, only by being released.
#
# Usage:
#   build-production.sh [dest]        default dest: ~/GitHub/ambient-library
#   build-production.sh --dry-run     show what would change, write nothing
#
# Exit codes: 0 ok · 1 validation failed · 2 bad dest · 3 manifest error
set -euo pipefail
cd "$(dirname "$0")/.."
REPO="$PWD"

DRY=false
DEST="${HOME}/GitHub/ambient-library"
for a in "$@"; do
  case "$a" in
    --dry-run) DRY=true ;;
    -*) echo "unknown flag: $a" >&2; exit 2 ;;
    *) DEST="$a" ;;
  esac
done

# --- guards ---------------------------------------------------------------
[ -f RELEASE.yaml ] || { echo "no RELEASE.yaml at $REPO" >&2; exit 3; }
if [ -f .aai/PRODUCTION ]; then
  echo "refusing: this clone is marked production (.aai/PRODUCTION)." >&2
  echo "Builds run in the dev workspace, which produces production." >&2
  exit 2
fi
if [ -e "$DEST/.git" ]; then
  echo "refusing: $DEST is a git repo." >&2
  echo "Production is a build output now, not a clone. Move it aside first:" >&2
  echo "  mv '$DEST/.git' '$DEST/.git.was-a-clone'" >&2
  exit 2
fi

# --- validate before shipping --------------------------------------------
echo "validating..."
python3 scripts/audit-distribution.py >/dev/null || {
  echo "audit-distribution.py reported drift — fix before releasing." >&2; exit 1; }

# HEAD, not the working tree: an uncommitted edit must never ship.
SRC=$(mktemp -d); trap 'rm -rf "$SRC"' EXIT
git archive HEAD | tar -x -C "$SRC"
SHA=$(git rev-parse --short HEAD)
DIRTY=$([ -n "$(git status --porcelain)" ] && echo " (working tree has uncommitted changes — NOT included)" || echo "")

# --- assemble -------------------------------------------------------------
STAGE=$(mktemp -d); trap 'rm -rf "$SRC" "$STAGE"' EXIT
python3 scripts/release_filter.py "$SRC" "$STAGE" "$SHA" "$REPO" || exit 3

# --- ship -----------------------------------------------------------------
RSYNC=(rsync -a --delete --exclude '.git.was-a-clone' "$STAGE/" "$DEST/")
if $DRY; then
  echo; echo "--- dry run: changes that would land in $DEST ---"
  rsync -a --delete --itemize-changes --dry-run --exclude '.git.was-a-clone' "$STAGE/" "$DEST/" | grep -v '^\.d\.\.t' || echo "(no changes)"
  echo; echo "nothing written."
else
  mkdir -p "$DEST"
  "${RSYNC[@]}"
  echo "built $DEST from $SHA$DIRTY"
  echo "  skills: $(find "$DEST/library" -maxdepth 1 -mindepth 1 -type d | wc -l | tr -d ' ')"
fi
