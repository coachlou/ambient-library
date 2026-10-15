# App-skill anatomy

```
<app-name>/
├── SKILL.md            # orchestrator: persona, conversation contract, routing table
├── CONTEXT.md          # Skill Brief + App Brief (provenance, seeds evals)
├── state.md            # optional; orchestrator-owned run state
├── agents/<n>.md       # subagent role prompts, self-contained
├── skills/<n>/SKILL.md # bundled sub-skills (read explicitly, not auto-discovered)
├── references/         # resources, loaded on demand
├── scripts/            # tools: deterministic code steps
├── assets/             # templates / output files
└── evals/evals.json    # incl. orchestration evals
```

This is the skill-creator layout (`agents/`, `references/`, `scripts/`, `assets/`) plus `skills/` for nesting and a routing table. Progressive disclosure still applies: the orchestrator body stays under ~500 lines and points to parts; parts load only when routed to.

## Routing table format (in the orchestrator's SKILL.md)

```markdown
| When the user wants... | Do |
|------------------------|----|
| a competitor teardown | spawn subagent `agents/analyst.md` with {company, depth}; summarize its result |
| a formatted report    | read `skills/report/SKILL.md`, follow it with the analyst's result |
| to refresh data       | run `scripts/fetch.py <args>`; read output |
| anything else         | answer directly, or ask once |
```

## Subagent prompt contract (`agents/<n>.md`)

First line: `Spawn with: subagent_type <general-purpose|Explore|...>` (left out, the orchestrator picks one itself; in testing it chose Explore). Then role in one line; the inputs it will receive; the exact output shape (JSON or headed markdown); what it must not do (talk to the user, write state, cause external effects). Spawn via the Agent tool, passing the file's contents plus the inputs.
