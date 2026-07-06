# <folder-name> — Behavior

<!-- The folder's behavior: what it does when an agent acts inside it.
     Keep it a contract: inputs, process, outputs. Delete these comments. -->

## When this applies

<!-- One paragraph: the requests or tasks this folder handles. This is the
     routing trigger — write it as user intent, not implementation. -->

## Inputs

<!-- Explicit, auditable context scoping. The agent loads ONLY what's listed. -->

| File | Kind | Load when |
|------|------|-----------|
| .aai/references/<rules>.md | reference — internalize as constraints | always |
| .ailib/<capability>/ | vendored — resolve .aai/skills/<capability> first (shadowing) | when that capability applies |
| <working-file> | working — process as input | per run |

## Process

<!-- The steps. Deterministic steps go to scripts; inference only where
     judgment, synthesis, or generation is genuinely required. -->

## Outputs

<!-- What lands where. Every output is a plain file a human can read and edit. -->

- <artifact> → <destination>/

## Rules

<!-- Gotchas first: environment facts, mistakes an agent makes without being
     told. Then ground rules. Append here as real failures surface. -->
