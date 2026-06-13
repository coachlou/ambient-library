# Skills Catalog

## Core Skills (always available globally)

These are built into the `ambient` skill and available in every session. You don't add them to your manifest.

| Subskill | What it does | How to invoke |
|----------|-------------|---------------|
| **load** | Reads `skills-manifest.yaml` at session start, activates domain skills | Automatic — runs silently every session |
| **install** | Sets up ambient-library in a project | *"Set up ambient-library in this project"* |
| **select** | Configures `skills-manifest.yaml` via conversation | *"Configure my skills"* |
| **manage** | Updates, refreshes, adds/removes skills | *"Update my skills"*, *"Add X to this project"* |
| **review** | Code review for correctness, security, performance | *"Review this code"* |

## Domain Skills (project-level, opt-in)

Add these to `skills-manifest.yaml` to activate them for a specific project. Domain skills load additional instructions into context for that project's sessions.

*No additional domain skills yet. See [docs/MANAGEMENT.md](docs/MANAGEMENT.md) to add one.*

---

## Adding a Domain Skill

Domain skills are project-specific tools that extend the core system — documentation generators, deployment workflows, custom review standards, etc.

To add one: see [docs/MANAGEMENT.md](docs/MANAGEMENT.md).

To activate one in your project, add it to `skills-manifest.yaml`:

```yaml
domain_skills:
  - your-skill-name
```
