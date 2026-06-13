# Using Ambient Library

Once installed, just use natural language. The `ambient` skill is always active and routes requests automatically.

## Core Commands

### Set up a new project
> "Set up ambient-library in this project"

Ensures the library is current on your machine and walks you through manifest configuration.

### Configure skills
> "Configure my skills"
> "Which skills do I need for this project?"
> "Update my skill manifest"

Walks through a short conversation about your project and writes a minimal `skills-manifest.yaml`.

### Code review
> "Review this code"
> "Code review for src/auth.ts"
> "Check this for security issues"
> "Review the changes in this file"

Returns: summary, findings by severity (critical/major/minor) with file:line references, and suggested fixes. Applies project standards from `CLAUDE.md` automatically if present.

### Update skills
> "Update my skills to the latest version"
> "Refresh my skills"

Pulls latest from ambient-library and reloads the manifest for the current session.

### Manage skills
> "Add code-review to this project"
> "Remove code-review from this project"
> "What skills are active?"

Adds or removes skills from the manifest and confirms the change.

## How Skills Activate

At the start of every Claude Code session, `ambient` silently reads `skills-manifest.yaml` and loads the listed domain skills into context. You don't do anything — it just happens.

Domain skills add project-specific instructions. Core skills (install, select, manage, review) are always available regardless of the manifest.

## The Manifest

`skills-manifest.yaml` lives in your project root. It's the only file the system needs:

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

The `ambient` skill merges these rules automatically before executing any subskill.

## Questions?

- **Setup issues** → [INSTALLATION.md](INSTALLATION.md)
- **Adding custom skills** → [MANAGEMENT.md](MANAGEMENT.md)
- **Available skills** → [../SKILLS.md](../SKILLS.md)
