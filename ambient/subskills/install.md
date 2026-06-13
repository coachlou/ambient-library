# install

Sets up ambient-library globally on the machine and in the current project.

## Steps

### 1. Ensure the global ambient skill is installed and current

```bash
curl -fsSL https://raw.githubusercontent.com/coachlou/ambient-library/main/install-global.sh | bash
```

Always run this — it's idempotent and keeps the global skill up to date. This is also the one-time machine setup for new users.

### 2. Check for git repo

```bash
ls .git 2>/dev/null
```

If missing, run `git init` before continuing.

### 3. Check if project is already set up

If `skills-manifest.yaml` already exists, skip to select. Tell the user: "Ambient Library is already set up. Let me help you configure your skills."

### 4. Add the skills submodule

```bash
git submodule add https://github.com/coachlou/ambient-library.git skills
```

If this fails, report the error and stop.

### 5. Create a minimal manifest

Write `skills-manifest.yaml` to the project root:

```yaml
domain_skills: []
# Add domain skills here. Run "configure my skills" to set these up.
```

### 6. Hand off to select

Immediately read and execute `subskills/select.md` to configure the manifest.

## Rules

- Always run the curl in step 1 — it updates the global skill on this machine and bootstraps new machines.
- Keep output minimal. Don't narrate git internals.
- `skills` is a fixed folder name — the submodule must be at `skills/`. Do not use a different path.
