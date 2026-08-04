# Plan: Claudio — request-time capability orchestration

**Status: exploratory, not greenlit.** Captured from a design conversation
(2026-07-08). Lou is half-sold; revisit before building. This doc exists so the
next pass starts from the converged shape, not from the original (wrong) framing.

---

## What this stopped being

It started as "Claudio, a Chief-of-Staff agent" — an ambient folder with its own
identity, soul, memory, and cognitive profile, that would proactively run the
library on Lou's behalf and auto-"hire" new capabilities via an HR agent.

The grilling dissolved almost all of that into things that already exist or were
already rejected:

- **Persona + soul + memory of Lou** → already produced and owned by
  `cognitive-mirror` (`~/.aai/references/cognitive-profile-lou.md`, routed via
  `~/.aai/context.md`). Claudio would *read* it, not own a second copy.
- **"Hire this capability for future use" (HR agent)** → already built and
  deliberately human-gated as `propose.md → library/_staging/ → admin.md`.
  Auto-hiring was rejected by design (unvetted skills degrade routing; see
  ARCHITECTURE.md "Why do proposed skills go to `_staging`").
- **Proactivity / a standing agent that initiates** → the standalone
  agent/daemon/harness is explicitly deferred in `PLAN-global-librarian.md`.

What survived is small and real: **the library's router is a one-shot picker,
and nothing evaluates the full capability set, decides which combination a
request needs, sequences them, and validates the results.** Claudio is the
execution arm that does that. Nothing more.

## The core finding

`create-skill`'s **Step 0 routing gate** already classifies a request three ways
(reuse an existing capability / compose several / author new), and already warns
that orchestration "crammed into a document that can't orchestrate" is an
anti-pattern — orchestration wants an *agent context*, not a skill body.

So **Claudio is create-skill's Step 0 run at request time instead of authoring
time.** Same gate, different clock: create-skill runs it to decide *what to
build*; Claudio runs it to decide *what to run*.

```
request → [classifier: read catalog, classify] →
    (a) one capability fits   → load.md            run it            ← EXISTS
    (b) several compose        → orchestrate.md     sequence + gate   ← NET-NEW
    (c) nothing fits           → do it → propose.md → create-skill    ← EXISTS
```

create-skill acts on exit **(c)** (author). It *detects* (a)/(b) but dead-ends
into "propose composing it" — it never runs the composition, because it is an
authoring tool. **Claudio is the missing executor for exits (a)/(b).** That is
the entire net-new surface.

## Net-new vs reuse

| Function (Lou's four) | Status |
|---|---|
| Evaluate from a registry of all capabilities | `library/catalog.yaml` already is the registry |
| Decide which capabilities a request needs | **new** — the classifier's (b) verdict |
| Sequence / orchestrate them | **new** — `orchestrate.md`, run by an agent context |
| Validate the results | reuse `evaluate-article` / `audit-fix` as gates, inserted between stages |

The classifier is a lift of create-skill Step 0 Q1. The gates exist. The
registry exists. `load.md` (animate one), subagent dispatch (ARCHITECTURE.md:154,
isolate a noisy stage), and `propose.md` (crystallize a repeated chain) all
exist. Genuinely new = **one orchestration executor + a three-way classifier in
the router + a catalog metadata pass.**

---

## Workstream 1 — Upgrade the router's match step to a three-way classifier

Today `.aai/instructions.md` routes to exactly one subskill and picks the single
best catalog match ("Never load more than one domain skill body"). That rule is
load-bearing for context cost and stays the default. Add a classifier verdict in
front of it:

- **one** → existing single-skill path (`load.md`). Unchanged.
- **compose** → new `orchestrate.md`.
- **none** → handle directly, then offer `propose.md`.

Engage the `compose` path only when the request names an outcome that spans
stages ("idea to published", "research then draft then gate") or the best single
match requires an input that does not yet exist. Otherwise stay one-shot — do not
tax trivial requests with a planning step.

## Workstream 2 — `.aai/skills/orchestrate.md` (the executor)

A new subskill, followed by an agent context (the session, or a spawned
general-purpose subagent — not the document itself). Behavior:

1. Read `catalog.yaml` (the whole set — this is the "evaluate from a registry"
   step). Never read skill bodies to plan.
2. Produce an ordered plan of capabilities, sequenced by `produces → needs`.
   **Show the plan to the user before running** — this is also what removes the
   need to memorize the library: Claudio narrates which capabilities it chains
   and why, every time.
3. Execute: animate each stage via `load.md` or an isolated subagent.
4. Insert a `role: validator` gate between stages **only when the request states
   a quality bar** ("publish-ready", "flagship quality"). No auto-gating
   otherwise — slow and presumptuous.
5. On gate failure, replan or stop and report — do not loop silently.
6. A chain planned/run more than twice is the signal to offer `propose.md` —
   crystallize the ad-hoc plan into a named pipeline (this is what `writing-team`
   and `evaluate-article` already are). That is the "hire", already built.

## Workstream 3 — Catalog metadata for composition

`catalog.yaml` entries are tuned as *triggers*, not *composition contracts*. You
cannot sequence from a trigger string. Minimal evolution:

- Add `role:` (producer / transformer / validator) to **every** entry — cheap,
  and it is what makes verdict (b) and gate insertion mechanical.
- Add `needs:` / `produces:` **only** to capabilities that actually chain (the
  content pipeline, the audit/gate skills). Several entries already encode this
  in prose ("Requires a draft to already exist", "from a brief and optional
  dossier").
- Formalize further **only where a real orchestration trips.** Plan from prose;
  fix the entries that break. Do not enrich all 46 preemptively.

Tradeoff named: plan-from-prose is inference re-paid every request and degrades
on ambiguous entries; structured metadata is spend-once-to-stop-re-paying.
Spend it exactly where things compose, nowhere else.

---

## The open decision (unresolved — decide before building)

**Share narrow vs share wide.** create-skill Step 0 has three questions; only Q1
(classify request against the catalog) is genuinely shared. Q2/Q3 (skill-vs-agent,
worth-authoring) are authoring concerns Claudio lacks; sequencing is Claudio's and
not create-skill's.

- **Share narrow (recommended):** extract only the Q1 classifier as the one shared
  step. create-skill keeps Q2/Q3; Claudio keeps sequencing. Low coupling.
- **Share wide:** make Claudio a "dynamic mode" of create-skill — one skill, two
  clocks. Tighter, but couples request-time execution to an authoring tool's
  lifecycle, and create-skill is already large.

## Other questions still open

- Exact trigger for engaging `compose` vs staying one-shot (WS1) — needs real
  requests to tune, not a priori.
- How deep the catalog contract must go before chains are trustworthy (WS3) — the
  plan-from-prose bet may need revisiting after first real misfires.

## Explicitly deferred (the Chief-of-Staff parts — do not build)

- **Persona / soul / identity for Claudio** — its "judgment about Lou" is
  `cognitive-mirror` output, read not owned.
- **Claudio-owned memory store** — reuse the routing table; do not invent one.
- **Proactivity / triggers / daemon** — reactive, invoked only. The standing COS
  is a separate, riskier project that collides with an already-made decision.
- **Autonomous hiring** — promotion stays human-gated via `propose.md`/`admin.md`.

## Acceptance (if built)

- From a complex multi-stage request ("take this idea to a publish-ready piece"),
  the router returns the **compose** verdict, `orchestrate.md` shows an ordered
  plan referencing real catalog capabilities, runs them, inserts a validator gate
  because a quality bar was stated, and reports.
- A trivial single-capability request still takes the one-shot path — no planning
  tax (verify latency/tokens unchanged on a simple ask).
- Nothing new is owned: no persona file, no Claudio memory dir, no daemon.
  `git status` after a run shows only expected outputs.
- A chain run three times prompts a `propose.md` offer, not an auto-commit.
