# FAQ

## Setup

### How long does this take to set up?

About a minute in Claude Code:

```
/plugin marketplace add coachlou/ambient-library
/plugin install ambient@ambient-library
```

Then say *"set up ambient-library in this project"* in any project.

For Codex, install this repository as a Codex plugin from the plugin root. The
Codex wrapper is `.codex-plugin/plugin.json`.

### Does this work on harnesses without plugins (Gemini CLI, etc.)?

Yes, via the pointer adapter: clone the repo once per machine, then point the
agent at `instructions.md` and ask it to set up the project. It
writes a short routing block into your project's `AGENTS.md`; after that,
matching requests route automatically. Triggering is instruction-based rather
than harness-enforced, so indirect requests miss more often than with the
plugin — if a request doesn't route, say *"use the ambient library for this."*
Details: [INSTALLATION.md](INSTALLATION.md#other-harnesses-pointer-adapter).

### Do I need to install anything per project?

No. The plugin installs once and is available everywhere. A project's only
(optional) file is `skills-manifest.yaml`, which scopes its domain skills.

### Do I need a GitHub account or SSH keys?

No. Claude Code fetches the plugin for you over HTTPS.

### Can I do this without the terminal?

Yes in Claude Code — `/plugin marketplace add` and `/plugin install` run inside
Claude Code. In Codex, use the Codex plugin installation flow.

### What about a new machine?

Run the runtime's plugin install flow again. Plugins are per-machine.

---

## Using Skills

### How do I know what skills are available?

Check [../SKILLS.md](../SKILLS.md), or ask *"what skills are available?"*

### Do I activate skills each session?

No. The `ambient` skill is always available. Domain skills load automatically
when a request matches one — nothing to invoke manually.

### Can I use skills without a manifest?

Yes. Core capabilities (install, select, manage, review) always work. A
`skills-manifest.yaml` only scopes which domain skills the router considers.

### What's the difference between core skills and domain skills?

**Core** — install, select, manage, review — are built into the `ambient` skill
and always available.

**Domain skills** are project-specific capabilities in the plugin's `library/`.
They're read on demand and optionally scoped per project via `skills-manifest.yaml`.

Runtime wrappers are different from both: they are the thin Claude Code or Codex
plugin layers that expose the canonical `ambient` skill.

---

## The Manifest

### What goes in skills-manifest.yaml?

The domain skills to scope to this project:

```yaml
domain_skills:
  - project-brief
```

Core capabilities aren't listed — they're always available.

### Where does it live?

Project root. It's the only ambient-library file in your project, and it's
optional.

### What if it doesn't exist?

Everything still works. The router can use any domain skill in `library/`; the
manifest just narrows the set.

---

## Troubleshooting

### "Set up ambient-library" doesn't do anything

The plugin may not be installed. Run:
```
/plugin marketplace add coachlou/ambient-library
/plugin install ambient@ambient-library
```
Then start a fresh session.

In Codex, verify the Codex plugin is installed and that `.codex-plugin/plugin.json`
points at `codex-skills/`.

### The `/plugin` command doesn't exist

Update Claude Code to the latest version. Codex uses its own plugin flow instead
of Claude Code's `/plugin` command.

### How do I update?

```
/plugin update ambient
```

In Codex, use the Codex plugin update flow for the installed plugin.

### A skill edit isn't showing

In Claude Code, run `/plugin update ambient`, then `/reload-plugins` or start a
fresh session. In Codex, update or reinstall the plugin and start a fresh thread
if needed.

---

## Advanced

### Can I add project-specific rules?

Yes. Add runtime-appropriate project guidance to your project root, such as
`CLAUDE.md` for Claude Code or `AGENTS.md` for Codex. The adapter/router merges
it before acting.

### Can I create private domain skills?

Yes. Put an `instructions.md` in your project and reference it from `CLAUDE.md`.
It won't be in the plugin catalog but works locally. Better: contribute it to the
plugin's `library/` so the whole team gets it.

### Can the library learn from my work?

Yes, with a review gate. After a task no skill covered, say *"save this as a
skill"* — the agent drafts one **from the actual session trace** into
`library/_staging/`. That's a proposal, not a live skill: it's never routed and
not in the catalog. In a clone session you review it and *"promote"* it into the
library or *"reject"* it. Nothing auto-promotes — self-generated skills
underperform unless authored from real work and reviewed, and an unvetted
catalog entry shifts routing for its neighbors. See [MANAGEMENT.md](MANAGEMENT.md)
"Self-extension".

### Can projects use different skill versions?

Plugins are versioned per machine and per runtime, so all projects using the same
installed runtime wrapper share that installed version. Update through the
runtime's plugin flow.

---

## More

- **Setup** → [INSTALLATION.md](INSTALLATION.md)
- **Authoring skills** → [MANAGEMENT.md](MANAGEMENT.md)
- **How it works** → [../ARCHITECTURE.md](../ARCHITECTURE.md)
