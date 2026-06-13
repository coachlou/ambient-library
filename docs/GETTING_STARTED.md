# Getting Started with Ambient Library

Ambient Library is a central skills system for Claude Code. Skills are reusable tools that load automatically in your Claude sessions — code review, custom workflows, documentation, whatever your project needs. Only the skills you choose get loaded, keeping context lean.

## Setup from Claude Code (Recommended)

No terminal needed. Open Claude Code in your project folder and say:

> "Set up ambient-library in this project"

Claude runs the full installation and immediately asks what your project does to configure the right skills for you.

## Setup from Terminal

If you prefer the terminal:

```bash
cd your-project-root
git submodule add git@github-coachlou:coachlou/ambient-library.git skills
bash skills/bootstrap.sh
```

> **Note:** `skills` is the local folder name — don't change it. `setup-skills.sh` expects the submodule at exactly `skills/`.

After bootstrap, configure your manifest from Claude Code:
> "Configure my skills"

## What You Get

Four skills come built-in:

| Skill | Purpose |
|-------|---------|
| `skill-loader` | Always-active orchestration layer (required) |
| `skill-system-manager` | Handles updates and refreshes on request |
| `ambient-install` | Installs the system into new projects |
| `skill-picker` | Builds your manifest through natural language |

Plus any additional skills you add. See [../SKILLS.md](../SKILLS.md) for the full catalog.

## Configuring Your Manifest

`skills-manifest.yaml` controls which skills load in your sessions. The smaller it is, the leaner your context. After install, skill-picker walks you through choosing only what you need.

To reconfigure anytime:
> "Update my skill manifest"

## Next Steps

- **Full installation details** → [INSTALLATION.md](INSTALLATION.md)
- **Using skills** → [USAGE.md](USAGE.md)
- **Adding custom skills** → [MANAGEMENT.md](MANAGEMENT.md)
- **All available skills** → [../SKILLS.md](../SKILLS.md)
- **Something broken** → [INSTALLATION.md#troubleshooting](INSTALLATION.md#troubleshooting)
