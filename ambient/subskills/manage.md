# manage

Handles updates, refreshes, and maintenance of the ambient-library skill system.

## Operations

### Update skills to latest

Pull the latest skills from ambient-library:

```bash
git submodule update --remote skills
```

Confirm: "Skills updated to latest version."

### Refresh skills

Re-read the manifest and reload domain skill instructions for the current session. No git commands needed — just re-execute load.md.

Confirm: "Skills refreshed."

### Add a skill to this project

1. Check that the skill exists in `skills/`.
2. Add it to `skills-manifest.yaml` under `domain_skills`.
3. Re-execute load.md to activate it immediately.

Confirm: "Added [skill-name]. It's now active for this project."

### Remove a skill from this project

1. Remove it from `skills-manifest.yaml`.
2. Tell the user to start a fresh session for the change to take effect (skills are cached per session).

### Check skill system status

Show:
- Current manifest contents
- Whether `skills/` submodule is present and up to date
- Which domain skills are active this session

## Rules

- Always confirm briefly before running git commands.
- Never show raw git output.
- After any operation, state the outcome in plain language.
