# AI MASTER – bộ công cụ edit video

| Phần | Công cụ | Việc |
|---|---|---|
| Dựng chữ, hiệu ưng | Node.js + Remotion (`remotion/`) | Tạo video từ code React |
| Nghe giọng, phụ đề | Python + faster-whisper (`scripts/transcribe.py`) | Audio → `.srt` (+ `.json` timestamp từng từ) |
| Cắt ghép, xuất | FFmpeg | Cắt, nối, ghép âm thanh, gắn phụ đề |

## Cài đặt
```bash
./setup.sh
```
Lần đầu chạy whisper sẽ tải model từ Hugging Face (cần mạng tới huggingface.co).

## Dùng nhanh
```bash
# 1. Dựng chữ bằng Remotion
cd remotion && npx remotion render src/index.ts TitleDemo out/title.mp4   # xem trực tiếp: npm run studio

# 2. Tạo phụ đề (tiếng Việt nên dùng model medium hoặc large-v3)
.venv/bin/python scripts/transcribe.py video.mp4 -l vi -m medium --json

# 3. FFmpeg: cắt / ghép âm thanh / gắn phụ đề
ffmpeg -ss 00:00:05 -to 00:00:20 -i video.mp4 -c copy clip.mp4
ffmpeg -i title.mp4 -i voice.wav -c:v copy -c:a aac -shortest merged.mp4
ffmpeg -i merged.mp4 -vf subtitles=video.srt -c:a copy final.mp4
```
