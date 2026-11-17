#!/usr/bin/env python3
"""Check that this machine can make a video before any work starts.

usage:  preflight.py [WORK_DIR]   (default: current folder, where shots.json will live)
prints: one ok / MISSING line per need, with the fix
exit:   0 everything the scripts need is here · 1 something is missing

Voice (ElevenLabs) is checked by the agent, not here: it is a connector, not a binary.
"""

import glob
import os
import shutil
import subprocess
import sys

work = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
missing = 0


def line(ok, what, fix=""):
    global missing
    missing += not ok
    print(f"  {'ok     ' if ok else 'MISSING'} {what}" + ("" if ok else f"  ->  {fix}"))


def out(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True).stdout
    except OSError:
        return ""


ff_fix = "install ffmpeg (macOS: brew install ffmpeg · Debian/Ubuntu: apt install ffmpeg · Windows: winget install ffmpeg)"
for b in ("ffmpeg", "ffprobe"):
    line(bool(shutil.which(b)), b, ff_fix)
if shutil.which("ffmpeg"):
    enc, flt = (
        out(["ffmpeg", "-hide_banner", "-encoders"]),
        out(["ffmpeg", "-hide_banner", "-filters"]),
    )
    line(
        "libx264" in enc,
        "ffmpeg encoder libx264",
        "use a full ffmpeg build (the brew/apt one has it)",
    )
    line("aac" in enc, "ffmpeg encoder aac", "use a full ffmpeg build")
    for f in ("xfade", "sidechaincompress", "silencedetect", "volumedetect", "amix"):
        line(f" {f} " in flt, f"ffmpeg filter {f}", "ffmpeg 4.3 or newer")

line(
    sys.version_info >= (3, 8),
    f"python {sys.version.split()[0]} (3.8+, standard library only)",
    "install Python 3.8+",
)

node = out(["node", "--version"]).strip() if shutil.which("node") else ""
major = int(node.lstrip("v").split(".")[0]) if node else 0
line(major >= 18, f"node {node or 'not found'} (18+)", "install Node 18+ (nodejs.org)")

pw = any(
    os.path.isdir(os.path.join(work, "node_modules", m))
    for m in ("playwright-core", "playwright")
)
line(pw, f"playwright-core in {work}", f"cd '{work}' && npm i playwright-core")

home = os.path.expanduser("~")
browser = (
    os.path.exists("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
    or any(
        shutil.which(b)
        for b in (
            "google-chrome",
            "google-chrome-stable",
            "chromium",
            "chromium-browser",
            "chrome",
        )
    )
    or glob.glob(os.path.join(home, "Library/Caches/ms-playwright/chromium*"))
    or glob.glob(os.path.join(home, ".cache/ms-playwright/chromium*"))
    or glob.glob(
        os.path.join(os.environ.get("LOCALAPPDATA", home), "ms-playwright/chromium*")
    )
)
line(
    bool(browser),
    "a Chrome or Chromium browser",
    "install Google Chrome, or run `npx playwright install chromium`; off a Mac pass its path as `chrome` in the spec",
)

line(bool(shutil.which("curl")), "curl (downloads voice takes)", "install curl")

print("ready" if not missing else f"{missing} missing: fix these before step 1")
sys.exit(1 if missing else 0)
