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

    bash scripts/promote.sh <name>          # --dry-run to see the plan first

It checks the four-file contract before moving anything, moves the folder to
`library/<name>/`, and prints what is left: catalog line, marketplace entry,
`audit-distribution.py`, commit, push, and — separately — release.

**Reworking something already live is the normal case.** Develop the new
version here while the old one stays in `library/` serving production. On
promote, the script shows the version delta and a file diff, warns if you did
not bump the version, and tells you production is stale if the skill is
released. Production keeps serving the old version until you rebuild, which is
deliberate: promoting to the canonical library and shipping to folders are
different decisions on different days.

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

## Where proposals go

`.aai/skills/propose.md` drafts skills here too, when you say "save this as a
skill" after a session. Hand-built or machine-drafted, same folder, same
promotion path — there is no separate staging area. (`library/_staging/` was
merged into this folder on 2026-08-11.)
