---
name: deep-mirror
description: Lifecycle manager for the cognitive-mirror database — orchestrates the one-time deep mine of raw agent session logs (bootstrap), weekly Mine/Harvest maintenance, and the quarterly blind audit that re-mines new logs cold and diffs them against the profile. Use for "bootstrap the mirror", "deep mine my session logs", "weekly mirror", "run mirror maintenance", "audit the mirror", "blind re-mine", "is my profile still accurate", "mirror status", or any request to mine ~/.claude/projects or other agent session archives for behavioral patterns. Requires Claude Code with subagents; raw-log mining is delegated to cheap-model subagents.
---

Read `instructions.md` in this skill's directory and follow it.

Path note: this skill also ships inside the `ambient` library plugin, so its
instructions may reference files as `${CLAUDE_PLUGIN_ROOT}/library/deep-mirror/<file>`.
When installed standalone, resolve those to `<file>` in this directory.
