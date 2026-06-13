# Installation & Setup

## Prerequisites

- Git
- Claude Code or Claude running in your IDE
- SSH access to `git@github-coachlou:coachlou/ambient-library.git`

## Option A: One-Command Setup (Recommended)

First, navigate to your project root (all commands must run from here):

```bash
cd your-project-root
```

Then add the library and run bootstrap:

```bash
git submodule add git@github-coachlou:coachlou/ambient-library.git skills
bash skills/bootstrap.sh
```

> **Note:** `skills` at the end of the submodule command is the local folder name it clones into. Don't change it — `setup-skills.sh` expects the submodule to be at `skills/`. If you rename it, the script will break.

`bootstrap.sh` handles everything: copying templates, making scripts executable, installing skill pointers, and printing next steps.

---

## Option B: Manual Step-by-Step

Use this if you want to control exactly which template files get copied, or if `bootstrap.sh` doesn't fit your workflow.

### 1. Add Ambient Library as a Submodule

Make sure you're in your project root first, then run:

```bash
git submodule add git@github-coachlou:coachlou/ambient-library.git skills
```

> **Note:** `skills` is the local folder name the library clones into. Don't rename it — `setup-skills.sh` hardcodes this path. Changing it will break the setup script.

### 2. Copy the Project Templates

All template files live in `skills/templates/`. Copy what you need:

```bash
cp skills/templates/setup-skills.sh .
cp skills/templates/skills-manifest.yaml .
cp skills/templates/CLAUDE.md .
cp skills/templates/.gitignore .
mkdir -p .claude/hooks
cp skills/templates/.claude/settings.json .claude/settings.json
cp skills/templates/.claude/hooks/session-start.sh .claude/hooks/session-start.sh
chmod +x setup-skills.sh .claude/hooks/session-start.sh
```

**Template files:**

| File | Purpose |
|------|---------|
| `setup-skills.sh` | Installs skill pointers from the manifest |
| `skills-manifest.yaml` | Controls which skills are active for this project |
| `CLAUDE.md` | Project context for Claude — edit to add project rules |
| `.gitignore` | Excludes `.agents/skills/` from git |
| `.claude/settings.json` | Enables session hooks |
| `.claude/hooks/session-start.sh` | Auto-refreshes skills at the start of each Claude session |

### 3. Edit the Manifest

`skills-manifest.yaml` controls which skills are active. Edit as needed:

```yaml
skills:
  - skill-loader          # required — do not remove
  - skill-system-manager
  - code-review
  # Add more skills here
```

### 4. Run Setup

```bash
./setup-skills.sh
```

You should see:

```
🔄 Setting up magical skill system...
  ✓ Installed pointer: skill-loader
  ✓ Installed pointer: skill-system-manager
  ✓ Installed pointer: code-review
✅ Skill system is ready.
```

**That's it.** Start a Claude session — skills are active.

---

## Cloning a Project with Ambient Library

If you're cloning a repo that already has ambient-library wired up:

```bash
git clone <project-url>
cd <project>
git submodule update --init --recursive
./setup-skills.sh
```

---

## Updating Skills

To pull the latest skills from ambient-library:

```bash
git submodule update --remote skills
./setup-skills.sh
```

---

## Troubleshooting

### `setup-skills.sh` command not found

Ensure you're in the project root and the script is executable:

```bash
chmod +x setup-skills.sh
```

### `Error: Submodule not found`

The submodule wasn't initialized. Run:

```bash
git submodule update --init --recursive
```

### Skills aren't loading / Claude can't find them

1. Verify the manifest exists and lists skills:
   ```bash
   cat skills-manifest.yaml
   ```

2. Verify pointers were installed:
   ```bash
   ls -la .agents/skills/
   ```

3. Re-run setup:
   ```bash
   ./setup-skills.sh
   ```

4. Start a fresh Claude session (skills are cached per session).

### SSH key errors when cloning

If you see `fatal: Could not read from remote repository`:

- Ensure your SSH key is registered on GitHub for the `coachlou` account
- Verify `~/.ssh/config` has a `github-coachlou` host alias
- Test: `ssh -T git@github-coachlou`

### Session hook isn't running

Verify the hook file exists and is executable:

```bash
ls -la .claude/hooks/session-start.sh
chmod +x .claude/hooks/session-start.sh
```

Verify hooks are enabled in `.claude/settings.json`:

```json
{
  "hooks": {
    "enabled": true
  }
}
```

---

## Next: Using Skills

See [USAGE.md](USAGE.md) for how to invoke skills in your Claude sessions.
