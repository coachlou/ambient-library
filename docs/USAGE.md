# Using Ambient Library

Once installed, just use natural language. The runtime wrapper exposes one
`ambient` skill and routes requests to the canonical library automatically.

## Core Commands

### Set up a new project
> "Set up ambient-library in this project"

Enables the project's domain skills by writing `skills-manifest.yaml`.

### Configure skills
> "Configure my skills"
> "Which skills do I need for this project?"
> "Which skills should I have everywhere?"

Walks through a short conversation and writes the manifest for that scope —
the project's `skills-manifest.yaml`, or `~/.aai/skills-manifest.yaml` for every
project.

### Code review
> "Review this code"
> "Code review for src/auth.ts"
> "Check this for security issues"
> "Review the changes in this file"

Returns: summary, findings by severity (critical/major/minor) with file:line references, and suggested fixes. Applies project standards from `CLAUDE.md` automatically if present.

### Update skills
> "Update my skills"

Points you to the runtime's plugin update flow. In Claude Code, that is
`/plugin update ambient`.

### Manage skills
> "Add project-brief to this project"
> "Enable project-brief everywhere"
> "Remove project-brief from this project"
> "What skills are available?"

Enables or disables domain skills in the project's manifest, or in your
user-scope manifest when you say "everywhere" / "globally". Status shows what's
enabled at each scope and what's available but not enabled.

### Writing pipeline

Single stages — each runs on its own:
> "Research the history of espresso"  → researcher (sourced dossier)
> "Draft a post from these notes"     → writer (drafting only)
> "Edit this draft and tighten it"    → editor (surgical edits to an existing draft)

The full pipeline — research → draft → edit, end to end:
> "Write me an 800-word piece on espresso for a coffee-shop audience"

Run the pipeline in its own context (keeps research and draft churn out of this
conversation):
> "Write that piece, but run it in the background"
> "Do the whole pipeline separately"

The router spawns a subagent for the isolated run; the in-context run is the
default.

### One-off skill invocation
> "Use the project-brief skill on this"
> "Run project-brief from the ambient library"

Applies a named library skill to the current request only — even if it isn't
enabled at any scope. Nothing is written to the project; the skill is
active for this conversation, not persisted. To keep a skill permanently, say
*"add <name> to this project"* instead.

### Maintain the library (maintainers)
> "Add a new skill to the library"
> "Update the project-brief skill in the library"
> "Remove project-brief from the library"

Creates, edits, or deletes canonical library assets — catalog, `SKILLS.md`,
and version bumps included. Requires a source clone of ambient-library (it
never edits the installed plugin copy). Note the wording: *"to this project"*
edits your project's manifest; *"to the library"* edits the library itself.

### Grow the library from your work
> "Save this as a skill"
> "Propose a skill from what we just did"

After a task no skill covered, this drafts a new skill **from the session
trace** into `in-progress/` — a proposal, not yet a real skill. It stays
inert (never routed, not in the catalog) until you review it in a clone session:
*"what's in staging?"* lists proposals, *"promote <name>"* moves it into the
library, *"reject <name>"* deletes it. Requires a source clone. If the session
has no real trace to draft from, it declines rather than inventing one.

## How Skills Activate

The `ambient` skill is always available (one description in context per
runtime). Core capabilities (install, select, manage, review) are always
available. Domain skills are opt-in: when a request matches a skill **enabled**
at some scope, the router reads that skill's instructions on demand — nothing
else loads until it's needed. A skill that isn't enabled runs only when you name
it.

## The Manifest

A skill is enabled if it's listed in either manifest, or vendored into the
project's `.ailib/`. The scopes add up — a project gets its own skills plus your
user-scope ones.

| Scope | File |
|---|---|
| Every project | `~/.aai/skills-manifest.yaml` |
| This project | `skills-manifest.yaml` in the project root |

Both use the same format:

```yaml
domain_skills:
  - project-brief  # list the skills this project uses
  - researcher
```

Edit either file directly or say *"configure my skills"* to update it
conversationally. Enabling records a name — the skill still comes from the
library and picks up updates.

## Personalizing a Skill

Some skills need to know things about you — a sender address, a group name,
your brand. Those ship a `contract.yaml` listing what they need with nothing
filled in. The first time you run one it asks, saves your answers in the
project, and never asks again. You never edit the skill's own files; an update
would overwrite them.

Everything you customize lives in the project's `.aai/skills/<skill>/`, which no
update touches. Three tiers — use the first that covers you:

| What you want | File in `.aai/skills/<skill>/` | Keeps getting updates? |
|---|---|---|
| different values | `project.yaml`, `environment.yaml` | yes |
| a few extra rules | `overrides.md` | yes |
| a different skill | `instructions.md` (a fork) | no — you own it |

The two value files split on whether a setting travels. `project.yaml` holds
what belongs to the folder — copy that folder to another machine and the values
should come with it. `environment.yaml` holds what belongs to this machine or
account, and every project beneath it inherits the same file. The skill writes
both for you: say *"change the sender to X"* rather than editing them by hand.

Extra rules you write yourself:

```bash
mkdir -p .aai/skills/writing-team
cat > .aai/skills/writing-team/overrides.md <<'EOF'
- Drafts land in `content/drafts/`, never the repo root.
EOF
```

They're appended to whichever skill body was resolved, so the skill still gets
upstream updates. When a fork or an `overrides.md` is in play, the agent says
so — a silent override makes a skill's behavior impossible to explain later.

**No passwords or API keys go in any of these files.** A value may *name* a
credential — which account alias to send as — but the credential itself stays
in your environment or the relevant MCP server's own config.

## Project-Specific Rules

Add project guidance to your project root to set standards that apply to all
skill operations. Claude Code commonly uses `CLAUDE.md`; Codex commonly uses
`AGENTS.md`.

```markdown
# Project Standards
- All code must have test coverage for new endpoints
- Flag any use of deprecated crypto methods
- We use the Repository pattern throughout
```

The `ambient` adapter merges these rules automatically before executing.

## Questions?

- **Setup issues** → [INSTALLATION.md](INSTALLATION.md)
- **Adding custom skills** → [MANAGEMENT.md](MANAGEMENT.md)
- **Available skills** → [../SKILLS.md](../SKILLS.md)
