---
name: tinkerbuild
description: "Personal-app software factory (idea to UI to walking skeleton, then a no-HITL build/check loop, light testing, pre-release QA). Use ONLY when the user says \"tinkerbuild\" or \"tinker build\" explicitly, or the working folder contains a `.tinker/` directory. Do not trigger on generic \"add a feature\", \"fix this\", \"new app\" or \"release\" requests."
---

Read `instructions.md` in this skill's directory and follow it.

When installed as a plugin, this file lives at `${CLAUDE_PLUGIN_ROOT}/library/tinkerbuild/`;
when vendored by ambient-folder it lives at `.ailib/tinkerbuild/` (or `.aai/skills/tinkerbuild/`
if the folder owner has shadowed it).
