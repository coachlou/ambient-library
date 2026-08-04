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

Usage:  scripts/audit-distribution.py [--quiet]

Exit codes:
  0  no drift (warnings may still be printed)
  1  drift found
  2  a source file is missing or unparseable
"""

import json
import os
import re
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


def main():
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
            elif fm["description"] != desc:
                # Warning, not drift. A SKILL.md description is the live routing
                # trigger for the standalone install, where the skill competes
                # against every other skill the user has — the catalog line only
                # competes against 47 siblings the router already narrowed to.
                # Forcing them equal would silently re-route the standalone skill,
                # which admin.md warns against. Divergence is legitimate; check it.
                warnings.append(
                    f"{name}: SKILL.md description differs from catalog.yaml "
                    "(intentional tuning, or drift — verify)"
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

        if name not in mp_lib:
            errors.append(f"{name}: in catalog.yaml but has no marketplace.json entry")
        elif mp_lib[name] != desc:
            errors.append(
                f"{name}: marketplace.json description does not match catalog.yaml"
            )

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
