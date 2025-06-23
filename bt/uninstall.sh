#!/bin/bash

# brogit (c) 2025
# Author: r0b1ns

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

source "$SCRIPT_DIR/config.env"

AUDIO_DEVICE="${AUDIO_DEVICE:-hci0}"

sudo rm /etc/systemd/system/bt-agent@.service
sudo rm /etc/udev/rules.d/99-bluetooth-connect.rules

sudo systemctl disable bt-agent@${AUDIO_DEVICE}.service
sudo systemctl disable bluealsa
sudo systemctl disable bluetooth
sudo systemctl daemon-reload

cp /etc/bluetooth/main.conf.bak /etc/bluetooth/main.conf
