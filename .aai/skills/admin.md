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

## What you say, and what it means

You do not need to remember any command or flag. Match the request to a row and
run the command yourself — never make the user type it, and never ask them
which script they meant.

| The user says | Run | Notes |
|---|---|---|
| "start a new skill", "I want to build X", "new capability" | create `in-progress/<name>/` | Never straight into `library/`. Work in flight is not a library skill. |
| "what am I working on", "what's in flight", "what's unfinished", "what's still open", "where did I leave off" | `ls in-progress/` + read its README "Currently here" | |
| "this is ready", "promote it", "move it into the library", "add it to the canonical library" | `bash scripts/promote.sh <name>` | Run `--dry-run` first and show them the plan. Then do the catalog/marketplace/SKILLS steps it prints — do not hand that list back as homework. |
| "I'm reworking X", "make a new version of X" | copy `library/<name>/` to `in-progress/<name>/` | The live one keeps serving production while they work. |
| "ship it", "release it", "make it available", "push it to production", "deploy" | add to `RELEASE.yaml` → `bash scripts/build-production.sh` | Commit and push first — the build reads `HEAD`, so uncommitted work silently will not ship. Say so if the tree is dirty. |
| "what would change if I deploy", "preview the release" | `bash scripts/build-production.sh --dry-run` | Writes nothing. |
| "pull it back", "unrelease", "stop shipping X", "remove from production" | delete its line in `RELEASE.yaml` → rebuild | It stays in the library. Folders that already vendored it keep their copy. |
| "what's released", "what do folders actually get" | read `RELEASE.yaml` | Not `catalog.yaml` — that is everything in the library, released or not. |
| "is anything broken", "check the library", "did I miss a file" | `python3 scripts/audit-distribution.py` | Exit 0 = no drift. |
| "test the whole flow", "does self-extension still work" | `bash scripts/validate-self-extension.sh` | Cleans up after itself, including on failure. |
| "throw it away", "abandon X" | delete `in-progress/<name>/` | Nothing references it. |
| "update X", "change X's instructions" | edit `library/<name>/` directly | Small edits do not need the in-progress round trip. Bump the version; production is stale until rebuilt. |
| "delete the X skill" | `admin.md` → **Delete a domain skill** | Confirm first. Four files to remove, plus `RELEASE.yaml` if released. |

**A phrasing not in this table is still this table's job.** These are examples,
not an allowlist. If the request is about the library itself — building,
promoting, releasing, deploying, or its status — pick the closest row and run
it. Say what you matched. Never answer "that isn't a supported command."

**Two things that are always separate, no matter how it is phrased:**
promoting into the library is not releasing, and releasing is not deploying
until the build runs. If a request bundles them ("finish X and ship it"), do
each step and say which ones happened.

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

### Promote from in-progress into the library

`scripts/promote.sh <name>` — checks the four-file contract before moving
anything, moves `in-progress/<name>/` to `library/<name>/`, and prints what is
left to do. `--dry-run` shows the plan without moving.

**Reworking a live capability is the normal case.** You can develop a new
version in `in-progress/<name>/` while the old one stays in `library/` and
keeps serving production. On promote, the script detects the replacement, shows
the version delta and a file-level diff, warns if the version was not bumped,
and — if the skill is in `RELEASE.yaml` — tells you production is now stale.

It deliberately does not commit, push, or deploy. Promotion and release are
separate decisions, and so is the moment you ship:

    in-progress/  --promote-->  library/  --commit+push-->  canonical
                                          --RELEASE.yaml + build--> production

Production keeps serving the previous version until you rebuild. That is a
feature: a promoted capability can sit in the canonical library through as many
sessions as you like before it reaches anyone's folder.

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

`in-progress/` holds skills drafted from real task traces by
`propose.md` — inert until promoted here. To list them, read each
`in-progress/*/PROPOSAL.md` and show the proposed description and source
trace.

To promote `<name>`:

1. Read `in-progress/<name>/instructions.md` and its `PROPOSAL.md`. Sanity-
   check the instructions against the proposal's overlap check — if an existing
   skill already covers it, say so and recommend rejecting instead.
2. Present the proposal summary and get an explicit go-ahead.
3. Move `in-progress/<name>/` to `library/<name>/` and delete its
   `PROPOSAL.md`. Then run the **Create a domain skill** steps 3–9 above,
   using the proposal's description as the catalog line. A staged proposal
   carries only `instructions.md`, so `SKILL.md`, `plugin.json`, and the
   marketplace entry are all still missing at this point.

To reject `<name>`: confirm, then delete `in-progress/<name>/`. Nothing
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
