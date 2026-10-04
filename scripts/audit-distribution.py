#!/usr/bin/env python3
"""Cross-check distribution consistency across the library's four sources of truth.

A domain skill is routable when it is in library/catalog.yaml, and distributable
when it also has SKILL.md, .claude-plugin/plugin.json, and a marketplace.json
entry. Skills drift out of that agreement silently, because nothing until now
checked it. This does — deterministic set arithmetic, no judgment calls.

  catalog.yaml                       -> routing (what the router can pick)
  library/<n>/SKILL.md               -> standalone skill frontmatter
  library/<n>/.claude-plugin/*.json  -> standalone plugin manifest + version
  .claude-plugin/marketplace.json    -> installable plugin catalog

A skill that opted in to project values (contract.yaml) is also held to its
contract: see check_contract. Shared assets are held to admin.md's three rules:
see check_shared.

Usage:  scripts/audit-distribution.py [--quiet | --self-test | --sync-shared]

Exit codes:
  0  no drift (warnings may still be printed)
  1  drift found
  2  a source file is missing or unparseable
"""

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

# Repo root is this script's parent directory.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG = os.path.join(ROOT, "library", "catalog.yaml")
MARKETPLACE = os.path.join(ROOT, ".claude-plugin", "marketplace.json")

# ponytail: regex, not pyyaml — catalog.yaml's format is a hard one-line-per-skill
# contract stated in its own header, and a stdlib-only script needs no install step.
CATALOG_LINE = re.compile(r"^  ([a-z0-9][a-z0-9-]*): (.+?)\s*$")
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---", re.S)
FM_FIELD = re.compile(r"^(name|description): (.+?)\s*$", re.M)

# SKILL.md descriptions verified as deliberate tuning of their catalog line. Each is
# pinned to a hash of both texts, so editing either one brings the warning back.
# To record one, copy the hash its warning prints.
TUNED_DESCRIPTIONS = {
    "capture-chat": "e6d216948e17",  # names harnesses, vault phrasings, both modes
    "chat-n-build": "3f7ee5193e45",  # more trigger examples + not-for negatives
    "checkpoint": "e6ab8abb1f5a",  # spells out both modes and their triggers
    "publish-article": "baaa9cf9f2b4",  # adds aimmhub + writing-skill handoff triggers
}


def pair_hash(catalog_desc, skill_desc):
    return hashlib.sha256(f"{catalog_desc}\0{skill_desc}".encode()).hexdigest()[:12]


def die(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(2)


def load_catalog():
    """-> {name: description}. Only lines inside the `skills:` mapping count."""
    if not os.path.exists(CATALOG):
        die(f"missing {CATALOG}")
    entries, in_skills = {}, False
    for line in open(CATALOG, encoding="utf-8"):
        if line.startswith("skills:"):
            in_skills = True
            continue
        if not in_skills or line.lstrip().startswith("#"):
            continue
        m = CATALOG_LINE.match(line.rstrip("\n"))
        if m:
            entries[m.group(1)] = m.group(2)
    if not entries:
        die("parsed zero skills from catalog.yaml — format may have changed")
    return entries


def load_marketplace():
    """-> ({name: description} for ./library/* entries, {name: source} for all)."""
    if not os.path.exists(MARKETPLACE):
        die(f"missing {MARKETPLACE}")
    try:
        data = json.load(open(MARKETPLACE, encoding="utf-8"))
    except json.JSONDecodeError as e:
        die(f"{MARKETPLACE} is not valid JSON: {e}")
    lib, sources = {}, {}
    for p in data.get("plugins", []):
        name, src = p.get("name"), p.get("source", "")
        sources[name] = src
        if src.startswith("./library/"):
            lib[name] = p.get("description", "")
    return lib, sources


def read_frontmatter(path):
    """-> {name, description} from a SKILL.md, or None if absent/malformed."""
    if not os.path.exists(path):
        return None
    m = FRONTMATTER.match(open(path, encoding="utf-8").read())
    if not m:
        return None
    return {k: v for k, v in FM_FIELD.findall(m.group(1))}


def read_plugin_json(path):
    if not os.path.exists(path):
        return None
    try:
        return json.load(open(path, encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


PLACEHOLDER = re.compile(r"\{\{(env|project)\.([A-Za-z0-9_]+)\}\}")
SECTION = {"env": "environment", "project": "project"}


def check_contract(skill_dir):
    """-> [problems] for a skill that opted in with contract.yaml
    (docs/PLAN-personalization-layer.md §6)."""
    sys.dont_write_bytecode = True  # no scripts/__pycache__ left in the repo
    from resolve import parse_yaml  # same folder; one parser for one format

    contract = parse_yaml(open(os.path.join(skill_dir, "contract.yaml")).read())
    problems = []
    for sec in SECTION.values():
        filled = [k for k, v in (contract.get(sec) or {}).items() if v]
        if filled:
            problems.append(
                f"contract.yaml ships values for {', '.join(filled)} — canonical stays empty"
            )

    body = next(
        (
            f
            for f in ("instructions.md", "SKILL.md")
            if os.path.exists(os.path.join(skill_dir, f))
        ),
        None,
    )
    if (
        not body
        or "scripts/resolve.py --start"
        not in open(os.path.join(skill_dir, body)).read()
    ):
        problems.append(
            f"{body or 'body file'} does not open with the Project block (no `scripts/resolve.py --start`)"
        )

    copy = os.path.join(skill_dir, "scripts", "resolve.py")
    source = os.path.join(ROOT, "scripts", "resolve.py")
    if os.path.exists(copy) and open(copy).read() != open(source).read():
        problems.append(
            "scripts/resolve.py differs from the repo's scripts/resolve.py — the build copies it; delete the hand copy"
        )

    for dirpath, _, files in os.walk(skill_dir):
        for f in files:
            path = os.path.join(dirpath, f)
            rel = os.path.relpath(path, skill_dir)
            if rel == os.path.join("scripts", "resolve.py"):
                continue
            try:
                text = open(path, encoding="utf-8").read()
            except (UnicodeDecodeError, OSError):
                continue
            for cls, key in set(PLACEHOLDER.findall(text)):
                if key not in (contract.get(SECTION[cls]) or {}):
                    problems.append(
                        f"{rel}: {{{{{cls}.{key}}}}} is not a key in contract.yaml"
                    )
            for m in sorted(set(re.findall(r"YOUR_[A-Z_]+", text))):
                problems.append(
                    f"{rel}: hand-edit placeholder {m} — use a contract key"
                )
    return problems


MIN_SHARERS = 3  # rule of three: a file is shared only once three skills carry it
NOT_SHAREABLE = {"instructions.md", "SKILL.md"}  # procedure stays per skill


def check_shared(lib_root, skills):
    """-> [problems] for library/_shared/ and the shared/ copies skills carry.

    _shared/ is the dev-only source; it never ships. Each skill vendors what it
    uses into its own shared/, byte-identical, so every install is self-contained.
    """
    src_root = os.path.join(lib_root, "_shared")
    problems, users = [], {}
    for name in sorted(skills):
        skill_dir = os.path.join(lib_root, name)
        sdir = os.path.join(skill_dir, "shared")
        for dirpath, _, files in os.walk(sdir):
            for f in files:
                copy = os.path.join(dirpath, f)
                rel = os.path.relpath(copy, sdir)
                src = os.path.join(src_root, rel)
                users.setdefault(rel, []).append(name)
                if not os.path.exists(src):
                    problems.append(
                        f"{name}: shared/{rel} has no source at library/_shared/{rel}"
                    )
                elif open(copy, "rb").read() != open(src, "rb").read():
                    problems.append(
                        f"{name}: shared/{rel} differs from library/_shared/{rel} — "
                        "edit the source, then audit-distribution.py --sync-shared"
                    )
        for dirpath, _, files in os.walk(skill_dir):
            for f in files:
                try:
                    text = open(os.path.join(dirpath, f), encoding="utf-8").read()
                except (UnicodeDecodeError, OSError):
                    continue
                if "library/_shared" in text:
                    rel = os.path.relpath(os.path.join(dirpath, f), skill_dir)
                    problems.append(
                        f"{name}: {rel} points into library/_shared/, which does not ship — "
                        f"reference ${{CLAUDE_PLUGIN_ROOT}}/library/{name}/shared/<file>"
                    )
    for dirpath, _, files in os.walk(src_root):
        for f in files:
            rel = os.path.relpath(os.path.join(dirpath, f), src_root)
            if f in NOT_SHAREABLE:
                problems.append(
                    f"_shared/{rel}: instructions stay per skill — only context-free assets are shared"
                )
            n = len(users.get(rel, []))
            if n < MIN_SHARERS:
                problems.append(
                    f"_shared/{rel}: carried by {n} skill(s), needs {MIN_SHARERS} — "
                    "move it back into the skill(s) that use it"
                )
    return problems


def sync_shared(lib_root):
    """Refresh every skill's shared/ copy from library/_shared/. -> files rewritten."""
    src_root, n = os.path.join(lib_root, "_shared"), 0
    for name in os.listdir(lib_root):
        sdir = os.path.join(lib_root, name, "shared")
        for dirpath, _, files in os.walk(sdir):
            for f in files:
                copy = os.path.join(dirpath, f)
                src = os.path.join(src_root, os.path.relpath(copy, sdir))
                if (
                    os.path.exists(src)
                    and open(copy, "rb").read() != open(src, "rb").read()
                ):
                    shutil.copy2(src, copy)
                    print(
                        f"  synced library/{name}/shared/{os.path.relpath(copy, sdir)}"
                    )
                    n += 1
    return n


def self_test():
    """The one runnable check for check_contract. Run: audit-distribution.py --self-test"""
    import tempfile

    d = tempfile.mkdtemp()

    def put(name, text):
        with open(os.path.join(d, name), "w") as f:
            f.write(text)

    put(
        "contract.yaml",
        "environment:   # inherited\n  alias:  # hint\nproject:\n  group:\n",
    )
    put(
        "instructions.md",
        "run `scripts/resolve.py --start .`\n{{project.group}} via {{env.alias}}, then {{BODY_HTML}}\n",
    )
    assert check_contract(d) == [], check_contract(d)
    put("contract.yaml", "environment:\n  alias: lou\nproject:\n  group:\n")
    put("instructions.md", "{{project.groop}} {{env.group}} YOUR_GROUP_NAME\n")
    got = check_contract(d)
    assert len(got) == 5, got  # value shipped, no block, two bad keys, one YOUR_
    assert pair_hash("a", "bc") != pair_hash(
        "ab", "c"
    )  # separator keeps the pair unambiguous

    lib = tempfile.mkdtemp()

    def lput(rel, text):
        os.makedirs(os.path.dirname(os.path.join(lib, rel)), exist_ok=True)
        with open(os.path.join(lib, rel), "w") as f:
            f.write(text)

    lput("_shared/ref.md", "v1")
    for s in ("a", "b", "c"):
        lput(f"{s}/shared/ref.md", "v1")
    assert check_shared(lib, "abc") == [], check_shared(lib, "abc")
    lput("_shared/ref.md", "v2")  # source edited, copies stale
    assert len(check_shared(lib, "abc")) == 3
    assert sync_shared(lib) == 3 and check_shared(lib, "abc") == []
    os.remove(os.path.join(lib, "c/shared/ref.md"))  # below the rule of three
    lput("_shared/instructions.md", "x")  # procedure in the pool
    lput("a/instructions.md", "see library/_shared/ref.md")  # won't ship
    got = check_shared(lib, "abc")
    assert len(got) == 4, (
        got
    )  # ref.md 2<3, instructions.md not shareable + 0<3, a's path
    print("self-test passed")


def main():
    if "--self-test" in sys.argv:
        self_test()
        return 0
    if "--sync-shared" in sys.argv:
        n = sync_shared(os.path.join(ROOT, "library"))
        print(f"synced {n} shared file(s) — bump each touched skill's version")
        return 0
    quiet = "--quiet" in sys.argv
    if "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__)
        return 0

    catalog = load_catalog()
    mp_lib, mp_sources = load_marketplace()
    lib_root = os.path.join(ROOT, "library")
    dirs = {
        d
        for d in os.listdir(lib_root)
        if os.path.isdir(os.path.join(lib_root, d)) and not d.startswith("_")
    }

    errors, warnings = [], []

    # --- Routing vs disk ------------------------------------------------
    for name in sorted(set(catalog) - dirs):
        errors.append(f"{name}: in catalog.yaml but library/{name}/ does not exist")

    # Unrouted directories are a judgment call (scratch space, fixtures), so they
    # warn rather than fail — a human decides whether they are skills or cruft.
    for name in sorted(dirs - set(catalog)):
        warnings.append(f"{name}: library/{name}/ exists but is not in catalog.yaml")

    # --- Per-skill distribution artifacts -------------------------------
    for name, desc in sorted(catalog.items()):
        skill_dir = os.path.join(lib_root, name)
        if not os.path.isdir(skill_dir):
            continue  # already reported above

        fm = read_frontmatter(os.path.join(skill_dir, "SKILL.md"))
        if fm is None:
            errors.append(
                f"{name}: missing or malformed library/{name}/SKILL.md frontmatter"
            )
        else:
            if fm.get("name") != name:
                errors.append(
                    f"{name}: SKILL.md frontmatter name is {fm.get('name')!r}, expected {name!r}"
                )
            if not fm.get("description"):
                errors.append(f"{name}: SKILL.md frontmatter has no description")
            elif fm["description"] != desc and TUNED_DESCRIPTIONS.get(
                name
            ) != pair_hash(desc, fm["description"]):
                # Warning, not drift. A SKILL.md description is the live routing
                # trigger for the standalone install, where the skill competes
                # against every other skill the user has — the catalog line only
                # competes against 47 siblings the router already narrowed to.
                # Forcing them equal would silently re-route the standalone skill,
                # which admin.md warns against. Divergence is legitimate; check it.
                warnings.append(
                    f"{name}: SKILL.md description differs from catalog.yaml "
                    "(intentional tuning, or drift — verify; if intentional, add "
                    f"{name!r}: {pair_hash(desc, fm['description'])!r} to TUNED_DESCRIPTIONS)"
                )

        pj = read_plugin_json(os.path.join(skill_dir, ".claude-plugin", "plugin.json"))
        if pj is None:
            errors.append(f"{name}: missing library/{name}/.claude-plugin/plugin.json")
        else:
            if pj.get("name") != name:
                errors.append(
                    f"{name}: plugin.json name is {pj.get('name')!r}, expected {name!r}"
                )
            if not pj.get("version"):
                errors.append(f"{name}: plugin.json has no version")
            if pj.get("description") != desc:
                errors.append(
                    f"{name}: plugin.json description does not match catalog.yaml"
                )

        # Distro contract: templates/aai/ must carry the three stamped files; DEPENDS must resolve.
        tdir = os.path.join(skill_dir, "templates", "aai")
        if os.path.isdir(tdir):
            for t in ("identity.md", "instructions.md", "context.md"):
                if not os.path.exists(os.path.join(tdir, t)):
                    errors.append(f"{name}: distro templates/aai/ is missing {t}")
        dep_file = os.path.join(skill_dir, "DEPENDS")
        if os.path.exists(dep_file):
            for line in open(dep_file, encoding="utf-8"):
                dep = line.split("#", 1)[0].strip()
                if dep and not os.path.isdir(os.path.join(ROOT, "library", dep)):
                    errors.append(
                        f"{name}: DEPENDS names {dep!r}, which is not in library/"
                    )

        if os.path.exists(os.path.join(skill_dir, "contract.yaml")):
            errors += [f"{name}: {p}" for p in check_contract(skill_dir)]

        if name not in mp_lib:
            errors.append(f"{name}: in catalog.yaml but has no marketplace.json entry")
        elif mp_lib[name] != desc:
            errors.append(
                f"{name}: marketplace.json description does not match catalog.yaml"
            )

    # --- Shared assets: per-skill procedure, context-free pool, rule of three
    errors += check_shared(lib_root, [n for n in catalog if n in dirs])

    # --- Marketplace vs routing -----------------------------------------
    for name in sorted(set(mp_lib) - set(catalog)):
        errors.append(
            f"{name}: marketplace.json lists ./library/{name} but it is not in catalog.yaml"
        )

    # --- Every marketplace source must resolve --------------------------
    for name, src in sorted(mp_sources.items()):
        if not os.path.exists(os.path.join(ROOT, src)):
            errors.append(f"{name}: marketplace.json source {src} does not exist")

    # --- Report ----------------------------------------------------------
    # --- team-index freshness (read only by team-build) ----------------
    r = subprocess.run(
        [sys.executable, os.path.join(ROOT, "scripts", "build-team-index.py"), "--check"],
        capture_output=True, text=True,
    )
    if r.returncode:
        errors.append(
            f"team-index.yaml: {(r.stdout or r.stderr).strip()} "
            "(rerun scripts/build-team-index.py)"
        )

    if warnings and not quiet:
        print(f"warnings ({len(warnings)}) — not drift, review when convenient:")
        for w in warnings:
            print(f"  ! {w}")
        print()

    if errors:
        print(f"DRIFT: {len(errors)} issue(s) across {len(catalog)} catalog skills")
        for e in errors:
            print(f"  x {e}")
        print(
            "\nFix per .aai/skills/admin.md — create/update/delete each touch all four files."
        )
        return 1

    if not quiet:
        print(
            f"OK: {len(catalog)} catalog skills agree across "
            "SKILL.md, plugin.json, and marketplace.json"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
