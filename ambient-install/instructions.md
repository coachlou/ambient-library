# ambient-install

Installs the ambient-library skill system into the current project, then hands off to skill-picker to build the manifest.

## Steps

### 1. Check prerequisites

Verify you are in a project directory:
- If no `.git` folder exists, run `git init` before proceeding.
- Confirm the user wants to proceed before running any commands.

### 2. Check if already installed

```bash
ls skills/.git 2>/dev/null
```

If `skills/` already exists as a submodule, skip to Step 4 (skill-picker).

### 3. Run bootstrap

```bash
git submodule add git@github-coachlou:coachlou/ambient-library.git skills
bash skills/bootstrap.sh
```

Report what was installed. If bootstrap fails, surface the error and stop — do not continue.

### 4. Hand off to skill-picker

Immediately invoke the skill-picker skill to configure `skills-manifest.yaml` for this project.

Tell the user: "Skill system installed. Now let's configure which skills your project needs."

### Rules

- Never skip the skill-picker step — an unconfigured manifest loads all skills, which wastes context.
- If the user is already in a project with code, glance at the file structure before skill-picker runs so it has context to make good recommendations.
- Keep technical output minimal. Don't narrate git internals.
