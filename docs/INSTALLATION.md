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

## Installation scopes

The default install (`/plugin install ambient@ambient-library`) installs at **user scope** — available to you in every project on this machine. Two other scopes are available:

| Scope | Command | Settings file | Who gets it |
|-------|---------|---------------|-------------|
| `user` (default) | `claude plugin install ambient@ambient-library` | `~/.claude/settings.json` | You, in all projects |
| `project` | `claude plugin install ambient@ambient-library --scope project` | `.claude/settings.json` | Anyone who clones this repo |
| `local` | `claude plugin install ambient@ambient-library --scope local` | `.claude/settings.local.json` | You, this project only (gitignored) |

You can install at multiple scopes simultaneously — the plugin is active as long as it's enabled at any one of them.

**Project scope gotchas:**
- Commit `.claude/settings.json` to the repo so teammates pick it up.
- Claude Code only loads a project-scoped plugin when launched from the directory containing `.claude/settings.json`. Launch from the repo root, not a subdirectory.
- Teammates see a trust prompt on first use — this is expected (same gate as project `CLAUDE.md`).

After installing at a new scope, run `/reload-plugins` or start a fresh session.

To check which scopes the plugin is installed at: `claude plugin list`.
To remove from a scope: `claude plugin uninstall ambient --scope <scope>`.

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
Say *"set up ambient-library in this project"* — if Claude doesn't respond to
that, the plugin isn't active. Re-run the install commands and start a fresh
session.

### Marketplace add fails
Check the repo is reachable: `coachlou/ambient-library` must be a public GitHub
repo (or you must have access). You can also add by full URL:
`/plugin marketplace add https://github.com/coachlou/ambient-library`.

### Changes to a skill aren't showing
Run `/plugin update ambient`, then `/reload-plugins` (or start a fresh session).
