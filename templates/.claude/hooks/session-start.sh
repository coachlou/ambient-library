#!/bin/bash
# Refreshes skill pointers at the start of every Claude session.
# Runs silently — errors are suppressed so they never block a session.
./setup-skills.sh >/dev/null 2>&1 || true
