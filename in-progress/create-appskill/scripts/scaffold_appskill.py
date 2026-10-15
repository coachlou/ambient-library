#!/usr/bin/env python3
"""Create an empty app-skill layout: scaffold_appskill.py <parent-dir> <name>"""
import sys
from pathlib import Path

ORCH = """---
name: {name}
description: TODO what the app does and when to use it (be specific and a little pushy)
---

# {name}

## Conversation contract
TODO persona, opening move, finds-vs-asks.

## Routing table
| When the user wants... | Do |
|------------------------|----|
| TODO | TODO `agents/x.md` / `skills/x/SKILL.md` / `scripts/x.py` |
| anything else | answer directly, or ask once |
"""

def main(parent, name):
    root = Path(parent) / name
    if root.exists():
        sys.exit(f"{root} exists")
    for d in ("agents", "skills", "references", "scripts", "assets", "evals"):
        (root / d).mkdir(parents=True)
    (root / "SKILL.md").write_text(ORCH.format(name=name))
    (root / "evals" / "evals.json").write_text('{"skill_name": "%s", "evals": []}\n' % name)
    print(root)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(*sys.argv[1:])
