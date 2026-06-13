# Getting Started

## Step 1: Install once on your machine

Open a terminal and run:

```bash
curl -fsSL https://raw.githubusercontent.com/coachlou/ambient-library/main/install-global.sh | bash
```

This installs the `ambient` skill into `~/.claude/skills/ambient/`. It's now available in every Claude Code session, in every project, forever. You never run this again.

## Step 2: Set up a project

Open Claude Code in any project folder and say:

> "Set up ambient-library in this project"

Claude will:
1. Initialize git if needed
2. Add the skills library as a submodule
3. Ask what your project does
4. Write a minimal `skills-manifest.yaml` with only the skills you need

## That's it

Your project now has a `skills-manifest.yaml`. Every time you open Claude Code in that project, the `ambient` skill reads the manifest and activates the right domain skills automatically.

## Day-to-Day Usage

You don't manage anything. Just work. Use natural language:

- *"Review this code"*
- *"Update my skills to the latest"*
- *"Add a new skill to this project"*
- *"Configure my skills"*

## Next Steps

- **Full install details** → [INSTALLATION.md](INSTALLATION.md)
- **Using skills** → [USAGE.md](USAGE.md)
- **Adding custom skills** → [MANAGEMENT.md](MANAGEMENT.md)
- **Available skills** → [../SKILLS.md](../SKILLS.md)
