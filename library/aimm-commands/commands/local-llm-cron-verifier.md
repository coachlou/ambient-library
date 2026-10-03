---
name: Local LLM Cron Verifier
type: command
description: If any of these aren't true, consider the cloud API batch-processing path instead (50% discount on Claude and OpenAI APIs for batch/async jobs).
trigger: /aimm:local-llm-cron-verifier
source-sessions:
- 2026-05-07_Mastermind
---

# Command: Local LLM Cron Verifier

**What it produces:** A scheduled, local-LLM-powered verification pipeline that checks a data source against an authoritative reference on a recurring schedule and flags exceptions — without sending sensitive data to a cloud provider and without manual effort after initial setup.

**When to use:** When you have a structured verification task that recurs on a schedule, involves data you'd rather keep local (client records, internal rosters, proprietary databases), and where the verification logic is deterministic enough that a 7B model handles it fine.

**Modeled on:** Scott Delinger's contact verification system (2026-05-07) — local Mistral 7B + Ollama + Python + cron, saving his EA a week of annual work.

---

## When This Pattern Fits

- A spreadsheet or database that drifts over time against authoritative websites or sources
- Verification logic that is structured and deterministic (not nuanced judgment)
- Data containing PII, proprietary client info, or IP you won't send to a cloud API
- A task that can run unattended at low-traffic hours and deliver a flagged exceptions report

If any of these aren't true, consider the cloud API batch-processing path instead (50% discount on Claude and OpenAI APIs for batch/async jobs).

---

## Architecture

```
[Source data] → [Python script] → [Ollama / local model] → [Comparison logic] → [Exceptions tab / report]
                      ↑
                 [Cron job — monthly or weekly]
```

**Components:**
- **Ollama** — local model server; runs Mistral 7B (or any compatible model) on your machine
- **Python script** — checks if Ollama is running, fetches fresh data from each source, compares to your spreadsheet/database, writes a results tab with Confirmed/Changed flags
- **Bash wrapper** — ensures dependencies are live before the Python script runs
- **Cron job** — schedules the run; outputs to a log file

---

## Prompt to Build the Script

Use Claude (cloud) to build the implementation:

```
I want to build a local LLM verification pipeline using Ollama and Python.

**The task:**
[Describe the verification job — what data are you checking, against what source, and what does a "match" vs. "change" look like]

**Data source (what I'm checking):**
[Spreadsheet columns, CSV format, database table, etc.]

**Reference source (what I'm checking against):**
[Website URLs, internal docs, API endpoints, etc.]

**Output format:**
[What I want back — a new spreadsheet tab, a report file, a CSV with flags, etc.]

**Local model:** Mistral 7B via Ollama (or specify a different model)
**Platform:** [Mac / Linux / Windows]

Build me:
1. A Python script that checks if Ollama is running, processes each item, compares it to the reference source, and writes the output
2. A bash wrapper that handles startup checks and logging
3. A cron entry that schedules this to run monthly at 3:01am

Include error handling so a failed check on one item doesn't kill the whole run. Output a structured log.
```

---

## Cron Setup

```bash
# Open crontab
crontab -e

# Run monthly on the 1st at 3:01am, log to file
1 3 1 * * /bin/bash /path/to/wrapper.sh >> /var/log/verifier.log 2>&1
```

**Timing note:** Never schedule at midnight to 3am. DST transitions can cause midnight-3am cron jobs to run twice (fall-back) or not at all (spring-forward). 3:01am is the conventional safe window.

---

## Model Selection Notes

- **7B models (Mistral, Gemma 3 4B) are sufficient** for structured comparison tasks. Do not use Opus or GPT-4 for this — overkill costs money and adds latency for work that doesn't need reasoning.
- **On Mac:** Always pull the MLX-optimized version of the model in Ollama. Approximately 2× faster than the non-optimized equivalent on Apple Silicon.
- **Model too slow / not enough RAM:** Use OpenRouter for access to larger open-source models without local hardware requirements. Most models available at-cost or free.
- **Sensitive data concern:** If the data is too sensitive even for Ollama's local inference (edge case), structure the pipeline so only non-sensitive fields are processed by the LLM and sensitive fields are handled by deterministic code.

---

## Example Output Tab

| Contact | Spreadsheet Title | Verified Title | Status | Notes |
|---|---|---|---|---|
| J. Smith | VP Research | VP Research | ✓ Confirmed | |
| M. Jones | CIO | Director of IT | ⚠ Changed | Website updated 2026-05 |
| T. Lee | Provost | [not found] | ⚠ Changed | No longer listed on site |

EA or data owner reviews only the ⚠ Changed rows.

---

## Source

- Scott Delinger, 2026-05-07_Mastermind — demonstrated a local Mistral 7B contact-verification cron job built in 2 days. Result: 111 of 132 contacts confirmed automatically; EA only reviewed 10 exceptions vs. a week of manual checking. First live demo of a local model handling a real production task for a AIMM member.
- Lou, 2026-05-28_Mastermind — noted the expert-profile-update use case: a cron job that periodically researches each expert's recent publications, positions, and interviews to keep AI-briefed "council" files current.
- Lou, 2026-05-07_Mastermind — added OpenRouter, batch API (50% discount), and MLX optimization notes during the session debrief.
