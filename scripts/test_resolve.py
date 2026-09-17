#!/usr/bin/env python3
"""Checks for resolve.py over a throwaway tree. Run: python3 scripts/test_resolve.py"""

import json
import os
import subprocess
import sys
import tempfile

RESOLVE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "resolve.py")

MULTI = "multi: true\nenvironment:\n  operator_name:\nproject:\n  org_id:\nstate:\n  - .aai/memory/gears/\n  - output/\n"
SINGLE = "environment:\n  from_address:  # who sends\nproject:\n  list_name:\n"


class Tree:
    def __init__(self, contract, skill="gears"):
        self.root = os.path.realpath(tempfile.mkdtemp())
        self.home = self.mk("home")
        self.skill_dir = self.mk("lib", skill)
        self.P = os.path.join(".aai", "skills", skill)
        with open(os.path.join(self.skill_dir, "contract.yaml"), "w") as f:
            f.write(contract)

    def mk(self, *parts):
        d = os.path.join(self.root, *parts)
        os.makedirs(d, exist_ok=True)
        return d

    def run(self, cwd, *args, ok=True):
        r = subprocess.run(
            [sys.executable, RESOLVE, "--skill-dir", self.skill_dir, *args],
            cwd=cwd,
            env={**os.environ, "HOME": self.home},
            capture_output=True,
            text=True,
        )
        assert (r.returncode == 0) == ok, r.stderr or r.stdout
        return json.loads(r.stdout) if ok else r.stderr


def clients():
    """home/clients stamped multi with acme + globex, each with an org_id."""
    t = Tree(MULTI)
    c = t.mk("home", "clients")
    t.run(
        c,
        "--init",
        "--multi",
        "--env",
        "operator_name=Lou",
        "--project",
        "acme",
        "globex",
    )
    for name in ("acme", "globex"):
        t.run(c, "--start", name, "--set", f"project.org_id={name}-1")
    return t, c


def test_open_by_name_from_parent():
    t, c = clients()
    out = t.run(c, "--start", "acme")
    assert out["project_dir"] == os.path.join(c, "acme")
    assert out["project"] == {"org_id": "acme-1"} and out["environment"] == {
        "operator_name": "Lou"
    }
    assert out["environment_file"] == os.path.join(c, t.P, "environment.yaml")
    assert out["state"] == [
        os.path.join(c, "acme", ".aai/memory/gears/"),
        os.path.join(c, "acme", "output/"),
    ]
    assert out["overrides"] is None and "needs" not in out


def test_open_from_nested_path():
    t, c = clients()
    out = t.run(t.mk("home", "clients", "acme", "drafts", "deep"))
    assert out["project_dir"] == os.path.join(c, "acme")


def test_new_beside_siblings():
    t, c = clients()
    out = t.run(c, "--start", "initech", "--intent", "setup")
    assert (
        out["new"]
        and out["project_dir"] == os.path.join(c, "initech")
        and out["needs"] == ["project.org_id"]
    )
    assert not os.path.exists(out["project_dir"]), "plain resolution must not write"
    out = t.run(
        c, "--start", "initech", "--intent", "setup", "--set", "project.org_id=i-1"
    )
    assert out["project"] == {"org_id": "i-1"} and out["environment"] == {
        "operator_name": "Lou"
    }
    assert sorted(t.run(c, "--intent", "setup")["ask"]) == ["acme", "globex", "initech"]


def test_plain_cwd_no_layout():
    t = Tree(SINGLE, "news")
    d = t.mk("home", "newsletter")
    out = t.run(d)
    assert (
        out["new"] and out["project_dir"] == d and out["needs"] == ["project.list_name"]
    )
    t.run(
        d, "--set", "project.list_name=AIMM", ok=False
    )  # not confirmed: no --intent setup
    out = t.run(d, "--intent", "setup", "--set", "project.list_name=AIMM")
    assert out["project"] == {"list_name": "AIMM"} and out["needs"] == [
        "env.from_address"
    ]


def test_mid_session_switch():
    t, c = clients()
    acme = os.path.join(c, "acme")
    out = t.run(
        acme, "--start", "globex", "--current", acme
    )  # "now do globex", cwd still acme
    assert (
        out["project_dir"] == os.path.join(c, "globex")
        and out["project"]["org_id"] == "globex-1"
    )


def test_named_folder_missing_never_falls_back():
    t, c = clients()
    out = t.run(os.path.join(c, "acme"), "--start", "initrode")
    assert out["ask"] == ["acme", "globex"] and "project_dir" not in out


def test_sibling_named_from_inside_project_without_current():
    t, c = clients()
    assert t.run(os.path.join(c, "acme"), "--start", "globex")[
        "project_dir"
    ] == os.path.join(c, "globex")
    out = t.run(os.path.join(c, "acme"), "--start", "initech", "--intent", "setup")
    assert out["project_dir"] == os.path.join(c, "initech"), (
        "new project goes beside, not inside"
    )


def test_stamped_parent_zero_projects():
    t = Tree(MULTI)
    c = t.mk("home", "clients")
    t.run(c, "--init", "--multi")
    out = t.run(c)
    assert out["ask"] == [] and out["can_create"]


def test_single_child_no_ask():
    t = Tree(MULTI)
    c = t.mk("home", "clients")
    t.run(c, "--init", "--multi", "--project", "acme")
    assert t.run(c)["project_dir"] == os.path.join(c, "acme")


def test_parent_with_many_asks():
    t, c = clients()
    assert t.run(c)["ask"] == ["acme", "globex"]


def test_first_environment_save():
    # vendored parent: environment lands beside .ailib/, never in the project or inside .ailib/
    t = Tree(MULTI)
    c = t.mk("home", "clients")
    t.mk("home", "clients", ".ailib", "gears")
    t.run(
        c,
        "--start",
        "acme",
        "--intent",
        "setup",
        "--set",
        "project.org_id=a",
        "env.operator_name=Lou",
    )
    assert os.path.isfile(os.path.join(c, t.P, "environment.yaml"))
    assert not os.path.exists(os.path.join(c, "acme", t.P, "environment.yaml"))
    # nothing vendored: goes to ~/P, and an environment-only ~/P is not a project
    t = Tree(SINGLE, "news")
    d = t.mk("home", "newsletter")
    out = t.run(
        d,
        "--intent",
        "setup",
        "--set",
        "project.list_name=AIMM",
        "env.from_address=a@b.co",
    )
    assert (
        out["environment_file"] == os.path.join(t.home, t.P, "environment.yaml")
        and "needs" not in out
    )
    assert t.run(t.mk("home", "elsewhere"))["new"], (
        "~/P environment must not make ~ a project"
    )


def test_init_single_and_multi():
    t = Tree(SINGLE, "news")
    d = t.mk("home", "newsletter")
    out = t.run(d, "--init", "--env", "from_address=a@b.co")
    assert out["initialized"] == [d] and t.run(d)["environment"] == {
        "from_address": "a@b.co"
    }
    t.run(d, "--init", "--multi", ok=False)  # contract is not multi
    t.run(d, "--init", "--env", "nope=1", ok=False)  # key not in contract
    t.run(d, "--set", "project.list_name=AIMM")
    t.run(d, "--init")  # idempotent: re-init keeps values
    assert t.run(d)["project"] == {"list_name": "AIMM"}


def test_overrides_and_dry_run():
    t, c = clients()
    o = os.path.join(c, "acme", t.P, "overrides.md")
    open(o, "w").write("- sign off as Lou\n")
    assert t.run(c, "--start", "acme")["overrides"] == o
    t.run(c, "--start", "acme", "--set", "project.org_id=changed", "--dry-run")
    assert t.run(c, "--start", "acme")["project"]["org_id"] == "acme-1"


def test_values_with_yaml_specials_round_trip():
    t, c = clients()
    v = 'Lou: "the" #1 operator'
    assert (
        t.run(c, "--start", "acme", "--set", f"env.operator_name={v}")["environment"][
            "operator_name"
        ]
        == v
    )


if __name__ == "__main__":
    tests = [f for n, f in sorted(globals().items()) if n.startswith("test_")]
    for f in tests:
        f()
        print(f"ok  {f.__name__}")
    print(f"{len(tests)} passed")
