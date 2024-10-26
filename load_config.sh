#!/bin/bash

# Path to config file
CONFIG_FILE="mediapi.conf"

# Declare associative Array
declare -A config

# Read config
if [[ -f "$CONFIG_FILE" ]]; then
    while IFS='=' read -r key value; do
        # Remove whitespace
        key=$(echo "$key" | xargs)
        value=$(echo "$value" | xargs)
        config["$key"]="$value"
    done < "$CONFIG_FILE"
else
    echo "Config file $CONFIG_FILE does not exist."
    exit 1
fi
