# load

Reads and applies a domain skill on demand. Invoked by the router when a request
matches a skill in `library/`.

## Steps

1. Identify which domain skill the request needs. If the project has a
   `skills-manifest.yaml`, restrict to the skills it lists under `domain_skills`.
   Otherwise consider any skill in `library/`.
2. Read its instructions: `${CLAUDE_SKILL_DIR}/library/<skill-name>/instructions.md`.
   Resolve `${CLAUDE_SKILL_DIR}` to its absolute path with the Read tool.
3. The skill may reference its own sibling files (e.g.
   `library/<skill-name>/references/...`). Read those as the skill directs.
4. Merge rules from the project's `CLAUDE.md` if present.
5. Carry out the skill's instructions.

## Rules

- A domain skill costs nothing in context until you read it here. Read only the
  one the request needs.
- If no domain skill matches, return to the router and handle the request
  normally.
- Never mention `library/`, manifests, or paths unless the user asks.
