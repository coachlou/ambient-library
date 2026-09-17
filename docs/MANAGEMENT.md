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
keeps receiving upstream updates. Everything you customize lives in the
project's owned `.aai/skills/<skill>/`; canonical copies stay pristine in
`.ailib/` (pinned here) or `~/.ailib` (installed), which updates replace
wholesale. One folder per owner — nothing an update writes is ever yours.

Three tiers, cheapest first:

| Tier | File in `.aai/skills/<skill>/` | Keeps upstream updates? |
|------|-------------------------------|-------------------------|
| values | `project.yaml`, `environment.yaml` | yes |
| extra rules | `overrides.md` | yes |
| fork | `instructions.md` (the whole skill) | no — you own it |

**Values** exist only for skills that ship a `contract.yaml`. The skill's own
`scripts/resolve.py` asks for them once and saves them in the right file; don't
hand-place them. Design: `docs/PLAN-personalization-layer.md`.

**`overrides.md` — appended to whichever body resolved. Keeps upstream updates.**
This is the case worth reaching for. Adding a few project rules no longer
requires owning the whole skill:

```bash
mkdir -p .aai/skills/writing-team
cat > .aai/skills/writing-team/overrides.md <<'EOF'
# Project rules
- Drafts land in `content/drafts/`, never the repo root.
- House style: no em-dashes in headings.
EOF
```

**`instructions.md` — full replacement. You own it; no more updates.**
Only when the canonical skill is genuinely wrong for you (`lifecycle.md` →
Personalize).

`.aai/` lives **outside** the installed library, so an update overwrites
`library/` and `.ailib/` and leaves your files untouched. That's the whole
mechanism — no merge logic, no versioning, no protected paths. The earlier
overlay folders (`<project>/.ambient/<skill>/`, `~/.aai/library/<skill>/`) are
retired; the loader no longer reads them.

All three tiers apply **by canonical name**; they don't add catalog entries.
Authoring a genuinely new skill is still propose → stage → promote above.

When a fork or `overrides.md` is in play, the agent says so. A silent override is what
makes a skill's behavior impossible to explain later.

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
