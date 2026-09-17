# Promotion candidates

Things found outside the library during the 2026-09-16 compliance cleanup that
may deserve a place in it. Nothing here is routable. Promote via `admin.md`
("create a domain skill") after review, or delete the line.

Provenance rule used while reconciling: a skill with `library/<name>/app/VERSION`
is synced FROM an app repo by `scripts/sync-distro.sh` (solofactory,
software-dev-factory, wbs-toolkit today) — the app repo is its source of truth
and its app-side copy is never touched. Everything else is authored here.

| Candidate | Where it is now | Why it might belong |
|---|---|---|
| capability-architect | archive/2026-09-16-library-cleanup/ailibrary-cleanslate-2026-06/skills/ | June 2026 CleanSlate skill; designs skills — overlaps admin.md, check before promoting |
| inference-router | same | model/effort routing as a reusable skill |
| letsgo | same | unknown — read before deciding |
| wbs-prd | same | may be superseded by wbs-toolkit (synced) |
| writing-team-orchestrator | same | may be superseded by writing-team |
| curate | in-progress/aai-library-rescue/curate.md | old distro's "create a local canonical library" — partly what ~/.ailib now is |
| aai-setup / library-admin commands | in-progress/aai-library-rescue/commands/ | old distro slash commands |
| test-validation-skill | in-progress/aai-library-rescue/_staging/ | old staged proposal |
| nugget-mining | all-ai-chats-archives/nugget-mining/.aai/skills/nugget-mining/ | owned pilot skill with evals and scripts; portable across topics per its own README |
| okf-management | /Volumes/Extreme Pro/users/loudalo/GitHub/OKF/.aai/skills/okf-management/ | source of truth (reconciled 2026-09-16; aimm-shared-repo/AAI-Folders/okf mirrors it). Promote from here |

## Own skills imported from user scope (2026-09-16)

Copied, not moved, from user-scope skill folders; the originals stay installed
until each one is released. Review, then
`scripts/promote.sh <name>` and add it to `RELEASE.yaml`, or delete the folder.
Before promoting, strip anything private — the library is public.

| Candidate | Copied from | Review notes |
|---|---|---|
| ea | ~/.claude/skills | /ea persona (Claudio); slash-invoked |
| ed | ~/.claude/skills | /ed persona (editor-in-chief); slash-invoked |
| evaluate-article | ~/.claude/skills | needs the `article-evaluator` agent from ~/.claude/agents |
| fixedness-audit | ~/.claude/skills | |
| context-hygiene-sweep | ~/.claude/skills | |
| gears-content | ~/.claude/skills | local only (gitignored): production Supabase project and client data throughout |
| gears-init | ~/.claude/skills | local only (gitignored): same as gears-content |
| gears-onboard | ~/.claude/skills | local only (gitignored): same as gears-content |
| okf | ~/.claude/skills | check against the okf-management candidate above |
| skunny | ~/.claude/skills | personal trading method |
| create-skill | ~/.claude/skills | modified from Anthropic's skill-creator; keep `LICENSE.txt` (Apache 2.0) and note the changes |
| compile-skill | /Volumes/.../.claude/skills | overlaps create-skill and admin.md |
| deep-research | ~/.agents/skills | newer than the /Volumes copy |
| design-course | ~/.agents/skills | newer than the /Volumes copy |
| dynamic-writing-team | /Volumes/.../.claude/skills | `evolution/` holds run logs — drop before promoting |
| gic-leap | /Volumes/.../.claude/skills | local only (gitignored): personal portfolio app |
| haiku-article | /Volumes/.../.claude/skills | same in ~/.agents/skills |
| ideal-client-generator | /Volumes/.../.claude/skills | same in ~/.agents/skills |
| sakana-writing-team | /Volumes/.../.claude/skills | `.skill` zips left out |
| skillify | ~/.agents/skills | newer than the /Volumes copy |
| strategic-compass | /Volumes/.../.claude/skills | |
| teaching-block | ~/.agents/skills | newer; `teaching-block-workspace` (eval runs) not copied |
| topic-aar-controller | /Volumes/.../.claude/skills | pairs with topic-aar-worker |
| topic-aar-worker | /Volumes/.../.claude/skills | |
| weekly-intelligence-briefing | /Volumes/.../.claude/skills | reads your own sessions |
| zoom-mastermind-recap | ~/Downloads/zoom-recap-sandbox (via symlink) | AIMM-specific |
| angela | ~/Documents/Codex/2026-08-12/... (via ~/.codex/skills symlink) | |
| aimm-newsletter | /Volumes/.../.claude/skills (still installed there) | Rework of the released skill: this copy carries your branding (AI Leaders Mastermind, Successpod), which the library version replaced with placeholders. Don't switch to the library version until the personalization split below exists; then move the branding into the personal layer. |

## Library-wide follow-up: separate canonical structure from personalization

Canonical skills should ship generic logic and defaults only. Personal data
(branding, email templates, account and contact-group names, voice, client
settings) belongs in a personal layer that the skill reads when present, so
updating from the library never overwrites it and the public library never
carries it. Today the only option is forking the whole skill
(`.aai/skills/<name>/`), which stops it picking up library updates.

Direction to design (not built):
- a fixed override location per skill at user and project scope (for example
  `~/.aai/skills/<name>/` and `<project>/.aai/skills/<name>/`, holding only
  the overridden files), checked before the skill's own `assets/`
- a documented list in each skill of which files are overridable
- the placeholder convention the library already uses in
  `aimm-newsletter/assets/template.html` as the default

First users: aimm-newsletter (branded template), gears-broadcast, and the
GEARS and gic-leap candidates, whose private data is why they are gitignored.

## Follow-ups outside this repo

- solofactory and software-dev-factory `distro/templates/aai/` should emit GEMINI.md and
  the lookup-order paragraph (edit in the app repos, then `scripts/sync-distro.sh`).
- software-dev-factory `scripts/build-distro.mjs` bundles (`distro/dev`, `distro/v0.x`) vendor
  `.ailib/factory/` without a manifest.yaml; the SDF project generator writes an app-test
  launcher that hardcodes a deleted absolute path (see dev-factory/projects/app-test-1).
- dynamic-company-builder uses `.ailib/manifest.json`, not `manifest.yaml`. The duplicate
  `-agent-organization` folder was archived 2026-09-16 (its one unique file, the requirements
  doc, was copied into the kept folder first).
- Worktrees on other branches (`~/.grok/worktrees/github-software-dev-factory/*`,
  `all-ai-chats-archives/.worktrees/editorial-studio`) inherit compliance when their
  branches rebase onto main; not edited directly.
- `deepseek-harness-master/wip` uses `.aai/conversation/` as a design experiment, not as an
  ambient folder; its docs reference the path, so it was left as is.
