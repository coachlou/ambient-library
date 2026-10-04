# PLAN — `learned.md`, the agent-writable layer of a skill

**Status:** accepted 2026-10-03 (Lou). Not yet implemented. Proposed additions to
`templates/aai/README.md` (shadowing rule), `.aai/skills/load.md` (step 3),
and `.aai/skills/lifecycle.md` (sweep). Nothing in the canonical library
changes shape; this adds one optional file to the owned layer and one pass to
the existing sweep. Builds on `PLAN-personalization-layer.md` §3, which fixed
`overrides.md` at `.aai/skills/<n>/` and its precedence.

## Problem

A skill body carries two kinds of content under one rule. *Procedure* (steps,
order, gates, outputs, triggers) must not change without Lou knowing.
*Knowledge* (what the skill learned while running: quirks, edge cases,
calibration, rejected patterns) should change freely, or the skill never
learns. Today the strict rule covers both, so the only learning path is
purgatory (`propose` / `propose-upstream`), and almost nothing small enough to
be worth it goes through it.

## The split

| Layer | File | Who writes | Review |
|---|---|---|---|
| procedure | `instructions.md` (canonical, or a fork) | humans, via purgatory | before merge |
| extra rules | `.aai/skills/<name>/overrides.md` | Lou | none, it's owned |
| learned knowledge | `.aai/skills/<name>/learned.md` | **the agent, during a run** | after the fact, at sweep |

`learned.md` lives in the **owned** layer beside `overrides.md`, never in
`library/` or `.ailib/`. Installed copies stay pristine and updates can't
clobber it. This is the existing shadowing model with one more row, and the
memory contract (candidate → active) applied to skills: an entry in
`learned.md` is a candidate; the sweep decides what it becomes.
`audit-distribution.py` already treats `instructions.md` and `SKILL.md` as
"procedure stays per skill" (`NOT_SHAREABLE`); this draft is the same line
drawn for runtime learning.

## One capture point, two destinations

A skill improves in two independent ways, and a learning starts out
undifferentiated:

```
run → ~/.aai/skills/<name>/learned.md          (candidate; no review)
          │
      sweep = the fork point                     (Lou's review)
          │
   ┌──────┴──────────────────────────────┐
PRIVATE                               CANONICAL
~/.aai/skills/<name>/overrides.md      dev workspace: library/<name>/instructions.md
"Lou's edition"; survives updates      → git diff → commit → build-production
                                       → ~/.ailib pull → post-update sweep prunes
```

- **The shipped capability.** On the maintainer's machine the sweep resolves
  the `Dev source (canonical-library)` row in `~/.aai/context.md`, exactly as
  `propose-upstream.md` step 1 already does. A CANONICAL knowledge entry is
  then applied through the existing **Update a domain skill** path in
  `admin.md`: edit `library/<name>/instructions.md`, bump the skill's version.
  Review is `git diff`. The sweep never commits. Where the dev row does not
  resolve, the entry goes through `propose-upstream` unchanged (dev
  `in-progress/` → GitHub issue with a second yes → local mailbox); that
  routing already exists and needs no maintenance.
- **Unique to Lou.** `overrides.md` is already this: owned, appended after the
  body, never touched by updates. The sweep promotes PRIVATE entries into it,
  so Lou's edition improves rather than just accumulating. `~/.aai` under
  private git makes this track versioned too.
- **Other users.** Nothing to build. Their learnings live in their owned
  layer, which updates never touch. Folding anything back is their business.

Run day-to-day from `~/.ailib`, not the dev workspace. The dev workspace has
no version to stamp entries against, and running from it skips the one place a
bad release gets caught before users see it: the maintainer updating like a
user.

## Format

One entry per fact. Append-only during a run; the sweep is the only thing that
rewrites.

```markdown
# learned — <skill-name>

- 2026-10-03 · v1.4.2 · researcher · session 260526-1743: Firecrawl returns
  excerpts only for docs sites; scrape the page when a result is cut
  mid-sentence.
- 2026-10-01 · v1.4.2 · writer · Lou rejected draft: openers that start with a
  question read as clickbait to him. Avoid.
- 2026-09-28 · v1.4.1 · researcher · PROPOSE: step 3 (dossier outline) — the
  outline is always rewritten in step 5; drafting it twice wastes a pass.
```

Each entry: date, installed library version (from `manifest.yaml`), which skill
wrote it, source (session id, user correction, or observed failure), the fact.
No prose around the list. No headings per entry.

## Rules

1. **Add, never override.** An entry may refine a step ("when X, also Y") or
   record a fact. It may not contradict, skip, or reorder a step in
   `instructions.md`. If the agent believes a step is wrong, it follows the
   step as written and records `PROPOSE: <step> — <why>` so the sweep routes
   it.
2. **Precedence:** body → `overrides.md` → `learned.md`. Learned is lowest.
   The loader appends it after overrides and says so when it did (same
   disclosure rule as overrides in `load.md`: a silent layer is inexplicable).
3. **Cap:** 40 entries. At the cap the agent drops the oldest entry it judges
   least load-bearing before adding one, says which, and the sweep is due.
   The cap is the context budget; raise it per skill only with an
   `overrides.md` line.
4. **No secrets, no values.** Credentials and machine-side values belong in
   `environment.yaml` / `project.yaml`. A learned entry naming a path or key
   is pruned at sweep without promotion.
5. **Scope:** project-scoped by default (`<project>/.aai/skills/<name>/`).
   A fact true everywhere goes to `~/.aai/skills/<name>/learned.md`; the
   agent writes to the project copy and marks it `GLOBAL?` for the sweep to
   promote. Both files load when present, user-scope first.
6. **Default is private.** Nothing leaves the machine unless the sweep marks
   it CANONICAL *and* a human commits it. What travels is a diff to
   `instructions.md`, scrubbed of provenance and identifying detail; the
   learned entry itself never goes anywhere.

## Three moments

| Moment | Who acts | Review weight |
|---|---|---|
| **During a run** — skill appends to `learned.md` | agent | none; rule 1 bounds it |
| **Sweep** — entries classified and moved | agent proposes, Lou decides | `git diff` for knowledge; purgatory for procedure |
| **Release** — `build-production.sh`, then `~/.ailib pull` | Lou | when the diff is worth shipping |

### Sweep triggers

| Trigger | Why |
|---|---|
| Standing intention in `~/.aai/triggers.md` (weekly) | the normal cadence; `trigger-runner` runs it, or a Hermes routine once one exists |
| After `git -C ~/.ailib pull`, for skills whose body changed | catches entries the update made stale (version stamp older than the body) |
| A `learned.md` hits its cap | the skill is learning faster than it is being reviewed |

### Sweep output

One report (per skill: promote / keep / prune counts, entries listed with
their proposed fate) and, on the maintainer's machine, **uncommitted edits in
the dev workspace**. The sweep never commits.

Each entry gets one of four fates:

- **Private** → folded into `overrides.md` (owned). Entry removed from learned.
- **Canonical** (knowledge) → applied via **Update a domain skill**: edit
  `library/<name>/instructions.md`, bump version. Gate: `git diff`, commit or
  revert. Minutes.
- **Procedure** (`PROPOSE:`) → drafted into `in-progress/<name>/` with a
  `PROPOSAL.md`, never straight into the body. Gate: `skill-auditor` and
  `skill-evals` green, then `promote.sh` (its replace mode already shows the
  diff and checks the version bump). This is the existing purgatory, now fed
  by the skills themselves.
- **Prune** → stale, duplicated, contradicted, shipped since (version stamp
  older than a body that now covers it), or a secret. Removed.

`GLOBAL?` entries that survive move to user scope.

### Release

`build-production.sh` after any sweep that produced canonical commits, or
batched monthly. Then `git -C ~/.ailib pull`, which fires the post-update
sweep, which prunes what just shipped.

Nothing reaches a shipped body without passing `git diff`. Nothing changes a
procedure without passing evals.

## Enforcement

The split is a path, so it can be enforced by the filesystem, not by
convention. For a harness with its own learning loop (Hermes writes to any
skill dir it can reach), canonical dirs are read-only to that process and
`learned.md` is the one writable file.

Each `SKILL.md` shim gains one line: *"Record what you learn in
`<owned layer>/learned.md`; never edit `instructions.md`."* The Claude path
can carry the same instruction once in `load.md`; the shim line is for
harnesses that read `SKILL.md` directly. **Shims are hand-written, not
generated** (`promote.sh` only checks presence; bodies all differ), so this is
one `sed` over `library/*/SKILL.md` plus a line in `admin.md`'s **Four files**
contract for new skills, and an `audit-distribution.py` check so it can't drift
back out.

## Resolved: direct knowledge edits in the dev workspace

`propose-upstream.md` has a hard limit: *"Never edit an existing
`library/<name>/` — a revision is a proposal too."* Decided 2026-10-03: in
the checkout that the `Dev source (canonical-library)` row in
`~/.aai/context.md` resolves to, knowledge-class edits go straight into
`library/<name>/instructions.md` under the existing **Update a domain skill**
path; gate is `git diff` + version bump. The limit stays absolute everywhere
else (installed copies, any other machine) and for procedure, which still goes
through `in-progress/` + `promote.sh`. One sentence to add to
propose-upstream's limits when this ships.

**User context.** For a non-maintainer the dev row does not resolve, so the
Canonical fate collapses to Private (keep in `overrides.md`, the default) or
`propose-upstream` (GitHub issue, opt-in, second yes). `~/.ailib` stays
read-only; every learning is proprietary unless they choose to send it.
Updates never touch `.aai/skills/<name>/`, so nothing is lost across a distro
update. It can go stale: when a shipped body now covers or contradicts an
`overrides.md` line, the post-pull sweep flags it (version stamp older than
the body) and the user decides. Nothing is removed or kept silently.

## Durable-by-tag exception

Location sets the default: procedure is durable, learned is evolving. A
reference file that is operationally critical (a publishing checklist under
`references/`) can declare `durable: true` in frontmatter and is then treated
as procedure by the sweep and the propose gate. Tagging is for exceptions only;
tagging item by item is what would rot.

## What changes in existing capabilities

| What | Count | Change |
|---|---|---|
| `instructions.md` bodies | 0 | none; knowledge already baked into a body stays active where it is |
| `SKILL.md` shims | 67 (hand-written; one `sed`) | the one enforcement line above |
| `load.md` step 3, `templates/aai/README.md` shadowing table, `lifecycle.md` sweep, `admin.md` four-files contract | 4 | the loader and sweep rules in this draft |
| `audit-distribution.py` | 1 | check for the shim line |
| `contract.yaml` `state:` paths | 0 | no conflict; structured state is a different file under a different rule |

## Not in this draft

- **Eval-gated self-edit** (agent may change procedure directly if
  `skill-evals` stay green). Evals are prose-judged today; not trustworthy as
  a gate yet. Revisit when evals are deterministic for the skills that matter.
- **Automatic promotion.** Everything that reaches `instructions.md` still
  passes a human.
- **An org-shared layer** between owned and canonical. The lookup chain
  (project `.aai/skills/` → project `.ailib/` → `~/.ailib`) already has room
  for a private library as one more vendored layer, and the sweep would gain a
  fifth fate. Build it when there is a second human.
- **A per-skill `durable` flag.** Too coarse in both directions.
- **Conflict precedence between learned facts and other sources.** That is
  `DEFERRED-IDEAS.md` "Precedence — two tracks", which waits on graded memory.
  Rule 2 here is only file-append order, not a truth ladder.

## Smallest first step

Pick one skill that runs often and fails in small, learnable ways
(`researcher` is the obvious one). Add the `SKILL.md` line, let it write
`learned.md` for two weeks, run one sweep, and judge the entries. If fewer than
a third are worth keeping, the format needs tightening before it spreads.
