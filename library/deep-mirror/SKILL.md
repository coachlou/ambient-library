---
name: deep-mirror
description: Use this skill whenever the user wants to run, schedule, check, or audit their cognitive-mirror / behavioral-profile system — it is the lifecycle operator, not the live extractor. Trigger it for any "mirror" operation (weekly mirror, mirror maintenance, mirror status, audit the mirror, bootstrap the mirror, blind re-mine); any mining of stored agent session logs on disk (~/.claude/projects, codex sessions, months of Claude Code history) for patterns in how the user works; and any status or "what's due" check on the cognitive database or profile freshness ("is my profile still accurate", "haven't run maintenance since June"). Covers three jobs: one-time bootstrap deep-mine, recurring weekly Mine/Harvest maintenance, and quarterly blind audits that re-mine cold and diff against the profile. Prefer this over cognitive-mirror when the request is about maintaining, scheduling, auditing, or bulk-mining logs rather than extracting from the current conversation. Requires Claude Code with subagents.
---

Read `instructions.md` in this skill's directory and follow it.

Path note: this skill also ships inside the `ambient` library plugin, so its
instructions may reference files as `${CLAUDE_PLUGIN_ROOT}/library/deep-mirror/<file>`.
When installed standalone, resolve those to `<file>` in this directory.
