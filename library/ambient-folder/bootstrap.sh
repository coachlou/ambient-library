#!/usr/bin/env bash
# bootstrap.sh — one-line install of any canonical capability, no library plugin needed.
#
#   curl -fsSL https://raw.githubusercontent.com/coachlou/ambient-library/main/library/ambient-folder/bootstrap.sh | bash -s -- <cap> [target-dir]
#
# Fetches the library and runs ambient-folder/install.sh <cap> on <target-dir>
# (default: current directory). Needs curl and tar. Re-run to update.
set -euo pipefail
[ -n "${1:-}" ] || { sed -n '2,7p' "$0" 2>/dev/null || echo "usage: bootstrap.sh <cap> [target]"; exit 2; }
TARBALL="https://github.com/coachlou/ambient-library/archive/refs/heads/main.tar.gz"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
# ponytail: whole repo tarball (a few MB) — portable across BSD/GNU tar; filter if size ever matters
curl -fsSL "$TARBALL" | tar -xz -C "$TMP"
bash "$TMP/ambient-library-main/library/ambient-folder/install.sh" "$@"
