# ambient-library

Central reusable skill library for Claude Code projects. Skills are reusable tools you add to any project once — code review, custom workflows, documentation, whatever your team needs.

**New here?** → Start with [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md)

## What's Inside

```
ambient-library/
├── skill-loader/        # Always-active orchestration layer
├── skill-system-manager/ # Manages updates and refreshes
├── code-review/         # Example skill (customize or duplicate)
├── docs/                # User documentation
│   ├── GETTING_STARTED.md   # First-time setup
│   ├── INSTALLATION.md      # Detailed installation & troubleshooting
│   ├── USAGE.md             # How to use skills
│   ├── MANAGEMENT.md        # Adding & maintaining skills
│   └── FAQ.md               # Common questions
└── README.md
```

## Quick Start

**Set up a project with ambient-library:**

```bash
cd your-project-root
git submodule add git@github-coachlou:coachlou/ambient-library.git skills
cp /path/to/skills-manifest.yaml .
./setup-skills.sh
```

All skills are now available in your Claude sessions.

**Add a custom skill:**

See [docs/MANAGEMENT.md](docs/MANAGEMENT.md) for the full walkthrough.

## Documentation

- **[GETTING_STARTED.md](docs/GETTING_STARTED.md)** — First time? Start here (5 min)
- **[INSTALLATION.md](docs/INSTALLATION.md)** — Step-by-step setup + troubleshooting
- **[USAGE.md](docs/USAGE.md)** — How to invoke and use skills
- **[MANAGEMENT.md](docs/MANAGEMENT.md)** — Add new skills, update existing ones
- **[FAQ.md](docs/FAQ.md)** — Common questions and quick reference

## Key Features

✨ **Invisible** — No manual path management, git mechanics, or loading overhead  
🤝 **Shared** — One central library, all projects use the same skills  
🔄 **Project-aware** — Skills merge with your project's rules automatically  
📦 **Modular** — Add skills as needed, no bloat  

## About This System

The system uses:
- **Git submodules** to keep skills in sync across projects
- **Skills manifest** (YAML) to control which skills are active per project
- **Lightweight pointers** in `.agents/skills/` for fast loading
- **Orchestration layer** to hide all the mechanics

You never think about any of it. Just use skills naturally in Claude.

## Need Help?

- **Getting started** → [GETTING_STARTED.md](docs/GETTING_STARTED.md)
- **Installation issues** → [INSTALLATION.md#Troubleshooting](docs/INSTALLATION.md#troubleshooting)
- **Adding a skill** → [MANAGEMENT.md](docs/MANAGEMENT.md)
- **General questions** → [FAQ.md](docs/FAQ.md)
