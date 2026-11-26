"""Chỉnh ảnh hàng loạt: cân bằng trắng, đồng bộ độ sáng, tăng tương phản, màu và độ nét.

Cách dùng:  python3 chinh_anh.py anh-goc anh-da-chinh
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

TARGET_MEDIAN = 0.47   # độ sáng trung bình mong muốn (0..1) - "sáng vừa phải"
MIN_GAMMA = 0.50       # giới hạn kéo sáng cho ảnh quá tối, tránh bệt và nhiễu
WB_STRENGTH = 0.6     # mức khử ám vàng/cam (0 = giữ nguyên, 1 = trung tính hoàn toàn)
WARMTH = 1.015         # giữ lại chút ấm cho da người tự nhiên
CONTRAST = 0.35        # độ tương phản (S-curve)
SATURATION = 1.15      # độ tươi màu
VIBRANCE = 0.15        # tăng thêm cho vùng màu nhạt


def luma(a):
    return 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]


def to_lin(a):
    return np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)


def to_srgb(a):
    a = np.clip(a, 0, 1)
    return np.where(a <= 0.0031308, a * 12.92, 1.055 * a ** (1 / 2.4) - 0.055)


def white_balance(a):
    lin = to_lin(a)
    y = luma(a)
    mask = (y > 0.15) & (y < 0.85)
    sat = lin.max(2) - lin.min(2)
    mask &= sat < np.percentile(sat[mask], 70)   # bỏ qua vùng màu rực, chỉ lấy vùng gần trung tính
    means = lin[mask].mean(0)
    gains = means[1] / means
    gains = gains ** WB_STRENGTH
    gains[0] *= WARMTH
    gains[2] /= WARMTH
    return to_srgb(lin * gains)


def levels(a):
    y = luma(a)
    lo = np.percentile(y, 0.4)
    hi = np.percentile(y, 99.8)
    lo = min(lo, 0.06)
    hi = max(hi, 0.85)
    return np.clip((a - lo) / (hi - lo), 0, 1)


def brighten(a):
    y = luma(a)
    med = np.clip(np.median(y), 1e-3, 0.99)
    g = np.log(TARGET_MEDIAN) / np.log(med)
    g = float(np.clip(g, MIN_GAMMA, 1.0))
    y2 = np.clip(y, 1e-4, 1) ** g
    scale = (y2 / np.clip(y, 1e-4, 1))[..., None]
    out = a * scale
    # nén vùng vượt sáng thay vì cắt cháy
    m = out.max(2, keepdims=True)
    over = m > 1
    out = np.where(over, out / np.maximum(m, 1e-6) * (1 - np.exp(-m)) / (1 - np.exp(-1)) , out)
    return np.clip(out, 0, 1), g


def s_curve(a):
    s = 1 / (1 + np.exp(-(a - 0.5) * 6))
    s0, s1 = 1 / (1 + np.exp(3)), 1 / (1 + np.exp(-3))
    s = (s - s0) / (s1 - s0)
    return a * (1 - CONTRAST) + s * CONTRAST


def colour(a, g=1.0):
    y = luma(a)[..., None]
    sat = (a.max(2, keepdims=True) - a.min(2, keepdims=True))
    k = SATURATION + VIBRANCE * (1 - np.clip(sat * 2.5, 0, 1))
    k = 1 + (k - 1) * np.clip((g - 0.45) / 0.4, 0.3, 1)   # ảnh tối kéo sáng nhiều thì tăng màu ít lại
    return np.clip(y + (a - y) * k, 0, 1)


def finish(img, g):
    # giảm nhiễu màu (nhất là ảnh tối được kéo sáng nhiều), rồi làm nét kênh sáng
    ycc = img.convert("YCbCr")
    Y, Cb, Cr = ycc.split()
    r = 2 if g > 0.7 else 3
    Cb = Cb.filter(ImageFilter.GaussianBlur(r))
    Cr = Cr.filter(ImageFilter.GaussianBlur(r))
    if g < 0.7:
        Y = Y.filter(ImageFilter.GaussianBlur(0.6))
    Y = Y.filter(ImageFilter.UnsharpMask(radius=1.2, percent=90, threshold=2))
    Y = Y.filter(ImageFilter.UnsharpMask(radius=4, percent=35, threshold=3))   # tăng độ "trong", rõ khối
    return Image.merge("YCbCr", (Y, Cb, Cr)).convert("RGB")


def process(path, out_path):
    im = Image.open(path)
    exif = im.info.get("exif")
    a = np.asarray(im.convert("RGB")).astype(np.float64) / 255
    a = white_balance(a)
    a = levels(a)
    a, g = brighten(a)
    a = s_curve(a)
    a = colour(a, g)
    out = Image.fromarray((a * 255 + 0.5).astype(np.uint8))
    out = finish(out, g)
    kw = {"quality": 95, "subsampling": 0}
    if exif:
        kw["exif"] = exif
    out.save(out_path, **kw)
    return g


if __name__ == "__main__":
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    dst.mkdir(parents=True, exist_ok=True)
    for p in sorted(src.glob("*.jp*g")):
        g = process(p, dst / p.name)
        print(f"{p.name}: gamma {g:.2f}")
