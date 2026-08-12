# ambient-library — Context

| Path | What it is | Read when |
|------|------------|-----------|
| `.aai/instructions.md` | canonical router | always, first |
| `.aai/skills/*.md` | subskills (install/select/manage/review/load/admin/propose/lifecycle) | router directs you to one |
| `.aai/PRODUCTION` | marker: this is a production BUILD, not the source | present → do not author here; it names the dev workspace |
| `AGENTS.md` | discovery anchor for a cold agent; `CLAUDE.md` redirects to it | you arrived without being told this folder is ambient |
| `.aai/skills/lifecycle.md` | delegates folder ops to `ambient-folder`; owns the library rot sweep | making another folder ambient, or "what's stale" |
| `library/ambient-folder/instructions.md` | incept/stamp/install/personalize/learn/update a `.aai`/`.ailib` folder | any folder-scaffold operation |
| `library/catalog.yaml` | index of every domain skill | choosing a domain skill |
| `library/<skill>/instructions.md` | one domain skill's behavior | after catalog match |
| `templates/aai/README.md` | the `.aai`/`.ailib` scaffold spec | a lifecycle detail is ambiguous |
| `ARCHITECTURE.md` | full design rationale | understanding *why*, not routing |
| `in-progress/` | capabilities being built — not catalogued, not routable, not shipped | user is building something new, or asks what's in flight |
| `RELEASE.yaml` | what ships to production — explicit list, nothing else ships | releasing or unreleasing a skill |
| `scripts/build-production.sh` | builds the production library from `RELEASE.yaml` | after a release decision |
| `docs/MANAGEMENT.md` | maintainer workflows (add/update/delete a skill) | doing library upkeep |
