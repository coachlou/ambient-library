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
> "Add code-review to this project"
> "Remove code-review from this project"
> "What skills are available?"

Adds or removes domain skills from the project's manifest and confirms.

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
  - code-review
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
