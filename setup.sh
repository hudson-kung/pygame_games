#!/bin/bash
# Install system dependencies
apt-get update
apt-get install -y python3-dev libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
   libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev zlib1g-dev

# First install pip dependencies except pygame
pip install --upgrade pip
pip install -r <(grep -v '^\s*pygame' requirements.txt)

# Install pygame with pre-built wheels
if python -c "import sys; exit(0) if sys.version_info < (3, 13) else exit(1)"; then
    # For Python < 3.13, install normally
    pip install pygame==2.5.2
else
    # For Python 3.13+, install with --only-binary
    pip install --only-binary=:all: pygame==2.5.2
fi
