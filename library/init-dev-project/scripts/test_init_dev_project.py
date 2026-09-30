#!/usr/bin/env python3
"""Self-check: scaffold into a temp dir and assert the contract holds."""
import json, os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "init_dev_project.py")


def sh(*cmd, cwd=None, ok=True):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    assert (r.returncode == 0) == ok, f"{cmd}\n{r.stdout}\n{r.stderr}"
    return r.stdout


with tempfile.TemporaryDirectory() as tmp:
    p = os.path.join(tmp, "demo-app")
    out = json.loads(sh(sys.executable, SCRIPT, p, "--kind", "web", "--description", "Demo.", "--json"))
    for f in ["README.md", "VERSION", "CHANGELOG.md", "Makefile", ".gitignore",
              ".aai/instructions.md", ".aai/identity.md", ".aai/purpose.md", ".aai/context.md",
              ".aai/HANDOFF.md", ".aai/checkpoint.md", ".aai/references/dev-standard.md"]:
        assert os.path.isfile(os.path.join(p, f)), f
        assert "{{" not in open(os.path.join(p, f)).read(), f"unrendered placeholder in {f}"
    assert "demo-app" in open(os.path.join(p, "README.md")).read()
    assert open(os.path.join(p, ".aai/references/dev-standard.md")).read().startswith("<!-- init-dev-project v")
    assert sh("git", "tag", cwd=p).strip() == "v0.0.0"
    assert sh("git", "status", "--porcelain", cwd=p) == ""
    assert sh("git", "branch", "--show-current", cwd=p).strip() == "main"
    # idempotent: second run creates nothing, touches git nothing
    again = json.loads(sh(sys.executable, SCRIPT, p, "--json"))
    assert again["created"] == [] and "untouched" in again["git"]
    # the four verbs: help works, closed gates fail, deploy refuses when untagged
    assert "make release" in sh("make", cwd=p)
    sh("make", "check", cwd=p, ok=False)
    sh("make", "run", cwd=p, ok=False)
    # release path: define check, then release bumps VERSION, CHANGELOG and tags
    mk = open(os.path.join(p, "Makefile")).read().replace(
        '\t@echo "check: not defined yet — a gate with nothing behind it must fail" >&2; exit 1', '\t@true')
    open(os.path.join(p, "Makefile"), "w").write(mk)
    sh("git", "commit", "-qam", "define check", cwd=p)
    sh("make", "release", "NOTE=first", cwd=p)
    assert open(os.path.join(p, "VERSION")).read().strip() == "0.0.1"
    assert "## v0.0.1" in open(os.path.join(p, "CHANGELOG.md")).read().splitlines()[2]
    assert "v0.0.1" in sh("git", "tag", cwd=p)
    sh("make", "release", "BUMP=minor", cwd=p)
    assert open(os.path.join(p, "VERSION")).read().strip() == "0.1.0"
    # dry run writes nothing
    q = os.path.join(tmp, "dry")
    d = json.loads(sh(sys.executable, SCRIPT, q, "--dry-run", "--json"))
    assert d["created"] and not os.path.exists(q)
print("ok")
