# aai-library rescue (2026-09-16)

Content that existed only in coachlou/aai-library (the old distribution lineage,
last content commit 2026-07-16) before the first build from ambient-library
replaced it. Nothing here is promoted; review and promote or drop.

- `curate.md` — subskill for creating a curated *local* library (`~/.ailib-local`).
  Overlaps with the vendored `.ailib/` model; probably superseded.
- `commands/` — Claude Code slash commands `/aai-setup` and `/library-admin`
  that wrapped the router. Dev now ships `.claude-plugin/`; check whether
  anything there replaces these before dropping.
- `_staging/` (if present) — proposals staged under the old propose.md flow.
