import os, sys, json, wave, subprocess
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from timeline import *
import render as R

SP = R.SP
SR = 48000
rng = np.random.default_rng(7)
TOTAL = R.TOTAL
N = int(TOTAL * SR) + SR

def env(n, a=0.005, d=0.2):
    t = np.arange(n) / SR
    return np.minimum(1, t / a) * np.exp(-t / d)

def sweep(f0, f1, dur):
    n = int(dur * SR); t = np.arange(n) / SR
    f = f0 * (f1 / f0) ** (t / dur)
    return np.sin(2 * np.pi * np.cumsum(f) / SR)

def lp(x, k):
    return np.convolve(x, np.ones(k) / k, mode="same")

def bandsweep_noise(dur, f0, f1, bw=0.35):
    """noise whose passband sweeps f0->f1 (block-wise FFT filter, no scipy)"""
    n = int(dur * SR); x = rng.standard_normal(n); out = np.zeros(n)
    blk = 1024
    for i in range(0, n, blk // 2):
        seg = x[i:i + blk]
        if len(seg) < 16: break
        win = np.hanning(len(seg))
        X = np.fft.rfft(seg * win); fr = np.fft.rfftfreq(len(seg), 1 / SR)
        fc = f0 * (f1 / f0) ** (i / n)
        X *= np.exp(-0.5 * (np.log(np.maximum(fr, 1) / fc) / bw) ** 2)
        out[i:i + len(seg)] += np.fft.irfft(X, len(seg))
    return out / (np.abs(out).max() + 1e-9)

def sfx(kind):
    if kind == "bubble":      # bouncy text pop: quick upward "bloop" + click
        n = int(0.11 * SR)
        s = sweep(380, 1500, 0.11) * env(n, 0.002, 0.035)
        click = np.zeros(n); click[:60] = rng.standard_normal(60) * np.linspace(1, 0, 60)
        return 0.75 * s + 0.35 * click
    if kind == "bubble2":     # slightly lower variant for alternation
        n = int(0.11 * SR)
        return 0.75 * sweep(300, 1100, 0.11) * env(n, 0.002, 0.035)
    if kind == "boing":       # cartoon spring for stickers
        n = int(0.42 * SR); t = np.arange(n) / SR
        f = 260 + 220 * np.exp(-t * 6) * np.sin(2 * np.pi * 18 * t) + 140 * t
        return 0.6 * np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.003, 0.16)
    if kind == "whip":        # whip-pan whoosh for cuts
        s = bandsweep_noise(0.32, 500, 6000)
        n = len(s); t = np.arange(n) / SR
        return 0.85 * s * np.sin(np.pi * t / t[-1]) ** 1.5
    if kind == "swoosh":      # tag sliding in
        s = bandsweep_noise(0.25, 2500, 900)
        n = len(s); t = np.arange(n) / SR
        return 0.55 * s * np.sin(np.pi * t / t[-1]) ** 2
    if kind == "type":        # one keyboard tick
        n = int(0.03 * SR); t = np.arange(n) / SR
        c = rng.standard_normal(n) * env(n, 0.0003, 0.004)
        return 0.6 * (c + 0.5 * np.sin(2 * np.pi * 1800 * t) * env(n, 0.0003, 0.006))
    if kind == "sparkle":     # twinkle "ting" with shimmer for stars
        n = int(0.7 * SR); t = np.arange(n) / SR
        x = np.zeros(n)
        for k, f in enumerate((2637, 3520, 4186, 5274)):
            o = int(k * 0.035 * SR)
            x[o:] += np.sin(2 * np.pi * f * t[: n - o]) * env(n - o, 0.001, 0.18) * (0.9 - 0.15 * k)
        return 0.35 * x
    if kind == "thump":       # punch-in zoom
        n = int(0.18 * SR)
        return 0.8 * sweep(140, 60, 0.18) * env(n, 0.002, 0.05)
    if kind == "vineboom":    # big dramatic boom
        n = int(1.3 * SR); t = np.arange(n) / SR
        s = np.sin(2 * np.pi * np.cumsum(70 * np.exp(-t * 1.2) + 40) / SR)
        s = np.tanh(3 * s) * env(n, 0.002, 0.45)
        click = np.zeros(n); click[:200] = rng.standard_normal(200) * np.linspace(1, 0, 200)
        return 0.9 * s + 0.4 * click
    if kind == "pop":
        return 0.7 * sweep(1200, 320, 0.09) * env(int(0.09 * SR), 0.002, 0.03)
    if kind == "ding":
        n = int(0.9 * SR); t = np.arange(n) / SR
        return 0.35 * (np.sin(2*np.pi*1568*t) + 0.6*np.sin(2*np.pi*2349*t) + 0.3*np.sin(2*np.pi*3136*t)) * env(n, 0.002, 0.25)
    if kind == "whoosh":
        n = int(0.45 * SR); t = np.arange(n) / SR
        nz = rng.standard_normal(n)
        sh = np.sin(np.pi * t / t[-1]) ** 2
        return 0.6 * (lp(nz, 6) - lp(nz, 40)) * sh
    if kind == "boom":
        n = int(1.0 * SR)
        s = sweep(110, 38, 1.0) * env(n, 0.003, 0.35)
        nz = lp(rng.standard_normal(n), 30) * env(n, 0.001, 0.06)
        return 0.95 * s + 0.6 * nz
    if kind == "scratch":
        n = int(0.35 * SR); t = np.arange(n) / SR
        f = 600 + 500 * np.sin(2 * np.pi * 7 * t)
        nz = rng.standard_normal(n)
        tone = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR))
        return 0.25 * lp(tone * 0.6 + nz * 0.4, 5) * env(n, 0.005, 0.15)
    if kind == "tick":
        n = int(0.25 * SR); t = np.arange(n) / SR
        x = np.zeros(n)
        for k in range(3):
            o = int(k * 0.07 * SR)
            m = min(n - o, int(0.02 * SR))
            x[o:o + m] += np.sin(2 * np.pi * 2600 * t[:m]) * env(m, 0.0005, 0.006)
        return 0.5 * x
    raise ValueError(kind)

def riser(dur):
    n = int(dur * SR); t = np.arange(n) / SR
    nz = rng.standard_normal(n)
    hp = nz - lp(nz, 4)
    ramp = (t / dur) ** 2
    tone = sweep(200, 1600, dur)
    return (0.5 * hp + 0.35 * tone) * ramp

def place(buf, sig, t, gain=1.0):
    i = int(t * SR)
    j = min(len(buf), i + len(sig))
    buf[i:j] += gain * sig[: j - i]

# ---------- SFX track ----------
fx = np.zeros(N)
# hook: rush-in whoosh, impact on "nè nè", title slams, burst
place(fx, sfx("whoosh"), 0.0, 1.0)
place(fx, sfx("boom"), 0.02, 1.0)
place(fx, sfx("pop"), 0.10, 0.9)
place(fx, sfx("boom"), 0.30, 0.6)
place(fx, sfx("pop"), 0.62, 1.0)
place(fx, sfx("boom"), 0.62, 0.6)
place(fx, sfx("boom"), 0.92, 0.9)
place(fx, sfx("whoosh"), 0.88, 1.0)
place(fx, sfx("tick"), 1.8, 0.8)
place(fx, riser(HOOK_FX - 1.3), 1.3, 0.35)
place(fx, sfx("whoosh"), HOOK_FX - 0.3, 0.8)
# ---- automatic "everything that appears makes a sound" (like the reference video) ----
events = []
for i, (a, b, txt, emo) in enumerate(CAPS):
    big = txt.startswith("*") and txt.endswith("*")
    has_hl = "*" in txt
    events.append((R.s2o(a), "bubble" if i % 2 == 0 else "bubble2", 0.75))
    if big:
        events.append((R.s2o(a), "boing", 0.45))
    elif has_hl:
        events.append((R.s2o(a) + 0.05, "sparkle", 0.45))
for a, b, code, x, y, sz in STICKERS:
    events.append((R.s2o(a), "boing", 0.7))
for a, b, txt in TAGS:
    o = R.s2o(a)
    events.append((o, "swoosh", 0.8))
    nchar = len(txt.replace("*", ""))
    for c in range(0, nchar, 2):             # typewriter ticks
        events.append((o + 0.22 + c * TYPE_CPS_DT, "type", 0.55))
    events.append((o + 0.22 + nchar * TYPE_CPS_DT, "sparkle", 0.5))
for off in R.offsets[1:]:                   # whip whoosh on every cut
    events.append((off - 0.12, "whip", 0.8))
for a, b, zz in ZOOMS:
    events.append((R.s2o(a), "thump", 0.6))
for t0, dur in FLASHES:
    events.append((R.s2o(t0), "vineboom", 0.9))
for t, k in SFX:                            # hand-placed accents
    events.append((R.s2o(t), k, 0.7))
events.sort()
last = {}
for t, k, g in events:
    if t < HOOK_FX - 0.05 and k in ("bubble", "bubble2", "thump"):
        continue                            # hook already has its own sound design
    if k in last and t - last[k] < 0.08:
        continue
    last[k] = t
    place(fx, sfx(k), max(0.0, t), g)
place(fx, sfx("whoosh"), R.MAIN_END - 0.2, 1.0)
place(fx, sfx("ding"), R.MAIN_END + 0.15, 0.9)
place(fx, sfx("pop"), R.MAIN_END + 0.5, 1.0)

# ---------- music: upbeat 4/4 loop, 124 bpm ----------
bpm = 124; beat = 60 / bpm
mus = np.zeros(N)
def note(f, dur, kind="pluck"):
    n = int(dur * SR); t = np.arange(n) / SR
    if kind == "bass":
        w = np.sin(2*np.pi*f*t) + 0.3*np.sin(2*np.pi*2*f*t)
        return w * env(n, 0.005, 0.18)
    w = np.sin(2*np.pi*f*t) + 0.5*np.sin(2*np.pi*2*f*t) + 0.25*np.sin(2*np.pi*3*f*t)
    return w * env(n, 0.003, 0.12)
def kick():
    n = int(0.3 * SR); return sweep(150, 45, 0.3) * env(n, 0.001, 0.09)
def clap():
    n = int(0.2 * SR); nz = rng.standard_normal(n)
    return (nz - lp(nz, 8)) * env(n, 0.001, 0.05)
def hat():
    n = int(0.06 * SR); nz = rng.standard_normal(n)
    return (nz - lp(nz, 3)) * env(n, 0.0005, 0.012)
# chords: C  G  Am F  (in Hz, root + triad)
prog = [(130.81, [523.25, 659.25, 783.99]), (98.00, [493.88, 587.33, 783.99]),
        (110.00, [523.25, 659.25, 880.00]), (87.31, [523.25, 698.46, 880.00])]
start = R.hook_len  # music starts after hook (hook gets impact sfx)
t = start; b = 0
while t < TOTAL:
    bar = (b // 4) % 4
    root, triad = prog[bar]
    place(mus, kick(), t, 0.9)
    if b % 2 == 1:
        place(mus, clap(), t, 0.35)
    for h in (0, 0.5):
        place(mus, hat(), t + h * beat, 0.25)
    place(mus, note(root, beat * 0.9, "bass"), t, 0.55)
    place(mus, note(root, beat * 0.4, "bass"), t + 0.5 * beat, 0.4)
    arp = triad[(b * 2) % 3], triad[(b * 2 + 1) % 3]
    place(mus, note(arp[0], beat * 0.45), t, 0.14)
    place(mus, note(arp[1], beat * 0.45), t + 0.5 * beat, 0.14)
    t += beat; b += 1
# fade out music at end
fade = int(1.2 * SR); e = int(TOTAL * SR)
mus[e - fade:e] *= np.linspace(1, 0, fade); mus[e:] = 0

def save(path, x):
    x = x / max(1e-9, np.abs(x).max()) * 0.9
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())
W = f"{SP}/work"
save(f"{W}/sfx.wav", fx[: int(TOTAL * SR)])
save(f"{W}/music.wav", mus[: int(TOTAL * SR)])

# ---------- voice track (ffmpeg trims + concat) ----------
parts, labels = [], []
segs = SEGMENTS
fc = []
for i, (a, b) in enumerate(segs):
    vol = 1.0
    pad = ""
    fc.append(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={b-a-0.03:.3f}:d=0.03,volume={vol}{pad}[a{i}]")
    labels.append(f"[a{i}]")
fc.append("".join(labels) + f"concat=n={len(segs)}:v=0:a=1,highpass=f=100,lowpass=f=10000,afftdn=nr=20:nf=-30:tn=1,"
          f"equalizer=f=250:t=q:w=1:g=-3,equalizer=f=3200:t=q:w=1.2:g=5,equalizer=f=6500:t=q:w=1:g=2,"
          f"acompressor=threshold=-24dB:ratio=4:attack=5:release=100:makeup=4,alimiter=limit=0.9,apad=whole_dur={TOTAL:.3f},"
          f"atrim=0:{TOTAL:.3f},aresample={SR}[v]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", R.SRC, "-filter_complex", ";".join(fc),
                "-map", "[v]", "-ac", "1", f"{W}/voice.wav"], check=True)
print("audio ok", TOTAL)
