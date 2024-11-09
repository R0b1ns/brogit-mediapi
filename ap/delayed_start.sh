#!/bin/bash

# brogit (c) 2024
# Author: r0b1ns

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

PROJECT_RELATIVE_ROOT="../"
PROJECT_ROOT_PATH="$(cd "$SCRIPT_DIR/$PROJECT_RELATIVE_ROOT" && pwd)"

MODULE_DIR="$SCRIPT_DIR"

source "$PROJECT_ROOT_PATH/helper.sh"
source "$PROJECT_ROOT_PATH/load_config.sh"

MODULE_NAME="${config[project_name]}_ap"
PROJECT_USER="${config[project_user]}"
WIFI_INTERFACE="${config[wifi_interface]}"

LOG_DIR="${config[log_dir]}/${config[project_name]}"
LOG_FILE=$(create_log_with_rotation "$LOG_DIR" "$MODULE_NAME")

log_message "$LOG_FILE" "Delayed start :: Welcome"

PID_FILE="$MODULE_DIR/ap_delayed_start.pid"
CANCEL_FLAG_FILE="$MODULE_DIR/ap_cancel_start.flag"

AP_START_DELAY_AFTER_DISCONNECT="${AP_START_DELAY_AFTER_DISCONNECT:-10}"
DELAY_SECONDS=$((AP_START_DELAY_AFTER_DISCONNECT * 60))

if iwgetid -r "$WIFI_INTERFACE" > /dev/null 2>&1; then
    log_message "$LOG_FILE" "Delayed start :: Info: $WIFI_INTERFACE already connected. Exit"
    exit 0
fi

if [[ "$1" == "cancel" ]]; then
  log_message "$LOG_FILE" "Delayed start :: Cancel"
  if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null; then
      echo "Delayed start runs"
      log_message "$LOG_FILE" "Delayed start :: Active process exists"
      touch "$CANCEL_FLAG_FILE"
      log_message "$LOG_FILE" "Delayed start :: Created Cancel flag"
      exit 0
    else
      log_message "$LOG_FILE" "Delayed start :: Warning: PID File exists but no process running. PID file will be removed. Exit"
      rm "$PID_FILE"
      exit 1
    fi
  else
    log_message "$LOG_FILE" "Delayed start :: Warning: No delayed start running. Exit"
    exit 0
  fi
fi

if [ -f "$PID_FILE" ]; then
  # Lockfile already exists
  PID=$(cat "$PID_FILE")
  if ps -p "$PID" > /dev/null; then
    log_message "$LOG_FILE" "Delayed start :: Skript is already running PID=$PID. Exit"
    exit 1
  else
    log_message "$LOG_FILE" "Delayed start :: Warning: PID File exists but no process running. PID file will be removed."
    rm "$PID_FILE"
  fi
fi

# Save PID to File
echo $$ > "$PID_FILE"
log_message "$LOG_FILE" "Delayed start :: Skript is already running PID=$PID. Exit"

# Remove PID File when skript is canceled
trap ctrl_c INT
ctrl_c () {
  echo -n;
  rm "$PID_FILE"
  exit 0
}

if [ -f "$CANCEL_FLAG_FILE" ]; then
  log_message "$LOG_FILE" "Delayed start :: Stop file exists before even tried.. Must be a leftover. Lets remove it.."
  rm $CANCEL_FLAG_FILE
fi

log_message "$LOG_FILE" "Delayed start :: Start delayed in $DELAY_SECONDS seconds..."

# Delayed start. If stop file appears, we exit
for ((i=0; i<600; i++)); do
  if [ -f "$CANCEL_FLAG_FILE" ]; then
    log_message "$LOG_FILE" "Delayed start :: Info: Delayed start is stopped!"
    log_message "$LOG_FILE" "Delayed start :: Warning: Remove stop flag and pid file"
    rm "$CANCEL_FLAG_FILE"
    rm "$PID_FILE"
    exit 0
  fi
  sleep 1
done

log_message "$LOG_FILE" "Delayed start :: Start Access Point ..."
bash "$MODULE_DIR/start.sh"