# tinkerbuild commands

```
tb.py init                     create .tinker/ in the app folder (safe to re-run)
tb.py status                   stage + ticket counts
tb.py ticket add --kind fix|feature|enhancement --title "…" [--body "…"] [--parent T-xxxx] [--touches "mod,mod"]
tb.py ticket list [--status open|building|done|parked]
tb.py ticket set T-0001 --status done
tb.py intake                   inbox/*.json → tickets (+ notify)
tb.py run [--max N]            headless loop: oldest open ticket → agent → check_cmd → retry/park
tb.py qa                       whole-app QA, files fix tickets for failures
tb.py release [--allow-known-issues]
```
Config: `<app>/.tinker/config.json` — `adapter`, `check_cmd`, `max_attempts`, `dial`
(hands-off|steered|pair), `verify`, `notify_cmd`.
