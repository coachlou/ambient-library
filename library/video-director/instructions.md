# Video director

Makes a narrated video end to end, on its own. You are the director: you write the requirements
brief, pick the format, and run the crew below yourself, step by step. One spec file
(`shots.json`) drives capture, voice and the mix. The user gives a topic, a version or a product
at most; everything else is decided here. Ask only for what cannot be found (no voice id
anywhere, no way to run the app, no source for a claim).

## Formats
A format is a carve-out: the protocol, sources and defaults for a common kind of video. Pick one
from the user's words; when none fits, use the general process below with your own judgment for
each brief field. A format only overrides what it names; everything else is the general process.

| Format | Use for | File |
|---|---|---|
| release | what's new in a version, launch or update video | `formats/release.md` |
| tutorial | how-to, setup walkthrough, "show me how to X" | `formats/tutorial.md` |
| product-demo | tour of the app, sales or onboarding demo | `formats/product-demo.md` |
| promo | teaser, ad, 15-45 s social cut | `formats/promo.md` |
| explainer | how something works, a concept, often without a live app | `formats/explainer.md` |

Read the chosen format file now, before writing the brief.

**No format fits? Build one.** For a kind of video with no format yet (an onboarding welcome, a
case study, a changelog digest), write its format before the brief, in the same shape as the
files above: use for, sources, brief defaults (audience, length, tone, aspect), beats, shot
structure, script notes. Base it on the closest existing format and change only what differs.
Then use it for this video like any other format. When the video is done, revise the draft
with what worked, and offer it for the library:
- Find the ambient-library clone, the same way `.aai/skills/propose.md` does: the current
  project if it has `.aai/instructions.md` and `.claude-plugin/plugin.json`, otherwise ask the
  user for the clone's path. Never write into `${CLAUDE_PLUGIN_ROOT}`.
- Save the draft as `in-progress/video-director-formats/<name>.md` and add a row for it to
  `in-progress/CANDIDATES.md` (candidate, where it is, why: the video it was made for).
- Do not commit. Tell the user it is there for review. Promoting it means moving the file to
  `library/video-director/formats/` and adding a row to the table above.
- No clone to be found: keep the draft in the work folder and say where it is.

## Requirements
Run `python3 ${CLAUDE_PLUGIN_ROOT}/library/video-director/scripts/preflight.py <work folder>` first;
it checks the first five below and prints the install command for anything missing. Install what
it lists (ask before installing system packages), rerun until it says `ready`.
- ffmpeg and ffprobe 4.3+ with libx264 and aac (a brew or apt build has them).
- Python 3.8+. The scripts use only the standard library.
- Node 18+, with `npm i playwright-core` run in the work folder (the scripts load it from there).
- Google Chrome or Chromium (`npx playwright install chromium` if neither is installed; off a
  Mac, set `chrome` in the spec or pass `--chrome` to explore.mjs).
- curl.
- A voice, one of (check in this order, and say which one you are using):
  1. The ElevenLabs connector (`creative_generate_speech` and the other `creative_*` tools). Best:
     it does the [tags] and gives word timings. Voice id from the spec, the user's memory or
     profile, or `creative_list_voices` (pick a clone named after the user, else ask them to
     choose one from the list; never reuse a voice id from another person's example).
  2. The user's own recordings: one mp3 per shot in `vo_raw/`, named after the shot, reading its
     line with the [tags] removed. Skip step 7.
  3. No voice at all: say what is missing and stop before step 7. Do not ship a robotic
     system voice unless the user asks for one.
- For a video that shows an app: a way to run that app on its own port with throwaway data.
  Nothing else (no account, no repo of the author's) is assumed.

## The crew (roles you play, in order)
- **Director:** writes `brief.md` and holds every later step to it.
- **Producer/researcher:** gathers facts from the format's sources; every claim traces to one.
- **Scriptwriter:** shot list and narration (`shots.json`, voice-style.md).
- **Cinematographer:** stands up the demo, scouts, captures stills with callout rings.
- **Voice:** records each line in ElevenLabs and times the words.
- **Composer:** the music bed (music.py, or a file the user supplies).
- **Editor:** trims, cues, builds and mixes the mp4.
- **QA:** checks every frame and the final cut against the brief.
- **Publisher:** hands over locally; uploading or sending is the user's call.

## Gotchas
- **Never capture real data.** Run the app against a demo fixture on its own port (copy or seed a
  throwaway data folder; point the app's HOME/ROOT/DB at it). Never point capture at the user's
  live instance, and never open their media or client files.
- **Model must be eleven_v3.** The [tags] only work there; multilingual_v2 sounds robotic.
- **Use the app's own words.** Copy target text and captions from explore's JSON, not from
  memory or docs; a ring target that does not match the screen exactly fails capture.
- **Cues are voice-relative seconds.** `cue` is when the named words start in that shot's trimmed
  voice line (from `vo.py cues`), not video time. build.py adds the 0.4 s lead itself.
- **Trim before cueing.** Run `vo.py trim` first; cue times from untrimmed takes are off by the
  lead silence.
- **Draw the ring as an overlay.** A box-shadow on the target element gets clipped by overflow;
  capture.mjs already draws a separate fixed div. If a ring cuts off text (a group whose last item
  sits near the edge), use `union` with the first and last items plus `widen`, or raise `pad`.
  A `text` target boxes only that text, not its row: to end a group on a two-line row, make the
  last union member the row itself (`selector`, or `climb` with the row's size).
- **Check every frame before building.** A ring around the wrong element ships unnoticed unless
  you look. Make a contact sheet and view it (step 6).
- **climb picks the first ancestor at least minW x minH.** Too large and it rings the whole
  panel; keep the minimums just above the group's real size.
- **Mock state, don't stage it.** For states the demo can't reach (update available, a failed
  run), add a `mocks` entry rather than editing app data.
- **No app? Use cards.** A shot with `html` renders a card (title, diagram, stat, quote) instead
  of a page, as one still with no callouts; a video made only of cards needs no demo, scout
  or `baseUrl`.
- **Publishing is the user's call.** Deliver the mp4 locally; uploading or sending it needs their OK.
- Run explore.mjs and capture.mjs from the work folder: they load playwright-core from the
  current folder, not from the skill's.

## Files
- `${CLAUDE_PLUGIN_ROOT}/library/video-director/formats/*.md` format protocols (table above)
- `${CLAUDE_PLUGIN_ROOT}/library/video-director/scripts/preflight.py` `[WORK_DIR]`: checks the tools in Requirements, prints fixes, exit 1 if any is missing
- `${CLAUDE_PLUGIN_ROOT}/library/video-director/scripts/explore.mjs` scout: a screenshot plus a JSON map (text, tag, role, box, links) per page or clicked-open state (`--states`, `--help`)
- `${CLAUDE_PLUGIN_ROOT}/library/video-director/scripts/capture.mjs` stills per shot and callout (`--help`, `--dry-run`, `--only`)
- `${CLAUDE_PLUGIN_ROOT}/library/video-director/scripts/vo.py` `trim RAW OUT`, `cues FILE...`, `autocue SPEC` (sets each callout's `cue` from its `at` words, exact with a words file)
- `${CLAUDE_PLUGIN_ROOT}/library/video-director/scripts/music.py` `SECONDS [OUT.wav]`: original upbeat bed (build.py calls it if needed)
- `${CLAUDE_PLUGIN_ROOT}/library/video-director/scripts/build.py` clips, crossfades, voice placement, music duck, loudness (`--dry-run`)
- `${CLAUDE_PLUGIN_ROOT}/library/video-director/references/shots.example.json` spec format, annotated by example
- `${CLAUDE_PLUGIN_ROOT}/library/video-director/references/voice-style.md` voice settings, tag rules, script rules, a worked 14-line script

## Workflow
Work in a folder outside any repo the video is about (e.g. `notes/video-<topic>/`), with
`npm i playwright-core` run in it and preflight.py showing `ready`. Do every step yourself; do not stop for approval unless the
user asked to review the brief or script first.

1. **Brief (director).** Write `brief.md` with: audience (who watches, what they already know),
   goal (what they should do or believe after), length, tone (voice-style tags to lean on),
   sources (where facts come from), deliverable (mp4 size and aspect, captions or not, where it
   will be shown), and the 5-12 beats the video must hit, each with the screen or card that shows
   it. Take each field from the user's words, then the format's defaults, then your judgment.
2. **Research (producer).** Read the format's sources and fill each beat with facts and why they
   matter. Lead with the strongest beat. Brag with facts, never invent one; a beat with no source
   is cut or marked for the user.
3. **Stand up a demo (cinematographer).** If any beat shows an app: start it on a throwaway data
   folder and its own port, seeded with a few realistic fake records so every beat has something
   to show (see Gotchas). Set `baseUrl`. Skip for card-only videos.
4. **Scout.** `node ${CLAUDE_PLUGIN_ROOT}/library/video-director/scripts/explore.mjs <baseUrl> [paths...] --out explore`
   (no paths: it follows the app's own links). View the screenshots; read the JSON for exact text
   and positions. Screens that open only on a click (a menu, a selector, a folded group): list
   them in a `--states states.json` file (`[{"name","path","steps":[{"click":"Menu"}]}]`) and
   rerun, then copy the same steps into the shot's `setup`. Off a Mac, pass `--chrome <path>`.
5. **Script and shot list (scriptwriter).** Write `shots.json` from shots.example.json in the
   format's shot structure, one shot per beat. Each shot's `line` follows voice-style.md (one
   tag, short sentences) and the brief's length. For every thing the line names on screen, add a
   callout with a `ring` target taken from the explore JSON and `at`: the words in the line that
   name it. First callout is `{ "cue": 0 }`; to close on the whole screen, end with
   `{ "same": 0, "at": "<closing words>" }` (every callout after the first needs `at`, or
   autocue cannot place it).
6. **Capture, then look (cinematographer, QA).** `node ${CLAUDE_PLUGIN_ROOT}/library/video-director/scripts/capture.mjs shots.json`;
   fix FAIL targets and rerun with `--only <shot>`. Contact sheet:
   `ffmpeg -y -v error -pattern_type glob -i 'frames/*.png' -vf scale=480:-1,tile=4x6 sheet.png`
   and view it (on Windows, where ffmpeg has no glob, view the frames directly). Every ring on the right thing, nothing clipped, captions readable, no real data.
   Fix and recapture until it is clean. Capturing before voicing is deliberate: a shot that
   cannot be shown gets rewritten before it costs a voice take.
7. **Voice.** Without the ElevenLabs connector, use the user's recordings (see Requirements)
   and go to step 8. Voice id: `voice.id` in the spec, else the user's clone from memory or
   `creative_list_voices` (their own name or clone first, else let them pick); save the choice
   to `voice.id`. `creative_create_flow` once, then per
   shot `creative_generate_speech` with flow_id, voice_id, model_id `eleven_v3`,
   generations_count 1 and the line as prompt. `creative_get_flow_run_status` lists each
   generation's content URL; `curl -L -o vo_raw/<shot>.mp3` them, named exactly after the shot.
   Then, for word-accurate rings, `creative_transcribe_audio` (eleven_scribe_v1, same flow_id,
   connect_from the speech node) per shot and save its `words` list as `vo/<shot>.words.json`.
8. **Trim and cue (editor).** `python3 ${CLAUDE_PLUGIN_ROOT}/library/video-director/scripts/vo.py trim vo_raw vo`, then
   `python3 ${CLAUDE_PLUGIN_ROOT}/library/video-director/scripts/vo.py autocue shots.json`. It writes each callout's `cue`
   from the words file when there is one (exact), else an estimate (mean 0.36 s off, worst about
   2 s; it prints which). Without words files, listen to estimated shots in the build and fix any
   ring that lands a beat off. If cues do not rise, compare with `vo.py cues vo/<shot>.mp3` and
   set those `cue` values by hand.
9. **Music and build (composer, editor).** Set `music` to a user-supplied file, or leave it out
   for music.py's bed; `musicGain` (default 0.7) sets how loud it sits. Then
   `python3 ${CLAUDE_PLUGIN_ROOT}/library/video-director/scripts/build.py shots.json --dry-run` (timings,
   missing inputs), then without `--dry-run`. It prints the loudness; target about -21 dB mean,
   -0.5 dB peak. Check the dry-run total against the brief's length and cut or merge shots if
   it runs long.
10. **Verify and deliver (QA, publisher).** Pull a frame just after a few cues
    (`ffmpeg -ss T -i video.mp4 -frames:v 1 t.png`) and view them. Re-read the brief: every beat
    shown, length within it, tone right. Hand over the mp4 path with the script, and say what
    you would change next if anything looked weak.

Revisions are cheap: a voice change redoes steps 7, 8 and 9 for that shot; a ring fix redoes 6
(`--only`) and 9. Tone notes ("10% less enthusiastic") mean changing tags, not voice settings.
