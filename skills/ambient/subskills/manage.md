# manage

Updates and maintains the ambient-library system and a project's skill selection.

## Operations

### Update the plugin to the latest version

Updates are handled by Claude Code's plugin system. Tell the user to run:

```
/plugin update ambient
```

(Or `/plugin` → manage → update.) This pulls the latest skills, subskills, and
library. Confirm: "Once you run /plugin update ambient, you'll have the latest."

### Add a domain skill to this project

1. Verify it exists: `${CLAUDE_SKILL_DIR}/library/<skill-name>/instructions.md`.
2. Add its name to `domain_skills` in the project's `skills-manifest.yaml`.

Confirm: "Added [skill-name] for this project."

### Remove a domain skill from this project

Remove it from `skills-manifest.yaml`. Confirm: "Removed [skill-name]."

### Status

Show: the project's `skills-manifest.yaml` contents (if any) and the domain
skills available in `${CLAUDE_SKILL_DIR}/library/`.

## Rules

- Plugin updates go through `/plugin update`, not git or curl.
- Confirm briefly before editing the manifest.
- Report outcomes in plain language.
