# load

Runs silently at the start of every session. Activates domain skills listed in the project manifest.

## Steps

1. Look for `skills-manifest.yaml` in the current working directory.
2. If not found, do nothing. Session proceeds with core ambient skills only.
3. If found, read the file and note which domain skills are listed.
4. For each domain skill listed, look for its instructions in `skills/` submodule:
   - `skills/<skill-name>/instructions.md`
   - If found, load it into context silently.
   - If not found, skip — do not warn the user unless they ask.
5. Merge any rules from `CLAUDE.md` if present.

## Rules

- Completely silent. No output, no confirmation messages.
- Never mention manifest files, submodules, or loading mechanics.
- If `skills-manifest.yaml` is malformed or unreadable, skip gracefully.
