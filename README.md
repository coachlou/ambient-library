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

The library is distributed from `coachlou/aai-library` (development happens
in `coachlou/ambient-library`; don't install from there). The user-scope
install every harness reads is a clone at `~/.ailib`:

```bash
git clone https://github.com/coachlou/aai-library ~/.ailib
```

Claude Code, on top of that:

```
/plugin marketplace add coachlou/aai-library
/plugin install ambient@aai-library
```

Codex:

Install `~/.ailib` (the clone above) as a Codex plugin through your Codex
plugin workflow. Its `.codex-plugin/plugin.json` exposes one Codex skill from
`codex-skills/`.

Other harnesses (Gemini CLI, etc.):

No plugin needed. Using the `~/.ailib` clone above, tell the agent in your
project: *"Read `~/.ailib/.aai/instructions.md` and set up ambient-library in
this project."* The install flow writes a pointer block
into the project's `AGENTS.md` so future requests route automatically. See
[docs/INSTALLATION.md](docs/INSTALLATION.md#other-harnesses-pointer-adapter).

Updating is two steps: `git pull` in `~/.ailib` (the library every harness
reads), then the harness wrapper — `/plugin update ambient` in Claude Code, or
the Codex plugin update flow. Pointer-adapter installs need only the `git pull`.

## Use

Just talk:

| Say this | What happens |
|----------|-------------|
| "Set up ambient-library in this project" | Scopes the project's skills |
| "Configure my skills" | Picks the right skills via a quick chat |
| "Review this code" | Code review with project standards |
| "Add a skill to this project" | Enables it in this project's manifest |
| "Enable grill everywhere" | Enables it in your user-scope manifest |
| "Use the grill skill" | Runs a library skill once, enabled or not |
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

Domain skills are opt-in. One runs on its own only where it is enabled: in
`~/.aai/skills-manifest.yaml` (every project), in a project's
`skills-manifest.yaml`, or by being vendored into the project's `.ailib/`. The
scopes add up. Enabling records a name — nothing is copied. Any skill still runs
when you name it.

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
