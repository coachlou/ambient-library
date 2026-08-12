# load

Reads and applies a domain skill on demand. Invoked by the router when a request
matches a skill in `library/`, or when the user names one explicitly.

## Explicit one-off invocation

If the user names a specific skill or agent from the library ("use the
<name> skill", "run <name> from the ambient library", "one-off: <name>"),
skip the selection steps entirely:

- Read `${CLAUDE_PLUGIN_ROOT}/library/<name>/instructions.md` directly and
  carry it out (steps 4–5 below still apply).
- Ignore `skills-manifest.yaml` scoping — an explicit request overrides it.
- Do **not** add the skill to the manifest or change any project file. The
  invocation lives only in this conversation. If the user wants it permanently,
  they'll say so (that's `manage.md`'s job).
- If no skill matches the name, list the closest names from the catalog and stop.

## Steps

1. Read **only** `${CLAUDE_PLUGIN_ROOT}/library/catalog.yaml` to see the available
   skills and their one-line descriptions. This is the cheap selection step — do
   not open any skill's `instructions.md` yet.
2. Choose the single best match on the descriptions alone. If the project has
   a `skills-manifest.yaml`, restrict to the skills listed under
   `domain_skills`. If nothing matches, stop and let the router handle the
   request normally.
3. Resolve the skill body through the overlay cascade, most specific first:
   a. `<project root>/.ambient/<skill-name>/instructions.md`
   b. `~/.aai/library/<skill-name>/instructions.md`
   c. `${CLAUDE_PLUGIN_ROOT}/library/<skill-name>/instructions.md`

   Read the **first** one that exists — that is the skill body. Then append any
   `overrides.md` present at (b), then at (a), and treat them as additional
   rules that follow the body. Skip the cascade entirely when no overlay
   directory exists; (c) is the normal case.
4. The skill may reference its own sibling files (e.g.
   `library/<skill-name>/references/...`). Resolve those relative to the layer
   that supplied the body, and read them only as the skill directs.
5. Merge rules from the project's `CLAUDE.md` if present, then carry out the skill.

## Rules

- Selection reads the catalog only. Execution reads exactly one skill body.
- Never load more than one domain skill per request. Never load the whole library.
- Never mention `library/`, the catalog, manifests, or paths unless the user asks.
- Overlays override by canonical name — they never add new catalog entries.
  Selection still reads only `catalog.yaml`, so an overlay for a skill absent
  from the catalog is unreachable (that's `propose.md`'s job, not an overlay's).
- Say which layer supplied the body **only** when it wasn't (c) — a silent
  override is the one thing that makes a skill's behavior inexplicable.
