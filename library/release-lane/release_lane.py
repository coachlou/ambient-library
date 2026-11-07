#!/usr/bin/env python3
"""release-lane: the deterministic half of the release loop.

Verbs:
  status                     read-only JSON report: version, tags, Unreleased, UAT
  check                      run the configured check command
  rc [--bump patch|minor|major] [--dry-run]
                             cut vX.Y.Z-rc.N: bump once per version, accept, tag
  uat                        exit 1 on a blocker not fixed or a major still open
  release [--bump ...] [--dry-run]
                             promote: on the main branch, uat ok, tree == last rc,
                             accept, date CHANGELOG, tag vX.Y.Z (no rc: bump + accept)
  deploy --channel staging|production [--dry-run]
                             staging needs an rc tag on HEAD, production a release tag;
                             then deploy_verify (if set) must report {version}

Config: <repo>/.aai/skills/release-lane/project.toml (all keys optional; see DEFAULTS).
Commands may use {version}, {tag} and {channel}. Never pushes.

Exit codes: 0 ok, 1 a gate failed, 2 usage or config error.
"""

import argparse
import datetime
import json
import os
import re
import subprocess
import sys
import tomllib
from pathlib import Path

DEFAULTS = {
    "version_files": ["VERSION"],
    "version_check": "",
    "changelog": "CHANGELOG.md",
    "require_files": [],
    "check": "make check",
    "accept": "make accept",
    "uat_log": "tests/acceptance/UAT.md",
    "deploy_staging": "make ship CHANNEL=staging",
    "deploy_production": "make ship CHANNEL=production",
    "deploy_verify": "",
    "main_branch": "main",
}
SEMVER = re.compile(r"\d+\.\d+\.\d+")
CONFIG_PATH = ".aai/skills/release-lane/project.toml"
STATUSES = ("open", "fixed", "deferred")
SEVERITIES = ("blocker", "major", "minor")


class Gate(Exception):
    """A gate failed: exit 1 with this message."""


class Usage(Exception):
    """Bad config or arguments: exit 2."""


def git(*args, check=True):
    r = subprocess.run(["git", *args], capture_output=True, text=True)
    if check and r.returncode:
        raise Usage(f"git {' '.join(args)}: {r.stderr.strip()}")
    return r.stdout.strip()


def load_config(root):
    cfg = dict(DEFAULTS)
    p = root / CONFIG_PATH
    if p.exists():
        try:
            extra = tomllib.loads(p.read_text())
        except tomllib.TOMLDecodeError as e:
            raise Usage(f"{CONFIG_PATH}: {e}")
        unknown = set(extra) - set(DEFAULTS)
        if unknown:
            raise Usage(f"{CONFIG_PATH}: unknown keys {sorted(unknown)}")
        cfg.update(extra)
    return cfg


class Lane:
    def __init__(self, root, cfg, dry_run=False):
        self.root, self.cfg, self.dry = root, cfg, dry_run

    # --- helpers -------------------------------------------------------
    def say(self, msg):
        print(msg, file=sys.stderr)

    def sh(self, key, **fmt):
        cmd = self.cfg[key].format(**fmt)
        if not cmd:
            raise Usage(f"{key} is not configured in {CONFIG_PATH}")
        if self.dry:
            self.say(f"[dry-run] {key}: {cmd}")
            return True
        self.say(f"{key}: {cmd}")
        return subprocess.run(cmd, shell=True, cwd=self.root).returncode == 0

    def mutate(self, desc, fn):
        if self.dry:
            self.say(f"[dry-run] {desc}")
        else:
            fn()

    def version(self):
        f = self.root / self.cfg["version_files"][0]
        m = SEMVER.search(f.read_text())
        if not m:
            raise Usage(f"no X.Y.Z version in {f}")
        return m.group()

    def tag_exists(self, tag):
        return bool(git("tag", "-l", tag))

    def rcs(self, ver):
        tags = git("tag", "-l", f"v{ver}-rc.*").split()
        return sorted(
            int(t.rsplit(".", 1)[1])
            for t in tags
            if re.fullmatch(rf"v{re.escape(ver)}-rc\.\d+", t)
        )

    def head_tags(self):
        return git("tag", "--points-at", "HEAD").split()

    def require_clean(self, verb):
        if git("status", "--porcelain"):
            raise Gate(f"{verb}: working tree not clean")

    def unreleased(self):
        """Bullet lines under '## Unreleased', or None when no changelog is configured."""
        if not self.cfg["changelog"]:
            return None
        p = self.root / self.cfg["changelog"]
        if not p.exists():
            raise Gate(f"{p.name} is missing")
        lines, inside = [], False
        for line in p.read_text().splitlines():
            if line.startswith("## "):
                inside = line.strip().lower() == "## unreleased"
            elif inside and line.lstrip().startswith(("- ", "* ")):
                lines.append(line.strip())
        return lines

    def require_unreleased(self, verb):
        u = self.unreleased()
        if u is not None and not u:
            raise Gate(
                f"{verb}: '## Unreleased' in {self.cfg['changelog']} is empty; say what changed for users first"
            )

    def require_files(self, verb, ver):
        missing = [
            f.format(version=ver)
            for f in self.cfg["require_files"]
            if not (self.root / f.format(version=ver)).exists()
        ]
        if missing:
            raise Gate(f"{verb}: missing {missing}")

    @staticmethod
    def next_version(old, kind):
        a, b, c = map(int, old.split("."))
        return {
            "major": f"{a + 1}.0.0",
            "minor": f"{a}.{b + 1}.0",
            "patch": f"{a}.{b}.{c + 1}",
        }[kind]

    def bump(self, old, new):
        for name in self.cfg["version_files"]:
            p = self.root / name
            text = p.read_text()
            if old not in text:
                raise Usage(
                    f"{name} does not contain {old}; version files have drifted"
                )
            # ponytail: first occurrence only, so history lines mentioning the old version survive
            self.mutate(
                f"{name}: {old} -> {new}",
                lambda p=p, t=text: p.write_text(t.replace(old, new, 1)),
            )
        return new

    def restore_versions(self):
        if not self.dry:
            git("checkout", "--", *self.cfg["version_files"])

    def accept_or_restore(self, verb, ver, bumped):
        ok = (
            not self.cfg["version_check"] or self.sh("version_check", version=ver)
        ) and self.sh("accept", version=ver, tag=f"v{ver}")
        if not ok:
            if bumped:
                self.restore_versions()
            raise Gate(
                f"{verb}: acceptance failed on v{ver}; "
                + ("version files restored, " if bumped else "")
                + "nothing tagged"
            )

    def commit_and_tag(self, msg, tag, paths):
        def do():
            if paths:
                git("add", *paths)
                git("commit", "-q", "-m", msg)
            git("tag", "-a", tag, "-m", msg)

        self.mutate(f"commit '{msg}', tag {tag}", do)

    # --- verbs ---------------------------------------------------------
    def status(self):
        ver = self.version()
        last = git("describe", "--tags", "--abbrev=0", check=False) or None
        since = (
            git("rev-list", "--count", f"{last}..HEAD")
            if last
            else git("rev-list", "--count", "HEAD")
        )
        uat = self.uat_items()
        return {
            "version": ver,
            "released": self.tag_exists(f"v{ver}"),
            "rcs": [f"v{ver}-rc.{n}" for n in self.rcs(ver)],
            "branch": git("rev-parse", "--abbrev-ref", "HEAD"),
            "clean": not git("status", "--porcelain"),
            "head_tags": self.head_tags(),
            "last_tag": last,
            "commits_since_last_tag": int(since),
            "unreleased": self.unreleased(),
            "uat_blocking": [i["id"] for i in uat if i["blocking"]]
            if uat is not None
            else None,
        }

    def check(self):
        if not self.sh("check"):
            raise Gate("check failed")

    def rc(self, kind):
        branch = git("rev-parse", "--abbrev-ref", "HEAD")
        if branch == self.cfg["main_branch"]:
            raise Gate(f"rc: on {branch}; cut candidates on a branch, then merge --no-ff")
        self.require_clean("rc")
        self.require_unreleased("rc")
        cur = self.version()
        bumped = self.tag_exists(
            f"v{cur}"
        )  # current version shipped: this is a new version
        if (
            not bumped
            and (n := self.rcs(cur))
            and f"v{cur}-rc.{n[-1]}" in self.head_tags()
        ):
            raise Gate(f"rc: HEAD is already v{cur}-rc.{n[-1]}; commit a fix first")
        self.check()
        ver = self.next_version(cur, kind) if bumped else cur
        self.require_files("rc", ver)
        if bumped:
            self.bump(cur, ver)
        n = (self.rcs(ver) or [0])[-1] + 1
        tag = f"v{ver}-rc.{n}"
        self.accept_or_restore("rc", ver, bumped)
        self.commit_and_tag(
            f"RC {tag}", tag, self.cfg["version_files"] if bumped else []
        )
        self.say(
            f"tagged {tag}. Next: push the branch and tag, then deploy --channel staging"
        )

    def uat_items(self):
        p = self.root / self.cfg["uat_log"].format(version=self.version())
        if not p.exists():
            return None
        rows = [
            [c.strip() for c in ln.strip().strip("|").split("|")]
            for ln in p.read_text().splitlines()
            if ln.strip().startswith("|")
        ]
        if not rows:
            return []
        head, items = [h.lower() for h in rows[0]], []
        try:
            si, st = head.index("severity"), head.index("status")
        except ValueError:
            raise Usage(f"{p.name}: table needs 'severity' and 'status' columns")
        for r in rows[1:]:
            if set("".join(r)) <= set("-: ") or len(r) <= max(si, st):
                continue  # separator or short row
            sev, status = r[si].lower(), r[st].lower()
            if sev not in SEVERITIES or status not in STATUSES:
                raise Usage(
                    f"{p.name}: {r[0]} has severity '{sev}', status '{status}'; "
                    f"use {'|'.join(SEVERITIES)} and {'|'.join(STATUSES)}"
                )
            # ponytail: deferring is for majors only; a blocker blocks until fixed
            blocking = (sev == "blocker" and status != "fixed") or (
                sev == "major" and status == "open"
            )
            items.append(
                {"id": r[0], "severity": sev, "status": status, "blocking": blocking}
            )
        return items

    def uat(self):
        items = self.uat_items()
        if items is None:
            raise Gate(f"uat: no log at {self.cfg['uat_log']}")
        bad = [i for i in items if i["blocking"]]
        if bad:
            raise Gate(
                "uat: blocking "
                + ", ".join(f"{i['id']} ({i['severity']}, {i['status']})" for i in bad)
            )
        self.say(f"uat: ok ({len(items)} items, none blocking)")

    def release(self, kind):
        branch = git("rev-parse", "--abbrev-ref", "HEAD")
        if branch != self.cfg["main_branch"]:
            raise Gate(
                f"release: on {branch}; merge --no-ff to {self.cfg['main_branch']} first"
            )
        self.require_clean("release")
        self.require_unreleased("release")
        cur = self.version()
        bumped = False
        if self.tag_exists(f"v{cur}"):  # no candidate: legacy one-step release
            self.check()
            ver, bumped = self.next_version(cur, kind), True
        else:
            ver = cur
            if n := self.rcs(ver):
                rc = f"v{ver}-rc.{n[-1]}"
                self.uat()
                # the UAT log records testing of this rc, so it may change after it
                log = self.cfg["uat_log"].format(version=ver)
                diff = ["git", "diff", "--quiet", rc, "HEAD", "--", ".", f":(exclude){log}"]
                if subprocess.run(diff).returncode:
                    raise Gate(
                        f"release: HEAD differs from {rc}; cut a new rc and test it"
                    )
            else:
                self.check()
                self.say(f"release: no rc for v{ver}; releasing VERSION as written (--bump ignored)")
        self.require_files("release", ver)
        if bumped:
            self.bump(cur, ver)
        tag = f"v{ver}"
        self.accept_or_restore("release", ver, bumped)
        paths = list(self.cfg["version_files"]) if bumped else []
        if self.cfg["changelog"]:
            p = self.root / self.cfg["changelog"]
            dated = f"## Unreleased\n\n## {tag} — {datetime.date.today():%Y-%m-%d}"
            self.mutate(
                f"date {p.name}",
                lambda: p.write_text(
                    re.sub(
                        r"^## Unreleased[ \t]*$",
                        dated,
                        p.read_text(),
                        count=1,
                        flags=re.M | re.I,
                    )
                ),
            )
            paths.append(self.cfg["changelog"])
        self.commit_and_tag(f"Release {tag}", tag, paths)
        self.say(
            f"tagged {tag}. Next: push {self.cfg['main_branch']} and the tag, then deploy --channel production"
        )

    def deploy(self, channel):
        self.require_clean("deploy")
        tags = self.head_tags()
        want = r"v\d+\.\d+\.\d+-rc\.\d+" if channel == "staging" else r"v\d+\.\d+\.\d+"
        tag = next((t for t in tags if re.fullmatch(want, t)), None)
        if not tag:
            kind = (
                "an rc tag (run rc)"
                if channel == "staging"
                else "a release tag (run release)"
            )
            raise Gate(
                f"deploy: {channel} needs {kind} on HEAD; HEAD has {tags or 'none'}"
            )
        ver = SEMVER.search(tag).group()
        if not self.sh(f"deploy_{channel}", version=ver, tag=tag, channel=channel):
            raise Gate(f"deploy: {channel} command failed")
        if not self.cfg["deploy_verify"]:
            self.say("deploy: deploy_verify not configured; confirm the live version by hand")
        elif not self.sh("deploy_verify", version=ver, tag=tag, channel=channel):
            raise Gate(f"deploy: {channel} is not reporting {ver}; roll back to the previous tag")


def main(argv=None):
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument(
        "verb", choices=["status", "check", "rc", "uat", "release", "deploy"]
    )
    ap.add_argument("--bump", choices=["patch", "minor", "major"], default="patch")
    ap.add_argument("--channel", choices=["staging", "production"])
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    try:
        root = Path(git("rev-parse", "--show-toplevel"))
        os.chdir(root)  # git() and sh() then agree on the repo, wherever we were called
        lane = Lane(root, load_config(root), a.dry_run)
        if a.verb == "status":
            print(json.dumps(lane.status(), indent=2))
        elif a.verb == "deploy":
            if not a.channel:
                raise Usage("deploy needs --channel staging|production")
            lane.deploy(a.channel)
        elif a.verb in ("rc", "release"):
            getattr(lane, a.verb)(a.bump)
        else:
            getattr(lane, a.verb)()
    except Gate as e:
        print(e, file=sys.stderr)
        return 1
    except Usage as e:
        print(e, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
