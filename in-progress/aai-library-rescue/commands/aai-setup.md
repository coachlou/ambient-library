---
description: Wire AAI into a project or globally — stamp .aai/, set up routing pointers, vendor capabilities into .ailib/, write the skills manifest.
---

You are setting up Agentic Ambient Intelligence for the user. The library and
its behavior live at `${CLAUDE_PLUGIN_ROOT}`.

Target ($ARGUMENTS, or ask): a **project folder** or **global** (`~/.aai`).

- Make a folder ambient (stamp `.aai/`, vendor skills into `.ailib/`,
  personalize, re-sync) → read and follow
  `${CLAUDE_PLUGIN_ROOT}/.aai/skills/lifecycle.md`
- Set up ambient-library routing in a project (pointer in
  `CLAUDE.md`/`AGENTS.md`, optional `skills-manifest.yaml`) →
  `${CLAUDE_PLUGIN_ROOT}/.aai/skills/install.md`
- Choose which library skills the project uses →
  `${CLAUDE_PLUGIN_ROOT}/.aai/skills/select.md`

For **global** setup, apply the same stamp to `~/.aai` (identity: the user's
machine-wide ambient home) and add the pointer block from
`${CLAUDE_PLUGIN_ROOT}/templates/AGENTS-pointer.md` to the user's global
instruction file (`~/.claude/CLAUDE.md` or `~/AGENTS.md`), pinning the
library path.
