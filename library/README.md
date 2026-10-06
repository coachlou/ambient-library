# Domain Skills Library

Each subfolder here is a domain skill: a project-specific capability the `ambient`
router reads on demand. They are plain instruction files, **not** registered
Claude Code skills, so they add nothing to context until the router reads one.

## Layout

```
library/
├── catalog.yaml             # cheap index: skill name → one-line description
├── _shared/                 # dev-only source for assets 3+ skills carry; never ships
└── <skill-name>/
    ├── instructions.md      # required — the skill logic, never shared
    ├── shared/              # byte-identical copies from _shared/, audit-checked
    └── references/ etc.     # optional sibling files the skill reads
```

Sharing rules (procedure stays per skill, only context-free assets pool, rule of
three with copies) live in `.aai/skills/admin.md` → "Shared assets".

Each skill folder is also its own plugin (`<skill-name>@aai-library`). The root
`SKILL.md` is the dev source for that; the production build copies its
frontmatter to `skills/<skill-name>/SKILL.md`, the only path plugin loaders
register. Don't add that folder here by hand.

Sibling files resolve at runtime as `${CLAUDE_PLUGIN_ROOT}/library/<skill-name>/<file>`
— reference them that way inside `instructions.md`, never with repo-relative or
absolute paths, so the skill works from both the installed plugin and a
pointer-adapter clone.

`catalog.yaml` is the **only** file the router reads to decide which skill a
request needs. It then loads exactly one skill's `instructions.md`. This is how
context stays lean — the full library never loads, only the one selected skill.

## Adding one

See [../../../docs/MANAGEMENT.md](../../../docs/MANAGEMENT.md). In short: create
`<skill-name>/instructions.md`, describe when it applies and what it does, commit,
and bump the plugin version so users get it via `/plugin update`.
