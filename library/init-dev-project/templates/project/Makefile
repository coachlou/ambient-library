# The pipeline. Same verbs in every repo; bodies change per project.
# `make` alone prints the numbered pipeline map.
# rc / uat / release / deploy gates live in release-lane (vendored at .ailib/release-lane/);
# paths and commands override in .aai/skills/release-lane/project.toml.
.DEFAULT_GOAL := help
BUMP ?= patch
LANE := python3 .ailib/release-lane/release_lane.py

help:
	@echo "THE PIPELINE      folder    verb"
	@echo "1 SPEC            spec/     make spec      SPEC.md written before code: no TODO: lines left"
	@echo "2 BUILD           {{source}}make run       start it so you can touch it"
	@echo "3 PROVE           tests/    make check     candidate from deploy/SHIPLIST, then lint + unit + smoke"
	@echo "                            make accept    full system test on the candidate (optional, any time)"
	@echo "                            make rc        BUMP=patch|minor|major  bump once, accept, tag vX-rc.N"
	@echo "                            make uat       user testing stable? (no open blockers)"
	@echo "                            make release   promote: uat ok + HEAD == last rc, then tag vX"
	@echo "4 SHIP            deploy/   make deploy    CHANNEL=staging (rc tags) | production (release tags)"
	@echo ""
	@echo "CHANGES           CHANGELOG.md '## Unreleased': one user-facing line per behavior change"
	@echo "BESIDE IT         docs/ for users (ships)   tools/ for builders   .aai/ for the agent"
	@echo "STATE             data/ durable, backed up   build/ runtime/ disposable"

run:
	@echo "run: not defined yet — edit the run recipe in Makefile" >&2; exit 1

# The spec gate: SPEC.md exists and its TODO: placeholders are filled in.
spec:
	@test -f spec/SPEC.md || { echo "spec: spec/SPEC.md is missing" >&2; exit 1; }
	@! grep -n '^TODO:' spec/SPEC.md >&2 || { echo "spec: fill the TODO: lines in spec/SPEC.md first" >&2; exit 1; }

check: spec build
	@echo "check: not defined yet — a gate with nothing behind it must fail" >&2; exit 1

# The candidate: exactly what deploy/SHIPLIST names, verified both ways.
build:
	@rm -rf build/candidate && mkdir -p build/candidate
	@while IFS= read -r f; do [ -n "$$f" ] || continue; test -e "$$f" || { echo "build: $$f is on SHIPLIST but missing" >&2; exit 1; }; done < deploy/SHIPLIST
	@# ponytail: root .gitignore only; nested .gitignore files and ! negations are not honored
	@rsync -a --recursive --exclude-from=.gitignore --files-from=deploy/SHIPLIST . build/candidate/
	@cd build/candidate && find . -mindepth 1 -maxdepth 1 | sed "s|^./||" | while IFS= read -r f; do grep -qxF -e "$$f" -e "$$f/" ../../deploy/SHIPLIST || { echo "build: $$f is not on SHIPLIST" >&2; exit 1; }; done

# Production test on the candidate. rc and release run it after the bump,
# so the artifact it passes is the artifact that gets tagged.
accept: build
	@echo "accept: not defined yet — a gate with nothing behind it must fail" >&2; exit 1

rc:
	@$(LANE) rc --bump $(BUMP)

uat:
	@$(LANE) uat

release:
	@$(LANE) release --bump $(BUMP)

# Gate (tag matches channel, clean tree), then `make ship CHANNEL=...`.
deploy:
	@test -n "$(CHANNEL)" || { echo "deploy: say CHANNEL=staging or CHANNEL=production" >&2; exit 1; }
	@! grep -n "^| $(CHANNEL) |.*TODO" deploy/README.md >&2 || { echo "deploy: fill the $(CHANNEL) row in deploy/README.md first" >&2; exit 1; }
	@$(LANE) deploy --channel $(CHANNEL)

# The per-project ship body. Name both targets and their rollback in README.
ship:
	@echo "ship: no $(CHANNEL) target defined yet — name it in README and fill this recipe" >&2; exit 1

.PHONY: help spec run check build accept rc uat release deploy ship
