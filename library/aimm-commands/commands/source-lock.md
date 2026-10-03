---
name: The Source Lock
type: command
description: Constrain Claude to a specific authoritative source, kills hallucinated citations by treating one URL as ground truth. From the May 28, 2026 AIMM session, Lou writing a CLAUDE.md instruction live to stop Claude from inventing regulatory citations in Joanna's legal documents.
trigger: /aimm:source-lock
source-sessions:
- 2026-05-28_Mastermind
---

# The Source Lock

Constrain Claude to a specific authoritative source, kills hallucinated citations by treating one URL as ground truth. From the May 28, 2026 AIMM session, Lou writing a CLAUDE.md instruction live to stop Claude from inventing regulatory citations in Joanna's legal documents.

---

$ARGUMENTS

If no source URL was provided above, ask me which URL (and what type of information) before proceeding.

For any [TYPE OF INFORMATION, e.g., regulations, citations, product specs, policy] in this work, follow these rules:

- Only pull answers from this URL and its subfolders: [GROUND-TRUTH URL, paste or confirm from $ARGUMENTS]
- Treat that website as ground truth.
- Do NOT use your pretraining or general internet search for this information unless I explicitly ask you to.
- When you cite something, include the link so I can verify it myself.
- If something is ambiguous or you can't find it in the source, tell me, do not guess or fill the gap.

[OPTIONAL, add more sources:]
- Also treat this as ground truth: [SECOND URL]

Confirm you understand these constraints before we proceed. Then ask me what I need.

## Source

- Session recap, 2026-05-28
