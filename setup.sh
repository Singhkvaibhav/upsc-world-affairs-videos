#!/usr/bin/env bash
# One-time setup for the video pipeline.
set -e
cd "$(dirname "$0")"
pip install --break-system-packages -q -r requirements.txt
command -v ffmpeg >/dev/null || (apt-get update -qq && apt-get install -y -qq ffmpeg)
fc-list | grep -qi "Inter" || echo "Note: Inter font not found; install fonts-inter or text will fall back to a default font."
mkdir -p voice
if [ ! -f voice/en-us-lessac-medium.onnx ]; then
  curl -sSL -o voice/v.tgz https://github.com/rhasspy/piper/releases/download/v0.0.2/voice-en-us-lessac-medium.tar.gz
  tar xzf voice/v.tgz -C voice && rm voice/v.tgz
fi
python3 -c "import cairo, piper, numpy; print('setup ok')"
echo "Voice model: $(pwd)/voice/en-us-lessac-medium.onnx"
