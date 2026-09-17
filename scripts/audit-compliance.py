#!/usr/bin/env python3
"""Say whether a folder uses the canonical library the way the model says.

    audit-compliance.py [--json] [--library ~/.ailib] <folder> [<folder>...]

Per folder it checks:
  - .aai/instructions.md exists (an ambient folder without it is inert)
  - AGENTS.md, CLAUDE.md, GEMINI.md exist and reach .aai/ (directly or via a
    redirect to AGENTS.md) — the harness auto-loads one of these, never .aai/
  - .aai/instructions.md names the lookup order (.aai/skills → .ailib → ~/.ailib)
  - .ailib/, if present, has manifest.yaml naming every vendored capability
  - every local copy of a catalogued skill (.aai/skills/<name>/, .ailib/<name>/)
    compared file-by-file to the library's:
      identical        every file matches
      library-superset every local file matches, the library has more
      diverged         at least one local file differs or is not in the library
    A vendored (.ailib) copy that is not identical is a defect; a fork in
    .aai/skills that diverged is a fork, reported so it can be reconciled.

Verdicts: COMPLIANT · MINOR (missing GEMINI.md or lookup paragraph) ·
NON-COMPLIANT (no instructions.md, no pointer reaches .aai, .ailib without a
manifest, or a vendored copy that is not pristine). Exit 1 if any folder is
NON-COMPLIANT, 0 otherwise. Text output by default; --json for tooling.
"""

import hashlib
import json
import os
import re
import sys

LOOKUP_RE = re.compile(r"\.aai/skills.*\.ailib.*~/\.ailib", re.S)


def read(p):
    try:
        return open(p, encoding="utf-8", errors="replace").read()
    except OSError:
        return ""


def file_hashes(root):
    """{relative path: sha1} for every file under root; skips .DS_Store and .git."""
    out = {}
    for d, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if x != ".git"]
        for f in files:
            if f == ".DS_Store":
                continue
            p = os.path.join(d, f)
            out[os.path.relpath(p, root)] = hashlib.sha1(
                open(p, "rb").read()
            ).hexdigest()
    return out


def compare(local, lib):
    a, b = file_hashes(local), file_hashes(lib)
    # files the capability's install.d/post.sh rewrote, listed by the installer
    hook = set(read(os.path.join(local, ".post-install")).split())
    a.pop(".post-install", None)
    differing = sorted(k for k in a if k not in hook and (k not in b or a[k] != b[k]))
    if differing:
        return "diverged", differing
    return ("identical" if a.keys() == b.keys() else "library-superset"), []


def catalog_names(library):
    names = set()
    for line in read(os.path.join(library, "library", "catalog.yaml")).splitlines():
        m = re.match(r"^  ([a-z0-9][a-z0-9-]*): ", line)
        if m:
            names.add(m.group(1))
    return names


def audit(folder, library, catalog):
    r = {"folder": folder, "problems": [], "minor": [], "copies": []}
    aai = os.path.join(folder, ".aai")
    inst = os.path.join(aai, "instructions.md")
    if not os.path.isdir(aai):
        r["problems"].append("no .aai/ — not an ambient folder")
    elif not os.path.isfile(inst):
        r["problems"].append("no .aai/instructions.md")
    elif not LOOKUP_RE.search(read(inst)):
        r["minor"].append(
            "instructions.md does not state the lookup order (.aai/skills → .ailib → ~/.ailib)"
        )

    # pointers: the file the harness auto-loads must reach .aai/
    reaches = {}
    for f in ("AGENTS.md", "CLAUDE.md", "GEMINI.md"):
        t = read(os.path.join(folder, f))
        reaches[f] = bool(t) and (".aai/" in t or "AGENTS.md" in t)
    if not any(reaches.values()):
        r["problems"].append("no AGENTS.md/CLAUDE.md/GEMINI.md reaches .aai/")
    else:
        for f, ok in reaches.items():
            if not ok:
                r["minor"].append(f"{f} missing or does not reach .aai/")

    # vendored copies must be manifested and pristine
    ailib = os.path.join(folder, ".ailib")
    if os.path.isdir(ailib):
        manifest = read(os.path.join(ailib, "manifest.yaml"))
        if not manifest:
            r["problems"].append(".ailib/ without manifest.yaml")
        for name in sorted(os.listdir(ailib)):
            if (
                name.startswith(".")
                or name == "manifest.yaml"
                or not os.path.isdir(os.path.join(ailib, name))
            ):
                continue
            if manifest and not re.search(rf"^{re.escape(name)}:", manifest, re.M):
                r["problems"].append(f".ailib/{name} not in manifest.yaml")
            if name in catalog:
                state, diff = compare(
                    os.path.join(ailib, name), os.path.join(library, "library", name)
                )
                r["copies"].append(
                    {"where": f".ailib/{name}", "state": state, "differing": diff[:20]}
                )
                if state == "diverged":
                    r["problems"].append(
                        f".ailib/{name} is not pristine ({len(diff)} files differ)"
                    )
            else:
                r["copies"].append(
                    {
                        "where": f".ailib/{name}",
                        "state": "not-in-catalog",
                        "differing": [],
                    }
                )

    # forks: reported, not judged
    skills = os.path.join(aai, "skills")
    if os.path.isdir(skills):
        for name in sorted(os.listdir(skills)):
            p = os.path.join(skills, name)
            if name in catalog and os.path.isdir(p):
                state, diff = compare(p, os.path.join(library, "library", name))
                r["copies"].append(
                    {
                        "where": f".aai/skills/{name}",
                        "state": state,
                        "differing": diff[:20],
                    }
                )

    r["verdict"] = (
        "NON-COMPLIANT" if r["problems"] else ("MINOR" if r["minor"] else "COMPLIANT")
    )
    return r


def main(argv):
    as_json, library, folders = False, os.path.expanduser("~/.ailib"), []
    it = iter(argv)
    for a in it:
        if a == "--json":
            as_json = True
        elif a == "--library":
            library = os.path.expanduser(next(it))
        elif a in ("-h", "--help"):
            print(__doc__)
            return 0
        else:
            folders.append(os.path.abspath(os.path.expanduser(a)))
    if not folders:
        folders = [os.getcwd()]
    if not os.path.isfile(os.path.join(library, "library", "catalog.yaml")):
        sys.exit(f"no library at {library} (expected library/catalog.yaml)")
    catalog = catalog_names(library)
    results = [audit(f, library, catalog) for f in folders]
    if as_json:
        print(json.dumps(results, indent=2))
    else:
        for r in results:
            print(f"{r['verdict']:14} {r['folder']}")
            for p in r["problems"]:
                print(f"    ! {p}")
            for m in r["minor"]:
                print(f"    - {m}")
            for c in r["copies"]:
                extra = (
                    f" ({', '.join(c['differing'][:3])}{'…' if len(c['differing']) > 3 else ''})"
                    if c["differing"]
                    else ""
                )
                print(f"    = {c['where']}: {c['state']}{extra}")
    return 1 if any(r["verdict"] == "NON-COMPLIANT" for r in results) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
