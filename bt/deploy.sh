#!/bin/bash

# brogit (c) 2025
# Author: r0b1ns

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

source "$SCRIPT_DIR/config.env"

# Define default variables
LOCALE="${LOCALE:-en-US}"
DEVICE_CLASS="${DEVICE_CLASS:-0x200414}"
DISCOVERABLE="${DISCOVERABLE:-on}"
AUDIO_DEVICE="${AUDIO_DEVICE:-hci0}"

# Bluetooth adapter configuration
if [[ ! -f /etc/bluetooth/main.conf.bak ]]; then
  cp /etc/bluetooth/main.conf /etc/bluetooth/main.conf.bak
  echo "Created Backup of /etc/bluetooth/main.conf"
fi
cat << EOF | sudo tee /etc/bluetooth/main.conf > /dev/null
[General]
Class = $DEVICE_CLASS
DiscoverableTimeout = 0
PairableTimeout = 0

[Policy]
AutoEnable=true
EOF

# Bluetooth Agent Service
cat << EOF | sudo tee /etc/systemd/system/bt-agent@.service > /dev/null
[Unit]
Description=Bluetooth Agent
Requires=bluetooth.service
After=bluetooth.service

[Service]
ExecStartPre=/usr/bin/bluetoothctl discoverable $DISCOVERABLE
ExecStartPre=/bin/hciconfig %I piscan
ExecStartPre=/bin/hciconfig %I sspmode 1
ExecStart=/usr/bin/bt-agent --capability=NoInputNoOutput
RestartSec=5
Restart=always
KillSignal=SIGUSR1

[Install]
WantedBy=multi-user.target
EOF

# Enable and Start services
sudo systemctl daemon-reload

# Disable all other bt-agent service instances except the current AUDIO_DEVICE
active_services=$(systemctl list-units --type=service --no-legend 'bt-agent@*.service' | awk '{print $1}')

for svc in $active_services; do
  if [[ "$svc" != "bt-agent@${AUDIO_DEVICE}.service" ]]; then
    echo "Disabling and stopping $svc"
    sudo systemctl disable "$svc"
    sudo systemctl stop "$svc"
  fi
done

# Autostart Agent for audio device agent
sudo systemctl enable bt-agent@${AUDIO_DEVICE}.service
sudo systemctl start bt-agent@${AUDIO_DEVICE}.service