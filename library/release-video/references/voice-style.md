# Voice style: calm, confident launch read

The style comes from voice + model + tags + script wording, with default voice settings.
No custom ElevenLabs voice is needed.

## ElevenLabs settings
- Voice: the user's own cloned voice if they have one (ask, or check their memory/profile),
  else pick a clear general-purpose voice with `creative_list_voices`. Put the id in the spec
  (`voice.id`) so later videos reuse it.
- Model: **eleven_v3**. It is needed for the [tags]; multilingual_v2 sounded robotic.
- Voice settings: defaults (no stability/similarity/style overrides).
- One generation per line (`generations_count: 1`); regenerate only the lines you dislike.

## Tags
Open each line with ONE tag; at most one more mid-line for a beat.
- Use: `[warmly]` `[upbeat]` `[confident]` `[playfully]` `[proudly]` `[softly]` `[laughs softly]`
- Avoid: `[excited]` and `!`-heavy lines. That read came out about 10% too enthusiastic.
- A closing line works well as `[proudly] That's all there is to it.`

## Script rules
- One short line per shot, about 5 to 13 seconds spoken. Short sentences, plain words.
- Conversational fillers make it sound human: "right?", "No problem.", "right there".
- Spell numbers the way they are said ("zero point eleven", "four hundred ninety-two").
- Periods, not exclamation marks (at most one "!" in the whole script).
- Name on-screen things with the exact words the UI shows, so a callout can ring them.

## Worked example (SoloFactory 0.11.0, 14 shots, approved)
1. [warmly] Okay, wonderful. SoloFactory zero point eleven is here. The project hub. And this one's kind of a big deal.
2. [upbeat] Every project in one place, right? What needs you, what's running, what's queued, what's done. Across all of them.
3. [confident] The side rail keeps score. Build slots up top, anything paused flagged under Needs you. Fold a group away, or click any item to jump in.
4. [upbeat] The project selector. Every project a click away, with its state right beside it.
5. [upbeat] Watch it work, step by step. Something goes sideways? No problem. It parks the run, keeps what passed, and you resume from right there.
6. [confident] Ask it straight. Is it moving? Is it healthy? How far along? Restart from a step, not from scratch. Reorder the queue. [laughs softly] All that kind of stuff.
7. [upbeat] The Guide is always on. Attach a doc or a screenshot, talk it through, and it writes a spec you can read and edit. Nothing ships till you hit Send.
8. [upbeat] Your live app, right there! Open it, stop it, relaunch it, and see its traffic.
9. [confident] Claude or Codex, per project. Make your own profiles too. [playfully] And yes, the Settings picker stays put now.
10. [warmly] Bottom left, the Menu. New project, Settings, the Manual, Feedback, and Check for updates.
11. [warmly] Spot a problem, or got an idea? The feedback form is right there in the menu.
12. [upbeat] Updating? One button. Claude Code or Codex does the work, SoloFactory restarts, and your projects and runs stay right where you left them.
13. [upbeat] In the last test set before release: three apps built, twenty out of twenty features shipped, under twenty dollars, in about an hour. Four hundred ninety-two tests green. [proudly] That's all there is to it.
14. [warmly] Let's serve people, do good, have fun, and make money, abundantly. [softly] Namaste.
