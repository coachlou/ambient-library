#!/usr/bin/env bash
# sync-app.sh — refresh the vendored SoloFactory snapshot in app/ from its source repo.
#
#   bash sync-app.sh [source-repo]     default: $SOLOFACTORY_SRC or the coachlou/soloFactory clone
#
# app/ is a pristine copy of the runtime (src, public, skills, package.json, README).
# Tests, specs, and local run state stay in the source repo. Writes app/VERSION.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="${1:-${SOLOFACTORY_SRC:-/Volumes/Extreme Pro/users/loudalo/GitHub/soloFactory}}"
[ -f "$SRC/package.json" ] || { echo "not a soloFactory checkout: $SRC" >&2; exit 1; }
rsync -a --delete \
  --include='/src/***' --include='/public/***' --include='/skills/***' \
  --include='/package.json' --include='/README.md' --exclude='*' \
  "$SRC/" "$HERE/app/"
VER=$(python3 -c "import json;print(json.load(open('$SRC/package.json'))['version'])")
SHA=$(git -C "$SRC" rev-parse --short HEAD 2>/dev/null || echo unknown)
printf 'solofactory %s (%s) synced %s\n' "$VER" "$SHA" "$(date -u +%F)" > "$HERE/app/VERSION"
cat "$HERE/app/VERSION"
