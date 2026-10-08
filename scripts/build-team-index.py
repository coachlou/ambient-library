#!/usr/bin/env python3
"""Build library/team-index.yaml, the dense per-skill index team-build reads.

Usage: scripts/build-team-index.py [--check] [--only NAME ...] [--model M] [--jobs N]
  For every skill in library/catalog.yaml, hash its body (instructions.md, or
  SKILL.md) plus its catalog line. Entries whose hash changed, or are missing,
  are regenerated with one `claude -p` call each; unchanged entries are kept
  verbatim. The index is committed; this script only runs when a skill changes.
  A regenerated entry's not_for is merged with its previous not_for, not
  replaced, so hand-added or model-specific contrasts survive future runs.
  --check   exit 1 and list stale entries instead of regenerating.
  --only    regenerate only these skills (still writes the whole file).
  --reset-not-for NAME ...   rebuild these skills' not_for from scratch
                instead of merging, for when their neighbours changed.
  --dump DIR    write each stale skill's prompt to DIR/<name>.prompt.txt and stop.
  --replies DIR read DIR/<name>.md (a reply to that prompt) instead of calling
                claude; for harnesses where `claude -p` is not authenticated.
Exit 0 ok, 1 stale (--check) or a generation failed, 2 a skill has no body.
Needs `claude` on PATH. Spec: in-progress/team-build/SPEC.md.
"""

import hashlib
import pathlib
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
LIB = ROOT / "library"
OUT = LIB / "team-index.yaml"
BODY_CAP = 14000  # chars; enough for the contract, keeps the prompt bounded
# ponytail: one prompt string, no template file; edit here if the index schema changes.
PROMPT = """You are indexing one skill from a library of agent skills so a later
selector can match project needs to the right skill and tell it apart from its
nearest neighbours. Write ONLY a fenced yaml block with these keys:

summary: |
  150 to 250 words, Chain-of-Density style: dense, concrete, no filler. Name
  the inputs it needs, the artifact it produces, what it refuses to do, and
  its stage in any pipeline it belongs to.
requests:
  - 5 to 8 realistic user requests this skill should win, in the user's words
not_for:
  - <neighbour-name>: one line saying when the neighbour wins instead
  (2 to 5 entries; neighbour-name MUST be a name from the catalog below)
stage: one or two lowercase words (research, draft, edit, publish, audit, setup, operate, ...)

SKILL NAME: {name}
CATALOG LINE: {line}

CATALOG (names and one-line descriptions of every skill, for the not_for contrasts):
{catalog}

SKILL BODY:
{body}
"""


def catalog():
    text = (LIB / "catalog.yaml").read_text()
    rows = dict(re.findall(r"^  ([a-z0-9-]+): (.+)$", text, re.M))
    rows.pop("team-build", None)  # the index's own reader; it never recommends itself
    return rows


def body_of(name):
    for f in ("instructions.md", "SKILL.md"):
        p = LIB / name / f
        if p.exists():
            return p.read_text()[:BODY_CAP]
    sys.exit(print(f"{name}: no instructions.md or SKILL.md", file=sys.stderr) or 2)


def parse(text, cat):
    """YAML block out of a claude reply; drop not_for entries naming unknown skills."""
    m = re.search(r"```ya?ml\n(.*?)```", text, re.S)
    raw = m.group(1) if m else text
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError:
        # Models write list items like `- "Recap this" with a VTT`; quote the whole item.
        fixed = re.sub(
            r'^(\s*- )(?!["\'\w-]+:)(.*"\S.*)$',
            lambda mm: mm.group(1) + '"' + mm.group(2).replace('"', "'") + '"',
            raw,
            flags=re.M,
        )
        data = yaml.safe_load(fixed)
    if not isinstance(data, dict):
        raise ValueError("no mapping")
    out = {"summary": " ".join(str(data["summary"]).split())}
    words = len(out["summary"].split())
    if not 80 <= words <= 350:
        raise ValueError(f"summary {words} words")
    out["requests"] = [str(r) for r in data["requests"]][:8]
    if len(out["requests"]) < 3:
        raise ValueError("too few requests")
    nf = []
    for item in data.get("not_for") or []:
        if isinstance(item, dict):
            for k, v in item.items():
                if k in cat:
                    nf.append({k: " ".join(str(v).split())})
    out["not_for"] = nf
    out["stage"] = " ".join(str(data.get("stage", "")).lower().split()) or "other"
    return out


def merge_not_for(prev, new, cat, name):
    """Merge a regenerated not_for list into the previous one instead of replacing it.

    Previous items are kept, in order, dropping any naming a skill no longer in the
    catalog or the entry itself. New items are appended for names not already kept;
    a name collision keeps the previous wording.
    """
    kept = []
    seen = set()
    for item in prev:
        for k, v in (item or {}).items():
            if k in cat and k != name and k not in seen:
                kept.append({k: v})
                seen.add(k)
    for item in new:
        for k, v in item.items():
            if k not in seen:
                kept.append({k: v})
                seen.add(k)
    return kept


def not_for_for(name, prev_index, entry, cat, reset):
    if name in reset or name not in prev_index:
        return entry["not_for"]
    return merge_not_for(
        prev_index[name].get("not_for") or [], entry["not_for"], cat, name
    )


def names_after(argv, flag):
    """Variadic names following `flag`, stopping at the next --flag or end of argv."""
    if flag not in argv:
        return set()
    i = argv.index(flag) + 1
    out = []
    while i < len(argv) and not argv[i].startswith("--"):
        out.append(argv[i])
        i += 1
    return set(out)


def prompt_for(name, line, cat):
    return PROMPT.format(
        name=name,
        line=line,
        catalog="\n".join(f"- {k}: {v}" for k, v in cat.items()),
        body=body_of(name),
    )


def generate(name, line, cat, model, replies=None):
    if replies:
        return parse((replies / f"{name}.md").read_text(), cat)
    prompt = prompt_for(name, line, cat)
    cmd = ["claude", "-p", "--permission-mode", "auto"] + (
        ["--model", model] if model else []
    )
    r = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=600)
    if r.returncode:
        raise RuntimeError(r.stderr.strip()[-400:])
    return parse(r.stdout, cat)


def main(argv):
    check = "--check" in argv
    model = argv[argv.index("--model") + 1] if "--model" in argv else ""
    jobs = int(argv[argv.index("--jobs") + 1]) if "--jobs" in argv else 4
    only = set(argv[argv.index("--only") + 1 :]) if "--only" in argv else set()
    reset_not_for = names_after(argv, "--reset-not-for")
    dump = pathlib.Path(argv[argv.index("--dump") + 1]) if "--dump" in argv else None
    replies = (
        pathlib.Path(argv[argv.index("--replies") + 1]) if "--replies" in argv else None
    )
    cat = catalog()
    index = yaml.safe_load(OUT.read_text()) if OUT.exists() else {}
    hashes = {
        n: hashlib.sha1((body_of(n) + line).encode()).hexdigest()[:12]
        for n, line in cat.items()
    }
    stale = [n for n in cat if index.get(n, {}).get("source_hash") != hashes[n]]
    if only:
        stale = [n for n in stale if n in only] or sorted(only)
    if check:
        print(
            f"{len(cat)} skills; "
            + (f"STALE: {' '.join(stale)}" if stale else "index up to date")
        )
        return 1 if stale else 0
    if dump:
        dump.mkdir(parents=True, exist_ok=True)
        for n in stale:
            (dump / f"{n}.prompt.txt").write_text(prompt_for(n, cat[n], cat))
        print(f"dumped {len(stale)} prompts to {dump}")
        return 0
    if replies:
        stale = [n for n in stale if (replies / f"{n}.md").exists()]

    def work(n):
        try:
            return n, generate(n, cat[n], cat, model, replies)
        except Exception as e:  # keep the batch going; report at the end
            print(f"FAIL {n}: {e}", file=sys.stderr)
            return n, None

    failed = []
    with ThreadPoolExecutor(jobs) as pool:
        for n, entry in pool.map(work, stale):
            if entry is None:
                failed.append(n)
                continue
            nf = not_for_for(n, index, entry, cat, reset_not_for)
            index[n] = {
                "description": cat[n],
                **entry,
                "not_for": nf,
                "source_hash": hashes[n],
            }
            print(f"indexed {n}")
    index = {
        n: index[n] for n in cat if n in index
    }  # catalog order, drop removed skills
    OUT.write_text(
        "# not_for is merged across regenerations; hand-added items persist."
        " Other fields are regenerated.\n"
        + yaml.safe_dump(index, sort_keys=False, allow_unicode=True, width=88)
    )
    print(
        f"wrote {OUT.relative_to(ROOT)}: {len(index)}/{len(cat)} entries, {len(stale)} regenerated"
    )
    return 1 if failed else 0


def selftest():
    cat = {"writer": "x", "editor": "y"}
    reply = (
        "```yaml\nsummary: "
        + "w " * 100
        + "\nrequests: [a, b, c]\nnot_for:\n  - editor: draft exists\n  - ghost: nope\nstage: Draft\n```"
    )
    e = parse(reply, cat)
    assert e["not_for"] == [{"editor": "draft exists"}] and e["stage"] == "draft"
    bad = (
        "summary: "
        + "w " * 100
        + '\nrequests:\n  - "Recap this" with a VTT\n  - plain\n  - more\nnot_for: []\nstage: x\n'
    )
    assert parse(bad, cat)["requests"] == ["'Recap this' with a VTT", "plain", "more"]

    cat3 = {"writer": "x", "editor": "y", "proof": "z"}
    # merge keeps old items, appends new ones, name collision keeps old wording,
    # and an item naming a removed skill ("ghost") is dropped.
    prev_nf = [{"editor": "old wording"}, {"ghost": "gone"}]
    new_nf = [{"editor": "new wording"}, {"proof": "fresh"}]
    merged = merge_not_for(prev_nf, new_nf, cat3, "writer")
    assert merged == [{"editor": "old wording"}, {"proof": "fresh"}]

    entry = {"not_for": new_nf}
    prev_index = {"writer": {"not_for": prev_nf}}
    assert not_for_for("writer", prev_index, entry, cat3, set()) == merged
    # --reset-not-for rebuilds from scratch: previous items are ignored.
    assert not_for_for("writer", prev_index, entry, cat3, {"writer"}) == new_nf
    # a skill with no previous entry also just takes the generated list.
    assert not_for_for("new-skill", prev_index, entry, cat3, set()) == new_nf


if __name__ == "__main__":
    selftest()
    sys.exit(main(sys.argv[1:]))
