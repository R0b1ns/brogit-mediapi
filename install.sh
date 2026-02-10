#!/bin/bash

# brogit (c) 2024
# Author: r0b1ns

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

chown -R :www-data "$SCRIPT_DIR"

### NOTE: ###
# Its deprecated now to install everything modular. So therefore we commented that out.
# You can still install all modules via the webapp. This is the way it should go!
###

# modules
# TODO: Change permissions in module
# chmod g+r "$SCRIPT_DIR/modules/gmrender-resurrect/config.env"
# chmod g+r "$SCRIPT_DIR/modules/shairport-sync/config.env"

# bt
# chown -R :www-data "$SCRIPT_DIR/bt"
# chmod +x "$SCRIPT_DIR/bt/install.sh"
# bash "$SCRIPT_DIR/bt/install.sh"

# ap
# chown -R :www-data "$SCRIPT_DIR/ap"
# chmod +x "$SCRIPT_DIR/ap/install.sh"
# bash "$SCRIPT_DIR/ap/install.sh"

# webapp
chown -R :www-data "$SCRIPT_DIR/webapp"
chmod +x "$SCRIPT_DIR/webapp/install.sh"
bash "$SCRIPT_DIR/webapp/install.sh"

# Prompt for nginx setup
chmod +x "$SCRIPT_DIR/modules/nginx/install.sh"

read -r -p "Install nginx and overwrite default vHost? [Y/n] " REPLY
REPLY=${REPLY,,} # to lowercase

if [[ -z "$REPLY" || "$REPLY" == "y" || "$REPLY" == "yes" ]]; then
    "$SCRIPT_DIR/modules/nginx/install.sh"
else
    echo "Skipping nginx setup."
fi
