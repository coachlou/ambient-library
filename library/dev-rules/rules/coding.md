# Coding rules

Applies to every conversation that writes, changes, or reviews code, in any
folder, harness, or capability. Project instructions (`CLAUDE.md`,
`AGENTS.md`, `.aai/`) may tighten these rules for that project. They do not
loosen them silently; a project that needs an exception states it and why.

## 1. Design: deep modules, one owner per concern

1. **Deep modules.** A module's interface is the cost it imposes on every
   caller; its implementation is the value it hides from them. Keep the public
   surface small and let it hide real work: policy, sequencing, error
   recovery, caching, persistence, format details.
2. **One owner per concern.** Each concern (a domain concept, an external
   system, a data store, a policy) has exactly one owning module. Everything
   else reaches it through that module's public interface.
3. **Hide decisions, not steps.** Draw boundaries around decisions likely to
   change (storage format, vendor API, algorithm), not around the order steps
   run in. A module per pipeline stage sharing one data shape leaks that shape
   everywhere.
4. **Pull complexity down.** If a choice can be made correctly inside the
   module (defaults, retries, normalization, edge cases), make it there. Do not
   export a flag, option, or call-order requirement to avoid deciding.
5. **Dependencies point toward stability.** Entry points (CLI, routes, UI)
   depend on domain modules; domain modules depend on abstractions of
   infrastructure, never on entry points. No import cycles.

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

## 2. Changing code

- Read the code you are changing and the module that owns the concern before
  writing. Match the surrounding naming, idiom, and comment density.
- Extend the existing owner; do not create a parallel module beside it.
- Make the smallest change that fully solves the task. No speculative
  generality, no unrequested compatibility shims, no drive-by refactors mixed
  into a feature change.
- Public surface is a decision: every new public name must be needed by a
  real caller. Everything else stays private by the language's convention.
- A behavior change gets a test. Tests call the public interface; a test that
  must reach into private state signals a missing operation or a leaked
  concern.
- Never skip, weaken, or delete a test or check to get green. Fix the code, or
  stop and say why.

## 3. Before calling it done

- Run the project's own checks (tests, lint, typecheck) and read the output.
- Walk the red-flag table against your diff. A violation you cannot fix within
  the task's scope is reported, with a proposed fix, not hidden.
- Report what was verified and what was not, plainly.

## 4. Projects

- A folder scaffolded by `init-dev-project` also follows its stamped standard,
  `.aai/references/dev-standard.md`: lanes, the four `make` verbs, the layout,
  and the ship list. That standard governs where things live; these rules
  govern how code is shaped.
- A project's module map (for example `## Module Boundaries` in a WBS
  `.wbs/context.md`) is that project's statement of who owns each concern.
  Follow it, and propose a correction when it is wrong instead of working
  around it.
