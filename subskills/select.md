# select

Scopes which domain skills a project uses by writing `skills-manifest.yaml`.

## Why this matters

Domain skills are read on demand, so the cost is already low. The manifest scopes
which ones the router will consider for this project — useful for focus and for
applying project-specific skills consistently.

## Steps

### 1. Discover available domain skills

Read `${CLAUDE_PLUGIN_ROOT}/library/catalog.yaml` — a cheap list of skill names and
one-line descriptions. Don't open individual skill `instructions.md` files here.

### 2. Understand the project

If the project has files, run a quick `ls` for context. Then ask one question:

> "What does this project do, and what kinds of tasks will you mostly ask me to
> help with?"

### 3. Recommend a manifest

Propose only the domain skills clearly relevant, each with a one-line reason:

```yaml
namespaces:
  - writing         # this is a content project
domain_skills:
  - project-brief   # you mentioned you need a project overview
```

A `namespaces` entry scopes in a whole family from the catalog's
`namespaces:` map — prefer it over listing every member when the project
clearly needs the family.

Ask: "Does this look right, or anything to add or remove?"

### 4. Write the manifest

On confirmation, write `skills-manifest.yaml` to the project root.

Confirm: "Your skills are set. I'll use these for this project."

## Rules

- Default to the smallest useful set. When in doubt, leave it out.
- If the user wants a skill not in `library/`, offer to create it (see MANAGEMENT.md).
- If a manifest already exists, show it and ask what to change.
