# Capability install standard

Every capability in this library installs the same way. Learn it once.

## Install

```sh
curl -fsSL https://raw.githubusercontent.com/coachlou/ambient-library/main/library/ambient-folder/bootstrap.sh \
  | bash -s -- <capability> [target-folder]
```

Target defaults to the current folder. The installer writes:

| Path | Yours? | What |
|---|---|---|
| `.aai/` | yes, never overwritten | identity, instructions, context for this folder |
| `.ailib/<capability>/` | no, vendored | the capability itself, re-synced on every install |
| `.ailib/manifest.yaml` | no | what is vendored and at which version |
| `CLAUDE.md`, `AGENTS.md` | appended | an "## Ambient folder" anchor so any agent finds `.aai/` |
| `./<launcher>` | no | the capability's command, if it has one |

## Update

Re-run the same command. `.ailib/` refreshes, `.aai/` is left alone.
Add `--check` (via `install.sh`) to report drift without writing.

## Use

```sh
./<launcher> --help
```

Then read `.ailib/<capability>/instructions.md`. To customize behavior, copy it into
`.aai/skills/<capability>/` and edit there; the copy shadows the vendored one.

## For authors

Package with `distro-kit`: `init` scaffolds `distro/` in your repo, `validate` checks it
against this contract, `publish` puts it in the library. See `library/distro-kit/instructions.md`.
