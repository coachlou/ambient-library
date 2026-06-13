# Getting Started

## First time on a new machine

Run this once in your terminal:

```bash
curl -fsSL https://raw.githubusercontent.com/coachlou/ambient-library/main/install-global.sh | bash
```

This clones the library to `~/ambient-library`, installs the `ambient` skill,
and records the library path so both your shell and Claude can find it. After
this, open Claude Code in any project and the skill is available.

## Every new project — from Claude Code

Say:

> "Set up ambient-library in this project"

Claude will:
1. Make sure the library is current on your machine
2. Ask what your project does
3. Write a minimal `skills-manifest.yaml` with only the skills you need

## That's it

The only file added to your project is `skills-manifest.yaml`. Every session,
the `ambient` skill reads it and activates the right skills from the library —
which lives in one place on your machine, not copied into each project.

## Day-to-day

Just work. Natural language:

- *"Review this code"*
- *"Update my skills"*
- *"Configure my skills"*
- *"Add code-review to this project"*

## Next Steps

- **Full install details** → [INSTALLATION.md](INSTALLATION.md)
- **Using skills** → [USAGE.md](USAGE.md)
- **Adding custom skills** → [MANAGEMENT.md](MANAGEMENT.md)
- **How it works** → [../ARCHITECTURE.md](../ARCHITECTURE.md)
- **Available skills** → [../SKILLS.md](../SKILLS.md)
