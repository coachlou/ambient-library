# Deferred ideas

Design records for work that was built on a branch, never shipped, and whose
branch has since been deleted. Nothing here is live. Each entry keeps the idea
and the reason it was set aside, so a future pass starts from the converged
shape instead of rediscovering it.

Every entry names its commit SHA. Deleted branches stay recoverable via
`git reflog` for the usual ~90 days; after that these summaries and the two
preserved plan docs are what remains.

**Common cause of deferral.** All of this predates the AAI consolidation that
moved folder scaffolding out of `.aai/skills/lifecycle.md` into the
`library/ambient-folder/` domain skill. Each branch rewrites files that
consolidation rewrote differently, so none of them merge — they would have to be
re-authored against the current shape.

---

## Federated scopes, bindings, and graded memory

**Branch:** `claude/ambient-federated-v2` @ `aa1abf5` (6 commits, 952 lines)
**Full plan preserved:** [`PLAN-federated-scopes.md`](PLAN-federated-scopes.md)

A v2 of the whole ambient model: a four-concern unit, three scopes, risk-gated
bindings, Node→Self promotion, and graded memory (`templates/aai/memory/facts.md`
with trust tiers). Touched every subskill, every template, and `ARCHITECTURE.md`.

**Why deferred.** Two reasons. It rewrites the five subskills and
`.aai/instructions.md` wholesale, against a base the consolidation has since
replaced. And its nearest neighbor is already explicitly deferred in
[`PLAN-global-librarian.md`](PLAN-global-librarian.md) — *"namespace-first
routing / hierarchical catalogs — flat catalog is fine at ~46 skills; revisit
past ~150 or when routing errors show up."* The catalog is at 48.

**Revival trigger.** Routing errors in the flat catalog, or passing ~150 skills.
Read the preserved plan first; it is the converged design, not a sketch.

## Declared-scope inheritance (lineage)

**Branch:** `claude/agentic-os-architecture-5ec1a9` @ `c59dc1c` (2 commits, 104 lines)

An ambient folder declares `scope:<name>` rows in its Inputs table to inherit
another scope's *context* — a domain glossary, a client's rules. The edge is a
**declaration, not a location**: a project need not sit inside its domain's
folder, and sitting inside one creates no edge. Names resolve through the
`## Scopes` section of `~/.aai/context.md`.

The load-time rules were worked out in detail: inherit the *map* (a scope's
`context.md` index), never blanket-load its `references/`; local `.aai/` wins on
collision, then declared scopes in declaration order, then parents breadth-first;
a visited-set keyed by logical name for termination; state the resolved order in
one line so precedence drift shows up in transcripts. Two modes trade DRY against
portability — **link** (registry lookup, breaks copy-portability) and **vendor**
(flatten into `.ailib/scopes/<name>/`, re-synced like any vendored capability).

**Why deferred.** Smallest and most mergeable of the three, but it targets
`.aai/skills/load.md` and the `lifecycle.md` that consolidation gutted. Porting
it means re-authoring against `library/ambient-folder/instructions.md`.

**Revival trigger.** A second folder needing the same client or domain context.
Until there are two consumers, the sharing mechanism is speculative.

## Precedence — two tracks

**Branch:** `claude/dreamy-bohr-d610c0` @ `0d0a080`

A conflict-resolution reference loaded *only* when instructions conflict, split
into two ladders because "which fact is true" and "whose voice wins" have
opposite answers about cognition. Classify first: if either side is an Approved
fact or a bound instruction it is the **facts track**, otherwise the **style
track**. Facts run `user > Approved truth > local override > bound skill >
global standard > Observed/Inferred > base model`. Style runs
`user > local override > Self cognition > bound house style > generic standard >
base model`.

The load-bearing detail: an Approved fact carries a `review-by` date, and a
fresher Observed fact contradicting it forces verification before assertion —
source authority never outranks current reality.

**Why deferred.** Depends on the graded-memory tiers (Approved / Observed /
Inferred) and `bindings.md` from the federated-v2 model. Without those the ladder
has nothing to rank.

## `promote` as a router disambiguation

**Branch:** `claude/dreamy-bohr-d610c0` @ `0d0a080`

Not a skill and not a catalog entry — a router leg over two paths that already
exist. A reusable capability routes to `propose.md` → `_staging` → `admin`; a
rule for *this* folder routes to the folder's `references/`.

Its sharpest conclusion is a **rejection**: cognition is not a promote target.
"Update my profile" stays inside `cognitive-mirror`'s own batch flow, because the
mirror appends to a *global* store with no redaction insertion point — an
auto-promote-from-correction leg would leak client specifics across folders.
Revisit only if a validated redaction mechanism is ever built.

**Why deferred.** The library leg already works today via `propose`. The second
leg is `ambient-folder`'s §Learn. The disambiguation adds a trigger surface for
routing that already resolves correctly.

## `scripts/aai-init.sh` — deterministic stamp

**Branch:** `claude/dreamy-bohr-d610c0` @ `0d0a080` (190 lines)

A bash stamper: idempotent, `--dry-run`, `--force`, `--bootstrap-home`, writing
AGENTS.md as the canonical pointer with CLAUDE.md / GEMINI.md as one-line
redirects.

**Why deferred — this one is superseded, not postponed.** `library/ambient-folder/`
is *"self-contained by design — it writes the scaffold directly rather than
copying a template, so it behaves the same installed standalone, vendored into a
folder's `.ailib/`, or bundled in the plugin."* A script that copies templates
from a known clone path contradicts that directly. The multi-harness adapter rule
is the part worth keeping, and it lives in the next entry.

## Pointer-adapter placement — an observed failure

**Branch:** `claude/dreamy-bohr-d610c0` @ `bfcc792`
**Status: PORTED — this entry is history, not a pending idea.**

Two findings from an actual test drive of `templates/AGENTS-pointer.md`:

1. **Claude Code auto-loads `CLAUDE.md`, not `AGENTS.md`.** A pointer placed in
   `AGENTS.md` alone is never seen by Claude Code. The fix keeps the canonical
   block in `AGENTS.md` and makes `CLAUDE.md` / `GEMINI.md` one-line redirects,
   so the block lives in exactly one place.
2. **"Make this an aai folder" was read as Node.js** — the agent ran `npm init`
   instead of reading the router. The fix says so explicitly in the pointer:
   *"aai folder means an ambient `.aai/` local-memory layer — not Node.js. Do not
   run `npm init`."*

Unlike everything else on this page, this was a reproduced bug with a written
fix, independent of the deferred architecture — so it was ported rather than
archived. `templates/AGENTS-pointer.md` now carries the placement table, both
`npm init` warnings, and the redirect block; `.aai/skills/install.md` names the
per-harness target file so the placement rule reaches the agent doing the
install. Terminology was adapted from the branch's "aai folder" to main's
"ambient folder", and its "trust-tagged local-memory layer" phrasing was dropped
— that concept belongs to the deferred graded-memory model above.
