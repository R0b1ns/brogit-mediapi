#!/bin/bash

# brogit (c) 2024
# Author: r0b1ns

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Delayed start AP"

PID_FILE="$SCRIPT_DIR/ap_delayed_start.pid"
CANCEL_FLAG_FILE="$SCRIPT_DIR/ap_cancel_start.flag"

AP_START_DELAY_AFTER_DISCONNECT="${AP_START_DELAY_AFTER_DISCONNECT:-10}"
DELAY_SECONDS=$((AP_START_DELAY_AFTER_DISCONNECT * 60))

if iwgetid -r "$WIFI_INTERFACE" > /dev/null 2>&1; then
    echo "Info: $WIFI_INTERFACE already connected. Exit"
    exit 0
fi

if [[ "$1" == "cancel" ]]; then
  if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null; then
      echo "Delayed start runs"
      touch "$CANCEL_FLAG_FILE"
      echo "Info: Created Cancel flag"
      exit 0
    else
      echo "Warning: PID File exists but no process running. PID file will be removed. Exit"
      rm "$PID_FILE"
      exit 1
    fi
  else
    echo "Warning: No delayed start running. Exit"
    exit 0
  fi
fi

if [ -f "$PID_FILE" ]; then
  # Lockfile already exists
  PID=$(cat "$PID_FILE")
  if ps -p "$PID" > /dev/null; then
    echo "Skript is already running PID=$PID. Exit"
    exit 1
  else
    echo "Warning: PID File exists but no process running. PID file will be removed."
    rm "$PID_FILE"
  fi
fi

# Save PID to File
echo $$ > "$PID_FILE"

# Remove PID File when skript is canceled
trap ctrl_c INT
ctrl_c () {
  echo -n;
  rm "$PID_FILE"
  exit 0
}

if [ -f "$CANCEL_FLAG_FILE" ]; then
  echo "Stop file exists before even tried.. Must be a leftover. Lets remove it.."
  rm $CANCEL_FLAG_FILE
fi

echo "Start delayed in $DELAY_SECONDS seconds..."

# Delayed start. If stop file appears, we exit
for ((i=0; i<600; i++)); do
  if [ -f "$CANCEL_FLAG_FILE" ]; then
    echo "Info: Delayed start is stopped!"
    echo "Warning: Remove stop flag and pid file"
    rm "$CANCEL_FLAG_FILE"
    rm "$PID_FILE"
    exit 0
  fi
  sleep 1
done

echo "Start Access Point ..."
bash "$SCRIPT_DIR/start.sh"