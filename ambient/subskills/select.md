# select

Configures `skills-manifest.yaml` through a short conversation. Goal: activate
only the domain skills this project actually needs.

## Why this matters

Domain skills add instructions to context. Unnecessary ones waste tokens. Core
skills (install, select, manage, load, review) are always available globally —
they never go in the manifest.

## Steps

### 1. Discover available domain skills

Read `$AMBIENT_HOME/SKILLS.md` for the catalog. (Resolve `AMBIENT_HOME` per
load.md.) The domain skills are the ones listed under "Domain Skills."

### 2. Understand the project

If the project has files, run a quick `ls` for context. Then ask one question:

> "What does this project do, and what kinds of tasks will you mostly ask me to
> help with?"

### 3. Recommend a minimal manifest

Propose only the domain skills clearly relevant to their answer, each with a
one-line reason:

```yaml
domain_skills:
  - code-review   # you mentioned code quality is a priority
```

Ask: "Does this look right, or anything to add or remove?"

### 4. Write the manifest

On confirmation, write `skills-manifest.yaml` to the project root. Then activate
immediately by executing load.md for the current session.

Confirm: "Your skills are set and active. They'll load automatically every
session in this project."

## Rules

- Default to the smallest useful set. When in doubt, leave it out.
- If the user wants a skill not in the catalog, offer to create it (MANAGEMENT.md).
- If a manifest already exists, show it and ask what to change.
