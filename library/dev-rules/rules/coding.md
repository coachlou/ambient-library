# Coding Rules

Runtime-independent policy for coding scope, implementation, testing, approval, and
completion. Harness adapters route here. Runtime-specific tool instructions may supplement
this policy but must not override it. Do not duplicate these rules elsewhere.

Project instructions (`CLAUDE.md`, `AGENTS.md`, `.aai/`) may tighten these rules for that
project. They do not loosen them silently; a project that needs an exception states it and why.

Complete the current task with the **minimum sufficient change**: the smallest coherent
change that restores the required behavior or invariant — not necessarily the fewest
lines or files. This policy supersedes any "wait for approval before coding" rule:
read-only discovery and routine implementation within the stated task need no approval.

Trivial tasks (single file, a few lines) skip the written plan below; keep the judgment,
skip the ceremony.

## Design: deep modules, one owner per concern

1. **Deep modules.** A module's interface is the cost it imposes on every caller; its
   implementation is the value it hides from them. Keep the public surface small and let it
   hide real work: policy, sequencing, error recovery, caching, persistence, format details.
2. **One owner per concern.** Each concern (a domain concept, an external system, a data
   store, a policy) has exactly one owning module. Everything else reaches it through that
   module's public interface.
3. **Hide decisions, not steps.** Draw boundaries around decisions likely to change
   (storage format, vendor API, algorithm), not around the order steps run in. A module per
   pipeline stage sharing one data shape leaks that shape everywhere.
4. **Pull complexity down.** If a choice can be made correctly inside the module (defaults,
   retries, normalization, edge cases), make it there. Do not export a flag, option, or
   call-order requirement to avoid deciding.
5. **Dependencies point toward stability.** Entry points (CLI, routes, UI) depend on domain
   modules; domain modules depend on abstractions of infrastructure, never on entry points.
   No import cycles.

### Red flags: treat as defects

| Flag | Symptom | Correct move |
|---|---|---|
| Shallow module | Interface about as complex as its implementation | Merge into its caller or into the concern's owner |
| Pass-through | A method or wrapper only forwards arguments | Remove the layer, or give it a real responsibility |
| Leaked internals | Callers import private names or depend on internal data shapes | Expose an intention-revealing operation; keep the shape private |
| Split concern | The same rule, format, or query encoded in two places | Move it to the single owner; callers ask the owner |
| Caller-side sequencing | Callers must call A before B or it misbehaves | Fold the sequence into one operation |
| Option creep | A new boolean or mode parameter added for one caller | Decide internally, or add a distinct, named operation |
| Logic in entry points | Business rules inside CLI, route, or UI handlers | Move them to the owning module; keep the entry point a thin adapter |
| Dumping ground | `utils`, `helpers`, `common`, `misc` growing unrelated code | Move each function to the module whose concern it serves |

## Before editing

- Read the relevant code, tests, and configuration directly. Do not work from search snippets or guesses.
- Read the module that owns the concern you are changing, not only the file you are editing.
- If the requirement is ambiguous or the premise is unverified, resolve that before building on it.
- For non-trivial tasks, state a minimal plan:
  - **Outcome** — the exact behavior requested
  - **Non-goals** — what this task will not do
  - **Files** — the smallest set expected to change
  - **Proof** — the check that will prove the change works
- Start with one implementation path. Split work only when the task has genuinely independent parts.
- When multiple approaches exist, or a non-obvious choice is made (library, pattern, architecture), name the tradeoff — don't silently pick one.

## While editing

- Reuse existing code, helpers, patterns, and test setup before adding anything new.
- Extend the existing owner of a concern; do not create a parallel module beside it.
- Match the surrounding naming, idiom, and comment density.
- Public surface is a decision: every new public name must be needed by a real caller.
  Everything else stays private by the language's convention.
- Fix bugs at the root cause. Do not stack patches around a wrong premise. If a root-cause fix changes behavior outside the requested change, say so in the completion report.
- Add an abstraction, adapter, or config layer only when required by an existing architectural boundary, a stated requirement, or a second real caller in this task.
- Remove code you replace. Keep an old path only when compatibility is an explicit requirement.
- Keep recipient-facing documentation accurate — docs are not "unrelated" cleanup.
- Treat every workaround and scaffolding as temporary. Comment *why* it exists and when it can be removed.

## Pause and confirm

Read-only discovery of the local repository is always allowed. Get approval before:

- Touching more than ~3 files or materially expanding the scope (if the change can't fit in ~3 files coherently, break the task into smaller tasks instead)
- Adding a dependency, framework, service, or test infrastructure
- Changing a public API, schema, storage format, or wire format
- Committing, pushing, opening PRs, deploying, running migrations, or writing to any external system
- Accessing sensitive or production data, even read-only
- Deleting or overwriting user data, discarding uncommitted work, rewriting history, or keeping two implementations of the same behavior alive

## Git hygiene

- Stage specific files for commit, not `git add -A`.
- Never push to a remote without explicit user permission.
- Write commit messages that explain *why*, not *what*.

## Testing

- Run the narrowest tests that exercise the change, then any broader check justified by the change's blast radius.
- Add or update a test when behavior, an important invariant, failure handling, security, or data integrity changes — and only then. For a bug, first add a test that reproduces the failure when practical.
- Tests call the public interface. A test that must reach into private state signals a
  missing operation or a leaked concern.
- Never skip, weaken, or delete a test or check to get green. Fix the code, or stop and say why.
- Do not backfill unrelated coverage or introduce test infrastructure for this task alone.
- Do not use passing tests as justification for extra abstractions or scope.

## Projects

The dev-and-deploy standard is the source of truth; these are the rules an agent
breaks without it. In a scaffolded project, follow its stamped copy,
`.aai/references/dev-standard.md`: that is the version the project adopted. Elsewhere,
and when starting a project, use the canonical
`~/.ailib/library/init-dev-project/references/standard.md`.

- Start a new project with the init-dev-project skill, not a hand-built layout.
- In a scaffolded project, run `make` first to see the pipeline map; use its verbs, not ad-hoc commands.
- Write the spec in `spec/` before the code.
- Release only with `make release`; never hand-edit VERSION or tag by hand. It tests the exact candidate it tags.
- Deploy only with `make deploy`; it refuses an untagged commit.
- Only what `deploy/SHIPLIST` names ships; update it when the layout changes.
- `data/` is durable state; `build/` and `runtime/` are disposable.
- A project's module map (for example `## Module Boundaries` in a WBS `.wbs/context.md`) is
  that project's statement of who owns each concern. Follow it, and propose a correction
  when it is wrong instead of working around it.

## If the plan grows

Stop when the work starts adding future-use layers, workaround stacks, unrelated cleanup,
or tests for unstated behavior. Rewrite a smaller plan. Continue without asking if it stays
within the authorized outcome; confirm only if it changes scope, contracts, risk, or
acceptance criteria.

## Done means

- The requested behavior works and the acceptance criteria are met
- The project's own checks (tests, lint, typecheck) were run and their output read
- Relevant checks pass, with the exact commands and results reported
- The red-flag table above was walked against the diff; a violation that can't be fixed
  within the task's scope is reported with a proposed fix, not hidden
- Every touched file is necessary for implementation, verification, or keeping recipient-facing documentation accurate; the diff contains nothing unrelated
- No debug code, backup copies, dead paths, or scratch files remain
- Assumptions, limitations, and unverified runtime behavior are stated plainly
- Edge cases worth covering are listed, even when no test was added
