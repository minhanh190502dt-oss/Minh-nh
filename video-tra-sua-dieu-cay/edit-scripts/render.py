import sys, os, math, random, subprocess, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from timeline import *

SP = "/tmp/claude-0/-home-user-Minh-nh/29b71c64-0cb4-5c97-be8e-a6ce7d01b2d8/scratchpad"
SRC = f"{SP}/work/proxy.mp4"
OUT = sys.argv[1] if len(sys.argv) > 1 else f"{SP}/work/video_only.mp4"
PREVIEW = os.environ.get("PREVIEW")  # e.g. "3.0,12.5" -> write jpgs at those output times only
FONT_BLACK = f"{SP}/fonts/Grandstander%5Bwght%5D.ttf"
FONT_XB = f"{SP}/fonts/Grandstander%5Bwght%5D.ttf"
EMO = f"{SP}/emoji"
YELLOW = (255, 122, 26)   # brand-style orange highlight
PINK = (255, 122, 26)
TEAL = (20, 110, 104)
TEAL_DARK = (9, 70, 66)

# ---------- timeline mapping ----------
hook_len = HOOK_LEN
offsets = []
o = hook_len
for a, b in SEGMENTS:
    offsets.append(o)
    o += b - a
MAIN_END = o
TOTAL = MAIN_END + ENDCARD
json.dump({"hook": HOOK, "segments": SEGMENTS, "offsets": offsets, "total": TOTAL},
          open(f"{SP}/work/map.json", "w"))

def s2o(t):
    for (a, b), off in zip(SEGMENTS, offsets):
        if a - 1e-6 <= t <= b + 1e-6:
            return off + (t - a)
    # snap to nearest following segment start
    for (a, b), off in zip(SEGMENTS, offsets):
        if t < a:
            return off
    return MAIN_END

def o2s(t):
    """return (kind, seg_index, src_time)"""
    if t < hook_len:
        return "hook", -1, min(HOOK[0] + t, HOOK[1] - 0.05)
    for i, ((a, b), off) in enumerate(zip(SEGMENTS, offsets)):
        if t < off + (b - a):
            return "main", i, a + (t - off)
    return "end", len(SEGMENTS) - 1, SEGMENTS[-1][1]

# ---------- caching helpers ----------
_font_cache = {}
def font(path, size):
    k = (path, size)
    if k not in _font_cache:
        f = ImageFont.truetype(path, size)
        try:
            f.set_variation_by_axes([900 if path == FONT_BLACK else 800])
        except Exception:
            pass
        _font_cache[k] = f
    return _font_cache[k]

_emo_cache = {}
def emoji(code, size):
    k = (code, size)
    if k not in _emo_cache:
        _emo_cache[k] = Image.open(f"{EMO}/{code}.png").convert("RGBA").resize((size, size), Image.LANCZOS)
    return _emo_cache[k]

def parse_hl(text):
    """split '*A B* c' into [(word, highlighted)]"""
    out, hl = [], False
    for tok in text.split(" "):
        start = tok.startswith("*")
        if start:
            hl = True
            tok = tok[1:]
        end = tok.endswith("*")
        if end:
            tok = tok[:-1]
        out.append((tok, hl))
        if end:
            hl = False
    return out

def text_block(text, size=86, emo=None, max_w=960, fill=(255, 255, 255), hl_fill=YELLOW,
               stroke=10, fontpath=FONT_BLACK, upper=False, line_gap=1.5):
    f = font(fontpath, size)
    words = parse_hl(text)
    if upper:
        words = [(w.upper(), h) for w, h in words]
    space = f.getlength(" ")
    # wrap: "|" forces a line break; a highlighted phrase is never split across lines
    groups = []
    for w, h in words:
        if w == "|":
            groups.append("BR"); continue
        if h and groups and groups[-1] != "BR" and groups[-1][-1][1]:
            groups[-1].append((w, h))
        else:
            groups.append([(w, h)])
    lines, cur, cur_w = [], [], 0
    for g in groups:
        if g == "BR":
            if cur:
                lines.append(cur)
            cur, cur_w = [], 0
            continue
        gw = sum(f.getlength(w) for w, _ in g) + space * (len(g) - 1)
        if cur and cur_w + space + gw > max_w:
            lines.append(cur); cur, cur_w = [], 0
        for w, h in g:
            ww = f.getlength(w)
            cur_w += (space if cur else 0) + ww
            cur.append((w, h, ww))
    if cur:
        lines.append(cur)
    text_block.last_lines = len(lines)
    lh = int(size * line_gap)
    emo_sz = int(size * 1.25) if emo else 0
    widths = [sum(x[2] for x in L) + space * (len(L) - 1) for L in lines]
    last_extra = (emo_sz + 14) if emo else 0
    Wd = int(max(widths[:-1] + [widths[-1] + last_extra]) + 2 * stroke + 20)
    TP = int(size * 0.7)  # room for stacked Vietnamese diacritics (Ữ, Ế, Ặ...)
    Hd = int(TP + lh * len(lines) + 2 * stroke + size * 0.6)
    img = Image.new("RGBA", (Wd, Hd), (0, 0, 0, 0))
    # drop shadow layer
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(img); ds = ImageDraw.Draw(sh)
    for li, L in enumerate(lines):
        lw = widths[li] + (last_extra if li == len(lines) - 1 else 0)
        x = (Wd - lw) / 2
        y = TP + stroke + li * lh
        for w, h, ww in L:
            inner = max(3, int(stroke * 0.55))
            ds.text((x + 5, y + 8), w, font=f, fill=(0, 0, 0, 130), stroke_width=stroke, stroke_fill=(0, 0, 0, 130))
            d.text((x, y), w, font=f, fill=TEAL_DARK, stroke_width=stroke, stroke_fill=TEAL_DARK)
            if h:
                d.text((x, y), w, font=f, fill=hl_fill, stroke_width=inner, stroke_fill=(255, 255, 255))
            else:
                d.text((x, y), w, font=f, fill=fill, stroke_width=0)
            x += ww + space
        if emo and li == len(lines) - 1:
            img.alpha_composite(emoji(emo, emo_sz), (int(x + 4), int(y - size * 0.12)))
    sh = sh.filter(ImageFilter.GaussianBlur(4))
    sh.alpha_composite(img)
    bb = sh.getchannel("A").getbbox()
    if bb:
        m = 10
        sh = sh.crop((max(0, bb[0] - m), max(0, bb[1] - m), min(sh.width, bb[2] + m), min(sh.height, bb[3] + m)))
    return sh

def pill(text, size=46, bg=PINK, fg=(255, 255, 255)):
    t = text.replace("*", "")
    f = font(FONT_XB, size)
    tw = f.getlength(t)
    pad_x, pad_y = 30, 16
    Wd, Hd = int(tw + 2 * pad_x), int(size * 1.7 + 2 * pad_y)
    img = Image.new("RGBA", (Wd + 12, Hd + 12), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((8, 10, Wd + 8, Hd + 10), radius=Hd // 2, fill=(0, 0, 0, 140))
    d.rounded_rectangle((0, 0, Wd, Hd), radius=Hd // 2, fill=bg + (255,))
    bb = d.textbbox((0, 0), t, font=f)
    d.text((pad_x, (Hd - (bb[3] - bb[1])) / 2 - bb[1]), t, font=f, fill=fg)
    return img

_tb_cache = {}
def cached(key, fn):
    if key not in _tb_cache:
        _tb_cache[key] = fn()
    return _tb_cache[key]

def pop_scale(dt, dur=0.18):
    if dt < 0:
        return 0
    if dt < dur * 0.55:
        return 0.55 + (1.12 - 0.55) * (dt / (dur * 0.55))
    if dt < dur:
        return 1.12 - 0.12 * ((dt - dur * 0.55) / (dur * 0.45))
    return 1.0

def paste_center(frame, img, cx, cy, scale=1.0, alpha=1.0, rot=0):
    if scale <= 0.01 or alpha <= 0.01:
        return
    im = img
    if scale != 1.0:
        im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.BILINEAR)
    if rot:
        im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
    if alpha < 1.0:
        a = im.getchannel("A").point(lambda v: int(v * alpha))
        im = im.copy(); im.putalpha(a)
    frame.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2))) if (
        0 <= int(cx - im.width / 2) and int(cx - im.width / 2) + im.width <= W and
        0 <= int(cy - im.height / 2) and int(cy - im.height / 2) + im.height <= H) else \
        safe_composite(frame, im, int(cx - im.width / 2), int(cy - im.height / 2))

def safe_composite(frame, im, x, y):
    layer = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    layer.paste(im, (x, y), im)
    frame.alpha_composite(layer)

def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3

# ---------- camera ----------
def camera(kind, seg, st, ot):
    z = 1.0
    if kind == "main" and ot < HOOK_FX:
        kind = "hook"
    if kind == "main":
        z = 1.0 if seg % 2 == 0 else 1.07   # jump-cut zoom alternation
        for a, b, zz in ZOOMS:
            if a <= st <= b:
                z *= 1 + (zz - 1) * ease((st - a) / 0.10)
            elif b < st <= b + 0.12:
                z *= 1 + (zz - 1) * (1 - ease((st - b) / 0.12))
    elif kind == "hook":
        # violent punch-in on open, then slow push
        z = 1.55 - 0.43 * ease(ot / 0.35)
        z += 0.12 * max(0.0, ot - 0.35) / (HOOK_FX - 0.35)
        for t0 in (0.15, 0.45):   # micro bumps on each title slam
            if t0 <= ot < t0 + 0.15:
                z += 0.08 * (1 - (ot - t0) / 0.15)
    dx = dy = 0.0
    shakes = list(SHAKES) if kind == "main" else []
    tt = st
    if kind == "hook":
        shakes = [(0.0, 0.35, 34), (0.15, 0.3, 26), (0.45, 0.4, 30), (1.0, 0.25, 14)]
        tt = ot
    for t0, dur, amp in shakes:
        if t0 <= tt <= t0 + dur:
            k = 1 - (tt - t0) / dur
            rnd = random.Random(int(tt * 1000) + int(t0 * 7))
            dx += amp * k * rnd.uniform(-1, 1)
            dy += amp * k * rnd.uniform(-1, 1)
    if (dx or dy) and z < 1.06:
        z = 1.06
    return z, dx, dy

def apply_camera(img, z, dx, dy):
    if z == 1.0 and dx == 0 and dy == 0:
        return img
    cw, ch = W / z, H / z
    cx, cy = W / 2 + dx, H * 0.47 + dy
    x0 = min(max(cx - cw / 2, 0), W - cw)
    y0 = min(max(cy - ch / 2, 0), H - ch)
    return img.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + cw, y0 + ch))


# ---------- hook effects ----------
def slam_scale(dt):
    if dt < 0:
        return 0
    if dt < 0.10:
        return 2.8 - (2.8 - 0.9) * ease(dt / 0.10)
    if dt < 0.18:
        return 0.9 + 0.1 * ((dt - 0.10) / 0.08)
    return 1.0 + 0.035 * math.sin((dt - 0.18) * 7)

def _focus_lines(seed):
    rnd = random.Random(seed)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy = W / 2, H * 0.45
    for _ in range(120):
        a = rnd.uniform(0, 2 * math.pi)
        r0 = rnd.uniform(520, 760)
        r1 = 1500
        wdt = rnd.uniform(0.004, 0.012)
        pts = [(cx + r0 * math.cos(a), cy + r0 * math.sin(a)),
               (cx + r1 * math.cos(a - wdt), cy + r1 * math.sin(a - wdt)),
               (cx + r1 * math.cos(a + wdt), cy + r1 * math.sin(a + wdt))]
        d.polygon(pts, fill=(255, 255, 255, rnd.randint(140, 220)))
    return img

def _vignette():
    y, x = np.ogrid[:H, :W]
    r = np.sqrt(((x - W / 2) / (W / 2)) ** 2 + ((y - H * 0.45) / (H / 2)) ** 2)
    a = np.clip((r - 0.55) / 0.6, 0, 1) * 200
    arr = np.zeros((H, W, 4), np.uint8); arr[..., 3] = a.astype(np.uint8)
    return Image.fromarray(arr, "RGBA")

def glitch(img, t, strength):
    arr = np.asarray(img.convert("RGB")).copy()
    sh = int(18 * strength)
    out = arr.copy()
    out[:, :, 0] = np.roll(arr[:, :, 0], sh, axis=1)
    out[:, :, 2] = np.roll(arr[:, :, 2], -sh, axis=1)
    rnd = random.Random(int(t * 1000))
    for _ in range(int(7 * strength) + 1):
        y0 = rnd.randint(0, H - 80); hgt = rnd.randint(20, 120)
        out[y0:y0 + hgt] = np.roll(out[y0:y0 + hgt], rnd.randint(-80, 80), axis=1)
    return Image.fromarray(out).convert("RGBA")

BURST = [(i * 2 * math.pi / 12 + random.Random(i).uniform(-0.2, 0.2), random.Random(i + 50).uniform(900, 1500),
          ["1f9cb", "1f525", "1f631", "1f4a8"][i % 4], random.Random(i + 9).uniform(-40, 40)) for i in range(12)]

def draw_hook(frame, ot):
    # focus lines (re-drawn every 2 frames for a "vibrating" comic look)
    k = int(ot * FPS / 2) % 4
    fl = cached(("fl", k), lambda: _focus_lines(k))
    a = 0.85 if ot < 2.0 else 0.85 * max(0, 1 - (ot - 2.0) / 1.0)
    paste_center(frame, fl, W / 2, H / 2, 1.0, alpha=a)
    frame.alpha_composite(cached("vig", _vignette))
    # emoji burst from centre at second slam
    bt = ot - 0.45
    if 0 <= bt <= 1.3:
        for ang, spd, code, rot in BURST:
            dist = spd * (1 - (1 - min(bt, 0.8) / 0.8) ** 2) * 0.55
            x = W / 2 + dist * math.cos(ang); y = H * 0.45 + dist * math.sin(ang) * 1.2
            al = 1.0 if bt < 0.9 else max(0, 1 - (bt - 0.9) / 0.4)
            paste_center(frame, emoji(code, 150), x, y, 0.6 + 0.6 * min(1, bt / 0.3), alpha=al, rot=rot * bt)
    t1 = cached("h1", lambda: text_block("TRÀ SỮA", size=165, stroke=15, max_w=1040))
    t2 = cached("h2", lambda: text_block("*ĐIẾU CÀY?!*", size=175, stroke=17, max_w=1060))
    fade = 1.0 if ot < HOOK_FX - 0.3 else max(0.0, (HOOK_FX - ot) / 0.3)
    paste_center(frame, t1, W / 2, 500, slam_scale(ot - 0.15), alpha=fade, rot=-4)
    paste_center(frame, t2, W / 2, 710, slam_scale(ot - 0.45), alpha=fade, rot=3)
    bob = math.sin(ot * 9) * 12
    paste_center(frame, emoji("1f9cb", 220), 150, 290 + bob, pop_scale(ot - 1.2, 0.2), alpha=fade, rot=12)
    paste_center(frame, emoji("1f525", 190), 930, 300 - bob, pop_scale(ot - 1.25, 0.2), alpha=fade, rot=-10)

# ---------- overlays ----------
CAP_Y = 1300

def draw_overlays(frame, kind, seg, st, ot):
    if kind == "main" and ot < HOOK_FX:
        draw_hook(frame, ot)
    if kind == "end":
        et = ot - MAIN_END
        frame.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 130)))
        a = cached("e1", lambda: text_block("mấy bà muốn", size=88))
        b = cached("e2", lambda: text_block("*NHẬP VỀ BÁN* | hông?", size=110, stroke=12))
        c = cached("e3", lambda: pill("comment liền cho tui biết nha", size=50, bg=PINK))
        paste_center(frame, a, W / 2, 700, pop_scale(et, 0.2))
        paste_center(frame, b, W / 2, 880, pop_scale(et - 0.15, 0.22), rot=-2)
        paste_center(frame, c, W / 2, 1080, pop_scale(et - 0.35, 0.2))
        bounce = abs(math.sin(et * 6)) * 40
        paste_center(frame, emoji("1f447", 200), W / 2, 1300 + bounce, pop_scale(et - 0.5, 0.2))
        paste_center(frame, emoji("1f9cb", 220), 170, 470, pop_scale(et - 0.25, 0.2), rot=10)
        paste_center(frame, emoji("1f923", 200), 900, 480, pop_scale(et - 0.35, 0.2), rot=-10)
        return
    # tags (top pill, slide in)
    for a, b, txt in TAGS:
        if a <= st <= b:
            p = cached(("tag", txt), lambda: pill(txt, size=46, bg=TEAL if "comment" not in txt else PINK))
            k = ease((st - a) / 0.2)
            frame.alpha_composite(p, (int(-p.width + (60 + p.width) * k), 230)) if k >= 1 else \
                safe_composite(frame, p, int(-p.width + (60 + p.width) * k), 230)
    # stickers
    for a, b, code, x, y, sz in STICKERS:
        if a <= st <= b:
            bob = math.sin((st - a) * 8 + x) * 14
            rot = math.sin((st - a) * 5 + y) * 10
            paste_center(frame, emoji(code, sz), x, y + bob, pop_scale(st - a, 0.2), rot=rot)
    # captions
    for a, b, txt, emo in CAPS:
        if a <= st < b:
            big = txt.startswith("*") and txt.endswith("*")
            img = cached(("cap", txt), lambda: text_block(txt, size=128 if big else 94, emo=emo,
                                                           stroke=12 if big else 10, upper=False))
            paste_center(frame, img, W / 2, CAP_Y, pop_scale(st - a, 0.16), rot=(-3 if big else 0))
            break
    # red flash
    for t0, dur in FLASHES:
        if t0 <= st <= t0 + dur:
            al = int(150 * (1 - (st - t0) / dur))
            frame.alpha_composite(Image.new("RGBA", (W, H), (255, 30, 30, al)))

# ---------- frame source ----------
class Reader:
    def __init__(self, start, dur):
        self.p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{start:.3f}", "-i", SRC, "-t", f"{dur:.3f}",
                                   "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
        self.last = None
    def read(self):
        buf = self.p.stdout.read(W * H * 3)
        if len(buf) == W * H * 3:
            self.last = Image.frombuffer("RGB", (W, H), buf, "raw", "RGB", 0, 1)
        return self.last

def main():
    nframes = int(round(TOTAL * FPS))
    preview = [float(x) for x in PREVIEW.split(",")] if PREVIEW else None
    enc = None
    if not preview:
        enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                                "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                                "-pix_fmt", "yuv420p", OUT], stdin=subprocess.PIPE)
    readers = {}
    endbg = None
    prev_kind_seg = None
    want = set(int(round(p * FPS)) for p in preview) if preview else None
    for fi in range(nframes):
        ot = fi / FPS
        kind, seg, st = o2s(ot)
        key = (kind, seg)
        if kind == "end":
            if endbg is None:
                endbg = base.filter(ImageFilter.GaussianBlur(14))
            base = endbg
        else:
            if key not in readers:
                for r in readers.values():
                    r.p.kill()
                readers = {}
                a, b = HOOK if kind == "hook" else SEGMENTS[seg]
                readers[key] = Reader(a, b - a + 0.2)
            base = readers[key].read()
        if want is not None and fi not in want and kind != "end":
            continue
        z, dx, dy = camera(kind, seg, st, ot)
        img = apply_camera(base, z, dx, dy).convert("RGBA")
        if ot < HOOK_FX:
            for g0, g1 in ((0.0, 0.28), (0.45, 0.6), (1.6, 1.72), (2.82, 3.0)):
                if g0 <= ot < g1:
                    img = glitch(img, ot, 1.0 - 0.5 * (ot - g0) / (g1 - g0))
        draw_overlays(img, kind, seg, st, ot)
        if ot < 0.12:
            img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(255 * (1 - ot / 0.12)))))
        # white flash after hook
        if hook_len <= ot < hook_len + 0.15:
            al = int(230 * (1 - (ot - hook_len) / 0.15))
            img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, al)))
        if kind == "end" and ot - MAIN_END < 0.12:
            al = int(200 * (1 - (ot - MAIN_END) / 0.12))
            img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, al)))
        if want is not None:
            if fi in want:
                img.convert("RGB").resize((540, 960)).save(f"{SP}/work/prev_{ot:05.2f}.jpg", quality=85)
            continue
        enc.stdin.write(img.convert("RGB").tobytes())
        if fi % 150 == 0:
            print(f"frame {fi}/{nframes}", flush=True)
    if enc:
        enc.stdin.close(); enc.wait()
    print("done", TOTAL)

if __name__ == "__main__":
    main()
