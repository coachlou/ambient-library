# Plan: Global Librarian + Gated Self-Extension

**Goal.** Two gaps stand between the current repo and "skills are just there in
every folder, and the library grows from real work":

1. **Global availability** — today `ambient` must be installed per project.
   Make it available in every folder Lou works in with zero per-folder setup.
2. **Self-extension** — when a task has no matching skill, the agent can draft
   one from the real task trace into a staging area; promotion to the canonical
   library is a deliberate, reviewed step. Never auto-commit to the catalog.

Everything else the "single librarian agent" idea needs already exists here:
one registered `ambient` skill, `.aai/instructions.md` router,
`library/catalog.yaml` cheap index, load-on-demand domain skills. Do not
rebuild any of that. Do not create a standalone harness, daemon, or agent
binary.

**Execution rules for the implementing agent (read first):**

- Read `ARCHITECTURE.md`, `.aai/instructions.md`, `.aai/skills/admin.md`,
  `.aai/skills/load.md`, and `templates/aai/README.md` before editing anything.
- Match the existing voice and format of the subskill files exactly — terse,
  imperative, gotchas up front. No headers-for-show.
- All skill-internal paths use `${CLAUDE_PLUGIN_ROOT}/...`, never absolute or
  repo-relative paths (see admin.md for why).
- Work in this source clone only. Never edit an installed plugin copy.
- Bump `version` in `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json`
  once, at the end.
- One commit per workstream, message explains *why*.

---

## Workstream 1 — Global availability

### 1.1 Verify what Claude Code already gives us

Before building anything, check (via `claude plugin --help`, the local docs, or
the claude-code-guide agent): when a plugin is installed from a marketplace at
**user scope**, is it enabled in every project automatically, or per-project?

- **If user-scope install is already global:** the deliverable is documentation
  only. Update `docs/INSTALLATION.md` with a "Install once, everywhere" section
  giving the exact commands (add marketplace from the local clone path, install
  `ambient` at user scope). Skip 1.2. This is the preferred outcome — do not
  build the shim if this works.
- **If enablement is per-project:** build 1.2.

### 1.2 User-level pointer shim (only if needed)

A personal skill in `~/.claude/skills/ambient-library/SKILL.md` that does what
`templates/AGENTS-pointer.md` does, but as a registered user-level skill so it
triggers in every project:

- Frontmatter: `name: ambient-library`; description copied from the `ambient`
  plugin's skill description (`skills/ambient/SKILL.md`) — reuse, don't rewrite,
  descriptions are tuned triggers.
- Body: "Treat `${CLAUDE_PLUGIN_ROOT}` as `<CANONICAL_CLONE_PATH>`. Read
  `<CANONICAL_CLONE_PATH>/.aai/instructions.md` and follow it." Nothing else —
  the router does the rest.
- Deliverables:
  - `templates/user-shim/SKILL.md` — the template, with a
    `<CANONICAL_CLONE_PATH>` placeholder.
  - `scripts/install-global.sh` — copies the template into
    `~/.claude/skills/ambient-library/`, substituting the placeholder with this
    clone's absolute path (`git rev-parse --show-toplevel` of the *main*
    worktree, not a linked worktree). Idempotent; `--dry-run` flag; refuses if
    the target exists unless `--force`.
  - `docs/INSTALLATION.md` section documenting it.

**Precedence gotcha to document:** if a project *also* installs the `ambient`
plugin, both the plugin skill and the user shim may match. Note in the shim
body: "If an installed `ambient` plugin is active in this project, defer to it."

### Acceptance (WS1)

- From a folder with no `.claude/` config at all, a request like "what skills
  cover writing an article?" reaches the canonical router and answers from
  `catalog.yaml`. Verify manually with `claude -p` from an empty temp dir and
  record the transcript result in the commit message or PR notes.

---

## Workstream 2 — Gated self-extension (propose → stage → promote)

### 2.1 Staging area

Create `library/_staging/` with a `README.md` (~10 lines) stating the contract:

- Skills here are **proposals**: drafted from real task traces, unreviewed,
  not in `catalog.yaml`, not in `SKILLS.md`, not in `marketplace.json`, never
  loaded by the router's selection flow.
- Each proposal is `library/_staging/<name>/` containing `instructions.md`
  (same format as a real domain skill) plus `PROPOSAL.md`.
- Promotion or deletion goes through `admin.md`. Nothing auto-promotes.

Underscore prefix keeps it sorted apart and signals "not a skill". Confirm
nothing globs `library/*/instructions.md` indiscriminately (grep the repo;
the router reads only the catalog, so this should be safe — verify).

### 2.2 New subskill: `.aai/skills/propose.md`

Written in the same voice as the other subskills. Behavior:

1. **Trigger context:** the user just completed (or is completing) a task the
   library didn't cover, and asks to "save this as a skill", "propose a skill
   from this", "remember how we did this" — or the agent finished such a task
   and *offers* ("No library skill covered this; want me to draft one into
   staging?"). The offer is one sentence; silence means no. Never write to
   staging without an explicit yes.
2. **Source from the trace, not from imagination.** The draft must be built
   from what actually happened in the session: the steps taken, the commands
   run, the corrections the user made. If the session lacks enough substance
   (one-liner tasks, pure Q&A), refuse: "not enough trace to author from."
3. Write `library/_staging/<name>/instructions.md` — same conventions as a
   real domain skill (kebab-case name, `${CLAUDE_PLUGIN_ROOT}` sibling paths,
   description phrased as *when it applies*).
4. Write `library/_staging/<name>/PROPOSAL.md` with exactly these fields:
   - **Proposed description** (the one-line catalog entry it would get)
   - **Namespace** (existing namespace or "none")
   - **Source trace** (date, project, 2–3 sentence summary of the task it
     came from)
   - **Evidence** (what in the session shows the pattern is real/repeatable)
   - **Overlap check** (nearest existing catalog entries and why they don't
     cover this)
5. **Hard limits:** never touch `catalog.yaml`, `SKILLS.md`,
   `marketplace.json`, or plugin versions. Never edit an existing library
   skill from here (that's admin). Operates on a source clone only — same
   locate-the-clone steps as `admin.md` (copy that section's logic, reference
   it, don't duplicate the prose).
6. If a staging proposal with the same name exists, append to its PROPOSAL.md
   Evidence section instead of overwriting — repeated proposals are the
   strongest promotion signal.

### 2.3 Router wiring

In `.aai/instructions.md` routing table, add one row:

| Save/draft a new skill from work just done ("save this as a skill", "propose a skill", "remember how we did this") | `.aai/skills/propose.md` |

Add one line to the existing Disambiguation paragraph: "create a skill **in
the library**" with content the user supplies is admin; "save **this
session's work** as a skill" is propose.

### 2.4 Promotion path in `admin.md`

Add a "Promote a staged proposal" operation:

1. List `library/_staging/*/PROPOSAL.md` on request ("what's in staging?").
2. To promote `<name>`: review `instructions.md` against the overlap check;
   present the proposal summary and get an explicit go-ahead.
3. Then run the **existing** "Create a domain skill" steps (move the folder to
   `library/<name>/`, drop `PROPOSAL.md`, add catalog + SKILLS.md entries, add
   a `marketplace.json` plugin entry if the other skills have one, bump
   versions).
4. "Reject <name>" deletes the staging folder.

Do not duplicate the create steps — reference them.

### 2.5 Docs

Add a short "Self-extension" section to `docs/MANAGEMENT.md`: the
propose → stage → promote lifecycle, and the rationale (self-generated skills
underperform unless authored from real traces and reviewed; routing quality
degrades if the catalog fills with unvetted entries).

### Acceptance (WS2)

- `library/_staging/README.md` exists; staging is invisible to routing
  (grep confirms nothing reads `_staging` except propose.md and admin.md).
- Router table routes "save this as a skill" to propose.md and "add a skill to
  the library" to admin.md — check the disambiguation reads unambiguously.
- Dry-run test: in a scratch session, complete a small multi-step task, invoke
  propose, confirm a well-formed proposal lands in `_staging/` and nothing
  else changed (`git status` shows only the two new files).
- Promote the test proposal via admin, confirm catalog/SKILLS.md/marketplace/
  version all updated; then revert the test commit.

---

## Explicitly deferred (do not build)

- **Namespace-first routing / hierarchical catalogs** — flat catalog is fine
  at ~46 skills; revisit past ~150 or when routing errors show up.
- **Auto-proposal without user confirmation** — rejected by design.
- **Standalone agent/daemon/harness** — the harness is Claude Code; this repo
  is content, not runtime.
- **Skill usage telemetry** — nice for the rewrite loop, separate project.

## Order and sizing

WS1 first (it may be docs-only), then WS2. WS2 touches four files plus two new
ones — commit 2.1+2.2 (staging + propose) separately from 2.3+2.4+2.5 (wiring +
promotion + docs) so each commit is reviewable.
