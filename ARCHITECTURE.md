# Architecture

## The core idea

ambient-library is a Claude Code **plugin**. Installing the plugin distributes
everything — Claude Code clones it to `~/.claude/plugins/` and keeps it updated.
No manual clone, no environment variables, no dotfile edits, no submodule.

The plugin contains exactly **one registered skill** (`ambient`). Everything else
— the router's subskills and every domain skill — is a plain file inside the
plugin, read on demand. So the only thing in context by default is one skill
description.

```
plugin root (~/.claude/plugins/.../ambient/)
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
└── skills/
    └── ambient/                     ${CLAUDE_SKILL_DIR}
        ├── SKILL.md                 ← the ONLY registered skill
        ├── instructions.md          ← router (loads when ambient triggers)
        ├── subskills/*.md           ← read on demand
        └── library/<skill>/instructions.md   ← domain skills, read on demand

your-project/skills-manifest.yaml    ← optional; scopes domain skills
```

## Context cost

This is the property that drove the design:

| Item | In context? |
|------|-------------|
| `ambient` skill description | Always (one line — the trigger) |
| `ambient` body / router | Only when ambient triggers |
| Any subskill | Only when the router reads it |
| Any domain skill in `library/` | Only when the router reads it |

Domain skills are **not** registered skills, so they contribute **zero**
frontmatter to context — globally or per project. They're inert files until read.
This is why everything can be bundled in one plugin without context bloat.

## How a request flows

```
user request
  → ambient skill description matches → ambient triggers
  → SKILL.md tells Claude to read ${CLAUDE_SKILL_DIR}/instructions.md
  → router routes to one subskill (install / select / manage / review / load)
  → subskill executes; if a domain skill applies, load.md reads
    library/<skill>/instructions.md and follows it
  → project CLAUDE.md rules merged throughout
```

## Why ${CLAUDE_SKILL_DIR}

`${CLAUDE_SKILL_DIR}` is the absolute path to the skill's own directory inside
the installed plugin. The router uses it to read subskills and domain skills
regardless of the working directory. Because the whole plugin is installed
intact, every sibling file a skill needs (`references/`, `scripts/`) is always present.

## Design Decisions

**Why a plugin instead of a clone + global skill?**
The plugin system already does distribution, versioning, and updates natively,
and `${CLAUDE_SKILL_DIR}` already solves sibling-file resolution. A plugin
replaces `install-global.sh`, `AMBIENT_HOME`, the `~/.zshrc` export, the
`~/.claude/CLAUDE.md` record, and the per-project submodule — all of it.

**Why one router skill instead of five separate skills?**
Five registered skills would put five descriptions in context. One `ambient`
skill with subskills as plain files keeps the always-on cost to a single
description while still covering install, select, manage, review, and domain
loading.

**Why are domain skills plain files, not skills/ entries?**
Anything under `skills/<name>/SKILL.md` registers and adds a description to
context. Domain skills are project-specific and potentially numerous, so they
live in `library/` as `instructions.md` files — read on demand, zero standing
cost.

**Why keep `skills-manifest.yaml` at all?**
It's optional now. It scopes which domain skills the router considers for a
project — useful for focus and for applying project-specific skills consistently.

## Running a domain skill in its own context

Domain skills run in-context by default. When a user wants one isolated — "in the
background", "separately" — the router spawns a **general-purpose subagent** via
the Agent tool and hands it the resolved absolute path to the skill's
`instructions.md`. The subagent reads and follows that same file, so there is one
definition and two execution contexts.

This is how the `writing-team` pipeline offers an isolated run **without shipping
a registered agent**. A plugin agent would add a second standing description to
every session; routing to a general-purpose subagent on demand costs nothing
until used. The one-description invariant above still holds — `ambient` remains
the only description in context.

## Extending

**Add a domain skill:** create `skills/ambient/library/<name>/instructions.md`
(plus any sibling files), commit, bump `plugin.json` version. Users get it via
`/plugin update ambient`. See [docs/MANAGEMENT.md](docs/MANAGEMENT.md).

**Project rules:** add `CLAUDE.md` to the project root; the router merges it.
