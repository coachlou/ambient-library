---
description: Canonical library admin — create/edit/delete skills, edit the catalog, manage bundles, promote proposals, curate local libraries, rot sweep.
---

You are administering the canonical AAI library. The library and its
management behavior live at `${CLAUDE_PLUGIN_ROOT}`.

Route the user's request ($ARGUMENTS, or ask what they want if empty):

- Create/edit/delete a library skill, edit `catalog.yaml`, promote a staged
  proposal → read and follow `${CLAUDE_PLUGIN_ROOT}/.aai/skills/admin.md`
- Create or maintain a curated **local library** →
  `${CLAUDE_PLUGIN_ROOT}/.aai/skills/curate.md`
- Rot sweep / staleness audit → `${CLAUDE_PLUGIN_ROOT}/.aai/skills/lifecycle.md`
- Save recent session work as a new skill →
  `${CLAUDE_PLUGIN_ROOT}/.aai/skills/propose.md`

Important: admin edits happen in a **source clone** of the library, never in
the installed plugin copy — admin.md explains how to locate or ask for it.
