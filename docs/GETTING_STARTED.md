# Getting Started

## Install (once)

ambient-library has one canonical library with separate runtime wrappers.

Claude Code:

```
/plugin marketplace add coachlou/ambient-library
/plugin install ambient@ambient-library
```

The first command registers the marketplace; the second installs the `ambient`
plugin at **user scope** — available in every project on this machine. To install
for a specific project or team instead, see [INSTALLATION.md](INSTALLATION.md).

Codex:

Install this repository as a Codex plugin from the plugin root. The Codex
manifest is `.codex-plugin/plugin.json`, and it registers the adapter skill in
`codex-skills/`.

## First use

Open Claude Code or Codex in any project and say:

> "Set up ambient-library in this project"

Claude asks what your project does and writes an optional `skills-manifest.yaml`
scoping which domain skills the project uses. (Core capabilities work with or
without it.)

## Day-to-day

Just talk:

- *"Review this code"*
- *"Configure my skills"*
- *"Add project-brief to this project"*
- *"Update my skills"* → points to the runtime's plugin update flow
- *"Save this as a skill"* → drafts a proposal from your work into staging (see [USAGE.md](USAGE.md))

## Updating

Claude Code uses `/plugin update ambient`. Codex uses the Codex plugin update
flow for the installed plugin. Both pull the latest wrappers and canonical
library.

## Next Steps

- **Install details** → [INSTALLATION.md](INSTALLATION.md)
- **Using skills** → [USAGE.md](USAGE.md)
- **Authoring skills** → [MANAGEMENT.md](MANAGEMENT.md)
- **How it works** → [../ARCHITECTURE.md](../ARCHITECTURE.md)
