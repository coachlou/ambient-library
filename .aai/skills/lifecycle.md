# lifecycle

Operations that make another folder ambiently intelligent and maintain it over
time: the **stamp → install → personalize → learn → update** lifecycle of the
`.aai`/`.ailib` scaffold. The full spec is
`${CLAUDE_PLUGIN_ROOT}/templates/aai/README.md` — read it if a detail here is
ambiguous.

## The ownership rule (governs every operation below)

- `.aai/` is **owned** by the target folder. No operation here ever overwrites
  a file the user has edited in `.aai/`.
- `.ailib/` is **vendored** — pristine, read-only copies of canonical
  capabilities. Install and update may delete and re-sync it freely.
- **`.aai/` shadows `.ailib/`.** When both define a capability `<cap>`, the copy
  in `.aai/skills/<cap>` wins.

## Stamp — make a folder ambient

1. Confirm the target folder path. If it already has `.aai/instructions.md`,
   stop and report — never overwrite an existing profile.
2. Copy `${CLAUDE_PLUGIN_ROOT}/templates/aai/` into `<target>/.aai/`.
3. Rewrite `identity.md` (who the folder is) and `instructions.md` (what it does
   with requests) for the target. Fill `context.md` with its real layout.
4. Delete every optional element the folder doesn't need yet (`memory/`,
   `references/`, `templates/`). `.ailib/` is created by the first install, not
   the stamp.

## Install — vendor a canonical capability

1. Resolve the capability in this library: `${CLAUDE_PLUGIN_ROOT}/library/<cap>/`.
2. Copy it pristine into `<target>/.ailib/<cap>/`.
3. Record it in `<target>/.ailib/manifest.yaml`: name, source, version.
4. Never edit inside `.ailib/` — edits there are lost on the next update.

## Personalize — fork a capability (shadowing)

1. Copy `<target>/.ailib/<cap>/` → `<target>/.aai/skills/<cap>/`.
2. Edit the copy. The router now resolves `<cap>` to the `.aai/` fork; the
   pristine canonical stays in `.ailib/` for comparison and re-sync.

## Learn — promote memory into a reference

`.aai/memory/` is runtime state (handoffs, progress, observations across runs)
and is never touched by any update. When a pattern recurs — the same correction
three runs running — promote it deliberately into `.aai/references/<rule>.md` as
a rule the behavior internalizes as a constraint. Memory is where the folder
notices; references are where it has learned.

## Update — re-sync vendored capabilities

1. For each entry in `<target>/.ailib/manifest.yaml`, re-copy the pristine
   capability from `${CLAUDE_PLUGIN_ROOT}/library/<cap>/` and refresh its version.
2. `.aai/` — forks, references, and memory — is untouched. That is the entire
   point of the ownership boundary: a personalized fork keeps overriding the
   refreshed `.ailib/` copy via shadowing.

## Rules

- Confirm the target path before writing. Never stamp or install into this
  library repo itself by accident.
- One operation per request.
- Report what changed in plain language: which files, which folder.
