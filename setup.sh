#!/bin/bash
# Install system dependencies required for Pygame
apt-get update
apt-get install -y python3-dev libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
   libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev zlib1g-dev

# Install Python dependencies
pip install -r requirements.txt
