#!/bin/bash

echo "Install system dependencies ..."
sudo apt install -y python3-pip python3-venv wireless-tools

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ ! -d ".venv" ]; then
    echo "Create virtual environment..."
    python3 -m venv "$SCRIPT_DIR/.venv"
fi

source "$SCRIPT_DIR/.venv/bin/activate"

echo "Install project dependencies ..."
pip3 install -r "$SCRIPT_DIR/requirements.txt"