# Promotion candidates

Things found outside the library during the 2026-09-16 compliance cleanup that
may deserve a place in it. Nothing here is routable. Promote via `admin.md`
("create a domain skill") after review, or delete the line.

Provenance rule used while reconciling: a skill with `library/<name>/app/VERSION`
is synced FROM an app repo by `scripts/sync-distro.sh` (solofactory,
software-dev-factory, wbs-toolkit today) — the app repo is its source of truth
and its app-side copy is never touched. Everything else is authored here.

| Candidate | Where it is now | Why it might belong |
|---|---|---|
| capability-architect | archive/2026-09-16-library-cleanup/ailibrary-cleanslate-2026-06/skills/ | June 2026 CleanSlate skill; designs skills — overlaps admin.md, check before promoting |
| inference-router | same | model/effort routing as a reusable skill |
| letsgo | same | unknown — read before deciding |
| wbs-prd | same | may be superseded by wbs-toolkit (synced) |
| writing-team-orchestrator | same | may be superseded by writing-team |
| curate | in-progress/aai-library-rescue/curate.md | old distro's "create a local canonical library" — partly what ~/.ailib now is |
| aai-setup / library-admin commands | in-progress/aai-library-rescue/commands/ | old distro slash commands |
| test-validation-skill | in-progress/aai-library-rescue/_staging/ | old staged proposal |
| nugget-mining | all-ai-chats-archives/nugget-mining/.aai/skills/nugget-mining/ | owned pilot skill with evals and scripts; portable across topics per its own README |
| okf-management (two forks) | ~/Documents/OKF/.aai/skills/ vs aimm-shared-repo/AAI-Folders/okf/.aai/skills/ | diverged both ways (Documents: newer references; aimm-shared: eval_retrieval.py, fixtures, newer instructions). Diff saved in the 2026-09-16 dogfood scratch log. Reconcile by diff before promoting |

## Follow-ups outside this repo

- solofactory and software-dev-factory `distro/templates/aai/` should emit GEMINI.md and
  the lookup-order paragraph (edit in the app repos, then `scripts/sync-distro.sh`).
- software-dev-factory `scripts/build-distro.mjs` bundles (`distro/dev`, `distro/v0.x`) vendor
  `.ailib/factory/` without a manifest.yaml; the SDF project generator writes an app-test
  launcher that hardcodes a deleted absolute path (see dev-factory/projects/app-test-1).
- dynamic-company-builder uses `.ailib/manifest.json`, not `manifest.yaml`, and exists twice
  (`dynamic-company-builder`, `-agent-organization`, same HEAD c8c02a2, no remote) — pick one.
- Worktrees on other branches (`~/.grok/worktrees/github-software-dev-factory/*`,
  `all-ai-chats-archives/.worktrees/editorial-studio`) inherit compliance when their
  branches rebase onto main; not edited directly.
- `deepseek-harness-master/wip` uses `.aai/conversation/` as a design experiment, not as an
  ambient folder; its docs reference the path, so it was left as is.
