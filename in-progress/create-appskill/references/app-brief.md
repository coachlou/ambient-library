# App Brief — extends the Skill Brief

Fill after the base Skill Brief (`references/context-contract.md`). Save both together as the app-skill's `CONTEXT.md`. Source order is the same: conversation → filesystem → batched questions.

```markdown
## App Brief: <app-name>

### Persona & conversation contract
- Who the orchestrator is, in one sentence; tone.
- Opening move: <what it says first, what it offers>
- Finds vs asks: <context it reads itself vs questions it asks, batched>
- Progress reporting: <when it narrates delegation vs stays quiet>

### Parts inventory (all must exist in the folder before the orchestrator is written)
| Kind | Name | File | Purpose | Inputs -> Outputs |
|------|------|------|---------|-------------------|
| tool (script) | | scripts/ | | |
| resource | | references/ | | |
| sub-skill | | skills/<n>/SKILL.md | | |
| subagent | | agents/<n>.md | | |

### Routing table (user intent -> part)
| Intent / trigger phrasing | Route | Delegate? | Side-effects needing confirmation |
|---------------------------|-------|-----------|-----------------------------------|

### Shared state
- State file and schema; who reads, who writes (orchestrator only).

### Orchestration evals
- 2–3 multi-part requests + which parts must be invoked; 1 near-miss answered with no delegation.
```
