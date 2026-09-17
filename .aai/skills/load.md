# load

Reads and applies a domain skill on demand. Invoked by the router when a request
matches a skill **enabled** at some scope, or when the user names one explicitly.

## The enabled set

Domain skills are opt-in. A skill may be picked for an unnamed task only if it
appears in at least one of these (union — no scope removes another's skills):

- `~/.aai/skills-manifest.yaml` → `domain_skills` (user scope, every folder)
- `<project root>/skills-manifest.yaml` → `domain_skills` (this project)
- `<project root>/.ailib/<name>/` or `<project root>/.aai/skills/<name>/`
  (vendored or forked here — installing it is enabling it). An
  `.aai/skills/<name>/` counts only if it holds `instructions.md`,
  `project.yaml`, or `overrides.md` — one holding only `environment.yaml`
  (notably under `~`) is inherited settings and enables nothing.

Missing files contribute nothing. An empty set means no domain skill is picked
unless the user names one — say nothing about it and let the router fall back
to general capabilities. Don't create a manifest to fill the gap.

## Explicit one-off invocation

If the user names a specific skill or agent from the library ("use the
<name> skill", "run <name> from the ambient library", "one-off: <name>"),
skip the selection steps entirely:

- Read `${CLAUDE_PLUGIN_ROOT}/library/<name>/instructions.md` directly and
  carry it out (steps 4–5 below still apply).
- Ignore the enabled set — an explicit request overrides it.
- Do **not** add the skill to the manifest or change any project file. The
  invocation lives only in this conversation. If the user wants it permanently,
  they'll say so (that's `manage.md`'s job).
- If no skill matches the name, list the closest names from the catalog and stop.

## Steps

1. Build the enabled set (above). If it is empty, stop.
2. Read `${CLAUDE_PLUGIN_ROOT}/library/catalog.yaml` and consider **only** the
   enabled names' one-line descriptions — do not open any skill's
   `instructions.md` yet. Choose the single best match on those descriptions.
   If nothing matches, stop and let the router handle the request normally.
3. Resolve the skill body, most specific first:
   a. `<project root>/.aai/skills/<skill-name>/instructions.md` (this folder's fork)
   b. `<project root>/.ailib/<skill-name>/instructions.md` (vendored, pinned)
   c. `${CLAUDE_PLUGIN_ROOT}/library/<skill-name>/instructions.md`

   Read the **first** one that exists — that is the skill body. For a skill
   that ships a `contract.yaml`, also look for (b) in each folder above the
   project root, so a parent's vendored copy serves its project subfolders.
   Then, if `<project root>/.aai/skills/<skill-name>/overrides.md` exists,
   append it as additional rules that follow the body — whichever layer
   supplied it. (c) is the normal case.
4. The skill may reference its own sibling files (e.g.
   `library/<skill-name>/references/...`). Resolve those relative to the layer
   that supplied the body, and read them only as the skill directs.
5. Merge rules from the project's `CLAUDE.md` if present, then carry out the skill.

## Rules

- Selection reads the manifests and the catalog only, and picks only from the
  enabled set. Execution reads exactly one skill body.
- Never load more than one domain skill per request. Never load the whole library.
- Never mention `library/`, the catalog, manifests, or paths unless the user asks.
- Forks and `overrides.md` apply by canonical name — they never add new
  catalog entries. Selection still reads only `catalog.yaml`, so one for a
  skill absent from the catalog is unreachable (that's `propose.md`'s job).
- Say which layer supplied the body, and that `overrides.md` was applied,
  **only** when it wasn't plain (c) — a silent
  override is the one thing that makes a skill's behavior inexplicable.
