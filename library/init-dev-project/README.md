# init-dev-project

A library skill that scaffolds a folder into the dev-and-deploy standard and
makes it a git repo. The standard is [references/standard.md](references/standard.md).

**Status:** studio · **Kind:** skill · **Lane:** incubator (promote to ambient-library at first tag)

## Run

```bash
python3 scripts/init_dev_project.py ~/GitHub/my-thing --kind web --description "One sentence."
```

Creates `README.md`, `VERSION`, `CHANGELOG.md`, `Makefile`, `.gitignore`, and
`.aai/` (instructions, identity, purpose, context, HANDOFF, checkpoint, and a
version-stamped copy of the standard). Then `git init -b main`, one commit, tag
`v0.0.0`. Never overwrites, never adds a remote.

```bash
make check      # self-test: scaffolds into a temp dir and checks the contract
```

## Deploy

Target: ambient-library. Promote with its admin flow (`~/.ailib/.aai/skills/admin.md`),
then add `init-dev-project` to `RELEASE.yaml`.
