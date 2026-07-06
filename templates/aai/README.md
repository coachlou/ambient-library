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
