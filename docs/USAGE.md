# Using Ambient Library Skills

Once [installed](INSTALLATION.md), skills are available in your Claude sessions. You never need to think about how they load — just use them naturally.

## The Three Built-In Skills

### Skill Loader (Always Active)

The invisible orchestration layer. It:
- Resolves skill paths automatically
- Merges project rules from `CLAUDE.md` / `AGENTS.md`
- Caches skills for your session
- Makes everything feel transparent

**You don't invoke this directly.** It runs automatically.

### Skill System Manager

Manages the skill system. Use when you need to:

**Update to the latest skills:**
```
"Update my skills to the latest version"
"Refresh the skill system"
```

**Add a new skill to the project:**
```
"Add the deploy skill to this project"
```

**Refresh skill pointers:**
```
"Refresh the skill system"
```

The manager will:
1. Ask for quick confirmation
2. Run the refresh silently
3. Reply: "Skill system is now up to date and ready."

### Code Review

Performs thorough code reviews covering:

- **Correctness** — logic errors, edge cases, off-by-one bugs
- **Security** — injection risks, auth gaps, exposed secrets
- **Performance** — unnecessary allocations, N+1 queries, blocking calls
- **Readability** — naming, structure, comments
- **Project standards** — adherence to patterns in `CLAUDE.md`

**Use it:**
```
"Review this code"
"Code review for src/auth.ts"
"Check this for security issues"
```

The skill will return:
- Summary (2–3 sentences)
- Findings by severity (critical/major/minor) with file:line and fixes
- Optional praise for well-written sections

## Adding Custom Skills

Want a new skill? See [MANAGEMENT.md](MANAGEMENT.md).

## Workflow Examples

### Example 1: Quick Code Review

```
You: "Review the changes in api/handlers.ts for security issues"
Claude: [Review loads Code Review skill, scans your files, returns findings]
```

### Example 2: Update Skills

```
You: "Update my skills to the latest version"
Claude: [System Manager confirms, refreshes, syncs]
You: [New skills are now available]
```

### Example 3: Custom Workflow with Merged Rules

When you add a skill, Skill Loader automatically merges any rules from your project's `CLAUDE.md`:

```
# In your project's CLAUDE.md:
## Code Review Standards
- Always check for SQL injection
- Flag any use of weak crypto
- Require test coverage for new endpoints
```

When Code Review runs, it includes these standards automatically.

## Skill Discovery

To see available skills, check:

```bash
ls -la .agents/skills/
```

Each folder is an active skill. Look at the `SKILL.md` file to understand what each one does:

```bash
cat .agents/skills/code-review/SKILL.md
```

## Questions?

- **How do I add a skill?** → [MANAGEMENT.md](MANAGEMENT.md)
- **Something's broken?** → [INSTALLATION.md#Troubleshooting](INSTALLATION.md#troubleshooting)
- **How does this work under the hood?** → [ambient-library/README.md](../README.md)
