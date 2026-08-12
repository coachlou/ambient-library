# admin

CRUD for canonical library assets: domain skills, the catalog, subskills. This
is a maintainer capability — it edits the library itself, not a project.

## CRITICAL: operate on a source clone, never the installed plugin

`${CLAUDE_PLUGIN_ROOT}` is the installed copy; the next plugin update overwrites
it, so edits there silently vanish. Locate the source clone first:

1. If the current project root is an ambient-library clone (has
   `.aai/instructions.md` and `.claude-plugin/plugin.json`), use it.
2. Otherwise ask the user for their clone's path. Do not clone one yourself
   and do not fall back to `${CLAUDE_PLUGIN_ROOT}`.

All paths below are relative to that clone.

## Three stages, three promotions

| Stage | Where | Reachable | Ships |
|---|---|---|---|
| in progress | `in-progress/<name>/` | no | no |
| in the library | `library/<name>/` + catalog line | yes, here | no |
| released | named in `RELEASE.yaml` | yes | yes |

Work being figured out belongs in `in-progress/` — nothing there is catalogued,
so the router cannot reach it and no folder can install it. Promote it into
`library/` with **Create a domain skill** below only once it works. See
`in-progress/README.md`.

## Authoring does not release

Creating a skill makes it exist in the dev workspace. It does **not** reach
production. Production is built from `RELEASE.yaml` by
`scripts/build-production.sh`, and a skill not named there does not ship.

This is deliberate: a skill should be exercised on real work before folders
start installing it. Create, use, then release — see **Release a skill** below.

## Four files, not one

A skill is **routable** when it is in `library/catalog.yaml` — that is all the
router needs. It is **distributable** only when it also has `SKILL.md`,
`.claude-plugin/plugin.json`, and a `marketplace.json` entry, which is what lets
someone install it standalone. Touching the catalog alone leaves a skill the
router can pick and nobody can install; nine skills drifted that way before this
was written down. Every create, update, and delete below touches all four.

Descriptions: the `plugin.json` and `marketplace.json` descriptions are display
metadata and must be the catalog line **verbatim**. The `SKILL.md` description
is a live routing trigger for the standalone install — it may legitimately be
longer or tuned differently, because there it competes against every skill the
user has rather than 47 siblings.

Verify with `python3 scripts/audit-distribution.py` (exit 0 = no drift).

## Operations

### List / inspect

Read `library/catalog.yaml` and show skill names and
descriptions. To inspect one, read its `instructions.md`.

### Create a domain skill

If `library/<name>/` already exists, **refuse and notify** —
tell the user the skill exists and that saying "update <name>" will overwrite
it. Never overwrite on a create/save request.

1. Gather from the user: kebab-case name, a one-line description of *when it
   applies* (this is the routing trigger — user intent, not implementation),
   and the skill content. Best source is a real task trace or artifact, not a
   vague prompt.
2. Write `library/<name>/instructions.md`. Sibling files
   (`references/`, `scripts/`) only as needed. Inside `instructions.md`,
   reference siblings as `${CLAUDE_PLUGIN_ROOT}/library/<name>/<file>` — never
   repo-relative or absolute paths — so the skill works from both the
   installed plugin and a pointer-adapter clone.
3. Write `library/<name>/SKILL.md` — frontmatter `name:` (must equal the folder
   name) and `description:`, then the two standard body paragraphs. Copy a
   sibling's exactly; the path note is what makes a standalone install resolve
   `${CLAUDE_PLUGIN_ROOT}` paths correctly.
4. Write `library/<name>/.claude-plugin/plugin.json` — `name`, `description`,
   `version` (start at `1.0.0`), and the `author`/`homepage`/`repository`/
   `license` block copied from a sibling.
5. Add the one-line entry to `library/catalog.yaml`.
6. Add the `.claude-plugin/marketplace.json` plugin entry: `name`,
   `source` `./library/<name>`, `description` matching the catalog line.
   Entries sort by name after the leading `ambient` entry.
7. Add a human-readable entry to `SKILLS.md`.
8. Bump `version` in `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json`.
9. Run `python3 scripts/audit-distribution.py` and confirm it exits 0.

### Release a skill to production

Only after the skill has been exercised on real work. Releasing an untested
skill is how a library accumulates capabilities nobody trusts.

1. Confirm it is complete: `python3 scripts/audit-distribution.py` exits 0.
2. Add its name to the `skills:` list in `RELEASE.yaml`, alphabetically. One
   line. This edit is the release decision and should read as one in the diff.
3. Preview: `scripts/build-production.sh --dry-run`. Nothing is written; you
   see exactly which files would land.
4. Build: `scripts/build-production.sh`.

The build refuses if the audit fails, if `RELEASE.yaml` names a skill that
does not exist or is not in the catalog, or if it is run from a clone marked
`.aai/PRODUCTION`. It builds from `HEAD`, never the working tree, so an
uncommitted edit cannot ship — commit first.

**Unreleasing** is the same edit in reverse: delete the line, rebuild. The
build uses `rsync --delete`, so the skill disappears from production. Folders
that already vendored it into their `.ailib/` keep their copy until they
re-sync — vendored copies are theirs, by design.

### Promote a staged proposal

`library/_staging/` holds skills drafted from real task traces by
`propose.md` — inert until promoted here. To list them, read each
`library/_staging/*/PROPOSAL.md` and show the proposed description and source
trace.

To promote `<name>`:

1. Read `library/_staging/<name>/instructions.md` and its `PROPOSAL.md`. Sanity-
   check the instructions against the proposal's overlap check — if an existing
   skill already covers it, say so and recommend rejecting instead.
2. Present the proposal summary and get an explicit go-ahead.
3. Move `library/_staging/<name>/` to `library/<name>/` and delete its
   `PROPOSAL.md`. Then run the **Create a domain skill** steps 3–9 above,
   using the proposal's description as the catalog line. A staged proposal
   carries only `instructions.md`, so `SKILL.md`, `plugin.json`, and the
   marketplace entry are all still missing at this point.

To reject `<name>`: confirm, then delete `library/_staging/<name>/`. Nothing
else changes.

### Update a domain skill

"Update <name>" is itself approval to overwrite the existing skill — no extra
confirmation needed. If the skill doesn't exist, say so and offer to create it
instead. Edit its `instructions.md`; bump the skill's own
`library/<name>/.claude-plugin/plugin.json` `version` as well as the wrapper
versions. If any distribution file is missing, add it now per the create steps
above — an update is the cheapest moment to close the gap.

If the **catalog description** changes, warn the user: descriptions are routing
triggers, and a change can shift routing for neighboring skills — re-test
matching before release. Then re-sync it into the skill's `plugin.json` and its
`marketplace.json` entry (verbatim), and decide deliberately whether `SKILL.md`
should follow — that one is the standalone install's trigger, so changing it is
its own routing decision.

Finish by running `python3 scripts/audit-distribution.py`.

### Delete a domain skill

Confirm with the user first, then: remove the skill folder (which takes its
`SKILL.md` and `plugin.json` with it), its `catalog.yaml` line, its
`marketplace.json` entry, and its `SKILLS.md` entry; bump wrapper versions. A
left-behind marketplace entry points at a missing source and breaks the
marketplace for every skill in it, so run
`python3 scripts/audit-distribution.py` to confirm nothing dangles.

### Create or edit a bundle

A bundle (`bundles/<name>/`) is a meta-plugin installing a set of library
skills via symlinks — see docs/MANAGEMENT.md "Bundles" for the layout. Create
the symlinked `skills/` dir, the bundle's plugin.json, and a marketplace.json
entry with source `./bundles/<name>`. Same verb rules as skills: create
refuses if the bundle exists; "update" overwrites.

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
