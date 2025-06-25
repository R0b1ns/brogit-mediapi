#!/bin/bash

# brogit (c) 2025
# Author: r0b1ns

# Install dependencies
sudo apt update -qq
sudo apt install --no-install-recommends gmediarender gstreamer1.0-alsa -yy

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

"$SCRIPT_DIR/deploy.sh"