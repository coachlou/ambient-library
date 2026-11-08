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
| `aimm-shared-repo` | coachlou/aimm | **publish from here** (must be clean; herenow/ and other local-only files are gitignored) |
| `~/.ailib` | coachlou/aai-library | Lou's local library (non-plugin harnesses) |
| `~/.claude/plugins/…/aai-library` | coachlou/aai-library | Claude's `ambient@aai-library` plugin |

## The chain

1. **soloFactory** (skip if unchanged): bump `package.json`, add a PROGRESS entry, tests pass,
   `git tag v<ver>`, `git push origin main --tags`.
   **Docs review first**, against every owner-visible change since the last tag (`git log v<prev>..`):
   `docs/INSTALL.md` (+ `distro/INSTALL.md`) *below <ver>* update note, `docs/manual/index.html`
   (section and Settings row), `README.md`, guides in `docs/`. Record it as a `- Docs:` bullet in
   the PROGRESS entry ("none" with the reason if nothing changed). `npm test` fails without that
   bullet, or when `src/` reads a `SOLOFACTORY_*` setting the manual's Settings table lacks.
2. **ambient-library**: `scripts/sync-distro.sh --ref v<ver> solofactory ../soloFactory`, commit;
   bump `.claude-plugin/plugin.json`, commit; `git push origin main`.
3. **aai-library**: `scripts/publish-distro.sh ../aai-library-release`, then
   `git -C ../aai-library-release push origin main --tags`.
4. **aimm** (members): `scripts/publish-aimm.sh ../aimm-shared-repo`, then
   `git -C ../aimm-shared-repo push origin main`.
5. **Working clones**: `git pull --ff-only` in `aai-library`.
6. **Lou's local copies**: `git -C ~/.ailib pull --ff-only`;
   `claude plugin marketplace update aai-library`; `claude plugin update ambient@aai-library`
   (takes effect after a Claude restart).
7. **`scripts/release-check.sh`**: fix every FAIL line, rerun until it exits 0.
8. **Member letter**: an unsent draft in soloFactory `notes/member-letter-*.md` is renamed to the
   new version and updated for it (version in subject, body and update prompt; a line for each
   owner-visible change since the last *sent* SoloFactory release email (any segment), found in Resend
   broadcasts, not just this release). Part of the release, not a follow-up.
