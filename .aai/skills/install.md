# install

Sets up ambient-library for the current project: records which skills the
project wants and confirms everything is ready.

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

### 1. Determine how you were loaded

**Plugin harness** (Claude Code, Codex): `${CLAUDE_PLUGIN_ROOT}` or the plugin
adapter resolved this file. Nothing to clone or download — the skills,
subskills, and `library/` all live in the installed plugin. Continue to step 2.

**Pointer harness** (any other agent — you reached this file via a path the
user gave you or an existing AGENTS.md pointer): the library root is the
repository root this file's `.aai/` directory sits under — resolve it to
an absolute path. If the project's `AGENTS.md` (or equivalent instruction file)
doesn't yet reference the library, copy the template at
`<library root>/templates/AGENTS-pointer.md` into it, replacing
`{{LIBRARY_ROOT}}` with that absolute path. This pins the library location so
future sessions route automatically without the user pointing you here.

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

- Project artifacts are `skills-manifest.yaml` (optional) and, on pointer
  harnesses only, the AGENTS.md pointer block.
- On plugin harnesses: no clone, no submodule, no scripts, no dotfile edits.
  The plugin is the install.
- Keep output minimal.
