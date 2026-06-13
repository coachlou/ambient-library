# ambient-library

A global skill system for Claude Code. One install on your machine — skills available everywhere, in every project.

**New here?** → [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md)

## How It Works

One global skill (`ambient`) routes all requests — project setup, skill configuration, code review, updates. Projects only need a single file: `skills-manifest.yaml`.

```
~/.claude/skills/ambient/    ← installed once on your machine
├── SKILL.md                 # always-active router
├── instructions.md          # routing logic
└── subskills/
    ├── load.md              # reads manifest, activates domain skills
    ├── install.md           # sets up ambient-library in a project
    ├── select.md            # configures skills-manifest.yaml
    ├── manage.md            # updates and maintenance
    └── review.md            # code review

your-project/
└── skills-manifest.yaml     ← the only project file needed
```

## Setup

**One-time machine setup:**

```bash
curl -fsSL https://raw.githubusercontent.com/coachlou/ambient-library/main/install-global.sh | bash
```

**Every new project — from Claude Code:**

> "Set up ambient-library in this project"

That's it.

## What You Can Say

| Say this | What happens |
|----------|-------------|
| "Set up ambient-library in this project" | Installs submodule, configures manifest |
| "Configure my skills" | Walks through manifest setup via conversation |
| "Review this code" | Runs code review with project standards |
| "Update my skills" | Pulls latest from ambient-library |
| "Refresh my skills" | Reloads manifest for this session |

## Repository Structure

```
ambient-library/
├── ambient/              # The global skill (installed via install-global.sh)
├── templates/            # Minimal project templates
│   └── skills-manifest.yaml
├── docs/                 # Documentation
├── install-global.sh     # One-time machine setup
├── SKILLS.md             # Domain skills catalog
├── ARCHITECTURE.md       # How the system works
└── README.md
```

## Documentation

- **[GETTING_STARTED.md](docs/GETTING_STARTED.md)** — Start here
- **[INSTALLATION.md](docs/INSTALLATION.md)** — Detailed setup
- **[USAGE.md](docs/USAGE.md)** — Using skills day-to-day
- **[MANAGEMENT.md](docs/MANAGEMENT.md)** — Adding and managing domain skills
- **[FAQ.md](docs/FAQ.md)** — Common questions
- **[SKILLS.md](SKILLS.md)** — Available domain skills
- **[ARCHITECTURE.md](ARCHITECTURE.md)** — System design
