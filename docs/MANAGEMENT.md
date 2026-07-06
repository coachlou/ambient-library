# Managing Skills

Everything below can also be done conversationally: in a session inside your
ambient-library clone, say *"add a new skill to the library"*, *"update the
<name> skill"*, or *"remove <name> from the library"*. The admin flow scaffolds
the folder, updates the catalog and `SKILLS.md`, and bumps wrapper versions —
the same steps documented here. It only operates on a source clone, never on
the installed plugin.

## Adding a Domain Skill

Domain skills are project-specific capabilities the router reads on demand. They
live in the canonical library under `library/` and cost nothing
in context until used. Runtime wrappers for Claude Code and Codex both delegate
to this same library.

### 1. Create the skill folder

In your clone of this repo:

```bash
mkdir -p library/my-skill
```

### 2. Write instructions.md

`library/my-skill/instructions.md` holds the skill logic:

```markdown
# My Skill

What this skill does, and when it applies.

## Instructions

Step-by-step instructions for the agent...
```

It may include sibling files (`references/`, `scripts/`) — they ship with the
plugin and resolve relative to the skill folder. Keep it focused: one skill, one
class of work.

### 3. Register it in the catalog

Add a one-line entry to `library/catalog.yaml`:

```yaml
skills:
  my-skill: One-line description of when this skill applies.
```

This is the **only** file the router reads to choose a skill, so the description
must be enough to match a request without opening the skill body. Keeping it to
one line is what prevents context bloat — the router reads this catalog, picks one
skill, and loads only that skill's `instructions.md`. Also add a fuller entry to
`SKILLS.md` for human readers.

### 4. Bump wrapper versions and release

Edit each affected runtime manifest, bump `version`, then commit and push:

- `.claude-plugin/plugin.json`
- `.codex-plugin/plugin.json`

```bash
git add library/my-skill SKILLS.md .claude-plugin/plugin.json .codex-plugin/plugin.json
git commit -m "Add my-skill domain skill"
git push
```

Users receive it on their runtime's next plugin update.

### 5. Activate in a project

Add it to the project's `skills-manifest.yaml`, or from your agent:
*"Add my-skill to this project"*.

---

## Updating a Domain Skill

Edit `library/my-skill/instructions.md`, bump affected wrapper
versions, commit, push. Users pull it with their runtime's plugin update flow.

---

## Removing a Domain Skill

```bash
git rm -r library/my-skill
# remove its SKILLS.md entry, bump wrapper plugin versions
git commit -m "Remove my-skill"
git push
```

If the skill belongs to any bundle in `bundles/`, remove its symlink there too.

---

## Namespaces

Related skills are grouped into logical namespaces in the catalog's
`namespaces:` map (currently: `writing`, `thinking`, `sessions`, `audit`).
Namespaces are **logical only** — skill folders stay flat under `library/`.
They give the router family-level disambiguation and let a project's
`skills-manifest.yaml` scope in a whole family:

```yaml
namespaces:
  - writing
```

**Design decision (recorded 2026-07-06): logical now, structural later.**
Two implementation depths were considered:

- *Logical* (current): a grouping map in catalog.yaml. Cheap, no moves,
  no routing changes.
- *Structural*: `library/<namespace>/` as a mid-level agentic folder with its
  own `instructions.md` and `catalog.yaml`, skills nested inside. This is the
  recursive agentic-folder framework applied one level down.

**Promotion criterion — when to convert a namespace to structural form:**
the moment a family needs *shared behavior* — e.g. "all writing skills load
Lou's voice profile" or "all AIMM commands cite their source session." That
shared rule needs a home, and the home is the namespace folder's own
`instructions.md`. Until a family needs shared behavior, structural nesting
is organization without function — don't do it. Converting costs: folder
moves, marketplace source-path regeneration, two-hop routing in the router,
and new trigger evals for the namespace-level catalog entries.

Membership changes are one-line edits to the `namespaces:` map. A skill may
belong to at most one namespace; skills outside every namespace are fine.

## Bundles

A bundle is a meta-plugin: one marketplace install that registers a set of
library skills. It contains no skill content — only symlinks, which Claude Code
dereferences (copies content) at install time because they resolve within the
same marketplace.

```bash
mkdir -p bundles/my-bundle/.claude-plugin bundles/my-bundle/skills
cd bundles/my-bundle/skills
ln -s ../../../library/skill-a skill-a
ln -s ../../../library/skill-b skill-b
```

Add `bundles/my-bundle/.claude-plugin/plugin.json` (name, description, version)
and a marketplace entry with `"source": "./bundles/my-bundle"`. Every bundled
skill registers its description on install — bundles trade standing context for
reliable direct triggering, the same tradeoff as à-la-carte installs, in sets.
Pair each bundle with its orchestrator skill where one exists (writing-suite
includes writing-team).

---

## Updating Core Subskills

The canonical router (`instructions.md`) and its subskills (`skills/`) live in
`.aai/` at the repo root. Edit, bump affected wrapper versions, commit, push.
Users get changes through their runtime's plugin update flow.

---

## Local Development

Test Claude Code changes without publishing using `--plugin-dir`:

```bash
claude --plugin-dir /path/to/ambient-library
```

Run `/reload-plugins` to pick up edits without restarting. Validate before
publishing:

```bash
claude plugin validate /path/to/ambient-library
```

Validate the Codex wrapper with the Codex plugin validator before publishing or
installing it as a Codex plugin.

---

## Best Practices

**One skill, one class of work.** Split anything that grows too broad.

**Describe when it applies.** Start `instructions.md` with the trigger conditions
and purpose so the router knows when to read it.

**Test before releasing.** Exercise each runtime wrapper in a real session before
bumping the version.

**Bump the version.** Users only get updates when the runtime manifest's
`version` changes (or, if unset, on every commit when installed from git).
