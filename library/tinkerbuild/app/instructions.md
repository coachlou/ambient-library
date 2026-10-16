# tinkerbuild

Gives a folder the ability to build a personal app the way one person tinkers: idea → UI → walking
skeleton → features and fixes in a no-human-in-the-loop loop → light checks → a QA pass at release →
keep using it and feed fixes back in. Not for productized or enterprise work.

`<skill>` below is this skill's directory. `TB` = `python3 <skill>/scripts/tb.py --app <app folder>`.

## Pick the move

| User says | Do |
|---|---|
| new app / "I have an idea" | `TB init`, then `references/bootstrap.md` |
| anything bigger than one slice: a concept, a capability, several features, "it should also…" | `references/decompose.md` → tickets, then run (below) |
| "design X" / "how should this look" / "redesign X" | design options only (see Design gate), stop for the pick |
| "build X" / "just build it" | build; no design step, no question |
| one clear add / change | `TB ticket add --kind feature\|enhancement --title "…" --touches "<modules>"`, then run |
| fix / "it broke when…" | `TB ticket add --kind fix --title "…" --body "…"`, then run |
| "work the backlog" / "run the tickets" | run |
| "release" / "ship it" | `TB release` (see `references/qa.md`) |
| "what's going on" | `TB status`, `TB ticket list` |

## Design gate

Decide by what the change does, not by the user's wording. It **needs design** if it adds a
screen, a control, or a flow that `.tinker/design/design.md` does not already cover. Backend
work, fixes, and changes that reuse an existing pattern do not.

- **User present, not told "design" or "build":** ask once: "This changes the UI. Design first
  (recommended) or build straight?"
- **Design:** 2-3 options, scoped to the change. For a feature in an existing app, compare
  *interactions* (settings page vs inline picker vs curated defaults), not visual styles; full
  3-5 visual directions are for a new app (`references/bootstrap.md` step 2). Update `design.md`
  with the pick before building. The feature is not done until `design.md` covers it.
- **Unattended (headless run, or user away):** never wait. Still mock the 2-3 options into
  `.tinker/design/`, pick the one that reuses existing patterns and adds the fewest screens,
  build it, and append a Decision line to `.tinker/architecture.md` tagged `(review)` with the
  options and why. The end report leads with every `(review)` line: "Chose A over B, C because…
  keep or swap?" The user clearing the tag is the approval.
- **Hard stops, even unattended:** sending user data to an outside service, adding a paid
  dependency, deleting or moving user files. Park the ticket with the question and move on.

## Two ways to run a ticket (same core)

- **In-session** (you are the agent): `TB intake`, take the oldest open ticket, follow
  `references/loop.md` yourself, then run the config's `check_cmd` and, if green,
  `TB ticket set <id> --status done`, add a changelog line, commit. If red, retry with the output up to
  `max_attempts`, then `TB ticket set <id> --status parked` and tell the user.
- **Headless** (spawn fresh agents): `TB run`. It does the same with the configured adapter. Use it
  to clear a backlog, from a script or a scheduler, or from a harness that cannot do the loop itself.

Adapters (`adapters/*.json`) are the only harness-specific part: a command that reads a prompt on
stdin and runs one agent task in the app folder. Config `inference.chain` orders them: `claude`,
`codex` (both verified shapes), `orca` (stub, unverified). Subscriptions first, API only as an
approved last resort, optional per-role model/effort: `references/inference.md`. The same
settings shape goes into every agent-driven app you build (`templates/inference.json`). Add your
own adapter by dropping a JSON file in `<app>/.tinker/adapters/`.

## Intake from the app

Errors the app catches and the in-app "Report a problem" button write a JSON file to
`.tinker/inbox/`; `TB intake` makes it a ticket and notifies the user. Snippets:
`templates/report-button.md`. Set `notify_cmd` in `.tinker/config.json` to be pinged
(`$TB_MSG` holds the message), e.g. `osascript -e 'display notification "'"$TB_MSG"'" with title "tinker"'`.

## Architecture and seams

`.tinker/architecture.md` is the one design document: modules (deep, one concern each), seams
(every boundary has a schema and a contract check in `.tinker/seams/*.sh`), data, decisions.
Written at the skeleton, read before every slice, appended by any slice that changes a module or
seam (`references/architecture.md`). The per-ticket gate is `check_cmd` **plus** every seam check,
so testing stays scoped to the slice: it is correct, the core path runs, and the seams still hold.

## Rules

- The check gate is `check_cmd` + seam checks exiting 0, never your own say-so.
- No human wait: decide small things, park what you cannot finish or a hard stop, report at the end, pending `(review)` picks first.
- Keep it small. Personal app: no coverage targets, no ceremony.
