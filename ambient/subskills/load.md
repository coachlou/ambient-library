# load

Runs silently at the start of every session. Activates the domain skills this
project asked for, reading them from the canonical library.

## Resolving AMBIENT_HOME

The library root is `AMBIENT_HOME`. Resolve it in this order:
1. The `$AMBIENT_HOME` environment variable, if set.
2. The path recorded in `~/.claude/CLAUDE.md` under "## Ambient Library".
3. Default: `~/ambient-library`.

## Steps

1. Look for `skills-manifest.yaml` in the current working directory.
2. If not found, do nothing — core skills still work. Session proceeds.
3. If found, read the `domain_skills` list.
4. For each domain skill, read its instructions from the canonical library:
   `$AMBIENT_HOME/<skill-name>/instructions.md`
   - If found, load it into context silently.
   - If not found, skip — don't warn unless the user asks.
5. Merge rules from the project's `CLAUDE.md` if present.

## Rules

- Completely silent. No output, no confirmation.
- Never mention manifests, AMBIENT_HOME, or loading mechanics.
- If the manifest is malformed, skip gracefully.
