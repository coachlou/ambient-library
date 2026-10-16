# Decompose: conversation → slices

Input is whatever the user said, at any grain: a fledgling concept, one clear fix, a general
capability, or a whole app with few details. Output is tickets. Every ticket is one **vertical
slice**: UI → logic → storage for one observable behavior, buildable in one loop run.

## Steps

1. **Read `.tinker/brief.md` and `.tinker/architecture.md`** first (create them via `bootstrap.md`
   if the app is new). Slices are cut along the architecture's modules and seams, never across
   them at random. If `.tinker/design/design.md` exists, each of its screens is covered by at
   least one slice, and a UI slice's `body` names the screen and components it builds.
2. **Name the behaviors.** One line each, as the user would see it. A concept with few details
   gets the 3–5 behaviors that make it real; defaults fill the rest. Ask at most one question, only
   when two decompositions lead to different architectures.
3. **Cut slices.** Each slice passes: observable on its own, testable with a 2–4 line `accept`,
   touches one or two modules, finishable within `max_attempts`. Anything bigger is a parent:
   `tb.py ticket add --title "<parent>"`, then children with `--parent T-xxxx`, then
   `tb.py ticket set T-xxxx --status split`. The first child of a new app is always the walking
   skeleton (thinnest end-to-end path).
4. **Mark seams.** For each slice set `--touches "module,module"` and, if it changes a seam's
   schema, say so in `body` and add the architecture update to the slice's acceptance.
5. **Order.** Skeleton, then slices others depend on, then the rest. Tickets run oldest-first, so
   file them in that order.
6. **Report** the list in one screen: id, title, touches. Then run (in-session or `tb.py run`).

## Scoping the testing

Per slice: its own `accept`, the app's `check_cmd` (smoke of the core path), and every
`.tinker/seams/*.sh` (contract checks at module boundaries). That is the whole per-run guarantee:
the slice works, the core path works, and the seams still behave. Whole-app QA waits for release.
