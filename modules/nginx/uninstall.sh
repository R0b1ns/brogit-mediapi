#!/bin/bash

# brogit uninstall (c) 2025
# Author: r0b1ns

set -e

DEFAULT_CONF="/etc/nginx/sites-available/default"
BACKUP_CONF="${DEFAULT_CONF}.bak"

echo "Reverting nginx default config..."

if [[ -f "$BACKUP_CONF" ]]; then
  sudo cp "$BACKUP_CONF" "$DEFAULT_CONF"
  echo "Default nginx config restored from backup."
else
  echo "No backup config found at '$BACKUP_CONF'. Nothing to restore."
fi

echo "Stopping nginx service..."
sudo systemctl stop nginx

echo "Disabling nginx autostart..."
sudo systemctl disable nginx

echo "Uninstalling nginx..."
sudo apt-get remove --purge -y nginx nginx-common
sudo apt-get autoremove -y

echo "nginx successfully uninstalled."
