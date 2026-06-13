# Managing Skills

## Adding a New Skill

### 1. Create the Skill Folder

Copy the `code-review/` template inside `ambient-library/`:

```bash
cd /path/to/ambient-library
cp -r code-review my-new-skill
cd my-new-skill
```

You now have:
```
my-new-skill/
├── SKILL.md         # Metadata and description
└── instructions.md  # The skill logic
```

### 2. Edit SKILL.md

Update the frontmatter to describe your skill:

```yaml
---
name: My New Skill
description: What this skill does. Describe the user intent, not the implementation.
version: 1.0
instructions_path: ./instructions.md
---
```

**Guidelines for `description`:**
- 1–2 sentences, max
- Describe what the user would ask for, not what the code does
- Examples:
  - ✅ "Generates a skeleton project with best-practice structure and configuration"
  - ❌ "Reads a template folder and scaffolds a new project"
  - ✅ "Reviews code for security vulnerabilities, logic errors, and performance issues"
  - ❌ "Analyzes files and produces a report"

### 3. Write instructions.md

The skill logic goes here. It can be:

**Prose instructions** (for skills that rely on Claude's reasoning):
```markdown
# Deploy to Production

When the user asks to deploy code, follow these steps:
1. Check for uncomitted changes (abort if found)
2. Run the test suite
3. Build the artifact
4. Upload to the deployment service
5. Verify the deployment health check

Rules:
- Never deploy from a dirty working tree
- Always require explicit confirmation before deploying
- Log the deployment ID for reference
```

**Code + prose** (for skills that need deterministic validation):
```markdown
# Schema Validator

Validates JSON files against a schema.

Usage:
\`\`\`bash
validate-schema.sh <file> <schema>
\`\`\`

... (script details)
```

**Custom workflows** (for domain-specific orchestration):
```markdown
# Database Migration Review

When the user submits a migration for review:
1. Read the migration file
2. Check for unsafe patterns (renaming columns without backfill, etc.)
3. Verify lock times
4. Suggest rollback procedures
5. Output a safety report
```

Keep it concise. If the skill logic is complex, consider whether it should be multiple smaller skills instead.

### 4. Add to Project Manifest

In the **project** using the skill (not in ambient-library), edit `skills-manifest.yaml`:

```yaml
skills:
  - skill-loader
  - skill-system-manager
  - code-review
  - my-new-skill  # ← Add here
```

### 5. Install and Test

```bash
./setup-skills.sh
```

Verify it installed:
```bash
ls -la .agents/skills/ | grep my-new-skill
```

Start a Claude session and test the skill by asking for what it does.

### 6. Commit to ambient-library

Once the skill is working, commit it to the central library:

```bash
cd /path/to/ambient-library
git add my-new-skill/
git commit -m "Add my-new-skill"
git push
```

Now all projects can use it.

## Updating a Skill

### Small changes (instructions only)

Edit `instructions.md`, test in a project session, commit:

```bash
cd /path/to/ambient-library
# Edit my-skill/instructions.md
git add my-skill/instructions.md
git commit -m "Improve my-skill instructions: add examples"
git push
```

In projects, refresh to pick up the change:

```bash
git submodule update --remote
./setup-skills.sh
```

### Major changes (name, version, description)

Update `SKILL.md`, bump the version:

```yaml
---
name: My Skill
description: (updated description)
version: 1.1  # ← bump this
instructions_path: ./instructions.md
---
```

Commit and push:

```bash
git add my-skill/SKILL.md my-skill/instructions.md
git commit -m "Bump my-skill to 1.1: add new use case"
git push
```

## Removing a Skill

If a skill is obsolete:

### 1. Remove from projects

In each project's `skills-manifest.yaml`, remove the skill name.

### 2. Remove from ambient-library

```bash
cd /path/to/ambient-library
git rm -r my-old-skill/
git commit -m "Remove my-old-skill: deprecated in favor of better-skill"
git push
```

### 3. Refresh projects

```bash
git submodule update --remote
./setup-skills.sh
```

## Versioning

Skills use semantic versioning:

- **1.0** — First release
- **1.1** — Bug fixes, minor improvements (backwards compatible)
- **2.0** — Breaking changes (new workflow, removed features, renamed commands)

Bump the version in `SKILL.md` whenever you change the skill. Projects will know an update is available by the version number.

## Best Practices

### Keep Skills Focused

One skill = one coherent class of work. If you're building something that touches multiple domains, split it into multiple skills.

### Document Your Assumptions

If the skill depends on specific tools, project structure, or configuration, call it out in `instructions.md`:

```markdown
# Prerequisites

- Project must have a `schema.sql` file in the root
- Node.js 18+
- The `@aidx/cli` package installed
```

### Provide Examples

If the skill has a non-obvious usage pattern, show it:

```markdown
## Usage Examples

**Deploy a single service:**
\`\`\`
"Deploy auth-service to staging"
\`\`\`

**Deploy everything:**
\`\`\`
"Deploy all services to production"
\`\`\`
```

### Test Before Pushing

Always test a new skill or update in a real project session before committing to ambient-library.

## Questions?

- **Skill won't load?** → Check [INSTALLATION.md#Troubleshooting](INSTALLATION.md#troubleshooting)
- **How does Skill Loader work?** → [ambient-library/README.md](../README.md)
