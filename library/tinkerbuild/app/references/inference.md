# Inference: subscriptions first, API last

Applies to tinkerbuild itself (`inference` block in `.tinker/config.json`) and to every app it
builds that calls a model (`inference.json` at the app root, copied from
`templates/inference.json`). Same shape, so settings travel with the app.

## The rule

1. Try `chain` in order. Each name is an adapter: a CLI logged in with a subscription
   (`claude -p`, `codex exec`). `chain[0]` is the harness the user is working in.
2. A run whose output matches the adapter's `skip_patterns` (usage limit, not logged in) means
   "move to the next adapter", not "the task failed". Remember the fallback for `cooldown_s`,
   then try `chain[0]` again. Notify the user on every switch.
3. Only when every subscription is unavailable, and `api.approved` is true, and the env var
   named by `api.key_env` is set: run `chain[0]` again with that variable in the environment.
   Otherwise strip it, so a subscription CLI never silently bills the API.
4. Never write the key itself to any file; `key_env` holds the variable's *name*.
5. `roles.<role>.model` / `.effort` are optional overrides; `""` means the harness default.
   The adapter's `model_flag` / `effort_flag` say how each CLI spells them; an adapter without
   the flag ignores the setting. tinkerbuild roles: `builder`, `checker`. Apps: `default` plus
   whatever the app defines.

## Building an agent-driven app

- Copy `templates/inference.json` to the app root at the skeleton; it is a seam
  (`inference-settings` in `.tinker/architecture.md`) with a check that the file parses and
  `chain` is non-empty.
- One module owns it (e.g. `infer`): `run(role, prompt) -> (rc, text)` that implements the rule
  above. Thirty lines in any language; `scripts/tb.py` `agent()` is the reference implementation.
- The in-app settings screen, if there is one, edits `inference.json` and nothing else.
- Spawn the CLI with the prompt on stdin, in the app's folder, with `TB_ROLE=<role>` set.

## Changing the order

Edit `chain` by hand or from the app's settings. tinkerbuild: `.tinker/config.json`;
`tb.py status` shows when a fallback is active.
