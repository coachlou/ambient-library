# curate — create and maintain a local canonical library

A **local library** is a new instance of this folder: an AAI folder whose
behavior is "manage a library" and whose content is a user-chosen subset of
this canonical library. Same pattern, one level down — creating a local
library IS creating an AAI folder whose library is an instance of this one.

## Create a local library

1. Confirm the target path (default suggestion: `~/.ailib-local` or wherever
   the user says). If it already has `.aai/instructions.md`, stop and report.
2. Stamp it as an AAI folder: copy this repo's `.aai/` (router, subskills,
   identity, context) into `<target>/.aai/` — the local library inherits the
   full management behavior, not the scaffold template.
3. Rewrite `<target>/.aai/identity.md`: name it, state that it is a curated
   local instance of this canonical library, and record the upstream path/URL.
4. Create `<target>/library/` with an empty `catalog.yaml` (`skills:` header
   only) and `<target>/manifest.yaml` for provenance.

## Sources — a local library can curate from many

The default source is this canonical library, but any library-shaped folder
or repo is a valid source: another team's library-as-AAI repo, a second
clone, or nothing at all (skills authored directly in the local library get
`source: local` and are skipped by re-sync). `manifest.yaml` records the
source **per skill**, so one local library can mix them freely. The local
`catalog.yaml` stays one flat index — routing never cares where a skill
came from.

**Name collision rule:** if a requested skill already exists in the local
library from a different source, stop and ask which wins — never silently
overwrite one source's skill with another's.

## Add capabilities (curate in)

1. Resolve each requested skill or bundle against the source's
   `library/catalog.yaml` (default source: this library). Bundles expand to
   their member skills.
2. **Validate the subset is self-contained**: if a skill orchestrates siblings
   (e.g. `writing-team` needs researcher/writer/editor), pull the whole
   cluster in and tell the user you did.
3. Copy each skill folder pristine into `<target>/library/<skill>/`, append
   its one-line catalog entry to the local `catalog.yaml`, and record it in
   `<target>/manifest.yaml`: name, upstream source, `git log -1 --format=%h`
   of the upstream skill dir, date.

## Re-sync against upstream

1. For each `manifest.yaml` entry, compare against **that entry's own
   source** (multi-source libraries re-sync per skill; `source: local`
   entries are skipped): if the skill changed,
   re-copy it and refresh the manifest line — **unless** the local copy was
   edited (a local fork). The ownership rule applies: local edits win; report
   that an upstream update exists rather than overwriting.
2. Report per skill: updated / unchanged / fork-kept (update available).

## Prune

Remove the skill folder, its catalog line, its manifest line, and any bundle
membership — atomically, all four or none.

## Projects inherit from the local library

A project's `.ailib/` can vendor from a local library exactly as from
canonical — the lifecycle install/update operations take a source path, and a
local library is a valid source. Pin the local library's path in the project's
pointer or manifest.

## Rules

- Never edit skills inside this canonical repo from a curate operation — that
  is admin's job, in a source clone, deliberately.
- Confirm the target path before writing.
- Always keep catalog.yaml, manifest.yaml, and the skill folders consistent —
  a half-applied curate is worse than none.
