# In-app report button / error capture

Both write one JSON file into `<app>/.tinker/inbox/`. `tb.py intake` (also the first step of
`tb.py run`) turns each into a ticket and notifies you. No server, no API.

File: `.tinker/inbox/<timestamp>.json`
```json
{"kind": "fix", "title": "one line", "detail": "what happened, steps, error text, stack", "source": "report-button"}
```
Use `"source": "app-error"` when the app caught the error itself, `"report-button"` when you pressed the button.

## Web app (Node/Express-style backend)
```js
import { writeFileSync } from "node:fs";
export function report(title, detail, source = "report-button") {
  writeFileSync(`.tinker/inbox/${Date.now()}.json`,
    JSON.stringify({ kind: "fix", title, detail, source }));
}
process.on("uncaughtException", e => report(String(e.message), e.stack, "app-error"));
// button: POST /__report {title, detail} -> report(title, detail)
```

## Python app
```python
import json, time, traceback, sys
def report(title, detail="", source="report-button"):
    open(f".tinker/inbox/{int(time.time()*1000)}.json", "w").write(
        json.dumps({"kind": "fix", "title": title, "detail": detail, "source": source}))
sys.excepthook = lambda t, v, tb: report(str(v), "".join(traceback.format_exception(t, v, tb)), "app-error")
```

## Native or agent-driven app
Same file from whatever language it is written in. For an app whose UI is an agent, also drop the
last conversation turn into `detail`; it is usually the whole bug report.

Button copy: "Report a problem" with one optional text field. The captured error and recent log
lines are attached automatically.
