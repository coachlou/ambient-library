# Checkpoint — ambient-library

## Current state
**Next objective:** none queued — the personalization layer is built and
released (2.2.1). The AIMM newsletter migration is **parked as work in
progress**: Lou is not using aimm-newsletter right now (sends go through the
resend skill), so the live test was skipped on purpose.

**Parked: AIMM migration (2026-09-17).** Done: project home stamped at
`/Volumes/Extreme Pro/users/loudalo/GitHub/aimm-newsletter` with the live
values (environment in `~/.aai/skills/aimm-newsletter/`); the filled template
matches the branded one; `~/.claude/commands/aimm-send.md` trimmed to point at
the library skill and that folder. Not done: no test send — `advanced-gmail-mcp`
is configured only in Claude Desktop (as `gmail`), not in Claude Code, so
`/aimm-send` cannot send from Code until it is added (`claude mcp add`). The
branded copy in `/Volumes/…/.claude/skills/aimm-newsletter/` stays installed
until a test passes. To resume: add the MCP to Code (or run the skill in
Desktop), send to two of Lou's own addresses, then archive the branded copy.

**Where things stand (2026-09-17):**
- Design: `docs/PLAN-personalization-layer.md` (v4.5). 1:n is an opt-in
  evolution of the standard skill — default stays cwd = workspace; an opted-in
  skill ships `contract.yaml`, and `scripts/resolve.py` decides which project
  folder it is working in and where values are saved. No existing skill
  migrates unless picked.
- Rollout steps 1–4 are done: shared rules, the resolver + 14 tests
  (`python3 scripts/test_resolve.py`), aimm-newsletter converted (v1.1.0), the
  build copies the resolver into opted-in skills, and the audit enforces the
  contract (`python3 scripts/audit-distribution.py --self-test`).
- Released: dev and distribution repos pushed, `~/.ailib` pulled at 2.2.1.
  `v2.2.0` exists but carries 2.1.0 manifests (rsync skipped same-size files;
  the build now uses `--checksum`) — use `v2.2.1`. The build also now drops
  this file from the distribution.

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
