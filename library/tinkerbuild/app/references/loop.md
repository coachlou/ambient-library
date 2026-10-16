# The build loop (one ticket)

You are the builder for ONE ticket in a personal-use app. The ticket JSON is below.
Personal app, not a product: make it work, keep it small, skip enterprise rigor.

0. **Read `.tinker/architecture.md`.** Know which module owns this change and which seams it
   crosses (`touches` on the ticket). Design inside that: a deep module behind a small surface,
   data crossing seams only in the schema written there. See `architecture.md` in this folder.
   If the ticket has UI and `.tinker/design/design.md` exists, build to it: its screens,
   components, states and copy, styled through the app's `theme` module (never new hard-coded
   colors or fonts). A new screen, control or flow it doesn't cover: follow the Design gate in
   `instructions.md` (unattended path) before building, then update `design.md`.
0b. **Investigate the code, not just the docs.** The ticket says WHAT; the codebase decides HOW,
   and it may have moved since the ticket was filed. Before writing anything: read the code that
   owns this change and its callers; `git log` since the ticket's `created` for commits touching
   the same modules; skim done tickets with overlapping `touches`. Then decide:
   - fits: build on what is there (reuse, don't duplicate).
   - earlier work must change to satisfy this ticket: change it in this slice, and say so in
     the ticket's `accept`.
   - this ticket contradicts a done one (same behavior, different outcome): the newer ticket
     wins; append a Decision line naming both. If the choice is expensive to undo, park instead.
   - already satisfied by existing code: verify with `accept`, mark nothing new built, stop.
1. **Shape.** If `accept` is empty, write 2-4 lines of observable acceptance into the ticket file
   (`.tinker/tickets/<id>.json`, field `accept`). For a fix, reproduce the bug first. Default any
   ambiguity yourself; only an expensive-to-undo choice is worth stopping for. If the ticket is
   more than one vertical slice, do not build: split it per `decompose.md` (children with
   `--parent`, this one `--status split`) and stop.
2. **Build.** Smallest change that satisfies `accept`. Reuse what exists. No unrelated cleanup;
   put anything extra you notice in a new ticket (`python3 <skill>/scripts/tb.py ticket add ...`).
   If you changed a seam's schema or a module's surface, update `.tinker/architecture.md` and
   the seam's `.tinker/seams/<name>.sh` in the same slice, and append a dated Decision line.
3. **Run it.** Actually start the app and exercise the changed path (see `checking.md` for how, by
   app type). Reading the code is not checking.
4. **Leave a check.** Feature/enhancement: add `.tinker/qa/<id>.sh`, a script that exits 0 when the
   feature works. Fix: add one only if the bug was real and could recur.
5. **Stop.** Do not mark the ticket done and do not commit; the driver runs `check_cmd` and does both.
   If the check fails you will be called again with its output: fix that, do not start over.

Dials (config `dial`): `hands-off` runs straight through, `steered` pauses before each ticket,
`pair` pauses before each attempt. The dial changes how much you show, not what you do.
