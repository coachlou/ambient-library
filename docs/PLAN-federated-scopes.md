# Spec + Plan: Federated Scopes (v2)

Evolves ambient-library from "one canonical library + stampable ambient folders"
to the **three-scope federated model**: one recursive unit instantiated at
**Self**, **Library**, and **Node** scope, with precedence flowing down and
gated promotion flowing up. This document is both the spec (Part A) and the
execution plan (Part B). Part B carries the live status.

Authored from the v1 files, not from imagination. v1 is more mature than it
looks — the recursive `.aai/`+`.ailib/` unit, per-folder `memory/`→`references/`
graduation, and Node→Library promotion (`propose`→`_staging`→`admin`) already
exist. This is a delta, not a rewrite.

---

# Part A — Spec (target architecture)

## A1. The one principle

At every scope the same four concerns are true, and only these four:

| Concern | File | Lifecycle | Trust |
|---------|------|-----------|-------|
| **Behavior** — how to act here | `instructions.md` | canonical, overwrite-on-update | — |
| **Identity** — who this agent is | `identity.md` | slow, personal, high-trust | — |
| **Memory** — what's true / happened here | `memory/` + `context.md` | fast, local | graded |
| **Bindings** — what it pulls from other scopes | `bindings.md` | explicit, risk-gated | — |

Separating these by lifecycle and trust is the whole design: it is why an update
never eats your cognitive profile (identity, not behavior), and why a client
fact never leaks into the global library (memory, not promotion).

## A2. The three scopes (same unit, one concern leads)

- **Self — `~/.aai/`.** You as an agent. Identity = your **cognitive profile**;
  memory = your decision harvest; behavior = your operating directives. Binds
  nothing — root of personal truth. Consumers today: `cognitive-mirror`,
  `deep-mirror`. Resolved through the existing `~/.aai/context.md` routing table.
- **Library — this repo.** The capability commons. Behavior-heavy: `library/`
  skills, catalog-routed, one description of standing context cost. Little
  memory, no per-client identity.
- **Node — any project/client folder.** Local truth. Memory-heavy: facts tagged
  Observed / Inferred / Approved with provenance. Binds the skills it needs and,
  by default (privacy-gated), the Self cognitive profile.

`.aai/memory/` is the Node's **native** memory — always present when a folder is
ambient. `context-mgr`/`session` (`.context/`) are an **optional heavyweight
capability** for multi-agent continuity that operates on Node memory — not a
competing scope.

## A3. Bindings (the fourth concern, new in v2)

A `.aai/bindings.md` ledger records what a folder pulls from other scopes.
Replaces implicit binding (vendoring + `skills-manifest.yaml` scoping) with one
visible, auditable file.

- **Two fulfillment strategies**, both recorded in the same ledger:
  - *by reference* (default, lean) — point at the canonical `library/<skill>`.
  - *vendored* (portable/offline) — copy into `.ailib/` (the existing v1 path),
    for a Node that must work without the global reachable.
- **Risk tiers + gates** (from ICM):
  - *low* (editorial standards, templates, non-executable workflows) → approve
    once per Node.
  - *medium* (scripts, validators, many-file readers) → approve bind + first use.
  - *high* (network, browser, publishing, credentialed, shell-write) → approve
    every use.
- **Cognition binding**: a `private` Node binds Self identity by default; a
  `commit-safe` or `shared-team` Node does **not** (leak prevention).

`skills-manifest.yaml` is subsumed — its domain-skill scoping becomes the
`skill`-type rows of `bindings.md` (legacy manifests still honored).

## A4. Precedence (explicit in the router)

When instructions conflict:

```
user instruction now
> Node local truth (Approved > Observed > Inferred)
> Node local override
> bound skill / workflow
> global standard
> Self cognition (default lens)
> base agent behavior
```

Self cognition sits low on purpose: the ambient default lens, always overridable
by a specific fact about *this* Node.

## A5. Promotion (one verb, three destinations by scope, all human-gated)

| Pattern | Destination | Mechanism | Status |
|---------|-------------|-----------|--------|
| recurs within one folder | `.aai/references/` (that folder) | `lifecycle` Learn | exists |
| reusable capability | Library skill | `propose` → `_staging` → `admin` | exists |
| a fact about how you think | Self cognitive profile | `lifecycle` Promote-to-Self → `cognitive-mirror` | **new** |

Every correction is either a capability (→ Library) or a fact about you (→ Self).
Inferred until you approve; never auto-promoted.

## A6. Portability invariant (unchanged, protected)

The unit is plain files + an agent that reads them — harness-independent. Each
harness supplies only *discovery* (wake the router, resolve the global path) via
its wrapper (plugin / Codex skill / `AGENTS.md` pointer). **Bindings live in the
folder, never in harness-native config.** That is the portability leak to guard.

---

# Part B — Plan (workstreams + status)

Status: ☐ todo · ◐ in progress · ☑ done. One commit per workstream, message
explains *why*, staged files only, no push.

## WS1 — Unit + scopes contract ☑
Evolve the scaffold spec to the four-concern unit and name the three scopes.
- `templates/aai/README.md` — added `bindings.md` as 4th concern, the four-concern
  table, the three-scope section, graded memory, and a Promotion table. ☑
- `templates/aai/bindings.md` — **new** ledger template (fulfillment, risk gates,
  cognition binding, overrides, disallowed). ☑
- `templates/aai/memory/facts.md` — **new** local-truth template with
  Approved/Observed/Inferred + provenance (chose memory over context.md: facts
  are memory, context.md stays the routing map). ☑
- `templates/aai/identity.md` — added Privacy field. `instructions.md` — added
  memory + bindings rows to the Inputs table. ☑

## WS2 — Precedence + binding + risk gates ☑
- `.aai/instructions.md` — added "Scopes, bindings, and precedence" section:
  the precedence chain, `bindings.md` + risk-gate honoring, Self-cognition
  default lens. Selection step now reads `bindings.md` skills section (legacy
  `skills-manifest.yaml` still honored). ☑

## WS3 — Self scope + cognition-by-default ☑ (router part; docs in WS6)
- Router: `private` Nodes bind Self identity by default, resolved via
  `~/.aai/context.md`; commit-safe/shared-team do not. ☑ Full Self-scope
  narrative lands in ARCHITECTURE.md (WS6). No new template — Self reuses the
  one unit. Verified `~/.aai/context.md` and `library/cognitive-mirror/` exist.

## WS4 — Node→Self promotion ☑
- `.aai/skills/lifecycle.md` — added **Bind** and **Promote to Self** operations;
  Learn now names the three promotion destinations. ☑
- `.aai/instructions.md` — lifecycle routing row + disambiguation updated. ☑

## WS5 — Reconcile `.context/` ☑
- `library/catalog.yaml` — **appended** a positioning clause to `context-mgr`/
  `session` (existing trigger phrases untouched, so routing is safe): they are
  the optional multi-agent-continuity capability over a Node's native
  `.aai/memory/`. ☑
- Full storage-path retarget deferred + noted in MANAGEMENT.md "Known follow-ups".

## WS6 — Documentation (dev / admin / user) ☑  ← the "done" bar
- **Dev:** `ARCHITECTURE.md` — three-scope section, unit/precedence/promotion,
  four new design decisions. `docs/MANAGEMENT.md` — Nodes/Bindings, Promotion-to-
  Self, deferred `.context/` note. ☑
- **Admin:** `docs/INSTALLATION.md` — Self-scope `~/.aai/` section + Node stamping. ☑
- **User:** `GETTING_STARTED.md`, `USAGE.md` (Nodes/bindings/cognition section),
  `FAQ.md` (Scopes/Nodes/Bindings Q&A incl. leak question). ☑
- `README.md` three-scope framing; repo `.aai/identity.md` + `.aai/context.md`
  touch-ups. (SKILLS.md left as-is — human catalog, nothing stale.) ☑
- Bumped both plugin manifests → **2.0.0**. ☑

## WS7 — Verify + commit ☑
- Verified: one-description invariant holds (only the two ambient shims are
  registered); routing still catalog-only; all new references resolve
  (`bindings.md`, `memory/facts.md`, `cognitive-mirror`); catalog parses
  (46 skills); no stale "only artifact" claims. ☑
- Committed per workstream on `claude/ambient-federated-v2`. Not pushed.

## WS8 — Adversarial review + remediation ☑
A red-team of WS1–7 found the migration boundary was drawn wrong: the router,
lifecycle, templates, and docs moved to v2, but the four execution/on-ramp
subskills stayed on v1 — so v2 was documented but not wired at its entry points.
Nine findings, all fixed:

1. **On-ramp didn't build v2** (`install`/`select`/`manage` wrote
   `skills-manifest.yaml`, never a Node/ledger) → retargeted all three to
   `.aai/bindings.md` (legacy manifest still read). ☑
2. **Execution ignored the model** (`load.md` knew only the manifest + CLAUDE.md)
   → now scopes by ledger skill rows, checks the risk gate before running, and
   executes under the full precedence chain incl. the private-only cognition gate. ☑
3. **Phantom `skills:` section** the router referenced → unified on `skill`-type
   ledger rows across router, `load`, template, and docs. ☑
4. **Undefined default privacy = leak** → fail-safe everywhere: unset / placeholder
   / non-Node ⇒ do **not** bind Self cognition (router, template, load, lifecycle). ☑
5. **Privacy declared twice** → `bindings.md` is the sole authority; `identity.md`
   points to it. ☑
6. **Risk gate unenforceable** (no markings) → high/medium-risk skills enumerated
   in the `catalog.yaml` header (routing-safe comment). ☑
7. **`propose` vs Promote-to-Self mis-route** → disambiguation sharpened ("how we
   did this" = skill; "how I think" = profile). ☑
8. **Node's own `instructions.md` vs router undefined** → router states it: a Node
   is data-only unless deliberately stamped standalone, in which case local
   behavior leads (precedence "Node local override"). ☑
9. **Taught phrase not a trigger** → "make this folder remember" added to the
   lifecycle route. ☑

Re-audit after fixes: no phantom refs remain; all four on-ramp/exec subskills
reference the ledger; catalog still parses (46); one-description invariant intact.

## Explicitly deferred (not this ship)
- Retargeting `context-mgr`/`session` storage from `.context/` to `.aai/memory/`.
- Scripts (inspect/create/redact) — prose + templates until manual proves repeat.
- Autonomy levels 0–4 — collapsed to one rule (read-only default; memory writes
  after approval; else ask).
- Auto-promotion, daemons, per-skill catalog risk fields.
