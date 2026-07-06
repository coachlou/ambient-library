# ambient-library — Context

| Path | What it is | Read when |
|------|------------|-----------|
| `.aai/instructions.md` | canonical router | always, first |
| `.aai/skills/*.md` | subskills (install/select/manage/review/load/admin) | router directs you to one |
| `library/catalog.yaml` | index of every domain skill | choosing a domain skill |
| `library/<skill>/instructions.md` | one domain skill's behavior | after catalog match |
| `ARCHITECTURE.md` | full design rationale | understanding *why*, not routing |
| `docs/MANAGEMENT.md` | maintainer workflows (add/update/delete a skill) | doing library upkeep |
