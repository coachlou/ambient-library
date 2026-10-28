# Deploy targets

`make deploy CHANNEL=staging|production` checks the tag, then runs `make ship CHANNEL=...`.
Fill each row before its first deploy, and the `ship` recipe in the Makefile to match.

| channel | ships | target | rollback |
|---|---|---|---|
| staging | rc tags (`vX.Y.Z-rc.N`), for testers | TODO | TODO |
| production | release tags (`vX.Y.Z`) | TODO | TODO |
