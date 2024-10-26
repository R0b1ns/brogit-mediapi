#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ ! -d ".venv" ]; then
    echo "Create virtual environment..."
    python3 -m venv "$SCRIPT_DIR/.venv"
fi

source ./.venv/bin/activate

echo "Install dependencies ..."
pip3 install -r "$SCRIPT_DIR/requirements.txt"

echo "Run ..."
source "$SCRIPT_DIR/.venv/bin/activate"
python3 "$SCRIPT_DIR/app.py"