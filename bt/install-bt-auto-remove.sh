#!/bin/bash
set -e

# Get the absolute directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Source files relative to the script directory
SCRIPT_SRC="$SCRIPT_DIR/bt-auto-remove.sh"
SERVICE_SRC="$SCRIPT_DIR/bt-auto-remove.service"
LOGROTATE_SRC="$SCRIPT_DIR/bt-auto-remove.logrotate"

# Destination paths
SCRIPT_DST="/usr/local/bin/bt-auto-remove.sh"
SERVICE_DST="/etc/systemd/system/bt-auto-remove.service"
LOGROTATE_DST="/etc/logrotate.d/bt-auto-remove"

echo "Copying bt-auto-remove.sh to $SCRIPT_DST"
sudo cp "$SCRIPT_SRC" "$SCRIPT_DST"
sudo chmod +x "$SCRIPT_DST"

echo "Copying systemd service to $SERVICE_DST"
sudo cp "$SERVICE_SRC" "$SERVICE_DST"
sudo chmod 644 "$SERVICE_DST"

echo "Copying logrotate config to $LOGROTATE_DST"
sudo cp "$LOGROTATE_SRC" "$LOGROTATE_DST"
sudo chmod 644 "$LOGROTATE_DST"

echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

echo "Enabling and starting bt-auto-remove service..."
sudo systemctl enable bt-auto-remove.service
sudo systemctl restart bt-auto-remove.service

echo "Installation finished successfully."
