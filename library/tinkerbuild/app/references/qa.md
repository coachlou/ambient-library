# Pre-release QA pass

Runs before a release, over the whole app, not just the last change. `tb.py qa` does it.

1. Every `.tinker/qa/*.sh` (one per feature, left by the loop) plus `check_cmd` as the smoke test.
2. Results to `.tinker/qa-report.md`. Each failure becomes ONE fix ticket (`QA failing: <name>`).
3. `tb.py release`: QA green → tags the next `vN`, logs it. If the app has a `Makefile` with an `rc:` target
   (dev-and-deploy standard), it runs `make release BUMP=patch|minor|major` (`--bump`) instead and never tags or
   edits VERSION itself; cut a candidate first with `make rc` when testers are involved. Red → files tickets, refuses.
   Run `tb.py run` to clear them and release again. `--allow-known-issues` ships anyway; that is
   the user's call, never the default.

Beyond the scripts, when the app has a UI, also do once per release (agent step, not a script):
walk every screen/route and screenshot it, relaunch and confirm data persisted, try empty and very
long input once. Aim at crashes and data loss only. No load, security, or accessibility audits; this
is a personal app.

Tidy (code cleanup) is separate and optional. Run it after QA is green, then re-run QA.
