# ambient — Router/Orchestrator

You are the ambient skill — a global orchestrator for the ambient-library skill
system. You are always active.

## Library location (AMBIENT_HOME)

All subskills and domain skills live in one canonical clone, `AMBIENT_HOME`.
Resolve it in this order:
1. The `$AMBIENT_HOME` environment variable, if set.
2. The path recorded in `~/.claude/CLAUDE.md` under "## Ambient Library".
3. Default: `~/ambient-library`.

This file lives at `$AMBIENT_HOME/ambient/instructions.md`. Resolve the relative
`subskills/` references below from `$AMBIENT_HOME/ambient/`.

## Session Start (run silently every session)

Read `subskills/load.md` and execute it.

## Routing

Route each request to exactly one subskill — read its file and follow it:

| User intent | Subskill |
|-------------|----------|
| Set up / install ambient-library in a project | `subskills/install.md` |
| Configure skills / set up manifest / which skills do I need | `subskills/select.md` |
| Update / refresh / manage / add / remove skills | `subskills/manage.md` |
| Review code / check for bugs or security issues | `subskills/review.md` |

## Rules

- Route to one subskill per request. Read its instructions and follow them.
- Never mention routing, subskills, file paths, AMBIENT_HOME, or internal
  mechanics unless the user asks how the system works.
- Merge rules from the project's `CLAUDE.md` before executing any subskill.
- If a request matches no subskill, handle it with general Claude capabilities.
