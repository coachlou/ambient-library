# Installation

## Machine Setup (once per machine)

```bash
curl -fsSL https://raw.githubusercontent.com/coachlou/ambient-library/main/install-global.sh | bash
```

Installs the `ambient` skill to `~/.claude/skills/ambient/`. After this, ambient is available in every Claude Code session on this machine — no per-project setup needed.

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

The `ambient/install` subskill runs automatically. It:

1. Runs `git init` if there's no git repo
2. Adds the skills library as a submodule at `skills/` — **this folder name is fixed**, don't rename it
3. Hands off to `ambient/select` to configure the manifest

Result: a single `skills-manifest.yaml` in your project root.

## What the Project Needs

Just one file:

```
your-project/
└── skills-manifest.yaml
```

No scripts, no hooks, no generated folders. Everything else is handled by the global `ambient` skill.

## Updating the Global Skill

To update `ambient` to the latest version:

```bash
curl -fsSL https://raw.githubusercontent.com/coachlou/ambient-library/main/install-global.sh | bash
```

Same command — safe to re-run anytime.

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
