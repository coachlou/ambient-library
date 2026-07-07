# Using Ambient Library

Once installed, just use natural language. The runtime wrapper exposes one
`ambient` skill and routes requests to the canonical library automatically.

## Core Commands

### Set up a new project
> "Set up ambient-library in this project"

Scopes the project's domain skills and writes an optional `skills-manifest.yaml`.

### Configure skills
> "Configure my skills"
> "Which skills do I need for this project?"

Walks through a short conversation about your project and writes `skills-manifest.yaml`.

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
> "Remove project-brief from this project"
> "What skills are available?"

Adds or removes domain skills from the project's manifest and confirms.

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
in the project's manifest. Nothing is written to the project; the skill is
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
trace** into `library/_staging/` — a proposal, not yet a real skill. It stays
inert (never routed, not in the catalog) until you review it in a clone session:
*"what's in staging?"* lists proposals, *"promote <name>"* moves it into the
library, *"reject <name>"* deletes it. Requires a source clone. If the session
has no real trace to draft from, it declines rather than inventing one.

## How Skills Activate

The `ambient` skill is always available (one description in context per
runtime). When a request matches a domain skill, the router reads that skill's
instructions on demand — nothing else loads until it's needed. Core capabilities
(install, select, manage, review) are always available regardless of the
manifest.

## The Manifest

`skills-manifest.yaml` lives in your project root. It's optional and scopes which
domain skills the router considers:

```yaml
domain_skills:
  - project-brief  # list the skills this project uses
  - researcher
```

Edit it directly or say *"configure my skills"* to update it conversationally.

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
