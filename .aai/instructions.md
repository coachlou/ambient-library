# ambient — Router

You route an ambient-library request to exactly one subskill, then follow that
subskill's instructions. All paths below are relative to `${CLAUDE_PLUGIN_ROOT}`
(this skill's directory inside the installed plugin).

## Routing

| User intent | Read and follow |
|-------------|-----------------|
| Set up / install ambient-library in this project | `.aai/skills/install.md` |
| Configure / choose which skills this project uses | `.aai/skills/select.md` |
| Update / refresh / add / remove skills | `.aai/skills/manage.md` |
| Review code / check for bugs or security issues | `.aai/skills/review.md` |
| A task a domain skill in `library/` covers | `.aai/skills/load.md` |
| Explicitly named skill, one-off ("use the <name> skill") | `.aai/skills/load.md` |
| Maintain the library itself — create/edit/delete a library skill, edit the catalog, promote a staged proposal | `.aai/skills/admin.md` |
| Save the work just done as a new skill ("save this as a skill", "propose a skill", "remember how we did this") | `.aai/skills/propose.md` |
| Make another folder ambiently intelligent — stamp `.aai/` into it, vendor a capability into its `.ailib/`, personalize (fork/shadow), re-sync, or promote a memory pattern to a reference | `.aai/skills/lifecycle.md` |
| Rot sweep — "what's stale", "which skills have rotted", audit the canonical library for outdated context | `.aai/skills/lifecycle.md` |

Disambiguation: "add <skill> **to this project**" is manage (edits the
project's manifest); "add a skill **to the library**" with content you supply is
admin (edits the canonical library in a source clone); "save **this session's
work** as a skill" is propose (drafts from the trace into `library/_staging/`,
where admin later promotes it); "add <skill> **into a folder's `.ailib`**"
or "make this folder ambient" is lifecycle (stamps/vendors the `.aai`/`.ailib`
scaffold into a target folder).

Read the chosen file with the Read tool (resolve `${CLAUDE_PLUGIN_ROOT}` to its
absolute path), then carry out its steps.

## Running a domain skill in its own context

Domain skills run in-context by default. If the user asks to run one "in its own
context", "in the background", or "separately" (most relevant for the
`writing-team` pipeline), don't run it inline — instead spawn a general-purpose
subagent with the Agent tool and pass it the **resolved absolute path** to that
skill's `instructions.md` (e.g. `${CLAUDE_PLUGIN_ROOT}/library/writing-team/instructions.md`),
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

## The ambient-folder model

This folder is the reference `.aai`/`.ailib` ambient folder, and every folder it
stamps inherits the same two-part contract:

- **`.aai/` is owned.** Behavior, identity, forks, references, and memory live
  here and are never overwritten by an update.
- **`.ailib/` is vendored.** Pristine, read-only canonical capabilities, freely
  deleted and re-synced. `.aai/` shadows it — a fork in `.aai/skills/` overrides
  the `.ailib/` copy of the same capability.
- **Memory graduates to references.** `.aai/memory/` is runtime state no update
  touches; recurring patterns are promoted deliberately into `.aai/references/`.

The operations that apply this model to other folders live in
`.aai/skills/lifecycle.md`. The full spec is `templates/aai/README.md`.

## Rules

- Route to one subskill per request; read its file before acting.
- Never mention routing, subskills, `${CLAUDE_PLUGIN_ROOT}`, or internal mechanics
  unless the user asks how the system works.
- Merge rules from the project's `CLAUDE.md` before executing.
- If nothing matches, handle the request with general Claude capabilities.
