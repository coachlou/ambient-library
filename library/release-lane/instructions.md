# release-lane

The loop: **checkpoint** (repeat) → optional **systest** → **rc** → testers + staging →
**uat** (fixes go back through checkpoint, then rc again) → **release**.
`release_lane.py` asserts every gate a script can check; this file covers the judgment
and the pauses.

## Important

- **⏸ means stop and wait for the user.** Every push, merge to main, deploy and message
  to testers or users is its own step and needs a yes in chat. The script never pushes.
- **Find the script and config first.** Script: `<repo>/.ailib/release-lane/release_lane.py`,
  else `${CLAUDE_PLUGIN_ROOT}/library/release-lane/release_lane.py`. Config: `<repo>/.aai/skills/release-lane/project.toml`,
  data only; keys and defaults are in `DEFAULTS` at the top of the script. Never fork
  this skill for different paths or commands; set them in the config. Call it `RL` below:
  `python3 <script> <verb>`.
- **Never run `rc` or `release` past a failed gate** by editing around it. Exit 1 means
  the gate held; show the user the message. Exit 2 means the config is wrong; fix the config.
- VERSION is the final version from rc.1 on. The rc number lives only in the tag
  `vX.Y.Z-rc.N`. Fixes found in testing fold into the same version.
- `release` refuses unless HEAD's tree equals the last rc. Merge to main with
  `--no-ff`, so the rc tag stays an ancestor of the release.

## Modes

**checkpoint** (after each build step)
1. Group `git status` / the diff. If it mixes unrelated work, propose a split.
2. `RL check`. A failure means no commit; show the output.
3. Behavior changed (source touched, not just docs): a test should have changed too, and
   the changelog's `## Unreleased` needs a user-facing line. Draft one if missing.
   If the config has no changelog (`changelog = ""`), apply the project's own change
   record instead (its AGENTS.md names it).
4. Commit on a non-main branch.
5. ⏸ Push the branch?
Done: commit on a non-main branch, check exit 0.

**status** (read-only): `RL status`, plus a docs-drift pass: list areas whose code changed
since the last tag while their docs did not. Report on one screen. Change nothing.

**systest** (optional): `RL check`, then the config's `accept` command run directly
(`RL rc --dry-run` prints it); if the project has screens, a browser pass over the key
ones with a console-error check. Write `tests/acceptance/runs/<date>.md`: pass, fail,
skipped. Done: report written.

**rc**
1. ⏸ Confirm the bump (`minor` if Unreleased has behavior changes, else `patch`; ignored
   for rc.2+).
2. Docs sync: update the docs status flags as drifted, so the candidate ships what
   production will. ⏸ The user reviews the docs diff. Commit.
3. `RL rc --bump <kind>`.
4. ⏸ Push the branch and tag, then `RL deploy --channel staging`.
5. Install in staging **following the shipped install docs literally**. Where the docs
   are wrong, that is a UAT issue, not something to work around.
6. Draft the tester note from Unreleased: what's new, how to install, how to report.
   ⏸ Send.
Done: rc tag deployed to staging, staging install worked from the docs alone, note sent.

**uat**
- `add`: append a row to the UAT log (`id | reporter | rc | severity | status | commit`,
  severity `blocker|major|minor`, status `open`). Fix it through checkpoint.
- `close <id>`: status `fixed`, link the commit. Any fix means the next step is rc again.
- `defer <id>`: only on the user's say-so, for a major they accept shipping.
- `stable?`: `RL uat`, and the user's own criteria (days with no new rc, tester installs
  confirmed), which the project's config or README names.
Done: `RL uat` exit 0.

**release**
1. `RL uat`.
2. ⏸ Merge `--no-ff` to main.
3. `RL release` (asserts HEAD == last rc, re-runs accept, dates the changelog, tags).
4. ⏸ Push main and the tag, then `RL deploy --channel production`.
5. Verify the deployed instance reports the version.
6. Draft the announcement. ⏸ Send.
7. List merged branches. ⏸ Delete.
Done: release tag on main, deployed, version verified live.

## Gotchas

- A project with no testers skips rc: `RL release` on main with no rc tag bumps,
  accepts and tags in one step.
- `version_files` bump the first occurrence of the old version in each file, so lines
  of history further down survive. `version_check` (if set) runs after the bump.
