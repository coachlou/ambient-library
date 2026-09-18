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

## Self-extension (propose → stage → promote)

The library grows from real work without letting unvetted skills degrade
routing. The loop has three stops:

1. **Propose.** After a task no library skill covered, say *"save this as a
   skill"* (or the agent offers). `propose.md` drafts a skill **from the session
   trace** — the actual steps and corrections, not a vague idea — into
   `in-progress/<name>/`, alongside a `PROPOSAL.md` (proposed description,
   source trace, evidence, overlap check). If the session has no real
   trace to author from, it refuses.
2. **Stage.** The proposal is inert: not in the catalog, `SKILLS.md`, or
   marketplace, and never loaded by the router (selection reads only the
   catalog, and `in-progress/` sits outside `library/` entirely). Re-proposing the
   same name appends evidence instead of overwriting — repetition is the
   strongest promotion signal.
3. **Promote.** In a clone session, *"what's in staging?"* lists proposals and
   *"promote <name>"* reviews it against its overlap check, then runs the normal
   create-a-skill steps (catalog, `SKILLS.md`, marketplace, version bumps).
   *"reject <name>"* deletes it.

Why gated rather than auto-committed: self-generated skills underperform unless
authored from real traces and reviewed, and every unvetted catalog description
shifts routing for its neighbors. Staging keeps the learning loop while a human
gate protects catalog quality.

---

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

## Overlays (local customization without forking)

A canonical skill can be adjusted per project **without copying it**, so it
keeps receiving upstream updates. Everything a user customizes lives in the
project's owned `.aai/skills/<skill>/`; canonical copies stay pristine in
`.ailib/` (pinned) or `~/.ailib` (installed), which updates replace wholesale.
Three tiers — values (`project.yaml`, `environment.yaml`), `overrides.md`, and
a full `instructions.md` fork — only the last of which gives up updates. The
user-facing walkthrough is [USAGE.md](USAGE.md#personalizing-a-skill); the rest
of this section is what an author has to do.

`.aai/` lives **outside** the installed library, so an update overwrites
`library/` and `.ailib/` and leaves those files untouched. That's the whole
mechanism — no merge logic, no versioning, no protected paths. The earlier
overlay folders (`<project>/.ambient/<skill>/`, `~/.aai/library/<skill>/`) are
retired; the loader no longer reads them.

All three tiers apply **by canonical name**; they don't add catalog entries.
Authoring a genuinely new skill is still propose → stage → promote above.

---

## Giving a Skill a Contract (opting in to values)

Only needed when a skill can't do its job without something it can't know: a
sender address, a group name, a brand. Without a contract the skill either
hardcodes one user's details or ships `YOUR_GROUP_NAME` placeholders users
hand-edit — and an update overwrites the edit. A skill that needs nothing from
the user should not have a contract.

Four things, all audited by `scripts/audit-distribution.py`:

**1. `library/<name>/contract.yaml`, values left empty.** Canonical ships the
keys and their hints, never a value — a filled value brands every user's copy.

```yaml
environment:        # this machine or account; inherited by projects beneath it
  from_address:     # who the mail comes from
project:            # travels with the project folder
  list_name:        # the audience this folder writes to
state:
  - .aai/memory/<name>/   # paths the skill writes, relative to the project
```

Which class a key belongs in has one test: copy the project folder to another
operator's machine — a value that must travel is `project:`, one that would be
wrong there is `environment:`. In doubt, `project:`. Add `multi: true` only if
one parent folder holds several projects of this skill.

**No secrets.** A value may *name* a credential (which account alias to send
as); the credential itself stays in the environment or the MCP server's config.

**2. Open `instructions.md` with the Project block**, which tells the agent to
run the resolver before acting and again before any write or send, to treat
`{{env.*}}` / `{{project.*}}` as lookups in its output rather than one-time
substitutions, and to state the resolved folder to the user. Copy
`library/aimm-newsletter/instructions.md`'s opening block verbatim and change
nothing but the skill's own steps — the audit requires the literal string
`scripts/resolve.py --start` in the body.

**3. Every placeholder is a contract key.** `{{project.foo}}` with no `foo` in
`contract.yaml` is silently never asked for, so the audit fails the build on it.
Runtime placeholders the skill fills itself (`{{BODY_HTML}}`) are unaffected —
only the `env.`/`project.` namespaces are checked.

**4. Don't commit a copy of `resolve.py`.** There is one source,
`scripts/resolve.py`; the release filter copies it into every skill whose folder
has a `contract.yaml`. A hand copy drifts, and the audit compares them.

Design and rationale: `docs/PLAN-personalization-layer.md`.

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
