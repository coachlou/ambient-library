---
name: teaching-block-synthesized
description: >
  Writes ONE publishable teaching-block article from a working session: a first-person process
  walkthrough showing the real prompts, the real outputs, the wrong turns and the reasoning behind
  each move, so a reader can follow it and do it themselves. Produces the article, its diagrams, and
  a self-contained rendered HTML. Works for any domain — code, writing, planning, research, agent
  work. Use for "write this up as a teaching block", "turn this session into an article", "field
  guide this", "debrief this session", "post-mortem this", "write up what we just did", "capture this
  for AIMM". Invoke proactively when a session reaches a clear conclusion and the user seems to be
  wrapping up. Prefer extract-codify-patterns instead when the user wants the full
  look-over-my-shoulder BUNDLE (README with reading paths, brief, chat export, vault artifacts)
  rather than a single deeply-crafted article.
metadata:
  summary: Writes one publishable teaching-block article from a working session — real prompts, real outputs, wrong turns, reasoning, diagrams, and rendered HTML; use for "write this up as a teaching block", "field guide this", "debrief this session", "turn this session into an article". Any domain. For the full look-over-my-shoulder bundle (README, brief, chat export, vault artifacts) use extract-codify-patterns instead.
  status: experimental
---

Read `instructions.md` in this skill's directory and follow it.

Path note: this skill also ships inside the `ambient` library plugin, so its
instructions may reference files as `${CLAUDE_PLUGIN_ROOT}/library/teaching-block-synthesized/<file>`.
When installed standalone, resolve those to `<file>` in this directory — that
applies to `references/devices.md`, `references/writing-style.md`, and `evals/evals.json`.
