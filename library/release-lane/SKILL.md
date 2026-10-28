---
name: release-lane
description: Use this skill to move work through the release loop: commit a validated group of changes, check where a release stands, run an optional full system test, cut a release candidate for testers and staging, log and triage user-testing issues, and promote a stable candidate to production. Triggers on "checkpoint this", "commit this group", "where is this release", "release status", "full system test", "cut an rc", "build a test distro", "send it to testers", "log this bug from testing", "is it stable", "ship it to production", "release it", even when the user doesn't say release-lane.
---

Read `instructions.md` in this skill's directory and follow it.

Path note: this skill also ships inside the `ambient` library plugin, so its
instructions may reference files as `${CLAUDE_PLUGIN_ROOT}/library/release-lane/<file>`.
When installed standalone, resolve those to `<file>` in this directory.
