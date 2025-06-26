#!/bin/bash

# brogit (c) 2025
# Author: r0b1ns

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Deploy and install dependencies
"$SCRIPT_DIR/deploy.sh"

# Grant rights
chown -R www-data:www-data "$SCRIPT_DIR"

# Install service
"$SCRIPT_DIR/scripts/install_service.sh"