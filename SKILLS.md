# Skills Catalog

All skills available in Ambient Library. Add any of these to your project's `skills-manifest.yaml`.

## Setup Skills

### ambient-install
**Installs ambient-library into a project from within Claude Code.**

The entry point for the entire system. Invoke from a Claude session:
- *"Set up ambient-library in this project"*
- *"Install the skill system"*
- *"Add ambient-library to this project"*

Runs bootstrap, then hands off to skill-picker to configure the manifest. No terminal required.

### skill-picker
**Builds `skills-manifest.yaml` through a natural language conversation.**

Asks what your project does, recommends a minimal skill set, writes the manifest, and runs setup. Keeps context lean by loading only the skills you actually need. Invoked automatically after ambient-install, or anytime:
- *"Configure my skills"*
- *"Update my skill manifest"*
- *"Which skills do I need for this project?"*

## Built-In Skills

### skill-loader
**Always active. Do not remove from your manifest.**

The invisible orchestration layer. Handles skill resolution, caching, and merging project rules from `CLAUDE.md` / `AGENTS.md`. You never invoke this directly — it runs automatically at the start of every session.

### skill-system-manager
**Manages updates and maintenance.**

Handles skill refreshes, updates, and changes to the skill system. Invoke it naturally:
- *"Update my skills to the latest version"*
- *"Refresh the skill system"*
- *"Add the X skill to this project"*

### code-review
**Thorough, constructive code reviews.**

Reviews code for correctness, security, performance, readability, and project standards. Invoke it naturally:
- *"Review this code"*
- *"Code review for src/auth.ts"*
- *"Check this for security issues"*

Output: summary, findings by severity (critical/major/minor) with file:line references, suggested fixes.

---

## Adding Skills

To contribute a new skill to this library, see [docs/MANAGEMENT.md](docs/MANAGEMENT.md).

To activate a skill in your project, add its folder name to `skills-manifest.yaml`:

```yaml
skills:
  - skill-loader
  - skill-system-manager
  - code-review
  - your-skill-name   # ← add here
```

Then run `./setup-skills.sh`.
