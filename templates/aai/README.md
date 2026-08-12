# .aai / .ailib — Ambient Agentic Intelligence scaffold

A folder becomes **ambiently intelligent** by adding a `.aai/` directory.
Nothing else about the folder changes. Its visible contents stay whatever they
were — documents, skills, a codebase, a client workspace — and `.aai/` overlays
behavior, identity, and routing onto them. Additive, removable, stampable:
what `git init` is to version control, `.aai/` is to agentic intelligence.

Capabilities installed from a canonical library land in a sibling `.ailib/`
directory. The two form a pair with one ownership rule:

- **`.aai/` is owned.** Everything in it belongs to this instance. Updates
  never touch it.
- **`.ailib/` is vendored.** Pristine, read-only copies of canonical
  capabilities. The update flow may delete and re-sync it at any time.

## Anatomy

```
<folder>/
├── .aai/                  # OWNED — the folder's own agentic intelligence
│   ├── instructions.md    #   required: behavior — what the folder does with requests
│   ├── identity.md        #   who this folder is: voice, disposition, ground rules
│   ├── context.md         #   map of the folder's contents, for routing without reading
│   ├── memory/            #   runtime state across runs — no update ever touches this
│   ├── references/        #   curated rules the behavior internalizes as constraints
│   ├── skills/            #   own capabilities + personalized forks of canonical ones
│   └── templates/         #   scaffolds this folder stamps out (including .aai itself)
└── .ailib/                # VENDORED — canonical includes, read-only
    ├── manifest.yaml      #   what's installed: name, source, version
    └── <capability>/      #   pristine copy; personalize by forking to .aai/skills/
```

Only `instructions.md` is required. Graduated adoption: start with it alone and
add elements when the behavior needs them. `.ailib/` exists only once something
is installed.

## The shadowing rule

**`.aai/` shadows `.ailib/`.** To personalize a canonical capability, copy it
from `.ailib/` into `.aai/skills/` and edit the copy. When both define the same
capability, the router resolves to `.aai/`. The pristine canonical stays in
`.ailib/` for comparison and re-sync; the fork is yours forever.

Never edit inside `.ailib/` — edits there are lost on the next re-sync, by
design.

## Memory

`.aai/memory/` is the instance's runtime state: session handoffs, progress,
edit history, observations across runs. Rules:

- No update, re-stamp, or re-sync may touch it. It is what makes this
  instance *itself*.
- It is working state, not doctrine. When a pattern in memory recurs (the same
  correction three runs in a row), promote it deliberately into
  `.aai/references/` as a rule. Memory is where the folder notices;
  references are where it has learned.

## Augmenting a folder's capabilities

When an agent — or its human — determines the folder needs a capability it
doesn't have, placement is decided by this test, not improvised. Apply it to
the **smallest independently owned unit**: composite workflows decompose into
their reference, skill, and agent parts before placing each.

### The placement test

Two questions, in order. **Q1 — what does the knowledge DO?**
inform | transform | decide. **Q2 — what does it NEED?**
nothing | deterministic steps | stateless inference | accreting memory +
jurisdiction | a home with a corpus. Stop at the first rung that holds.

| Rung | It... | And needs... | Then it is a... | Lives at |
|---|---|---|---|---|
| 0 | is needed once | — | nothing — do it inline | (nowhere) |
| 1 | informs (constraints, formats, facts) | to be consulted | **reference**; if parametric and machine-consumed, a **profile** | `.aai/references/` |
| 2 | transforms input→output | deterministic steps | **script** | alongside its consumer |
| 3 | transforms, same for a stranger | inference, no memory | **skill** | resolved from canonical, or `.aai/skills/` |
| 4 | decides — discretion that accretes | memory + jurisdiction | **agent** (a hire) | its own `.aai/` folder |
| 5 | any of the above | to live WITH a corpus/place | **ambient folder** — stamp `.aai/` on the data's folder | the data's folder |

Clarifications the rungs need:

- **Rung 0 is real but bounded.** Inline is for reversible, low-risk work
  inside existing gates. Side-effectful or gated acts (publish, send,
  delete) keep their approval gates regardless of how rarely they occur.
- **A stateless verdict is a transform, not a decision.** An evaluator that
  takes a draft and returns a judgment, cold, with no memory, is rung 3 —
  and its blindness is usually the point. Rung 4 "decide" means accreting
  discretion over a jurisdiction, not producing a judgment output.
- **Rung 5 uses invariant 4's threshold.** A corpus stays plain data —
  visible input — until it needs behavior beyond a single instructions
  file. Only then does it earn its own `.aai/`, which is then authoritative
  for it (outer agents defer).

### Sourcing — canonical library first

Two distinct orders. **Discovery** (acquiring, rungs 1–4): check the
canonical library first — it is the default, expected home of
ambient-agentic capability; augmenting a folder normally means resolving or
installing from it, not creating. Create only when the library lacks it:
born owned, in the `.aai/` of the folder that needed it, authored from the
real task trace — never from speculation. **Execution** (running): the
shadowing rule, unchanged — `.aai/` fork over `.ailib/` copy over canonical.

Promotion runs the reverse of discovery: an owned creation graduates to the
canonical library when recorded evidence shows a second consumer or repeated
use (dated memory/debrief entries are the evidence — not impressions).
Promotion is a deliberate, human-approved act, never a side effect.

### Competence vs. configuration

Skills own **competence** — how a class of work is done, including its
domain knowledge (a video skill legitimately knows video formats). Agents
own **instance configuration** — which capability applies here, with what
parameters, for this folder and this human — resolved at plan time and
passed via briefs. An executor that absorbs instance configuration forces
one-executor-per-variant sprawl; an agent that absorbs competence stops
being a router and becomes a bottleneck.

### Migration — capabilities move rungs over their lifetime

A reference that hardens into procedure (same steps, recorded 3+ times)
promotes to a script or skill. A skill that starts accreting state is
misplaced — move the state to an agent's memory, restore the skill to
statelessness. An agent whose memory and jurisdiction never differentiate
is a costume — demote to a skill or profile.

### Decision rights

| Act | Who decides |
|---|---|
| Create/update a reference, profile, or script | the agent, freely; recorded in memory/debrief |
| Fork a canonical capability (shadowing rule) | the agent, freely |
| Create a NEW owned skill | the agent — usable in this folder at once; discoverable to others only via promotion |
| Hire an agent / stamp a new ambient folder | proposal to the human — never unilateral |
| Promote anything to the canonical library | human-approved, always |

One writer per folder: an ambient folder's `.aai/` is written only by its
own agent. Dispatched executors return outputs to the dispatcher; they never
write shared state directly.

## Invariants

1. **Behavior travels with the folder.** Copy the folder, you've copied its
   intelligence — identity, forks, memory, and installed capabilities included.
2. **One ownership rule.** `.aai/` owned and never overwritten; `.ailib/`
   vendored and freely re-syncable. All update semantics follow from this.
3. **Portable paths.** Inside `.aai/` files, reference siblings relative to the
   folder root, never by absolute path.
4. **Recursion is graduated.** Any subfolder may carry its own `.aai/` and
   become a smaller ambient folder — but only when it has behavior beyond a
   single instructions file.
5. **Structural vs. content stays separated.** `.aai/references/` holds rules
   to internalize as constraints; the visible folder holds working material to
   process as input. Don't mix them in one load.

## Lifecycle

| Step | Action | Touches |
|------|--------|---------|
| Stamp | copy this template in as `.aai/`, rewrite identity + instructions | `.aai/` |
| Install | vendor a canonical capability, record it in the manifest | `.ailib/` |
| Personalize | fork `.ailib/<cap>` → `.aai/skills/<cap>`, edit the fork | `.aai/skills/` |
| Learn | accumulate state; promote recurring patterns to references | `.aai/memory/` → `.aai/references/` |
| Update | delete and re-sync vendor space from canonical | `.ailib/` only |

## Discovery

A cold agent finds `.aai/` through whatever anchor the host environment
provides: a registered skill shim (plugin installs), an `AGENTS.md` /
`CLAUDE.md` pointer block (pointer adapter), or by convention — check for
`.aai/instructions.md` when told a folder is ambient.

## Stamping a new ambient folder

1. Copy this template into the target folder as `.aai/`.
2. Rewrite `identity.md` — who is this folder?
3. Rewrite `instructions.md` — what does it do with requests?
4. Fill `context.md` with the folder's actual layout.
5. Delete every optional element the behavior doesn't need. `.ailib/` will be
   created by the first install.
