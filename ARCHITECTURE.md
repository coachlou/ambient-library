# Architecture

## Overview

```
~/.claude/skills/ambient/     ← global skill, installed once per machine
└── subskills/                  always active in every Claude Code session
    ├── load.md                 reads project manifest at session start
    ├── install.md              sets up new projects
    ├── select.md               configures the manifest
    ├── manage.md               updates and maintenance
    └── review.md               code review

your-project/
├── skills-manifest.yaml      ← the only required project file
└── skills/                   ← git submodule (ambient-library)
    └── <domain-skill>/       ← loaded by ambient/load per manifest
        └── instructions.md
```

## Data Flow

**Machine setup (once):**
```
install-global.sh
  → clones ambient/ from GitHub
  → copies to ~/.claude/skills/ambient/
  → ambient skill available in all future sessions
```

**Session start (every session):**
```
Claude Code starts
  → ambient SKILL.md loaded (always active, global)
  → ambient/load.md runs silently
      → checks for skills-manifest.yaml
      → reads domain_skills list
      → loads skills/<name>/instructions.md for each
      → merges CLAUDE.md if present
  → all skills ready, session begins
```

**Project setup:**
```
User: "Set up ambient-library in this project"
  → ambient routes to install.md
      → git init (if needed)
      → git submodule add ambient-library → skills/
      → hands off to select.md
          → asks about the project
          → writes minimal skills-manifest.yaml
          → done
```

## Design Decisions

**Why a single global skill instead of per-project skills?**

Core capabilities (install, review, manage) don't depend on project context. Making them global means:
- No per-project setup overhead
- Always available, even in new projects
- One place to update when the system changes

**Why keep `skills-manifest.yaml` per project?**

Domain skills ARE project-specific — they carry context, standards, and instructions that differ per project. The manifest is the minimal, explicit declaration of what extra context this project needs.

**Why a git submodule for domain skills?**

Domain skills live in ambient-library and get pulled into projects via submodule. This keeps them centralized (one source of truth) while allowing projects to pin to a specific version.

**Why no setup scripts or hooks?**

With a global skill handling session-start loading, shell scripts are unnecessary. The skill reads the manifest directly — no intermediate generated files, no scripts to copy or maintain.

## Extending the System

**Add a domain skill:** Create a folder in ambient-library with `instructions.md`. Add its name to a project's `skills-manifest.yaml`. See [docs/MANAGEMENT.md](docs/MANAGEMENT.md).

**Extend core subskills:** Edit files in `ambient/subskills/`. Re-run `install-global.sh` to update your machine. Other users update by re-running the same install command.

**Project-specific overrides:** Add `CLAUDE.md` to the project root. `ambient/load.md` merges its contents automatically.
