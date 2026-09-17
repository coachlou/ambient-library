# Checkpoint — ambient-library

## Current state
**Next objective:** design the personalization override layer. The work was
interrupted before any design was written. Start from the "Library-wide
follow-up" section in `in-progress/CANDIDATES.md`.

**Where things stand (2026-09-16):**
- v2.1.0 is released: domain skills are opt-in per scope. The dev repo
  (`ambient-library`) and the distribution repo (`aai-library`) are pushed, and
  `~/.ailib` has been pulled.
- User-scope skill cleanup is finished. Your own skills are waiting in
  `in-progress/`; the originals stay installed until each one is released.
- The working tree is clean and everything is pushed (last commit `eb37efc`).

**Open questions for the design:**
- Where do overrides live? The draft is `~/.aai/skills/<name>/` for all
  projects and `<project>/.aai/skills/<name>/` for one project, but
  `.aai/skills/<name>/` is already used for whole-skill forks.
- How does a skill say which of its files can be overridden?
- How do placeholders get their values: whole-file replacement, or
  placeholders plus a values file?
- Which lookup files and scripts need to change? Probably
  `.aai/skills/load.md`, `.aai/skills/lifecycle.md`, and
  `scripts/audit-distribution.py`.

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
