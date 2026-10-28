# {{name}}

{{description}}

**Status:** studio · **Kind:** {{kind}} · **Lane:** incubator

## Run

```bash
make            # prints the numbered pipeline map
make run
```

## Deploy

Two channels: `staging` (release candidates, for testers) and `production` (releases).
Targets and rollback: `deploy/README.md`. Per-target config goes in `deploy/<target>/`.

Governed by `.aai/references/dev-standard.md`.
