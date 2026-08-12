# in-progress/ — capabilities being built, not yet in the library

Work lives here while it is being figured out. Nothing here is in
`library/catalog.yaml`, so the router cannot reach it and no folder can install
it. That is the point: a half-built capability should be impossible to invoke
by accident.

## The three stages

| Stage | Where | Reachable by | Ships to production |
|---|---|---|---|
| **1. In progress** | `in-progress/<name>/` | nobody — you open it by hand | no |
| **2. In the library** | `library/<name>/` + a `catalog.yaml` line | the router, in this workspace | no |
| **3. Released** | named in `RELEASE.yaml` | folders that install from production | yes |

Each promotion is a deliberate act. Stage 1 → 2 is `.aai/skills/admin.md`
("create a domain skill"), which writes the four files a skill needs to be both
routable and installable. Stage 2 → 3 is one line in `RELEASE.yaml` plus
`scripts/build-production.sh`.

## Promoting out of here

1. Get it working. Exercise it on real tasks while it sits here.
2. Run it past `.aai/skills/admin.md` — it needs `instructions.md`, `SKILL.md`,
   `.claude-plugin/plugin.json`, a `catalog.yaml` line, and a
   `marketplace.json` entry. Missing any of those is what "not in the library
   yet" actually means.
3. Move the folder to `library/<name>/` and delete it from here.
4. `python3 scripts/audit-distribution.py` — exit 0 or it is not done.
5. Release it separately, later, once you trust it.

## Abandoning something

Delete the folder. Nothing references it, so nothing breaks. Work that has sat
here untouched for months is usually answering a question you no longer have.

## Currently here

**`cognitive-stack-code/`** — moved 2026-08-11 from
`aai-framework/canonical-library/`, where it had been committed to a copy of
the library that nothing installs from, so it was never reachable. 31 files,
10 MB, of which 9.9 MB is `references/data/` — two CSV encyclopedias
(mental models, paradigms). Open questions before it can be promoted: whether a
10 MB capability should be vendored into folders at all, and whether the data
belongs in the skill or behind a lookup script.

## Note on `library/_staging/`

There is a second pre-library area: `library/_staging/`, which
`.aai/skills/propose.md` writes into when it drafts a skill from a session
trace. Same stage, different origin — that one is machine-drafted, this one is
hand-built. If keeping both proves confusing, merge them; `_staging` is
referenced by `propose.md` and `scripts/validate-self-extension.sh`.
