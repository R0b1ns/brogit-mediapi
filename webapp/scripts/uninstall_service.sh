#!/bin/bash

# brogit (c) 2025
# Author: r0b1ns

set -e

SERVICE_NAME="brogit-cast-webapp"
SERVICE_PATH="/etc/systemd/system/${SERVICE_NAME}.service"

if systemctl is-enabled --quiet "$SERVICE_NAME"; then
  echo "Disabling $SERVICE_NAME..."
  sudo systemctl disable "$SERVICE_NAME"
fi

if systemctl is-active --quiet "$SERVICE_NAME"; then
  echo "Stopping $SERVICE_NAME..."
  sudo systemctl stop "$SERVICE_NAME"
fi

if [[ -f "$SERVICE_PATH" ]]; then
  echo "Removing service file..."
  sudo rm "$SERVICE_PATH"
else
  echo "Service file not found, skipping removal."
fi

echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

echo "Uninstall completed."
