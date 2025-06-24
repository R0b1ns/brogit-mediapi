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
DEVICE_NAME="${DEVICE_NAME:-}"

# Set DEVICE_NAME_STR only if DEVICE_NAME is not empty
if [[ -n "$DEVICE_NAME" ]]; then
  DEVICE_NAME_STR="Name = $DEVICE_NAME"
else
  DEVICE_NAME_STR=""
fi

# Bluetooth adapter configuration
MAIN_CONF="/etc/bluetooth/main.conf"
BACKUP_CONF="/etc/bluetooth/main.conf.bak"
TEMP_CONF="$(mktemp)"

if [[ ! -f "$BACKUP_CONF" ]]; then
  sudo cp "$MAIN_CONF" "$BACKUP_CONF"
  echo "Created Backup of $MAIN_CONF"
fi

# Neue Konfiguration in TEMP_CONF schreiben
cat << EOF > "$TEMP_CONF"
[General]
Class = $DEVICE_CLASS
DiscoverableTimeout = 0
PairableTimeout = 0
$DEVICE_NAME_STR

[Policy]
AutoEnable=true
EOF

# Compare and replace if different, then restart
if ! cmp -s "$TEMP_CONF" "$MAIN_CONF"; then
  echo "Bluetooth config changed: updating and restarting bluetooth"
  sudo cp "$TEMP_CONF" "$MAIN_CONF"
  sudo rm /var/lib/bluetooth/*/settings
  sudo systemctl restart bluetooth
else
  echo "Bluetooth config unchanged: skipping restart"
fi

rm "$TEMP_CONF"


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
active_services=$(systemctl list-units --type=service --all --output=json 'bt-agent@*.service' | jq -r '.[].unit')

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