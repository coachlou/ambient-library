# ambient-library

A runtime-agnostic library of agents, skills, and reusable capabilities. It ships
thin plugin wrappers for Claude Code and Codex, while the canonical library stays
in one place. Project setup, skill selection, management, and code review all
work through natural language.

**New here?** → [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md)

## Install

Claude Code:

```
/plugin marketplace add coachlou/ambient-library
/plugin install ambient@ambient-library
```

Codex:

The Codex wrapper lives in `.codex-plugin/plugin.json` and exposes one Codex
skill from `codex-skills/`. Install it through your Codex plugin workflow from
this plugin root, or add it to a Codex marketplace when publishing.

Other harnesses (Gemini CLI, etc.):

No plugin needed. Clone this repo to a fixed location, then in your project
tell the agent: *"Read `<clone>/skills/ambient/instructions.md` and set up
ambient-library in this project."* The install flow writes a pointer block
into the project's `AGENTS.md` so future requests route automatically. See
[docs/INSTALLATION.md](docs/INSTALLATION.md#other-harnesses-pointer-adapter).

Claude updates are `/plugin update ambient`. Codex updates follow the Codex
plugin update flow for the installed plugin. Pointer-adapter installs update
with `git pull` in the clone.

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

Each runtime registers one skill (`ambient`) — so only one skill description sits
in context. Everything else (the router's subskills, and every domain skill) is a
plain file in the canonical library, read on demand. Nothing else loads into
context until it's actually needed.

```
ambient-library/                  (canonical library + runtime wrappers)
├── .claude-plugin/
│   ├── plugin.json               # Claude Code plugin manifest
│   └── marketplace.json          # Claude Code marketplace
├── .codex-plugin/
│   └── plugin.json               # Codex plugin manifest
├── codex-skills/
│   └── ambient/SKILL.md          # Codex adapter skill
└── skills/
    └── ambient/
        ├── SKILL.md              # Claude Code adapter skill
        ├── instructions.md       # canonical router
        ├── subskills/            # install, select, manage, load, review, admin
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
