# load

Reads and applies a domain skill on demand. Invoked by the router when a request
matches a skill in `library/`.

## Steps

1. Read **only** `${CLAUDE_SKILL_DIR}/library/catalog.yaml` to see the available
   skills and their one-line descriptions. This is the cheap selection step — do
   not open any skill's `instructions.md` yet.
2. Choose the single best match. If the project has a `skills-manifest.yaml`,
   restrict to the skills it lists under `domain_skills`. If nothing matches,
   stop and let the router handle the request normally.
3. Read **only that one** skill's instructions:
   `${CLAUDE_SKILL_DIR}/library/<skill-name>/instructions.md`.
4. The skill may reference its own sibling files (e.g.
   `library/<skill-name>/references/...`). Read those only as the skill directs.
5. Merge rules from the project's `CLAUDE.md` if present, then carry out the skill.

## Rules

- Selection reads the catalog only. Execution reads exactly one skill body.
- Never load more than one domain skill per request. Never load the whole library.
- Never mention `library/`, the catalog, manifests, or paths unless the user asks.
