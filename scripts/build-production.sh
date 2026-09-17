#!/bin/bash
# Build the production library from this dev workspace.
#
# Production is a BUILD OUTPUT, not a clone. It contains only the skills named
# in RELEASE.yaml, and none of the authoring machinery — so a skill cannot
# reach production by being committed, only by being released.
#
# Usage:
#   build-production.sh [dest]        default dest: ./distro (gitignored staging)
#   build-production.sh --dry-run     show what would change, write nothing
#
# The only git repo accepted as dest is a clone of coachlou/aai-library, the
# distribution repo — scripts/publish-distro.sh uses that path.
#
# Exit codes: 0 ok · 1 validation failed · 2 bad dest · 3 manifest error
set -euo pipefail
cd "$(dirname "$0")/.."
REPO="$PWD"

DRY=false
DEST="$REPO/distro"
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
  case "$(git -C "$DEST" remote get-url origin 2>/dev/null || true)" in
    *coachlou/aai-library*) ;;   # the distribution repo: build into it, keep its .git and LICENSE
    *) echo "refusing: $DEST is a git repo that is not the coachlou/aai-library clone." >&2
       echo "Production is a build output, not a clone. Use scripts/publish-distro.sh to release." >&2
       exit 2 ;;
  esac
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
EXCL=(--exclude '.git' --exclude '/LICENSE')   # the destination repo's own root LICENSE only — nested ones ship
# --checksum: a same-size edit (2.1.0 -> 2.2.0) whose mtime happens to match the
# clone's is otherwise skipped, and the release ships the old file.
RSYNC=(rsync -a --checksum --delete "${EXCL[@]}" "$STAGE/" "$DEST/")
if $DRY; then
  echo; echo "--- dry run: changes that would land in $DEST ---"
  rsync -a --checksum --delete --itemize-changes --dry-run "${EXCL[@]}" "$STAGE/" "$DEST/" | grep -v '^\.d\.\.t' || echo "(no changes)"
  echo; echo "nothing written."
else
  mkdir -p "$DEST"
  "${RSYNC[@]}"
  echo "built $DEST from $SHA$DIRTY"
  echo "  skills: $(find "$DEST/library" -maxdepth 1 -mindepth 1 -type d | wc -l | tr -d ' ')"
fi
