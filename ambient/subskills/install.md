# install

Sets up ambient-library for the current project. The heavy lifting (cloning the
library, registering paths) is global and already done by `install-global.sh`;
this just gives the project its manifest.

## Steps

### 1. Ensure the global system is installed and current

```bash
curl -fsSL https://raw.githubusercontent.com/coachlou/ambient-library/main/install-global.sh | bash
```

Idempotent. This clones/updates the canonical library at `$AMBIENT_HOME`,
regenerates the global pointer, and records `AMBIENT_HOME` in `~/.zshrc` and
`~/.claude/CLAUDE.md`. For a brand-new machine, this is also the one-time setup.

### 2. Check if the project is already set up

If `skills-manifest.yaml` exists in the project root, skip to select. Tell the
user: "Ambient Library is already set up here — let's review your skills."

### 3. Create a minimal manifest

Write `skills-manifest.yaml` to the project root:

```yaml
domain_skills: []
# Domain skills for this project. Run "configure my skills" to set these up.
```

### 4. Hand off to select

Immediately read and execute `subskills/select.md` to configure the manifest.

## Rules

- No git submodule, no `git init`, no scripts copied into the project. The only
  project artifact is `skills-manifest.yaml`. Everything else resolves from
  `$AMBIENT_HOME`.
- Always run step 1 — it keeps the machine current and bootstraps new machines.
- Keep output minimal.
