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
| `user` (default) | `claude plugin install ambient@aai-library` | `~/.claude/settings.json` | You, in all projects |
| `project` | `claude plugin install ambient@aai-library --scope project` | `.claude/settings.json` | Anyone who clones this repo |
| `local` | `claude plugin install ambient@aai-library --scope local` | `.claude/settings.local.json` | You, in this project only (gitignored) |

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
Pointer installs (no plugin) update with `git -C ~/.ailib pull` instead.

### Enable a domain skill

Domain skills are opt-in: a skill runs on its own only where it is enabled (the
enabled set is defined in `load.md`). Pick the manifest by scope:

| User says | Manifest |
|-----------|----------|
| "for this project", "here", or no scope named | `<project root>/skills-manifest.yaml` |
| "everywhere", "globally", "for me", "user scope", "all projects" | `~/.aai/skills-manifest.yaml` |

1. Verify it exists: `${CLAUDE_PLUGIN_ROOT}/library/<skill-name>/instructions.md`.
2. Add its name to `domain_skills` in that manifest, creating the file as
   `domain_skills: []` first if it is missing.

Enabling writes a name, never a copy — the skill still resolves from the
library, so updates reach it. Pinning a copy into the project's `.ailib/` is
`lifecycle.md`'s vendor operation, only when the user asks for it.

Confirm: "Enabled [skill-name] for this project." / "…in every project."

### Disable a domain skill

Remove it from the manifest for the scope the user named. Scopes are a union,
so a skill enabled in the other manifest (or vendored into the project) keeps
running — say so, and offer to remove it there too. Confirm: "Disabled [skill-name]."

### Status

Show, labeled by scope: `~/.aai/skills-manifest.yaml`, the project's
`skills-manifest.yaml`, and any skills vendored or forked into the project's
`.ailib/` / `.aai/skills/`. List the rest of `catalog.yaml` separately as
available but not enabled.

## Rules

- Plugin updates go through `/plugin update`, not git or curl.
- Confirm briefly before editing either manifest.
- Report outcomes in plain language.
