---
name: gears-broadcast
description: Sends any email to GEARS licensees (gears_owners) via Resend — accepts a subject/body if already given, otherwise drafts them with the user first; use for "send a gears broadcast", "email the licensees", "notify gears owners", "send this to gears_owners". Skips Resend's dashboard-editor round trip and sends straight from raw HTML/text.
---

Read `instructions.md` in this skill's directory and follow it.

Path note: this skill also ships inside the `ambient` library plugin, so its
instructions may reference files as `${CLAUDE_PLUGIN_ROOT}/library/gears-broadcast/<file>`.
When installed standalone, resolve those to `<file>` in this directory.
