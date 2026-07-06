# ambient-library — Context

| Path | What it is | Read when |
|------|------------|-----------|
| `.aai/instructions.md` | canonical router | always, first |
| `.aai/skills/*.md` | subskills (install/select/manage/review/load/admin/lifecycle) | router directs you to one |
| `.aai/skills/lifecycle.md` | stamp/install/personalize/learn/update a `.aai`/`.ailib` folder | making another folder ambient |
| `library/catalog.yaml` | index of every domain skill | choosing a domain skill |
| `library/<skill>/instructions.md` | one domain skill's behavior | after catalog match |
| `templates/aai/README.md` | the `.aai`/`.ailib` scaffold spec | a lifecycle detail is ambiguous |
| `ARCHITECTURE.md` | full design rationale | understanding *why*, not routing |
| `docs/MANAGEMENT.md` | maintainer workflows (add/update/delete a skill) | doing library upkeep |
