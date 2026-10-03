# team-build

Turn a project brief into `<project>/skills-manifest.yaml`: one skill per
need, each with a reason, plus a rationale record. Everything runs inside
this one invocation.

## Important

- Recall reads `${CLAUDE_PLUGIN_ROOT}/library/team-index.yaml` only. Never
  read skill bodies to shortlist; only the stage 3 subagents read bodies,
  and at most 3 per need. The index is about 40K tokens; load it once.
- Project scope only. Write `<project>/skills-manifest.yaml`. Never write or
  edit `~/.aai/skills-manifest.yaml`, even when asked "for everywhere"; say
  that is `select`'s job.
- Every skill name you output must appear as a key in `team-index.yaml`.
  If a name in `library/catalog.yaml` is missing from the index, say the
  index is stale (regenerate with `scripts/build-team-index.py` in a source
  clone) and continue without that skill.
- If the user names a specific skill ("add editor to this project"), stop:
  that is `manage`, not a team build.

## 0. Brief

Take whatever the user gave: a paragraph, a README, a folder (run `ls` and
read its README or `.aai/purpose.md` if present). If the brief has no stated
purpose or is under about 50 words, ask these three questions inline, in
one message, and wait:

1. What does this project produce?
2. For whom?
3. What kinds of tasks will you ask for most?

Append the answers to the brief verbatim. Do not hand off to any interview.

Read `~/.aai/skills-manifest.yaml` if it exists and note its
`domain_skills` as already in force. If `<project>/skills-manifest.yaml`
exists, show it and say the build will replace it on confirmation.

## 1. Needs

One pass, inference. From the brief, write up to 10 needs. Each need is one
sentence in the shape of a request the user will actually make: "draft
articles from research notes", "keep context across sessions", and each
quotes the brief phrase it came from. No phrase, no need: short briefs
yield one or two needs, and that is correct. Needs the brief implies but
never states ("edit and polish", "sound like me", "publish it") are not
written; the evals showed every one of them became a wrong pick. More than
10 means merge.

## 2. Recall

One pass, inference, with the whole index and all needs in context. For
each need return up to 5 candidates ranked, each with the one line from the
index (a `requests` item or a `summary` phrase) that earned its place:

```yaml
- need: draft articles from research notes
  candidates:
    - name: writer
      because: '"Draft this from my notes" with a brief and raw notes'
    - name: writing-team
      because: full research, draft, edit pipeline to a publish-ready piece
```

Validate: every `name` is an index key. If not, rerun this step once with
the bad names quoted; on a second failure drop them and say so.

## 3. Precision

For each need, spawn one general-purpose subagent with a fresh context
(Agent tool). Give it the need, the full brief, the full numbered list of
needs, and the resolved absolute paths of the top 3 candidates'
`instructions.md` (or `SKILL.md` where that is the only file). Tell it to
read each body in full, not the first screen; a truncated read misses the
later stages that decide between siblings. Run the subagents in parallel.
Its reply must be exactly:

```yaml
need: draft articles from research notes
pick: writer
runner_up: writing-team
reason: brief says research is done by a human; writing-team would redo it
confidence: high | medium | low
covered_by: none   # or a shortlist skill that serves this need as part of another need
```

The reason names the runner-up and says what in the brief decided it.
`covered_by` is a concession, not a claim: the subagent names a skill from
its own shortlist, picked for another need in the list, that would also
handle this need without a second skill, so this need can ride on it. It
never says which other needs its own pick covers; the evals showed every
such outward claim dropped a skill the other need's reader had rejected. Validate `pick` and `runner_up`
against the index keys. `pick` is always a skill from the shortlist, never
`none`: when nothing fits, the reader names the least-bad candidate and marks
it `low`, so validation and step 5 have something to work with.

**Second opinion.** A reply is noise when its confidence is `low`, when its
reason argues for a skill other than its `pick`, or when its `covered_by`
names a skill the same reason says lacks something the need requires. For
a noisy reply, spawn one fresh subagent with the same inputs and use that
second reply instead; the evals showed a single reader contradicting itself
in about one need per ten, and each time it cost a skill the brief needed.
Record both replies for step 5. If the second reply is also noise, keep the
second one but treat it as `low`: it becomes a question for the user in
step 5, the pick stays out of the manifest until answered, and its
`covered_by` is ignored in step 4. A reason saying the candidates are
interchangeable counts as `low` too. Never resolve a `low` silently.

## 4. Set-cover

No inference. Apply in order and record every change for step 5:

1. **Merge.** Two needs with the same pick become one manifest entry that
   lists both needs.
2. **Subsume.** If need n's reply says `covered_by: A` and A is the pick
   for some other need, drop need n's pick B and note "covered by A". Only
   need n's own reader may concede it; a pick never subsumes needs it was
   not evaluated against. Do not use the index's `not_for` for this:
   sibling skills name each other there in both directions, so it cannot
   say which one does more.
3. **User scope.** Drop any pick already in `~/.aai/skills-manifest.yaml`
   and note "already enabled for every project".

## 5. Confirm and write

Show one table: need, pick, runner-up, reason. Below it list drops from
step 4, then the gaps: needs whose pick was `low` confidence, shown as
questions, not as manifest rows. Ask: "Write this manifest?"

On yes, write both files:

`<project>/skills-manifest.yaml`:

```yaml
# Built by team-build on <YYYY-MM-DD>. Rationale: .aai/memory/team-build-<YYYY-MM-DD>.md
domain_skills:
  - writer           # need: draft articles from research notes
  - checkpoint       # need: keep context across sessions
```

`<project>/.aai/memory/team-build-<YYYY-MM-DD>.md` (create `.aai/memory/`
if absent): the brief as received, the three answers if asked, the needs,
the step 2 shortlists, every step 3 reply, the step 4 drops with reasons,
and the questions asked with the user's answers. This file is the audit
trail and the eval corpus seed; keep it plain markdown, no em-dashes.

Close with: "Your team is set. I'll use these skills for this project." If
the user wants the skills vendored into `.ailib/`, hand off to `lifecycle`;
team-build does not vendor.
