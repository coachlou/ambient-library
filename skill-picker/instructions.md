# skill-picker

Builds or updates `skills-manifest.yaml` through a short natural language conversation. Goal: load only the skills this project actually needs.

## Why this matters

Every skill in the manifest is loaded into context at session start. Unnecessary skills waste tokens and slow responses. The manifest should be minimal and intentional.

## Steps

### 1. Discover available skills

Read `skills/SKILLS.md` to get the current skill catalog with descriptions. If that file is missing, scan `skills/*/SKILL.md` files directly.

### 2. Understand the project

Ask the user one focused question:

> "What does this project do, and what kinds of tasks will you mostly ask Claude to help with?"

Listen for signals:
- Code work → `code-review` likely useful
- Writing / content → content-focused skills
- Deployment / ops → ops skills
- Just getting started → minimal set is fine

If the project already has code, glance at the file structure (top-level `ls`) for additional signals before asking — it saves a round-trip.

### 3. Recommend a minimal manifest

Based on their answer, propose a manifest. Always include:
- `skill-loader` (required — orchestration layer, must always be present)
- `skill-system-manager` (recommended — enables updates)

Add other skills only if clearly relevant to what they described.

Show the proposed manifest and explain each inclusion in one line. Example:

```yaml
skills:
  - skill-loader          # required
  - skill-system-manager  # lets you update skills later
  - code-review           # you mentioned code reviews as a core workflow
```

Ask: "Does this look right, or would you like to add or remove anything?"

### 4. Write the manifest

Once confirmed, write `skills-manifest.yaml` to the project root:

```bash
# Write the confirmed manifest
```

Then run:

```bash
./setup-skills.sh
```

Confirm which skills were installed.

### 5. Done

Tell the user their skill manifest is configured and skills are ready. Mention they can update it anytime by saying "update my skill manifest" or editing `skills-manifest.yaml` directly and re-running `./setup-skills.sh`.

## Rules

- Never include a skill just because it exists. Default to the smallest useful set.
- `skill-loader` is non-negotiable — always in the manifest.
- If the user asks for a skill that doesn't exist in `skills/`, tell them and offer to add it via the skill creation workflow (see `docs/MANAGEMENT.md`).
- Don't re-run setup-skills.sh if the manifest didn't change.
