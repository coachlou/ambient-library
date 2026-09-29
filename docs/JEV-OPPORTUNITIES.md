# JEV Opportunities in the Library

Survey of every skill, script, and the router for steps that could be upgraded with
**Jev** (TypeSafe System One) — a small classification model that returns typed
judgments + probabilities + confidence in ~100ms.

**Status:** findings only, recorded 2026-09-20. No integrations yet. Deferred next
steps are listed at the end.

**Live demos:** [`library/jev-arcade/`](../library/jev-arcade/README.md) — seven
working examples mapped to canonical skills (gmail-triage, meeting-nuggets,
aimm-writing-team / editorial-desk, voice-crm-pipeline, skill-evals /
deep-comprehension-assessment, conversation-ip-extractor, ideal-client-generator).
Those seven are *not* repeated as recommendations below except where the arcade
misses deeper hooks.

## What "Jev-shaped" means

A job qualifies when it is a **small repeated judgment with a definable answer set**
where a probability would change the next step:

| Type | Shape | Example |
|------|-------|---------|
| **Choice** | pick 1 from a fixed option set | severity: blocker / major / minor / nit |
| **Noul** | boolean / presence | does acting on this finding change the outcome? |
| **Score** | rubric level against written anchors | relevance 0–10 with a ≥6 gate |

It is **not** Jev-shaped when the step is freeform generation, multi-step reasoning,
or math. Jev cannot count or do date arithmetic — code owns that.

Cost context: `jev-latest` at **$0.042 per million input tokens**, output free;
many independent questions batch into one request. Question design rules (atomic
judgments, contrastive `what` / `not_for` / `examples`, `not_stated` options, code
does all math) follow the [TypeSafe docs](https://docs.typesafe.ai) and the arcade's
"Show the wires" panel.

---

## Tier 1 — strongest fits

Batched closed-set judgment with a clear cost, speed, quality, or receipts win.

| Skill | Judgment step | Fit | Primary benefit |
|-------|--------------|-----|-----------------|
| **cognitive-mirror** (Harvest) | Per decision moment: `decision_type` (7-way), domain, confidence band, trivial-decision filter — scheduled runs over many conversations | Choice + Noul, batched | Cost + receipts |
| **paradigm-collision-engine** | Relevance 0–10 over 400+ paradigms (≥6 generation gate); tournament rubric 0–2 ×3 criteria; head-to-head picks | Score + Choice | Cost/speed — the skill's biggest cost center (~30–60 min subagent batch collapses to one request; generation only for survivors) |
| **audit-fix** | Step 2 "earn filter": per finding — does acting on this change the outcome? Discard reason when not | Noul | Receipts — independent judge with probabilities instead of the model filtering its own findings |
| **audit-mcp** | Per-finding false-positive triage (node_modules placeholders, transitive-dep inflation) + PASS / PASS WITH CAVEATS / FAIL verdict table | Noul + Choice | Quality — applies written gotchas uniformly to a security gate; probability gates install-or-not |
| **gmail-manager** | Same classification problem as gmail-triage, wider answer set: promo / newsletter / outreach Nouls + urgent / action / FYI / quick-decision Choice | Noul + Choice | Cost/speed — shares one question bank with gmail-triage |
| **brand-writing-team** | Independent ≥9 / <7 role gate scoring; zero-fabrication and source-verified binary gates (skill warns "the whole system breaks if roles inflate their scores") | Score + Noul | Receipts — breaks judge-and-defendant contamination |
| **teaching-block-synthesized** | ~40-item pre-finalize audit checklist; heading spoiler-vs-narrate classification; skill itself says "run three judges in parallel and take the median" | Noul fan-out + Choice | Receipts — Jev *is* the cheap multi-judge panel the skill already asks for |
| **voice-profile-trainer** | Stage 5 seven-item authentication checklist + AI-telltales blacklist presence per draft (≥5/7 threshold stays in code) | Noul | Receipts + speed — turns aspirational "70–80% similarity" into per-item receipts |
| **trello-pipeline** (agent prompts, not the `.py` scripts) | APPROVED / NEEDS_REVISION; P0/P1/P2; issue severity; vision-alignment 1–10 | Choice + Score | Receipts — currently uncalibrated single-judge scores per card |
| **skill-evals** (deeper than arcade) | Per-assertion Noul fan-out across an entire `evals.json` in one request; keeps the skill's "no scores, PASS/FAIL only" rule | Noul | Cost — a skill's full eval file graded in one call |
| **enrich-prompt** | Enrich-or-skip pre-gate: "would enrichment change the substance of the answer?" (has an eval case) | Noul | Quality + speed — eval-backed binary gate on every invocation |

## Tier 2 — good fits

Real judgment with moderate leverage.

- **aimm-commands**
  - `capture-bin-catalyst` — per-note green / yellow / red rating + duplicate Noul over hundreds of fragments (batched).
  - `transcript-miner` — signal strength 1–3 + nugget type over already-flagged moments; drop Signal-1 gated by probability.
  - `era-locator` — Era 1–8 assignment (closed set; opening prose stays with the main LLM).
  - `iteration-compressor` — high / medium / low compression bands against written anchors.
  - `brand-alignment-audit` — 4-dimension 1–10 scores as an *independent* scorer; contradiction Noul pass.
- **conversation-consolidation-system** — Step 2 topic-cluster assignment (explicitly a non-summarizing sort); low P(assignment) → human granularity review. Hundreds of conversations, weekly.
- **deep-mirror** — audit classify Validated / Drift / Anchoring-suspect; 6-category triage of grep'd candidate lines. Counting ("3+ dated occurrences") stays in code.
- **extract-codify-patterns** — output type (insight / framework / skill / rule / tool / combination) + skill-vs-command promotion bar — decides which artifact tree gets built.
- **cognitive-operations** — recipe routing (category ~10-way; wrong route loads the 606-line `recipes.md`) + stuck-type {lens, operation, recipe}.
- **fresh-eyes** — walker hiccup severity {BLOCKER, FRICTION, COSMETIC} batched across the ledger; fix-free-vs-log Noul.
- **gauntlet** — per-criterion pass/fail Noul over already-extracted evidence + failure severity; orchestrator gates on probabilities. (Artifact inspection stays with the critic LLM.)
- **graphify** — edge class {EXTRACTED, INFERRED, AMBIGUOUS} — the extraction spec *documents* rubric collapse (>50% at 0.5); vocab-token relevance fan-out for query Step 0 (fixed graph vocab, "do not invent tokens").
- **leaderize-storytelling-framework** — framework mapping Choice (Transformation Arc / ABT / Case Study); 6 ICP checkbox Nouls; 5-Moments detection (code counts the ≥2 threshold).
- **solofactory** — `interview.mjs` coverage recheck: 13 keys × {missing, partial, complete} after every turn in ~100ms without burning an agent turn; code keeps the fail-closed `ready` check.
- **project-index** — status-label Choice from the run's 3–6 label set + "metadata too thin to describe" Noul — replaces subagent fan-out at ≥40 folders. One-sentence descriptions = generation (keep with LLM); recency = date math (code).
- **polyglot-language-coach** — trigger Noul (practice vs quoted/utility text) + ambiguity gate; the skill's "if interpretation B is even 20% likely, still ask" is a probability policy Jev speaks natively. Correction prose stays with the main LLM.
- **deep-comprehension-assessment** — 4-dimension weighted rubric Score (30/25/25/20) batched per student answer + gap-flag Nouls (invented info, evidence missing). The arcade grades artifacts; this is the per-answer fan-out.

## Tier 3 — cross-cutting / architectural

1. **Shared severity question set** — `session` reviewer, `trello-pipeline` reviewer,
   and `software-dev-factory` review-guide all grade findings against
   {blocker, major, minor, nit}. One shared Jev question bank serves all three.
   *SDIF caveat:* its gates are deliberately deterministic / fail-closed
   (`mintAgentVerdict`, `evaluateQuality`, `diagnose.ts` are code by design). Jev may
   only supply upstream severity *with probability*; the human verdict stays
   authoritative. Replacing the deterministic gates would violate the factory's own
   trust chain.
2. **Catalog router** (`.aai/skills/load.md` step 2): pick 1 enabled skill from
   `catalog.yaml` one-line descriptions as a Choice (answer set = enabled names +
   explicit `none`), optionally gated by a prior Noul. Defensible wins are
   **calibration, misroute receipts feeding `skill-evals`, and cost** — not a
   guaranteed accuracy jump over the LLM already reading the same file. Enabled-set
   building and the `none` fallback stay deterministic code. Confidence: medium.
3. **gmail-triage arcade gaps** — thread already-handled Noul fan-out ("did Lou send
   the last reply?"), triage-queue priority Score (code does the sort), recommended
   action Choice (`archive|reply|skip`) per queue email. Plus one shared classifier
   with gmail-manager.
4. **meeting-nuggets arcade gaps** — callout-type Choice per topic section
   (`hot_take | what_this_means | go_deeper | none`), Community Corner worth Noul
   (code picks top 2–4), topic-clustering input (pairwise same-topic Noul; code
   merges to 3–5), draft quality gates ("reads as minutes?", "generic bolded opener?").

## Non-opportunities

Verified during the survey — leave these alone.

**Deterministic by design** (Jev would add cost and weaken receipts):

- `distro-kit` validate / selfcheck — semver, file presence, DEPENDS membership.
- `wbs-toolkit` `wbs.py` gates — verify-command exit codes; "an agent may verify, but
  the owner authorizes."
- `capture-chat/export-conversation.py` — JSONL field predicates.
- `aimm-newsletter/scripts/resolve.py` — "which folder am I working in must be
  deterministic" is a stated design invariant; recipient gate is human.
- `ambient-folder` / `context-mgr` installers — file-existence checks; user decides
  overwrites.
- `skill-auditor` — explicitly engineered to have "no model judgment in the findings."
- `software-dev-factory` `evaluateQuality` / verdict mint / `diagnose.ts` —
  deliberately code-only, fail-closed.
- `project-index/scripts/scan.sh` + `build_html.py` — mechanical parsing.
- `trello_ops.py` / `trello_client.py` / `setup_board.py` — API plumbing; card type
  from workflow metadata.

**Date / count math** (Jev cannot — code must):

- `trigger-runner` cadence elapsed ("weekly, last stamped 8+ days ago").
- Session / context stale-Doing (>4h) and stale-lock checks.
- project-index recency thresholds.
- Any "3+ dated occurrences" / histogram / tally check.

**Pure generation or orchestration** (main LLM stays):

- `writer`, `project-brief`, `ireport`, `gears-broadcast` send gate,
  `multi-model-debate-live`, `deep-field` (essay), `aimm-newsletter` templating.
- Interview stretches of `irreplaceable-edge`, `grill`, `geo-authority-architect` —
  deep contextual conversation; only their checklist-style tests (listed in Tier 2 /
  survey) are Jev-shaped.

## Tier 1: how the judgment step works now vs with Jev

Cost assumptions (order-of-magnitude only): frontier LLM ≈ **$3–15/M input,
$15–75/M output** (mid-tier ≈ 3–5× cheaper); Jev = **$0.042/M input, output free**.
"Inference" below means the main LLM pass.

### 1. cognitive-mirror (Harvest)

- **Now:** One inference pass reads conversations, *finds* decision moments, *quotes*
  them, **and** fills `decision_type` / domain / confidence / trivial-filter —
  extraction and classification fused in the same expensive call; confidence is prose.
- **With Jev:** Mining agent still *finds and quotes* moments (inference keeps
  comprehension); Jev only fills the closed-set fields in one batched request. Code
  applies the trivial-filter threshold (high P → auto-store, mid → review).
- **Cost:** ~10 chats × 10 moments × ~200 tokens ≈ 20k tokens. Frontier
  classify+format ≈ **$0.07–0.20**; Jev ≈ **$0.001** (~50–150× less), plus free
  structured output.

### 2. paradigm-collision-engine

- **Now:** Parallel subagents each score 100+ paradigms 0–10 and run the 0–2 ×3
  tournament *inside* inference — prose rationales, ~30–60 min wall time, most
  tokens spent on paradigms that get dropped.
- **With Jev:** Relevance + tournament Scores batched in ~one request (~100ms); code
  applies ≥6 and drop-below-3 gates; subagents only *generate insights* for
  survivors.
- **Cost:** ~50–100k tokens of paradigm text per run. LLM scoring ≈
  **$0.50–2.00** + long latency; Jev ≈ **$0.002–0.004**. Biggest $ and time delta
  in the tier (generation time remains, scoring time → ~zero).

### 3. audit-fix

- **Now:** Same inference that *wrote* the findings applies the earn filter —
  self-grading, binary, no probability, no receipt.
- **With Jev:** LLM still generates the six-lens findings; Jev answers one Noul per
  finding ("does acting change the outcome?") + discard-reason Choice. Code routes:
  high P → act, ~0.5 → escalate to LLM/user, low → discard.
- **Cost:** Small either way (N findings × ~300 tokens ≈ few k). Jev ≈
  **< $0.0005**; the win is *independence + calibrated borderline surfacing*, not
  dollars. Inference only runs on escalated findings.

### 4. audit-mcp

- **Now:** Bash collects signals (counts stay in code); main inference reads the
  whole report + repo context, applies FP gotchas in prose, writes a
  PASS/CAVEATS/FAIL paragraph.
- **With Jev:** Code parses findings into rows; Jev batch-answers per-finding FP Noul
  + 3-way verdict Choice against the written criteria table. Hard rules (hardcoded
  secret → FAIL) stay code; low confidence → human.
- **Cost:** Report ~5–20k tokens. LLM judgment pass ≈ **$0.02–0.30**; Jev ≈
  **$0.0003–0.001**. Quality win: gotchas applied uniformly, install gate gets a
  probability.

### 5. gmail-manager

- **Now:** Inference reads full bodies, classifies each email (promo? urgent?
  action?), usually emits JSON per batch — classification fused with reading; cost
  scales with body tokens × model rate.
- **With Jev:** Deterministic rules (CATEGORY_PROMOTIONS etc.) archive first at
  **0 tokens**; Jev gets headers/snippets + 6–7 typed questions for the fuzzy
  remainder, all batched. Inference only to draft replies.
- **Cost:** 25 emails × ~300 tokens ≈ 7.5k. LLM classify ≈ **$0.02–0.10**; Jev ≈
  **$0.0003** (~50–300×), ~100ms, confidence-gated auto-archive.

### 6. brand-writing-team

- **Now:** Each role's *own* inference assigns 1–10 scores to its own draft
  (contaminated judge); orchestrator trusts the numbers. Second full re-read if
  revising.
- **With Jev:** Writer inference still drafts/revises; Jev re-reads draft+criteria
  once as Score × criteria + fabrication/source Nouls. Code enforces ≥9 / <7 /
  min-overall rules; only failing roles burn revision inference.
- **Cost:** Judging is a full draft read (2–5k tokens). Self-grade = folded into
  writing pass (no clear $ delta); *independent* LLM re-grade ≈ **$0.02–0.15/draft**
  vs Jev ≈ **$0.0002**. Win = ungamed gates, not primarily $.

### 7. teaching-block-synthesized

- **Now:** Finalization re-infers over the full draft against ~40 checklist items;
  skill even suggests 3 parallel judges + median = 3 expensive full reads,
  oscillating verdicts.
- **With Jev:** Draft is state; ~40 Noul + heading Choices in **one** batch; code
  counts passes and takes median-of-3 trivially; inference only rewrites flagged
  sections.
- **Cost:** Draft ~3–5k tokens. 3-judge LLM ≈ **$0.03–0.25**; Jev ≈ **$0.0002**
  (~150–1000× on the audit step). Checklist consistency replaces flip-flop
  re-grades.

### 8. voice-profile-trainer

- **Now:** Inference re-reads every draft for the 7-item checklist + telltale
  blacklist — presence checks done as full reads.
- **With Jev:** Jev answers 7+ Nouls per draft in one batch; code counts ≥5/7;
  borderline items flagged by probability. Inference only when returning the draft
  for fixes.
- **Cost:** Draft ~2k tokens. LLM check ≈ **$0.01–0.05**; Jev ≈ **$0.0001**
  (~100×). Receipts: *which* check is marginal, not just pass/fail.

### 9. trello-pipeline

- **Now:** One reviewer inference turn per card reads spec + issues, emits
  APPROVED/NEEDS_REVISION + severity + vision score in prose — slow at N cards,
  scores uncalibrated, decision mixed with feedback writing.
- **With Jev:** LLM reviewer still *inspects* and writes findings once; Jev grades
  decision Choice + severity + alignment Score batched across parallel cards; bounce
  rule = deterministic severity map; feedback prose inference only when
  NEEDS_REVISION.
- **Cost:** Per-card review ~3–8k tokens. Grading portion LLM ≈ **$0.01–0.10/card**
  vs Jev ≈ **< $0.0001/card batched**; latency N cards → ~one batch. Same shared
  severity bank as session / SDIF.

### 10. skill-evals

- **Now:** Triggering cases correctly stay as fresh harness sessions; quality cases:
  LLM judge reads output + prose criteria → PASS/FAIL, often per-case or one big
  judge prompt — one inference pass per eval run, no per-criterion signal.
- **With Jev:** Triggering unchanged; each `expectations[]` assertion → Noul, whole
  `evals.json` in one request; code ANDs to case PASS (scores stay banned per skill
  policy).
- **Cost:** Say criteria+outputs ≈ 5–15k tokens. LLM judge ≈ **$0.02–0.15**; Jev ≈
  **$0.0003**. Win = per-assertion probabilities show *which* criterion is marginal;
  judge can't drift.

### 11. enrich-prompt

- **Now:** Same inference that answers also decides skip-vs-enrich — the gate costs
  nothing extra, but is inconsistent and invisible (no receipt), and over-enrichment
  wastes a big answer pass.
- **With Jev:** Pre-gate Noul (~200–300 token state ≈ **$0.00001**) before any
  inference; skip → direct answer; enrich → full layers as today. At single-chat
  volume the gate itself is free either way; the savings come from *not* running
  enrichment layers when the gate would say skip, and from consistency at API/batch
  volume (N gates ≈ free vs N frontier judgments).
- **Cost:** Per call delta ≈ noise; structural win = enrichment inference only when
  it changes the substance (the skill's own eval case).

### Responsibility split (the pattern)

| | Without Jev | With Jev |
|---|---|---|
| **Inference owns** | Find + quote + classify + decide, fused | Find, quote, explain, revise (comprehension + generation) |
| **Jev owns** | — | Closed-set labels, presence checks, rubric scores, with P() |
| **Code owns** | Ad-hoc thresholds in prose | Counts, dates, gates, routing on probabilities |
| **Output cost** | Structured JSON often expensive output tokens | Jev output free |
| **Typical $ on the judgment slice** | cents per run (frontier) | fractions of a cent (50–1000× less) |

Dollar savings are largest where judgment is **repeated and batched**
(paradigm-collision, gmail-manager, teaching-block, trello, skill-evals). Where
judgment runs once (audit-fix, enrich-prompt gate), the win is **independence +
calibration**, not cost.

### Latency & cost comparison (orders of magnitude)

Latency = wall time for the *judgment slice* only (extraction/generation time is
unchanged and excluded). "Without" assumes the judgment rides along with a main-LLM
pass; "with" = one batched Jev request (~100ms) + code. Dollar figures are for the
judgment slice alone, order-of-magnitude.

| Skill | Judgment slice (tokens) | Cost without Jev | Cost with Jev | ~Savings | Latency without | Latency with |
|-------|------------------------:|-----------------:|--------------:|---------:|-----------------:|-------------:|
| cognitive-mirror Harvest | ~20k | $0.07–0.20 | ~$0.001 | 50–150× | seconds–minutes (in fused pass) | ~100ms batch |
| paradigm-collision-engine | ~50–100k | $0.50–2.00 | ~$0.002–0.004 | ~100–500× | 30–60 min (subagent batch) | ~100ms + generation for survivors only |
| audit-fix | few k | $0.01–0.05 | < $0.0005 | ~20–100× | folded into findings pass | ~100ms |
| audit-mcp | ~5–20k | $0.02–0.30 | ~$0.0003–0.001 | ~30–300× | seconds | ~100ms |
| gmail-manager (25 mails) | ~7.5k | $0.02–0.10 | ~$0.0003 | ~50–300× | seconds–tens of seconds | ~100ms |
| brand-writing-team (per draft) | ~2–5k (judge re-read) | $0.02–0.15 (independent re-grade) | ~$0.0002 | ~100–700× | seconds per role gate | ~100ms |
| teaching-block (40-item audit) | ~3–5k × 3 judges | $0.03–0.25 | ~$0.0002 | ~150–1000× | seconds × 3 judges | ~100ms (one batch, median in code) |
| voice-profile-trainer | ~2k | $0.01–0.05 | ~$0.0001 | ~100× | seconds | ~100ms |
| trello-pipeline (per card grade) | ~3–8k | $0.01–0.10 | < $0.0001 (batched across cards) | ~100–1000× | seconds per card, serialized | ~100ms for the batch |
| skill-evals (quality cases) | ~5–15k | $0.02–0.15 | ~$0.0003 | ~50–500× | seconds per judge pass | ~100ms |
| enrich-prompt (gate) | ~200–300 | ~$0.001 (folded into answer) | ~$0.00001 | ~100× on the gate; main win = skipping enrichment passes | folded, invisible | ~100ms pre-gate |

Reading the table: **cost ratios are 10²–10³× on the judgment slice**; latency
collapses from *seconds to minutes* (or an entire subagent batch, in
paradigm-collision's case) to **~100ms** wherever the judgment becomes a dedicated
batched Jev request. Extraction and generation latencies are untouched in both
columns.

## Deferred next steps

Not started — recorded so the survey can be picked up later:

1. **Tier-1 prototypes** — add a Jev layer to the highest-confidence instruction-file
   skills first (candidates: audit-fix earn filter, cognitive-mirror harvest,
   teaching-block checklist — no scripts to break), following the arcade's question
   design rules.
2. **Shared infrastructure** — one zero-dependency `callJev` helper extracted from
   `jev-arcade/server.mjs`, plus shared severity / gate question banks multiple
   skills can import.
3. **Router experiment** — Jev Choice layer behind a flag in `load.md`, measured
   against existing `skill-evals` triggering cases.
4. **Arcade mapping gaps** — gmail-triage and meeting-nuggets deeper hooks above.
