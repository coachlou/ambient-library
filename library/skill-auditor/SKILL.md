---
name: skill-auditor
description: Audits a library skill directory against the publishing schema — SKILL.md frontmatter (name, description, metadata.summary, metadata.status), catalog.yaml projection sync, resolvable references (relative paths and ${CLAUDE_PLUGIN_ROOT}/library/... forms), and evals presence/shape — and reports ordered, deduplicated, actionable findings with copy-editable fixes. Read-only; never edits the target. Use for "audit this skill", "does X follow the schema", "lint X against the catalog", "check X before I publish it", "validate X's SKILL.md", or batch-auditing a directory.
metadata:
  summary: Audits a skill's SKILL.md frontmatter, catalog.yaml projection, references, and evals shape against the library schema, reporting ordered actionable findings; use for "audit this skill", "does X follow the schema", "lint X against the catalog", "check X before I publish it".
  status: experimental
---

Read `instructions.md` in this skill's directory and follow it.

Path note: this skill also ships inside the `ambient` library plugin, so its
instructions may reference files as `${CLAUDE_PLUGIN_ROOT}/library/skill-auditor/<file>`.
When installed standalone, resolve those to `<file>` in this directory.
