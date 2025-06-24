#!/bin/bash

# brogit (c) 2025
# Author: r0b1ns

sudo apt update
sudo apt install gmediarender gstreamer1.0-alsa

# TODO: Here is configuration required. Please check that
# TODO: Take a look on old/install_pre.sh

systemctl enable gmediarender
systemctl start gmediarender