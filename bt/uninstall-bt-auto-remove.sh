#!/bin/bash
set -e

SCRIPT_DST="/usr/local/bin/bt-auto-remove.sh"
SERVICE_DST="/etc/systemd/system/bt-auto-remove.service"
LOGROTATE_DST="/etc/logrotate.d/bt-auto-remove"

echo "Stopping bt-auto-remove service..."
sudo systemctl stop bt-auto-remove.service || true

echo "Disabling bt-auto-remove service..."
sudo systemctl disable bt-auto-remove.service || true

echo "Removing service file: $SERVICE_DST"
sudo rm -f "$SERVICE_DST"

echo "Removing script: $SCRIPT_DST"
sudo rm -f "$SCRIPT_DST"

echo "Removing logrotate config: $LOGROTATE_DST"
sudo rm -f "$LOGROTATE_DST"

echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

echo "Uninstallation finished successfully."
