# Domain Skills Library

Each subfolder here is a domain skill: a project-specific capability the `ambient`
router reads on demand. They are plain instruction files, **not** registered
Claude Code skills, so they add nothing to context until the router reads one.

## Layout

```
library/
└── <skill-name>/
    ├── instructions.md      # required — the skill logic
    └── references/ etc.     # optional sibling files the skill reads
```

## Adding one

See [../../../docs/MANAGEMENT.md](../../../docs/MANAGEMENT.md). In short: create
`<skill-name>/instructions.md`, describe when it applies and what it does, commit,
and bump the plugin version so users get it via `/plugin update`.
