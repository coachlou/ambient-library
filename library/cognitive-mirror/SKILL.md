---
name: cognitive-mirror
description: >
  Self-observation system that extracts how the user thinks, decides, and
  evaluates from conversation evidence — the live extractor, not the lifecycle
  manager. 5 modes: /loms (live extraction from the current chat), Mine (batch
  from past chats), Diff (compare against the profile), Query (answer from the
  profile), Harvest (extract decision instances for DSPy). Trigger on: "/loms",
  "look over my shoulder", "cognitive mirror", "mine my conversations", "update
  my cognitive profile", "harvest my decisions", "how do I typically approach
  X", "what's my pattern when". Prefer deep-mirror instead when the request is
  about maintaining, scheduling, auditing, or bulk-mining raw session logs on
  disk. Do NOT trigger for cognitive-operations or irreplaceable-edge requests.
---

Read `instructions.md` in this skill's directory and follow it.

Path note: this skill ships inside the `ambient` library plugin, so its
instructions may reference files as `${CLAUDE_PLUGIN_ROOT}/library/cognitive-mirror/<file>`.
When installed standalone, resolve those to `<file>` in this directory.

Data note: the profile and harvest data this skill reads and writes are NOT in
this skill directory — they live in the global ambient home `~/.aai/` (see
instructions.md § Data location). Only static doctrine (dimensions, template,
scheduled-task prompts) ships here in `references/`.
