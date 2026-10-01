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
              ".aai/HANDOFF.md", ".aai/checkpoint.md", ".aai/references/dev-standard.md",
              "deploy/SHIPLIST"]:
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
    # build enforces SHIPLIST: nothing in src/ or docs/ yet, so it fails
    sh("make", "build", cwd=p, ok=False)
    os.makedirs(os.path.join(p, "src")); os.makedirs(os.path.join(p, "docs"))
    open(os.path.join(p, "src", "app.py"), "w").write("print('hi')\n")
    open(os.path.join(p, "docs", "help.md"), "w").write("# help\n")
    sh("make", "build", cwd=p)
    assert sorted(os.listdir(os.path.join(p, "build", "candidate"))) == ["VERSION", "docs", "src"]
    # define check only; accept still fails, so release must restore VERSION and tag nothing
    mk = os.path.join(p, "Makefile")
    src = open(mk).read(); open(mk, "w").write(src.replace(
        '\t@echo "check: not defined yet — a gate with nothing behind it must fail" >&2; exit 1', '\t@true'))
    sh("git", "add", "-A", cwd=p); sh("git", "commit", "-qm", "define check", cwd=p)
    r = subprocess.run(["make", "release", "NOTE=first"], cwd=p, capture_output=True, text=True)
    assert r.returncode != 0 and "acceptance failed" in r.stderr, r.stderr
    assert open(os.path.join(p, "VERSION")).read().strip() == "0.0.0"
    assert sh("git", "status", "--porcelain", cwd=p) == ""
    assert sh("git", "tag", cwd=p).strip() == "v0.0.0"
    # define accept; it must see the bumped VERSION in the candidate
    src = open(mk).read(); open(mk, "w").write(src.replace(
        '\t@echo "accept: not defined yet — a gate with nothing behind it must fail" >&2; exit 1',
        '\t@cat build/candidate/VERSION > build/accepted'))
    sh("git", "commit", "-qam", "define accept", cwd=p)
    sh("make", "release", "NOTE=first", cwd=p)
    assert open(os.path.join(p, "VERSION")).read().strip() == "0.0.1"
    assert open(os.path.join(p, "build", "accepted")).read().strip() == "0.0.1", "accept ran on a stale VERSION"
    assert "## v0.0.1" in open(os.path.join(p, "CHANGELOG.md")).read().splitlines()[2]
    assert "v0.0.1" in sh("git", "tag", cwd=p)
    sh("make", "release", "BUMP=minor", cwd=p)
    assert open(os.path.join(p, "VERSION")).read().strip() == "0.1.0"
    assert sh("git", "status", "--porcelain", cwd=p) == ""
    # existing deploy/: a ship list the owner already wrote is kept, not overwritten
    e = os.path.join(tmp, "existing")
    os.makedirs(os.path.join(e, "deploy", "docker"))
    open(os.path.join(e, "deploy", "SHIPLIST"), "w").write("VERSION\nworker/\n")
    open(os.path.join(e, "deploy", "docker", "compose.yaml"), "w").write("services: {}\n")
    r = json.loads(sh(sys.executable, SCRIPT, e, "--json"))
    assert "deploy/SHIPLIST" in r["skipped"] and "deploy/SHIPLIST" not in r["created"]
    assert open(os.path.join(e, "deploy", "SHIPLIST")).read() == "VERSION\nworker/\n"
    assert open(os.path.join(e, "deploy", "docker", "compose.yaml")).read() == "services: {}\n"
    assert sh("git", "status", "--porcelain", cwd=e) == ""   # owner's files are in the first commit
    # ship list entries with spaces: one line is one path, never split on whitespace
    os.makedirs(os.path.join(p, "user guide"))
    open(os.path.join(p, "user guide", "intro.md"), "w").write("# intro\n")
    open(os.path.join(p, "deploy", "SHIPLIST"), "a").write("user guide/\n")
    sh("make", "build", cwd=p)
    assert os.path.isfile(os.path.join(p, "build", "candidate", "user guide", "intro.md"))
    # a listed path with spaces that does not exist still fails the build
    open(os.path.join(p, "deploy", "SHIPLIST"), "a").write("release notes.md\n")
    r = subprocess.run(["make", "build"], cwd=p, capture_output=True, text=True)
    assert r.returncode != 0 and "release notes.md is on SHIPLIST but missing" in r.stderr, r.stderr
    # dry run writes nothing
    q = os.path.join(tmp, "dry")
    d = json.loads(sh(sys.executable, SCRIPT, q, "--dry-run", "--json"))
    assert d["created"] and not os.path.exists(q)
print("ok")
