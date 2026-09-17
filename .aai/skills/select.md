# select

Chooses which domain skills are enabled, for this project or for every project,
by writing a `skills-manifest.yaml`.

## Why this matters

Domain skills are opt-in: the router only picks skills enabled in a manifest
(or vendored into the project). Without one, a skill runs only when the user
names it. Scopes are a union — user-scope skills apply everywhere, and a
project manifest adds its own.

| Scope | Manifest |
|-------|----------|
| This project (default) | `<project root>/skills-manifest.yaml` |
| Every project ("everywhere", "globally", "for me") | `~/.aai/skills-manifest.yaml` |

## Steps

### 1. Discover available domain skills

Read `${CLAUDE_PLUGIN_ROOT}/library/catalog.yaml` — a cheap list of skill names and
one-line descriptions. Don't open individual skill `instructions.md` files here.

### 2. Understand the scope

For a project: if it has files, run a quick `ls` for context. Then ask one
question:

> "What does this project do, and what kinds of tasks will you mostly ask me to
> help with?"

For user scope, ask instead what kinds of tasks they want handled in every
project. If `~/.aai/skills-manifest.yaml` exists, don't re-propose its skills for
a project — they already apply.

### 3. Recommend a manifest

Propose only the domain skills clearly relevant, each with a one-line reason:

```yaml
domain_skills:
  - project-brief   # you mentioned you need a project overview
  - writer          # drafting content
```

Ask: "Does this look right, or anything to add or remove?"

### 4. Write the manifest

On confirmation, write the manifest for the chosen scope.

Confirm: "Your skills are set. I'll use these for this project." / "…in every project."

## Rules

- Default to the smallest useful set. When in doubt, leave it out.
- If the user wants a skill not in `library/`, offer to create it (see MANAGEMENT.md).
- If the manifest for that scope already exists, show it and ask what to change.
