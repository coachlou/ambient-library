# publish-article — in progress

Standalone skill: take a finished Markdown article and get it live on
aimmhub.coachlou.com. Writing skills (article-studio, the writing teams,
evaluate-article) end at "here's a draft"; this is the missing last step.

Drafted (2026-09-29): `instructions.md`, `SKILL.md`, `.claude-plugin/plugin.json`,
`evals/trigger-evals.json`. Not yet promoted or in the catalog. Standalone trigger
evals scored 0/8 should-trigger: in Lou's environment, routing goes through
`~/.aai/references/publishing.md` first, and that file still sends hub publishing to
the old here.now `publish-hub.sh`. Fix that routing, re-run the evals, then run
`bash scripts/promote.sh publish-article`.

## Proven by hand (2026-09-29, "Transfer Your Intelligence, Not Your Content")

1. Copy the `.md` to `okf-kb/inbox/general/`; hash it, check the ledger.
2. Ingest (okf-management): source under `aimm-okf/sources/article-<date>-<slug>/`
   **and** a published concept `aimm-okf/knowledge/articles/<slug>.md`
   (`type: article`, `status: published`, `source-type: original`, `source_ids`).
   The general workflow alone is source-only, so the hub never sees it.
3. Index, `validate_bundle.py`, prepend `log.md`, ledger row, run record;
   commit specific files in okf-kb (do not push without asking).
4. In `AIMM-AstroSite/aimm-hub`: `npm run deploy` (cache clear, sync from OKF,
   build, `wrangler deploy`). This is what goes live; `git push` does not.
5. Verify on `https://aimm-hub-astro.accounts-0c6.workers.dev/articles/<slug>/`
   (the custom domain is behind Cloudflare Access).
6. Commit `content/articles/<slug>.md` (synced copy, never hand-edited) and push.

## Design decisions

- Thin orchestrator: ingest -> deploy -> verify. KB logic stays in okf-kb; the
  ingest half belongs in a new `okf-kb/inbox/articles/SKILL.md` (the `general`
  inbox hit its 3-article promotion threshold) that always creates the concept.
- Contract: input = md path (+ optional title/date/tags); output = live URL +
  commit hashes.
- Repo paths come from `~/.aai/context.md`, not hard-coded.
- Deterministic steps (hash, stage, index, validate, deploy, verify) as a
  script with `--dry-run` and JSON output; inference only for
  description/tags/aliases and the sensitive-content check.
- Default stops after KB ingest; deploy + push need explicit `publish: true`.
  Never push okf-kb unasked. Stage specific files (both repos are dirty).
- Destinations: aimm-hub only for now; Notion/newsletter as later stages.

## Gotchas

- YAML-quote `description` (an unquoted one failed frontmatter parsing).
- `content/articles/` is rsync `--delete`d from the bundle; edit the bundle.
- Both repos are outside a session's cwd: request directory access first.
- Description must stay distinct from `ed`, `evaluate-article`, writing teams.
- Evals before shipping (should-trigger: "get this online"; near-miss: "edit/write this").
