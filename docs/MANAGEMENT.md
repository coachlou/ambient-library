# Managing Skills

## Adding a Domain Skill

Domain skills extend the system for specific project needs — documentation generators, deployment workflows, custom linting rules, API-specific helpers, etc.

### 1. Create the skill folder in ambient-library

```bash
cd /path/to/ambient-library
mkdir my-skill
```

### 2. Write instructions.md

This is the skill logic — what Claude does when this skill is active:

```markdown
# My Skill

Brief description of what this skill does.

## When to activate

Describe what user requests this skill should respond to.

## Instructions

Step-by-step instructions for Claude...
```

Keep it focused. One skill, one class of work.

### 3. Commit to ambient-library

```bash
git add my-skill/
git commit -m "Add my-skill: brief description"
git push
```

### 4. Activate in a project

Add the skill name to the project's `skills-manifest.yaml`:

```yaml
domain_skills:
  - my-skill
```

Or from Claude Code: *"Add my-skill to this project"*

### 5. Update the skills submodule in the project

```bash
git submodule update --remote skills
```

Or from Claude Code: *"Update my skills"*

---

## Updating a Domain Skill

Edit `instructions.md`, commit, push to ambient-library:

```bash
cd /path/to/ambient-library
# edit my-skill/instructions.md
git add my-skill/instructions.md
git commit -m "Update my-skill: describe change"
git push
```

Projects pick up the change with: *"Update my skills"*

---

## Removing a Domain Skill

### From a project

Remove it from `skills-manifest.yaml`. Start a fresh session for the change to take effect.

### From ambient-library

```bash
cd /path/to/ambient-library
git rm -r my-skill/
git commit -m "Remove my-skill: reason"
git push
```

---

## Updating Core Subskills

Core subskills (`load`, `install`, `select`, `manage`, `review`) live in `ambient/subskills/`. To update one:

1. Edit the file in ambient-library
2. Commit and push
3. Each user re-runs the global install to update their machine:
   ```bash
   curl -fsSL https://raw.githubusercontent.com/coachlou/ambient-library/main/install-global.sh | bash
   ```

---

## Best Practices

**One skill, one class of work.** If a skill is growing too broad, split it.

**Instructions over cleverness.** Write clear, direct instructions. Claude follows explicit steps better than implied ones.

**Document the trigger.** Start `instructions.md` with a clear description of when the skill should activate and what user requests it handles.

**Test before committing.** Activate the skill in a real project session and verify it behaves as expected before pushing to ambient-library.
