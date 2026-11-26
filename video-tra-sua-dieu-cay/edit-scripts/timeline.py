# Edit decision list for "Trà sữa điếu cày" video (all source times in seconds)
FPS = 30
W, H = 1080, 1920

# Hook teaser shown first (finished cup), then main segments
HOOK = (39.60, 41.20)
SEGMENTS = [
    (0.00, 4.98),
    (5.95, 11.70),
    (11.85, 24.70),
    (25.05, 27.55),
    (28.95, 31.40),
    (32.70, 34.25),
    (34.90, 39.55),
    (41.15, 42.60),
]
ENDCARD = 2.6

# Captions: (src_start, src_end, text, emoji or None). *word* = highlighted
CAPS = [
    (0.00, 0.58, "*NÈ NÈ!*", None),
    (0.60, 1.88, "bà nào xúi tui", "1f914"),
    (1.88, 2.78, "mua cái", None),
    (2.78, 3.98, "*TRÀ SỮA ĐIẾU CÀY* này", "1f9cb"),
    (3.98, 5.00, "nhập về bán", "1f62d"),
    (6.10, 7.70, "cái này khách tui đem lại", None),
    (7.70, 8.46, "mà bỏ đá vô thôi", None),
    (8.46, 9.06, "là *ĐỦ MỆT*", "1f62e-200d-1f4a8"),
    (9.08, 9.86, "hôm bữa chị tính nhập", None),
    (9.86, 10.98, "*1 THÙNG NGÀN CÁI* á", "1f4e6"),
    (11.00, 11.66, "*TRỜI ƠI*", "1f631"),
    (11.96, 13.22, "chị hỏi giá luôn rồi", None),
    (13.32, 14.08, "chết chưa chị ơi", "1f480"),
    (14.10, 14.56, "chị tìm được", None),
    (14.56, 15.66, "*GIÁ SỈ RẺ* lắm luôn á", "1f4b8"),
    (17.92, 18.30, "trời ơi", None),
    (18.32, 19.66, "bình thường làm nước", None),
    (19.66, 20.36, "mà khách dồn lên", None),
    (20.36, 21.20, "là làm *LÂU* rồi", "23f3"),
    (21.74, 22.90, "mà giờ bày thêm", None),
    (22.90, 23.82, "cái vụ *ĐIẾU CÀY* này nữa", None),
    (23.82, 24.70, "*CHẮC CHẾT*", "1f480"),
    (25.18, 26.20, "rồi sao nhét *ỐNG HÚT* ta?", "1f914"),
    (26.20, 27.50, "sao nhét *ỐNG HÚT* ta??", "2753"),
    (29.14, 30.10, "*ĐƯỢC ĐƯỢC ĐƯỢC*", "2728"),
    (30.52, 31.36, "cũng được đi", "1f605"),
    (32.86, 34.20, "biểu hiện của *SỰ CỐ CHẤP*", "1f624"),
    (35.04, 36.22, "ê nhưng mà mọi người thích", None),
    (36.22, 37.40, "thì có *NÊN NHẬP* không ta?", "1f914"),
    (38.24, 38.90, "*NÊN NHẬP KHÔNG?*", None),
    (38.96, 39.55, "ủa chú ơi", "1f972"),
    (41.26, 42.60, "rồi... cháu *KHÔNG NGHE*", "1f649"),
]

# Punch-in zooms: (src_start, src_end, zoom)
ZOOMS = [
    (0.00, 0.58, 1.18),
    (2.78, 3.98, 1.10),
    (8.46, 9.06, 1.15),
    (9.86, 10.98, 1.10),
    (11.00, 11.66, 1.22),
    (14.56, 15.66, 1.10),
    (20.36, 21.20, 1.12),
    (23.82, 24.70, 1.25),
    (25.18, 27.50, 1.12),
    (29.14, 30.10, 1.10),
    (32.86, 34.20, 1.18),
    (38.24, 38.90, 1.15),
    (41.26, 42.60, 1.10),
]
# Camera shakes: (src_time, duration, amplitude px)
SHAKES = [
    (11.00, 0.55, 26),
    (23.82, 0.70, 32),
    (29.14, 0.40, 14),
    (38.24, 0.40, 18),
]
# Extra floating stickers: (src_start, src_end, emoji, x, y, size)
STICKERS = [
    (2.78, 4.98, "1f9cb", 820, 330, 230),
    (9.86, 11.00, "1f4e6", 140, 380, 200),
    (11.00, 11.66, "1f631", 800, 360, 260),
    (14.56, 15.66, "1f4b8", 160, 360, 210),
    (14.80, 15.66, "1f4b8", 840, 470, 170),
    (23.82, 24.70, "1f480", 760, 330, 280),
    (29.14, 30.10, "2728", 150, 420, 200),
    (32.86, 34.20, "1f624", 820, 360, 230),
    (41.26, 42.60, "1f923", 820, 360, 240),
]
# Side tags: (src_start, src_end, text)
TAGS = [
    (6.10, 9.06, "POV: chỉ mới bỏ đá thôi"),
    (17.92, 21.20, "khách ngoài kia: đợi dài cổ"),
    (25.18, 27.50, "*thử thách nhét ống hút*"),
    (35.04, 39.55, "comment cho tui biết đi"),
]
# Red flash on "chắc chết"
FLASHES = [(23.82, 0.25)]
# Sound effects: (src_time, kind) ; kind in pop, whoosh, ding, boom, scratch, tick
SFX = [
    (0.02, "pop"), (2.78, "ding"), (3.98, "pop"), (8.46, "whoosh"),
    (9.86, "pop"), (11.00, "boom"), (13.32, "tick"), (14.56, "ding"),
    (20.36, "tick"), (23.82, "boom"), (25.18, "whoosh"), (26.20, "pop"),
    (29.14, "ding"), (30.52, "pop"), (32.86, "scratch"), (36.22, "pop"),
    (38.24, "whoosh"), (41.26, "scratch"),
]
