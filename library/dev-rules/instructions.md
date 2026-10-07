# dev-rules

The global coding rules, made ambient. One rules file in the owner's self
scope, `~/.aai/rules/coding.md`, applies to every conversation that writes,
changes, or reviews code, in any folder, harness, or capability (chat-n-build,
solofactory, vibe, software-dev-factory, or none). This capability seeds it,
routes to it, wires every harness to it, and publishes the owner's edits back
into the library.

## Authority

```
~/.aai/rules/coding.md                      authority: the owner edits it here only
   │ publish.sh (committed edits only)
   ▼
library/dev-rules/rules/coding.md           published snapshot: never hand-edited
   │ install.sh / vendoring / paste.sh
   ▼
new homes, .ailib/dev-rules/, chat settings  copies: refreshed, never edited
```

Capabilities do not carry their own copy of these rules. A capability that
needs a design artifact specific to its method (a WBS module map, a factory's
gate) points here for the rules and keeps only its own mechanics.

## Operations

### Apply: any coding conversation

Read the first that exists, then follow it:

1. `~/.aai/rules/coding.md`
2. `.ailib/dev-rules/rules/coding.md` in the current folder (vendored, for
   machines and cloud containers without the owner's `~/.aai`)
3. `${CLAUDE_PLUGIN_ROOT}/library/dev-rules/rules/coding.md`

Project instructions may tighten the rules; they never loosen them silently.

### Install: "set up the coding rules", "make the rules global"

```
bash ${CLAUDE_PLUGIN_ROOT}/library/dev-rules/scripts/install.sh --check
bash ${CLAUDE_PLUGIN_ROOT}/library/dev-rules/scripts/install.sh
```

Show the `--check` plan, then run it. It is user scope: it seeds
`~/.aai/rules/coding.md` if absent, adds one trigger row to `~/.aai/context.md`
if it exists and does not route coding yet, puts `~/.aai` under local git if it
is not already, and appends a pointer to each installed harness's global file
unless that file already points at `~/.aai`. It never edits `core.md` and
never overwrites an owned file.

| Harness | How it gets the rules |
|---|---|
| Claude Code (CLI, desktop Code tab, IDE) | `~/.claude/CLAUDE.md` pointer, or the existing `~/.aai` bootstrap |
| Codex | `$CODEX_HOME/AGENTS.md` (default `~/.codex/`); `AGENTS.override.md` instead when it exists, because Codex then ignores `AGENTS.md` |
| opencode | Reads `~/.claude/CLAUDE.md` while it has no `AGENTS.md` of its own, so nothing is created; an existing `$OPENCODE_CONFIG_DIR` or `~/.config/opencode/AGENTS.md` gets the pointer |
| DeepSeek Harness (`dsh`) | `$DSH_HOME/AGENTS.md` (default `~/.dsh/`) |
| Orca | Runs the CLIs above, each loading its own global file; nothing to write |
| claude.ai chat and Cowork | One shared UI field, Settings → Instructions for Claude; no file access, so paste once (below) |
| Wave AI | No instruction hook (hard-coded system prompt); use the CLIs above inside Wave's terminal |
| Any other file-based harness | Add its global file to `HARNESSES` in `install.sh` |

### Paste: chat surfaces without file access

```
bash ${CLAUDE_PLUGIN_ROOT}/library/dev-rules/scripts/paste.sh
```

Give the user the output and where it goes: Settings → Instructions for
Claude, one field shared by claude.ai chat and Cowork (or a Project's
instructions). Say plainly that a pasted copy does not update; re-paste after each
publish.

### Publish: "publish my coding rules", "update the library's coding rules"

Only in the library dev workspace (never `.aai/PRODUCTION`).

```
bash library/dev-rules/scripts/publish.sh --check
bash library/dev-rules/scripts/publish.sh
```

It refuses while `~/.aai/rules/coding.md` has uncommitted changes, so every
snapshot traces to a commit. Then bump `.claude-plugin/plugin.json`, commit,
and release through `admin.md` as usual.

### Vendor: folders that must work without `~/.aai`

Cloud sessions and collaborators' machines have no owner home. Vendor with
`library/ambient-folder/install.sh dev-rules <folder>` and make sure the
folder's `CLAUDE.md`/`AGENTS.md` (or `.aai/instructions.md`) says to read
`.ailib/dev-rules/rules/coding.md` when coding.

## Rules

- Edit rules only in `~/.aai/rules/coding.md`, with the owner's approval per
  `core.md`; never in the snapshot, a vendored copy, or a harness file.
- Harness files get a pointer, never the rules text.
- Run `scripts/test_dev_rules.sh` after changing any script.
