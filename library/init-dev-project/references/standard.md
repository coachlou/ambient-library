# Dev and deploy standard

One standard for skills, tools, skill-apps, and web apps. It names the lanes a
project moves through, the four verbs every repo answers to, and the six files
every repo carries. It is not a factory. You have built five factories
(software-dev-factory, recursive-development, agentic-state-harness,
grokbot ADLC studio, vibe-skilling); this reuses their surviving parts.

## 1. Lanes — where a thing lives, by maturity

| Lane | Location | Rule |
|---|---|---|
| **Scratch** | `GitHub/code experiments/<name>/` | Anything goes. Only rule: `README.md` first line = what it is + `Status:`. No git required. |
| **Incubator** | `GitHub/code experiments/tinkering/<name>/` | Shared private repo. Follows the folder contract (§3). One `HANDOFF.md` per sub-project. |
| **Project** | `GitHub/<name>/` own repo | Full contract. `main` is always releasable. Graduates from incubator by decision, not by event. |
| **Released** | a version tag on `main` + a publish target (§4) | Only the release channel puts it in front of a user. |

Move rule: incubator → project is an explicit decision, made when the thing
needs its own maintenance or distribution (its own issues, its own release
cadence, its own installers). Write the decision in the README. A tag is a
release event, not evidence a project needs its own repo; incubator projects
may tag. Project → released happens at the first tag that reaches a publish
target. Nothing moves down; dead projects get `Status: archived` in the README
and stay put.

## 2. Stages — the same loop for every kind

```
idea ──▶ studio ──▶ release ──▶ deploy ──▶ maintain
         (any order,  (full pass,   (one command,  (HANDOFF.md at
          just enough  only when     target in      end of every
          checking)    you say so)   README)        session)
```

This is vibe-skilling decision 5, applied to everything. Studio and release
are different modes, not phases; per-request checks in studio never substitute
for the cold end-to-end run in release.

**Gates** (a gate is a command that exits 0, not a checklist to read):

| Gate | Command | Passes when |
|---|---|---|
| studio entry | `make run` | it starts and you can touch it |
| release entry | `make check` | lint + unit + smoke pass, locally, in under a minute |
| release exit | `make release BUMP=patch` | acceptance passes on the built candidate, then: version bumped in one place, CHANGELOG line added, tag on `main` |
| deploy exit | `make deploy` | one smoke request against the deployed instance reports the released version, and `deploy/README.md` names the rollback |

## 3. Repo layout — one folder per concern

Two questions decide where a file goes: **who reads it** (human, agent, or
machine) and **does it ship**. Folders are created on first use, not up front.
An empty folder is the first sign of a template that is too heavy.

```
<repo>/
├── README.md              entry point: what, status, run, deploy. One screen.
├── VERSION  CHANGELOG.md  Makefile
│
├── spec/                  WHAT it must do. Written before code, changed by decision.
│   ├── SPEC.md            requirements + decisions log
│   ├── PROTOCOL.md        any wire or file contract, normative
│   └── adr/               one file per non-obvious choice, dated, never edited
│
├── src/                   HOW it does it. Ships (see the ship list, §4).
│   (or skills/, app-skills/, worker/ — whatever the kind dictates)
│
├── tests/                 PROOF, split by what it proves and how long it takes
│   ├── unit/              dev test: fast, pure, every `make check`
│   ├── smoke/             dev test: does it start, does one button round-trip
│   └── acceptance/        production test: end-to-end on the built candidate,
│                          real target. Only in `make release`, before the tag.
│                          Cold run on a second model only where it has caught
│                          a real failure; it is not charged to every release.
│
├── deploy/                WHERE it goes. Config only, no logic.
│   ├── <target>/          cloudflare/  docker/  library/  — one is active
│   └── README.md          which target is live, how to roll back
│
├── docs/                  FOR the user of the thing. Ships with it.
│   ├── help.md            command grammar, Help page source
│   └── examples/          one worked run
│
├── tools/                 FOR the builder. Never ships. Stdlib scripts with --help.
│
├── .aai/                  FOR the agent. Never ships.
│   ├── checkpoint.md      session state
│   └── HANDOFF.md         where we stopped and why; rewritten every session
│
├── build/                 regenerable output of `make check` / `make release`
├── runtime/               disposable state of a running instance: caches, pids,
│                          logs. Safe to delete at any time. Both gitignored.
└── data/                  durable state: user data, databases. Never regenerable,
                           never gitignored by default, backed up by `deploy/`.
```

### The four verbs

The Makefile is the pipeline: `run`, `check`, `release`, `deploy`. `make` alone
prints help. Targets call whatever tools the project already has (`lint_app.py`,
`smoke.py`, `try_app.py`, `package_app.py`, `wrangler deploy`, `docker compose
up`). A new kind of project changes the recipe bodies, never the verb names.

### Separation rules

- **Spec is upstream of everything.** A change to `spec/` needs a decision. A
  change to behavior in `src/` needs a test; docs, comments and low-risk edits
  do not. If they drift, one of them is wrong; fix that one, never let both
  float.
- **Tests split by cost and stage, not by module.** Unit and smoke run in studio
  on every `make check`; they are fast and local. Acceptance runs only in
  `make release`, against the candidate `build/` produces, and the tag is cut
  only after it passes. `try_app` transcripts are acceptance tests and live in
  `tests/acceptance/`, not in `build/`.
- **Deploy holds config, not code.** `wrangler.toml`, `compose.yaml`,
  `RELEASE.yaml` live in `deploy/<target>/`. `src/` does not know where it runs.
  Switching targets touches one folder.
- **Docs are two audiences, two folders.** `docs/` is for whoever uses the thing
  and ships with it. `spec/` and `.aai/` are for whoever builds it and never
  ship.
- **Regenerable means gitignored.** `build/`, `runtime/`, `__pycache__`. If
  `make check` can recreate it, git does not track it. `data/` is the opposite:
  if losing it loses a user's work, it is not runtime and `deploy/` says how it
  is backed up and restored.
- **The ship set is a whitelist, per kind.** Each kind in §4 names the ship
  list; `make check` verifies the built package contains exactly that list.
  `spec/`, `tests/`, `tools/`, `.aai/` are never on it. A production copy
  cannot author because the files are not there, not because a policy says so.
- **Universal rules stay in `~/.aai/rules/`.** Coding policy, skill authoring,
  commit style. Nothing in the repo duplicates them.

## 4. Kinds and their publish channels

| Kind | Source shape | `make check` | Ship list | `make deploy` target |
|---|---|---|---|---|
| **skill** | `SKILL.md` or `instructions.md` + `references/` + `scripts/` | skill-auditor + trigger evals | `SKILL.md`, `instructions.md`, `.claude-plugin/`, `references/`, `scripts/`, `templates/`, `docs/` | ambient-library → `RELEASE.yaml` → `build-production.sh` → aai-library-release → `~/.ailib` |
| **tool** | one Python file, stdlib, `--help`, `--json`, no prompts | `python3 tool.py --help` + one `test_*.py` | the one file | rides inside a skill's `scripts/`; standalone = `pyproject` + `uv` |
| **skill-app** | vibe-skilling folder (bridge/dashboard/scripts/adapters) | `lint_app` + `smoke` + `try_app` | what `package_app` emits | `package_app` → same skill channel |
| **web app / service** | repo with `wrangler.*`, `Dockerfile`, or `vercel.json` | typecheck + build + one smoke request | `src/` + `docs/` + the target's manifest | Cloudflare (`wrangler deploy`), Docker on Hostinger, or Vercel; **one** of them, named in README |

The skill channel already exists and already has the right property:
committing does not release, a one-line `RELEASE.yaml` edit does. Web apps get
the same property from the tag: `make deploy` refuses on an untagged commit.

## 5. Versioning and git

- One version, one file (`VERSION`, or the single manifest the platform forces:
  `package.json`, `pyproject.toml`, `manifest.json`). `make release` reads it,
  bumps it, and rewrites every copy that must match. No hand edits in N places.
- `main` is always releasable. Work on `claude/*` or `feat/*` in a worktree.
  Squash-merge, delete the branch, delete the worktree, tag on `main`.
- Every tag gets a CHANGELOG line. Pushing tags is a deliberate `make release
  PUSH=1`, never implicit.
- `.aai/HANDOFF.md` is rewritten, not appended, at the end of every session;
  history is in git.

## 6. What this standard deliberately leaves out

- No state machine, no WBS tree, no leases, no evidence ledger. Those were the
  factories; use one only when a project outgrows `make check`.
- No CI until a repo has a second committer. Local `make check` before tag is
  the CI.
- No new tooling. The scaffold skill in this folder drops the root files, a
  Makefile with four stub targets, and `.aai/`. Other folders appear on first
  use. That is its whole job.

## Decisions

1. **Makefile** is the pipeline entry point (decided 2026-09-30). Zero install on
   macOS, agents know it, one entry point.
2. `tinkering/` stays an incubator; graduation is a written decision in the
   README, not a tag (revised 2026-09-30, was "at first tag").
3. Open: which ten lines of this go into `~/.aai/rules/coding.md` as doctrine.
4. v0.2.0 (2026-09-30) adopts all four findings of a codex review: graduation
   rule, per-kind ship list, check/acceptance split, deploy proof + `data/`.
   The standard is piloted through this skill and a web app before any of it
   becomes `~/.aai` doctrine.
