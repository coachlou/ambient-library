# FAQ & Quick Reference

## General Questions

### What is Ambient Library?

A central skill library for Claude Code. Skills are reusable tools (code review, custom workflows, docs generation, etc.) that you add to projects once and use forever.

### How is this different from other tool systems?

- **Centralized** — One source of truth for all skills
- **Invisible** — You don't manage paths, git mechanics, or loading logistics
- **Project-aware** — Skills merge with your project's rules automatically
- **Scalable** — Add new skills once, available to all projects

### Does it work offline?

Skills are stored locally in `.agents/skills/` after setup, so yes — Claude loads them offline. To update skills from ambient-library, you need internet access for `git submodule update`.

---

## Installation Questions

### How long does setup take?

~5 minutes if you know your way around git. If it's your first time:
1. Read [GETTING_STARTED.md](GETTING_STARTED.md) (2 min)
2. Follow [INSTALLATION.md](INSTALLATION.md) (5 min)
3. Done

### Can I use ambient-library without git?

No. Git submodules are core to the design — they keep skills in sync across projects without duplicating storage.

### What if I can't access github-coachlou:coachlou/ambient-library.git?

You need:
- SSH key registered on the `coachlou` GitHub account
- `~/.ssh/config` configured with the `github-coachlou` alias

See [INSTALLATION.md#SSH](INSTALLATION.md#ssh-key-errors-when-cloning) for details.

### Can I use this with other projects/teams?

Yes. The ambient-library repo is a normal git repo. You can:
- Fork it and customize for your team
- Maintain multiple versions
- Create a private copy for your org

---

## Using Skills

### How do I know what skills are available?

```bash
ls -la .agents/skills/
cat .agents/skills/SKILL.md  # Read the skill description
```

Or check the [Skills List](SKILLS.md) (if you create one).

### Do I need to activate skills manually?

No. All skills listed in `skills-manifest.yaml` are automatically active. Start a Claude session and use them.

### Can I use a skill in multiple projects?

Yes. Just add its name to `skills-manifest.yaml` in each project.

### What if a skill doesn't work?

1. Check [INSTALLATION.md#Troubleshooting](INSTALLATION.md#troubleshooting)
2. Verify it's in the manifest and installed:
   ```bash
   ./setup-skills.sh
   ls -la .agents/skills/
   ```
3. Start a fresh Claude session (skills are cached per session)

---

## Managing Skills

### How do I add a custom skill?

Follow [MANAGEMENT.md#Adding a New Skill](MANAGEMENT.md#adding-a-new-skill). TL;DR:
1. Copy `code-review/` as a template
2. Edit `SKILL.md` and `instructions.md`
3. Add to `skills-manifest.yaml`
4. Run `./setup-skills.sh`
5. Test, then commit to ambient-library

### What's the difference between editing instructions.md and SKILL.md?

- **SKILL.md** — Metadata (name, description, version). Describes what the skill does.
- **instructions.md** — The actual skill logic. How it works.

Change `instructions.md` to improve the skill. Change `SKILL.md` to rename it, change the description, or bump the version.

### Can I delete a skill?

Yes. Remove its folder from ambient-library, commit, and projects will stop seeing it on the next `git submodule update`.

### How do I know when skills are updated?

Watch the `ambient-library` repo or check the version numbers in `SKILL.md`. When a skill version bumps, you can pull the update:

```bash
git submodule update --remote
./setup-skills.sh
```

---

## Troubleshooting

### Skills aren't loading

Check the basics:
```bash
ls -la .agents/skills/          # Are pointers there?
cat skills-manifest.yaml        # Is the skill listed?
./setup-skills.sh               # Re-run setup
```

Then start a fresh Claude session (skills cache per session).

### `git submodule add` fails

SSH key or GitHub access issue. Test:
```bash
ssh -T git@github-coachlou
```

If that fails, check [INSTALLATION.md#SSH](INSTALLATION.md#ssh-key-errors-when-cloning).

### Cloning a project gives submodule errors

Run:
```bash
git submodule update --init --recursive
./setup-skills.sh
```

### I edited a skill but changes aren't showing up

Restart your Claude session. Skills cache per session.

### The submodule is out of sync with my local changes

Ambient-library is a shared resource. Don't edit skills directly in the submodule. Instead:
1. Copy the skill folder out of `skills/`
2. Edit it locally
3. Test it
4. Commit it back to ambient-library
5. Run `./setup-skills.sh` to pick up the change

---

## Advanced

### Can I create private skills (not in ambient-library)?

Yes, but we don't recommend it. The whole point is centralization. If you need a private skill:
1. Create a parallel folder at the project level
2. Manually reference it in your project's CLAUDE.md
3. Load it in Claude sessions as needed

Better: contribute it to ambient-library so the team benefits.

### Can I version skills independently?

Yes. Each skill has its own version number in `SKILL.md`. Ambient-library itself isn't versioned — it moves forward continuously. If you need a locked version:

```bash
git submodule set-url skills git@github-coachlou:coachlou/ambient-library.git@v1.0.0
```

(Note: you'd need to create git tags in ambient-library for this to work.)

### How do I measure if a skill is being used?

Not built-in. You'd need to add logging to the skill's `instructions.md` to track invocations.

---

## Still Have Questions?

- **Installation help** → [INSTALLATION.md](INSTALLATION.md)
- **Adding a skill** → [MANAGEMENT.md](MANAGEMENT.md)
- **Using skills** → [USAGE.md](USAGE.md)
- **System design** → [ambient-library/README.md](../README.md)
