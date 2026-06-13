---
description: Use for all ambient-library operations. Triggers on setting up ambient-library in a project ("set up ambient-library", "install skills", "initialize the skill system"), configuring project skills ("configure my skills", "which skills do I need"), updating or managing skills ("update skills", "refresh skills", "add/remove a skill"), and code review ("review this code", "code review", "check for security issues").
---

# ambient

You are the ambient router. Your bundled instructions and subskills live in
`${CLAUDE_SKILL_DIR}`. Read the router instructions and follow them:

**Read `${CLAUDE_SKILL_DIR}/instructions.md` and execute it for this request.**

That file routes the request to the correct subskill in
`${CLAUDE_SKILL_DIR}/subskills/` and tells you how to handle domain skills in
`${CLAUDE_SKILL_DIR}/library/`. Do not guess — read it first.
