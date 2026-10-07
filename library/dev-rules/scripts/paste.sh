#!/usr/bin/env bash
# paste.sh — print the coding rules for surfaces that cannot read ~/.aai.
#
#   bash paste.sh [--source FILE]
#
# claude.ai chat and Cowork share one field (Settings → Instructions for
# Claude, or a Project's instructions) that takes pasted text, not a path. This
# prints the owner's ~/.aai/rules/coding.md (else the published snapshot)
# framed for pasting, with its character count. Re-paste after each publish:
# a pasted copy does not update itself.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$HOME/.aai/rules/coding.md"
[ -f "$SRC" ] || SRC="$HERE/../rules/coding.md"
while [ $# -gt 0 ]; do
  case "$1" in
    --source) SRC="$2"; shift ;;
    -h|--help) sed -n '2,10p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
  shift
done

BODY="$(printf 'When this conversation writes, changes, or reviews code, follow these rules.\n\n'; cat "$SRC")"
printf '%s\n' "$BODY"
echo "--- $(printf '%s' "$BODY" | wc -m | tr -d ' ') characters from $SRC" >&2
