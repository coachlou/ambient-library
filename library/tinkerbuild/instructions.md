# tinkerbuild

Turns a folder into a personal app that tinkerbuild builds: idea to UI to walking skeleton, then features and fixes in a no-HITL ticket loop

## Install

```sh
curl -fsSL https://raw.githubusercontent.com/coachlou/ambient-library/main/library/ambient-folder/bootstrap.sh \
  | bash -s -- tinkerbuild [target-folder]
```

Re-running the same command is the update path: `.ailib/` refreshes, `.aai/` is left alone.
`--check` reports drift without writing. Requires: Python 3.10+.

## Operate

```sh
./tb.sh --help
```

`./tb.sh init` sets up `.tinker/` in this folder. Then follow `.ailib/tinkerbuild/app/instructions.md`:
idea → design → walking skeleton, then `./tb.sh ticket add --kind feature --title "..."` and `./tb.sh run`
to work the ticket loop.

## Maintain

- `.aai/` is yours. Edit `identity.md`, `instructions.md`, `context.md` freely.
- `.ailib/tinkerbuild/` is vendored. Never edit; re-run install to update.
- To override behavior, copy into `.aai/skills/tinkerbuild/` and edit there.

## Rules

- The app's own `instructions.md` (under `app/`) is the workflow; this file only covers install.
- Never mark tickets done or commit by hand; the `run` driver does both after `check_cmd` passes.
