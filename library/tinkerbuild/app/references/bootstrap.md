# Idea → brief → UI → walking skeleton

Run once per app, in order, recording each with `tb.py stage <name>` when it is done.
Same defaults rule as the loop: decide small things yourself, ask only what is costly to reverse.

## 1. brief  (`stage brief`)
Write `.tinker/brief.md`, one page: what it does; who it's for (the user); the 3-5 things it must
do; what is explicitly out of scope; where it runs (web / macOS / iOS / CLI / agent-driven).
Ask at most 3 questions, only for gaps you cannot sensibly default.

## 2. design  (`stage design`)
Show the user **3-5 genuinely different directions** for the key screens before committing to one
(different layout, density, navigation; not one design in five colour schemes). Seeing options side
by side is the point of this step; it is the one place in bootstrap worth a user decision.

- **In the Claude app** (Artifact tool available): make a Design artifact (`Artifact` quickstart,
  intent `design`), one artboard per direction, same screens in each. If the user has a Design
  System artifact, build on it; if not, offer once to make one from their pick so later apps
  inherit it. The user picks or mixes on the canvas; iterate there until they say go.
- **Anywhere else** (Codex, headless, no artifacts): write each direction as a plain HTML file,
  `.tinker/design/option-<n>.html`, and ask which.

Mock in the medium of the app: screens for web/desktop/mobile, terminal output as text for a CLI,
the 2-3 core exchanges as a transcript for an agent-driven app (plus any screen it has).

**Hand-off (the part builders use).** When the user picks:
1. Copy the chosen screens into `.tinker/design/chosen/` as reference. From a canvas:
   `Artifact read` with `path` `project/<board>.dc.html` for each chosen artboard, and
   `project/ds/<folder>/tokens.json` if a design system is installed. These are canvas component
   files, not runnable pages: a picture to read, not code to ship.
2. Write `.tinker/design/design.md`, stack-neutral, from what was picked. This is the contract:

   ```
   # Design: <option name>   (canvas: <link or none>)
   ## Tokens      colors (name: hex), type (role: family size weight), spacing scale, radii
   ## Screens     one line each: name, purpose, main regions, primary action
   ## Components  each reusable piece: name, what it shows, its states (empty/loading/error)
   ## Copy        exact labels, headings, empty-state text
   ## Keep from other options   one line, or none
   ```
3. One line in `brief.md`: the pick and why.

Builders read `.tinker/design/design.md` (and glance at `chosen/`), never the canvas, so every
harness and every stack gets the same design.

## 3. skeleton  (`stage skeleton`)
Thinnest end-to-end slice that runs: UI → logic → storage, one core path, nothing else, in the
brief's stack (it is never built on the canvas). Its UI is the primary screen from `design.md`.
Tokens become a `theme` module in the stack's own idiom (CSS variables for web, a Color/Font
extension for SwiftUI, an ANSI style table for a CLI) so later slices reuse it instead of
re-deriving the look. Web apps may lift markup and inline styles from `chosen/`, dropping the
canvas runtime (`support.js`, `<x-dc>`, `{{…}}`); other stacks translate.
Before writing it, write `.tinker/architecture.md` from the brief (shape in `architecture.md`
here): the one or two modules the skeleton needs and the one seam between them, with its schema
and `.tinker/seams/<name>.sh`. An app that calls a model also gets `inference.json` from
`templates/inference.json` and follows `inference.md`. Then set up the check: define `check_cmd` in `.tinker/config.json`
(see `checking.md`) so it launches the app and exercises that one path. Commit. Then `stage build`.

From here every request is decomposed into slices (`decompose.md`), each a ticket that goes
through `loop.md`.
