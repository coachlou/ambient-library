# ai-skills

Central reusable skill library for Claude Code projects.

## Structure

```
ai-skills/
├── skill-loader/        # Always-active orchestration layer
├── skill-system-manager/ # Handles updates and maintenance
├── code-review/         # Example skill — duplicate for new skills
└── README.md
```

## Adding to a project

```bash
git submodule add https://github.com/YOURUSERNAME/ai-skills.git skills
./setup-skills.sh
```

## Adding a new skill

1. Copy `code-review/` as a template
2. Edit `SKILL.md` frontmatter (name, description, version)
3. Write skill logic in `instructions.md`
4. Add the skill name to `skills-manifest.yaml` in your project
5. Run `./setup-skills.sh`
