"""Build and mix the release video from a video spec, its frames and its voice lines.

Each shot is a chain of callout stills that crossfade (0.25 s) at the cue times; shots
crossfade into each other (0.6 s). A voice line starts 0.4 s into its shot and a shot lasts
max(planned seconds, voice + 1.4 s). Then the music bed is ducked under the voice with a
sidechain compressor and the result is limited to -0.5 dB peak.

usage:  build.py SPEC.json [--dry-run]
reads:  <frames>/<shot>-<k>.png  (capture.mjs)   <vo>/<shot>.mp3  (trimmed voice lines)
        <music> wav if the spec names one, else generates music.wav with music.py
writes: <out>.mp4 (final) and work/ (per-shot clips, voiced.mp4)
exit:   0 ok · 1 ffmpeg failed · 2 bad spec or missing input
"""

import json
import os
import subprocess
import sys

X, X2, LEAD, TAIL = 0.6, 0.25, 0.4, 1.0


def sh(cmd):
    r = subprocess.run(cmd)
    if r.returncode:
        sys.exit(1)


def probe(path):
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
                path,
            ]
        )
    )


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0 if a else 2)
    dry = "--dry-run" in a
    spec_path = os.path.abspath(a[0])
    try:
        spec = json.load(open(spec_path))
    except Exception as e:
        print("bad spec:", e, file=sys.stderr)
        sys.exit(2)
    os.chdir(os.path.dirname(spec_path))
    frames, vo_dir, out = (
        spec.get("frames", "frames"),
        spec.get("vo", "vo"),
        spec.get("out", "release-video"),
    )
    vw, vh = spec.get("viewport", [1440, 900])
    W = spec.get("width", 1920)
    H = round(W * vh / vw / 2) * 2
    V = f"scale={W}:{H},fps=30,format=yuv420p,setsar=1"
    shots = spec["shots"]

    missing, plan = [], []
    for s in shots:
        cs = s.get("callouts") or [{}]
        keys, k = [], 0  # frame index per cue: `same` reuses an earlier frame
        for c in cs:
            if "same" in c:
                keys.append(c["same"])
            else:
                keys.append(k)
                k += 1
        for i in set(keys):
            f = f"{frames}/{s['name']}-{i}.png"
            if not os.path.exists(f):
                missing.append(f)
        v = f"{vo_dir}/{s['name']}.mp3"
        has_vo = os.path.exists(v)
        if s.get("line") and not has_vo:
            missing.append(v)
        vd = probe(v) if has_vo else 0.0
        d = round(max(s.get("seconds", 5), vd + LEAD + TAIL), 2)
        cues = [0.0 if not c.get("cue") else c["cue"] + LEAD for c in cs]
        if any(b <= a_ for a_, b in zip(cues, cues[1:])) or cues[-1] >= d:
            print(
                f"bad cues in {s['name']}: must rise and fall inside the shot ({d}s)",
                file=sys.stderr,
            )
            sys.exit(2)
        plan.append((s["name"], d, keys, cues, v if has_vo else None))
    if missing:
        print("missing inputs:\n  " + "\n  ".join(missing), file=sys.stderr)
        sys.exit(2)
    n, last = plan[-1][0], plan[-1]
    if last[4]:
        plan[-1] = (
            n,
            max(last[1], probe(last[4]) + LEAD + 1.6),
            *last[2:],
        )  # room for the fade-out
    total = sum(p[1] for p in plan) - X * (len(plan) - 1)
    for name, d, keys, cues, v in plan:
        print(
            f"{name:24s} {d:6.2f}s  frames {keys}  cues {[round(c, 2) for c in cues]}  {'voice' if v else 'silent'}"
        )
    print(f"total {total:.2f}s")
    if dry:
        return

    os.makedirs("work", exist_ok=True)
    for name, d, keys, cues, _ in plan:
        L = [cues[k + 1] - cues[k] + X2 for k in range(len(cues) - 1)] + [d - cues[-1]]
        inp = []
        for key, ln in zip(keys, L):
            inp += ["-loop", "1", "-t", f"{ln:.3f}", "-i", f"{frames}/{name}-{key}.png"]
        f = [f"[{i}:v]{V}[v{i}]" for i in range(len(keys))]
        prev = "v0"
        for k in range(1, len(keys)):
            f.append(
                f"[{prev}][v{k}]xfade=transition=fade:duration={X2}:offset={cues[k]:.3f}[x{k}]"
            )
            prev = f"x{k}"
        sh(
            [
                "ffmpeg",
                "-y",
                "-v",
                "error",
                *inp,
                "-filter_complex",
                ";".join(f),
                "-map",
                f"[{prev}]",
                "-t",
                str(d),
                "-c:v",
                "libx264",
                "-crf",
                "16",
                "-preset",
                "fast",
                f"work/{name}.mp4",
            ]
        )

    N = len(plan)
    args = ["ffmpeg", "-y", "-v", "error"]
    for p in plan:
        args += ["-i", f"work/{p[0]}.mp4"]
    voiced = [(i, p[4]) for i, p in enumerate(plan) if p[4]]
    for _, v in voiced:
        args += ["-i", v]
    f = [f"[{i}:v]{V}[v{i}]" for i in range(N)]
    prev, off, starts = "v0", 0.0, [0.0]
    for i in range(1, N):
        off += plan[i - 1][1] - X
        starts.append(off)
        f.append(
            f"[{prev}][v{i}]xfade=transition=fade:duration={X}:offset={off:.2f}[x{i}]"
        )
        prev = f"x{i}"
    f.append(f"[{prev}]fade=t=out:st={total - 0.8:.2f}:d=0.8[vout]")
    for j, (i, _) in enumerate(voiced):
        ms = int((starts[i] + LEAD) * 1000)
        f.append(f"[{N + j}:a]aresample=44100,adelay={ms}|{ms}[a{j}]")
    f.append(
        "".join(f"[a{j}]" for j in range(len(voiced)))
        + f"amix=inputs={len(voiced)}:normalize=0,afade=t=out:st={total - 0.8:.2f}:d=0.8,atrim=0:{total:.2f}[aout]"
    )
    sh(
        args
        + [
            "-filter_complex",
            ";".join(f),
            "-map",
            "[vout]",
            "-map",
            "[aout]",
            "-c:v",
            "libx264",
            "-crf",
            "20",
            "-preset",
            "medium",
            "-c:a",
            "aac",
            "-b:a",
            "160k",
            "-movflags",
            "+faststart",
            "work/voiced.mp4",
        ]
    )

    music = spec.get("music")
    if not music:
        music = "music.wav"
        sh(
            [
                sys.executable,
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "music.py"),
                str(round(total + 1, 1)),
                music,
            ]
        )
    # Voice is mono: pan it to both ears. Music: light echo, 0.7 gain, ducked 4:1 under the voice.
    sh(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-i",
            "work/voiced.mp4",
            "-i",
            music,
            "-filter_complex",
            f"[0:a]aresample=44100,pan=stereo|c0=c0|c1=c0,apad=whole_dur={total:.2f},asplit=2[vo][key];"
            f"[1:a]aresample=44100,aecho=0.8:0.5:45:0.12,volume={spec.get('musicGain', 0.7)}[mus];"
            "[mus][key]sidechaincompress=threshold=0.04:ratio=4:attack=40:release=300[duck];"
            "[vo][duck]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95[a]",
            "-map",
            "0:v",
            "-map",
            "[a]",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-movflags",
            "+faststart",
            f"{out}.mp4",
        ]
    )
    lv = subprocess.run(
        ["ffmpeg", "-i", f"{out}.mp4", "-af", "volumedetect", "-f", "null", "-"],
        capture_output=True,
        text=True,
    ).stderr
    print(
        f"wrote {out}.mp4  {probe(out + '.mp4'):.1f}s  "
        + " ".join(
            ln.split("] ")[-1]
            for ln in lv.splitlines()
            if "mean_volume" in ln or "max_volume" in ln
        )
    )


if __name__ == "__main__":
    main()
