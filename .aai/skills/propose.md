# propose

Drafts a new skill from work just completed, into `library/_staging/`. This is
how the library learns — but a proposal is not a skill. It stays inert in
staging until `admin.md` promotes it.

## CRITICAL: never write to staging without an explicit yes

Writing a proposal is opt-in. Either the user asks ("save this as a skill",
"propose a skill from this", "remember how we did this"), or you *offer* in one
sentence after finishing a task no library skill covered — "No library skill
covered this; want me to draft one into staging?" Silence or anything short of
yes means no. Never auto-propose.

## CRITICAL: author from the trace, not from imagination

The draft must be built from what actually happened this session — the steps
taken, commands run, and corrections the user made. If the session lacks enough
substance (a one-liner task, pure Q&A, nothing repeatable), refuse: say there's
not enough trace to author from, and stop. A skill invented from a vague idea is
exactly the kind that underperforms and pollutes routing.

## Source clone only

Same as `admin.md`: proposals are library assets, so locate the source clone
first —

1. If the current project root is an ambient-library clone (has
   `.aai/instructions.md` and `.claude-plugin/plugin.json`), use it.
2. Otherwise ask for the clone's path. Don't clone one yourself, don't fall
   back to `${CLAUDE_PLUGIN_ROOT}`.

All paths below are relative to that clone.

## Steps

1. Pick a kebab-case `<name>`. If `library/<name>/` already exists as a real
   skill, this isn't new — stop and point the user at "update <name>" (admin).
2. If `library/_staging/<name>/` already exists, **do not overwrite**. Append to
   its `PROPOSAL.md` Evidence section instead — a repeated proposal is the
   strongest signal it deserves promotion — and stop.
3. Write `library/_staging/<name>/instructions.md`, same conventions as a real
   domain skill: a name/what-it-does opening, then imperative steps. Reference
   any sibling files as `${CLAUDE_PLUGIN_ROOT}/library/<name>/<file>` (the path
   it will have once promoted, not the staging path) — never repo-relative or
   absolute.
4. Write `library/_staging/<name>/PROPOSAL.md` with exactly these fields:
   - **Proposed description** — the one-line catalog entry it would get, phrased
     as *when it applies* (user intent, not implementation).
   - **Source trace** — date, project, and 2–3 sentences on the task it came from.
   - **Evidence** — what in the session shows the pattern is real and repeatable.
   - **Overlap check** — the nearest existing catalog entries and why they don't
     already cover this.

## Hard limits

- Never touch `catalog.yaml`, `SKILLS.md`, `marketplace.json`, or any plugin
  `version`. Those change only at promotion, in `admin.md`.
- Never edit an existing `library/<name>/` skill — that's `admin.md`.
- Write only under `library/_staging/<name>/`. Nothing else in the repo changes.

## Rules

- Explicit yes before any write. Trace before imagination. Existing proposal →
  append evidence, don't overwrite.
- When done, tell the user it's in staging and that "promote <name>" (in a clone
  session) reviews and moves it into the real library.
