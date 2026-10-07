---
name: dev-rules
description: Applies one global set of coding rules — deep modules, one owner per concern, minimal tested changes — to every conversation that writes or reviews code, in any folder, harness, or capability; installs and publishes ~/.aai/rules/coding.md; use for "set up the coding rules", "make the rules global", "publish my coding rules", or before writing code.
---

Read `instructions.md` in this skill's directory and follow it.

Path note: this skill also ships inside the `ambient` library plugin, so its
instructions may reference files as `${CLAUDE_PLUGIN_ROOT}/library/dev-rules/<file>`.
When installed standalone, resolve those to `<file>` in this directory.
