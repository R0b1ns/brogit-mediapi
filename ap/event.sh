#!/bin/bash

# brogit (c) 2024
# Author: r0b1ns

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

AP_START_DELAY_AFTER_DISCONNECT="${AP_START_DELAY_AFTER_DISCONNECT:-10}"

if [[ "$1" == "$WIFI_INTERFACE" && "$2" == "up" ]]; then
  echo "Up"
  AP_START_DELAY_AFTER_DISCONNECT="$AP_START_DELAY_AFTER_DISCONNECT" bash "$SCRIPT_DIR/delayed_start.sh cancel"
elif [[ "$1" == "$WIFI_INTERFACE" && "$2" == "down" ]]; then
  echo "Down"
  AP_START_DELAY_AFTER_DISCONNECT="$AP_START_DELAY_AFTER_DISCONNECT" bash "$SCRIPT_DIR/delayed_start.sh"
fi
