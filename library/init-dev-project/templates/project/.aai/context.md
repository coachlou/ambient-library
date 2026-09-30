# Context — what's in this folder

| Path | What it is | Read when |
|------|-----------|-----------|
| README.md | what, status, run, deploy | first |
| Makefile | the pipeline: run · check · release · deploy | before any stage |
| VERSION, CHANGELOG.md | the only version; one line per release | at release |
| spec/ | requirements, protocol, ADRs — what it must do | before changing src/ |
| src/ | the thing itself; the only folder that ships | when building |
| tests/unit, tests/smoke | dev tests, every `make check` | when changing src/ |
| tests/acceptance | production tests, only in `make release` | at release |
| deploy/<target>/ | config for the live target, no logic | at deploy |
| docs/ | for the user of the thing; ships with it | when behavior changes |
| tools/ | for the builder; never ships | when a check needs a script |
| .aai/references/dev-standard.md | the standard this folder follows | always |
| .aai/HANDOFF.md, .aai/checkpoint.md | session state | at session start and end |
| build/, runtime/ | regenerable; gitignored | never commit |
