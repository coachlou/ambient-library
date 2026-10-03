---
name: Cheap-Model Prompt
type: command
description: Use a top-tier model to write a prompt optimized for a specific cheaper model, so the cheap model performs the task as well as the expensive one. Pay once for the reasoning, then run the volume cheaply.
trigger: /aimm:cheap-model-prompt
source-sessions:
- 2026-06-11_Mastermind
---

# Cheap-Model Prompt

## What it does

Inverts the usual model-selection instinct. Instead of running a task on a premium model, you **fix the cheapest viable model** and hire the premium model for one job: author a prompt that compensates for the cheap model's limits so it performs like the expensive one. The reasoning is paid for once (in the prompt) and reused on every cheap inference after.

Use it for any repetitive task where the reasoning is stable — especially forked/spawned sub-steps where you already pin the child's model.

## The prompt

> I'm going to run the task below on **[CHEAP MODEL — e.g. Haiku 4.5]** at **[effort: low/medium/high]**.
>
> You are **[STRONG MODEL — e.g. Opus 4.8]**. Knowing the specific capabilities and constraints of [CHEAP MODEL], write a single prompt that gets [CHEAP MODEL] to perform this task **as well as you would**. Bake in:
> - the strategy or method it should follow,
> - exactly where it should think step-by-step,
> - any sub-step it's likely to get wrong without explicit instruction,
> - the output format and quality bar.
>
> Don't solve the task yourself — produce the prompt I'll hand to [CHEAP MODEL].
>
> **Task:** [DESCRIBE THE TASK + paste any inputs/examples]

## How to use

1. Fill in the cheap model, effort level, strong model, and task.
2. Run it on the strong model to get the optimized prompt.
3. Run that prompt on the cheap model.
4. Compare against your old premium-model output. Where it holds up, keep the cheap-model prompt as your standing version of that task.
5. Optional: feed the prompt through a DSPy-style optimizer for a further lift.

## Notes

- Distinct from dynamic model routing (which decides the tier per step). Here the tier is fixed at the bottom on purpose; the intelligence moves upstream into the prompt.
- Reported gains run 20–75% over running the cheap model unaided.
- Pairs with per-step model routing — see Insight - Model Altitude — Route Model and Effort by Workflow Step, Not by Whole Artifact.

## Source

- PowerUp AI Mastermind Recap — 2026-06-11 (Lou — "use the smartest model to prompt the cheapest model so it performs as well as it can")
