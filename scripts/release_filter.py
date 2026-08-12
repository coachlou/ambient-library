#!/usr/bin/env python3
"""Assemble the production tree from a clean export of HEAD.

Called by build-production.sh. Takes an exported source tree and produces a
staging tree containing only released skills and no authoring machinery.

    release_filter.py <src> <stage> <sha> <dev-root>

Exits 3 on any manifest error — a skill named in RELEASE.yaml that does not
exist, or exists but is not in the catalog. Failing closed is the whole point:
production should be impossible to fill by accident.
"""

import json
import os
import re
import shutil
import sys

src, stage, sha, dev_root = sys.argv[1:5]

# --- read the manifest (flat "skills:" list — no yaml dependency) ---------
released, in_list = [], False
for line in open(os.path.join(src, "RELEASE.yaml")):
    if re.match(r"^skills:\s*$", line):
        in_list = True
        continue
    if in_list:
        m = re.match(r"^\s*-\s*([a-z0-9][a-z0-9-]*)\s*$", line)
        if m:
            released.append(m.group(1))
        elif line.strip() and not line.lstrip().startswith("#"):
            in_list = False
released = sorted(set(released))
if not released:
    sys.exit("RELEASE.yaml lists no skills — refusing to build an empty library")

# --- catalog is the contract: released ⊆ catalogued ⊆ on disk -------------
catalog_path = os.path.join(src, "library", "catalog.yaml")
catalog = {}
for line in open(catalog_path):
    m = re.match(r"^  ([a-z0-9][a-z0-9-]*): (.*)$", line.rstrip("\n"))
    if m:
        catalog[m.group(1)] = m.group(2)

missing = [s for s in released if not os.path.isdir(os.path.join(src, "library", s))]
uncatalogued = [s for s in released if s not in catalog]
if missing:
    sys.exit(f"RELEASE.yaml names skills that do not exist: {', '.join(missing)}")
if uncatalogued:
    sys.exit(
        f"RELEASE.yaml names skills missing from catalog.yaml: {', '.join(uncatalogued)}"
    )

# --- what production needs to install and vend ---------------------------
KEEP_FILES = ["README.md", "SKILLS.md", "ARCHITECTURE.md", "AGENTS.md", "CLAUDE.md"]
KEEP_DIRS = [
    ".claude-plugin",
    ".codex-plugin",
    "skills",
    "codex-skills",
    "templates",
    "bundles",
]
# docs/ is mixed: consumer guides ship, maintainer and planning notes do not.
DROP_DOCS = ["MANAGEMENT.md", "DEFERRED-IDEAS.md"]
# Authoring only — production cannot create, propose, or promote a skill.
DROP_SUBSKILLS = ["admin.md", "propose.md"]

os.makedirs(stage, exist_ok=True)
for f in KEEP_FILES:
    p = os.path.join(src, f)
    if os.path.exists(p):
        shutil.copy2(p, os.path.join(stage, f))
for d in KEEP_DIRS:
    p = os.path.join(src, d)
    if os.path.isdir(p):
        shutil.copytree(p, os.path.join(stage, d), symlinks=True)

# docs/ — consumer guides only
os.makedirs(os.path.join(stage, "docs"))
for f in sorted(os.listdir(os.path.join(src, "docs"))):
    if f in DROP_DOCS or f.startswith("PLAN-"):
        continue
    shutil.copy2(os.path.join(src, "docs", f), os.path.join(stage, "docs", f))

# library/README.md explains what the directory is — it ships with it
# .aai/ minus the authoring subskills
shutil.copytree(os.path.join(src, ".aai"), os.path.join(stage, ".aai"), symlinks=True)
for f in DROP_SUBSKILLS:
    p = os.path.join(stage, ".aai", "skills", f)
    if os.path.exists(p):
        os.remove(p)

# released skills only
os.makedirs(os.path.join(stage, "library"))
lr = os.path.join(src, "library", "README.md")
if os.path.exists(lr):
    shutil.copy2(lr, os.path.join(stage, "library", "README.md"))
for s in released:
    shutil.copytree(
        os.path.join(src, "library", s),
        os.path.join(stage, "library", s),
        symlinks=True,
    )

# --- rewrite the derived indexes to match what actually shipped ----------
with open(os.path.join(stage, "library", "catalog.yaml"), "w") as fh:
    for line in open(catalog_path):
        m = re.match(r"^  ([a-z0-9][a-z0-9-]*): ", line)
        if m and m.group(1) not in released:
            continue
        fh.write(line)

mp = os.path.join(stage, ".claude-plugin", "marketplace.json")
if os.path.exists(mp):
    m = json.load(open(mp))
    m["plugins"] = [
        p for p in m["plugins"] if p["name"] == "ambient" or p["name"] in released
    ]
    json.dump(m, open(mp, "w"), indent=2)
    open(mp, "a").write("\n")

# SKILLS.md table rows for unreleased skills would advertise what isn't there
sk = os.path.join(stage, "SKILLS.md")
if os.path.exists(sk):
    out = []
    for line in open(sk):
        m = re.match(r"^\| \*\*([a-z0-9][a-z0-9-]*)\*\* \|", line)
        if m and m.group(1) not in released:
            continue
        out.append(line)
    open(sk, "w").writelines(out)

# --- routing rows for subskills that no longer exist ---------------------
inst = os.path.join(stage, ".aai", "instructions.md")
s = open(inst).read()
s = "\n".join(
    row
    for row in s.split("\n")
    if not any(
        f"`.aai/skills/{d}`" in row and row.startswith("|") for d in DROP_SUBSKILLS
    )
)
open(inst, "w").write(s)

# a bundle symlinking an unreleased skill would dangle in production
bdir = os.path.join(stage, "bundles")
for b in sorted(os.listdir(bdir)) if os.path.isdir(bdir) else []:
    sk = os.path.join(bdir, b, "skills")
    if not os.path.isdir(sk):
        continue
    dangling = [x for x in os.listdir(sk) if x not in released]
    if dangling:
        shutil.rmtree(os.path.join(bdir, b))
        print(f"  dropped bundle {b}: unreleased members {', '.join(sorted(dangling))}")

# --- provenance ----------------------------------------------------------
open(os.path.join(stage, ".aai", "PRODUCTION"), "w").write(f"""\
# Production build — do not edit, do not author here.

Built from ambient-library@{sha} by scripts/build-production.sh.
Contents are whatever RELEASE.yaml named at that commit: {len(released)} skills.

This folder is a build output, not a git clone. Editing it changes nothing
upstream and is overwritten by the next build. admin.md and propose.md are not
present — authoring happens in the dev workspace:

  {dev_root}

To release a skill: add its name to RELEASE.yaml there, then re-run
scripts/build-production.sh.
""")

print(f"staged {len(released)} skills")
