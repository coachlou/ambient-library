# Skills Catalog

## Core Capabilities (built into the `ambient` skill)

The `ambient` skill routes to these subskills. They're plain files read on
demand — always available, no manifest entry needed.

| Subskill | What it does | How to invoke |
|----------|-------------|---------------|
| **install** | Sets up ambient-library in a project | *"Set up ambient-library in this project"* |
| **select** | Scopes the project's domain skills via conversation | *"Configure my skills"* |
| **manage** | Adds/removes skills, points to `/plugin update` | *"Update my skills"*, *"Add X to this project"* |
| **review** | Code review for correctness, security, performance | *"Review this code"* |
| **load** | Reads a domain skill on demand when a request matches | Automatic — invoked by the router |

## Domain Skills (in `library/`, read on demand)

Domain skills live in the plugin at `skills/ambient/library/<name>/instructions.md`.
They are plain files — **not** registered skills — so they add nothing to context
until the router reads one. Optionally scope which a project uses via
`skills-manifest.yaml`.

| **project-brief** | Creates a one-page project overview anyone can read and share | *"Write a project brief"*, *"Summarize this project"* |

---

## Adding a Domain Skill

Domain skills are project-specific tools that extend the core system — documentation generators, deployment workflows, custom review standards, etc.

To add one: see [docs/MANAGEMENT.md](docs/MANAGEMENT.md).

To activate one in your project, add it to `skills-manifest.yaml`:

```yaml
domain_skills:
  - your-skill-name
```
