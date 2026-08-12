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

## Which clone am I in?

**Check whether `.aai/PRODUCTION` exists in this folder.** That file, and only
that file, decides this clone's role — this pointer is byte-identical in both,
so it cannot tell you on its own.

| `.aai/PRODUCTION` | Role | Authoring |
|---|---|---|
| absent | dev workspace | allowed — `admin.md`, `propose.md` |
| present | production; folders install and vend from it | refused |

Author in a clone without the marker. Adding or editing a library skill goes
through
`.aai/skills/admin.md`, which writes all four files a skill needs to be both
routable and installable — skill dir, `.claude-plugin/plugin.json`, a
`library/catalog.yaml` line, and a `.claude-plugin/marketplace.json` entry.
Touching the catalog alone leaves a skill the router can pick and nobody can
install.

Verify with `python3 scripts/audit-distribution.py` — exit 0 means no drift.

Production updates by `git pull`. Both clones stay byte-identical in git; the
marker is gitignored, so the role is local to each clone.

## Do not develop in the copy

`agentic-ambient-intelligence/canonical-library/` (repo `coachlou/aai-framework`)
contains an `rsync` copy of `library/`. It has no router, no `admin.md`, and no
marketplace, so nothing committed there is installable. Five skills were lost
that way between 2026-07-16 and 2026-08-10. See that folder's `MOVED.md`.
