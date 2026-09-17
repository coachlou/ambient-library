# propose-upstream

The production-build counterpart of `propose.md`. An installed library
(`.aai/PRODUCTION` present) is read-only, so a proposal drafted here cannot be
staged in place — it has to travel to the dev workspace's `in-progress/`. This
subskill drafts the proposal and delivers it by the first route that works.

## CRITICAL: never draft without an explicit yes

Opt-in only. Either the user asks ("save this as a skill", "propose a skill",
"propose a change to <name>", "remember how we did this"), or you *offer* in
one sentence after finishing a task no library skill covered. Silence or
anything short of yes means no. Never auto-propose.

## CRITICAL: author from the trace, not from imagination

Build the draft from what actually happened this session — steps taken,
commands run, corrections the user made. If the session lacks enough substance,
refuse: say there's not enough trace to author from, and stop.

## Draft

Pick a kebab-case `<name>`. Write two files into a temp folder (`$TMPDIR` or
`/tmp`), same contract as `propose.md`:

- `instructions.md` — the skill body, same conventions as a domain skill.
  Sibling references use `${CLAUDE_PLUGIN_ROOT}/library/<name>/<file>`, the
  path it will have once promoted.
- `PROPOSAL.md` — exactly: **Proposed description**, **Source trace**,
  **Evidence**, **Overlap check**. For a revision of an existing skill, the
  overlap check names the skill and states what changes and why.

## Deliver — first route that works

1. **Dev workspace on this machine.** Read `~/.aai/context.md`, find the
   `Dev source (canonical-library)` row, and check the path has
   `.aai/instructions.md` and no `.aai/PRODUCTION`. If so, copy the draft to
   `<dev>/in-progress/<name>/`. If that folder already exists, append to its
   `PROPOSAL.md` Evidence section instead of overwriting. Tell the user it is
   there and that "promote <name>" in a dev session moves it into the library.
2. **GitHub issue.** Otherwise, if `gh auth status` succeeds: show the user the
   full issue text (title `[proposal] <name>`, body = PROPOSAL.md then
   instructions.md in a fenced block) and get a second explicit yes — an issue
   is public. Then `gh issue create -R coachlou/ambient-library --title
   "[proposal] <name>" --body-file <file>`; add `--label proposal` only if that
   label exists. Report the issue URL.
3. **Local mailbox.** Otherwise write to `~/.aai/proposals/<name>/` and tell the
   user it is waiting there for a session that can reach the dev workspace.

## Hard limits

- Never write inside the installed library, any `.ailib/`, `catalog.yaml`,
  `SKILLS.md`, or `marketplace.json`.
- Never edit an existing `library/<name>/` — a revision is a proposal too.
- Never open an issue without showing its text and getting a separate yes.
