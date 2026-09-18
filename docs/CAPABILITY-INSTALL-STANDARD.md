# Capability install standard

Every capability in this library installs the same way. Learn it once.

## Install

```sh
curl -fsSL https://raw.githubusercontent.com/coachlou/ambient-library/main/library/ambient-folder/bootstrap.sh \
  | bash -s -- <capability> [target-folder]
```

Target defaults to the current folder.

The script is public; the library it installs is a private repo, so this needs
GitHub read access to `coachlou/aai-library` — either the `gh` CLI signed in
(`gh auth login`) or `GITHUB_TOKEN` / `GH_TOKEN` set. Ask for an invite if you
have neither. Don't put a token in the command itself: it lands in your shell
history and in the process list.

The installer writes:

| Path | Yours? | What |
|---|---|---|
| `.aai/` | yes, never overwritten | identity, instructions, context for this folder |
| `.ailib/<capability>/` | no, vendored | the capability itself, re-synced on every install |
| `.ailib/manifest.yaml` | no | what is vendored and at which version |
| `CLAUDE.md`, `AGENTS.md` | appended | an "## Ambient folder" anchor so any agent finds `.aai/` |
| `./<launcher>` | no | the capability's command, if it has one |

## Update

Re-run the same command. `.ailib/` refreshes, `.aai/` is left alone.
Add `--check` (`bash .ailib/ambient-folder/install.sh <capability> --check [target]`)
to report drift without writing.

## Use

```sh
./<launcher> --help
```

Then read `.ailib/<capability>/instructions.md`. Customize in
`.aai/skills/<capability>/`, which shadows the vendored copy and survives every
update: saved values first (where the capability ships a `contract.yaml`), then
an `overrides.md` of extra rules, and only as a last resort a forked
`instructions.md` — a fork stops receiving updates.

## For authors

Package with `distro-kit`: `init` scaffolds `distro/` in your repo, `validate` checks it
against this contract, `publish` puts it in the library. See `library/distro-kit/instructions.md`.
