# ambient-library

A global skill system for Claude Code. One install on your machine — skills available everywhere, in every project.

**New here?** → [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md)

## How It Works

One canonical clone of the library lives on your machine at `$AMBIENT_HOME`
(default `~/ambient-library`). A thin pointer in `~/.claude/skills/` tells Claude
where to find it. Nothing is copied per project — every skill, with all its
sibling files, stays in the one clone. Projects need a single file:
`skills-manifest.yaml`.

```
$AMBIENT_HOME/                 ← one clone, the source of truth
└── ambient/
    ├── SKILL.md               # canonical frontmatter
    ├── instructions.md        # router
    └── subskills/             # load, install, select, manage, review

~/.claude/skills/ambient/SKILL.md   ← thin pointer into the clone
~/.zshrc                            ← exports AMBIENT_HOME
~/.claude/CLAUDE.md                 ← records AMBIENT_HOME

your-project/
└── skills-manifest.yaml       ← the only project file needed
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
| "Set up ambient-library in this project" | Ensures the library is current, writes & configures the manifest |
| "Configure my skills" | Walks through manifest setup via conversation |
| "Review this code" | Runs code review with project standards |
| "Update my skills" | Pulls latest from ambient-library |
| "Refresh my skills" | Reloads manifest for this session |

## Repository Structure

```
ambient-library/
├── ambient/              # The global skill: router + subskills
├── templates/            # Minimal project template (skills-manifest.yaml)
├── docs/                 # Documentation
├── install-global.sh     # Machine setup: clone, pointer, AMBIENT_HOME
├── SKILLS.md             # Skills catalog (core + domain)
├── ARCHITECTURE.md       # How the system works
└── README.md
```

Domain skills, when added, live as top-level folders here (each with its own
`instructions.md` and any sibling files) and resolve from `$AMBIENT_HOME` in
every project.

## Documentation

- **[GETTING_STARTED.md](docs/GETTING_STARTED.md)** — Start here
- **[INSTALLATION.md](docs/INSTALLATION.md)** — Detailed setup
- **[USAGE.md](docs/USAGE.md)** — Using skills day-to-day
- **[MANAGEMENT.md](docs/MANAGEMENT.md)** — Adding and managing domain skills
- **[FAQ.md](docs/FAQ.md)** — Common questions
- **[SKILLS.md](SKILLS.md)** — Available domain skills
- **[ARCHITECTURE.md](ARCHITECTURE.md)** — System design
