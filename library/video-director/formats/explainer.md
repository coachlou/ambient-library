# Format: explainer

Makes one idea or mechanism clear: how something works, or why.

- **Sources:** the spec, design doc, docs page or article the idea comes from; the code or app
  only to confirm a detail. Every claim in the script traces to one of them.
- **Brief defaults:** audience knows the domain but not this idea; goal is "I could explain it
  to someone else"; length 1-3 min; tone warm and clear (`[warmly]`, `[confident]`, `[softly]`);
  16:9.
- **Beats:** the question, the one-sentence answer, then 3-5 steps that build it up, each
  adding one piece, then the answer again with the whole picture.
- **Shot structure:** mostly `html` cards: a question card, one diagram card per step (draw it
  in HTML/SVG inside `html`, adding the new piece each step so the picture grows), an optional
  app shot where the idea shows up for real, a summary card. Card-only explainers need no demo,
  scout or `baseUrl`.
- **Cards take no callouts:** an `html` shot is one still. To point at a new piece, make it
  its own shot (same diagram, the new piece in an accent color), or serve the diagrams as a
  static page and capture them as `path` shots with rings.
- **Script:** one idea per shot, plain words, an everyday analogy once if it helps; define every
  term the first time it is said.
