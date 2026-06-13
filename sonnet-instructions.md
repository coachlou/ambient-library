

---

```markdown
# AI Skills System – Complete Setup Guide (Magical & Opaque)
**Goal**: A central reusable skill library using Git submodules + lightweight pointers + invisible orchestration. 
The user never sees technical details (paths, submodules, pointers, loading, etc.). Everything feels like normal built-in skills.
### 1. Create the Central Skills Repository (One Time)
1. Create a new Git repository (GitHub recommended) called `ai-skills`.
2. Use this exact folder structure:
```

ai-skills/
├── skill-loader/
│ ├── SKILL.md
│ └── instructions.md
├── skill-system-manager/
│ ├── SKILL.md
│ └── instructions.md
├── code-review/ # ← Example skill (add more as needed)
│ ├── SKILL.md
│ └── instructions.md
├── README.md

```
#### skill-loader/SKILL.md
```yaml
---
name: Skill Loader
description: Orchestrates all skills transparently. Handles pointer resolution, caching, and project rules.
version: 1.0
priority: highest
always_active: true
---
You are the Skill Loader — an invisible orchestration layer.
At the start of every conversation:
1. Confirm Skill System Manager is available.
2. If needed, silently ask Skill System Manager to refresh the skill system.
When any skill is requested or relevant:
- Silently resolve its instructions_path.
- Merge rules from the current project's AGENTS.md / CLAUDE.md.
- Cache the loaded skill for this conversation.
- Never mention paths, pointers, SKILL.md, submodules, git, loading mechanics, or any technical details unless the user explicitly asks about the system itself.
- Act as if every skill is a normal, fully-loaded capability.
```

#### skill-system-manager/SKILL.md

```yaml
---
name: Skill System Manager
description: Manages initialization, updates, and maintenance of the entire skill system.
version: 1.0
priority: high
---
You are the Skill System Manager.
Available operations (use only when user requests or Skill Loader determines it is necessary):
- Initialize skills submodule
- Update skills to latest version
- Refresh skill pointers
- Add or remove skills from the manifest
Rules:
- Always confirm briefly with the user before running commands (e.g. "Updating skills library...").
- Run commands safely inside the current project folder.
- Never show raw git output or technical paths.
- After success, reply only: "Skill system is now up to date and ready."
- Stay invisible about implementation details.
```

#### Example Skill (code-review/SKILL.md)

```yaml
---
name: Code Review
description: Performs thorough, constructive code reviews focusing on correctness, security, performance, readability, and project standards.
version: 2.3
instructions_path: ./instructions.md
---
```

(You can duplicate this pattern for any new skill.)
---

### 2. Project Setup (Do This in Every New Project)

Run these commands in your project root:

```bash
# 1. Add the central skills as a submodule
git submodule add https://github.com/YOURUSERNAME/ai-skills.git skills
# 2. Create the required files (copy from below)
```

#### skills-manifest.yaml

```yaml
skills:
 - skill-loader
 - skill-system-manager
 - code-review
 # Add any other skills you want for this project
```

#### .gitignore

```gitignore
# Generated lightweight skill pointers
.agents/skills/
```

#### setup-skills.sh

```bash
#!/bin/bash
set -e
PROJECT_DIR="${1:-.}"
MANIFEST="$PROJECT_DIR/skills-manifest.yaml"
SUBMODULE_PATH="$PROJECT_DIR/skills"
TARGET_DIR="$PROJECT_DIR/.agents/skills"
echo "🔄 Setting up magical skill system..."
if [ ! -d "$SUBMODULE_PATH" ]; then
 echo "Error: Submodule not found. Run: git submodule update --init --recursive"
 exit 1
fi
mkdir -p "$TARGET_DIR"
rm -rf "$TARGET_DIR"/*
while IFS= read -r skill || [ -n "$skill" ]; do
 skill=$(echo "$skill" | xargs)
 [[ -z "$skill" || "$skill" == \#* ]] && continue
 SOURCE="$SUBMODULE_PATH/$skill"
 TARGET="$TARGET_DIR/$skill"
 if [ -f "$SOURCE/SKILL.md" ]; then
 mkdir -p "$TARGET"
 cp "$SOURCE/SKILL.md" "$TARGET/SKILL.md"
 echo " ✓ Installed pointer: $skill"
 else
 echo " ✗ Warning: Skill $skill not found"
 fi
done < <(grep -oP '^\s*-\s*\K.+' "$MANIFEST" || true)
echo "✅ Skill system is ready."
```

Make executable:

```bash
chmod +x setup-skills.sh
```

#### .claude/hooks/session-start.sh (recommended)

```bash
#!/bin/bash
# Runs automatically at the start of every Claude session
./setup-skills.sh >/dev/null 2>&1 || true
```

Make executable:

```bash
mkdir -p .claude/hooks
chmod +x .claude/hooks/session-start.sh
```

---

### 3. Project AGENTS.md / CLAUDE.md (Put at Root)

```markdown
# Project Context
You are operating inside a project with the full magical skill system.
- The Skill Loader is always active with highest priority.
- All skills work transparently. Use them naturally.
- Never mention technical details (paths, git, submodules, pointers, SKILL.md, loading, etc.) unless the user specifically asks about the system.
- Always read this file first for project-specific rules, architecture, and conventions.
```

---

### 4. Daily Usage (What the User Says)

- “Update my skills to the latest version”
- “Refresh the skill system”
- “Add the deploy skill to this project”
- “Review this code using Code Review”
- “Initialize skills in this project”
  The Skill Loader + Skill System Manager will handle everything invisibly.

---

### 5. Maintenance Commands (Run Manually When Needed)

```bash
# After cloning a project
git submodule update --init --recursive
./setup-skills.sh
# Update skills to latest
git submodule update --remote
./setup-skills.sh
```

---

**You are done.**
Implement this structure exactly as written. Use the file contents verbatim. Do not add extra explanation unless the user asks.
Start by creating the central `ai-skills` repository first, then set up one project to test.
```
---


