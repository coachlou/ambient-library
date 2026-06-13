# Installation & Setup

## Prerequisites

- Git (already installed, probably)
- Claude Code or Claude running in your IDE
- Access to this repository (`git@github-coachlou:coachlou/ambient-library.git`)

## Step-by-Step Setup

### 1. Add Ambient Library as a Submodule

In your project root:

```bash
git submodule add git@github-coachlou:coachlou/ambient-library.git skills
```

This clones the skill library into a `skills/` folder. Git tracks it as a submodule, so it's always available but takes minimal space.

### 2. Create the Manifest

Create `skills-manifest.yaml` in your project root:

```yaml
skills:
  - skill-loader
  - skill-system-manager
  - code-review
  # Add more skills as needed
```

This tells the system which skills to activate for your project. You can add/remove skills anytime by editing this file.

### 3. Copy the Setup Script

Copy `setup-skills.sh` from ambient-library:

```bash
cp skills/setup-skills.sh .
chmod +x setup-skills.sh
```

Or if you already have it in your repo, ensure it's executable:

```bash
chmod +x setup-skills.sh
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

**That's it.** Skills are now available in your Claude sessions.

## Optional: Auto-Refresh on Session Start

To refresh skills at the start of every Claude session, create `.claude/hooks/session-start.sh`:

```bash
mkdir -p .claude/hooks
cat > .claude/hooks/session-start.sh << 'EOF'
#!/bin/bash
./setup-skills.sh >/dev/null 2>&1 || true
EOF
chmod +x .claude/hooks/session-start.sh
```

Add this to `.claude/settings.json` to enable hooks (if not already enabled):

```json
{
  "hooks": {
    "enabled": true
  }
}
```

Now skills refresh silently when you start a new Claude session.

## Cloning a Project with Ambient Library

If you're cloning a repo that already has ambient-library wired up:

```bash
git clone <project-url>
cd <project>
git submodule update --init --recursive
./setup-skills.sh
```

The submodule automatically initializes and skills are installed.

## Troubleshooting

### `setup-skills.sh` command not found

Ensure you're in the project root and the script is executable:

```bash
ls -l setup-skills.sh  # Check for 'x' permissions
chmod +x setup-skills.sh
```

### `Error: Submodule not found`

The submodule wasn't initialized. Run:

```bash
git submodule update --init --recursive
```

### Skills aren't loading / Claude can't find them

1. Verify the manifest file exists and lists skills:
   ```bash
   cat skills-manifest.yaml
   ```

2. Verify the setup ran:
   ```bash
   ls -la .agents/skills/
   ```

   You should see folders like `skill-loader/`, `skill-system-manager/`, etc.

3. Re-run setup:
   ```bash
   ./setup-skills.sh
   ```

4. Start a fresh Claude session (the skills are cached per session).

### SSH key errors when cloning

If you see `fatal: Could not read from remote repository`:

- Ensure your SSH key is registered on GitHub for the `coachlou` account
- Verify your `~/.ssh/config` has an entry for `github-coachlou` (see [SETUP NOTES](../README.md))
- Test the connection: `ssh -T git@github-coachlou`

## Next: Using Skills

Once setup is done, see [USAGE.md](USAGE.md) for how to invoke and use skills in your projects.
