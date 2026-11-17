"""Voice-line helpers: trim lead/tail silence, and find phrase starts for callout cues.

usage:  vo.py trim RAW_DIR OUT_DIR     trim every RAW_DIR/*.mp3 into OUT_DIR (same names)
        vo.py cues FILE.mp3 [...]       print phrase start times (s) per file, for `cue` values
        vo.py autocue SPEC.json [--dry-run]
                                        set each callout's `cue` from its `at` (words of the
                                        shot's `line` that name what it rings) and write the spec
exit:   0 ok · 1 ffmpeg failed · 2 bad arguments or spec
Best cues come from word timings: save the ElevenLabs transcript words (creative_transcribe_audio
on the speech node, `words` = [{text, start, end}]) as <vo>/<shot>.words.json, timed on the RAW
take; `trim` records each take's removed lead in <out>/trim.json and autocue subtracts it. The
ring then leads the words by 0.15 s. Without a words file autocue falls back to the words' share
of the line's voiced time (silencedetect -35 dB, 0.18 s), 0.3 s early, snapped to a phrase start
within 0.6 s: mean error 0.36 s, worst 2.1 s on 24 hand-set cues, so check those by ear.
"""

import glob
import itertools
import json
import os
import re
import subprocess
import sys

TRIM = (
    "silenceremove=start_periods=1:start_threshold=-45dB,areverse,"
    "silenceremove=start_periods=1:start_threshold=-45dB,areverse"
)


def silences(f, db=-35, d=0.18):
    err = subprocess.run(
        ["ffmpeg", "-i", f, "-af", f"silencedetect=n={db}dB:d={d}", "-f", "null", "-"],
        capture_output=True,
        text=True,
        check=False,
    ).stderr
    st = [float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", err)]
    en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    return list(zip(st, en + [None] * (len(st) - len(en))))


def starts(f):
    err = subprocess.run(
        ["ffmpeg", "-i", f, "-af", "silencedetect=n=-35dB:d=0.18", "-f", "null", "-"],
        capture_output=True,
        text=True,
        check=False,
    ).stderr
    return [0.0] + [
        round(float(x), 2) for x in re.findall(r"silence_end: ([\d.]+)", err)
    ]


def duration(f):
    return float(
        subprocess.check_output(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "csv=p=0",
                f,
            ]
        )
    )


def norm(t):
    return re.sub(r"[^\w']+", " ", t.lower()).split()


def cue_from_words(words, at, lead):
    """Start (s, trimmed take) of the first run of `words` matching `at`, 0.15 s early."""
    want, toks = norm(at), [norm(w["text"]) for w in words]
    flat = [(t, w["start"]) for ts, w in zip(toks, words) for t in ts]
    for i in range(len(flat) - len(want) + 1):
        if [t for t, _ in flat[i : i + len(want)]] == want:
            return round(max(0.0, flat[i][1] - lead - 0.15), 2)
    raise ValueError(f"'{at}' is not in the transcript")


def cue_for(line, words, dur, phrases, gaps=()):
    """Estimated start (s) of `words` by its share of the line's voiced time, snapped to a phrase."""
    text = re.sub(r"\[[^\]]*\]", "", line)
    text = re.sub(r"\s+", " ", text).strip()
    i = text.lower().find(words.lower())
    if i < 0:
        raise ValueError(f"'{words}' is not in the line")
    segs, t0 = [], 0.0  # voiced stretches between silences
    for s, e in gaps:
        if s > t0:
            segs.append((t0, s))
        t0 = e if e is not None else dur
    if t0 < dur:
        segs.append((t0, dur))
    need = sum(e - s for s, e in segs) * i / max(len(text), 1)
    est = segs[0][0] if segs else 0.0
    for s, e in segs:
        if need <= e - s:
            est = s + need
            break
        need -= e - s
        est = e
    est = max(0.0, est - 0.3)
    near = min(
        [t for t in phrases if t < dur - 0.3] or [0.0], key=lambda t: abs(t - est)
    )
    return round(near if abs(near - est) <= 0.6 else est, 2)


def autocue(spec_path, dry):
    try:
        with open(spec_path) as fh:
            spec = json.load(fh)
    except (OSError, ValueError) as e:
        print("bad spec:", e, file=sys.stderr)
        sys.exit(2)
    root = os.path.dirname(os.path.abspath(spec_path))
    vo_dir = os.path.join(root, spec.get("vo", "vo"))
    leads = {}
    tf = os.path.join(vo_dir, "trim.json")
    if os.path.exists(tf):
        with open(tf) as fh:
            leads = json.load(fh)
    bad = 0
    for s in spec["shots"]:
        cs = [c for c in s.get("callouts") or [] if c.get("at")]
        if not cs:
            continue
        f = os.path.join(vo_dir, s["name"] + ".mp3")
        if not s.get("line") or not os.path.exists(f):
            print(f"{s['name']}: needs a line and {f}", file=sys.stderr)
            bad += 1
            continue
        dur, ph, gaps = duration(f), starts(f), silences(f)
        wf = os.path.join(vo_dir, s["name"] + ".words.json")
        words = None
        if os.path.exists(wf):
            with open(wf) as fh:
                words = json.load(fh)
            words = words.get("words", words) if isinstance(words, dict) else words
        lead = leads.get(s["name"] + ".mp3", 0.0)
        for c in cs:
            try:
                if words:
                    c["cue"] = cue_from_words(words, c["at"], lead)
                else:
                    c["cue"] = cue_for(s["line"], c["at"], dur, ph, gaps)
                how = "words" if words else "estimate"
                print(f"{s['name']:24s} {c['cue']:5.2f}s  {how:8s} {c['at']}")
            except ValueError as e:
                print(f"{s['name']}: {e}", file=sys.stderr)
                bad += 1
        cues = [c.get("cue", 0) for c in s["callouts"]]
        if any(b <= a for a, b in itertools.pairwise(cues)):
            print(
                f"{s['name']}: cues do not rise {cues}; reword `at` or set `cue` by hand",
                file=sys.stderr,
            )
            bad += 1
    if bad:
        sys.exit(2)
    if not dry:
        with open(spec_path, "w") as fh:
            json.dump(spec, fh, indent=2)
            fh.write("\n")
        print("wrote", spec_path)


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0 if a else 2)
    if a[0] == "trim" and len(a) == 3:
        os.makedirs(a[2], exist_ok=True)
        leads = {}
        for f in sorted(glob.glob(os.path.join(a[1], "*.mp3"))):
            g = silences(f, -45, 0.01)
            leads[os.path.basename(f)] = (
                round(g[0][1], 3) if g and g[0][0] <= 0.01 and g[0][1] else 0.0
            )
            r = subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-v",
                    "error",
                    "-i",
                    f,
                    "-af",
                    TRIM,
                    os.path.join(a[2], os.path.basename(f)),
                ]
            )
            if r.returncode:
                sys.exit(1)
            print("ok", os.path.basename(f))
        with open(os.path.join(a[2], "trim.json"), "w") as fh:
            json.dump(leads, fh, indent=1)
    elif a[0] == "cues" and len(a) > 1:
        for f in a[1:]:
            print(os.path.basename(f), starts(f))
    elif a[0] == "autocue" and len(a) in (2, 3):
        autocue(a[1], "--dry-run" in a)
    else:
        print(__doc__, file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
