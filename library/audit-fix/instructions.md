# Audit-Fix — adversarial audit through to root cause

An audit that stops at findings is half a job. This skill runs the full motion:
attack the artifact, keep only findings that earn their place, fix the survivors at
the root cause, and leave the surrounding docs consistent. The three beats are
inseparable — a list of unfixed findings and a pile of symptom patches are both
failure modes.

## Gotchas (read first)

- **The earn filter is a real gate, not a formality.** A finding earns its place only
  if acting on it changes the outcome. Style preferences, hypothetical edge cases
  nothing will hit, and "could also consider..." padding get discarded — *visibly*,
  with a one-line reason each. Showing the discards is what makes the filter
  trustworthy.
- **Root cause means the shared choke point.** Before fixing anything, find every
  path that reaches the defect (grep all callers, all docs referencing the stale
  fact, all copies of the duplicated logic). One fix where all paths route through
  beats N patches on the paths you noticed. A guard added only where the symptom
  appeared leaves every sibling path still broken.
- **Never weaken a verify to pass it.** If a test or verify command blocks a fix,
  fix the code. Correcting a verify's *path* is fine; changing what it checks is not.
- **Audit the actual artifact, not your memory of it.** Re-read the plan/diff/spec
  fresh before attacking it. Auditing from memory reproduces the same blind spots
  that created the defects.

## Step 0 — Identify the target and mode

- **Target**: a plan/spec (no code yet), a change (diff exists), or reasoning (a
  recommendation or analysis in this conversation). If ambiguous, the most recently
  produced artifact is the target.
- **Mode**: full (audit → fix → verify, the default) or **report-only** (user said
  "report only", "don't act", "just audit") — stop after Step 2 and present.

## Step 1 — Adversarial pass, six lenses

Attack the artifact as a hostile expert reviewer whose reputation depends on finding
what the author missed. Work lens by lens; adjacent lenses catch different defects:

1. **Errors** — things that are wrong: broken logic, false claims, code that won't run.
2. **Omissions** — required things that are absent: missing steps, unhandled inputs,
   absent acceptance criteria.
3. **Oversights** — things considered but handled carelessly: stale references,
   inconsistent naming, a case handled in one place but not its twin.
4. **Blind spots** — things structurally invisible from the author's position:
   unstated assumptions, the user class this breaks for, what happens at 10× scale
   or on a fresh machine. Ask "what would someone from a different discipline flag?"
5. **Conflicts** — internal contradictions, or collisions with locked decisions,
   existing code, or neighboring systems.
6. **Duplications** — the same logic/fact/instruction living in two places, guaranteed
   to drift.

For changes, also check the change's *neighbors*: what does this diff assume about
code it didn't touch?

## Step 2 — The earn filter

Sort every finding into:

- **Survivors** — acting on this changes the outcome. State the concrete failure it
  prevents.
- **Discards** — everything else, each with a one-line reason ("style preference",
  "unreachable given X", "cost exceeds benefit").

Present both lists. In report-only mode, stop here.

## Step 3 — Fix at root cause

For each survivor, in severity order:

1. Trace to the choke point (grep callers/references/copies — evidence, not intuition).
2. Make the minimum fix *at that point*. For duplications, collapse to one canonical
   source and point the copies at it.
3. Record: finding → root cause → fix, one line each.

If a survivor requires a genuine scope decision (new dependency, design change,
destructive operation), pause and surface it rather than deciding unilaterally.

## Step 4 — Ripple the fixes

A fix that leaves the docs lying is a new defect. Update everything the fixes
touched: README/guides, scripts, skill instructions, indexes, comments that describe
changed behavior. Grep for the old names/paths/claims before declaring done.

## Step 5 — Verify and report

- Re-run whatever proves the fixes: tests, build, render, or a re-read of the revised
  plan against the original findings. Report results faithfully — a failing re-verify
  goes in the report, not under the rug.
- Final report: survivors fixed (finding → root cause → fix), discards with reasons,
  ripple updates made, verification evidence, and anything deferred to the user.
