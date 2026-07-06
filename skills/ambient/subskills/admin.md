# admin

CRUD for canonical library assets: domain skills, the catalog, subskills. This
is a maintainer capability — it edits the library itself, not a project.

## CRITICAL: operate on a source clone, never the installed plugin

`${CLAUDE_SKILL_DIR}` is the installed copy; the next plugin update overwrites
it, so edits there silently vanish. Locate the source clone first:

1. If the current project root is an ambient-library clone (has
   `skills/ambient/instructions.md` and `.claude-plugin/plugin.json`), use it.
2. Otherwise ask the user for their clone's path. Do not clone one yourself
   and do not fall back to `${CLAUDE_SKILL_DIR}`.

All paths below are relative to that clone.

## Operations

### List / inspect

Read `skills/ambient/library/catalog.yaml` and show skill names and
descriptions. To inspect one, read its `instructions.md`.

### Create a domain skill

If `skills/ambient/library/<name>/` already exists, **refuse and notify** —
tell the user the skill exists and that saying "update <name>" will overwrite
it. Never overwrite on a create/save request.

1. Gather from the user: kebab-case name, a one-line description of *when it
   applies* (this is the routing trigger — user intent, not implementation),
   and the skill content. Best source is a real task trace or artifact, not a
   vague prompt.
2. Write `skills/ambient/library/<name>/instructions.md`. Sibling files
   (`references/`, `scripts/`) only as needed.
3. Add the one-line entry to `skills/ambient/library/catalog.yaml`.
4. Add a human-readable entry to `SKILLS.md`.
5. Bump `version` in `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json`.

### Update a domain skill

"Update <name>" is itself approval to overwrite the existing skill — no extra
confirmation needed. If the skill doesn't exist, say so and offer to create it
instead. Edit its `instructions.md`; bump wrapper versions. If the **catalog
description** changes, warn the user: descriptions are routing triggers, and a
change can shift routing for neighboring skills — re-test matching before
release.

### Delete a domain skill

Confirm with the user first, then: remove the skill folder, its `catalog.yaml`
line, and its `SKILLS.md` entry; bump wrapper versions.

### Edit core assets (router, subskills, templates)

Same pattern: edit the file in the clone, bump wrapper versions. Be
conservative — every installed copy inherits these on update.

## Releasing

After any change, offer to commit — stage the specific files touched, never
`git add -A`. Never push without the user's explicit say-so. Remind them:
plugin users get the change via their runtime's plugin update flow;
pointer-adapter installs get it on `git pull`.

## Rules

- Source clone only. If you can't locate one, stop and ask — don't improvise.
- One skill, one class of work; catalog descriptions stay one line.
- Create never overwrites; update always may. The user's verb is the consent
  signal. Delete still requires explicit confirmation.
- "Add <skill> to this project" is `manage.md`, not admin — admin changes the
  library, manage changes a project's manifest.
