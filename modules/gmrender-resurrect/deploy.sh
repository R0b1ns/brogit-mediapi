#!/bin/bash

# dlna-renderer-setup (c) 2025
# Author: r0b1ns

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.env"

# Default values
DEVICE_NAME="${DEVICE_NAME:-DLNA-Renderer}"
INITIAL_VOLUME_DB="${INITIAL_VOLUME_DB:--10}"
UPNP_UUID="$(ip link show | awk '/ether/ {print \\\"salt:)-\\\" \$2}' | head -1 | md5sum | awk '{print \$1}')"

SERVICE_PATH="/etc/systemd/system/gmediarender.service"
BACKUP_PATH="${SERVICE_PATH}.bak"
TEMP_PATH="$(mktemp)"

# Backup existing service
if [[ ! -f "$BACKUP_PATH" ]]; then
  sudo cp "$SERVICE_PATH" "$BACKUP_PATH" 2>/dev/null || true
  echo "Backup created: $BACKUP_PATH"
fi

# Generate service file
cat << EOF > "$TEMP_PATH"
[Unit]
Description=gmrender-resurrect service
After=network.target sound.target

[Service]
Environment="UPNP_DEVICE_NAME=${DEVICE_NAME}"
ExecStartPre=/bin/sh -c "/bin/systemctl set-environment UPNP_UUID=$UPNP_UUID"

ExecStart=/usr/local/bin/gmediarender -f "$DEVICE_NAME" -u "$UPNP_UUID" \\
  --gstout-audiosink=alsasink --gstout-audiodevice=sysdefault \\
  --logfile=/var/log/gmediarenderer.log --gstout-initial-volume-db=${INITIAL_VOLUME_DB}
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Apply service file if changed
if ! cmp -s "$TEMP_PATH" "$SERVICE_PATH"; then
  echo "Updating gmediarender.service"
  sudo cp "$TEMP_PATH" "$SERVICE_PATH"
  sudo systemctl daemon-reload
  sudo systemctl enable gmediarender.service
  sudo systemctl restart gmediarender.service
else
  echo "gmediarender service unchanged"
fi

rm "$TEMP_PATH"
