# How to check: `check_cmd` by app type

`check_cmd` is a single command that exits 0 only if the app really starts and the core path works.
It is the gate for every ticket. Never let the builder's own opinion stand in for it.

| App | check_cmd should |
|---|---|
| Web | start the dev server in the background, hit the main route + one API call (curl or a headless browser script), kill the server |
| CLI | run the command on a fixture input, diff the output |
| macOS/iOS | build, launch (simulator for iOS), take a screenshot, assert it launched without a crash log |
| Agent-driven (an LLM talks to a UI agent that drives skills/tools) | replay a short scripted conversation through the real agent, assert the tool calls / outputs, not the exact wording |

Keep it under about a minute. If it is flaky, fix the check; do not retry until green.

For agent-driven apps, the replay script is the single most valuable test: record one good session
as a transcript, then assert on the *actions* (files written, tools invoked, state changed).

Optional second opinion: set `"verify": true` in config. After `check_cmd` passes, a fresh agent
(role `checker`, no memory of the build) is asked to confirm the ticket's acceptance and must end
its reply with PASS or FAIL.
