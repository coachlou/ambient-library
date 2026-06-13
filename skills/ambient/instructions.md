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

## Domain skills

Project-specific skills live in `library/<skill-name>/instructions.md`. They are
plain files — not registered skills — so they cost nothing in context until you
read one. List `library/` or read the catalog in `SKILLS.md` (plugin root) to
see what's available.

When a request matches a domain skill's purpose, read that skill's
`instructions.md` from `library/` and follow it. If the project has a
`skills-manifest.yaml`, prefer the domain skills it lists.

## Rules

- Route to one subskill per request; read its file before acting.
- Never mention routing, subskills, `${CLAUDE_SKILL_DIR}`, or internal mechanics
  unless the user asks how the system works.
- Merge rules from the project's `CLAUDE.md` before executing.
- If nothing matches, handle the request with general Claude capabilities.
