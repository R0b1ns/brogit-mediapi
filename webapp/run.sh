#!/bin/bash

# brogit (c) 2025
# Author: r0b1ns

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

"$SCRIPT_DIR/deploy.sh"

echo "Activate environment ..."
source "$SCRIPT_DIR/.venv/bin/activate"

python3 "$SCRIPT_DIR/app.py"