#!/usr/bin/env python3
"""Checks for sync-skill-stubs.py over a throwaway project. Run: python3 scripts/test_sync_skill_stubs.py"""

import json
import os
import subprocess
import sys
import tempfile

SCRIPT = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "sync-skill-stubs.py"
)
LIB = os.path.realpath(os.path.join(os.path.dirname(SCRIPT), "..", "library"))
SKILL = "deep-mirror"  # any library skill that ships a SKILL.md


def run(root, manifest, *args):
    with open(os.path.join(root, "skills-manifest.yaml"), "w") as f:
        f.write(manifest)
    r = subprocess.run(
        [sys.executable, SCRIPT, "--project", root, *args],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout)


def main():
    root = tempfile.mkdtemp()
    stub = os.path.join(root, ".claude", "skills", SKILL, "SKILL.md")
    on = f"# project skills\ndomain_skills:   # opt-in\n  - {SKILL}  # trailing\nother: x\n"

    assert run(root, on, "--dry-run")["written"] and not os.path.exists(stub), (
        "dry run writes"
    )
    out = run(root, on)
    assert out["written"] == [f".claude/skills/{SKILL}", f".agents/skills/{SKILL}"], out
    text = open(stub).read()
    front = open(os.path.join(LIB, SKILL, "SKILL.md")).read().split("\n---", 1)[0]
    assert text.startswith(front), "frontmatter copied verbatim"
    assert os.path.join(LIB, SKILL, "instructions.md") in text, "points at library body"
    assert not os.path.islink(os.path.dirname(stub)), "plain files, not links"
    assert run(root, on) == {
        "written": [],
        "removed": [],
        "missing": [],
        "skipped": [],
    }, "idempotent"

    with open(stub, "a") as f:
        f.write("drift\n")
    assert run(root, on)["written"] == [f".claude/skills/{SKILL}"], (
        "stale stub rewritten"
    )

    own = os.path.join(root, ".claude", "skills", "mine")
    os.makedirs(own)
    open(os.path.join(own, "SKILL.md"), "w").write("---\nname: mine\n---\n")
    open(os.path.join(os.path.dirname(stub), "notes.txt"), "w").write("user file")
    out = run(root, "domain_skills: [nope, mine]\n")
    assert out["missing"] == ["nope", "mine"], out
    assert out["removed"] == [f".claude/skills/{SKILL}", f".agents/skills/{SKILL}"], out
    assert not os.path.exists(stub), "disabled stub removed"
    assert os.path.exists(os.path.join(os.path.dirname(stub), "notes.txt")), (
        "user file kept"
    )
    assert os.path.exists(os.path.join(own, "SKILL.md")), "user skill untouched"
    assert not os.path.exists(os.path.join(root, ".agents", "skills", SKILL)), (
        "empty stub dir removed"
    )

    os.makedirs(os.path.join(root, ".agents", "skills", SKILL))
    open(os.path.join(root, ".agents", "skills", SKILL, "SKILL.md"), "w").write(
        "---\nname: fork\n---\n"
    )
    assert run(root, on)["skipped"] == [f".agents/skills/{SKILL}"], (
        "unmarked folder skipped"
    )
    print("ok")


if __name__ == "__main__":
    main()
