#!/usr/bin/env bash
# publish.sh — promote the owner's ~/.aai/rules/coding.md into this capability.
#
#   bash publish.sh [--check] [--source FILE]
#
# Authority flows one way: ~/.aai/rules/coding.md (edited by the owner) →
# rules/coding.md here (the published snapshot, never hand-edited) → installs
# and vendored .ailib/ copies. Run it in the library dev workspace, then bump
# .claude-plugin/plugin.json and commit; releasing stays a separate step.
# Refuses when the source has uncommitted changes in its git repo, so every
# snapshot traces to a commit in ~/.aai. --check shows the diff, writes nothing.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="$HERE/../rules/coding.md"
SRC="$HOME/.aai/rules/coding.md"
CHECK=0
while [ $# -gt 0 ]; do
  case "$1" in
    --check) CHECK=1 ;;
    --source) SRC="$2"; shift ;;
    -h|--help) sed -n '2,12p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
  shift
done

ROOT="$(cd "$HERE/../../.." && pwd)"
[ -f "$ROOT/.aai/PRODUCTION" ] && {
  echo "this is a production build; publish from the dev workspace named in .aai/PRODUCTION" >&2
  exit 2
}
[ -f "$SRC" ] || { echo "no source rules at $SRC (run install.sh first)" >&2; exit 2; }

SRC_DIR="$(dirname "$SRC")"
COMMIT="untracked"
if git -C "$SRC_DIR" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  if [ -n "$(git -C "$SRC_DIR" status --porcelain -- "$(basename "$SRC")")" ]; then
    echo "$SRC has uncommitted changes; commit them in $(git -C "$SRC_DIR" rev-parse --show-toplevel) first" >&2
    exit 1
  fi
  COMMIT="$(git -C "$SRC_DIR" rev-parse --short HEAD)"
fi

if cmp -s "$SRC" "$DEST"; then
  echo "already published (source commit $COMMIT)"
  exit 0
fi
diff -u "$DEST" "$SRC" || true
[ $CHECK = 1 ] && { echo "nothing written."; exit 0; }

cp "$SRC" "$DEST"
echo "published $SRC (commit $COMMIT) → $DEST"
echo "next: bump .claude-plugin/plugin.json, commit; release separately"
