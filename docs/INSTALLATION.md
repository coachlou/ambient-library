# Installation

## Install (from within Claude Code)

```
/plugin marketplace add coachlou/ambient-library
/plugin install ambient@ambient-library
```

- The first command adds this GitHub repo as a plugin marketplace.
- The second installs the `ambient` plugin from it.

Claude Code fetches the plugin and stores it under `~/.claude/plugins/`. The
skill is then available in every session — no per-project setup, no scripts, no
dotfile edits.

## Verify

Say *"set up ambient-library in this project"* — if Claude walks you through
project setup, it's working.

## Project setup (optional)

In any project, say *"set up ambient-library in this project"*. Claude writes an
optional `skills-manifest.yaml` that scopes which domain skills the project uses:

```yaml
domain_skills:
  - project-brief
```

Core capabilities (install, select, manage, review) work with or without this
file. The manifest only scopes domain skills.

## Updating

```
/plugin update ambient
```

Pulls the latest version of the plugin — skills, subskills, and the whole
`library/`.

## Uninstalling

```
/plugin uninstall ambient
```

## Troubleshooting

### `/plugin` command not found
Update Claude Code to the latest version, then retry.

### The skill doesn't trigger
Confirm it's installed: run `/help` and look for `ambient`. If missing, re-run
the install commands above and start a fresh session.

### Marketplace add fails
Check the repo is reachable: `coachlou/ambient-library` must be a public GitHub
repo (or you must have access). You can also add by full URL:
`/plugin marketplace add https://github.com/coachlou/ambient-library`.

### Changes to a skill aren't showing
Run `/plugin update ambient`, then `/reload-plugins` (or start a fresh session).
