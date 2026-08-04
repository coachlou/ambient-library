# lifecycle

Two different things share this route: **folder operations** (making another
folder ambient and maintaining it) and **library rot detection** (auditing this
repo's own skills). Pick one.

## Folder operations — delegate

Stamp, incept (interview then stamp), install, personalize, learn, and update
are defined once, in the canonical domain skill. Read
`${CLAUDE_PLUGIN_ROOT}/library/ambient-folder/instructions.md` and follow it.

Do not restate those mechanics here. They live in `library/` rather than in this
subskill because a folder may need to vendor the capability into its own
`.ailib/` and stamp its sub-folders — a subskill can't travel; a domain skill
can.

## Sweep — detect rot in the canonical library

Stays here: it audits *this repository's* skills, not a target folder.

Context rots: model behavior shifts, tools deprecate, trigger phrases drift.
Update re-syncs vendored copies, but nothing checks whether the *canonical*
skills are still true. Sweep does, on request ("rot sweep", "what's stale").

1. **Find stale candidates by git age** — don't duplicate dates into files:
   `git log -1 --format=%as -- library/<skill>/` per catalog entry. Thresholds:
   domain skills 90 days; `.aai/` router, subskills, and `identity.md` 180
   days. A skill touched more recently is presumed fresh — skip it.
2. **Check each stale candidate against three questions:**
   - Do its referenced paths, tools, and commands still exist?
   - Would its catalog description still win routing for its real use cases?
   - Does it over-instruct current models (steps newer models no longer need)?
3. **Report, don't fix.** One ranked list — skill, age, failed question,
   one-line suggested remedy. Changing a description re-routes the whole
   catalog, so every fix is a deliberate follow-up via review.md, never part
   of the sweep itself.

## Distribution drift — a different question

Rot is about whether a skill is still *true* over time. Drift is about whether
its four files still *agree* right now. For drift, don't reason — run
`python3 scripts/audit-distribution.py` and report its output; fixes go through
`admin.md`, which owns all four files.

## Rules

- One operation per request.
- Report what changed in plain language: which files, which folder.
