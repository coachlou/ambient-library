# Skill Brief: create-appskill

## Purpose
Create and improve skills and app-skills (conversational orchestrators over bundled scripts, references, sub-skills, subagents), layered over Anthropic's skill-creator.

## Origin
Merges the former `create-skill` (a full fork of upstream skill-creator plus routing gate, brief, step classification, rubric, packaging checks) and `create-appskill` (app-skill overrides). Upstream is now vendored unmodified (see `UPSTREAM.md`); everything else is overlay in `instructions.md`.

## Invocation
Triggers: "create a skill", "turn this into a skill", "create an appskill", "app-skill", "improve/audit/eval this skill". Near-misses: one-line CLAUDE.md rules, hooks, one-off scripts.
Inputs: a description of the skill/app, or an existing skill path (`--improve`). Output: a skill folder under `in-progress/<name>/` of the dev clone (or user-named path). No side effects beyond file writes; never pushes.

## Known gotchas
- Upstream's workflow uses bare relative paths; they resolve only because upstream's files live at the same paths here. Keep it that way.
- `agentic-ambient-intelligence/canonical-library/` is a stale rsync copy; author in `ambient-library/`.
- Subagents spawned from a subagent work only if the orchestrator is general-purpose or the main session.
