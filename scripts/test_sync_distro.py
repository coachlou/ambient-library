#!/usr/bin/env python3
"""Checks for sync-distro.sh over a throwaway app repo + library. Run: python3 scripts/test_sync_distro.py"""

import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.realpath(__file__))
SYNC = os.path.join(HERE, "sync-distro.sh")

PLUGIN = {"name": "demo", "version": "0.1.0"}
APP_FILES = "src\nREADME.md\n"


def git(cwd, *args):
    subprocess.run(["git", "-C", cwd, *args], check=True, capture_output=True, text=True)


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(text)


class Tree:
    """An app repo with distro/ + src/ + README.md, and a library checkout to sync into."""

    def __init__(self, app_files=APP_FILES):
        self.root = os.path.realpath(tempfile.mkdtemp())
        self.app = os.path.join(self.root, "app-repo")
        self.lib = os.path.join(self.root, "lib")
        # library layout: only scripts/ and an existing library/<cap>/ matter to the script
        os.makedirs(os.path.join(self.lib, "scripts"))
        os.makedirs(os.path.join(self.lib, "library", "demo"))
        shutil.copy(SYNC, os.path.join(self.lib, "scripts", "sync-distro.sh"))

        write(os.path.join(self.app, "distro", "SKILL.md"), "# demo\n")
        write(
            os.path.join(self.app, "distro", ".claude-plugin", "plugin.json"),
            json.dumps(PLUGIN) + "\n",
        )
        write(os.path.join(self.app, "distro", "APP_FILES"), app_files)
        write(os.path.join(self.app, "src", "main.py"), "print(1)\n")
        write(os.path.join(self.app, "README.md"), "committed readme\n")
        write(os.path.join(self.app, ".gitignore"), "__pycache__/\n")
        git(self.app, "init", "-q")
        git(self.app, "config", "user.email", "t@t.test")
        git(self.app, "config", "user.name", "t")
        self.commit("first")

    def commit(self, msg):
        git(self.app, "add", "-A")
        git(self.app, "commit", "-q", "-m", msg)
        return self.head()

    def head(self):
        return subprocess.run(
            ["git", "-C", self.app, "rev-parse", "--short", "HEAD"],
            check=True, capture_output=True, text=True,
        ).stdout.strip()

    def sync(self, *args, ok=True):
        r = subprocess.run(
            ["bash", os.path.join(self.lib, "scripts", "sync-distro.sh"), *args,
             "demo", self.app],
            cwd=self.lib, capture_output=True, text=True,
        )
        assert (r.returncode == 0) == ok, r.stderr or r.stdout
        return r.stderr + r.stdout

    def dest(self, *parts):
        return os.path.join(self.lib, "library", "demo", *parts)

    def read(self, *parts):
        with open(self.dest(*parts)) as f:
            return f.read()


def test_clean_sync_matches_commit():
    t = Tree()
    t.sync()
    assert t.read("SKILL.md") == "# demo\n"
    assert t.read("app", "src", "main.py") == "print(1)\n"
    assert t.read("app", "README.md") == "committed readme\n"
    assert t.read("app", "VERSION").startswith(f"demo 0.1.0 ({t.head()})"), (
        t.read("app", "VERSION")
    )


def test_modified_tracked_file_is_not_synced():
    t = Tree()
    write(os.path.join(t.app, "README.md"), "DIRTY local edit\n")
    out = t.sync()
    assert t.read("app", "README.md") == "committed readme\n"
    assert "1 uncommitted path(s)" in out, out


def test_untracked_file_is_not_synced():
    t = Tree()
    write(os.path.join(t.app, "src", "scratch.py"), "wip\n")
    t.sync()
    assert not os.path.exists(t.dest("app", "src", "scratch.py"))


def test_ignored_file_is_not_synced():
    t = Tree()
    write(os.path.join(t.app, "src", "__pycache__", "main.pyc"), "junk\n")
    t.sync()
    assert not os.path.exists(t.dest("app", "src", "__pycache__"))


def test_ref_syncs_that_commit():
    t = Tree()
    first = t.head()
    write(os.path.join(t.app, "src", "main.py"), "print(2)\n")
    t.commit("second")
    t.sync("--ref", first)
    assert t.read("app", "src", "main.py") == "print(1)\n"
    assert f"({first})" in t.read("app", "VERSION")
    t.sync()  # back to HEAD
    assert t.read("app", "src", "main.py") == "print(2)\n"


def test_missing_app_files_entry_fails():
    t = Tree(app_files="src\nREADME.md\nnope/\n")
    out = t.sync(ok=False)
    assert "nope/" in out, out


def test_bad_ref_fails():
    t = Tree()
    out = t.sync("--ref", "v9.9.9-nope", ok=False)
    assert "does not resolve" in out, out


def test_stale_dest_file_is_removed():
    t = Tree()
    write(t.dest("leftover.md"), "from an earlier sync\n")
    t.sync()
    assert not os.path.exists(t.dest("leftover.md"))


if __name__ == "__main__":
    tests = [f for n, f in sorted(globals().items()) if n.startswith("test_")]
    for f in tests:
        f()
        print(f"ok  {f.__name__}")
    print(f"{len(tests)} passed")
