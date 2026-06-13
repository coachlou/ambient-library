# select

Configures `skills-manifest.yaml` through a short natural language conversation. Goal: activate only the domain skills this project actually needs.

## Why this matters

Domain skills add instructions to context. Unnecessary ones waste tokens. The manifest should be minimal and intentional. Core skills (install, select, manage, load, review) are always available globally — they don't need to be in the manifest.

## Steps

### 1. Discover available domain skills

Read `skills/SKILLS.md` if the submodule is present. If not, work from general knowledge of available skills.

### 2. Understand the project

If the project already has files, run a quick `ls` to get context. Then ask the user one question:

> "What does this project do, and what kinds of tasks will you mostly ask me to help with?"

### 3. Recommend a minimal manifest

Based on their answer, propose only the domain skills that are clearly relevant. Show each one with a one-line reason:

```yaml
domain_skills:
  - code-review   # you mentioned code quality as a priority
```

Ask: "Does this look right, or anything to add or remove?"

### 4. Write the manifest

Once confirmed, write `skills-manifest.yaml`:

```yaml
domain_skills:
  - skill-name
  # ...
```

Confirm: "Your skill manifest is set. These skills will load automatically in every session for this project."

## Rules

- Default to the smallest useful set. When in doubt, leave it out.
- Never add a skill just because it exists.
- If the user asks for a skill not in the library, tell them and offer to create it (see MANAGEMENT.md).
- If the manifest already exists, show current contents and ask what they'd like to change.
