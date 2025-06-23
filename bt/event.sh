#!/bin/bash

# brogit (c) 2025
# Author: r0b1ns

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

source "$SCRIPT_DIR/config.env"

# Function universal_true
universal_true() {
    local val_lower=$(echo "$1" | tr '[:upper:]' '[:lower:]')  # Convert $1 to lower

    case "$val_lower" in
        1|true)
            echo "true"
            ;;
        *)
            echo "false"
            ;;
    esac
}

VOICE_ENABLED="$(universal_true "${VOICE_ENABLED:-true}")"
SOUND_ENABLED="$(universal_true "${SOUND_ENABLED:-true}")"

LOCALE="${LOCALE:-en-US}"
LANGUAGE="${LOCALE%%-*}"
echo "Load locale for LANGUAGE=$LANGUAGE"
source "$SCRIPT_DIR/locale/${LANGUAGE}.env"

CONNECT_TEXT="${CONNECT_TEXT:-Connected with: %s}"
ERROR_DEVICES_EMPTY="${ERROR_DEVICES_EMPTY:-Error: No devices connected}"

if [[ "$1" == "add" ]]; then
    if [ "$(universal_true "$SOUND_ENABLED")" == "true" ]; then
      aplay "$SCRIPT_DIR/audio/connect.wav"
    fi
    if [ "$(universal_true "$VOICE_ENABLED")" == "true" ]; then
      DEVICES=$(bluetoothctl devices Connected | grep "Device" | awk '{print $3, $4}' | paste -sd ',' - | sed 's/,/, /g')
      TEMP_FILE_NAME="temp$(date +%s).wav"
      if [[ -z "$DEVICES" ]]; then
          echo "Warning: No devices"
          OUTPUT_TEXT="$ERROR_DEVICES_EMPTY"
      else
          OUTPUT_TEXT=$(printf "$CONNECT_TEXT" "$DEVICES")
      fi
      pico2wave -w "$TEMP_FILE_NAME" -l "$LOCALE" "$OUTPUT_TEXT"
      aplay "$TEMP_FILE_NAME"
      rm "$TEMP_FILE_NAME"
    fi
elif [[ "$1" == "remove" ]]; then
    if [ "$(universal_true "$SOUND_ENABLED")" == "true" ]; then
      aplay "$SCRIPT_DIR/audio/disconnect.wav"
    fi
fi
