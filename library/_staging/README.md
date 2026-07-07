# _staging — proposed skills, not yet real

Skills here are **proposals** drafted from a real task trace (see
`.aai/skills/propose.md`). They are unreviewed and deliberately inert:

- **Not** in `catalog.yaml`, `SKILLS.md`, or `marketplace.json`.
- **Never** loaded by the router — selection reads only the catalog, and the
  leading underscore keeps this folder sorted apart from real skills.

Each proposal is `_staging/<name>/` with:

- `instructions.md` — same format as a real domain skill.
- `PROPOSAL.md` — where it came from and why it might earn a place (proposed
  catalog description, source trace, evidence, overlap check).

Promotion or rejection goes through `.aai/skills/admin.md` ("Promote a staged
proposal"). Nothing here auto-promotes — self-generated skills underperform
unless authored from real traces and reviewed, and an unvetted catalog degrades
routing for every skill.
