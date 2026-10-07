#!/usr/bin/env bash
# test_dev_rules.sh — exercise install.sh, publish.sh, and paste.sh in throwaway homes.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SNAPSHOT="$HERE/../rules/coding.md"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"; [ -f "$TMP.snap" ] && mv "$TMP.snap" "$SNAPSHOT"' EXIT
export GIT_AUTHOR_NAME=test GIT_AUTHOR_EMAIL=test@localhost
export GIT_COMMITTER_NAME=test GIT_COMMITTER_EMAIL=test@localhost
unset CODEX_HOME XDG_CONFIG_HOME OPENCODE_CONFIG_DIR DSH_HOME OPENCODE_DISABLE_CLAUDE_CODE OPENCODE_DISABLE_CLAUDE_CODE_PROMPT
FAILS=0
ok() { echo "ok    $1"; }
bad() { echo "FAIL  $1"; FAILS=$((FAILS + 1)); }
check() { if eval "$2"; then ok "$1"; else bad "$1"; fi; }
count() { grep -cF "$1" "$2" 2>/dev/null || true; }

# ── fresh user: no ~/.aai, no harness files ──────────────────────────────────
F="$TMP/fresh"; mkdir -p "$F"
HOME="$F" bash "$HERE/install.sh" --check >/dev/null
check "--check writes nothing" '[ ! -e "$F/.aai" ] && [ ! -e "$F/.claude" ]'
HOME="$F" bash "$HERE/install.sh" >/dev/null
check "seeds coding.md from the snapshot" 'cmp -s "$SNAPSHOT" "$F/.aai/rules/coding.md"'
check "puts ~/.aai under git" 'git -C "$F/.aai" log --oneline | grep -q dev-rules'
check "never creates core.md" '[ ! -e "$F/.aai/rules/core.md" ]'
check "anchors Claude Code" '[ "$(count dev-rules:begin "$F/.claude/CLAUDE.md")" = 1 ]'
check "skips harnesses not installed" '[ ! -e "$F/.codex" ] && [ ! -e "$F/.config/opencode" ]'
HOME="$F" bash "$HERE/install.sh" >/dev/null
check "re-run adds no second pointer" '[ "$(count dev-rules:begin "$F/.claude/CLAUDE.md")" = 1 ]'

# ── owner: existing bootstrap adapter, context.md, other harnesses ───────────
O="$TMP/owner"; mkdir -p "$O/.aai/rules" "$O/.claude" "$O/.codex" "$O/.config/opencode" "$O/.dsh"
printf '# Core\n' > "$O/.aai/rules/core.md"
printf '# My coding rules\n' > "$O/.aai/rules/coding.md"
printf '# Context\n\n| Trigger | Load |\n|---|---|\n' > "$O/.aai/context.md"
printf 'Read ~/.aai/identity.md and ~/.aai/rules/core.md first.\n' > "$O/.claude/CLAUDE.md"
printf '# my codex notes\n' > "$O/.codex/AGENTS.md"
HOME="$O" bash "$HERE/install.sh" --no-git >/dev/null
check "keeps the owner's coding.md" 'grep -q "My coding rules" "$O/.aai/rules/coding.md"'
check "leaves core.md untouched" '[ "$(cat "$O/.aai/rules/core.md")" = "# Core" ]'
check "routes coding in context.md" '[ "$(count rules/coding.md "$O/.aai/context.md")" = 1 ]'
check "keeps an adapter already wired to ~/.aai" '! grep -q dev-rules "$O/.claude/CLAUDE.md"'
check "appends to an existing Codex file" 'grep -q "my codex notes" "$O/.codex/AGENTS.md" && grep -q dev-rules:begin "$O/.codex/AGENTS.md"'
check "never creates opencode's AGENTS.md (it falls back to CLAUDE.md)" '[ ! -e "$O/.config/opencode/AGENTS.md" ]'
check "anchors DeepSeek Harness" 'grep -q dev-rules:begin "$O/.dsh/AGENTS.md"'

# ── harness precedence: existing opencode file, Codex override ───────────────
P="$TMP/prec"; mkdir -p "$P/.codex" "$P/.config/opencode"
printf '# override\n' > "$P/.codex/AGENTS.override.md"
printf '# opencode rules\n' > "$P/.config/opencode/AGENTS.md"
HOME="$P" bash "$HERE/install.sh" --no-git >/dev/null
check "Codex override gets the pointer" 'grep -q dev-rules:begin "$P/.codex/AGENTS.override.md" && [ ! -e "$P/.codex/AGENTS.md" ]'
check "existing opencode file gets the pointer" 'grep -q dev-rules:begin "$P/.config/opencode/AGENTS.md"'
check "--no-git leaves ~/.aai unversioned" '[ ! -d "$O/.aai/.git" ]'
HOME="$O" bash "$HERE/install.sh" --no-git >/dev/null
check "re-run routes once" '[ "$(count rules/coding.md "$O/.aai/context.md")" = 1 ]'

# ── design-section note: any heading style counts ────────────────────────────
D="$TMP/design"; mkdir -p "$D/.aai/rules"
printf '# Coding Rules\n\n## Design: deep modules, one owner per concern\n' > "$D/.aai/rules/coding.md"
check "no merge note when an unnumbered Design heading exists" '! HOME="$D" bash "$HERE/install.sh" --no-git | grep -q "no design section"'
printf '# Coding Rules\n\n## Testing\n' > "$D/.aai/rules/coding.md"
check "merge note when the design section is missing" 'HOME="$D" bash "$HERE/install.sh" --no-git | grep -q "no design section"'

# ── publish: authority flows home → library ──────────────────────────────────
cp "$SNAPSHOT" "$TMP.snap"
echo "- extra rule" >> "$F/.aai/rules/coding.md"
check "publish refuses uncommitted source" '! HOME="$F" bash "$HERE/publish.sh" >/dev/null 2>&1'
git -C "$F/.aai" commit -qam "tighten"
HOME="$F" bash "$HERE/publish.sh" --check >/dev/null
check "publish --check writes nothing" 'cmp -s "$TMP.snap" "$SNAPSHOT"'
HOME="$F" bash "$HERE/publish.sh" >/dev/null
check "publish copies the committed source" 'grep -q "extra rule" "$SNAPSHOT"'
check "publish is idempotent" 'HOME="$F" bash "$HERE/publish.sh" | grep -q "already published"'

# ── paste: for surfaces without file access ──────────────────────────────────
check "paste prints the owner's rules" 'HOME="$F" bash "$HERE/paste.sh" 2>/dev/null | grep -q "extra rule"'
check "paste falls back to the snapshot" 'HOME="$TMP/nobody" bash "$HERE/paste.sh" 2>/dev/null | grep -qF "$(head -1 "$SNAPSHOT")"'

[ $FAILS = 0 ] && echo "all passed" || { echo "$FAILS failed"; exit 1; }
