# FAQ

## Setup

### How long does this take to set up?

Two minutes.

1. Run one terminal command to install globally (~30 seconds)
2. Say "Set up ambient-library in this project" in Claude Code (~1 minute)
3. Answer one question about your project

Done.

### Do I need to install anything on each project?

No. The `ambient` skill is global — installed once on your machine, available everywhere. The only per-project file is `skills-manifest.yaml`, which Claude creates for you.

### Do I need a GitHub account or SSH keys?

No. The install command uses HTTPS. No account or SSH setup required.

### Can I use this without the terminal at all?

Almost. The one-time machine setup requires a terminal command. After that, everything is done from Claude Code via natural language.

### What if I'm on a new machine?

Run the install command again:
```bash
curl -fsSL https://raw.githubusercontent.com/coachlou/ambient-library/main/install-global.sh | bash
```

---

## Using Skills

### How do I know what skills are available?

Check [../SKILLS.md](../SKILLS.md) for the full catalog.

Or ask: *"What skills are available?"*

### Do I have to activate skills manually each session?

No. The `ambient` skill reads your `skills-manifest.yaml` automatically at the start of every session. Domain skills load silently.

### Can I use skills without a manifest?

Yes. Core skills (install, select, manage, review) are always available even with no manifest. The manifest only controls which domain skills load.

### What's the difference between core skills and domain skills?

**Core skills** are always available globally — install, select, manage, review. They work in any project, any session.

**Domain skills** are project-specific — they add extra context or instructions for a particular project's needs. They're listed in `skills-manifest.yaml` and loaded per project.

---

## The Manifest

### What goes in skills-manifest.yaml?

Only domain skills specific to your project:

```yaml
domain_skills:
  - code-review
  - my-custom-skill
```

Core skills don't go here — they're always available.

### Where does skills-manifest.yaml live?

In your project root. That's the only file ambient-library needs in your project.

### What if it doesn't exist?

Claude Code still works normally. Core skills are available. Domain skills just won't load until you create the manifest (say *"Configure my skills"*).

---

## Troubleshooting

### "Set up ambient-library" doesn't trigger anything

The `ambient` skill isn't installed globally yet. Run:
```bash
curl -fsSL https://raw.githubusercontent.com/coachlou/ambient-library/main/install-global.sh | bash
```
Then start a fresh Claude Code session.

### Skills aren't loading

1. Check that `ambient` is installed: `ls ~/.claude/skills/ambient/`
2. Check that `skills-manifest.yaml` exists in your project root
3. Start a fresh Claude Code session (skills load at session start)

### Skills missing after cloning a project on a new machine

The project only carries `skills-manifest.yaml`. The skills themselves live in
the canonical library, so make sure it's installed on the machine:
```bash
curl -fsSL https://raw.githubusercontent.com/coachlou/ambient-library/main/install-global.sh | bash
```

### How do I update to the latest skills?

From Claude Code: *"Update my skills to the latest"*

Or re-run the global install to update core subskills:
```bash
curl -fsSL https://raw.githubusercontent.com/coachlou/ambient-library/main/install-global.sh | bash
```

---

## Advanced

### Can I add project-specific rules?

Yes. Add a `CLAUDE.md` to your project root. The `ambient` skill merges its contents automatically before executing any operation.

### Can I create private domain skills?

Yes. Create an `instructions.md` anywhere in your project and manually add the skill's path to your `CLAUDE.md`. It won't be in the ambient-library catalog but will work locally.

Better: contribute it to ambient-library so the whole team benefits.

### Can multiple projects use different skill versions?

No — by design. All projects on a machine share the one canonical clone at
`$AMBIENT_HOME`, so they always run the same version. Updating (`git pull`)
updates everything at once. This is the trade for zero per-project setup. If you
genuinely need divergent versions, install a second clone at a different
`AMBIENT_HOME` and point specific projects at it via their `CLAUDE.md`.

---

## Questions not answered here?

- **Setup** → [INSTALLATION.md](INSTALLATION.md)
- **Adding skills** → [MANAGEMENT.md](MANAGEMENT.md)
- **How it works** → [../ARCHITECTURE.md](../ARCHITECTURE.md)
