#!/bin/bash

# brogit (c) 2024
# Author: r0b1ns

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

bash "$SCRIPT_DIR/ap/install.sh"
bash "$SCRIPT_DIR/bt/install.sh"
# bash "$SCRIPT_DIR/webapp.sh"