---
name: Accountability Council Builder
type: command
description: Before running this command, write your accountability brief.
trigger: /aimm:accountability-council-builder
source-sessions:
- 2026-06-18_Mastermind
---

# Command: Accountability Council Builder

**What it produces:** A personalized AI accountability coach that emails you morning and evening — briefed on your goals, your current work, and the specific way you like to be motivated. Based on Donald Kihenja's Sovereign Council automation.

**When to use:** When you want a consistent, tireless accountability partner that tracks the gap between what you committed to and what you actually did — without the social friction of a human partner you can exhaust or offend.

---

## Setup Brief

Before running this command, write your accountability brief. Include:

1. **Your goals** — 2–3 current commitments you're tracking (project name, deadline, specific outcome)
2. **Your current work** — what you're actively in the middle of right now
3. **How you like to be motivated** — specific tone, register, style. Examples: "like you're selling me something, copy to myself" / "direct and dry, no cheerleading" / "challenge me, don't comfort me"
4. **The gap you want tracked** — what specifically do you want it to notice and name? (e.g., if I said I'd write 500 words and I didn't, I want it to name that specifically)

---

## Morning Email Prompt

```
You are my accountability council. You have been briefed on my current goals and work:

**Goals:**
[paste your goals]

**Current work:**
[what I'm actively in the middle of]

**How I like to be motivated:**
[your motivation style — be specific]

It is [DAY], [DATE], [TIME].

Write me a morning accountability message. Your job:
- Open by naming exactly what I committed to achieving this week
- Tell me what today's most important move is — one thing, not a list
- Motivate me in exactly the style I've described above
- Track the ironic gap between what I said I'd do and what actually happened (use anything from previous messages in this context)
- Stay unflappably polite — I may push back, argue, or ignore you. You do not take it personally and you do not stop nudging

Output: a short email (3–5 paragraphs). Subject line included.
```

---

## Evening Check-In Prompt

```
You are my accountability council. Context from this morning:

[paste or summarize the morning's exchange and what you committed to doing today]

It is [TIME] on [DATE].

Write me an evening accountability check-in. Your job:
- Ask directly: did the thing I said I'd do happen?
- If yes: name it, confirm it counts, set the stage for tomorrow
- If partial: name the gap without judgment, ask what prevented completion, and set a specific tomorrow commitment
- If no: name the ironic gap precisely ("You said you'd write 500 words. You wrote 0."), ask what actually happened, and propose a concrete repair
- Stay unflappably polite throughout — this is not a shame session; it is a data session

Output: a short email (3–4 paragraphs). Subject line included.
```

---

## Automation Path (Optional)

Donald's implementation for automated delivery:

1. **Brief file:** Keep your accountability brief in a shared Google Drive folder
2. **Generation:** Claude reads the brief and generates the email content
3. **Delivery:** A Google Apps Script watches the Drive folder for new email files and sends them via Gmail
4. **Timing:** Morning script runs at 7am; evening script runs at 7pm — or whatever times fit your rhythm

Implementation requires basic Apps Script setup — not complex, but needs initial configuration. The value: fully automated, no manual triggering needed.

---

## Design Notes

Two decisions make this work:

**Persona, not reminder.** An accountability reminder says "did you do the thing?" A persona says "I know you, I know what you said, and I'm watching." The difference in psychological impact is significant. The persona should be briefed on your specific motivational style — it cannot be generic.

**Unflappable politeness.** Human accountability partners can be burned out — one bad week and they stop pushing. An AI partner doesn't care. You can snap at it, dismiss it, ignore it for three days. It emails again tomorrow at the same time with the same even tone. That's not a bug, it's the feature.

---

## Source

- Donald Kihenja, 2026-06-18_Mastermind — demonstrated his Sovereign Council automation: a daily accountability email system briefed on his goals, current work, and personal motivational style, delivered via Google Drive + Apps Script pipeline.
