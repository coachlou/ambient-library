#!/usr/bin/env bash
# sync-distro.sh — pull an app repo's distro/ (and its app snapshot) into the library.
#
#   scripts/sync-distro.sh <cap> <app-repo> [src-dir]     src-dir defaults to "distro"
#
# The app repo owns packaging: <repo>/distro/ holds SKILL.md, .claude-plugin/plugin.json,
# instructions.md, templates/aai/, and optionally install.d/post.sh, run.sh, and APP_FILES
# (one path per line, copied from the repo root into app/). The library folder is a build
# output of that — never hand-edit library/<cap>/ for a distro.
#
# A repo that already uses distro/ for something else names its packaging folder as the
# third argument (software-dev-factory uses ambient-distro/, because distro/ there holds
# the release bundles its own build script produces).
#
# Destination: library/<cap>/ if it exists, else in-progress/<cap>/ (then promote.sh).
set -euo pipefail
cd "$(dirname "$0")/.."
CAP="${1:?cap}"; SRC="${2:?app-repo}"; SUB="${3:-distro}"
[ -d "$SRC/$SUB" ] || { echo "no $SUB/ in $SRC" >&2; exit 1; }
DEST="library/$CAP"; [ -d "$DEST" ] || DEST="in-progress/$CAP"
mkdir -p "$DEST"
rsync -a --delete --exclude='.DS_Store' --exclude='/app/' "$SRC/$SUB/" "$DEST/"
if [ -f "$SRC/$SUB/APP_FILES" ]; then
  mkdir -p "$DEST/app"
  rsync -a --delete -r --files-from="$SRC/$SUB/APP_FILES" "$SRC/" "$DEST/app/"
  VER=$(python3 -c "import json;print(json.load(open('$SRC/package.json'))['version'])" 2>/dev/null \
    || python3 -c "import json;print(json.load(open('$SRC/$SUB/.claude-plugin/plugin.json'))['version'])" 2>/dev/null \
    || echo unknown)
  SHA=$(git -C "$SRC" rev-parse --short HEAD 2>/dev/null || echo unknown)
  [ -z "$(git -C "$SRC" status --porcelain 2>/dev/null)" ] || echo "warn: $SRC has uncommitted changes — sha $SHA is not what app/ contains" >&2
  printf '%s %s (%s) synced %s\n' "$CAP" "$VER" "$SHA" "$(date -u +%F)" > "$DEST/app/VERSION"
  cat "$DEST/app/VERSION"
fi
echo "synced $SRC/$SUB -> $DEST"
