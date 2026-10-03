---
name: team-build
description: Builds a project's skills-manifest.yaml from a brief: turns the brief into needs, shortlists candidates from the team index, picks one skill per need with a reason and runner-up, then writes the manifest plus a rationale record; use for "build the team for this project", "which skills should this project use", "set up the capabilities for this folder", "pick what this folder needs from the library". Not for adding one named skill (manage) or running a skill (load).
---

Read `instructions.md` in this skill's directory and follow it.

Path note: this skill also ships inside the `ambient` library plugin, so its
instructions may reference files as `${CLAUDE_PLUGIN_ROOT}/library/team-build/<file>`.
When installed standalone, resolve those to `<file>` in this directory.
