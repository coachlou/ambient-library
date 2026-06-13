# Architecture

## The core idea

One canonical clone of ambient-library lives on the machine at `$AMBIENT_HOME`.
Everything else points into it. Nothing is duplicated, nothing is copied per
project, and any skill's sibling files (references, scripts, templates) are
always present because the whole library is there intact.

```
$AMBIENT_HOME/                       one full git clone — source of truth
├── ambient/
│   ├── SKILL.md                      canonical frontmatter
│   ├── instructions.md               router
│   └── subskills/                    load, install, select, manage, review
├── <domain-skill>/                   each with instructions.md + any siblings
└── SKILLS.md, docs/, ...

~/.claude/skills/ambient/SKILL.md     thin pointer → absolute instructions_path
~/.zshrc                              export AMBIENT_HOME=...   (for shells)
~/.claude/CLAUDE.md                   records AMBIENT_HOME      (for Claude)

your-project/skills-manifest.yaml     the ONLY per-project file
```

## Resolving AMBIENT_HOME

Three layers, each for a different consumer:

| Source | Read by | Precedence |
|--------|---------|-----------|
| `$AMBIENT_HOME` env var (set in `~/.zshrc`) | shell scripts, every terminal | 1st |
| `~/.claude/CLAUDE.md` managed block | Claude, in-context every session | 2nd |
| default `~/ambient-library` | fallback | 3rd |

The env var serves shell scripts (`git pull`, etc.). The CLAUDE.md record means
Claude knows the path in-context, so it can resolve skill files itself even if
the Claude Code loader doesn't auto-follow `instructions_path`.

## Why the pointer works

`~/.claude/skills/ambient/SKILL.md` is a thin pointer Claude Code discovers and
triggers on. Its frontmatter carries an **absolute** `instructions_path` into
the canonical clone, and its body restates that path. When triggered, the full
instructions load from `$AMBIENT_HOME/ambient/instructions.md` — and every
relative reference inside (`subskills/`, etc.) resolves, because the entire
library is sitting there. This is why separating frontmatter (the pointer) from
instructions (in the clone) is correct: only the pointer is duplicated into the
skills directory; everything with dependencies stays in the one clone.

## Data Flow

**Machine setup (`install-global.sh`, once — or re-run to update):**
```
resolve AMBIENT_HOME (env var → default)
  → git clone/pull library to $AMBIENT_HOME
  → write pointer ~/.claude/skills/ambient/SKILL.md (absolute instructions_path)
  → write managed block: export AMBIENT_HOME in ~/.zshrc
  → write managed block: record AMBIENT_HOME in ~/.claude/CLAUDE.md
```

**Session start (every session):**
```
ambient pointer triggers (always active)
  → loads $AMBIENT_HOME/ambient/instructions.md
  → runs subskills/load.md silently
      → reads project skills-manifest.yaml
      → for each domain skill: read $AMBIENT_HOME/<skill>/instructions.md
      → merge project CLAUDE.md
```

**Project setup ("Set up ambient-library in this project"):**
```
ambient routes to subskills/install.md
  → runs install-global.sh (ensures machine is current; bootstraps new machines)
  → writes minimal skills-manifest.yaml
  → hands off to subskills/select.md (configures the manifest)
```

**Updating:**
```
"Update my skills"  →  git -C $AMBIENT_HOME pull
                       (updates every project on the machine at once)
```

## Design Decisions

**Why one canonical clone instead of copying skills per project?**
Copying only `SKILL.md` (the old "pointer" model) breaks any skill with sibling
files — references, scripts, templates point at nothing. A single full clone
keeps every dependency intact and gives one place to update.

**Why no project git submodule?**
The canonical clone already holds every skill. Projects resolve domain skills
from `$AMBIENT_HOME`, so they need nothing but `skills-manifest.yaml`. Dropping
the submodule removes per-project setup, generated folders, and update friction.
Trade-off: projects no longer pin a skill version independently — all projects
on a machine share the one clone. The system's model is "pull to update," which
makes that the right trade.

**Why record the path in both `.zshrc` and `CLAUDE.md`?**
Different readers. Shell scripts need an env var; Claude needs the path in its
context. Recording both means neither has to guess.

**Why managed blocks?**
Re-running `install-global.sh` must be safe. Fenced blocks (`# >>> ... <<<`) let
the script replace its own section in place without touching the user's other
content.

## Extending the System

**Add a domain skill:** create `$AMBIENT_HOME/<skill>/instructions.md` (plus any
sibling files), push to the repo, and `git pull`. Activate it in a project by
adding its name to `skills-manifest.yaml`. See [docs/MANAGEMENT.md](docs/MANAGEMENT.md).

**Change where the library lives:** set `AMBIENT_HOME` before running
`install-global.sh` (e.g. `AMBIENT_HOME=/Volumes/Extreme\ Pro/lib bash install-global.sh`).
Use a path without spaces to keep YAML frontmatter simple.

**Project-specific rules:** add `CLAUDE.md` to the project root; `load.md` merges it.
