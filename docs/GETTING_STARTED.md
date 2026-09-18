# Getting Started

## Install (once)

ambient-library has one canonical library with separate runtime wrappers.
Always install from the distribution repo `coachlou/aai-library`, never the dev
repo `coachlou/ambient-library`.

Every harness reads the library from a user-scope clone:

```bash
git clone https://github.com/coachlou/aai-library ~/.ailib
```

Claude Code, on top of that:

```
/plugin marketplace add coachlou/aai-library
/plugin install ambient@aai-library
```

The first command registers the marketplace; the second installs the `ambient`
plugin at **user scope** — available in every project on this machine. To install
for a specific project or team instead, see [INSTALLATION.md](INSTALLATION.md).

Codex:

Install `~/.ailib` as a Codex plugin. Its manifest is
`.codex-plugin/plugin.json`, which registers the adapter skill in
`codex-skills/`.

Other harnesses (Gemini CLI, etc.) need no plugin — see
[INSTALLATION.md](INSTALLATION.md#other-harnesses-pointer-adapter).

## First use

Open Claude Code or Codex in any project and say:

> "Set up ambient-library in this project"

Claude asks what your project does and writes a `skills-manifest.yaml`
enabling the domain skills the project uses. Domain skills are opt-in: only
enabled ones run on their own, though any skill runs when you name it. Core
capabilities (install, select, manage, review) always work.

For skills you want in every project, say *"enable <skill> everywhere"* — that
writes `~/.aai/skills-manifest.yaml` instead.

A skill that needs a detail from you — a sender address, a group name — asks
once, saves the answer in the project, and never asks again. Nothing in the
skill's own files is edited. See
[USAGE.md](USAGE.md#personalizing-a-skill).

## Day-to-day

Just talk:

- *"Review this code"*
- *"Configure my skills"*
- *"Add project-brief to this project"* / *"Enable project-brief everywhere"*
- *"Use the grill skill"* → runs a library skill once, enabled or not
- *"Update my skills"* → points to the runtime's plugin update flow
- *"Save this as a skill"* → drafts a proposal from your work into staging (see [USAGE.md](USAGE.md))

## Updating

Run `git pull` in `~/.ailib` to update the library itself. Then update the
wrapper: `/plugin update ambient` in Claude Code, or the Codex plugin update
flow.

## Next Steps

- **Install details** → [INSTALLATION.md](INSTALLATION.md)
- **Using skills** → [USAGE.md](USAGE.md)
- **Authoring skills** → [MANAGEMENT.md](MANAGEMENT.md)
- **How it works** → [../ARCHITECTURE.md](../ARCHITECTURE.md)
