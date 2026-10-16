# Create App-Skill (skills and app-skills)

Creates and improves skills — plain skills and **app-skills**. An app-skill is a skill whose `SKILL.md` is a conversational orchestrator that routes each request to bundled scripts, references, sub-skills and subagents.

## How this is layered

Anthropic's `skill-creator` is vendored here **unmodified**: its workflow is `upstream-skill-creator.md`, and its scripts, agents, eval-viewer and `references/schemas.md` sit at their original paths in this folder (provenance: `UPSTREAM.md`). Read `upstream-skill-creator.md` and follow it; every relative path in it (`scripts/…`, `agents/…`, `eval-viewer/…`) resolves from this skill's root. The sections below are overlays: they run at the points named, and where one conflicts with upstream, the overlay wins. Refer to upstream sections by name, never by line number.

Overlay order: **Destination → (improve mode) → Step 0 → Step 1 → upstream "Capture Intent / Interview / Write the SKILL.md" → Classify the steps → app-skill mode if chosen → upstream test cases and iteration → Quality gate → Packaging & provenance checks → upstream description optimization.**

Upstream scripts run as modules from this skill's root (`cd <skill-dir> && python -m scripts.run_eval …`), exactly as `upstream-skill-creator.md` shows; the overlay scripts (`scaffold_appskill.py`, `validate_appskill.py`) run directly.

## Destination

Unless the user names a target ("create it in this folder", "make this a global skill", a path), author new skills into the dev clone of the canonical library, under `in-progress/<skill-name>/` (never straight into `library/` — promotion is a separate step the user triggers; see the clone's `.aai/skills/admin.md`). Find the clone from the `Dev source (canonical-library)` row of `~/.aai/context.md`, or the current project if it has `.aai/instructions.md` and `.claude-plugin/plugin.json`. If neither resolves or the volume is unmounted, say so and ask where to author — never silently fall back to `~/.claude/skills/`, and never author in `agentic-ambient-intelligence/canonical-library/` (a stale rsync copy). An explicit user-given destination overrides all of this. Never push.

## `--improve` mode: audit and improve an existing skill

When invoked as `/create-appskill --improve <skill-path-or-folder>` — or when the
user asks to audit, review, harden, or improve one or more existing skills
rather than create a new one — skip the creation flow and read
`references/improve-workflow.md`. It runs the quality-gate rubric plus the
packaging & provenance checks as a blind per-skill audit (parallel subagents
for a folder), applies fixes only to flagged criteria, re-scores, and reports
before/after with a scoreboard. The same protocol serves as the validation
step inside the creation flow's quality gate; --improve just adds the
apply-and-re-score half.


### Step 0: Routing gate — what kind of thing is the answer?

Before drafting anything, answer in order. Skipping this gate is how libraries fill with duplicates.

1. **Does it already exist?** Search the installed skill list and, if available, the marketplace (the `find-skills` skill does this discovery). If an existing skill covers ≥70% of the need, propose extending or composing it. Tell the user what you found either way.
2. **One-liner?** If the whole behavior fits in a sentence or a single command, suggest a CLAUDE.md line or a settings hook. A skill has to earn its index tokens.
3. **Skill, app-skill, or agent?**
   - **Skill** — instructions plus optional scripts for one coherent class of work.
   - **App-skill** — the user wants a conversation with an orchestrator that dispatches subagents, other skills, scripts and resources, all shipped in one folder. Go to **App-skill mode** below.
   - **Agent** (`.claude/agents/<name>.md`) — judgment and orchestration across agents that should *not* be packaged as a skill (it needs its own tool allowlist, model, or persistent identity rather than being loaded into the host's context).

State your routing conclusion in one or two sentences and get the user's nod before proceeding.

### Step 1: Fill the Skill Brief (context contract)

Do not draft until a Skill Brief exists. Read
`references/context-contract.md` for the template and field definitions. The
brief is the contract between the skill and its invoker: purpose, invocation
schema (required/optional inputs, preconditions, outputs and side-effects),
trigger phrases plus near-miss negatives, environment, success criteria, and
known gotchas.

Fill it from cheapest source to most expensive — ask the human only for the
holes:

1. **The current conversation** — if the user said "turn this into a skill,"
   most of the brief is already in the transcript: tools used, step sequence,
   corrections made, formats observed.
2. **The filesystem** — the project's `CLAUDE.md`, a `.context/` directory,
   a `CONTEXT.md`, existing sibling skills, and any example files the user
   mentioned.
3. **The user (HITL)** — targeted questions for whatever the first two
   couldn't answer. Batch them; don't drip one question per turn.

Save the completed brief as `CONTEXT.md` inside the new skill's folder. It
ships with the skill: future improvement sessions get provenance, and the
brief seeds the eval prompts and the description later in this workflow.


### Classify the steps: code, inference, or hybrid

With the brief filled, sketch the skill's workflow as a list of steps and label
each one **code**, **inference**, or **hybrid** before writing prose. Default
to code: if a step can be a script, it becomes a `scripts/` entry from day one
— don't wait for eval transcripts to reveal that every run reinvented the same
helper. Inference earns its place only when the output space is unbounded or
context-dependent, genuine synthesis or judgment is required, or the pattern is
too rare to justify maintaining code. For each inference step, note in the
skill (one line each) what goes in, what must come out, and why code can't do
it — that's what makes the step optimizable later. Keep inference isolated
from control flow: the workflow drives; inference fills specific holes.


### Quality gate — audit the draft before spending on evals

Eval runs are expensive; a rubric pass is cheap. Once the draft is written,
audit it against `references/quality-rubric.md` (8 criteria, scored /10, gate
at 7 with no zeros). Spawn a fresh subagent for a blind read if you can;
otherwise audit inline after re-reading the draft cold. If it fails, fix only
the flagged criteria and re-score — at most twice, then surface the remaining
gaps to the user rather than polishing in circles. Report the score either
way; if the skill is heading to production, say so and hold the gate firmly.
The full audit protocol (scoring format, fix rules, batch mode) lives in
`references/improve-workflow.md` — the same one `--improve` mode uses.


### Packaging & provenance checks

These failures showed up repeatedly in a 29-skill audit of real skill libraries;
they're invisible to a prose-only read of SKILL.md, so check them mechanically
whenever you create, update, or audit a skill:

1. **Every referenced file must exist and resolve from the skill root.** Skills
   ship "Load references/X.md" pointers to files that were never written, or that
   moved during repackaging (a nested export dir orphans every relative path).
   Verify with `ls`, not by trust. If a reference is genuinely external, path it
   explicitly and add an "if absent" fallback.
2. **Exactly one SKILL.md per skill folder.** Copied/packaged exports leave a
   nested duplicate — two entry points with diverging paths that drift apart.
3. **Bundled scripts/templates must be wired in and match the prose.** Check that
   the workflow actually invokes shipped assets, that literals in the body (paths,
   step counts, config sentinels) match the script's reality, and that templates
   work from the declared output directory. A config guard checking for a
   sentinel the shipped default never contains is dead code.
4. **Strip provenance from SKILL.md.** Session dates, contributor names, quality
   scores, version histories, testimonial metrics ("10x faster"), and vault
   furniture ([[wiki links]], author-machine absolute paths) are token cost that
   also overfits the skill to its origin. Keep at most a one-line Source pointer;
   provenance belongs in CONTEXT.md or git history. Translate vault paths to
   skill-relative ones.
5. **Sweep stray artifacts.** Upload/debug sessions leave duplicate .md copies,
   "FINAL_FIX" notes, hash-named exports, and empty READMEs at the skill root.
   The folder should contain only SKILL.md plus declared references/scripts/assets.
6. **Don't demand what the model can't measure.** Replace pseudo-metrics
   ("70-80% voice similarity") with countable checklist gates; for judgment-heavy
   skills, one sentence stating *why* a step is inference-bound beats a fabricated
   script.

## App-skill mode

Chosen at Step 0. Everything above still applies; these are the differences.

**Step 1 brief — extend.** After the Skill Brief, fill the App Brief in `references/app-brief.md`: parts inventory (tools, resources, sub-skills, subagents that exist in the folder), conversation contract (opening move, finds vs asks, progress reporting), routing table, shared state. Save both together as `CONTEXT.md`.

**Classify the steps — add a fourth label: delegate.** The step is done by a named subagent or sub-skill. Every delegate step names its target file and what goes in and out.

**Scaffold and build order.** Run `scripts/scaffold_appskill.py <parent-dir> <name>` to create the layout in `references/appskill-anatomy.md`. Author parts in this order: scripts (code steps) → references → sub-skills → subagent prompts → orchestrator last, because its routing table can only point at parts that exist.

**Orchestrator rules (the produced `SKILL.md` must do these):**
- Open the conversation itself, in persona, stating what it can do in one short list. It is the UI.
- Route by the table, never by guess. A request matching no row is answered directly, or the user is asked once, batched.
- Subagents get a self-contained prompt read from `agents/<name>.md` (which begins `Spawn with: subagent_type …`) plus the specific inputs; they see none of the conversation. They return a structured result; the orchestrator, not the subagent, talks to the user. Results may arrive as a separate hand-back message rather than a return value — expect that.
- Sub-skills are not auto-discovered inside a skill folder. The orchestrator reads `skills/<name>/SKILL.md` explicitly when a route calls for it.
- Confirm before any external or irreversible side-effect, however deep in the delegation chain.
- Keep run state in one file (`state.md` or `state.json`) the orchestrator owns; parts read it and return results, they do not write it.
- The orchestrator must run as the main session or a general-purpose agent; agent types without the Agent tool cannot delegate.

**Quality gate — add app checks.** After the rubric passes, run `python3 scripts/validate_appskill.py <app-dir>`: routing targets exist, no orphaned parts, sub-skills pass `scripts/quick_validate.py`, `evals/evals.json` has ≥3 evals. Orchestration evals: 2–3 multi-part requests whose pass criteria name which parts must be invoked, plus one near-miss answered by the orchestrator directly with no delegation. A demo app that exercises an upstream script (for example `scripts/run_eval.py`) through the documented paths is the cheapest proof that inherited paths resolve.

References: `references/appskill-anatomy.md` (layout, routing table, subagent prompt contract), `references/app-brief.md`.
