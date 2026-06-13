# install

Sets up ambient-library for the current project. The skill system itself is
already installed (it's a plugin) — this just records which skills the project
wants and confirms everything is ready.

## Steps

### 1. Confirm the plugin is active

You are running, so the plugin is installed. Nothing to clone or download — the
skills, subskills, and `library/` all live in `${CLAUDE_SKILL_DIR}`.

### 2. Check existing setup

If the project root has a `skills-manifest.yaml`, skip to select and offer to
review it.

### 3. Create a project manifest (optional but recommended)

Write `skills-manifest.yaml` to the project root to scope which domain skills
this project uses:

```yaml
domain_skills: []
# Domain skills this project uses. Run "configure my skills" to set these up.
```

Core capabilities (install, select, manage, review) always work without a
manifest. The manifest only scopes domain skills.

### 4. Hand off to select

Read and execute `select.md` to choose domain skills for the project.

## Rules

- The only project artifact is `skills-manifest.yaml`, and even that is optional.
- No clone, no submodule, no scripts, no dotfile edits. The plugin is the install.
- Keep output minimal.
