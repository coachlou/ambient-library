# {{name}} — Behavior

## When this applies

Any agent working inside this folder: building, testing, releasing, deploying,
or documenting {{name}}. The folder is governed by the dev-and-deploy standard.

## Inputs

| File | Kind | Load when |
|------|------|-----------|
| .aai/references/dev-standard.md | reference — internalize as constraints | always |
| .aai/identity.md, .aai/purpose.md | who this project is and why | always |
| .aai/context.md | routing map; find files without reading them | always |
| .aai/HANDOFF.md, .aai/checkpoint.md | where the last session stopped | at session start |
| spec/ | what it must do | before changing src/ |
| ~/.aai/rules/coding.md, capability-authoring.md | universal policy (never duplicated here) | per their triggers |

## Process

1. Read HANDOFF.md, then run `make` to see the numbered pipeline map.
2. Studio mode by default: change spec/ by decision, src/ with a test, verify
   just enough. Release mode only when the user says "release".
3. Every stage is a command: `make run`, `make check`, `make rc`, `make uat`,
   `make release`, `make deploy`.
   A stage that has no passing command is not done.
4. Before ending a session: check branches and worktrees (`git worktree list`,
   `git branch --no-merged main`) and apply the standard's §5 rule: delete merged,
   clean branches with their worktrees; flag, never delete, any branch idle 14 days
   with uncommitted or unmerged work. Then rewrite `.aai/HANDOFF.md` (where we
   stopped and why, plus `## Branches kept`) and `.aai/checkpoint.md`
   (done / touched / open / next).

## Outputs

- Code → `src/` (or the kind's folder). Proof → `tests/`. Config → `deploy/<target>/`.
- User docs → `docs/`. Decisions → `spec/`. Agent state → `.aai/`.
- Regenerable output → `build/`, `runtime/` (gitignored). Durable user state → `data/`, never regenerable.

## Rules

- Never edit VERSION by hand; `make rc` and `make release` own it.
- Tag only through the lane: rc tags on the branch, release tags on `main`.
- Never push without Lou's say-so; nothing in the pipeline pushes.
- Empty folders are not created ahead of need.
- Append gotchas here as real failures surface; do not restructure.
