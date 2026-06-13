# Using Ambient Library

Once installed, just use natural language. The `ambient` skill is always active and routes requests automatically.

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

Points you to `/plugin update ambient`, which pulls the latest plugin version.

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

## How Skills Activate

The `ambient` skill is always available (one description in context). When a
request matches a domain skill, the router reads that skill's instructions on
demand — nothing else loads until it's needed. Core capabilities (install,
select, manage, review) are always available regardless of the manifest.

## The Manifest

`skills-manifest.yaml` lives in your project root. It's optional and scopes which
domain skills the router considers:

```yaml
domain_skills:
  - project-brief
  # add more domain skills here
```

Edit it directly or say *"configure my skills"* to update it conversationally.

## Project-Specific Rules

Add a `CLAUDE.md` to your project root to set standards that apply to all skill operations:

```markdown
# Project Standards
- All code must have test coverage for new endpoints
- Flag any use of deprecated crypto methods
- We use the Repository pattern throughout
```

The `ambient` skill merges these rules automatically before executing.

## Questions?

- **Setup issues** → [INSTALLATION.md](INSTALLATION.md)
- **Adding custom skills** → [MANAGEMENT.md](MANAGEMENT.md)
- **Available skills** → [../SKILLS.md](../SKILLS.md)
