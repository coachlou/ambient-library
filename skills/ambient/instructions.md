# ambient — Router

You route an ambient-library request to exactly one subskill, then follow that
subskill's instructions. All paths below are relative to `${CLAUDE_SKILL_DIR}`
(this skill's directory inside the installed plugin).

## Routing

| User intent | Read and follow |
|-------------|-----------------|
| Set up / install ambient-library in this project | `subskills/install.md` |
| Configure / choose which skills this project uses | `subskills/select.md` |
| Update / refresh / add / remove skills | `subskills/manage.md` |
| Review code / check for bugs or security issues | `subskills/review.md` |
| A task a domain skill in `library/` covers | `subskills/load.md` |

Read the chosen file with the Read tool (resolve `${CLAUDE_SKILL_DIR}` to its
absolute path), then carry out its steps.

## Running a domain skill in its own context

Domain skills run in-context by default. If the user asks to run one "in its own
context", "in the background", or "separately" (most relevant for the
`writing-team` pipeline), don't run it inline — instead spawn a general-purpose
subagent with the Agent tool and pass it the **resolved absolute path** to that
skill's `instructions.md` (e.g. `${CLAUDE_SKILL_DIR}/library/writing-team/instructions.md`),
telling it to read and follow that file against the user's brief. The subagent
keeps research/draft churn out of the main thread. No registered agent is needed
or shipped — this keeps the always-on context cost to the single `ambient`
description.

## Domain skills

Project-specific skills live in `library/<skill-name>/instructions.md`. They are
plain files — not registered skills — so they cost nothing in context until read.

**To avoid context bloat, choosing a skill and loading a skill are separate steps:**

1. To find a match, read **only** `library/catalog.yaml` — a cheap list of skill
   names and one-line descriptions. Never read skill `instructions.md` files to
   decide relevance.
2. Pick the single best match. If the project has a `skills-manifest.yaml`,
   restrict to the skills it lists.
3. Read **only that one** skill's `instructions.md` and follow it.

Never load more than one domain skill body per request, and never load the whole
library.

## Rules

- Route to one subskill per request; read its file before acting.
- Never mention routing, subskills, `${CLAUDE_SKILL_DIR}`, or internal mechanics
  unless the user asks how the system works.
- Merge rules from the project's `CLAUDE.md` before executing.
- If nothing matches, handle the request with general Claude capabilities.
