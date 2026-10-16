# Architecture: `.tinker/architecture.md`

One living file, read by every builder before designing a change, appended by every slice that
changes a module or a seam. Short: one screen when the app is small, never a design document.

## Shape

```markdown
# <app> architecture
## Modules            one line each: name — what it owns — public surface (functions/routes/files)
## Seams              one block per boundary: name, schema (fields + types, or an example payload),
                      who writes, who reads, check: .tinker/seams/<name>.sh
## Data               where durable state lives, its schema, how it migrates
## Decisions          dated one-liners; append, never edit
```

## Rules

- **Deep modules.** Each module owns one concern completely behind a small surface. A slice that
  needs a module's internals is a sign the surface is wrong; widen the surface deliberately (and
  write the decision), do not reach around it.
- **Seams have a schema and a check.** A seam is any place two modules exchange data: an API
  route, a file format, a DB table, a message, a tool call an agent makes. Each one gets a schema
  in this file and a script `.tinker/seams/<name>.sh` that exits 0 when real data matches it. The
  loop runs these on every ticket, so a slice can only break a neighbor by breaking a seam, and
  that is caught before the ticket is marked done.
- **Changing a seam is a slice of its own** (or the first step of one): update the schema here,
  update the check, migrate data, then build on it.
- **Evolves with requirements.** `decompose.md` step 1 reads this file; when a new requirement
  needs a module or seam that is not here, the decomposer adds it before cutting slices. The
  builder appends a dated Decision line whenever a slice changes anything above.
- Created at the skeleton stage from the brief (one or two modules, one seam is typical). Do not
  pre-draw modules for features that are not yet tickets.
