#!/bin/bash

# brogit (c) 2025
# Author: r0b1ns

# Install dependencies
sudo apt update -qq

# Install Method: APT (default)
sudo apt install gmediarender gstreamer1.0-alsa -yy

# If you want to build from project instead of apt:
#sudo apt install gmediarender gstreamer1.0-alsa \
#             libupnp-dev libgstreamer1.0-dev \
#             gstreamer1.0-plugins-base gstreamer1.0-plugins-good \
#             gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly \
#             gstreamer1.0-libav \
#             build-essential autoconf automake libtool pkg-config -yy

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

DEPLOY_FILE_PATH="$SCRIPT_DIR/deploy.sh"
UNINSTALL_FILE_PATH="$SCRIPT_DIR/uninstall.sh"

cd $SCRIPT_DIR

# Create and enter repositories directory
mkdir -p repositories && cd repositories

git clone https://github.com/hzeller/gmrender-resurrect.git

chmod +x "$DEPLOY_FILE_PATH"
chmod +x "$UNINSTALL_FILE_PATH"

"$DEPLOY_FILE_PATH"