---
name: Tree-of-Thought Prep — Adversarial Exploration Before the PRD
type: command
description: Sets up an adversarial, non-sycophantic tree-of-thought exploration of an idea's entire solution surface before any PRD or spec is written, so the resulting spec is built on a fully-examined problem rather than an unexamined assumption.
trigger: /aimm:tree-of-thought-prep
source-sessions:
- 2026-06-18_Mastermind
---

# Tree-of-Thought Prep — Adversarial Exploration Before the PRD

Paste this at the start of a fresh chat, replacing the bracketed line with your idea. Walk the whole tree before you ask for a PRD. When the tree is exhausted, say: *"Now look back through our entire conversation and write the PRD."*

> **Setup prompt:**
>
> I have an idea: **[one-paragraph description of what you want to build or do].**
>
> Do **not** write a PRD, plan, or spec yet. Your job right now is to be my **adversarial, non-sycophantic stress-test and brainstorming partner.**
>
> Rules for this conversation:
> 1. **Push back** on anything I say that doesn't hold up. Don't soften it, don't hedge, don't agree to be agreeable.
> 2. **Don't cave** on anything you're genuinely convinced of just because I resist it.
> 3. Take me through a **tree of thought**: explore every branch of this solution — every feature, every failure mode, every blind spot, every technical requirement, every assumption I'm making without realizing it.
> 4. Any time something new surfaces, **open a new branch** and explore it. Don't let us collapse to the first plausible answer.
> 5. Make sure we **don't miss a single branch** before we stop.
> 6. If a branch is a clear dead end, say so and **prune it** (note it in one line so we don't revisit). If a branch is interesting but off the critical path, tell me to **defer it** to a separate chat so we stay focused.
>
> Start by reflecting the idea back to me, then name the two or three highest-risk assumptions you'd want to interrogate first. Ask me one question at a time.

## Notes for use

- **Expect this to take a while** — a complex idea can run an hour or two. The payoff is a PRD that's bulletproof because the thinking happened *before* the spec, not during implementation.
- **Manage the context** as you go: when a branch resolves into a decision, have it write that decision to a handoff and (optionally) start a fresh chat from the handoff. Use rewind rather than in-line correction to keep the thread high-signal. (See Rewind, Don't Re-Correct — Keep Failed Attempts Out of the Context Window.)
- **The failure mode this prevents:** jumping straight to "write me a PRD" makes the AI assume your idea is correct and merely document it — blind spots and all. This phase interrogates whether the idea should exist in its current form *first*.
- Pairs naturally with the *superpowers* chained-gate flow (brainstorm → plan → spec → implement, each confirmed before the next) that Kasimir noted in-session.

## Source

- PowerUp AI Mastermind Recap — 2026-06-18 (Lou — adversarial tree-of-thought exploration before writing the PRD; Don Back independent validation)
