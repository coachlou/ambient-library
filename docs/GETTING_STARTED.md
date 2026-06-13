# Getting Started

## First time on a new machine

Run this once in your terminal:

```bash
curl -fsSL https://raw.githubusercontent.com/coachlou/ambient-library/main/install-global.sh | bash
```

This installs the `ambient` skill globally at `~/.claude/skills/ambient/`. After this, open Claude Code in any project and the skill is available.

## Every new project — from Claude Code

Open Claude Code in your project folder and say:

> "Set up ambient-library in this project"

Claude will:
1. Re-run the curl to ensure the global skill is current
2. Initialize git if needed
3. Add the skills library as a submodule
4. Ask what your project does
5. Write a minimal `skills-manifest.yaml` with only the skills you need

## That's it

Your project has a `skills-manifest.yaml`. Every time you open Claude Code in that project, `ambient` reads the manifest and activates the right domain skills automatically.

## Day-to-day

Just work. Use natural language:

- *"Review this code"*
- *"Update my skills to the latest"*
- *"Configure my skills"*

## Next Steps

- **Full install details** → [INSTALLATION.md](INSTALLATION.md)
- **Using skills** → [USAGE.md](USAGE.md)
- **Adding custom skills** → [MANAGEMENT.md](MANAGEMENT.md)
- **Available skills** → [../SKILLS.md](../SKILLS.md)
