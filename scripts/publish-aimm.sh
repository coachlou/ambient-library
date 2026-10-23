#!/bin/bash
# Publish the SoloFactory install set to the AIMM members' repo (coachlou/aimm).
#
# Builds production, then copies library/{ambient-folder,dev-rules,solofactory}
# into <aimm clone>/aai-release/solofactory/library/. That is the same set the
# tester zip carries; bootstrap.sh falls back to it when aai-library is unreadable.
# Commits only; never pushes.
#
# Usage: publish-aimm.sh <aimm-clone> [--dry-run]    exit 2 = bad clone
set -euo pipefail
cd "$(dirname "$0")/.."
AIMM="${1:?usage: publish-aimm.sh <aimm-clone> [--dry-run]}"; DRY="${2:-}"
case "$(git -C "$AIMM" remote get-url origin 2>/dev/null || true)" in
  *coachlou/aimm*) ;; *) echo "refusing: $AIMM is not a coachlou/aimm clone" >&2; exit 2 ;;
esac
[ -z "$(git -C "$AIMM" status --porcelain)" ] || { echo "refusing: $AIMM has uncommitted changes" >&2; exit 2; }
git -C "$AIMM" pull -q --ff-only 2>/dev/null || true
STAGE="$(mktemp -d)"; trap 'rm -rf "$STAGE"' EXIT
scripts/build-production.sh "$STAGE" >/dev/null
VER=$(cat "$STAGE/library/solofactory/app/VERSION" | head -1)
OUT="$AIMM/aai-release/solofactory"; mkdir -p "$OUT/library"
for c in ambient-folder dev-rules solofactory; do
  rsync -a --checksum --delete ${DRY:+--dry-run --itemize-changes} "$STAGE/library/$c/" "$OUT/library/$c/"
done
[ -n "$DRY" ] && { echo "dry run, nothing written"; exit 0; }
cp "$STAGE/library/solofactory/INSTALL.md" "$OUT/INSTALL.md"
git -C "$AIMM" add aai-release/solofactory
git -C "$AIMM" diff --cached --quiet && { echo "nothing changed"; exit 0; }
git -C "$AIMM" commit -q -m "SoloFactory install set: $VER" -m "Built by ambient-library scripts/publish-aimm.sh."
echo "committed in $AIMM; to publish:  git -C '$AIMM' push origin main"
