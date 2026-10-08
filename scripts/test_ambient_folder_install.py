#!/usr/bin/env python3
"""Checks for ambient-folder/install.sh anchors over throwaway libraries.

Run: python3 scripts/test_ambient_folder_install.py
"""

import atexit
import os
import shutil
import subprocess
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
POINTER = "rules/coding.md"
BLOCK = "## Coding rules"


class Lib:
    """A throwaway library holding ambient-folder, dev-rules, and two capabilities."""

    def __init__(self):
        self.root = os.path.realpath(tempfile.mkdtemp())
        atexit.register(shutil.rmtree, self.root, True)
        self.lib = os.path.join(self.root, "library")
        for cap in ("ambient-folder", "dev-rules"):
            shutil.copytree(os.path.join(REPO, "library", cap), os.path.join(self.lib, cap))
        self.cap("with-rules", depends="ambient-folder\ndev-rules\n")
        self.cap("without-rules", depends="ambient-folder\n")
        self.target = os.path.join(self.root, "project")

    def cap(self, name, depends):
        d = os.path.join(self.lib, name)
        os.makedirs(d)
        with open(os.path.join(d, "SKILL.md"), "w") as f:
            f.write(f"---\nname: {name}\n---\n")
        with open(os.path.join(d, "DEPENDS"), "w") as f:
            f.write(depends)

    def install(self, cap, *args):
        r = subprocess.run(
            ["bash", os.path.join(self.lib, "ambient-folder", "install.sh"), cap, *args, self.target],
            capture_output=True, text=True,
        )
        assert r.returncode == 0, r.stderr
        return r.stdout

    def read(self, name):
        path = os.path.join(self.target, name)
        return open(path).read() if os.path.exists(path) else ""


def test_pointer_written_when_dev_rules_vendored():
    lib = Lib()
    lib.install("with-rules")
    for name in ("CLAUDE.md", "AGENTS.md", "GEMINI.md"):
        assert lib.read(name).count(BLOCK) == 1, name
        assert "ambient folder" in lib.read(name), name


def test_no_pointer_without_dev_rules():
    lib = Lib()
    lib.install("without-rules")
    assert POINTER not in lib.read("CLAUDE.md")


def test_reinstall_adds_no_duplicate():
    lib = Lib()
    lib.install("with-rules")
    lib.install("with-rules")
    assert lib.read("AGENTS.md").count(BLOCK) == 1


def test_existing_folder_gets_pointer_on_refresh():
    lib = Lib()
    lib.install("without-rules")
    assert POINTER not in lib.read("CLAUDE.md")
    lib.install("with-rules")
    text = lib.read("CLAUDE.md")
    assert text.count(BLOCK) == 1
    assert text.count("ambient folder") >= 1


def test_file_already_naming_rules_is_left_alone():
    lib = Lib()
    os.makedirs(lib.target)
    with open(os.path.join(lib.target, "CLAUDE.md"), "w") as f:
        f.write("Read ~/.aai/rules/coding.md before coding.\n")
    lib.install("with-rules")
    assert BLOCK not in lib.read("CLAUDE.md")


def test_owned_aai_untouched():
    lib = Lib()
    os.makedirs(os.path.join(lib.target, ".aai"))
    owned = os.path.join(lib.target, ".aai", "instructions.md")
    with open(owned, "w") as f:
        f.write("# mine\n")
    lib.install("with-rules")
    assert open(owned).read() == "# mine\n"


def test_check_plans_pointer_and_writes_nothing():
    lib = Lib()
    out = lib.install("with-rules", "--check")
    assert "coding-rules pointer" in out
    assert not os.path.exists(os.path.join(lib.target, "CLAUDE.md"))


if __name__ == "__main__":
    tests = [f for name, f in sorted(globals().items()) if name.startswith("test_")]
    for f in tests:
        f()
        print(f"ok  {f.__name__}")
    print(f"{len(tests)} passed")
