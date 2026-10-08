#!/usr/bin/env python3
"""Checks that release_filter.py ships team-index.yaml trimmed to released skills.

Run: python3 scripts/test_release_filter.py
"""

import os
import re
import shutil
import subprocess
import tempfile

import yaml

REPO = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def name(item):
    return next(iter(item)) if isinstance(item, dict) else str(item).split(":")[0]


def test_team_index_ships_trimmed_to_released():
    tmp = tempfile.mkdtemp()
    try:
        tar = subprocess.run(["git", "-C", REPO, "archive", "HEAD"], capture_output=True, check=True)
        subprocess.run(["tar", "-x", "-C", tmp], input=tar.stdout, check=True)
        shutil.copy2(os.path.join(REPO, "scripts", "release_filter.py"), os.path.join(tmp, "scripts"))
        stage = os.path.join(tmp, "stage")
        subprocess.run(["python3", os.path.join(tmp, "scripts", "release_filter.py"), tmp, stage, "test", REPO],
                       capture_output=True, check=True)
        released = set(re.findall(r"^  - ([a-z0-9-]+)\s*$", open(os.path.join(tmp, "RELEASE.yaml")).read(), re.M))
        src = yaml.safe_load(open(os.path.join(tmp, "library", "team-index.yaml")))
        out = yaml.safe_load(open(os.path.join(stage, "library", "team-index.yaml")))
        assert set(out) == set(src) & released
        for n, entry in out.items():
            assert entry["not_for"] == [x for x in src[n]["not_for"] or [] if name(x) in released], n
            assert {k: v for k, v in entry.items() if k != "not_for"} == \
                   {k: v for k, v in src[n].items() if k != "not_for"}, n
    finally:
        shutil.rmtree(tmp, True)


if __name__ == "__main__":
    test_team_index_ships_trimmed_to_released()
    print("ok  test_team_index_ships_trimmed_to_released\n1 passed")
