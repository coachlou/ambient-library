# Getting Started

## Install (once)

From within Claude Code, run:

```
/plugin marketplace add coachlou/ambient-library
/plugin install ambient@ambient-library
```

The first command registers the marketplace; the second installs the `ambient`
plugin at **user scope** — available in every project on this machine. To install
for a specific project or team instead, see [INSTALLATION.md](INSTALLATION.md).

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
- *"Add project-brief to this project"*
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
