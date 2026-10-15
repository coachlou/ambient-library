---
name: checkpoint
description: Preserve conversation context across compaction and hand off work across sessions, agents, and CLI windows. Three modes. COMPACT (default — "/checkpoint", "/checkpoint:compact", "checkpoint before compact", "save context before clearing", or when the context window is getting long) distills state since the last checkpoint into the project's `.aai/checkpoint.md`, then tells the user to run /compact. HANDOFF ("/checkpoint:handoff", "hand this off", "write a handoff", "handoff for the next session") verifies live state and writes a durable note for a cold-start successor — into the harness's project memory if it has one, else `.aai/handoff.md`. SESSION ("/checkpoint:session", "session check-in", "what should I work on", "resume work", "wrap up", "session check-out") runs the multi-agent .context/ store protocol for projects with a `.context/` directory.
---

Read `instructions.md` in this skill's directory and follow it.

Path note: this skill also ships inside the `ambient` library plugin, so its
instructions may reference files as `${CLAUDE_PLUGIN_ROOT}/library/checkpoint/<file>`.
When installed standalone, resolve those to `<file>` in this directory.
