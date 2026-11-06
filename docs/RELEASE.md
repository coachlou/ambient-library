# Releasing

One chain, every time. Each script commits only; pushes are separate steps.
A release is **done only when `scripts/release-check.sh` exits 0.**

## Clone roles (GitHub folder)

| Clone | Remote | Role |
|---|---|---|
| `soloFactory` | coachlou/soloFactory | dev |
| `ambient-library` | coachlou/ambient-library | canonical library (this repo) |
| `aai-library-release` | coachlou/aai-library | **publish from here** (must be clean) |
| `aai-library` | coachlou/aai-library | working clone: fast-forward only |
| `aimm-publish-clone` | coachlou/aimm | **publish from here** (must be clean) |
| `aimm-shared-repo` | coachlou/aimm | working clone, has Lou's edits: fast-forward only, never publish from it |
| `~/.ailib` | coachlou/aai-library | Lou's local library (non-plugin harnesses) |
| `~/.claude/plugins/…/aai-library` | coachlou/aai-library | Claude's `ambient@aai-library` plugin |

## The chain

1. **soloFactory** (skip if unchanged): bump `package.json`, add a PROGRESS entry, tests pass,
   `git tag v<ver>`, `git push origin main --tags`.
2. **ambient-library**: `scripts/sync-distro.sh --ref v<ver> solofactory ../soloFactory`, commit;
   bump `.claude-plugin/plugin.json`, commit; `git push origin main`.
3. **aai-library**: `scripts/publish-distro.sh ../aai-library-release`, then
   `git -C ../aai-library-release push origin main --tags`.
4. **aimm** (members): `scripts/publish-aimm.sh ../aimm-publish-clone`, then
   `git -C ../aimm-publish-clone push origin main`.
5. **Working clones**: `git pull --ff-only` in `aai-library` and `aimm-shared-repo`.
6. **Lou's local copies**: `git -C ~/.ailib pull --ff-only`;
   `claude plugin marketplace update aai-library`; `claude plugin update ambient@aai-library`
   (takes effect after a Claude restart).
7. **`scripts/release-check.sh`**: fix every FAIL line, rerun until it exits 0.
