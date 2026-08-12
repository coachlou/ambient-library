# ambient-library

This folder is ambient. Its behavior lives in `.aai/`.

**Read `.aai/instructions.md` and follow it.** That file routes the request to
one subskill in `.aai/skills/` and tells you how to load domain skills from
`library/`. Do not guess the routing — read it first.

Start with `.aai/context.md` if you need the folder's layout before routing.

## What this repo is

The canonical capability library — 56 domain skills in `library/`, plus the
`.aai`/`.ailib` ambient-folder scaffold it stamps into other folders. It ships
thin plugin wrappers for Claude Code (`.claude-plugin/`) and Codex
(`.codex-plugin/`), but the library is plain files and works without either.

## Say it plainly; the router picks the command

`.aai/skills/admin.md` opens with a phrasebook mapping ordinary requests —
"ship it", "promote this", "what am I working on", "pull it back" — to the
right command. Read that table before reaching for a script, and run the
command rather than telling the user to.

## Dev workspace or production build?

**Check whether `.aai/PRODUCTION` exists here.**

| `.aai/PRODUCTION` | What this is | Authoring |
|---|---|---|
| absent | the dev workspace — the source | yes: `admin.md`, `propose.md` |
| present | a build output folders install from | no — those files aren't here |

**Production is built, not cloned.** `scripts/build-production.sh` reads
`RELEASE.yaml`, copies only the skills named there, drops the authoring
subskills and maintainer docs, and `rsync --delete`s the result into the
production folder. So:

- Committing a skill does **not** ship it. Releasing is a separate, deliberate
  edit to `RELEASE.yaml`.
- The build runs from `HEAD`, never the working tree — an uncommitted edit
  cannot ship.
- Unrelease by deleting the line and rebuilding.
- Preview any release with `scripts/build-production.sh --dry-run`.

Adding or editing a skill goes through `.aai/skills/admin.md`, which writes all
four files a skill needs to be routable and installable — skill dir,
`.claude-plugin/plugin.json`, a `library/catalog.yaml` line, and a
`.claude-plugin/marketplace.json` entry. Verify with
`python3 scripts/audit-distribution.py` (exit 0 = no drift).

## Do not develop in the copy

`agentic-ambient-intelligence/canonical-library/` (repo `coachlou/aai-framework`)
contains an `rsync` copy of `library/`. It has no router, no `admin.md`, and no
marketplace, so nothing committed there is installable. Five skills were lost
that way between 2026-07-16 and 2026-08-10. See that folder's `MOVED.md`.
