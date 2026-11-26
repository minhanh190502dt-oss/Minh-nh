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

def sfx(kind):
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
# hook: impact, two slams, burst, banner, riser into the drop
place(fx, sfx("boom"), 0.0, 1.0)
place(fx, sfx("scratch"), 0.0, 0.8)
place(fx, sfx("boom"), 0.15, 0.7)
place(fx, sfx("pop"), 0.15, 1.0)
place(fx, sfx("boom"), 0.45, 0.9)
place(fx, sfx("whoosh"), 0.42, 1.0)
place(fx, sfx("ding"), 1.0, 0.9)
place(fx, sfx("pop"), 1.35, 1.0)
place(fx, sfx("tick"), 1.6, 1.0)
place(fx, riser(R.hook_len - 1.3), 1.3, 0.9)
place(fx, sfx("whoosh"), R.hook_len - 0.3, 1.0)
place(fx, sfx("boom"), R.hook_len, 0.9)
for t, k in SFX:
    place(fx, sfx(k), R.s2o(t), 0.9)
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
segs = [HOOK] + SEGMENTS
fc = []
for i, (a, b) in enumerate(segs):
    vol = 0.2 if i == 0 else 1.0
    pad = f",apad=whole_dur={HOOK_LEN},atrim=0:{HOOK_LEN}" if i == 0 else ""
    fc.append(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={b-a-0.03:.3f}:d=0.03,volume={vol}{pad}[a{i}]")
    labels.append(f"[a{i}]")
fc.append("".join(labels) + f"concat=n={len(segs)}:v=0:a=1,highpass=f=100,lowpass=f=10000,afftdn=nr=20:nf=-30:tn=1,"
          f"equalizer=f=250:t=q:w=1:g=-3,equalizer=f=3200:t=q:w=1.2:g=5,equalizer=f=6500:t=q:w=1:g=2,"
          f"acompressor=threshold=-24dB:ratio=4:attack=5:release=100:makeup=4,alimiter=limit=0.9,apad=whole_dur={TOTAL:.3f},"
          f"atrim=0:{TOTAL:.3f},aresample={SR}[v]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", R.SRC, "-filter_complex", ";".join(fc),
                "-map", "[v]", "-ac", "1", f"{W}/voice.wav"], check=True)
print("audio ok", TOTAL)
