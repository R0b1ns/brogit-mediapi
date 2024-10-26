#!/bin/bash

# brogit (c) 2024
# Author: r0b1ns

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

LOCALE="${LOCALE:-en-US}"
CONNECT_TEXT="${CONNECT_TEXT:-Connected with: %s}"
ERROR_DEVICES_EMPTY="${ERROR_DEVICES_EMPTY:-Error: No devices connected}"

if [[ "$1" == "add" ]]; then
    aplay $DIR/connect.wav
    DEVICES=$(bluetoothctl devices Connected | grep "Device" | awk '{print $3, $4}' | paste -sd ',' - | sed 's/,/, /g')
    TEMP_FILE_NAME="temp$(date +%s).wav"
    if [[ -z "$DEVICES" ]]; then
        echo "Warning: No devices"
        OUTPUT_TEXT="$ERROR_DEVICES_EMPTY"
    else
        OUTPUT_TEXT=$(printf "$CONNECT_TEXT" "$DEVICES")
    fi

    pico2wave -w $TEMP_FILE_NAME -l "$LOCALE" "$OUTPUT_TEXT"
    aplay $TEMP_FILE_NAME
    rm $TEMP_FILE_NAME
elif [[ "\$1" == "remove" ]]; then
    aplay $DIR/disconnect.wav
fi