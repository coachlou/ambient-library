# Session Observatory

Build a Langfuse-style observability dashboard from local AI coding session
logs. Stdlib-only Python parser + single-file HTML dashboard. No server, no
external dependencies.

## Security constraint

**Never print secrets, keys or full prompt text. Snippets max 10 words, with
keys, paths, URLs and long ids stripped.**

## Output directory

`~/Downloads/ai-observability/` — create if missing.

## Step 1: Parser (`parse_sessions.py`)

Write a Python script (stdlib only: `json`, `glob`, `os`, `re`,
`collections`, `datetime`, `pathlib`, `sys`) that:

### Data sources

1. **Claude Code**: `~/.claude/projects/*/*.jsonl` — one JSONL file per
   session. Event types: `user` (prompts + tool results), `assistant` (model
   responses with tool_use blocks and usage), `queue-operation` (enqueue =
   prompt). Subagent logs are separate files under
   `~/.claude/projects/*/*/subagents/*.jsonl`; parse them too with
   `is_subagent=True`.
2. **Codex**: `~/.codex/sessions/*.jsonl` — event types: `session_meta`,
   `event_msg`, `token_usage_record`, `response_item`, `turn_context`. When
   `session_meta` has no model, take it from `turn_context.payload.model` and
   re-key any `unknown|day` token entries.

### 7-day window

Only include sessions whose `start` timestamp falls within the last 7 days.
Skip individual events older than the window even within qualifying files.

### Per-session extraction

Each session produces:

| Field | Source |
|-------|--------|
| `session_id` | Filename stem |
| `harness` | `"claude-code"` or `"codex"` |
| `project` | Last 2 meaningful path components of `cwd` (strip `/Users/<user>`, `/Documents`, `/Volumes/…`, `/private/tmp`, `/var`) |
| `start` / `end` | Earliest / latest event timestamp |
| `models` | Set of model IDs from assistant messages |
| `prompts` | Sanitized snippets (max 10 words, keys/URLs/paths/IDs redacted) |
| `tool_calls` | `(name, timestamp, is_error, error_snippet)` — paired via `tool_use_id` with duration |
| `tokens` | By `model\|day` key: `{input, output, cache_read, cache_write}`. `input` is uncached input only: Codex `input_tokens` includes `cached_input_tokens`, so store `input_tokens - cached_input_tokens`. Session and chart totals sum all four fields. |
| `is_subagent` | `isSidechain` flag, or the file lives under `subagents/` |
| `kind` | `subagent` if is_subagent; `automated` if task_type is `automation` or cwd matches `^/private/tmp\|^/tmp/\|/T/\|judge`; else `interactive` |
| `turns` | `(role, ts, tool_name, is_error, duration_ms)` |

### Prompt classification (`classify_prompt`)

Classify the first *typed* prompt (skip empty prompts and injected harness
turns that start with `<`). `automation` first (cx distill/search notes,
query rewriters, judge/grader prompts), then word-start keyword match in
order: `publish`, `newsletter`, `plugin`, `status`, `debug`, `build`,
`review`, `writing`, `UI`, `research`, else `other`. Report the `other`
share each week (10-26: 4.2% overall).

### Error types (`error_type`)

First match on the error snippet: `tool_disabled`, `hook_blocked`,
`invalid_args`, `permission_denied`, `timeout`, `not_found`,
`exit_code_nonzero`, `no_op`, else `other` (`unknown` when empty). Applies to
every tool, not only Bash.

### Aggregation (`compute_summary`)

The summary object contains:

- **Globals**: `total_sessions`, `total_prompts`, `total_tool_calls`,
  `total_failed_tool_calls`, `period`, `sessions_by_harness`
- **Time series**: `sessions_per_day` (zero-filled for every day in the
  period), `tokens_by_model_day`
- **Kinds**: `sessions_by_kind` (interactive / automated / subagent)
- **Tool analytics**: `tool_calls_by_tool`, `failed_by_tool`,
  `failed_by_tool_error` (tool → error_type → count)
- **Latency**: `latency_overall` `{p50, p95, p99, max}` from tool call
  durations
- **Top lists**: top 10 sessions by tokens, top 10 by duration
- **Retries**: consecutive same-tool failures ≥ 3 per session
- **Classification**: `task_types`, `sessions_by_project`
- **Per-project details** (`project_details`): `sessions`, `tokens`,
  `errors`, `tool_calls`, `retries`, `error_rate`, `top_model`, `top_task`,
  `models` dict, `task_types` dict, `total_prompts`, `interactive_sessions`
- **Traces**: every session, each with: `session_id`, `harness`,
  `project`, `start`, `duration_s`, `prompts`, `tool_calls`, `errors`,
  `total_tokens`, `models`, `task_type`, `is_subagent`, `kind`,
  `first_prompt`. Automated traces beyond the top 200 by tokens drop
  `turns`, `prompt_snippets` and `end` to keep the file small.
- **Subagent count**

Write to `harness-summary.json`. Run with `python3 -I parse_sessions.py`.

## Step 2: Dashboard (`dashboard.html`)

Single-file HTML with the JSON injected inline as `const DATA = {…};`.

### Summary strip (reactive)

Stat cards that **recalculate on every filter change**:

| Stat | Calculation |
|------|-------------|
| Interactive | Count of `kind == interactive` over traces filtered by everything except kind |
| Automated | Same for `automated`; subtitle shows the subagent count |
| Sessions shown | `filtered.length` |
| Prompts | Sum of `t.prompts` across filtered traces |
| Tool Calls | Sum of `t.tool_calls` across filtered traces |
| Error Rate | `errors / toolCalls` with failed count subtitle |
| Total Tokens | Sum of `t.total_tokens` across filtered traces |
| Session Length p95 | From `t.duration_s` (seconds) of filtered traces, formatted with `fmtDur` (s/m/h), p50 subtitle. Do not multiply by 1000 or use `fmtMs`. |

A shared `getFilteredTraces()` function applies all Traces-tab filters and is
called by both `renderTraces()` and `updateSummaryStrip()`.

### Tabs

#### Traces
Sortable table. Columns: Harness, Project, Start, Duration,
Prompts, Tool Calls, Errors, Tokens, Models, Type.

Filters (all trigger summary strip recalculation):
- Text search (substring across all fields)
- Model dropdown
- Task type dropdown
- Kind tags: checkbox per kind (Interactive checked by default) plus "All tags"; Traces show only sessions whose kind is checked
- **Interactive only — 2+ prompts** (checkbox)

Click row → detail pane: duration, prompts, tool calls, errors, tokens,
models, task type, first prompt snippet, tool call timeline (or a note when
the trace has no `turns`).

#### Projects
Bar chart with detail rows per project.

Controls:
- Sort by: sessions / tokens / errors / retries / error_rate
- Hide eval/judge (checkbox — regex: `/judge|\/T\/|\/tmp|private/`)
- **Interactive only — 2+ prompts** (checkbox — filters to projects with
  `interactive_sessions > 0`)

Each row: bar scaled to sort metric, session count, tokens, tool calls,
errors (with rate), retries, top model, top task.

#### Tokens
Stacked bar chart: tokens by model per day (input, output, cache_read,
cache_write).

#### Models
Bar chart: sessions per model.

#### Latency
Bar chart: p95 latency per tool. `shortToolName()` strips MCP UUID prefixes.
Right-hand values: `min-width: 80px`, `white-space: nowrap`.

#### Errors
Bar chart: failures per tool with failure rate percentage.

#### Health
Retry storms table (sessions with 3+ consecutive same-tool retries).
Subagent session count.

#### Report
Weekly recommendations kept in a separate `REPORT` const (not inside DATA).
Each item: `{section, id, priority, status, title, issue, action, benefit,
blast, evidence}`. Priority is `high` (must do), `medium` (should do) or
`low` (could do), shown as a badge. Cards render Issue / Action / Benefit /
Blast radius rows, Approve / Hold / Reject buttons and a notes field.
Decisions persist in the artifact's `db` collection `decisions` (declare
`db` on first publish; omit `capabilities` on republish). A "Copy decisions
for Claude" button exports approved/held/rejected items with notes.

Recurring item **w-retry**: compare this week's retries with the previous
baseline and recommend tightening the 3-failure rule if they didn't drop.
Baseline (week ending 2026-10-25): 102 retries across 23 sessions; top
024e3e0e (18), b36e7f3d (16), f00e64ea (14).

### Theming

CSS custom properties on `:root` with full light/dark mode support via
`prefers-color-scheme` and `data-theme`. System font stack + monospace data
font.

### Data injection

The JSON is embedded via string-index splice, **not regex** (JSON contains
`\u` escape sequences that break `re.sub`):

```python
marker = 'const DATA = '
idx = html.index(marker)
start = idx + len(marker)
depth = 0; i = start
while i < len(html):
    c = html[i]
    if c == '{': depth += 1
    elif c == '}':
        depth -= 1
        if depth == 0: end = i + 1; break
    elif c == '"':
        i += 1
        while i < len(html) and html[i] != '"':
            if html[i] == '\\': i += 1
            i += 1
    i += 1
html = html[:start] + new_data + html[end:]
```

## Step 3: HARNESS.md

Generate a data-driven proposals document covering:

1. **Model routing** — keep/change per model, with session counts
2. **Tools — keep / fix / cut** — by call count and failure rate
3. **Skills** — proposed skills for repeated task types (3+ sessions)
4. **Guardrails** — top 3 failure patterns with proposed CLAUDE.md rules
5. **Budget** — top 5 token sinks with optimization proposals

Before writing a cause, check `failed_by_tool_error` and a sample of error
snippets; don't guess from the tool name. Mark proposals as unapproved
unless the user approved them in the Report tab, and list applied changes
separately.

## Step 4: Verify

Run the parser, inject data, serve locally (`python3 -m http.server 8789`),
and verify all tabs render, filters work, and the summary strip reacts to
filter changes.
