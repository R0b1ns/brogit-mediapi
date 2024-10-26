#!/bin/bash

# brogit (c) 2024
# Author: r0b1ns

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

LOCALE="${LOCALE:-en-US}"
CONNECT_TEXT="${CONNECT_TEXT:-Connected with: %s}"

echo $LOCALE
echo $CONNECT_TEXT

if [[ "$1" == "add" ]]; then
    aplay $DIR/connect.wav
    DEVICES=$(bluetoothctl devices Connected | grep "Device" | awk '{print $3, $4}' | paste -sd ',' - | sed 's/,/, /g')
    TEMP_FILE_NAME="temp$(date +%s).wav"
    OUTPUT_TEXT=$(printf "$CONNECT_TEXT" "$DEVICES")
    pico2wave -w $TEMP_FILE_NAME -l "$LOCALE" "$OUTPUT_TEXT"
    aplay $TEMP_FILE_NAME
    rm $TEMP_FILE_NAME
elif [[ "\$1" == "remove" ]]; then
    aplay $DIR/disconnect.wav
fi