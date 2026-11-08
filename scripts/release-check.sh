#!/bin/bash
# Read-only: is the whole release chain lined up? See docs/RELEASE.md.
# Fetches every repo, compares it with its remote, and checks that the
# distributions and Lou's local copies (~/.ailib, the ambient plugin) carry
# the latest versions. A release is done only when this exits 0.
#
# Usage: release-check.sh            GH_DIR overrides the GitHub folder.
set -uo pipefail
GH="${GH_DIR:-/Volumes/Extreme Pro/users/loudalo/GitHub}"
FAIL=0
ok()   { printf '  ok    %s\n' "$*"; }
warn() { printf '  note  %s\n' "$*"; }
bad()  { printf '  FAIL  %s\n' "$*"; FAIL=1; }

# repo <path> <label> <dirty-ok:yes|no>
repo() {
  local d="$1" name="$2" dirty_ok="$3"
  [ -d "$d/.git" ] || { bad "$name: no clone at $d"; return; }
  git -C "$d" fetch -q --tags origin 2>/dev/null || { bad "$name: fetch failed"; return; }
  local br; br=$(git -C "$d" rev-parse --abbrev-ref HEAD)
  [ "$br" = main ] || bad "$name: on branch $br, not main"
  local ahead behind
  read -r behind ahead < <(git -C "$d" rev-list --left-right --count origin/main...HEAD)
  if [ "$ahead" -gt 0 ]; then bad "$name: $ahead commit(s) not pushed"
  elif [ "$behind" -gt 0 ]; then bad "$name: $behind commit(s) behind origin (git -C '$d' pull --ff-only)"
  else ok "$name: matches origin ($(git -C "$d" rev-parse --short HEAD))"; fi
  if [ -n "$(git -C "$d" status --porcelain --untracked-files=no)" ]; then
    [ "$dirty_ok" = yes ] && warn "$name: has uncommitted edits (left alone)" \
                          || bad "$name: publish clone has uncommitted edits"
  fi
}

tag_on_remote() { git -C "$1" ls-remote --exit-code --tags origin "refs/tags/$2" >/dev/null 2>&1; }
pver() { python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["version"])' "$1"; }

echo "Repos"
repo "$GH/soloFactory"          "soloFactory (dev)"                  yes
repo "$GH/ambient-library"      "ambient-library (canonical)"        yes
repo "$GH/aai-library-release"  "aai-library-release (publish clone)" no
repo "$GH/aai-library"          "aai-library (working clone)"        yes
repo "$GH/aimm-shared-repo"     "aimm-shared-repo (publish clone)"   no
repo "$HOME/.ailib"             "~/.ailib (local library)"           no

echo "Versions"
SF=$(pver "$GH/soloFactory/package.json")
tag_on_remote "$GH/soloFactory" "v$SF" && ok "soloFactory v$SF tagged and pushed" \
  || bad "soloFactory v$SF: tag not on origin"
for f in "ambient-library:$GH/ambient-library/library/solofactory/app/VERSION" \
         "aai-library:$GH/aai-library-release/library/solofactory/app/VERSION" \
         "aimm:$GH/aimm-shared-repo/aai-release/solofactory/library/solofactory/app/VERSION" \
         "~/.ailib:$HOME/.ailib/library/solofactory/app/VERSION"; do
  n="${f%%:*}"; p="${f#*:}"
  grep -q "solofactory $SF " "$p" 2>/dev/null && ok "$n carries solofactory $SF" \
    || bad "$n carries '$(head -1 "$p" 2>/dev/null)', not solofactory $SF"
done

PL=$(pver "$GH/ambient-library/.claude-plugin/plugin.json")
tag_on_remote "$GH/aai-library-release" "v$PL" && ok "aai-library v$PL tagged and pushed" \
  || bad "aai-library v$PL: tag not on origin (publish-distro.sh, then push --tags)"
for f in "aai-library-release:$GH/aai-library-release/.claude-plugin/plugin.json" \
         "~/.ailib:$HOME/.ailib/.claude-plugin/plugin.json"; do
  v=$(pver "${f#*:}" 2>/dev/null); [ "$v" = "$PL" ] && ok "${f%%:*} plugin $v" || bad "${f%%:*} plugin $v, not $PL"
done

echo "Claude plugin"
MK="$HOME/.claude/plugins/marketplaces/aai-library"
REMOTE=$(git -C "$GH/aai-library-release" rev-parse origin/main)
[ "$(git -C "$MK" rev-parse HEAD 2>/dev/null)" = "$REMOTE" ] && ok "marketplace clone matches aai-library" \
  || bad "marketplace clone is stale (claude plugin marketplace update aai-library)"
python3 - "$PL" <<'PY' || FAIL=1
import json, os, sys
want = sys.argv[1]
recs = json.load(open(os.path.expanduser("~/.claude/plugins/installed_plugins.json")))["plugins"].get("ambient@aai-library", [])
user = [r for r in recs if r.get("scope") == "user"]
if user and user[0]["version"] == want:
    print(f"  ok    ambient plugin (user) {want}; restart Claude if just updated")
else:
    print(f"  FAIL  ambient plugin (user) {user[0]['version'] if user else 'missing'}, not {want} (claude plugin update ambient@aai-library)")
    sys.exit(1)
for r in recs:
    if r.get("scope") == "project" and r["version"] != want:
        print(f"  note  project install {r['version']} in {r.get('projectPath')}")
PY

echo
[ "$FAIL" = 0 ] && echo "All lined up: release done." || echo "Not done: fix the FAIL lines above."
exit "$FAIL"
