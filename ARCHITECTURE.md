# Architecture

## The core idea

ambient-library is a canonical library with thin runtime wrappers. The canonical
capabilities live under `skills/ambient/`; each LLM/runtime gets its own plugin
adapter that exposes one registered `ambient` skill and then delegates back to
the canonical library.

The Claude Code wrapper is in `.claude-plugin/` and `skills/ambient/SKILL.md`.
The Codex wrapper is in `.codex-plugin/` and `codex-skills/ambient/SKILL.md`.
For harnesses without a plugin system, `templates/AGENTS-pointer.md` is a
pointer adapter: a block pasted into the project's `AGENTS.md` that routes
matching requests to the same canonical router by absolute path.

Each wrapper contains exactly **one registered skill** (`ambient`). Everything
else — the router's subskills and every domain skill — is a plain canonical file
read on demand. So the only thing in context by default is one skill description.

```
plugin root
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── .codex-plugin/
│   └── plugin.json
├── templates/
│   └── AGENTS-pointer.md           ← pointer adapter for non-plugin harnesses
├── codex-skills/
│   └── ambient/
│       └── SKILL.md                ← Codex adapter
└── skills/
    └── ambient/
        ├── SKILL.md                 ← Claude Code adapter
        ├── instructions.md          ← canonical router
        ├── subskills/*.md           ← canonical subskills, read on demand
        └── library/<skill>/instructions.md   ← domain skills, read on demand

your-project/skills-manifest.yaml    ← optional; scopes domain skills
```

## Context cost

This is the property that drove the design:

| Item | In context? |
|------|-------------|
| Runtime `ambient` skill description | Always (one line — the trigger) |
| Runtime adapter / canonical router | Only when ambient triggers |
| Any subskill | Only when the router reads it |
| Any domain skill in `library/` | Only when the router reads it |

Domain skills are **not** registered skills, so they contribute **zero**
frontmatter to context — globally or per project. They're inert files until read.
This is why everything can be bundled in one plugin without context bloat.

## How a request flows

```
user request
  → runtime ambient skill description matches → ambient triggers
  → runtime adapter locates skills/ambient/instructions.md
  → canonical router routes to one subskill (install / select / manage / review / load / admin)
  → subskill executes; if a domain skill applies, load.md reads
    library/<skill>/instructions.md and follows it
  → project rules are merged throughout
```

## Runtime path adapters

Claude Code provides `${CLAUDE_SKILL_DIR}`, so its adapter uses that path to find
the canonical router and sibling files.

Codex does not use `${CLAUDE_SKILL_DIR}`. Its adapter lives at
`codex-skills/ambient/SKILL.md` and translates the canonical library root to
`../../skills/ambient/` relative to that file. When canonical instructions mention
`${CLAUDE_SKILL_DIR}`, the Codex adapter treats it as the canonical library root.

The pointer adapter has no manifest at all. It pins the library's absolute
path directly in the project's `AGENTS.md` and instructs the agent to treat
`${CLAUDE_SKILL_DIR}` as that path. Triggering is by instruction rather than
harness-enforced skill matching, so it is less reliable on indirect requests —
the tradeoff for working on any harness that reads a project instruction file.

This keeps the runtime-specific path logic in the wrapper, not in the canonical
capability files.

## Design Decisions

**Why runtime wrappers instead of runtime-specific libraries?**
The library should be canonical. Claude Code, Codex, and future runtimes may have
different plugin manifests or path variables, but they should load the same
router, subskills, and domain skill instructions.

**Why one router skill instead of five separate skills?**
Five registered skills would put five descriptions in context per runtime. One
`ambient` skill with subskills as plain files keeps the always-on cost to a
single description while still covering install, select, manage, review, and
domain loading.

**Why are domain skills plain files, not skills/ entries?**
Registered skill paths are runtime-specific. Domain skills are project-specific
and potentially numerous, so they live in the canonical `library/` as
`instructions.md` files — read on demand, zero standing cost.

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
(plus any sibling files), update `skills/ambient/library/catalog.yaml`, commit,
and bump each runtime plugin version as needed. Users get it through their
runtime's plugin update flow. See [docs/MANAGEMENT.md](docs/MANAGEMENT.md).

**Project rules:** add runtime-appropriate project guidance such as `AGENTS.md`
or `CLAUDE.md` to the project root; the adapter/router merges it.
