#!/usr/bin/env bash
# Cài bộ AI MASTER: Remotion (Node) + faster-whisper (Python) + FFmpeg
set -e
cd "$(dirname "$0")"
command -v ffmpeg >/dev/null || { sudo apt-get update && sudo apt-get install -y ffmpeg; }
[ -d .venv ] || python3 -m venv .venv
.venv/bin/pip install -q -r requirements.txt
(cd remotion && npm install)
echo "== Kiểm tra =="; node -v; ffmpeg -version | head -1
.venv/bin/python -c "import faster_whisper; print('faster-whisper', faster_whisper.__version__)"
