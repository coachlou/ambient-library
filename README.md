# ambient-library

> **Status: this repo is THE canonical library.** Corrected 2026-08-11 — an
> earlier banner here said the canonical library had moved to
> `coachlou/aai-framework` under `canonical-library/`. That was wrong in both
> directions, and the two repos spent a month each pointing at the other as the
> real one. `aai-framework/canonical-library/` is an **rsync copy** of this
> repo's `library/` (its own `MANIFEST.md` says so); it has no router, no
> `admin.md`, and no marketplace, so nothing committed there is installable.
> Develop here.
>
> **Dev and production are different things, not two clones.** This repo is the
> source. The production library is *built* from it:
>
> | | |
> |---|---|
> | `RELEASE.yaml` | explicit list of what ships — nothing else does |
> | `scripts/build-production.sh` | assembles production from `HEAD` and rsyncs it into place |
>
> Committing a skill does not release it. Releasing is a separate one-line edit
> to `RELEASE.yaml`, reviewable as a diff, reversible by deleting the line and
> rebuilding. The build drops `admin.md` and `propose.md`, so a production
> library cannot author — not by policy, but because the files are not there.

A runtime-agnostic library of agents, skills, and reusable capabilities. It ships
thin plugin wrappers for Claude Code and Codex, packaging the canonical
library for global, harness-agnostic access. Project setup, skill
selection, management, and code review all work through natural language.

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
tell the agent: *"Read `<clone>/.aai/instructions.md` and set up
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
ambient-library/                  (the canonical library + runtime wrappers)
├── .aai/                         # OWNED: this folder's own agentic intelligence
│   ├── instructions.md           #   canonical router
│   ├── identity.md               #   the folder's identity/soul
│   └── skills/                   #   install, select, manage, load, review, admin, propose, lifecycle
├── in-progress/                  # WORK IN FLIGHT: not catalogued, not routable, not shipped
├── library/                      # domain skills — plain data, read on demand
│   ├── <skill>/instructions.md
├── .claude-plugin/
│   ├── plugin.json               # Claude Code plugin manifest
│   └── marketplace.json          # Claude Code marketplace
├── .codex-plugin/
│   └── plugin.json               # Codex plugin manifest
├── codex-skills/
│   └── ambient/SKILL.md          # Codex adapter skill
└── skills/
    └── ambient/SKILL.md          # Claude Code adapter skill
```

A project's only artifact is an optional `skills-manifest.yaml` scoping which
domain skills it uses.

The library also grows from real work: after a task no skill covered, *"save this
as a skill"* drafts one from the session trace into `in-progress/`, where a
reviewed *"promote"* moves it into the catalog. Proposals stay inert until then —
never routed, never in the catalog.

## Documentation

- **[GETTING_STARTED.md](docs/GETTING_STARTED.md)** — Install and first use
- **[INSTALLATION.md](docs/INSTALLATION.md)** — Install details + troubleshooting
- **[USAGE.md](docs/USAGE.md)** — Day-to-day commands
- **[MANAGEMENT.md](docs/MANAGEMENT.md)** — Authoring domain skills
- **[FAQ.md](docs/FAQ.md)** — Common questions
- **[SKILLS.md](SKILLS.md)** — Skills catalog
- **[ARCHITECTURE.md](ARCHITECTURE.md)** — How it works
