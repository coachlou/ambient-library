<!-- ambient-library pointer adapter.

     PLACEMENT MATTERS — the pointer must live in the file the harness actually
     auto-loads, or the agent never sees it and improvises (observed: it read
     "make this folder ambient" as Node.js and ran `npm init`):
       - Codex        → AGENTS.md
       - Claude Code  → CLAUDE.md   (it auto-loads CLAUDE.md, NOT AGENTS.md)
       - Gemini       → GEMINI.md

     All three files are required outputs of an install: the full "## Ambient
     Library" block goes in AGENTS.md, and CLAUDE.md and GEMINI.md each get the
     one-line redirect (second block below) — a missing one means that harness
     never finds .aai/. Replace {{LIBRARY_ROOT}} with the library path; the
     user-scope default is ~/.ailib. -->

## Ambient Library   <!-- the canonical block — paste into AGENTS.md -->

A canonical skill library lives at `{{LIBRARY_ROOT}}`.

For any request about setting up or configuring project skills, updating or
managing skills, code review, **making this folder ambiently intelligent /
stamping `.aai/` here**, a library skill the user names, or a task covered by a
domain skill **enabled** here — listed in `~/.aai/skills-manifest.yaml` or this
project's `skills-manifest.yaml`, or vendored into its `.ailib/` (one-line
descriptions are in `{{LIBRARY_ROOT}}/library/catalog.yaml`; other catalog
skills are not candidates):

**Read `{{LIBRARY_ROOT}}/.aai/instructions.md` and follow it before acting.**

Note: an "ambient folder" is a folder carrying an `.aai/` behavior layer — it has
nothing to do with Node.js. Do not run `npm init` or scaffold a project; read the
router first. Where those instructions mention `${CLAUDE_PLUGIN_ROOT}`, treat it
as `{{LIBRARY_ROOT}}`. Do not read subskill or domain skill files until the
router directs you to one.

---

<!-- The redirect — written to BOTH CLAUDE.md (Claude Code) and GEMINI.md
     (Gemini CLI), so the canonical block lives in exactly one place (AGENTS.md). -->

**Read `AGENTS.md` in this folder and follow it before doing anything.** Do not
improvise, scaffold, or run `npm init` first — "ambient folder" here means a
folder with an `.aai/` behavior layer, not Node.js.
