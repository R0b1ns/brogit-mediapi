#!/bin/bash

# brogit (c) 2025
# Author: r0b1ns

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Install system dependencies and create .venv
echo "Install system dependencies ..."
"$SCRIPT_DIR/scripts/generic_apt_install.sh" "$SCRIPT_DIR/apt-requirements.txt"

VENV_DIR="$SCRIPT_DIR/.venv"

if [ -d "$VENV_DIR" ]; then
    echo "Existing virtual environment found — removing it..."
    rm -rf "$VENV_DIR"
fi

echo "Create virtual environment..."
python3 -m venv "$VENV_DIR"

# Deploy
"$SCRIPT_DIR/deploy.sh"

# Grant rights
chown -R www-data:www-data "$SCRIPT_DIR"

# Install service
"$SCRIPT_DIR/scripts/install_service.sh"

# Prompt for nginx setup
read -r -p "Install nginx and overwrite default vHost? [Y/n] " REPLY
REPLY=${REPLY,,} # to lowercase

if [[ -z "$REPLY" || "$REPLY" == "y" || "$REPLY" == "yes" ]]; then
    "$SCRIPT_DIR/scripts/install_nginx.sh"
else
    echo "Skipping nginx setup."
fi
