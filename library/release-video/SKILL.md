---
name: release-video
description: Use this skill when the user wants a narrated product or release video of their app — a launch or "what's new" video in their own (ElevenLabs) voice, with screen captures, callout rings pointing at what the narration names, a music bed, and an mp4 out. It does the whole job itself: reads the changelog and git history to find what's new, writes the script and shot list, runs a demo copy of the app, scouts and screenshots the screens, records the voice, then builds and mixes with ffmpeg. Triggers include "make a release video", "make a video for v1.2", "record a launch video for this version", "a video that brags about the release", "redo the video with callouts", "add voice-over to the demo", or reusing the voice style from an earlier video.
---

Read `instructions.md` in this skill's directory and follow it.

Path note: this skill also ships inside the `ambient` library plugin, so its
instructions may reference files as `${CLAUDE_PLUGIN_ROOT}/library/release-video/<file>`.
When installed standalone, resolve those to `<file>` in this directory.
