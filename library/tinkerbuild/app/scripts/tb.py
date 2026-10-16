#!/usr/bin/env python3
"""tinkerbuild core: tickets, the build->check loop, QA, release. Stdlib only, no harness names.

State lives in <app>/.tinker/. The agent step goes through an adapter JSON
({"cmd": [...]}, prompt on stdin), so any harness can drive it.
Run from the app folder, or pass --app DIR.
"""

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
INFERENCE = {
    # subscriptions first, in this order; chain[0] defaults to the harness tb.py runs in
    "chain": ["claude", "codex"],
    # "" = the harness's own default; adapter JSON says how each is spelled
    "roles": {
        "builder": {"model": "", "effort": ""},
        "checker": {"model": "", "effort": ""},
    },
    # last resort: same adapter, metered by API key. Only the env var NAME is stored.
    "api": {"approved": False, "key_env": "ANTHROPIC_API_KEY"},
    "cooldown_s": 3600,  # how long to stay on a fallback before retrying chain[0]
}
DEFAULTS = {
    "check_cmd": "make check",
    "max_attempts": 3,
    "dial": "hands-off",
    "notify_cmd": "",
    "verify": False,
    "inference": INFERENCE,
}
KINDS = ("feature", "fix", "enhancement")


class App:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.t = self.root / ".tinker"

    def cfg(self):
        p = self.t / "config.json"
        return {**DEFAULTS, **(json.loads(p.read_text()) if p.exists() else {})}

    def tickets(self):
        return [
            json.loads(p.read_text())
            for p in sorted((self.t / "tickets").glob("T-*.json"))
        ]

    def save(self, tk):
        (self.t / "tickets" / f"{tk['id']}.json").write_text(
            json.dumps(tk, indent=2) + "\n"
        )

    def get(self, tid):
        p = self.t / "tickets" / f"{tid}.json"
        if not p.exists():
            die(f"no such ticket: {tid}", 2)
        return json.loads(p.read_text())

    def state(self):
        p = self.t / "state.json"
        return json.loads(p.read_text()) if p.exists() else {"stage": "idea"}

    def set_state(self, **kv):
        (self.t / "state.json").write_text(json.dumps({**self.state(), **kv}) + "\n")

    def log(self, fname, line):
        with open(self.t / fname, "a") as f:
            f.write(line.rstrip() + "\n")

    def notify(self, msg):
        print(f"[tinker] {msg}", file=sys.stderr)
        cmd = self.cfg()["notify_cmd"]
        if cmd:
            subprocess.run(
                cmd, shell=True, cwd=self.root, env={**os.environ, "TB_MSG": msg}
            )

    def sh(self, cmd, timeout=900):
        r = subprocess.run(
            cmd,
            shell=True,
            cwd=self.root,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return r.returncode, (r.stdout + r.stderr)


def die(msg, code=1):
    print(f"tb: {msg}", file=sys.stderr)
    sys.exit(code)


def add_ticket(app, kind, title, body="", source="user", parent="", touches=""):
    if kind not in KINDS:
        die(f"kind must be one of {KINDS}", 2)
    n = len(list((app.t / "tickets").glob("T-*.json"))) + 1
    tk = {
        "id": f"T-{n:04d}",
        "kind": kind,
        "title": title,
        "body": body,
        "source": source,
        "status": "open",
        "attempts": 0,
        "accept": "",
        "parent": parent,  # a slice of a bigger ticket (status "split")
        "touches": touches,  # modules from .tinker/architecture.md this slice changes
        "created": time.strftime("%F %T"),
    }
    app.save(tk)
    app.notify(f"{tk['id']} captured ({kind}, {source}): {title}")
    return tk


def cmd_init(app, a):
    for d in ("tickets", "inbox", "qa", "seams"):
        (app.t / d).mkdir(parents=True, exist_ok=True)
    cfg = json.loads(json.dumps(DEFAULTS))
    h = host_harness()
    if h in cfg["inference"]["chain"]:  # the harness we run in goes first
        cfg["inference"]["chain"].remove(h)
        cfg["inference"]["chain"].insert(0, h)
    for f, content in (
        ("config.json", json.dumps(cfg, indent=2) + "\n"),
        ("state.json", json.dumps({"stage": "idea"}) + "\n"),
        ("changelog.md", "# Changelog\n"),
        ("parked.md", "# Parked\n"),
    ):
        if not (app.t / f).exists():
            (app.t / f).write_text(content)
    print(f"tinker workspace ready: {app.t}")


def cmd_status(app, a):
    st = app.state()
    counts = {}
    for tk in app.tickets():
        counts[tk["status"]] = counts.get(tk["status"], 0) + 1
    print(f"stage: {st['stage']}\ntickets: {counts or 'none'}")
    fb = st.get("inference", {})
    if fb.get("active"):
        print(
            f"inference: on fallback {fb['active']} since {time.strftime('%F %T', time.localtime(fb['since']))}"
        )


def cmd_stage(app, a):
    app.set_state(stage=a.name)


def cmd_ticket(app, a):
    if a.op == "add":
        print(
            add_ticket(app, a.kind, a.title, a.body, a.source, a.parent, a.touches)[
                "id"
            ]
        )
    elif a.op == "list":
        for tk in app.tickets():
            if not a.status or tk["status"] == a.status:
                sub = f"  ↳ {tk['parent']}" if tk.get("parent") else ""
                print(
                    f"{tk['id']}  {tk['status']:8} {tk['kind']:11} {tk['title']}{sub}"
                )
    elif a.op == "set":
        tk = app.get(a.id)
        tk["status"] = a.status
        app.save(tk)


def cmd_intake(app, a):
    for p in sorted((app.t / "inbox").glob("*.json")):
        d = json.loads(p.read_text())
        add_ticket(
            app,
            d.get("kind", "fix"),
            d.get("title", "untitled"),
            d.get("detail", d.get("body", "")),
            d.get("source", "app"),
        )
        p.unlink()


def adapter(app, name):
    for d in (app.t / "adapters", SKILL / "adapters"):
        p = d / f"{name}.json"
        if p.exists():
            spec = json.loads(p.read_text())
            if not spec.get("verified", True):
                die(
                    f"adapter {name} is an unverified stub; edit adapters/{name}.json first",
                    2,
                )
            return spec
    die(f"unknown adapter: {name}", 2)


def inference(app):
    cfg = app.cfg()
    inf = {**INFERENCE, **cfg.get("inference", {})}
    inf["roles"] = {**INFERENCE["roles"], **inf.get("roles", {})}
    inf["api"] = {**INFERENCE["api"], **inf.get("api", {})}
    if "adapter" in cfg:  # pre-inference config: one adapter, no fallback
        inf["chain"] = [cfg["adapter"]]
    return inf


def host_harness():
    """The harness tb.py is running inside, if any; becomes chain[0] at init."""
    if os.environ.get("CLAUDECODE"):
        return "claude"
    if any(k.startswith("CODEX") for k in os.environ):
        return "codex"
    return ""


def agent(app, role, prompt):
    """Run one agent step, walking the subscription chain, then the API if approved.

    An adapter whose output matches its skip_patterns (usage limit, not logged in) is
    skipped and remembered in state.json for cooldown_s so the next step starts there.
    Any other crash or timeout is a failed attempt, not an error.
    """
    inf, st = inference(app), app.state()
    fb = st.get("inference", {})
    chain = list(inf["chain"])
    if (
        fb.get("active") in chain
        and time.time() - fb.get("since", 0) < inf["cooldown_s"]
    ):
        chain = chain[chain.index(fb["active"]) :]
    key = inf["api"]["key_env"]
    tries = [(n, False) for n in chain]
    if inf["api"]["approved"] and os.environ.get(key):
        tries.append((chain[0], True))
    out = "no adapter in chain"
    for name, use_api in tries:
        spec = adapter(app, name)
        env = {k: v for k, v in os.environ.items() if use_api or k != key}
        cmd = list(spec["cmd"])
        for opt in ("model", "effort"):
            val = inf["roles"].get(role, {}).get(opt)
            if val and spec.get(f"{opt}_flag"):
                cmd += [s.replace(f"{{{opt}}}", val) for s in spec[f"{opt}_flag"]]
        try:
            r = subprocess.run(
                cmd,
                input=prompt,
                cwd=app.root,
                capture_output=True,
                text=True,
                timeout=1800,
                env={**env, "TB_ROLE": role},
            )
            rc, out = r.returncode, r.stdout + r.stderr
        except (OSError, subprocess.TimeoutExpired) as e:
            rc, out = 1, f"agent failed to run: {e}"
        low = out.lower()
        if rc == 0 or not any(p.lower() in low for p in spec.get("skip_patterns", [])):
            return rc, out
        nxt = tries[tries.index((name, use_api)) + 1 :]
        where = f"{nxt[0][0]}{' (API)' if nxt[0][1] else ''}" if nxt else "nothing left"
        app.notify(
            f"{name}{' (API)' if use_api else ''} unavailable; falling back to {where}"
        )
        if nxt and not nxt[0][1]:
            app.set_state(inference={"active": nxt[0][0], "since": time.time()})
    return 1, out


def prompt_for(app, tk, failure):
    loop = (SKILL / "references" / "loop.md").read_text()
    p = f"{loop}\n\n## Ticket\n```json\n{json.dumps(tk, indent=2)}\n```\n"
    if failure:
        p += f"\n## Last check failed. Fix this, do not start over:\n```\n{failure[-3000:]}\n```\n"
    return p


def verify(app, tk):
    rc, out = agent(
        app,
        "checker",
        f"Fresh eyes. Run the app and confirm this ticket's acceptance holds. "
        f"Last line of your reply must be PASS or FAIL.\n\n{json.dumps(tk, indent=2)}",
    )
    return out.strip().splitlines()[-1:] == ["PASS"], out


def check(app):
    """Per-ticket gate: the app's check_cmd plus every seam contract. Stops at the first failure."""
    cmds = [app.cfg()["check_cmd"]] + [
        f"sh {p}" for p in sorted((app.t / "seams").glob("*.sh"))
    ]
    for c in cmds:
        rc, out = app.sh(c)
        if rc:
            return rc, f"$ {c}\n{out}"
    return 0, ""


def work(app, tk):
    cfg = app.cfg()
    failure = ""
    tk["status"] = "building"
    while tk["attempts"] < cfg["max_attempts"]:
        tk["attempts"] += 1
        app.save(tk)
        if cfg["dial"] == "pair" and sys.stdin.isatty():
            input(f"{tk['id']} attempt {tk['attempts']}: Enter to run agent ")
        agent(app, "builder", prompt_for(app, tk, failure))
        # the builder may have written accept/touches into the ticket file; keep them
        tk = {**app.get(tk["id"]), "status": tk["status"], "attempts": tk["attempts"]}
        rc, out = check(app)
        if rc == 0 and cfg["verify"]:
            ok, out = verify(app, tk)
            rc = 0 if ok else 1
        if rc == 0:
            tk["status"] = "done"
            app.save(tk)
            app.log(
                "changelog.md",
                f"- {time.strftime('%F')} {tk['id']} {tk['kind']}: {tk['title']}",
            )
            if (app.root / ".git").exists():
                app.sh(
                    f"git add -A && git commit -q -m 'tinker: {tk['id']} {tk['title']}'"
                )
            return True
        failure = out
    tk["status"] = "parked"
    app.save(tk)
    app.log(
        "parked.md",
        f"- {tk['id']} {tk['title']}: failed {tk['attempts']} attempts. Last output:\n```\n{failure[-1500:]}\n```",
    )
    app.notify(f"{tk['id']} parked after {tk['attempts']} attempts: {tk['title']}")
    return False


def cmd_run(app, a):
    cmd_intake(app, a)
    done = 0
    while done < a.max:
        todo = [t for t in app.tickets() if t["status"] == "open"]
        if not todo:
            break
        if app.cfg()["dial"] == "steered" and sys.stdin.isatty():
            input(f"next: {todo[0]['id']} {todo[0]['title']} (Enter to build) ")
        work(app, todo[0])
        done += 1
    print(f"processed {done} ticket(s)")


def cmd_qa(app, a):
    results = {p.stem: app.sh(f"sh {p}") for p in sorted((app.t / "qa").glob("*.sh"))}
    results["check+seams"] = check(app)
    lines = ["# QA report", time.strftime("%F %T"), ""]
    failed = [n for n, (rc, _) in results.items() if rc]
    for n, (rc, out) in results.items():
        lines.append(
            f"- {'PASS' if rc == 0 else 'FAIL'} {n}"
            + ("" if rc == 0 else f"\n```\n{out[-800:]}\n```")
        )
    (app.t / "qa-report.md").write_text("\n".join(lines) + "\n")
    known = {t["title"] for t in app.tickets()}
    for n in failed:
        if f"QA failing: {n}" not in known:
            add_ticket(app, "fix", f"QA failing: {n}", results[n][1][-800:], "qa")
    print(
        f"qa: {len(results) - len(failed)} passed, {len(failed)} failed (see .tinker/qa-report.md)"
    )
    return 1 if failed else 0


def cmd_release(app, a):
    if cmd_qa(app, a) and not a.allow_known_issues:
        die(
            "QA failed; fix tickets filed. Run `tb.py run`, then release again (or --allow-known-issues)."
        )
    if not (app.root / ".git").exists():
        die("not a git repo; nothing to tag", 2)
    rc, out = app.sh("git tag -l 'v[0-9]*'")
    tag = f"v{len(out.split()) + 1}"
    app.sh(f"git add -A && git commit -q -m 'release {tag}'; git tag {tag}")
    app.log("changelog.md", f"- {time.strftime('%F')} released {tag}")
    app.notify(f"released {tag}")


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--app", default=".")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init").set_defaults(fn=cmd_init)
    sub.add_parser("status").set_defaults(fn=cmd_status)
    sub.add_parser("intake").set_defaults(fn=cmd_intake)
    sub.add_parser("qa").set_defaults(fn=cmd_qa)
    s = sub.add_parser("stage")
    s.add_argument("name")
    s.set_defaults(fn=cmd_stage)
    s = sub.add_parser("run")
    s.add_argument("--max", type=int, default=99)
    s.set_defaults(fn=cmd_run)
    s = sub.add_parser("release")
    s.add_argument("--allow-known-issues", action="store_true")
    s.set_defaults(fn=cmd_release)
    s = sub.add_parser("ticket")
    s.add_argument("op", choices=("add", "list", "set"))
    s.add_argument("id", nargs="?")
    s.add_argument("--kind", default="feature")
    s.add_argument("--title", default="")
    s.add_argument("--body", default="")
    s.add_argument("--source", default="user")
    s.add_argument("--status", default="")
    s.add_argument("--parent", default="", help="id of the ticket this is a slice of")
    s.add_argument(
        "--touches", default="", help="comma-separated modules this slice changes"
    )
    s.set_defaults(fn=cmd_ticket)
    a = ap.parse_args()
    app = App(a.app)
    if a.cmd != "init" and not app.t.exists():
        die("no .tinker/ here; run `tb.py init`", 2)
    sys.exit(a.fn(app, a) or 0)


if __name__ == "__main__":
    main()
