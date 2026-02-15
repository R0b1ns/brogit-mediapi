#!/bin/bash

# brogit (c) 2026
# Author: r0b1ns

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

CONFIG_FILE="${1:-"$SCRIPT_DIR/config.env"}"

if [[ ! -f "$CONFIG_FILE" ]]; then
  echo "Config file not found: $CONFIG_FILE" >&2
  exit 1
fi

source "$CONFIG_FILE"

# Configuration
DEVICE_NAME="${DEVICE_NAME:-""}"
SHAIRPORT_SYNC_CONFIG_FILE=="${SHAIRPORT_SYNC_CONFIG_FILE:-"/etc/shairport-sync.conf"}"

# Function to update or add a config line in a specific group
update_config_line() {
    local file="$1"
    local group="$2"
    local key="$3"
    local value="$4"

    # Prepare timestamp comment
    local timestamp
    timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    local modified_line="    $key = \"$value\";  # Added/Modified by script at $timestamp"

    local changed=0

    # Check if group exists
    if ! grep -q "^[[:space:]]*$group[[:space:]]*=" "$file"; then
        # Add the group at the end of the file
        echo -e "\n$group = {\n$modified_line\n};" >> "$file"
        changed=1
    else
        # Extract the group block
        local group_block
        group_block=$(sed -n "/^[[:space:]]*$group[[:space:]]*=/,/^[[:space:]]*};/p" "$file")

        # Check if the key exists in the group
        if echo "$group_block" | grep -q "^[[:space:]]*$key[[:space:]]*="; then
            # Check if the value is already correct
            if ! echo "$group_block" | grep -q "^[[:space:]]*$key[[:space:]]*=[[:space:]]*\"$value\""; then
                # Replace existing line with modified line (keep comment)
                sed -i "/^[[:space:]]*$group[[:space:]]*=/,/^[[:space:]]*};/ s|^[[:space:]]*$key[[:space:]]*=.*|$modified_line|" "$file"
                changed=1
            fi
        else
            # Insert new line before closing };
            sed -i "/^[[:space:]]*$group[[:space:]]*=/,/^[[:space:]]*};/ {
                /^[[:space:]]*};/ i\\
$modified_line
            }" "$file"
            changed=1
        fi
    fi

    return $changed
}

# Decide the value for 'name'
if [ -z "$DEVICE_NAME" ]; then
    NAME_VALUE="%H"
else
    NAME_VALUE="$DEVICE_NAME"
fi

# Call the function
update_config_line "$SHAIRPORT_SYNC_CONFIG_FILE" "general" "name" "$NAME_VALUE"
exit_code=$?

if [ $exit_code -eq 1 ]; then
    echo "Configuration updated."
else
    echo "No changes needed."
fi

exit $exit_code
