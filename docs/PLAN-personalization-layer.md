# PLAN — capability / project layer (opt-in 1:n)

Status: **design draft v4.5, not built.** 2026-09-17. v1–v3.1 solved a narrower
problem (branding config for one user). v4 re-founded the design on Lou's
app/file framing; v4.3 folds in three independent reviews of the v4 line and
Lou's governing principle below. Review loop closed (iteration cap reached).

## Governing principle

**1:n is an opt-in aai/ailib evolution of the standard skill, not a replacement.**

- **Default = the standard skill mechanism.** Root folder = the workspace = cwd,
  one project per folder. A skill that doesn't opt in is untouched, carries zero
  new tokens, and is never migrated. `SKILL.md` stays standards-compliant
  (Anthropic/OpenAI); everything here is additive files beside it, and a
  harness that knows nothing of aai still runs the skill on cwd.
- **A skill may opt in** to having its workspace *selectable* instead of
  defaulted to cwd, and — as a further option — to recognizing **many projects
  under one folder**. The multi layout is stamped explicitly (at install or by
  the skill's `init`), never inferred.

## Operating constraint (Lou, 2026-09-17)

**Minimal user knowledge and intervention.** A human in the loop at install
time is fine; after that, as little as possible. The user never needs to know
a file name, a folder convention, or a command. Consequences, applied below:

- Everything on disk is written by the agent or a script, never by hand. "In
  this project always do X" → the agent writes `overrides.md`. "Set up newco" →
  the agent stamps the project.
- Resolution is **code, not prose** (§5) — deterministic, so it doesn't ask
  questions a rule could have answered.
- The agent asks only on true ambiguity: one child project → use it; an unnamed
  request mid-session → the session's current project (re-read from disk).
- Nothing the user must remember to run: no manual checks, no permission
  toggles, no maintenance commands.

## The model

*The capability is the app. A project folder is the file it works on.* One app,
many files. Three things:

| Thing | Holds | Lives | Flows |
|---|---|---|---|
| **Capability** (app) | logic, templates, tooling | `.ailib/<n>/` or `~/.ailib`, pristine | — |
| **Project** (file) | what this piece of work *is*, plus its context/data | the project folder: `.aai/` for what only the capability needs; the folder root for user input/output | **never sideways, never up** |
| **Environment** (app preferences) | accounts, runtime, tool bindings, operator identity | the folder that received the capability, else `~` | **inherits down** |

The whole mechanic is **one pointer — the workspace.** Every path the skill
reads or writes is workspace-relative; environment is what you find walking
*up* from it. The pointer is never persisted: it is resolved per request,
re-read from disk, and stated before every write or send. (gears today stores
an "active org" in its database — a second pointer, and exactly how cwd says
acme while the pointer says globex.)

Precedent already in the library: **solofactory** (`projects/<name>/`
workspaces, app-level state in the parent's `.aai/memory/solofactory/`).

## Design

### 1. Opting in — `contract.yaml` beside the skill body

```yaml
# library/gears-content/contract.yaml        (all values empty in canonical)
multi: true               # omit for single-project skills
environment:              # inherited; how the app runs here
  supabase_project_ref:
  operator_name:
project:                  # travels with the project folder
  org_id:
state:                    # project-relative; where this capability reads/writes
  - .aai/memory/gears-content/    # capability-only: run log, last-published
  - output/                        # user-facing deliverables
```

One file is the opt-in, the schema, the hints, and the answer to "where does
this project's state live." Canonical carries empty keys. No secrets —
credentials stay in `.env` / the harness; a key may *name* the env var.

**Which class is a key?** Copy the project folder to another operator's
machine. The value must travel with it → `project:`. It would be wrong there →
`environment:`. In doubt → project. Keys that must agree (`account_alias` +
`from_address`) share a class. A project that needs a different environment
holds its own whole `environment.yaml`.

### 2. Layouts

```
single (default)                          multi (stamped by install/init)
newsletter/                               clients/
├── .aai/skills/aimm-newsletter/          ├── .ailib/gears-content/            app
│   └── project.yaml                      ├── .aai/skills/gears-content/
├── .aai/memory/aimm-newsletter/          │   └── environment.yaml             inherited
└── issues/ …                             ├── acme/
                                          │   ├── .aai/skills/gears-content/project.yaml
(environment.yaml: here, or ~/P)          │   ├── .aai/memory/gears-content/
                                          │   └── output/ …
                                          └── globex/ …
```

`P` = `.aai/skills/<n>/`. A folder is a project of `<n>` iff it has
`P/project.yaml`. There is no mode flag on disk: the stamped layout is the
configuration. `init` = write `environment.yaml` at the receiving folder and
run New for each project the user names.

### 3. Resolution

```
start        a path the request gives; or a name = child of cwd, else sibling of the
             current project; else cwd
             name given but no such folder: set-up intent → New there; otherwise ask.
             NEVER fall back to cwd or an ancestor when a name was given.
workspace    1. nearest folder at/above start with P/project.yaml   (stop below ~ / at volume root)
             2. [multi] cwd is a receiving folder (has P/environment.yaml or .ailib/<n>/)
                with no project.yaml of its own → ask which child project, or New
             3. otherwise → workspace = cwd — the standard behaviour.
                No project.yaml there yet: confirm "set up <cwd> as a <n> project?"
                (declined → stop), ask the project keys, write it.
environment  nearest P/environment.yaml at/above the workspace → ~/P/environment.yaml
             a new one is saved in P of the nearest ancestor that holds .ailib/<n>/
             (never a project folder, never inside .ailib/), else ~/P
capability   fork (.aai/skills/<n>/ with instructions.md) → .ailib/<n>/ → ~/.ailib.
             For opted-in skills only, .ailib/<n>/ is looked for up the same walk,
             so clients/.ailib/<n>/ serves clients/acme/. Others: unchanged.
             Then append .aai/skills/<n>/overrides.md, if present, as extra rules
             after whichever body resolved.
```

**One folder per owner (decided 2026-09-17).** `.aai/` is yours and no update
ever writes in it; `.ailib/` is the library's, pristine and replaced wholesale;
`~/.ailib` is the installed library. Canonical copies are *not* nested in
`.aai/library/` — that would make every update write inside the owned folder.
`.ambient/` and `~/.aai/library/` are retired: a second owned folder doing
`.aai/`'s job.

**`overrides.md` is kept, relocated (decided 2026-09-17).** It is the only way
to add a small prose rule to a skill without forking it off upstream updates —
contract keys can't do that. It lives in `.aai/skills/<n>/` beside
`project.yaml`: the project folder holds the project's data *and* its rules.
Project scope only; the `~`-level override was never used and is dropped until
needed. Ceiling: standalone installs bypass `load.md`, so they don't see it —
opted-in skills may add "then apply `P/overrides.md` if present" to their block.

- **New** = create the named folder if needed, ask the `project:` keys, write
  `P/project.yaml`. Nothing else.
- **Enablement needs no new router rule:** a `P/project.yaml` found by the walk
  enables `<n>`; at the receiving folder `.ailib/<n>/` already does. The one
  tightening: a `.aai/skills/<n>/` enables a skill only if it holds
  `instructions.md`, `project.yaml`, or `overrides.md` — an environment-only folder (notably
  `~/P/`) enables nothing.
- **Files are used whole; never merge two of the same class.**
- `state:` paths resolve under the workspace only. Nothing is read from or
  written to a sibling project.
- **Every request re-resolves.** Before any write or send, re-read
  `project.yaml` from disk and state the workspace folder. Placeholders are
  lookups at use, not a one-time substitution — this is what survives a
  mid-session switch ("now do globex") and context compaction.
- New creates `project.yaml` only; state folders appear on first write.
- Deleted from earlier drafts: the `~` default project (cwd fallback covers
  the one-newsletter user and removes the "quietly picks Lou's audience"
  hazard), per-file shadowing, name-matching on yaml values, and any
  router-wide rule that would touch non-opted-in skills.

### 4. Placeholders

`{{env.<key>}}` and `{{project.<key>}}`. Distinct from runtime placeholders
(`{{BODY_HTML}}`) and third-party merge tags. Behavioral values are labelled
switches in the body, not free prose.

### 5. Runtime — a resolver script, and a short block that calls it

§3 is a critical, order-dependent procedure. Three reviews each found the prose
version failing literal execution, and Lou's own skill rules say "scripts for
critical validations, not prose." So §3 runs as code.

**`scripts/resolve.py`** — one stdlib-Python source in this repo; the build
copies it into each opted-in skill's `scripts/` so it travels with vendored and
standalone installs alike (skills already may carry `scripts/`; nothing
non-standard). No hand-maintained duplicates; the audit checks the copies match.

```
resolve.py --start <path|name> [--current <project_dir>] [--intent setup]
  → {"project_dir", "project": {…}, "environment_file", "environment": {…},
     "state": [abs paths], "overrides": path|null}
  → or {"ask": ["acme","globex"], "can_create": true}      true ambiguity only
  → or {"needs": ["org_id"], "write_to": ".../project.yaml"} keys to ask once
resolve.py --init [--multi] --env k=v … --project name …    install-time stamping
resolve.py --set project.org_id=… | env.from_address=…      saves to the right file
```

Stdlib has no YAML parser, so `contract.yaml`, `project.yaml` and
`environment.yaml` stay inside a tiny subset the script parses itself: top-level
sections, `key: value`, `- item`, `#` comments (same approach as
`audit-distribution.py`'s catalog reader). Nobody hand-edits these files, so the
subset is not a user burden. Ceiling: nested values or multi-line strings need
a real parser — upgrade path is PEP 723 inline deps with `uv run`.

The split follows the step-classification rule: **inference** = read the
request for a path/name and set-up intent; **code** = the walk, the fallbacks,
where files get saved. The agent never decides where a file goes.

The block each opted-in skill opens with (literal skill name; audit-checked):

> **Project.** Before acting, and again before any write or send, run this
> skill's `scripts/resolve.py --start <path or name the request gives, else .>`
> (add `--current <last project_dir>` after the first run). Use only its output
> for `{{env.*}}` / `{{project.*}}` values; every path in the steps below is
> relative to `project_dir`; write nowhere else. If it returns `ask` or `needs`,
> follow its `do` line. Tell the user `project_dir` before any write or send.
> No shell available → ask the `project:` keys and work in the current folder.

~95 tokens, half the prose version, and it no longer has to be *correct as
prose* — only to get the script called.

**What this does and doesn't buy (audited).** It is determinism, not
enforcement: a cooperative-but-fallible agent gets the right answer every time
it runs the script, and the script is unit-testable. It does **not** stop an
agent that skips it — the yaml files are plain text it could read directly.
Nothing harness-neutral can. Two ideas considered and rejected against the
operating constraint:
- *Read-only `.ailib/` via chmod* — git doesn't preserve write bits, the agent
  can undo it, and lifting it for updates is user-facing friction. `.ailib/` is
  already replaced wholesale on update, which silently heals stray edits.
- *Post-run write check* — catches writes outside the project, but the real
  hazard is wrong *values* sent externally, which it can't see; and its false
  positives (first environment save, other skills in the session) would
  interrupt the user. Upgrade path if a stray write is ever observed.

### 6. Guardrails

- **Preview before any irreversible action**, added to the skill's *existing*
  confirm step: project folder, both file paths, resolved values, target count.
  The only guard against "resolved, but the wrong project." Then grep the
  rendered template (before user content goes in) for `{{env.` / `{{project.` /
  `YOUR_`; a hit blocks the action.
- **`scripts/audit-distribution.py`:** for skills with a `contract.yaml` —
  every placeholder key exists in it; the block is present in the body file
  (`instructions.md` where `SKILL.md` is a redirect) and names the
  skill's directory; the bracketed sentence is present iff `multi: true`;
  canonical values are empty; no `YOUR_[A-Z_]+`.

## Contradictions with what exists

1. `load.md` line 13 counts any `.aai/skills/<name>/` as enabling. Tighten to
   "holds `instructions.md`, `project.yaml`, or `overrides.md`" (§3). No ancestor-union of
   manifests — that would change selection for every skill everywhere.
2. `.aai/instructions.md` and `ambient-folder` resolve a capability by first
   *directory* that exists; a yaml-only `.aai/skills/<n>/` would resolve to a
   body-less skill. Fix: "first directory with `instructions.md`".
3. `load.md` contradicts itself: line 13 says a fork in `.aai/skills/<n>/`
   enables a skill, but step 3 resolves the body through `.ambient/` →
   `~/.aai/library/` → canonical and never looks in `.aai/skills/` or
   `.ailib/` — so a fork is selected and the canonical body runs, and a pin is
   skipped. Neither overlay folder exists on disk. Fix: step 3 becomes fork →
   `.ailib/` → canonical, then append `.aai/skills/<n>/overrides.md`. The
   "Overlays" section of `docs/MANAGEMENT.md` is rewritten to match.
4. `ambient-folder`: a sub-folder gets `.aai/` "only when it has behavior of
   its own." Amend: `.aai/` without `instructions.md` is a data-only project
   folder and inherits behavior from above.
5. `.aai/memory/` is keyed by agent id at `~` and by skill name in projects.
   Accepted; noted so nobody "fixes" it.
6. gears-* select the client via `get_operator_org` / `set_operator_org` — a
   stored pointer competing with the folder. `project.yaml: org_id` replaces it.
7. Rule sites are mirrored under `distro/` by the build — edit source, rebuild.

## Worked examples

**aimm-newsletter — single-project (the default shape).** Opts in only to ship
unbranded. Environment: `account_alias`, `from_address`. Project: `org_name`,
`copyright_holder`, `group_name`, `unsubscribe_url`, `subject_prefix`,
`send_mode`. Lou's AIMM folder holds `project.yaml`; his sender lives in
`~/P/environment.yaml`. A client newsletter sent from the client's address puts
a whole `environment.yaml` in that project. Migration steps from v3.1 stand
(diff whole branded skill; publish → pull → write files → add to manifest →
repoint `aimm-send.md` → two-member test → archive → delete).

**gears-content — multi.** `supabase_project_ref` leaves `_shared/config.json`
and the hardcoded `project_id:` lines → `clients/…/environment.yaml`.
`project.yaml` is just `org_id` (slug and brand already live in the
`organizations` table). The operator/active-org init step and "switch org" are
deleted. `output/{slug}/` → `output/` in the project; `build_knowledge_hub.py`
moves into the skill (tooling, not a deliverable). gears-onboard's New *is*
client onboarding. Ceilings: DB rows are isolated only by `WHERE
organization_id`; upgrade path RLS per org. Bodies use `/mnt/skills/user/…`
(claude.ai sandbox, no folder tree) — there the skill degrades to asking the
project keys each session.

## Rollout — nothing migrates unless Lou picks it

1. **Shared rules (3 files), none of which alter a non-opted-in skill:**
   `.aai/skills/load.md` (line 13 tightening; step 3 rewritten to fork →
   `.ailib/` → canonical + `overrides.md`; "say which layer supplied the body"
   rule kept),
   `.aai/instructions.md` (capability = first directory with
   `instructions.md`), `library/ambient-folder/instructions.md` (data-only
   project folders; the option documented). `docs/MANAGEMENT.md` "Overlays"
   follows as its own one-file step.
2. **Resolver + proof (2 files):** `scripts/resolve.py` and
   `scripts/test_resolve.py` — asserts over a throwaway tree for: open by name
   from the parent; open from a nested path; New beside siblings; plain cwd
   with no layout; mid-session switch via `--current`; a named folder that
   doesn't exist; a sibling named from inside a project; a stamped parent with
   zero projects; a single child (no ask); first environment save; `--init`
   single and multi. Then one fresh subagent holding *only* the block + a stub
   skill confirms an agent actually calls it. Before anything live is touched.
3. **aimm-newsletter:** `contract.yaml`, `instructions.md`, `template.html`;
   migrate Lou's live setup. Every `YOUR_*` / `[YOUR PREFIX]` gets a key; the
   `${CLAUDE_PLUGIN_ROOT}` template path keeps working; `aimm-send.md` passes
   the AIMM project path (with no `~` default, a bare "send the newsletter"
   from elsewhere would offer to make that cwd a project).
4. **Audit:** `scripts/audit-distribution.py` + one test.
5. **gears-* (multi):** in ≤3-file sub-steps (~26 files carry the Supabase
   ref); only if Lou wants them converted.
6. **gears-broadcast:** remove the shipped segment ID and sender via a contract.

Not touched: every other library skill, including checkpoint / session /
context-mgr.

## Deliberately not built

- No project registry, stored active-project pointer, or "recent files."
  (A resolver script *is* built — §5 — reversing v4–v4.4.)
- No chmod lock on `.ailib/`, no post-run write check (§5, rejected).
- No per-key merge, defaults, types, provenance; no per-file shadowing; no
  user-scope forks; no `~` default project.
- **No contract versioning.** A new key is found empty and asked. Ceiling: a
  renamed key orphans old values; upgrade path is a `contract:` version line in
  `project.yaml` plus a changelog note.
- No locking: two agents on one project can interleave state writes. Upgrade
  path: a lockfile in the state folder.
- Child search is one level deep (`clients/2026/acme/` is not listed from
  `clients/`). Upgrade path: name the path.

## Open to challenge

1. **Project facts shared across capabilities.** Plan: gears-* become one
   capability with modes (they already share one selector), so one contract;
   elsewhere accept repetition.
2. **cwd fallback writes `project.yaml` into whatever folder you're in.** The
   confirm question is the guard. Alternative: refuse outside a stamped folder.
3. **Nearest-ancestor environment** lets a stray file shadow the intended one;
   the save rule no longer creates strays and the preview names the path.

## Decisions that are Lou's

- AIMM `send_mode`: individual (branded body) or bcc (`aimm-send.md`)?
- gears-broadcast's segment ID and sender are in public git history — leave or
  scrub?
- Collapse gears-onboard / -content / -init / -broadcast into one capability
  with modes? Delete the DB "active org" selector?
- Which skills opt in first (proposed: aimm-newsletter, then gears-*).

## Change log

- **v4.5 (self-audit + operating constraint):** minimal user knowledge after
  install; §3 moves from a ~190-token prose block to `scripts/resolve.py` + a
  ~95-token calling block; `--init` does install-time stamping; agent-mediated
  file creation everywhere; asks only on true ambiguity. Claims corrected: the
  script is determinism, not enforcement. chmod lock and write check rejected.

- **v4.4 (Lou's decisions):** canonical copies stay in a separate `.ailib/`,
  one folder per owner; `.ambient/` and `~/.aai/library/` retired;
  `overrides.md` kept and moved to `.aai/skills/<n>/`; `load.md` step 3
  rewrite is now part of rollout step 1, not conditional.

- **v4.3 (review 3, blockers only):** a named-but-missing folder never falls
  back to cwd; environment save location can't be read as "inside `.ailib/`";
  ancestor-union enablement dropped (it touched every skill) for a one-line
  tightening; pinned capability found up the walk for opted-in skills; multi
  ask fires on a stamped parent with zero projects; declined → stop; block
  honest at ~190 tokens.
- **v4.2:** governing principle — opt-in evolution, cwd default, no migration;
  `multi:` flag and stamped layout; cwd fallback replaces ask/`~`/New chain;
  `~` default project deleted; re-resolve + re-read before every write;
  ancestor-union enablement; key-class deciding rule; gears `project.yaml` =
  `org_id`; bounded search; stub-skill runtime check added; state-only skills
  and router-wide rules dropped.
- **v4.1:** review 1 of v4 (environment save location, walk stops below `~`,
  gears DB selector, per-file shadowing deleted, contradictions section).
- **v4:** re-founded on app / environment / project.
- **v1–v3.1:** three reviews on the single-scope values design.
