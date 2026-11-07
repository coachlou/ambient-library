# The pipeline. Four verbs, same names in every repo; bodies change per project.
# `make` alone prints this help.
.DEFAULT_GOAL := help
BUMP ?= patch
VERSION := $(shell cat VERSION)

help:
	@echo "make run      start it so you can touch it"
	@echo "make check    lint + unit + smoke; must pass before release"
	@echo "make release  BUMP=patch|minor|major  bump VERSION, date ## Unreleased, tag (never pushes)"
	@echo "make deploy   ship src/ and docs/ to the target named in README (refuses untagged HEAD)"

run:
	@python3 scripts/init_dev_project.py --help

check:
	@python3 scripts/test_init_dev_project.py

release: check
	@test -z "$$(git status --porcelain)" || { echo "release: working tree not clean" >&2; exit 1; }
	@awk '/^## /{ok=($$0=="## Unreleased"); getline l; exit !(ok && l ~ /^- /)}' CHANGELOG.md || { echo "release: add a line under ## Unreleased first" >&2; exit 1; }
	@new=$$(awk -F. -v b=$(BUMP) '{ if (b=="major") {$$1++; $$2=0; $$3=0} else if (b=="minor") {$$2++; $$3=0} else {$$3++} ; print $$1"."$$2"."$$3 }' VERSION); \
	 echo "$$new" > VERSION; \
	 awk -v h="## v$$new — $$(date +%F)" '$$0=="## Unreleased"{print; print ""; print h; next} {print}' CHANGELOG.md > CHANGELOG.tmp && mv CHANGELOG.tmp CHANGELOG.md; \
	 git add VERSION CHANGELOG.md && git commit -q -m "Release v$$new" && git tag "v$$new" && echo "tagged v$$new"

deploy:
	@git describe --tags --exact-match HEAD >/dev/null 2>&1 || { echo "deploy: HEAD is not tagged — run make release first" >&2; exit 1; }
	@echo "deploy: release to ambient-library via ~/.ailib/.aai/skills/admin.md (see README Deploy)" >&2; exit 1

.PHONY: help run check release deploy
