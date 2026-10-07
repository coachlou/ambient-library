#!/usr/bin/env bash
# install.sh — make the global coding rules ambient in every harness.
#
#   bash install.sh [--check] [--no-git] [--home DIR]
#
# User scope (the ~/.aai self scope), never a project folder. It:
#   1. seeds ~/.aai/rules/coding.md from this capability's published snapshot
#      when absent. The owner's copy is the authority and is never overwritten;
#   2. routes coding work to it: when ~/.aai/context.md exists (the trigger
#      table core.md's bootstrap reads), appends one trigger row unless
#      coding.md is already routed. core.md itself is never edited;
#   3. puts ~/.aai under git when it is not already in a repo, and commits
#      rules/ and context.md. Local only: no remote, no push. --no-git skips it;
#   4. for each installed file-based harness (HARNESSES below), appends a
#      pointer block to its global instruction file, unless that file already
#      sends the agent to ~/.aai: an existing bootstrap adapter reaches
#      coding.md through context.md, and a second pointer would duplicate it.
# Chat surfaces without file access (claude.ai chat, Cowork settings) cannot
# be written by a script; run paste.sh and paste its output once.
# Re-running is safe: every step is skipped when already done.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SNAPSHOT="$HERE/../rules/coding.md"
CHECK=0 GIT=1 H="$HOME"
while [ $# -gt 0 ]; do
  case "$1" in
    --check) CHECK=1 ;;
    --no-git) GIT=0 ;;
    --home) H="$2"; shift ;;
    -h|--help) sed -n '2,21p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
  shift
done
[ -f "$SNAPSHOT" ] || { echo "missing snapshot: $SNAPSHOT" >&2; exit 2; }

AAI="$H/.aai"
CONTEXT="$AAI/context.md"
RULES="$AAI/rules/coding.md"
BEGIN="<!-- dev-rules:begin -->"
END="<!-- dev-rules:end -->"
say() { printf '  %-7s %s\n' "$1" "$2"; }

# File-based harnesses: "<name>|<global instruction file>|<installed when this dir exists>".
# An empty third field means always (the primary harness).
HARNESSES="
claude-code|$H/.claude/CLAUDE.md|
codex|${CODEX_HOME:-$H/.codex}/AGENTS.md|${CODEX_HOME:-$H/.codex}
opencode|${XDG_CONFIG_HOME:-$H/.config}/opencode/AGENTS.md|${XDG_CONFIG_HOME:-$H/.config}/opencode
"

pointer() {
  printf '%s\n' "$BEGIN" \
    "## Coding rules (ambient)" \
    "" \
    "Whenever this conversation writes, changes, or reviews code, in any folder," \
    "read and follow \`~/.aai/rules/coding.md\`. Project instructions may tighten" \
    "those rules; they do not loosen them. If \`~/.aai/rules/core.md\` exists," \
    "follow its bootstrap as well." \
    "$END"
}

context_route() {
  printf '%s\n' "" \
    "## Coding rules (added by dev-rules)" \
    "" \
    "| Trigger | Load |" \
    "|---|---|" \
    "| Writing, changing, or reviewing code, in any folder, harness, or capability | \`rules/coding.md\` |"
}

# Already wired: our block, or an existing adapter that points at ~/.aai.
wired() { [ -f "$1" ] && grep -qE "dev-rules:begin|~/\.aai|\\\$HOME/\.aai" "$1"; }

targets() {
  echo "$HARNESSES" | while IFS='|' read -r name file when; do
    [ -n "$name" ] || continue
    [ -z "$when" ] || [ -d "$when" ] || continue
    echo "$name|$file"
  done
}

# ── plan ─────────────────────────────────────────────────────────────────────
if [ -f "$RULES" ]; then say keep "$RULES (owned, never overwritten)"; else say seed "$RULES"; fi
if [ ! -f "$CONTEXT" ]; then say skip "$CONTEXT absent; harness pointers route coding directly"
elif grep -qF "rules/coding.md" "$CONTEXT"; then say keep "$CONTEXT (routes coding already)"
else say route "$CONTEXT (append coding trigger)"; fi
IN_GIT=0
git -C "$AAI" rev-parse --is-inside-work-tree >/dev/null 2>&1 && IN_GIT=1
if [ $GIT = 1 ]; then
  if [ $IN_GIT = 1 ]; then say keep "$AAI (already in git; commit changes yourself)"
  else say git "init $AAI, commit rules/ and context.md"; fi
fi
while IFS='|' read -r name file; do
  if wired "$file"; then say keep "$file ($name, already points to ~/.aai)"
  else say anchor "$file ($name)"; fi
done < <(targets)
say paste "claude.ai chat, Cowork: run paste.sh and paste once (no file access)"
[ $CHECK = 1 ] && { echo "nothing written."; exit 0; }

# ── seed and route ───────────────────────────────────────────────────────────
mkdir -p "$AAI/rules"
[ -f "$RULES" ] || cp "$SNAPSHOT" "$RULES"
if [ -f "$CONTEXT" ] && ! grep -qF "rules/coding.md" "$CONTEXT"; then
  context_route >> "$CONTEXT"
fi

# ── version ~/.aai ───────────────────────────────────────────────────────────
if [ $GIT = 1 ] && [ $IN_GIT = 0 ]; then
  git -C "$AAI" init -q -b main
  git -C "$AAI" add rules
  [ -f "$CONTEXT" ] && git -C "$AAI" add context.md
  git -C "$AAI" -c user.name="${GIT_AUTHOR_NAME:-dev-rules}" \
    -c user.email="${GIT_AUTHOR_EMAIL:-dev-rules@localhost}" \
    commit -q -m "Track ~/.aai rules (dev-rules install)"
fi

# ── anchor each installed harness ────────────────────────────────────────────
while IFS='|' read -r name file; do
  wired "$file" && continue
  mkdir -p "$(dirname "$file")"
  { [ -s "$file" ] && echo; pointer; } >> "$file"
done < <(targets)

grep -q '^## 1\. Design' "$RULES" || \
  say note "$RULES has no design section; merge it from $SNAPSHOT"
echo "dev-rules: coding conversations in every wired harness now load $RULES"
