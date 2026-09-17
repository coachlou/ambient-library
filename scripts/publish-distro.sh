#!/bin/bash
# Publish the production build to the distribution repo (coachlou/aai-library).
#
# Runs build-production.sh into a clone of aai-library, commits the result, and
# tags it with the plugin version. It never pushes — the push command is
# printed so the release is a deliberate step.
#
# Usage:
#   publish-distro.sh [clone]     default clone: ../aai-library (sibling of this repo)
#                                 or $AAI_DISTRO_CLONE if set
#   publish-distro.sh --dry-run   build only, show what would change
#
# Exit codes: 0 ok · 1 build failed · 2 bad clone
set -euo pipefail
cd "$(dirname "$0")/.."

DRY=false; DIST="${AAI_DISTRO_CLONE:-$(dirname "$PWD")/aai-library}"
for a in "$@"; do
  case "$a" in
    --dry-run) DRY=true ;;
    -*) echo "unknown flag: $a" >&2; exit 2 ;;
    *) DIST="$a" ;;
  esac
done

# --- guards: only ever write into the real distribution clone ---------------
ORIGIN=$(git -C "$DIST" remote get-url origin 2>/dev/null || true)
case "$ORIGIN" in
  *coachlou/aai-library*) ;;
  *) echo "refusing: $DIST origin is '$ORIGIN', not coachlou/aai-library" >&2; exit 2 ;;
esac
if [ -n "$(git -C "$DIST" status --porcelain)" ]; then
  echo "refusing: $DIST has uncommitted changes" >&2; exit 2
fi
git -C "$DIST" pull -q --ff-only

# --- build --------------------------------------------------------------------
SHA=$(git rev-parse --short HEAD)
VER=$(python3 -c 'import json;print(json.load(open(".claude-plugin/plugin.json"))["version"])')
if $DRY; then
  scripts/build-production.sh --dry-run "$DIST"; exit
fi
scripts/build-production.sh "$DIST" || exit 1

# --- commit + tag, no push ----------------------------------------------------
cd "$DIST"
git add -A   # the whole tree is the build output; nothing here is hand-authored
if git diff --cached --quiet; then
  echo "nothing changed in $DIST"; exit 0
fi
git commit -q -m "Release from ambient-library@$SHA" -m "Built by scripts/publish-distro.sh; plugin version $VER."
if git rev-parse -q --verify "refs/tags/v$VER" >/dev/null; then
  echo "tag v$VER already exists — bump .claude-plugin/plugin.json version before the next release" >&2
else
  git tag "v$VER"
fi
echo "committed $(git rev-parse --short HEAD) in $DIST"
echo "to publish:  git -C '$DIST' push origin main --tags"
