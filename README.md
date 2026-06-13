# ambient-library

Central reusable skill library for Claude Code projects. Skills are reusable tools you add to any project once — code review, custom workflows, documentation, whatever your team needs.

**New here?** → Start with [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md)

## What's Inside

```
ambient-library/
├── skill-loader/             # Always-active orchestration layer
├── skill-system-manager/     # Manages updates and refreshes
├── code-review/              # Example skill (customize or duplicate)
├── templates/                # Copy these into new projects
│   ├── setup-skills.sh           # Installs skill pointers from the manifest
│   ├── skills-manifest.yaml      # Controls which skills are active
│   ├── CLAUDE.md                 # Project context for Claude
│   ├── .gitignore                # Excludes generated .agents/skills/
│   └── .claude/
│       ├── settings.json         # Enables session hooks
│       └── hooks/
│           └── session-start.sh  # Auto-refreshes skills each session
├── docs/                     # User documentation
│   ├── GETTING_STARTED.md        # First-time setup
│   ├── INSTALLATION.md           # Detailed installation & troubleshooting
│   ├── USAGE.md                  # How to use skills
│   ├── MANAGEMENT.md             # Adding & maintaining skills
│   └── FAQ.md                    # Common questions
├── bootstrap.sh              # One-command project setup
├── SKILLS.md                 # Full catalog of available skills
├── ARCHITECTURE.md           # How the system works under the hood
└── README.md
```

## Quick Start

**One command — sets up everything:**

```bash
cd your-project-root
git submodule add git@github-coachlou:coachlou/ambient-library.git skills
bash skills/bootstrap.sh
```

That's it. Skills are active in your next Claude session.

**What bootstrap.sh does:**
- Copies all template files into your project root
- Makes scripts executable
- Runs `setup-skills.sh` to install skill pointers
- Prints next steps

**Add a custom skill:**

See [docs/MANAGEMENT.md](docs/MANAGEMENT.md) for the full walkthrough.

## Documentation

- **[GETTING_STARTED.md](docs/GETTING_STARTED.md)** — First time? Start here (5 min)
- **[INSTALLATION.md](docs/INSTALLATION.md)** — Step-by-step setup + troubleshooting
- **[USAGE.md](docs/USAGE.md)** — How to invoke and use skills
- **[MANAGEMENT.md](docs/MANAGEMENT.md)** — Add new skills, update existing ones
- **[FAQ.md](docs/FAQ.md)** — Common questions and quick reference
- **[SKILLS.md](SKILLS.md)** — Full catalog of available skills
- **[ARCHITECTURE.md](ARCHITECTURE.md)** — How the system works under the hood

## Key Features

✨ **Invisible** — No manual path management, git mechanics, or loading overhead  
🤝 **Shared** — One central library, all projects use the same skills  
🔄 **Project-aware** — Skills merge with your project's rules automatically  
📦 **Modular** — Add skills as needed, no bloat  
⚡ **One-command setup** — `bootstrap.sh` handles everything for new projects  

## Need Help?

- **Getting started** → [GETTING_STARTED.md](docs/GETTING_STARTED.md)
- **Installation issues** → [INSTALLATION.md#Troubleshooting](docs/INSTALLATION.md#troubleshooting)
- **Adding a skill** → [MANAGEMENT.md](docs/MANAGEMENT.md)
- **General questions** → [FAQ.md](docs/FAQ.md)
- **How it works** → [ARCHITECTURE.md](ARCHITECTURE.md)
