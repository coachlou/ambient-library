#!/usr/bin/env python3
"""Validate an app-skill: validate_appskill.py <app-dir>
Checks: routing targets exist, no orphaned parts, sub-skills pass quick_validate."""

import re
import subprocess
import sys
from pathlib import Path

QV = Path(__file__).parent / "quick_validate.py"
PART = re.compile(
    r"`((?:agents|skills|references|scripts|assets)/[^`\s]+?)(?:\s[^`]*)?`"
)


def main(app):
    root = Path(app)
    body = (root / "SKILL.md").read_text()
    errs = []
    refs = {m.group(1).rstrip("/") for m in PART.finditer(body)}
    for r in sorted(refs):
        if not (root / r).exists() and "<" not in r and "*" not in r:
            errs.append(f"routing target missing: {r}")
    if "TODO" in body:
        errs.append("SKILL.md still contains TODO")
    # every part on disk should be mentioned by the orchestrator or another md file
    corpus = body + "".join(
        p.read_text() for p in root.rglob("*.md") if p != root / "SKILL.md"
    )
    for d in ("agents", "references", "scripts"):
        for f in (root / d).glob("*") if (root / d).exists() else []:
            if (
                f.is_file()
                and f.suffix != ".pyc"
                and f.name != "__init__.py"
                and f.name not in corpus
            ):
                errs.append(f"orphaned part: {d}/{f.name}")
    for s in (root / "skills").glob("*/") if (root / "skills").exists() else []:
        if not (s / "SKILL.md").exists():
            errs.append(f"sub-skill without SKILL.md: {s.name}")
        elif QV.exists():
            r = subprocess.run(
                [sys.executable, str(QV), str(s)], capture_output=True, text=True
            )
            if r.returncode:
                errs.append(f"sub-skill {s.name}: {(r.stdout + r.stderr).strip()}")
    ev = root / "evals" / "evals.json"
    if (
        not ev.exists()
        or len(__import__("json").loads(ev.read_text()).get("evals", [])) < 3
    ):
        errs.append(
            "evals/evals.json needs >=3 evals (2 multi-part + 1 no-delegation near-miss)"
        )
    print("\n".join(errs) or "OK")
    sys.exit(bool(errs))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
