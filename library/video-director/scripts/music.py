"""Bright, upbeat product-announcement music bed (pure stdlib, no samples, no licence issues).

D major I-V-vi-IV at 116 BPM: syncopated chord stabs, bell arpeggio, eighth-note bass,
four-on-the-floor kick, claps, hats. Fades in 0.6 s, out over the last 3 s. Peak 0.8.

usage: music.py SECONDS [OUT.wav]      (default OUT: music.wav)
exit:  0 ok, 2 bad arguments
"""

import math
import array
import wave
import random
import sys

if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
    print(__doc__)
    sys.exit(0 if len(sys.argv) > 1 else 2)
try:
    TOTAL = float(sys.argv[1])
except ValueError:
    print(__doc__, file=sys.stderr)
    sys.exit(2)
OUT = sys.argv[2] if len(sys.argv) > 2 else "music.wav"
SR = 32000
N = int(SR * TOTAL)
L = array.array("f", [0.0]) * N
R = array.array("f", [0.0]) * N
BEAT = 60 / 116
BAR = BEAT * 4


def hz(m):
    return 440 * 2 ** ((m - 69) / 12)


# D, A, Bm, G (one bar each): root, chord tones
chords = [
    (38, [62, 66, 69, 74]),
    (45, [61, 64, 69, 73]),
    (47, [62, 66, 71, 74]),
    (43, [62, 67, 71, 74]),
]
random.seed(7)


def add(t0, dur, f, amp, atk, rel, harm=((1, 1.0),), decay=None, pan=0.0):
    s0, s1 = int(t0 * SR), min(N, int((t0 + dur + rel) * SR))
    gl, gr = amp * (1 - pan) / 2**0.5, amp * (1 + pan) / 2**0.5
    w = [(2 * math.pi * f * k / SR, a) for k, a in harm]
    for i in range(max(0, s0), s1):
        t = (i - s0) / SR
        n = i - s0
        env = min(1.0, t / atk) if t < dur else max(0.0, 1 - (t - dur) / rel)
        if decay:
            env *= math.exp(-t / decay)
        v = 0.0
        for dw, a in w:
            v += a * math.sin(dw * n)
        v *= env
        L[i] += gl * v
        R[i] += gr * v


def noise(t0, length, amp, decay, hp=True, pan=0.0):
    s0 = int(t0 * SR)
    prev = 0.0
    gl, gr = amp * (1 - pan), amp * (1 + pan)
    for i in range(s0, min(N, s0 + int(length * SR))):
        x = random.uniform(-1, 1)
        v = (x - prev) if hp else x
        prev = x
        v *= math.exp(-(i - s0) / SR / decay)
        L[i] += gl * v
        R[i] += gr * v


bars = int(TOTAL / BAR) + 1
outro = TOTAL - 4.5
for b in range(bars):
    t = b * BAR
    root, tones = chords[b % 4]
    if t > TOTAL:
        break
    late = t >= outro
    # chord stabs: 1, the "and" of 2, and 4 — piano-ish, bright partials, slight spread
    for pos in ((0, 2.0), (1.5, 1.0), (3.0, 0.9)) if not late else ((0, 3.6),):
        for j, m in enumerate(tones[:3]):
            add(
                t + pos[0] * BEAT,
                0.05,
                hz(m),
                0.030,
                0.005,
                min(0.5, pos[1] * BEAT),
                ((1, 1), (2, 0.45), (3, 0.2), (4, 0.1)),
                decay=0.45 if not late else 1.6,
                pan=(j - 1) * 0.35,
            )
    if late:
        continue
    # bass: eighth notes from bar 1, octave pop on the last eighth
    if b >= 1:
        for k in range(8):
            add(
                t + k * BEAT / 2,
                BEAT * 0.35,
                hz(root + (12 if k == 7 else 0)),
                0.085,
                0.004,
                0.05,
                ((1, 1), (2, 0.35), (3, 0.1)),
            )
    # bell arpeggio in 16ths, two octaves up, from bar 2
    if b >= 2:
        arp = [tones[0], tones[1], tones[2], tones[3], tones[2], tones[1]]
        for k in range(16):
            if k % 4 == 3 and b % 2:
                continue  # little gaps so it breathes
            add(
                t + k * BEAT / 4,
                0.02,
                hz(arp[k % len(arp)] + 12),
                0.016,
                0.002,
                0.25,
                ((1, 1), (2.76, 0.25), (5.4, 0.08)),
                decay=0.18,
                pan=0.45 if k % 2 else -0.45,
            )
    # drums from bar 2: kick on every beat, clap on 2 and 4, closed hats on offbeats
    if b >= 2:
        for beat in range(4):
            s0 = int((t + beat * BEAT) * SR)
            for i in range(s0, min(N, s0 + int(0.2 * SR))):
                x = (i - s0) / SR
                f = 48 + 90 * math.exp(-x / 0.025)
                v = 0.17 * math.exp(-x / 0.07) * math.sin(2 * math.pi * f * x)
                L[i] += v
                R[i] += v
            if beat in (1, 3):
                for d in (0, 0.012, 0.022):
                    noise(t + beat * BEAT + d, 0.15, 0.035, 0.05, hp=False)
            noise(t + (beat + 0.5) * BEAT, 0.06, 0.03, 0.018, pan=0.3)
# fade in/out, normalize
fi, fo = int(0.6 * SR), int(3 * SR)
for i in range(fi):
    L[i] *= i / fi
    R[i] *= i / fi
for i in range(fo):
    L[N - 1 - i] *= i / fo
    R[N - 1 - i] *= i / fo
pk = max(max(abs(x) for x in L), max(abs(x) for x in R)) or 1
g = 0.8 / pk
out = array.array("h", [0]) * (2 * N)
for i in range(N):
    out[2 * i] = int(L[i] * g * 32767)
    out[2 * i + 1] = int(R[i] * g * 32767)
with wave.open(OUT, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(out.tobytes())
print("ok", OUT, TOTAL)
