---
name: negotiation-prep
type: command
description: 'Before running this command, gather:'
---

# Command: Negotiation Prep

**When to use:** Before any significant meeting where you need to advocate for a position against informed opposition — board meetings, contract negotiations, high-ticket sales conversations, partnership discussions, governance decisions.

---

## Setup

Before running this command, gather:
1. **Governing documents** — contracts, bylaws, regulations, policies, or terms relevant to the matter
2. **Meeting transcript** — from the most recent meeting where all parties stated their positions (even rough notes work)
3. **Your objective** — what specific outcome you need from this meeting
4. **Your strategy** — what you're willing to trade away to get what you want

---

## Prompt Template

```
I am preparing for a negotiation / meeting on [DATE] about [TOPIC].

Here are the relevant documents: [attach/paste governing docs]

Here is the most recent meeting where all parties stated their positions: [attach/paste transcript]

My objective: [specific outcome you want]
What I'm willing to give up: [concessions you can live with]
What I'm NOT willing to give up: [your non-negotiables]

Now I want to rehearse the negotiation before the real meeting.

Step 1: Analyze the documents and transcript. Identify every party's stated position, their likely interests behind that position, and what they would need to accept the outcome I want.

Step 2: Role-play as the opposing parties. Hold their positions firmly. Push back on my arguments using their actual logic and concerns. Do NOT change your position unless I give you specific data or evidence — restating my position more forcefully is not enough.

Step 3: I will propose my strategy and argue for my outcome. Audit my reasoning. Challenge every weak point. Tell me what I haven't thought through.

Step 4: When my strategy holds under your scrutiny, produce:
- A briefing note with [N] recommended actions, including [my real goal] plus [N-1] tradeable items I'm willing to negotiate away
- A list of the 3 most likely objections I'll face and how to answer them
- Any elements of my position that remain vulnerable

Let's begin. Step 1:
```

---

## Cannon-Fodder Tactic

When building the briefing note, deliberately include more recommended actions than you actually want. The extras are **cannon fodder** — positions you're willing to trade in negotiation to secure the one outcome that matters. Structure the brief so your real goal reads as one item among several reasonable options, not as the obvious ask.

Example: if you want Action #3, the brief might recommend Actions 1–7. In the room, you let them push back on 1, 2, 4, and 5 while holding 3. They feel they've influenced the outcome; you got what you came for.

---

## Calibration Notes

- This command assumes you've loaded real documents and real transcripts. Generic or hypothetical input produces generic output.
- The quality of the rehearsal depends on how accurately the transcript captures the other parties' actual positions. Record or transcribe real meetings when this matters.
- Don Back uses Claude Chat (not Claude Code) for this — simpler setup, everything in one thread.
- Run the rehearsal at least 24 hours before the real meeting so you have time to adjust strategy.

---

## Institutional Document Setup (Governance Variant)

When the negotiation involves formal institutional documents (corporate bylaws, non-profit Acts, board resolutions, regulatory frameworks), load them as a structured package before running the main prompt. Don Back's setup for a non-profit governance dispute:

**Document package loaded:**
- The governing Act (statutory authority for the dispute)
- The organization's bylaws (internal governance rules)
- Meeting transcript from the last session where all parties stated their positions
- His objective + negotiating strategy + proposed actions list (7 items, only 1 of which he actually wanted)

**Why the package matters:** The AI needs all three layers — the statutory authority, the internal rules, and the actual positions stated — to role-play the opposing parties accurately. Without the governing docs, it can only guess at what arguments the other side will reach for. With them, it can pull the exact clause they'll cite.

**Cannon-fodder design in practice:** Don's 7 proposed actions list was structured so that his real ask (1 item) was indistinguishable from his 6 tradeable items in appearance. The opposing parties spent the meeting negotiating down from 7. They thought they'd won. He got the one thing he came for.

---

## Source

Don Back, 2026-06-04_Mastermind. Outcome: a three-year governance dispute resolved in one executive committee meeting — *"it rolled out exactly as it was role-played by Claude."* Institutional document setup documented from the same session: loading the Act, bylaws, and meeting transcript as a structured package before rehearsal.
