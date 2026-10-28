"""One full lane on a throwaway repo: rc.1 -> issue -> rc.2 -> uat -> release -> deploy.

Run: python3 -m pytest test_release_lane.py   (or: python3 test_release_lane.py)
"""

import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).with_name("release_lane.py").resolve()

CONFIG = """\
check = "true"
accept = "test ! -f FAIL_ACCEPT"
deploy_staging = "echo {tag} > deployed-{channel}.txt"
deploy_production = "echo {tag} > deployed-{channel}.txt"
"""
UAT_HEAD = (
    "| id | reporter | rc | severity | status | commit |\n|---|---|---|---|---|---|\n"
)


def sh(repo, *cmd):
    return subprocess.run(cmd, cwd=repo, capture_output=True, text=True)


def lane(repo, *args):
    r = sh(repo, sys.executable, str(SCRIPT), *args)
    return r.returncode, r.stdout + r.stderr


def commit(repo, msg):
    sh(repo, "git", "add", "-A")
    assert sh(repo, "git", "commit", "-qm", msg).returncode == 0


def make_repo(tmp):
    repo = Path(tmp)
    sh(repo, "git", "init", "-qb", "main")
    sh(repo, "git", "config", "user.email", "t@example.com")
    sh(repo, "git", "config", "user.name", "t")
    (repo / "VERSION").write_text("0.1.0\n")
    (repo / "CHANGELOG.md").write_text(
        "# Changelog\n\n## Unreleased\n\n## v0.1.0 — 2026-01-01\n- first\n"
    )
    cfg = repo / ".aai/skills/release-lane"
    cfg.mkdir(parents=True)
    (cfg / "project.toml").write_text(CONFIG)
    (repo / ".gitignore").write_text("deployed-*.txt\n")
    (repo / "tests/acceptance").mkdir(parents=True)
    (repo / "tests/acceptance/UAT.md").write_text(UAT_HEAD)
    commit(repo, "init")
    sh(repo, "git", "tag", "-a", "v0.1.0", "-m", "v0.1.0")
    return repo


def test_full_lane():
    with tempfile.TemporaryDirectory() as tmp:
        repo = make_repo(tmp)
        sh(repo, "git", "checkout", "-qb", "feature")

        # empty Unreleased blocks the rc
        code, out = lane(repo, "rc")
        assert code == 1 and "Unreleased" in out, out

        cl = repo / "CHANGELOG.md"
        cl.write_text(
            cl.read_text().replace("## Unreleased\n", "## Unreleased\n- new thing\n")
        )
        commit(repo, "feature")

        # failed acceptance restores VERSION and tags nothing
        (repo / "FAIL_ACCEPT").touch()
        commit(repo, "break accept")
        code, out = lane(repo, "rc", "--bump", "minor")
        assert code == 1 and "restored" in out, out
        assert (repo / "VERSION").read_text() == "0.1.0\n"
        assert not sh(repo, "git", "tag", "-l", "v0.2.0*").stdout
        (repo / "FAIL_ACCEPT").unlink()
        commit(repo, "fix accept")

        # dry run changes nothing
        code, out = lane(repo, "rc", "--bump", "minor", "--dry-run")
        assert code == 0 and "[dry-run]" in out, out
        assert (repo / "VERSION").read_text() == "0.1.0\n"

        # rc.1 bumps once
        code, out = lane(repo, "rc", "--bump", "minor")
        assert code == 0, out
        assert (repo / "VERSION").read_text() == "0.2.0\n"
        assert "v0.2.0-rc.1" in sh(repo, "git", "tag").stdout

        # same HEAD again is refused; staging deploy works, production refuses an rc
        assert lane(repo, "rc")[0] == 1
        assert lane(repo, "deploy", "--channel", "staging")[0] == 0
        assert (repo / "deployed-staging.txt").read_text().strip() == "v0.2.0-rc.1"
        assert lane(repo, "deploy", "--channel", "production")[0] == 1

        # a tester finds a blocker
        uat = repo / "tests/acceptance/UAT.md"
        uat.write_text(
            UAT_HEAD
            + "| U1 | sam | rc.1 | blocker | open | |\n| U2 | sam | rc.1 | major | deferred | |\n"
        )
        commit(repo, "log U1")
        code, out = lane(repo, "uat")
        assert code == 1 and "U1" in out, out

        # fix, rc.2 keeps the version
        uat.write_text(
            UAT_HEAD
            + "| U1 | sam | rc.1 | blocker | fixed | abc |\n| U2 | sam | rc.1 | major | deferred | |\n"
        )
        commit(repo, "fix U1")
        assert lane(repo, "rc")[0] == 0
        assert (repo / "VERSION").read_text() == "0.2.0\n"
        assert "v0.2.0-rc.2" in sh(repo, "git", "tag").stdout
        assert lane(repo, "uat")[0] == 0

        # release refuses off main
        code, out = lane(repo, "release")
        assert code == 1 and "merge" in out, out

        # an untested commit slipped onto main is refused
        sh(repo, "git", "checkout", "-q", "main")
        sh(repo, "git", "merge", "-q", "--no-ff", "feature", "-m", "merge")
        (repo / "hotfix.txt").write_text("x")
        commit(repo, "untested")
        code, out = lane(repo, "release")
        assert code == 1 and "differs" in out, out
        sh(repo, "git", "reset", "-q", "--hard", "HEAD~1")

        # promote
        code, out = lane(repo, "release")
        assert code == 0, out
        assert "v0.2.0" in sh(repo, "git", "tag", "--points-at", "HEAD").stdout.split()
        assert "## Unreleased\n\n## v0.2.0 — " in cl.read_text()
        assert (
            sh(
                repo, "git", "merge-base", "--is-ancestor", "v0.2.0-rc.2", "HEAD"
            ).returncode
            == 0
        )
        assert lane(repo, "deploy", "--channel", "production")[0] == 0
        assert (repo / "deployed-production.txt").read_text().strip() == "v0.2.0"

        # status is JSON and sees the shipped version
        code, out = lane(repo, "status")
        assert code == 0 and '"released": true' in out, out


def test_legacy_release_without_rc():
    with tempfile.TemporaryDirectory() as tmp:
        repo = make_repo(tmp)
        cl = repo / "CHANGELOG.md"
        cl.write_text(
            cl.read_text().replace("## Unreleased\n", "## Unreleased\n- quick fix\n")
        )
        commit(repo, "fix")
        code, out = lane(repo, "release")
        assert code == 0, out
        assert (repo / "VERSION").read_text() == "0.1.1\n"
        assert "v0.1.1" in sh(repo, "git", "tag").stdout.split()


if __name__ == "__main__":
    test_full_lane()
    test_legacy_release_without_rc()
    print("ok")
