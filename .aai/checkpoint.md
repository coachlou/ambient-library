# Checkpoint — ambient-library

## Current state
**Next objective:** release 2.2.0 and move Lou's live AIMM newsletter onto it.
Each step is outward-facing and needs Lou's go: push `main`; build and publish
the distribution (`scripts/build-production.sh`, `scripts/publish-distro.sh`);
pull `~/.ailib`; in the AIMM folder run the skill's `scripts/resolve.py --init`
then `--set` with the live values (group `aimm_member`, account `aimm_support`,
prefix `[AIMM]`, `send_mode` individual, header "AI Leaders Mastermind", footer
"Successpod, Inc.", unsubscribe `none`); repoint `aimm-send` (location unknown
— ask Lou); send a two-member test; then archive the branded copy in
`/Volumes/…/.claude/skills/aimm-newsletter/`.

**Where things stand (2026-09-17):**
- The personalization layer is designed and built. Design:
  `docs/PLAN-personalization-layer.md` (v4.5). 1:n is an opt-in evolution of the
  standard skill — default stays cwd = workspace; an opted-in skill ships
  `contract.yaml`, and `scripts/resolve.py` decides which project folder it is
  working in and where values are saved. No existing skill migrates unless picked.
- Rollout steps 1–4 are done: shared rules (`load.md`, `.aai/instructions.md`,
  `ambient-folder`, `docs/MANAGEMENT.md`), the resolver + 14 tests
  (`python3 scripts/test_resolve.py`), aimm-newsletter converted (v1.1.0), the
  build copies the resolver into opted-in skills, and the audit enforces the
  contract (`python3 scripts/audit-distribution.py --self-test`).
- Versions are bumped to 2.2.0 but nothing is pushed or published, and
  `~/.ailib` still holds 2.1.0.

**Open, Lou's call:**
- Rollout steps 5–6 (gears-*, gears-broadcast) — only if Lou picks them.
- gears-broadcast's segment ID and sender are in public git history: scrub or leave?
- Collapse gears-* into one capability and delete the DB "active org" selector?
- For a new project the resolver lists only project keys as `needs`; env keys
  surface after the first `--set`. Works, but it is two rounds of questions.

---

## 2026-09-16 checkpoint

**Done since last:**
- **Opt-in domain skills (released as v2.1.0).** A domain skill runs on its own
  only if it appears in the enabled set: the union of
  `~/.aai/skills-manifest.yaml`, the project's `skills-manifest.yaml`, and any
  skills vendored or forked into the project. A skill the user names runs
  anywhere. Why: installing the library should not make every skill a routing
  candidate.
  - Changed: `.aai/skills/{load,manage,select,install}.md`,
    `.aai/instructions.md`, `templates/AGENTS-pointer.md`, and the docs.
  - The global pointer block is in `~/.claude/CLAUDE.md`,
    `~/.codex/AGENTS.md`, `~/.gemini/GEMINI.md` and `~/AGENTS.md`.
  - The `ambient` Claude plugin is *not* installed; Claude uses the pointer.
- **User-scope manifest:** `~/.aai/skills-manifest.yaml` lists checkpoint,
  cognitive-mirror and capture-chat.
- **Leftover copies of library skills removed** from `~/.claude/skills`,
  `/Volumes/…/.claude/skills` and `~/.agents/skills`. No merges were needed:
  every library version was newer. Backups are in
  `~/.aai/archive/2026-09-16-skill-cleanup/`.
  - `sync-cognitive-mirror.sh` now copies only to `~/ambience-claude`.
  - The profile paths in `/Volumes/…/.claude/CLAUDE.md` now point to
    `~/.aai/references/cognitive-mirror/`.
- **Rule for what gets imported:** leave third-party skills alone (the
  Cloudflare, HyperFrames, Supabase, find-skills, here-now, grill-me,
  notebooklm, Council, prompt-engineer, faceless-explainer and general-video
  skills). Leave wbs-* in the wbs-toolkit repo. Your own skills that aren't in
  the library become candidates in `in-progress/`, listed in `CANDIDATES.md`.
  They don't ship until you promote them and add them to `RELEASE.yaml`.
- **Candidates are tracked in git** (the repo is public), except the
  gitignored gears-content, gears-init, gears-onboard (production Supabase
  project and client data) and gic-leap (personal portfolio app). A dry-run
  build confirmed the distribution excludes `in-progress/`
  (`scripts/release_filter.py` builds from an allowlist).
- **create-skill** was derived from Anthropic's skill-creator, so it keeps its
  Apache 2.0 `LICENSE.txt` and a note saying it was modified.
- **aimm-newsletter** is held as a candidate. Your branded copy stays
  installed in `/Volumes/…/.claude/skills`, because the library version uses
  placeholders. Why: a personalization layer is needed first.

**Touched:** `.gitignore`, `in-progress/{README,CANDIDATES}.md`,
`in-progress/<27 candidates>/`, `~/.aai/skills-manifest.yaml`,
`~/.aai/scripts/sync-cognitive-mirror.sh`, `/Volumes/…/.claude/CLAUDE.md`.

**Open:**
- Review the 27 candidates (see `in-progress/CANDIDATES.md`).
- capture-chat's `CHANGELOG.md` lists versions out of order (v1.1 appears
  above v1.2).
- The opt-in routing hasn't been tested in a real session yet.

**Next:** Say "design the personalization override layer" and start from the
`in-progress/CANDIDATES.md` follow-up section and the open questions above.
Use aimm-newsletter as the first worked example: its branded
`assets/template.html` against the library's placeholder version.
