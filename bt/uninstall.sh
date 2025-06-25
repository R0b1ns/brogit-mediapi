#!/bin/bash

# brogit (c) 2025
# Author: r0b1ns

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

source "$SCRIPT_DIR/config.env"

BLUETOOTH_DEVICE="${BLUETOOTH_DEVICE:-hci0}"

sudo systemctl disable bt-agent@${BLUETOOTH_DEVICE}.service
sudo systemctl stop bt-agent@${BLUETOOTH_DEVICE}.service

sudo rm /etc/systemd/system/bt-agent@.service

sudo systemctl daemon-reload

cp /etc/bluetooth/main.conf.bak /etc/bluetooth/main.conf
sudo rm /etc/udev/rules.d/99-bluetooth-connect.rules

"$SCRIPT_DIR/uninstall-bt-auto-remove.sh"

sudo systemctl disable bluealsa
sudo systemctl disable bluetooth

sudo systemctl restart bluealsa
sudo systemctl restart bluetooth
