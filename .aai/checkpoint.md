# Checkpoint — ambient-library

## Current state
**Next objective:** none queued. Released and tagged **v2.14.2**; `~/.ailib` is
on v2.14.2.

**Parked:**
- AIMM newsletter migration, no test send yet; see the 2026-09-17 section.
- soloFactory `wip/feature-slice-recovery` (commit a097426): local only, never
  pushed. It holds the feature-slice-recovery work.

**Open, Lou's call:**
- gears-* rollout steps 5–6; scrub gears-broadcast's segment ID from history;
  collapse gears-* into one capability.
- Docs gaps from the 2.2.2 review; see the 2026-09-17 section.
- 27 `in-progress/` candidates still unreviewed (`in-progress/CANDIDATES.md`).
- `~/.claude/stats-cache.json` stopped updating at 2026-08-30. Cause not
  investigated.
- `dev-factory` (Downloads/softwareFactoryAlphaTesting): not reinstalled. It
  isn't a git repo, and is probably a stale test install.

---

## 2026-10-08 checkpoint: global coding rules (dev-rules), v2.11.0 → v2.14.2

**Done since last:**
- **dev-rules capability** (`library/dev-rules/`):
  - The authority is `~/.aai/rules/coding.md`; `publish.sh` copies it into the
    library snapshot.
  - `install.sh` adds a coding trigger to `~/.aai/context.md` and points each
    harness's global file at the rules: Claude Code, Codex (or its override
    file), opencode, and DeepSeek Harness.
  - `paste.sh` covers claude.ai chat and Cowork, which can't read files.
  - Lou's merged `coding.md` is published.
- **Rules reach installs and projects:**
  - wbs-toolkit 0.3.0 adds `## Module Boundaries` and module-design checks, and
    lists dev-rules in DEPENDS.
  - soloFactory 0.9.8 and software-dev-factory 0.3.4-alpha list dev-rules in
    DEPENDS and have a template Inputs row for the rules.
  - init-dev-project writes `CLAUDE.md`/`AGENTS.md` pointer files.
  - ambient-folder 1.2.0 appends a `## Coding rules` pointer whenever dev-rules
    is vendored. That runs on every install and refresh, and never edits `.aai/`.
- **Tooling fixes:**
  - `sync-distro.sh` copies committed content via git archive at `--ref`, not
    the working tree. Why: uncommitted WIP and ignored files used to ship.
  - `build-team-index.py` merges `not_for` lists instead of replacing them.
    Why: rebuilds dropped routing; PR #11 restored the lost entries.
  - `release_filter.py` now ships `team-index.yaml`, trimmed to released skills.
    Why: team-build was released without its index.
  - software-dev-factory's plugin version now moves with its package (1.1.0).
- **Projects reinstalled** with the pointer: `photo-library-prototype`,
  `soloFactory/my-folder`. A paused my-folder run resumed fine on 1.7.5.

**Touched:** library/{dev-rules,ambient-folder,init-dev-project,wbs-toolkit,
solofactory,software-dev-factory}/, scripts/{sync-distro.sh,release_filter.py,
build-team-index.py,test_*.py}, library/team-index.yaml, RELEASE.yaml.
PRs #3–#14.

**Open:** none from this work. The cloud session's proxy refuses tag pushes and
branch deletes, so Lou pushes tags from `~/.ailib`.

**Next:** nothing queued.

---

## 2026-09-29 checkpoint

**Done since last:**
- **token-activity-graph brought in through the dev repo** (it had been
  hand-added to `~/.ailib`). Promoted, released, `~/.ailib` restored to clean.
  - 1.0.1: `graph.js` is a pinned fork of bentossell.com's renderer with the
    remote data fetch removed (upstream charts its author's usage when inline
    data is missing). `check-graph.js` is its smoke test.
  - 1.0.2: daily totals are split by each model's lifetime in/out/cache mix
    from `modelUsage`, not a flat 30/70. Why: usage is ~95% cache reads, so
    30/70 priced it ~23× too high ($195,638 vs $8,632 over 43 days).
- **publish-article enabled everywhere** in `~/.aai/skills-manifest.yaml`.
  `admin.md` → Release now ends with step 5: ask where to enable the skill.
  Why: an unlisted domain skill is only reachable by name.
- **Audit warnings cleared.** `TUNED_DESCRIPTIONS` in
  `scripts/audit-distribution.py` records checked SKILL.md/catalog description
  pairs by a hash of both texts; editing either one brings the warning back.
  publish-article, capture-chat, chat-n-build and checkpoint were all
  deliberate tuning, not drift.
- **Housekeeping:** untracked a committed `distro-kit` `.pyc`; `__pycache__/`
  now in the dev `.gitignore`; the build (`scripts/release_filter.py`) writes
  its own `.gitignore` (`.DS_Store`, `__pycache__/`) into the distribution,
  since rsync `--delete` wipes anything added there by hand.
- Versions: wrappers 2.7.1 → 2.7.3. 2.7.2 was reused by two untagged
  republishes; 2.7.3 tags them.

**Touched:** `library/token-activity-graph/`, `library/catalog.yaml`,
`.claude-plugin/marketplace.json`, `SKILLS.md`, `RELEASE.yaml`,
`.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`,
`.aai/skills/admin.md`, `scripts/audit-distribution.py`,
`scripts/release_filter.py`, `.gitignore`, `~/.aai/skills-manifest.yaml`.

**Open:** checkpoint's standalone SKILL.md also claims "what should I work
on", which overlaps Claudio's EA triggers. Harmless inside the library, where
the catalog line routes it; left as-is.

**Next:** nothing in flight. The next release that changes a skill bumps to
2.7.4 (the publish script refuses to tag a version that already exists).

---

## 2026-09-17 checkpoint (former Current state header, kept verbatim)

**Next objective:** none queued — the personalization layer is built,
documented, and released (2.2.2). The AIMM newsletter migration is **parked as work in
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
- Docs audited against the contract layer (2.2.2): the architecture tree now
  shows `contract.yaml`, the resolver, and a project's owned
  `.aai/skills/<skill>/`; `templates/aai/README.md` and
  `docs/CAPABILITY-INSTALL-STANDARD.md` no longer teach forking as the way to
  personalize; the consumer walkthrough moved into `docs/USAGE.md` because the
  release filter drops `MANAGEMENT.md`, so no installed library explained the
  feature; `admin.md` and `MANAGEMENT.md` now carry the four contract rules the
  audit enforces.
- An independent review after 2.2.2 found two live gaps, fixed in 2.2.3: the
  curl one-liner installs from the public dev clone (the release repo is
  private), where the resolver lives only at `scripts/` — so a vendored
  contract capability had no `scripts/resolve.py` and could not start;
  `install.sh` now copies it. And both `instructions.md` templates plus
  `ambient-folder`'s Personalize operation still led with forking, which is the
  one tier that gives up updates.
- Still open from that review: ~9 shipping files link to `docs/MANAGEMENT.md`,
  which the release filter drops (`library/README.md:28` is wrong even in dev);
  several docs say saved answers live in the project, but `environment_file()`
  writes environment keys to `~/.aai/skills/<skill>/` when nothing is vendored
  above; `USAGE.md` tells users to hand-write `overrides.md`; shipped `.aai/`
  files cite `admin.md`, `propose.md`, `build-production.sh` and `in-progress/`,
  none of which ship; `AGENTS.md` says 56 domain skills, the build stages 61.
- Install channel settled (2.3.0): `aai-library` stays **private** — its audience
  is the dozen AIMM members plus Lou, not the public. `bootstrap.sh` is still
  served from the public dev repo (so the documented one-liner is unchanged) but
  now pulls the library tarball from the private release through `gh api`, or
  `GITHUB_TOKEN`/`GH_TOKEN` if `gh` is absent, and exits 2 with instructions when
  neither is there. Two gotchas it encodes: the API tarball's top folder is
  `<owner>-<repo>-<sha>`, not `<repo>-<branch>`, so it is globbed; and a token
  must never be interpolated into the URL or command line. Onboarding a member
  is now: invite to `coachlou/aai-library`, then `gh auth login`.
- Released: dev and distribution repos pushed, `~/.ailib` pulled at 2.3.0.
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
