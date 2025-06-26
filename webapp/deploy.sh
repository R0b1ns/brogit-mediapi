#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Install system dependencies ..."
"$SCRIPT_DIR/scripts/generic_apt_install.sh" "$SCRIPT_DIR/apt-requirements.txt"

if [ ! -d ".venv" ]; then
    echo "Create virtual environment..."
    python3 -m venv "$SCRIPT_DIR/.venv"
fi

source "$SCRIPT_DIR/.venv/bin/activate"

echo "Install pip dependencies ..."
pip3 install -r "$SCRIPT_DIR/requirements.txt"