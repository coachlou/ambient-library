# token-activity-graph

Builds an interactive self-contained HTML visualization of token usage across Claude Code sessions, aggregated by day, app, and model, with cost calculated from live pricing.

---

## Flow

**1. Verify Claude Code stats exist**

Read `~/.claude/stats-cache.json`. Required fields:
- `dailyModelTokens` — array of `{date, tokensByModel}` objects
- `modelUsage` — object of per-model stats

Exit with "No Claude Code session data found" if missing or empty.

**2. Fetch live pricing**

`GET https://models.dev/api.json` and filter to Claude models. Extract per-model:
- `input_price`, `output_price`, `cache_read_price`, `cache_creation_price` ($/1M tokens)

If cache prices missing, derive: `cache_read = input × 0.1`, `cache_write = cache_read × 3`.

**3. Transform to graph format**

Aggregate dailyModelTokens by date and app into:

```json
{
  "days": {
    "YYYY-MM-DD": {
      "app_name": {
        "in": input_tokens,
        "out": output_tokens,
        "cr": cache_read_tokens,
        "cw": cache_write_tokens,
        "cost": cost_usd,
        "calls": call_count
      }
    }
  },
  "models": {
    "YYYY-MM-DD": {
      "app_name": {
        "model_name": { "in", "out", "cr", "cw", "cost", "calls" }
      }
    }
  }
}
```

**Token split estimation:** If source provides only totals (no split), estimate input 30% / output 70%.

Cost = `(in × in_price + out × out_price + cr × cr_price + cw × cw_price) ÷ 1,000,000`

**4. Build self-contained HTML**

Create `token-graph.html`:

- **CSS variables** (light/dark @media prefers-color-scheme):
  - `--paper`: #fbfdfd (light), #0f1117 (dark)
  - `--ink`: #202126 (light), #e6edf3 (dark)
  - `--muted`: #6b7280 (light), #8b949e (dark)

- **Font:** SFMono-Regular, Consolas, Liberation Mono (monospace, tabular-nums)

- **Inline data:** `<script type="application/json" id="token-activity-data">` with graph format JSON

- **Renderer:** Inline `${CLAUDE_PLUGIN_ROOT}/library/token-activity-graph/graph.js` verbatim as a `<script>` after the data block. Never fetch it from the web.

- **Mount:** `<div data-token-activity></div>` — renderer auto-mounts

**5. Open in browser**

File must run in a live browser (file:// blocks JS in static preview). Use `open token-graph.html` or drag into browser.

---

## Gotchas

- **graph.js is a pinned, reviewed fork** — inline the bundled copy as-is. Upstream (bentossell.com) falls back to fetching its author's own usage data when inline data is missing or invalid, which would chart someone else's tokens as yours; the fork removes that and shows an error instead. Never swap in a fresh download without re-reviewing it; any re-pin must pass `node ${CLAUDE_PLUGIN_ROOT}/library/token-activity-graph/check-graph.js ${CLAUDE_PLUGIN_ROOT}/library/token-activity-graph/graph.js` (exit 0).
- **Validate the data block before inlining** — `json.loads` it (or `JSON.parse`) and confirm `days` is non-empty. An invalid block now renders an error, not a graph.
- **Claude Code only** — other agents (Codex, Cline, etc.) lack aggregated stats. Skip unless user explicitly includes others.
- **One self-contained file** — move it anywhere, it still works (all data inlined).
- **Cache pricing rule:** Mark "3x" as a comment if derived.
- **Local file limitations** — browsers block JS on file:// URLs in some contexts. Instruct user to open in browser directly.

---

## Data source notes

- **dailyModelTokens:** Total tokens per model per day (no input/output split).
- **modelUsage:** Cumulative per-model counts used for pricing reference.
- **Graph input/output split:** Estimated 30/70 when source lacks split. Refine if actual breakdown is available.

---

## Output

Confirm: `"Token activity graph ready at [path]. Open in your browser — shows usage by day, app, and model with live list pricing."`
