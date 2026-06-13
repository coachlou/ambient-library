# Code Review Instructions

Perform a thorough, constructive code review covering:

1. **Correctness** — logic errors, edge cases, off-by-one errors
2. **Security** — injection risks, auth gaps, exposed secrets, OWASP top 10
3. **Performance** — unnecessary allocations, N+1 queries, blocking calls
4. **Readability** — naming, structure, comment quality
5. **Project standards** — adherence to patterns in CLAUDE.md / AGENTS.md

Output format:
- Summary paragraph (2–3 sentences)
- Findings list: severity (critical/major/minor), file:line, description, suggested fix
- Optional: positive callouts for well-written sections
