#!/bin/bash

# Path to config file
CONFIG_FILE="mediapi.conf"

# Read config
load_config() {
    # Declare global associative Array
    declare -gA config
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
        echo "Error: Config file $CONFIG_FILE does not exist."
        exit 1
    fi
}

load_translations() {
    local lang_file="$1"
    declare -gA translations

    if [[ -f "$lang_file" ]]; then
        while IFS='=' read -r key value; do
            if [[ -n "$key" && -n "$value" ]]; then
              translations["$key"]="$value"
            fi
        done < "$lang_file"
    else
        echo "Warning: Locale not found"
    fi
}

load_config

# TODO: Dynamic load by locale
load_translations "locale/strings_de.conf"

echo "Host: ${config[host]}"
echo "Port: ${config[port]}"
echo "Willkommen: ${translations[bt_connect_text]}"