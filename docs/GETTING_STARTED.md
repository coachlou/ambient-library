# Getting Started with Ambient Library

Ambient Library is a central skills system for Claude Code. Skills are reusable tools you can add to any project — code review, documentation, custom workflows, whatever you need.

## Quick Setup (5 minutes)

You have a project? Here's how to add ambient-library to it:

```bash
cd your-project-root
git submodule add git@github-coachlou:coachlou/ambient-library.git skills
cp /path/to/skills-manifest.yaml .  # (provided separately or use example below)
./setup-skills.sh
```

Done. All skills are now available in your project.

## What You Get

Three skills come built-in:

- **Skill Loader** — Always-active orchestration. Handles everything transparently.
- **Skill System Manager** — Manages updates and skill refreshes.
- **Code Review** — Thorough code reviews (correctness, security, performance, style).

You can add more skills to `ambient-library/` anytime and they'll be available to all projects.

## Next Steps

- **New to the system?** → [INSTALLATION.md](INSTALLATION.md) for detailed walkthrough
- **Want to use a skill?** → [USAGE.md](USAGE.md) for how to invoke them
- **Adding a custom skill?** → [MANAGEMENT.md](MANAGEMENT.md) for contributing
- **Something broken?** → See Troubleshooting in [INSTALLATION.md](INSTALLATION.md)

## The Invisible Part

This system is designed to be **zero-friction**. You never think about:
- Where skills are stored (submodules, pointers, git mechanics)
- How they load (caching, path resolution)
- Technical plumbing

It just works. If you hit something weird, check [INSTALLATION.md](INSTALLATION.md) → Troubleshooting.
