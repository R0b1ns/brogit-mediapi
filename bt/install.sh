#!/bin/bash
set -e

# brogit (c) 2025
# Author: r0b1ns

# Install required packages
sudo apt install -y --no-install-recommends bluetooth bluez bluez-tools bluez-alsa-utils libttspico-utils jq

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

BT_SOUND_FILE_PATH="$SCRIPT_DIR/event.sh"
BT_DEPLOY_FILE_PATH="$SCRIPT_DIR/deploy.sh"
BT_AUTO_REMOVE_FILE_PATH="$SCRIPT_DIR/install-bt-auto-remove.sh"


# Make scripts executable
chmod +x "$BT_SOUND_FILE_PATH"
chmod +x "$BT_DEPLOY_FILE_PATH"

# Create UDEV rule
echo "Create UDEV rule ..."
cat << EOF | sudo tee /etc/udev/rules.d/99-bluetooth-connect.rules > /dev/null
ACTION=="add", SUBSYSTEM=="bluetooth", RUN+="$BT_SOUND_FILE_PATH add"
ACTION=="remove", SUBSYSTEM=="bluetooth", RUN+="$BT_SOUND_FILE_PATH remove"
EOF

echo "Reload rules ..."
sudo udevadm control --reload-rules
sudo udevadm trigger

# Execute deploy
echo "Deploy ..."
"$BT_DEPLOY_FILE_PATH"

# Enable and start services
echo "Enable auto-boot and start service ..."
sudo systemctl enable bluetooth
sudo systemctl start bluetooth

sudo systemctl enable bluealsa
sudo systemctl start bluealsa

# Execute autoremove service
"$BT_AUTO_REMOVE_FILE_PATH"