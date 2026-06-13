# Getting Started

## Install (once)

From within Claude Code, run:

```
/plugin marketplace add coachlou/ambient-library
/plugin install ambient@ambient-library
```

The first command registers the marketplace; the second installs the `ambient`
plugin. After this, the skill is available in every project on this machine.

## First use

Open Claude Code in any project and say:

> "Set up ambient-library in this project"

Claude asks what your project does and writes an optional `skills-manifest.yaml`
scoping which domain skills the project uses. (Core capabilities work with or
without it.)

## Day-to-day

Just talk:

- *"Review this code"*
- *"Configure my skills"*
- *"Add code-review to this project"*
- *"Update my skills"* → runs `/plugin update ambient`

## Updating

```
/plugin update ambient
```

Pulls the latest skills and library.

## Next Steps

- **Install details** → [INSTALLATION.md](INSTALLATION.md)
- **Using skills** → [USAGE.md](USAGE.md)
- **Authoring skills** → [MANAGEMENT.md](MANAGEMENT.md)
- **How it works** → [../ARCHITECTURE.md](../ARCHITECTURE.md)
