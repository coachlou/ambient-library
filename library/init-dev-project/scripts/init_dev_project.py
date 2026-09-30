#!/usr/bin/env python3
"""Scaffold a folder into the dev-and-deploy standard and make it a git repo.

Creates root files, Makefile and .aai/ from templates/project/. Never overwrites:
existing files are skipped, so re-running is safe. If the folder has no .git,
runs `git init -b main`, commits the scaffold and tags v0.0.0. Never adds a
remote, never pushes.

Exit codes: 0 ok, 1 bad arguments or template missing, 2 git failed.
"""
import argparse, datetime, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
TEMPLATES = os.path.join(SKILL, "templates", "project")
STANDARD = os.path.join(SKILL, "references", "standard.md")


def skill_version():
    with open(os.path.join(SKILL, "VERSION")) as f:
        return f.read().strip()


def render(text, values):
    for k, v in values.items():
        text = text.replace("{{" + k + "}}", v)
    return text


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", nargs="?", default=".", help="target folder (created if missing); default: current folder")
    ap.add_argument("--name", help="project name; default: folder basename")
    ap.add_argument("--kind", default="project", help="skill | tool | skill-app | web | anything; default: project")
    ap.add_argument("--description", help="one sentence; default: 'A <kind> project.'")
    ap.add_argument("--no-git", action="store_true", help="skip git init/commit/tag")
    ap.add_argument("--dry-run", action="store_true", help="print what would be created, write nothing")
    ap.add_argument("--json", action="store_true", help="machine-readable summary on stdout")
    a = ap.parse_args()

    if not os.path.isdir(TEMPLATES) or not os.path.isfile(STANDARD):
        print(f"template or standard missing under {SKILL}", file=sys.stderr)
        return 1
    root = os.path.abspath(a.path)
    name = a.name or os.path.basename(root)
    values = {
        "name": name,
        "kind": a.kind,
        "description": a.description or f"A {a.kind} project.",
        "date": datetime.date.today().isoformat(),
        "skill_version": skill_version(),
    }

    # (relative path, rendered content)
    files = []
    for d, _, fs in os.walk(TEMPLATES):
        for fn in fs:
            src = os.path.join(d, fn)
            rel = os.path.relpath(src, TEMPLATES)
            with open(src) as f:
                files.append((rel, render(f.read(), values)))
    with open(STANDARD) as f:
        std = f.read()
    stamp = f"<!-- init-dev-project v{values['skill_version']} · stamped {values['date']} · canonical: references/standard.md in the init-dev-project skill -->\n"
    files.append((os.path.join(".aai", "references", "dev-standard.md"), stamp + std))

    created, skipped = [], []
    for rel, content in sorted(files):
        dst = os.path.join(root, rel)
        if os.path.exists(dst):
            skipped.append(rel)
            continue
        created.append(rel)
        if not a.dry_run:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            with open(dst, "w") as f:
                f.write(content)

    git = "skipped"
    had_git = os.path.isdir(os.path.join(root, ".git"))
    if not a.no_git and not a.dry_run and not had_git:
        def run(*cmd):
            return subprocess.run(cmd, cwd=root, check=True, capture_output=True, text=True)
        try:
            run("git", "init", "-q", "-b", "main")
            run("git", "add", "-A")
            run("git", "commit", "-q", "-m", f"Scaffold {name} with init-dev-project v{values['skill_version']}")
            run("git", "tag", "v0.0.0")
            git = "initialized: main, 1 commit, tag v0.0.0"
        except subprocess.CalledProcessError as e:
            print(e.stderr, file=sys.stderr)
            return 2
    elif had_git:
        git = "existing repo left untouched"
    elif a.dry_run:
        git = "would initialize" if not had_git else "existing repo"

    summary = {"path": root, "name": name, "kind": a.kind, "dry_run": a.dry_run,
               "created": created, "skipped": skipped, "git": git}
    if a.json:
        print(json.dumps(summary, indent=2))
    else:
        verb = "would create" if a.dry_run else "created"
        print(f"{name} ({a.kind}) at {root}")
        print(f"  {verb}: {len(created)}  skipped (exists): {len(skipped)}  git: {git}")
        for r in created:
            print(f"  + {r}")
        print("  next: cd there and run `make`")
    return 0


if __name__ == "__main__":
    sys.exit(main())
