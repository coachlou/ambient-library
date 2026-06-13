# FAQ

## Setup

### How long does this take to set up?

About a minute, all from within Claude Code:

```
/plugin marketplace add coachlou/ambient-library
/plugin install ambient@ambient-library
```

Then say *"set up ambient-library in this project"* in any project.

### Do I need to install anything per project?

No. The plugin installs once and is available everywhere. A project's only
(optional) file is `skills-manifest.yaml`, which scopes its domain skills.

### Do I need a GitHub account or SSH keys?

No. Claude Code fetches the plugin for you over HTTPS.

### Can I do this without the terminal?

Yes — entirely. `/plugin marketplace add` and `/plugin install` run inside
Claude Code.

### What about a new machine?

Run the same two `/plugin` commands. Plugins are per-machine.

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

### The `/plugin` command doesn't exist

Update Claude Code to the latest version.

### How do I update?

```
/plugin update ambient
```

### A skill edit isn't showing

`/plugin update ambient`, then `/reload-plugins` or a fresh session.

---

## Advanced

### Can I add project-specific rules?

Yes. Add a `CLAUDE.md` to your project root. The router merges it before acting.

### Can I create private domain skills?

Yes. Put an `instructions.md` in your project and reference it from `CLAUDE.md`.
It won't be in the plugin catalog but works locally. Better: contribute it to the
plugin's `library/` so the whole team gets it.

### Can projects use different skill versions?

Plugins are versioned per machine, so all projects on a machine share the
installed plugin version. Update everything at once with `/plugin update ambient`.

---

## More

- **Setup** → [INSTALLATION.md](INSTALLATION.md)
- **Authoring skills** → [MANAGEMENT.md](MANAGEMENT.md)
- **How it works** → [../ARCHITECTURE.md](../ARCHITECTURE.md)
