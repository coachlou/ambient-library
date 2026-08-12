#!/bin/bash
# Promote a capability from in-progress/ into the canonical library.
#
#   promote.sh <name> [--dry-run]
#
# Handles both cases:
#   new      library/<name>/ does not exist — a straight move
#   replace  library/<name>/ exists — you have been reworking a live capability.
#            The old version is shown, the version bumped, and if the skill is
#            in RELEASE.yaml you are told production is now stale.
#
# It does NOT commit, push, or deploy. It prints exactly what is left to do.
# Exit codes: 0 ok · 1 not found · 2 incomplete skill · 3 wrong folder
set -euo pipefail
cd "$(dirname "$0")/.."

NAME="${1:-}"
DRY=false
[ "${2:-}" = "--dry-run" ] && DRY=true
[ -n "$NAME" ] || { echo "usage: promote.sh <name> [--dry-run]" >&2; exit 1; }

[ -f .aai/PRODUCTION ] && { echo "refusing: this is a production build, not the dev workspace." >&2; exit 3; }
SRC="in-progress/$NAME"
[ -d "$SRC" ] || { echo "no such capability: $SRC" >&2; exit 1; }

# --- the four-file contract, checked before anything moves ----------------
MISSING=()
[ -f "$SRC/instructions.md" ] || MISSING+=("instructions.md")
[ -f "$SRC/SKILL.md" ] || MISSING+=("SKILL.md")
[ -f "$SRC/.claude-plugin/plugin.json" ] || MISSING+=(".claude-plugin/plugin.json")
if [ ${#MISSING[@]} -gt 0 ]; then
  echo "not ready — $SRC is missing: ${MISSING[*]}" >&2
  echo "See .aai/skills/admin.md 'Create a domain skill'." >&2
  exit 2
fi

REPLACING=false
[ -d "library/$NAME" ] && REPLACING=true
RELEASED=$(grep -c "^  - $NAME\$" RELEASE.yaml || true)

if $REPLACING; then
  echo "REPLACING an existing library capability: $NAME"
  OLDV=$(python3 -c "import json;print(json.load(open('library/$NAME/.claude-plugin/plugin.json')).get('version','?'))" 2>/dev/null || echo "?")
  NEWV=$(python3 -c "import json;print(json.load(open('$SRC/.claude-plugin/plugin.json')).get('version','?'))" 2>/dev/null || echo "?")
  echo "  version: $OLDV -> $NEWV"
  [ "$OLDV" = "$NEWV" ] && echo "  ! same version — bump $SRC/.claude-plugin/plugin.json before promoting"
  echo "  diff:"; diff -rq "library/$NAME" "$SRC" 2>/dev/null | sed 's/^/    /' || true
else
  echo "NEW capability: $NAME"
fi

if $DRY; then echo; echo "dry run — nothing moved."; exit 0; fi

rm -rf "library/$NAME"
mv "$SRC" "library/$NAME"
echo "moved -> library/$NAME"

echo
echo "Still to do — promote.sh deliberately does none of this:"
if ! $REPLACING; then
  echo "  1. add a one-line entry to library/catalog.yaml"
  echo "  2. add the marketplace.json entry (see .aai/skills/admin.md)"
  echo "  3. add a SKILLS.md row"
  echo "  4. python3 scripts/audit-distribution.py   (must exit 0)"
  echo "  5. commit + push"
  echo "  6. release: add '$NAME' to RELEASE.yaml, then scripts/build-production.sh"
else
  echo "  1. if the description changed, re-sync it into catalog.yaml,"
  echo "     plugin.json and marketplace.json (verbatim) — descriptions are"
  echo "     routing triggers, so re-test matching before you ship"
  echo "  2. python3 scripts/audit-distribution.py   (must exit 0)"
  echo "  3. commit + push"
  if [ "$RELEASED" -gt 0 ]; then
    echo "  4. PRODUCTION IS NOW STALE — it still serves the old $NAME."
    echo "     Redeploy: scripts/build-production.sh"
  else
    echo "  4. not in RELEASE.yaml, so production is unaffected"
  fi
fi
