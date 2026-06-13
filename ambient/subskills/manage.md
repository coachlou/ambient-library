# manage

Updates, refreshes, and maintains the ambient-library system.

## Resolving AMBIENT_HOME

Resolve `AMBIENT_HOME` per load.md (env var → CLAUDE.md → `~/ambient-library`).

## Operations

### Update the library to latest

Pull the latest into the canonical clone — this updates every project on the
machine at once, since they all resolve from it:

```bash
git -C "$AMBIENT_HOME" pull --ff-only
```

Then regenerate the global pointer in case the skill itself changed:

```bash
curl -fsSL https://raw.githubusercontent.com/coachlou/ambient-library/main/install-global.sh | bash
```

Confirm: "Skills updated to the latest version."

### Refresh skills

Re-execute load.md to reload domain skills for the current session. No git
needed. Confirm: "Skills refreshed."

### Add a skill to this project

1. Verify the skill exists: `$AMBIENT_HOME/<skill-name>/instructions.md`.
2. Add its name to `domain_skills` in `skills-manifest.yaml`.
3. Re-execute load.md to activate it now.

Confirm: "Added [skill-name] — it's active for this project."

### Remove a skill from this project

Remove it from `skills-manifest.yaml`. Tell the user to start a fresh session
for the change to fully take effect (skills cache per session).

### Status

Show: current manifest contents, `AMBIENT_HOME` path and whether the clone is
up to date (`git -C "$AMBIENT_HOME" status -sb`), and which domain skills are
active this session.

## Rules

- Confirm briefly before running git commands.
- Never show raw git output. Report outcomes in plain language.
