---
name: create-appskill
description: Create and improve skills and "app-skills". A plain skill is instructions plus optional scripts; an app-skill is a self-contained skill folder whose SKILL.md is a conversational orchestrator (the UI) routing each request to bundled scripts, references, sub-skills and subagents. Includes a routing gate (reuse vs skill vs app-skill vs agent), a Skill Brief and App Brief intake, code/inference/delegate step classification, a quality-gate rubric, packaging checks, evals, benchmarking and description optimization, on top of Anthropic's skill-creator (vendored unmodified). Use for "create a skill", "turn this into a skill", "make a skill for X", "create an appskill", "app-skill", "build an app as a skill", "a skill that orchestrates other skills or subagents", "make an app I can talk to", and to improve, audit, eval or benchmark an existing skill.
---

Read `instructions.md` in this skill's directory and follow it.

Path note: this skill also ships inside the `ambient` library plugin, so its instructions may reference files as `${CLAUDE_PLUGIN_ROOT}/library/create-appskill/<file>`. When installed standalone, resolve those to `<file>` in this directory.
