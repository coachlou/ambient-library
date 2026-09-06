#!/usr/bin/env bash
# bootstrap.sh — one-line SoloFactory install for members without the library plugin.
#
#   curl -fsSL https://raw.githubusercontent.com/coachlou/ambient-library/main/library/solofactory/bootstrap.sh | bash -s -- [target-dir]
#
# Fetches the solofactory capability from the library and runs its install.sh
# on <target-dir> (default: current directory). Needs curl and tar. Re-run to update.
set -euo pipefail
TARBALL="https://github.com/coachlou/ambient-library/archive/refs/heads/main.tar.gz"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
# ponytail: pulls the whole repo tarball (~few MB) — portable across BSD/GNU tar; filter if size ever matters
curl -fsSL "$TARBALL" | tar -xz -C "$TMP"
CAP="$TMP/ambient-library-main/library/solofactory"
[ -f "$CAP/install.sh" ] || { echo "download failed: solofactory not found in archive" >&2; exit 1; }
bash "$CAP/install.sh" "$@"
