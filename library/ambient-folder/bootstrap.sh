#!/usr/bin/env bash
# bootstrap.sh — one-line install of any canonical capability, no library plugin needed.
#
#   curl -fsSL https://raw.githubusercontent.com/coachlou/ambient-library/main/library/ambient-folder/bootstrap.sh | bash -s -- <cap> [target-dir]
#
# Fetches the released library and runs ambient-folder/install.sh <cap> on
# <target-dir> (default: current directory). Needs tar. Re-run to update.
#
# This script is public; the releases it installs are not. It needs GitHub read
# access: the `gh` CLI signed in (`gh auth login`), or GITHUB_TOKEN / GH_TOKEN set.
# It tries coachlou/aai-library first, then falls back to the AIMM members' repo
# coachlou/aimm (aai-release/solofactory/), which every member can already read.
# With neither readable, ask for an invite to the AIMM repo.
set -euo pipefail
[ -n "${1:-}" ] || { sed -n '2,12p' "$0" 2>/dev/null || echo "usage: bootstrap.sh <cap> [target]"; exit 2; }
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
TOKEN="${GITHUB_TOKEN:-${GH_TOKEN:-}}"
fetch() {  # fetch <repo> -> $TMP/lib.tar.gz; non-zero when unreadable
  if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
    gh api "repos/$1/tarball/main" > "$TMP/lib.tar.gz" 2>/dev/null
  elif [ -n "$TOKEN" ]; then
    curl -fsSL -H "Authorization: Bearer $TOKEN" -o "$TMP/lib.tar.gz" "https://api.github.com/repos/$1/tarball/main" 2>/dev/null
  else
    sed -n '9,12p' "$0" >&2; exit 2
  fi
}
# ponytail: whole-repo tarball (a few MB) — portable across BSD/GNU tar
fetch coachlou/aai-library || fetch coachlou/aimm || { echo "cannot read coachlou/aai-library or coachlou/aimm — ask for an invite to the AIMM repo" >&2; exit 2; }
tar -xzf "$TMP/lib.tar.gz" -C "$TMP"
# aai-library keeps library/ at its root; aimm keeps it under aai-release/solofactory/
INSTALL="$(find "$TMP" -path '*/library/ambient-folder/install.sh' -print -quit)"
[ -n "$INSTALL" ] || { echo "unexpected tarball layout" >&2; exit 2; }
bash "$INSTALL" "$@"
