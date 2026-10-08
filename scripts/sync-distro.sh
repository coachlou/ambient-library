#!/usr/bin/env bash
# sync-distro.sh — pull an app repo's distro/ (and its app snapshot) into the library.
#
#   scripts/sync-distro.sh [--ref <rev>] <cap> <app-repo> [src-dir]
#
# src-dir defaults to "distro"; --ref defaults to HEAD. Pass --ref v1.4.0 to sync a
# release tag. Everything is exported from git at that ref — never read from the
# working tree — so in-flight edits, untracked files and git-ignored build output
# (node_modules/, __pycache__/) can't leak into the library. Same rule as
# build-production.sh: the library builds from committed content only.
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

REF=HEAD; POS=()
while [ $# -gt 0 ]; do
  case "$1" in
    --ref) REF="${2:?--ref needs a rev}"; shift 2 ;;
    --ref=*) REF="${1#*=}"; shift ;;
    *) POS+=("$1"); shift ;;
  esac
done
CAP="${POS[0]:?cap}"; SRC="${POS[1]:?app-repo}"; SUB="${POS[2]:-distro}"

SHA=$(git -C "$SRC" rev-parse --verify --quiet "$REF^{commit}") \
  || { echo "not a git repo, or $REF does not resolve there: $SRC" >&2; exit 1; }
SHORT=$(git -C "$SRC" rev-parse --short "$SHA")
git -C "$SRC" cat-file -e "$SHA:$SUB" 2>/dev/null \
  || { echo "no $SUB/ in $SRC at $REF" >&2; exit 1; }

# APP_FILES is itself read at the ref, so the copy list matches the content being copied.
PATHS=()
if git -C "$SRC" cat-file -e "$SHA:$SUB/APP_FILES" 2>/dev/null; then
  while IFS= read -r p; do
    [ -n "$p" ] || continue
    git -C "$SRC" cat-file -e "$SHA:$p" 2>/dev/null \
      || { echo "APP_FILES names $p, which does not exist in $SRC at $REF" >&2; exit 1; }
    PATHS+=("$p")
  done < <(git -C "$SRC" show "$SHA:$SUB/APP_FILES")
fi

DIRTY=$(git -C "$SRC" status --porcelain -- "$SUB" ${PATHS[@]+"${PATHS[@]}"} | grep -c . || true)
[ "$DIRTY" -eq 0 ] \
  || echo "note: $DIRTY uncommitted path(s) in $SRC were NOT synced; syncing $SHORT" >&2

TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
mkdir "$TMP/ex"
git -C "$SRC" archive "$SHA" -- "$SUB" ${PATHS[@]+"${PATHS[@]}"} | tar -x -C "$TMP/ex"

DEST="library/$CAP"; [ -d "$DEST" ] || DEST="in-progress/$CAP"
mkdir -p "$DEST"
# -I: git archive stamps every file with the commit date, so rsync's size+mtime
# quick-check would skip a changed file when two commits share a timestamp.
rsync -aI --delete --exclude='.DS_Store' --exclude='/app/' "$TMP/ex/$SUB/" "$DEST/"
if [ "${#PATHS[@]}" -gt 0 ]; then
  mkdir -p "$DEST/app"
  printf '%s\n' "${PATHS[@]}" > "$TMP/list"
  rsync -aI --delete -r --files-from="$TMP/list" "$TMP/ex/" "$DEST/app/"
  VER=$(git -C "$SRC" show "$SHA:package.json" 2>/dev/null | python3 -c 'import json,sys;print(json.load(sys.stdin)["version"])' 2>/dev/null \
    || git -C "$SRC" show "$SHA:$SUB/.claude-plugin/plugin.json" 2>/dev/null | python3 -c 'import json,sys;print(json.load(sys.stdin)["version"])' 2>/dev/null \
    || echo unknown)
  printf '%s %s (%s) synced %s\n' "$CAP" "$VER" "$SHORT" "$(date -u +%F)" > "$DEST/app/VERSION"
  cat "$DEST/app/VERSION"
fi
echo "synced $SRC/$SUB@$SHORT -> $DEST"
