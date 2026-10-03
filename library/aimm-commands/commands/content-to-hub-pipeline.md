---
name: Content-to-Hub Pipeline
type: command
description: Converts any productive AI working session into a published, indexed teaching block on the AIMM hub.
trigger: /aimm:content-to-hub-pipeline
source-sessions:
- 2026-05-28_Mastermind
- 2026-04-30_Mastermind
---

# Content-to-Hub Pipeline

Converts any productive AI working session into a published, indexed teaching block on the AIMM hub. This is a documented workflow — not a single prompt — that runs in five stages from raw session to live artifact.

**When to use:** At the end of any working session (mastermind, build session, client session, R&D session) where something teachable was produced. The target cycle time is under 10 minutes from session end to live.

---

## The Five Stages

### Stage 1 — Process the Conversation

Trigger session processing immediately after the session ends, while context is fresh.

**Prompt:**
```
Process this conversation. Produce:
1. A structured session recap (150–250 words): what was worked on, key decisions made, outputs produced
2. 2–5 extracted insights: ideas, frameworks, or approaches that have standalone value
3. One "most teachable moment" candidate: the single thing a reader could take and use today

Format each insight as: [Title] | [One-sentence summary] | [Why it matters]
Flag the teaching block candidate with a ★
```

Run this on the full conversation export (paste the chat, or use `/process-transcript` if it's a mastermind session with a transcript file).

---

### Stage 2 — Extract the Teaching Block

Take the ★ candidate from Stage 1 and expand it into the teaching block format.

**Prompt:**
```
Expand the teaching block candidate into a standalone publishable artifact.

Teaching block format:
- **The Problem** (1–2 sentences): what situation is this for?
- **The Mechanism** (2–3 sentences): what's the insight or approach?
- **The Steps / Template**: numbered steps or a prompt template the reader can copy
- **One Example**: a concrete instance from this session
- **You Can Do This Today**: one sentence — what's the immediate action?

Length: 200–350 words. This is not an article. Ship the useful thing, not the polished treatment.
```

---

### Stage 3 — Upload to the Hub

Convert the teaching block to HTML and publish to here.now.

```bash
# From LKB-Vault root:
bash "/Volumes/Extreme Pro/users/loudalo/GitHub/aimm-shared-repo/look-over-my-shoulder/critical-partner/herenow/publish-hub.sh" \
  /path/to/teaching-block.md
```

Or use the teaching-block button in Claude Code if configured.

The publish script handles: markdown → HTML render, copy to herenow/, hub index update, and live deployment to `aimmhub.coachlou.com`.

---

### Stage 4 — Update the Vault

Write the recap and insights to the vault so they compound with existing knowledge.

- Session recap → `wiki/mastermind/sessions/YYYY-MM-DD_[Session-Name].md`
- Each insight (score ≥ 70) → `wiki/mastermind/insights/Insight - [Title].md`
- Log the ingest in `log.md`
- Run lint: `node scripts/validate-vault.mjs --regenerate-backlinks`

If this was a mastermind session, use the `process-transcript` skill instead of running these steps manually — it handles all four.

---

### Stage 5 — Close the Loop

Verify the hub is live, the vault is clean, and the teaching block is indexed.

Checklist:
- [ ] Teaching block accessible at hub URL
- [ ] Hub index updated (catalog shows the new item)
- [ ] Session recap in vault
- [ ] Insights extracted and backlinks regenerated
- [ ] `log.md` updated with this session

---

## Design Notes

The pipeline's value is in making publishing the natural completion of a session, not a separate effort scheduled later. Each stage feeds the next. The teaching block is the minimum viable artifact — it ships the useful thing now. The vault entry is the compounding artifact — it connects the session's outputs to the rest of the knowledge base.

Don't wait for a "polished" version. The teaching block is the polished version, at the right grain size.

## Source

- PowerUp AI Mastermind Recap — 2026-05-28 (Lou D'Alo — teaching-block pipeline and here.now hub delivery model)
- April 30, 2026 — AIMM Mastermind (Lou D'Alo — end-of-session knowledge extraction pattern)
