#!/bin/bash
set -e

# Validate the propose→stage→promote self-extension loop
# Usage: bash scripts/validate-self-extension.sh [--keep]
#
# This script validates the gated self-extension feature by:
# 1. Creating a test proposal in in-progress/
# 2. Verifying it's isolated (not in catalog, not routable)
# 3. Running the promotion flow (move, update catalog/SKILLS/marketplace/versions)
# 4. Verifying the promoted skill is live and routable
# 5. Cleaning up — ALWAYS, including on failure or interrupt (--keep opts out)
#
# Cleanup is a trap, not a final block: `set -e` means a failing stage exits
# before any trailing code runs, which is how a previous run left
# test-validation-skill behind in library/ — where it was committed, and
# shipped to production.

REPO_ROOT="$(git rev-parse --show-toplevel)"
TEST_SKILL="test-validation-skill"
CLEANUP=true

case "${1:-}" in
  --keep)    CLEANUP=false ;;
  --cleanup) ;;                 # accepted: it used to be required
  "")        ;;
  *)         echo "unknown flag: $1 (use --keep to leave artifacts in place)" >&2; exit 2 ;;
esac

cleanup() {
  local rc=$?
  if [[ $CLEANUP == true ]]; then
    echo ""
    echo "Reverting test artifacts..."
    git -C "$REPO_ROOT" checkout library/catalog.yaml SKILLS.md \
      .claude-plugin/plugin.json .codex-plugin/plugin.json \
      .claude-plugin/marketplace.json 2>/dev/null || true
    rm -rf "$REPO_ROOT/library/$TEST_SKILL" "$REPO_ROOT/in-progress/$TEST_SKILL"
    if [[ -n "$(git -C "$REPO_ROOT" status --porcelain -- library SKILLS.md .claude-plugin .codex-plugin in-progress)" ]]; then
      echo "! cleanup left changes behind — inspect before committing:"
      git -C "$REPO_ROOT" status --short -- library SKILLS.md .claude-plugin .codex-plugin in-progress
    else
      echo "Clean."
    fi
  else
    echo ""
    echo "--keep: test artifacts left in place. To revert:"
    echo "  git -C $REPO_ROOT checkout library/catalog.yaml SKILLS.md .claude-plugin/plugin.json .codex-plugin/plugin.json .claude-plugin/marketplace.json"
    echo "  rm -rf $REPO_ROOT/library/$TEST_SKILL $REPO_ROOT/in-progress/$TEST_SKILL"
  fi
  exit $rc
}
trap cleanup EXIT INT TERM

echo "=== Self-Extension Validation ==="
echo "Repo root: $REPO_ROOT"
echo ""

# === STAGE 1: Verify staging area exists and is isolated ===
echo "[1/5] Checking staging area structure..."
if [[ ! -d "$REPO_ROOT/in-progress" ]]; then
  echo "❌ FAIL: in-progress/ doesn't exist"
  exit 1
fi
if [[ ! -f "$REPO_ROOT/in-progress/README.md" ]]; then
  echo "❌ FAIL: in-progress/README.md missing"
  exit 1
fi
echo "✓ Staging area exists"
echo ""

# === STAGE 2: Create a test proposal ===
echo "[2/5] Creating test proposal in staging..."
mkdir -p "$REPO_ROOT/in-progress/$TEST_SKILL"

cat > "$REPO_ROOT/in-progress/$TEST_SKILL/instructions.md" <<'EOF'
# test-validation-skill

A test skill to validate the self-extension pipeline. This demonstrates that
proposals can be authored, staged, promoted, and routed correctly.

## Instructions

This is a minimal validation skill with no real functionality — it exists only
to verify the propose→stage→promote loop works end-to-end.

1. If you see this, the promotion succeeded.
2. The skill was authored in a trace, staged in in-progress/, and promoted to
   library/ through the admin flow.
EOF

cat > "$REPO_ROOT/in-progress/$TEST_SKILL/PROPOSAL.md" <<EOF
# Proposal: $TEST_SKILL

**Proposed description:** Test skill to validate the self-extension pipeline; use to verify propose→stage→promote works end-to-end.

**Source trace:** Validation script $(date '+%Y-%m-%d'), ambient-library self-extension feature test.

**Evidence:** This is a synthetic proposal created by the validation script to exercise the propose→stage→promote loop without requiring a full Claude session.

**Overlap check:** No existing skills cover test validation. This is new.
EOF

echo "✓ Test proposal created"
if [[ ! -f "$REPO_ROOT/in-progress/$TEST_SKILL/instructions.md" ]]; then
  echo "❌ FAIL: proposal instructions.md not created"
  exit 1
fi
echo ""

# === STAGE 3: Verify isolation (not in catalog, not routable) ===
echo "[3/5] Verifying staging is isolated from routing..."

if grep -q "$TEST_SKILL\|in-progress" "$REPO_ROOT/library/catalog.yaml" 2>/dev/null; then
  echo "❌ FAIL: test skill or in-progress appears in catalog.yaml (should be invisible)"
  exit 1
fi
echo "✓ Catalog isolation verified"

if grep -q "in-progress" "$REPO_ROOT/.aai/skills/load.md" 2>/dev/null; then
  echo "❌ FAIL: load.md (routing path) mentions in-progress (should never route proposals)"
  exit 1
fi
echo "✓ Router isolation verified"
echo ""

# === STAGE 4: Promote the test skill ===
echo "[4/5] Promoting test skill from staging to library..."

# Move folder
mv "$REPO_ROOT/in-progress/$TEST_SKILL" "$REPO_ROOT/library/$TEST_SKILL"
rm -f "$REPO_ROOT/library/$TEST_SKILL/PROPOSAL.md"
echo "✓ Folder moved to library/"

# Add to catalog under skills:
sed -i '' "/^skills:/a\\
  $TEST_SKILL: Test skill to validate the self-extension pipeline; use to verify propose→stage→promote works end-to-end." "$REPO_ROOT/library/catalog.yaml"
echo "✓ Added to catalog.yaml"

# Add to SKILLS.md
if ! grep -q "^  $TEST_SKILL:" "$REPO_ROOT/SKILLS.md"; then
  cat >> "$REPO_ROOT/SKILLS.md" <<EOF
  $TEST_SKILL: Test skill to validate the self-extension pipeline; use to verify propose→stage→promote works end-to-end.
EOF
fi
echo "✓ Added to SKILLS.md"

# Bump plugin versions
for file in "$REPO_ROOT/.claude-plugin/plugin.json" "$REPO_ROOT/.codex-plugin/plugin.json"; do
  if [[ -f "$file" ]]; then
    # Increment patch version: x.y.z → x.y.(z+1)
    version=$(jq -r '.version' "$file")
    major=$(echo "$version" | cut -d. -f1)
    minor=$(echo "$version" | cut -d. -f2)
    patch=$(echo "$version" | cut -d. -f3)
    new_patch=$((patch + 1))
    new_version="$major.$minor.$new_patch"
    jq ".version = \"$new_version\"" "$file" > "$file.tmp" && mv "$file.tmp" "$file"
    echo "✓ Bumped $file to $new_version"
  fi
done

# Add to marketplace if template exists
if [[ -f "$REPO_ROOT/.claude-plugin/marketplace.json" ]]; then
  # Check if there's already a plugin entry template; add one for the test skill
  if ! jq -e ".plugins[] | select(.name == \"$TEST_SKILL\")" "$REPO_ROOT/.claude-plugin/marketplace.json" >/dev/null 2>&1; then
    # Simple append: find the last plugin entry and add after it
    # This is a bit fragile, but works for the test
    jq ".plugins += [{\"name\": \"$TEST_SKILL\", \"source\": \"./library/$TEST_SKILL\", \"description\": \"Test skill to validate self-extension pipeline\"}]" "$REPO_ROOT/.claude-plugin/marketplace.json" > "$REPO_ROOT/.claude-plugin/marketplace.json.tmp" && mv "$REPO_ROOT/.claude-plugin/marketplace.json.tmp" "$REPO_ROOT/.claude-plugin/marketplace.json"
    echo "✓ Added to marketplace.json"
  fi
fi
echo ""

# === STAGE 5: Verify promotion succeeded ===
echo "[5/5] Verifying promoted skill is live..."

if [[ ! -f "$REPO_ROOT/library/$TEST_SKILL/instructions.md" ]]; then
  echo "❌ FAIL: promoted skill instructions.md not in library/"
  exit 1
fi
echo "✓ Skill in library/"

if ! grep -q "$TEST_SKILL" "$REPO_ROOT/library/catalog.yaml"; then
  echo "❌ FAIL: skill not in catalog after promotion"
  exit 1
fi
echo "✓ Skill in catalog"

if ! grep -q "$TEST_SKILL" "$REPO_ROOT/SKILLS.md"; then
  echo "❌ FAIL: skill not in SKILLS.md after promotion"
  exit 1
fi
echo "✓ Skill in SKILLS.md"

# Verify not in staging
if [[ -d "$REPO_ROOT/in-progress/$TEST_SKILL" ]]; then
  echo "❌ FAIL: test skill still in in-progress after promotion"
  exit 1
fi
echo "✓ Removed from staging"

echo ""
echo "=== ✓ ALL VALIDATION CHECKS PASSED ==="
echo ""
echo "The self-extension loop works correctly:"
echo "  1. Proposed skills land in in-progress/ (isolated from routing)"
echo "  2. Staging is invisible to the catalog and router"
echo "  3. Promotion moves the skill to library/ and updates all artifacts"
echo "  4. The promoted skill is now live in the catalog and routable"
echo ""
