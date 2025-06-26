#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

source "$SCRIPT_DIR/.venv/bin/activate"

echo "Install pip dependencies ..."
"$SCRIPT_DIR/.venv/bin/pip" install --no-cache-dir -r "$SCRIPT_DIR/requirements.txt"
