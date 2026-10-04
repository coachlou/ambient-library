# brand-writing-team

A multi-role Claude Code skill that turns a raw idea into a publishable brand-building piece — a blog post, newsletter, thought-leadership article, personal-story essay, or how-to tutorial. The skill orchestrates a team of specialist sub-agents that each own one decision type and hand off structured artifacts. The only role allowed to write prose is the Drafter.

## What it produces

End-to-end output for one piece:

- A chosen headline and two runners-up
- The polished, publishable final piece
- A quality summary with the per-role self-evaluation scores
- Optional process notes: thesis, dossier, outline, source-verification report, avatar reactions, line-editor changelog

The bar is **top 1% — world-class**. Every role self-evaluates against a 5–8 criterion rubric and the overall score is the **minimum** across criteria, not the average. Roles revise up to 3 times or stop early at ≥9.

## How it works

```
            ┌─ Researcher ─┐
Strategist ─┤              ├─ Outliner ─ Drafter ─┬─ Skeptic ──┐
            └─ Avatar(1) ──┘                     └─ Avatar(2) ─┴─ Line Editor ─ DONE
```

Six stages, two of which fan out in parallel. Before any stage runs, the orchestrator runs an intake step that asks the user for topic, type of writing, audience, voice, and target length using `AskUserQuestion`. The intake auto-discovers available options by globbing the resources folders, so adding a new voice or avatar requires no code changes.

### The team

| # | Role | Owns |
|---|---|---|
| 1 | Strategist | the angle and thesis |
| 2 | Researcher | evidence, examples, data — with verified sources |
| 3 | Avatar Reviewer | the reader's reaction (consulted twice) |
| 4 | Outliner | section-by-section structure |
| 5 | Drafter | the first full draft (only role allowed to write prose) |
| 6 | Skeptic | red-team objections + fact-check, with live source verification |
| 7 | Line Editor | sentence-level polish and final piece |

### Critical guarantees

- **No fabricated sources.** The Researcher must produce verified citations. The Skeptic re-verifies them with `WebFetch` / `WebSearch` before the Line Editor runs. If "Source verification" scores below 9, the orchestrator does not proceed.
- **No AI tells.** The Drafter and Line Editor always load `resources/ai-isms-checklist.md`, which forbids em-dashes, exclamation points, and a long list of disallowed words and phrases. The checklist overrides any voice-specific punctuation guidance.
- **Voice is load-bearing.** The Drafter and Line Editor load the user's chosen brand voice file and check the final piece against its "do not" list before scoring.
- **Quality gate at the end.** If the Line Editor ships below 9, the orchestrator surfaces the score and the weakness notes to the user instead of silently delivering.

## Repository layout

```
brand-writing-team/
├── SKILL.md                       # the orchestrator
├── README.md                      # this file
└── resources/
    ├── ai-isms-checklist.md       # global anti-AI-tells rules (always loaded)
    ├── handoff-contract.md        # output format every role uses
    ├── quality-gates.md           # universal self-eval mechanics
    │
    ├── audience-avatars/          # one .md per persona; intake picks one
    │   ├── jules-corporate-ic.md
    │   ├── marcus-small-team-founder.md
    │   └── maya-knowledge-entrepreneur.md
    │
    ├── brand-voices/              # one .md per voice; intake picks one
    │   ├── analytical-pragmatic.md
    │   ├── compassionate-storyteller.md
    │   ├── direct-authoritative.md
    │   ├── experience-insight-guide.md
    │   └── warm-storyteller.md
    │
    ├── roles/                     # one .md per specialist
    │   ├── strategist.md
    │   ├── researcher.md
    │   ├── avatar-reviewer.md
    │   ├── outliner.md
    │   ├── drafter.md
    │   ├── skeptic.md
    │   └── line-editor.md
    │
    └── writing-types/             # one .md per piece type; intake picks one
        ├── blog.md
        ├── newsletter.md
        ├── thought-leadership-article.md
        ├── personal-story.md
        └── how-to-tutorial.md
```

## Default lengths

| Piece type | Default |
|---|---|
| Newsletter | ~600 words (max 1,000) |
| Blog post | ~900 words |
| Thought-leadership article | ~1,200 words |
| Personal story | ~1,000 words |
| How-to tutorial | ~1,200 words |
| Long-form cornerstone piece | ~1,800 words |

## Triggering the skill

Claude Code activates this skill on phrases like:

- "help me write a post about X"
- "I have an idea for a newsletter"
- "draft an article on Y"
- "turn this idea into a piece"
- "make this into a blog post"
- "I want to publish something about Z"

The user does not need to say "writing team."

## Extending the skill

Add a new voice, avatar, or writing type by dropping a single `.md` file into the appropriate folder. The orchestrator's intake globs the folder at runtime, so new options appear automatically with no code changes. Each file should follow the structural conventions of the existing files in that folder (frontmatter is not required, but the headings should match so the role files know how to read them).

## Installing

This skill lives in this shared repo. To install it locally for Claude Code:

1. Copy the folder to `~/.claude/skills/brand-writing-team/`
2. Or package it with the `skill-creator` skill: `python -m scripts.package_skill /path/to/brand-writing-team` and load the resulting `.skill` archive.

## Design notes

- **Separation of concerns is the central design principle.** Every role owns one decision type. Roles do not rewrite each other. They hand off and move on. This avoids the "committee writes mush" failure mode where every reviewer softens every line.
- **Parallel stages where independent.** Stage 2 (Researcher + Avatar 1st pass) and Stage 5 (Skeptic + Avatar 2nd pass) run as same-turn parallel sub-agents.
- **Self-evaluation uses minimum-not-average scoring.** A chain is as strong as its weakest link. Averaging hides failure modes; the minimum surfaces them.
- **The Drafter is the only role allowed to write prose from scratch.** Every other role produces a structured artifact in the format defined by `handoff-contract.md`.
- **The orchestrator never rewrites role outputs.** If a role returns something weak, the orchestrator sends it back to that role with a note targeting the weakest criterion.
