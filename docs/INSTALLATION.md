# Installation

## Machine Setup (once per machine)

```bash
curl -fsSL https://raw.githubusercontent.com/coachlou/ambient-library/main/install-global.sh | bash
```

Installs the `ambient` skill to `~/.claude/skills/ambient/`. After this, open Claude Code — the skill is available in every session on this machine.

**What gets installed:**
```
~/.claude/skills/ambient/
├── SKILL.md
├── instructions.md
└── subskills/
    ├── load.md
    ├── install.md
    ├── select.md
    ├── manage.md
    └── review.md
```

## Project Setup (per project, from Claude Code)

Open Claude Code in your project folder and say:

> "Set up ambient-library in this project"

The `ambient/install` subskill runs. It:

1. Re-runs the curl to ensure the global skill is current
2. Runs `git init` if there's no git repo
3. Adds the skills library as a submodule at `skills/` — **this folder name is fixed**, don't rename it
4. Hands off to `ambient/select` to configure the manifest

Result: a single `skills-manifest.yaml` in your project root.

## What the Project Needs

Just one file:

```
your-project/
└── skills-manifest.yaml
```

No scripts, no hooks, no generated folders. Everything else is handled by the global `ambient` skill.

## Updating the Global Skill

The install subskill re-runs the curl automatically every time you say *"Set up ambient-library"* in any project. To update manually at any time:

```bash
curl -fsSL https://raw.githubusercontent.com/coachlou/ambient-library/main/install-global.sh | bash
```

## Updating Domain Skills (per project)

From Claude Code:

> "Update my skills to the latest"

Or manually:

```bash
git submodule update --remote skills
```

## Cloning a Project

If you're cloning a repo that already has ambient-library set up:

```bash
git clone <project-url>
cd <project>
git submodule update --init --recursive
```

Then open Claude Code — the `ambient` skill reads the manifest automatically.

## Troubleshooting

### `ambient` skill isn't triggering

Verify it's installed:
```bash
ls ~/.claude/skills/ambient/
```

If missing, re-run the install command above.

### "Set up ambient-library" does nothing useful

The `ambient` skill may not be loaded yet. Start a fresh Claude Code session and try again.

### Submodule errors after cloning

```bash
git submodule update --init --recursive
```

### Skills manifest not found

Check the project root for `skills-manifest.yaml`. If missing, say *"Configure my skills"* — the select subskill will create it.

### SSH key errors

The install command uses HTTPS — no SSH key needed. If you see SSH errors, check that you're using the HTTPS URL, not an SSH alias.
