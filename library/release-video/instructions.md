# Release video

Makes a narrated product or release video end to end, on its own: works out what is new,
writes the script and shot list, records each line in the user's voice (ElevenLabs), scouts and
captures the app with callout rings on what the voice names, adds a bright music bed ducked
under the voice, and mixes to mp4 with ffmpeg. One spec file (`shots.json`) drives every step.
The user gives a version or a product at most; everything else is decided here. Ask only for
what cannot be found (no voice id anywhere, no way to run the app).

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
  you look. Make a contact sheet and view it (step 5).
- **climb picks the first ancestor at least minW x minH.** Too large and it rings the whole
  panel; keep the minimums just above the group's real size.
- **Mock state, don't stage it.** For states the demo can't reach (update available, a failed
  run), add a `mocks` entry rather than editing app data.
- **Publishing is the user's call.** Deliver the mp4 locally; uploading or sending it needs their OK.
- playwright-core must be installed in the work folder (`npm i playwright-core`); capture.mjs
  uses system Chrome on macOS, or set `chrome` in the spec.

## Files
- `${CLAUDE_PLUGIN_ROOT}/library/release-video/scripts/explore.mjs` scout: a screenshot plus a JSON map (text, tag, role, box, links) per page or clicked-open state (`--states`, `--help`)
- `${CLAUDE_PLUGIN_ROOT}/library/release-video/scripts/capture.mjs` stills per shot and callout (`--help`, `--dry-run`, `--only`)
- `${CLAUDE_PLUGIN_ROOT}/library/release-video/scripts/vo.py` `trim RAW OUT`, `cues FILE...`, `autocue SPEC` (sets each callout's `cue` from its `at` words, exact with a words file)
- `${CLAUDE_PLUGIN_ROOT}/library/release-video/scripts/music.py` `SECONDS [OUT.wav]`: original upbeat bed (build.py calls it if needed)
- `${CLAUDE_PLUGIN_ROOT}/library/release-video/scripts/build.py` clips, crossfades, voice placement, music duck, loudness (`--dry-run`)
- `${CLAUDE_PLUGIN_ROOT}/library/release-video/references/shots.example.json` spec format, annotated by example
- `${CLAUDE_PLUGIN_ROOT}/library/release-video/references/voice-style.md` voice settings, tag rules, script rules, a worked 14-line script

## Workflow
Work in a folder outside any repo the video is about (e.g. `notes/release-video-<version>/`),
with `npm i playwright-core` run in it. Do every step yourself; do not stop for approval unless
the user asked to review the script first.

1. **Find what's new.** Read the CHANGELOG / release notes entry for the version, `git log
   <previous tag>..<tag> --oneline`, and the docs or manual pages those changes touch. Write
   `brief.md`: the 5-10 changes a user would notice, each with why it matters and which screen
   shows it. Lead with the biggest; fold internal-only work into a stats line (tests, cost,
   time) if the release notes give numbers. Brag with facts, never invent one.
2. **Stand up a demo.** Start the app on a throwaway data folder and its own port, seeded with
   a few realistic fake projects or records so every screen in the brief has something to show
   (see Gotchas). Set `baseUrl`.
3. **Scout.** `node ${CLAUDE_PLUGIN_ROOT}/library/release-video/scripts/explore.mjs <baseUrl> [paths...] --out explore`
   (no paths: it follows the app's own links). View the screenshots; read the JSON for exact text
   and positions. Screens that open only on a click (a menu, a selector, a folded group): list
   them in a `--states states.json` file (`[{"name","path","steps":[{"click":"Menu"}]}]`) and
   rerun, then copy the same steps into the shot's `setup`. Off a Mac, pass `--chrome <path>`.
4. **Script and shot list.** Write `shots.json` from shots.example.json: a title card, one shot
   per brief item (`path`, `setup`, a `caption`), a stats card if earned, a closing card. Each
   shot's `line` follows voice-style.md (one tag, short sentences, 60-90 s total for 8-12 shots).
   For every thing the line names on screen, add a callout with a `ring` target taken from the
   explore JSON and `at`: the words in the line that name it. First callout is `{ "cue": 0 }`;
   to close on the whole screen, end with `{ "same": 0, "at": "<closing words>" }` (every callout
   after the first needs `at`, or autocue cannot place it).
5. **Capture, then look.** `node ${CLAUDE_PLUGIN_ROOT}/library/release-video/scripts/capture.mjs shots.json`; fix FAIL targets
   and rerun with `--only <shot>`. Contact sheet:
   `ffmpeg -y -v error -pattern_type glob -i 'frames/*.png' -vf scale=480:-1,tile=4x6 sheet.png`
   and view it. Every ring on the right thing, nothing clipped, captions readable, no real data.
   Fix and recapture until it is clean. Capturing before voicing is deliberate: a shot that
   cannot be shown gets rewritten before it costs a voice take.
6. **Voice.** Voice id: `voice.id` in the spec, else the user's clone from memory or
   `creative_list_voices` (their own name or clone first). `creative_create_flow` once, then per
   shot `creative_generate_speech` with flow_id, voice_id, model_id `eleven_v3`,
   generations_count 1 and the line as prompt. `creative_get_flow_run_status` lists each
   generation's content URL; `curl -L -o vo_raw/<shot>.mp3` them, named exactly after the shot.
   Then, for word-accurate rings, `creative_transcribe_audio` (eleven_scribe_v1, same flow_id,
   connect_from the speech node) per shot and save its `words` list as `vo/<shot>.words.json`.
7. **Trim and cue.** `python3 ${CLAUDE_PLUGIN_ROOT}/library/release-video/scripts/vo.py trim vo_raw vo`, then
   `python3 ${CLAUDE_PLUGIN_ROOT}/library/release-video/scripts/vo.py autocue shots.json`. It writes each callout's `cue`
   from the words file when there is one (exact), else an estimate (mean 0.36 s off, worst about
   2 s; it prints which). Without words files, listen to estimated shots in the build and fix any
   ring that lands a beat off. If cues do not rise, compare with `vo.py cues vo/<shot>.mp3` and
   set those `cue` values by hand.
8. **Build.** `python3 ${CLAUDE_PLUGIN_ROOT}/library/release-video/scripts/build.py shots.json --dry-run` (timings, missing
   inputs), then without `--dry-run`. It prints the loudness; target about -21 dB mean,
   -0.5 dB peak.
9. **Verify and deliver.** Pull a frame just after a few cues
   (`ffmpeg -ss T -i release-video.mp4 -frames:v 1 t.png`) and view them. Hand over the mp4 path
   with the script, and say what you would change next if anything looked weak.

Revisions are cheap: a voice change redoes steps 6, 7 and 8 for that shot; a ring fix redoes 5
(`--only`) and 8. Tone notes ("10% less enthusiastic") mean changing tags, not voice settings.
