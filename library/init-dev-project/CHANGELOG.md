# Changelog

## v0.3.1 — 2026-10-01
- Fix: `make build` split ship-list entries on whitespace, so a path like `user guide/` broke the build. It now reads one path per line and skips blank lines.
- Fix: a missing ship-list entry now fails with the build's own message before rsync runs, instead of an rsync link_stat error.
- Self-test covers both, plus scaffolding into a folder that already has `deploy/SHIPLIST` (kept, not overwritten).

## v0.3.0 — 2026-10-01
- Folds in the web-app pilot. Scaffold now writes `deploy/SHIPLIST`; the template Makefile gains `build` (copies exactly the ship list to `build/candidate`, fails on a gap or an extra) and an `accept` stub that fails until defined.
- `make release` bumps VERSION first, then runs acceptance on the candidate, then commits and tags, so the tested artifact is the tagged artifact. A failed acceptance restores VERSION and tags nothing.
- VERSION is on every kind's ship list. Stale "only src/ ships" wording removed from the templates.

## v0.2.0 — 2026-09-30
- Standard v0.2.0 after codex review: graduation is a decision, not a tag; ship list is per kind and verified by `make check`; `make check` is fast and local, acceptance runs on the candidate before the tag; deploy exit needs a version-reporting smoke request and a rollback; `data/` (durable) split from `runtime/` (disposable).

## v0.1.0 — 2026-09-30
- First version: scaffolds a folder into the dev-and-deploy standard, stamps `.aai/`, `git init`, tags `v0.0.0`.
