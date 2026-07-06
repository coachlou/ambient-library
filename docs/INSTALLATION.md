# Installation

ambient-library ships runtime-specific plugin wrappers around one canonical
library. Install the wrapper for the runtime you use.

## Claude Code

```
/plugin marketplace add coachlou/ambient-library
/plugin install ambient@ambient-library
```

- The first command adds this GitHub repo as a plugin marketplace.
- The second installs the `ambient` plugin from it.

Claude Code fetches the plugin and stores it under `~/.claude/plugins/`. The
skill is then available in every session — no per-project setup, no scripts, no
dotfile edits.

## À-la-carte skill installs

Every domain skill in the library is also published as its own single-skill
plugin in the same marketplace:

```
/plugin install grill@ambient-library
/plugin install audit-mcp@ambient-library
```

Installing `aimm-commands` additionally registers all 54 AIMM prompts as real
slash commands (`/aimm-commands:skeptic`, `/aimm-commands:canon-lock`, ...) —
user-triggered, so they add no standing context.

Browse the full list with `/plugin` or in [SKILLS.md](../SKILLS.md). Tradeoff:
a standalone install registers that skill's description in standing context
(reliable direct triggering, small per-skill cost), while the `ambient` plugin
keeps all 38 at zero standing cost behind the router. Installing both is
harmless — the standalone skill simply wins direct triggers.

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

## Codex

The Codex wrapper is defined by:

```text
.codex-plugin/plugin.json
codex-skills/ambient/SKILL.md
```

Install this repository as a Codex plugin through your Codex plugin workflow.
The Codex plugin registers one `ambient` skill and delegates to the canonical
library under `skills/ambient/`.

## Other harnesses (pointer adapter)

For agents without a plugin system (Gemini CLI and others), use the pointer
adapter: a short block in the project's instruction file that routes matching
requests to the canonical library.

1. Clone this repo to a fixed location (one clone per machine):

   ```bash
   git clone https://github.com/coachlou/ambient-library ~/ambient-library
   ```

2. In your project, tell the agent:
   *"Read ~/ambient-library/skills/ambient/instructions.md and set up
   ambient-library in this project."*

The install flow copies [templates/AGENTS-pointer.md](../templates/AGENTS-pointer.md)
into the project's `AGENTS.md` with the library path pinned. From then on,
matching requests route automatically — same progressive disclosure as the
plugin: the pointer is the only standing context; the router, subskills, and
domain skills load on demand.

Update with `git pull` in the clone; every project pointing at it picks up the
new version immediately.

**Tradeoff to know:** a pointer is an instruction the model must remember to
follow, not a harness-enforced trigger. Expect it to miss indirect requests
more often than the registered skill does, especially in long sessions. If a
request that should route doesn't, name it: *"use the ambient library for
this."*

## Verify

Say *"set up ambient-library in this project"* — if your agent walks you through
project setup, the wrapper is working.

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

Claude Code:

```
/plugin update ambient
```

Codex updates follow the Codex plugin update flow for the installed plugin.
Either way, the update pulls the latest wrapper plus the canonical `library/`.

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
