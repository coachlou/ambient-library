# Installation

## Machine Setup (once per machine)

```bash
curl -fsSL https://raw.githubusercontent.com/coachlou/ambient-library/main/install-global.sh | bash
```

This:
1. Clones the library once to `$AMBIENT_HOME` (default `~/ambient-library`)
2. Writes a thin pointer at `~/.claude/skills/ambient/SKILL.md`
3. Exports `AMBIENT_HOME` in `~/.zshrc`
4. Records `AMBIENT_HOME` in `~/.claude/CLAUDE.md`

After this, the `ambient` skill is available in every Claude Code session on the
machine. Re-run anytime to update — every write is an idempotent managed block,
so it never duplicates or clobbers your existing dotfile content.

**Custom location:**
```bash
AMBIENT_HOME=/path/to/lib bash install-global.sh
```
Use a path without spaces (keeps the YAML frontmatter simple).

## Project Setup (per project, from Claude Code)

Open Claude Code in your project folder and say:

> "Set up ambient-library in this project"

The `install` subskill runs. It:

1. Re-runs the machine setup (keeps the library current; bootstraps a new machine)
2. Writes a minimal `skills-manifest.yaml`
3. Hands off to `select` to configure which skills the project needs

That's the whole project footprint:

```
your-project/
└── skills-manifest.yaml     ← the only file
```

No submodule, no scripts, no hooks, no generated folders. Domain skills resolve
from the canonical clone at `$AMBIENT_HOME`.

## Updating

**Everything (library + all skills):**
> "Update my skills"

This runs `git -C $AMBIENT_HOME pull`, updating every project on the machine at
once. Or re-run the curl command above.

## How AMBIENT_HOME is resolved

Anything that needs the library location resolves it in this order:
1. `$AMBIENT_HOME` environment variable (from `~/.zshrc`)
2. The path recorded in `~/.claude/CLAUDE.md`
3. Default `~/ambient-library`

## Troubleshooting

### `ambient` skill isn't triggering
Verify the pointer exists:
```bash
ls ~/.claude/skills/ambient/SKILL.md
```
If missing, re-run the curl install. Then start a fresh Claude Code session.

### "Set up ambient-library" does nothing
The skill may not be loaded yet. Start a fresh Claude Code session and retry.

### Skills aren't loading in a project
1. Confirm `skills-manifest.yaml` exists in the project root.
2. Confirm the library is present: `ls $AMBIENT_HOME` (or `ls ~/ambient-library`).
3. Start a fresh session — skills load at session start.

### AMBIENT_HOME isn't set in new terminals
Open a new terminal (so `~/.zshrc` re-sources) or run `source ~/.zshrc`.

### Library location is wrong
Re-run with the correct path:
```bash
AMBIENT_HOME=/correct/path bash install-global.sh
```
This updates the pointer and both managed blocks.
