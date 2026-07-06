# manage

Updates and maintains the ambient-library system and a project's skill selection.

## Operations

### Check install scopes

To see which scopes the plugin is currently installed at:

```
claude plugin list
```

The output shows each installed plugin and its scope(s). Look for `ambient`.

### Change or add an installation scope

The plugin can be installed at one or more scopes simultaneously:

| Scope | Command | Settings file | Who gets it |
|-------|---------|---------------|-------------|
| `user` (default) | `claude plugin install ambient@ambient-library` | `~/.claude/settings.json` | You, in all projects |
| `project` | `claude plugin install ambient@ambient-library --scope project` | `.claude/settings.json` | Anyone who clones this repo |
| `local` | `claude plugin install ambient@ambient-library --scope local` | `.claude/settings.local.json` | You, in this project only (gitignored) |

Running the install command at a scope that already has it is safe — it's a no-op.

**Gotchas:**
- `--scope project` → commit `.claude/settings.json` to the repo so teammates get it.
- Project-scope plugins only activate when Claude Code is launched from the directory containing `.claude/settings.json`. Run from the repo root.
- After installing at a new scope, run `/reload-plugins` or start a fresh session.

### Remove from a scope

```
claude plugin uninstall ambient --scope <scope>
```

Use `--scope user`, `--scope project`, or `--scope local`. If this is the last scope, the plugin data directory is also removed (pass `--keep-data` to preserve it).

### Update the plugin to the latest version

Updates are handled by Claude Code's plugin system. Tell the user to run:

```
/plugin update ambient
```

(Or `/plugin` → manage → update.) This pulls the latest skills, subskills, and
library. Confirm: "Once you run /plugin update ambient, you'll have the latest."

### Add a domain skill to this project

1. Verify it exists: `${CLAUDE_PLUGIN_ROOT}/library/<skill-name>/instructions.md`.
2. Add its name to `domain_skills` in the project's `skills-manifest.yaml`.

Confirm: "Added [skill-name] for this project."

### Remove a domain skill from this project

Remove it from `skills-manifest.yaml`. Confirm: "Removed [skill-name]."

### Status

Show: the project's `skills-manifest.yaml` contents (if any) and the domain
skills available in `${CLAUDE_PLUGIN_ROOT}/library/`.

## Rules

- Plugin updates go through `/plugin update`, not git or curl.
- Confirm briefly before editing the manifest.
- Report outcomes in plain language.
