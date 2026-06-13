# install

Sets up ambient-library in the current project. Creates the manifest and adds the skills submodule.

## Steps

### 1. Check for git repo

```bash
ls .git 2>/dev/null
```

If missing, run `git init` before continuing.

### 2. Check if already installed

If `skills-manifest.yaml` already exists, skip to select. Tell the user: "Ambient Library is already set up. Let me help you configure your skills."

### 3. Add the skills submodule

```bash
git submodule add https://github.com/coachlou/ambient-library.git skills
```

If this fails, report the error and stop.

### 4. Create a minimal manifest

Write `skills-manifest.yaml` to the project root:

```yaml
domain_skills: []
# Add domain skills here. Run "configure my skills" to set these up.
```

### 5. Hand off to select

Immediately read and execute `subskills/select.md` to configure the manifest.

## Rules

- Keep output minimal. Don't narrate git internals.
- `skills` is a fixed folder name — the submodule must be at `skills/`. Do not use a different path.
- Confirm briefly before running commands if the user hasn't explicitly asked to proceed.
