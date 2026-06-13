# Getting Started with Ambient Library

Ambient Library is a central skills system for Claude Code. Skills are reusable tools you can add to any project — code review, documentation, custom workflows, whatever you need.

## Quick Setup (5 minutes)

You have a project? Two commands:

```bash
cd your-project-root
git submodule add git@github-coachlou:coachlou/ambient-library.git skills
bash skills/bootstrap.sh
```

Done. All skills are now available in your Claude sessions.

## What bootstrap.sh Does

1. Copies all project template files to your root (`setup-skills.sh`, `skills-manifest.yaml`, `CLAUDE.md`, `.gitignore`, `.claude/` hooks)
2. Makes scripts executable
3. Runs `setup-skills.sh` to install skill pointers into `.agents/skills/`
4. Prints next steps

## What You Get

Three skills come built-in:

- **Skill Loader** — Always-active orchestration. Handles everything transparently.
- **Skill System Manager** — Manages updates and skill refreshes on request.
- **Code Review** — Thorough code reviews (correctness, security, performance, style).

You can add more skills to `ambient-library/` anytime and they'll be available to all projects.

## Next Steps

- **Want to use a skill?** → [USAGE.md](USAGE.md)
- **Adding a custom skill?** → [MANAGEMENT.md](MANAGEMENT.md)
- **Full installation details?** → [INSTALLATION.md](INSTALLATION.md)
- **Something broken?** → [INSTALLATION.md#troubleshooting](INSTALLATION.md#troubleshooting)
- **See all available skills** → [../SKILLS.md](../SKILLS.md)

## The Invisible Part

This system is designed to be **zero-friction**. You never think about:
- Where skills are stored (submodules, pointers, git mechanics)
- How they load (caching, path resolution)
- Technical plumbing

It just works. If you hit something weird, check [INSTALLATION.md#troubleshooting](INSTALLATION.md#troubleshooting).
