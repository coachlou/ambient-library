# Format: release

What's new in a version, for people who already use the product.

- **Sources:** the CHANGELOG / release notes entry for the version, `git log <previous tag>..<tag>
  --oneline`, and the docs or manual pages those changes touch. Test, cost and timing numbers
  only if the release notes or a smoke report give them.
- **Brief defaults:** audience is current users; goal is "update, and try the new thing";
  length 60-90 s for 8-12 shots (up to about 2 min if the release is big); tone warm and
  confident (`[warmly]`, `[upbeat]`, `[confident]`, `[proudly]`); 16:9, 1920 wide.
- **Beats:** the 5-10 changes a user would notice, each with why it matters and which screen
  shows it, biggest first. Fold internal-only work into one stats line.
- **Shot structure:** title card (product + version + headline), one shot per change, a stats
  card if the numbers earn it, a closing card (how to update, or a sign-off).
- **Mocks:** states the release adds but the demo can't reach (update available, a failed run
  that recovers) go in `mocks`.
- **Worked example:** the SoloFactory 0.11.0 script in voice-style.md.
