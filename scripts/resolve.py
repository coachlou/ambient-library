#!/usr/bin/env python3
"""Resolve which project folder an opted-in skill is working in.

Implements docs/PLAN-personalization-layer.md §3 as code, so an agent never
decides where a project's files live. The build copies this file into each
opted-in skill's scripts/; the skill is the folder above scripts/.

  resolve.py --start <path|name|.> [--current <project_dir>] [--intent setup]
  resolve.py --set project.key=value env.key=value ... [--start ...] [--dry-run]
  resolve.py --init [--multi] [--env key=value ...] [--project name ...] [--dry-run]

Prints one JSON object. Shapes:
  resolved   {"project_dir", "project", "environment_file", "environment",
              "state", "overrides"}  (+ "needs" and "do" if keys are empty)
  ambiguous  {"ask": [names], "can_create": true, "do"}
  new        {"new": true, "project_dir", "write_to", "needs", "do"}

Plain resolution never writes; only --set and --init do. Exit 0 = answered
(including ask/needs), 1 = error (message on stderr).
"""

import argparse
import json
import os
import sys


def die(msg):
    print(f"resolve: {msg}", file=sys.stderr)
    sys.exit(1)


# ponytail: tiny YAML subset (sections, `key: value`, `- item`, # comments) —
# stdlib has no YAML parser and nobody hand-edits these files. Nested values or
# multi-line strings need a real parser: PEP 723 inline deps + `uv run`.
def scalar(v):
    v = v.strip()
    if v.startswith("#"):
        return ""
    if v.startswith('"'):
        return json.loads(v[: v.rindex('"') + 1])
    v = v.split(" #")[0].strip()
    return v.strip("'")


def parse_yaml(text):
    out, section = {}, None
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        body = line.strip()
        if line[0] not in " \t":
            key, _, val = body.partition(":")
            section = key.strip()
            out[section] = scalar(val) if scalar(val) else None
        elif section is None:
            die(f"cannot parse line: {raw!r}")
        elif body.startswith("- "):
            out[section] = (out[section] or []) + [scalar(body[2:])]
        else:
            key, _, val = body.partition(":")
            out[section] = {**(out[section] or {}), key.strip(): scalar(val)}
    return out


def read_yaml(path):
    if not os.path.isfile(path):
        return {}
    with open(path) as f:
        return {k: ("" if v is None else v) for k, v in parse_yaml(f.read()).items()}


def write_yaml(path, values, dry):
    if dry:
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write("# written by resolve.py; change values with `resolve.py --set`\n")
        for k, v in values.items():
            f.write(f"{k}: {json.dumps(v)}\n")


def ups(d, home):
    """d and its ancestors: stops below ~, or after the volume root."""
    d = os.path.realpath(d)
    while d != home:
        yield d
        if os.path.ismount(d) or os.path.dirname(d) == d:
            return
        d = os.path.dirname(d)


class Skill:
    def __init__(self, skill_dir):
        self.name = os.path.basename(skill_dir)
        contract = os.path.join(skill_dir, "contract.yaml")
        if not os.path.isfile(contract):
            die(f"{contract} not found — this skill has not opted in")
        with open(contract) as f:
            c = parse_yaml(f.read())
        self.multi = c.get("multi") == "true"
        self.env_keys = list(c.get("environment") or {})
        self.project_keys = list(c.get("project") or {})
        self.state = c.get("state") or []
        self.home = os.path.realpath(os.path.expanduser("~"))
        self.P = os.path.join(".aai", "skills", self.name)

    def p(self, folder, leaf):
        return os.path.join(folder, self.P, leaf)

    def project_at_or_above(self, d):
        return next(
            (a for a in ups(d, self.home) if os.path.isfile(self.p(a, "project.yaml"))),
            None,
        )

    def child_projects(self, d):
        return sorted(
            e.name
            for e in os.scandir(d)
            if e.is_dir() and os.path.isfile(self.p(e.path, "project.yaml"))
        )

    def is_receiving(self, d):
        return os.path.isfile(self.p(d, "environment.yaml")) or os.path.isdir(
            os.path.join(d, ".ailib", self.name)
        )

    def environment_file(self, project_dir):
        """Nearest existing file; else where a new one is saved (never inside .ailib/)."""
        for a in ups(project_dir, self.home):
            if os.path.isfile(self.p(a, "environment.yaml")):
                return self.p(a, "environment.yaml")
        home_file = self.p(self.home, "environment.yaml")
        if os.path.isfile(home_file):
            return home_file
        for a in ups(project_dir, self.home):
            if os.path.isdir(os.path.join(a, ".ailib", self.name)):
                return self.p(a, "environment.yaml")
        return home_file

    def new(self, folder):
        return {
            "new": True,
            "project_dir": folder,
            "write_to": self.p(folder, "project.yaml"),
            "needs": [f"project.{k}" for k in self.project_keys],
            "do": f"Confirm with the user: set up {folder} as a {self.name} project? "
            "Declined: stop. Accepted: ask the needs, then run --set with them "
            "and --intent setup (with no needs, run --set alone).",
        }

    def ask(self, names, missing=None):
        what = f"No folder named {missing!r}. " if missing else ""
        return {
            "ask": names,
            "can_create": True,
            "do": what + "Ask the user which project, or whether to create a new one. "
            "Do not pick one and do not fall back to the current folder.",
        }

    def resolve(self, start, current, setup):
        cwd = os.path.realpath(os.getcwd())
        current = (
            os.path.realpath(current) if current else self.project_at_or_above(cwd)
        )
        named = start not in ("", ".")
        if named:
            start = os.path.expanduser(start)
            sibling = (
                os.path.join(os.path.dirname(current), start)
                if current and os.sep not in start
                else None
            )
            tries = [os.path.join(cwd, start)] + ([sibling] if sibling else [])
            folder = next(
                (os.path.realpath(t) for t in tries if os.path.isdir(t)), None
            )
            if folder is None:
                if not setup:
                    names = self.child_projects(cwd)
                    if current:
                        names = sorted(
                            set(names + self.child_projects(os.path.dirname(current)))
                        )
                    return self.ask(names, missing=start)
                # inside a project, a new one goes beside it, not within it
                return self.new(
                    os.path.realpath(
                        sibling
                        if sibling and self.project_at_or_above(cwd)
                        else tries[0]
                    )
                )
        else:
            folder = cwd

        project_dir = self.project_at_or_above(folder)
        if project_dir is None:
            if named:  # exists but is not a project: never fall back to cwd
                return self.new(folder)
            if self.multi and self.is_receiving(cwd):
                names = self.child_projects(cwd)
                if len(names) == 1 and not setup:
                    project_dir = os.path.join(cwd, names[0])
                else:
                    return self.ask(names)
            else:
                return self.new(cwd)

        env_file = self.environment_file(project_dir)
        project, env = (
            read_yaml(self.p(project_dir, "project.yaml")),
            read_yaml(env_file),
        )
        for s in self.state:
            if os.path.isabs(s) or ".." in s.split("/"):
                die(f"state path escapes the project: {s}")
        overrides = self.p(project_dir, "overrides.md")
        out = {
            "project_dir": project_dir,
            "project": project,
            "environment_file": env_file,
            "environment": env,
            "state": [os.path.join(project_dir, s) for s in self.state],
            "overrides": overrides if os.path.isfile(overrides) else None,
        }
        needs = [f"project.{k}" for k in self.project_keys if not project.get(k)] + [
            f"env.{k}" for k in self.env_keys if not env.get(k)
        ]
        if needs:
            out["needs"] = needs
            out["do"] = "Ask the user for the needs once, then save them with --set."
        return out


def pairs(items, allowed):
    out = {}
    for item in items:
        key, eq, val = item.partition("=")
        if not eq or key not in allowed:
            die(
                f"bad assignment {item!r}; allowed keys: {', '.join(sorted(allowed)) or 'none'}"
            )
        out[key] = val
    return out


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument(
        "--start",
        default=".",
        help="path or folder name the request gives; default: current folder",
    )
    ap.add_argument(
        "--current",
        help="project_dir from the previous resolution, once a project is open",
    )
    ap.add_argument(
        "--intent", choices=["setup"], help="the request is to set up a new project"
    )
    ap.add_argument(
        "--set",
        nargs="*",
        metavar="CLASS.KEY=VALUE",
        help="save values (project.* / env.*), then resolve",
    )
    ap.add_argument(
        "--init",
        action="store_true",
        help="stamp the layout in the current folder (install time)",
    )
    ap.add_argument(
        "--multi", action="store_true", help="with --init: stamp a multi-project parent"
    )
    ap.add_argument(
        "--env",
        nargs="*",
        default=[],
        metavar="KEY=VALUE",
        help="with --init: environment values",
    )
    ap.add_argument(
        "--project",
        nargs="*",
        default=[],
        metavar="NAME",
        help="with --init --multi: project folders",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="with --set/--init: report, write nothing",
    )
    ap.add_argument(
        "--skill-dir",
        default=os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
        help="folder holding contract.yaml; default: the folder above scripts/",
    )
    a = ap.parse_args()
    sk, dry = Skill(os.path.realpath(a.skill_dir)), a.dry_run
    cwd = os.path.realpath(os.getcwd())

    if a.init:
        if a.multi and not sk.multi:
            die(
                f"{sk.name} is not a multi-project skill (no `multi: true` in contract.yaml)"
            )
        if a.project and not a.multi:
            die("--project needs --multi; a single-project folder is its own project")
        projects = [os.path.join(cwd, n) for n in a.project] if a.multi else [cwd]
        for d in projects:
            f = sk.p(d, "project.yaml")
            write_yaml(f, read_yaml(f), dry)  # marker; existing values kept
        env_file = (
            sk.p(cwd, "environment.yaml") if a.multi else sk.environment_file(cwd)
        )
        values = {**read_yaml(env_file), **pairs(a.env, sk.env_keys)}
        if values or a.multi:
            write_yaml(env_file, values, dry)
        print(
            json.dumps(
                {"initialized": projects, "environment_file": env_file, "dry_run": dry},
                indent=2,
            )
        )
        return

    out = sk.resolve(a.start, a.current, a.intent == "setup")
    if a.set is not None:
        if "ask" in out:
            die("cannot save: the project is ambiguous — resolve it first with --start")
        if out.get("new") and a.intent != "setup":
            die(
                f"{out['project_dir']} is not a {sk.name} project yet; confirm with the user, then add --intent setup"
            )
        new = pairs(
            a.set,
            [f"project.{k}" for k in sk.project_keys]
            + [f"env.{k}" for k in sk.env_keys],
        )
        project_file = sk.p(out["project_dir"], "project.yaml")
        proj = {k[8:]: v for k, v in new.items() if k.startswith("project.")}
        env = {k[4:]: v for k, v in new.items() if k.startswith("env.")}
        if proj or out.get("new"):
            write_yaml(project_file, {**read_yaml(project_file), **proj}, dry)
        if env:
            env_file = sk.environment_file(out["project_dir"])
            write_yaml(env_file, {**read_yaml(env_file), **env}, dry)
        if dry:
            out = {
                "dry_run": True,
                "would_write": {"project": proj, "env": env},
                "project_dir": out["project_dir"],
            }
        else:
            out = sk.resolve(out["project_dir"], None, False)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
