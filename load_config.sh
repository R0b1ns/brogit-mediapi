#!/bin/bash

# Path to config file
CONFIG_FILE="mediapi.conf"

# Read config
load_config() {
    # Declare associative Array
    declare -A config
    if [[ -f "$CONFIG_FILE" ]]; then
        while IFS='=' read -r key value; do
            # Remove whitespace
            key=$(echo "$key" | xargs)
            value=$(echo "$value" | xargs)

            # Only add valid kv
            if [[ -n "$key" && -n "$value" ]]; then
                config["$key"]="$value"
            fi
        done < "$CONFIG_FILE"
    else
        echo "Config file $CONFIG_FILE does not exist."
        exit 1
    fi
}

load_translations() {
    local lang_file="$1"
    declare -gA translations

    while IFS='=' read -r key value; do
        translations["$key"]="$value"
    done < "$lang_file"
}

load_config

# TODO: Dynamic load by locale
load_translations "locale/strings_de.conf"

echo "Host: ${config[host]}"
echo "Port: ${config[port]}"
echo "Willkommen: ${translations[bt_connect_text]}"