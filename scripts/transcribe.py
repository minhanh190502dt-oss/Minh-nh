#!/usr/bin/env python3
"""Nghe giọng và tạo phụ đề .srt bằng faster-whisper.
Dùng: .venv/bin/python scripts/transcribe.py input.mp4 [-o out.srt] [-m small] [-l vi]
"""
import argparse, json
from faster_whisper import WhisperModel

def ts(t):
    h, r = divmod(t, 3600); m, s = divmod(r, 60)
    return f"{int(h):02}:{int(m):02}:{int(s):02},{int((s % 1) * 1000):03}"

p = argparse.ArgumentParser()
p.add_argument("input"); p.add_argument("-o", "--output")
p.add_argument("-m", "--model", default="small")
p.add_argument("-l", "--language", default=None, help="vi, en,... (bỏ trống = tự nhận)")
p.add_argument("--json", action="store_true", help="xuất thêm timestamp từng từ (cho Remotion)")
a = p.parse_args()
out = a.output or a.input.rsplit(".", 1)[0] + ".srt"

model = WhisperModel(a.model, device="auto", compute_type="int8")
segs, info = model.transcribe(a.input, language=a.language, vad_filter=True, word_timestamps=a.json)
print(f"Ngôn ngữ: {info.language} ({info.language_probability:.2f})")
segs = list(segs)
with open(out, "w", encoding="utf-8") as f:
    for i, s in enumerate(segs, 1):
        f.write(f"{i}\n{ts(s.start)} --> {ts(s.end)}\n{s.text.strip()}\n\n")
if a.json:
    words = [{"text": w.word, "start": w.start, "end": w.end} for s in segs for w in (s.words or [])]
    json.dump(words, open(out.rsplit(".", 1)[0] + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"Đã ghi {out} ({len(segs)} đoạn)")
