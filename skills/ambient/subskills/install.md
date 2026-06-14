# install

Sets up ambient-library for the current project. The skill system itself is
already installed (it's a plugin) — this just records which skills the project
wants and confirms everything is ready.

## Scope — if the user is asking about WHERE to install

If the user says anything about "globally", "for the team", "project-wide",
"locally", or "which scope", give them the right command before doing anything
else:

| What they want | Command to give them |
|----------------|----------------------|
| Available to me in all projects (default) | `claude plugin install ambient@ambient-library` |
| Shared with the team via the repo | `claude plugin install ambient@ambient-library --scope project` |
| This project only, not committed to git | `claude plugin install ambient@ambient-library --scope local` |

**Gotchas to mention:**
- `--scope project` writes to `.claude/settings.json` — commit that file so teammates get it.
- Project-scope plugins only load when Claude Code is launched from the directory containing `.claude/settings.json`. Launch from the repo root.
- You can install at multiple scopes simultaneously (e.g., user + project). The skill runs as long as it's enabled at any scope.
- After installing at a new scope, run `/reload-plugins` or start a fresh session.

Once you've given them the command, stop — don't proceed to the manifest steps
below unless they confirm the plugin is running in the target session.

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
