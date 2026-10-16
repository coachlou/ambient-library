#!/usr/bin/env bash
# Runs after install with TARGET (the folder) and CAP_DIR (.ailib/tinkerbuild). Writes the launcher.
set -euo pipefail
cat > "$TARGET/tb.sh" <<'SH'
#!/usr/bin/env bash
d="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
for r in "$d/.aai/skills/tinkerbuild/run.sh" "$d/.ailib/tinkerbuild/run.sh"; do
  [ -f "$r" ] && exec bash "$r" "$@"
done
echo "tinkerbuild is not installed here; re-run the install one-liner" >&2; exit 1
SH
chmod +x "$TARGET/tb.sh"
