# ambient-library

A Claude Code plugin. Project setup, skill selection, management, and code review
— all through natural language. Install once; available in every project.

**New here?** → [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md)

## Install

From within Claude Code:

```
/plugin marketplace add coachlou/ambient-library
/plugin install ambient@ambient-library
```

That's the whole install. Updates are `/plugin update ambient`.

## Use

Just talk:

| Say this | What happens |
|----------|-------------|
| "Set up ambient-library in this project" | Scopes the project's skills |
| "Configure my skills" | Picks the right skills via a quick chat |
| "Review this code" | Code review with project standards |
| "Add a skill to this project" | Updates the project's skill list |
| "Update my skills" | Reminds you to run `/plugin update ambient` |

## How It Works

One registered skill (`ambient`) — so only one skill description sits in context.
Everything else (the router's subskills, and every domain skill) is a plain file
inside the plugin, read on demand via `${CLAUDE_SKILL_DIR}`. Nothing else loads
into context until it's actually needed.

```
ambient-library/                  (the plugin)
├── .claude-plugin/
│   ├── plugin.json               # plugin manifest
│   └── marketplace.json          # so it installs as a marketplace
└── skills/
    └── ambient/
        ├── SKILL.md              # the ONE registered skill (1 description)
        ├── instructions.md       # router (loads when ambient triggers)
        ├── subskills/            # install, select, manage, load, review
        └── library/              # domain skills — plain data, read on demand
            └── <skill>/instructions.md
```

A project's only artifact is an optional `skills-manifest.yaml` scoping which
domain skills it uses.

## Documentation

- **[GETTING_STARTED.md](docs/GETTING_STARTED.md)** — Install and first use
- **[INSTALLATION.md](docs/INSTALLATION.md)** — Install details + troubleshooting
- **[USAGE.md](docs/USAGE.md)** — Day-to-day commands
- **[MANAGEMENT.md](docs/MANAGEMENT.md)** — Authoring domain skills
- **[FAQ.md](docs/FAQ.md)** — Common questions
- **[SKILLS.md](SKILLS.md)** — Skills catalog
- **[ARCHITECTURE.md](ARCHITECTURE.md)** — How it works
