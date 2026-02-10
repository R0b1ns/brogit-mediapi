#!/bin/bash

# brogit (c) 2025
# Author: r0b1ns

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

DEPLOY_FILE_PATH="$SCRIPT_DIR/deploy.sh"
UNINSTALL_FILE_PATH="$SCRIPT_DIR/uninstall.sh"

install_package_if_missing() {
  if ! dpkg -s "$1" >/dev/null 2>&1; then
    echo "Installing $1..."
    sudo apt-get install -y "$1"
  else
    echo "Skip installing. $1 already exists"
  fi
}

echo "Updating package index..."
sudo apt-get update -y

# Install nginx and ssl-cert if missing
install_package_if_missing nginx
install_package_if_missing ssl-cert

chmod +x "$DEPLOY_FILE_PATH"
chmod +x "$UNINSTALL_FILE_PATH"
chmod g+r "$SCRIPT_DIR/config.env"
"$DEPLOY_FILE_PATH"

if grep -q '^INSTALLED=' "$CONFIG_FILE"; then
  sed -i "s/^INSTALLED=.*/INSTALLED='True'/" "$CONFIG_FILE"
else
  echo "INSTALLED='True'" >> "$CONFIG_FILE"
fi