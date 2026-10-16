#!/usr/bin/env bash
# Launcher target. Walks up from cwd to the ambient folder, then runs the vendored app.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
root="$PWD"
while [ "$root" != "/" ] && [ ! -d "$root/.aai" ]; do root="$(dirname "$root")"; done
[ -d "$root/.aai" ] || { echo "tinkerbuild: no .aai/ found above $PWD" >&2; exit 1; }
cd "$root"
exec python3 "$here/app/scripts/tb.py" "$@"
