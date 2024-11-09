#!/bin/bash

# brogit (c) 2024
# Author: r0b1ns

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

PROJECT_RELATIVE_ROOT="../"
PROJECT_ROOT_PATH="$(cd "$SCRIPT_DIR/$PROJECT_RELATIVE_ROOT" && pwd)"

MODULE_DIR="$SCRIPT_DIR"

AP_START_DELAY_AFTER_DISCONNECT="${AP_START_DELAY_AFTER_DISCONNECT:-10}"

source "$PROJECT_ROOT_PATH/helper.sh"
source "$PROJECT_ROOT_PATH/load_config.sh"

MODULE_NAME="${config[project_name]}_ap"
PROJECT_USER="${config[project_user]}"
WIFI_INTERFACE="${config[wifi_interface]}"

LOG_DIR="${config[log_dir]}/${config[project_name]}"
LOG_FILE=$(create_log_with_rotation "$LOG_DIR" "$MODULE_NAME")

# Log-Nachricht hinzufügen
log_message "$LOG_FILE" "Event :: Wifi dispatcher event (Controls '$WIFI_INTERFACE'): $1, $2"


if [[ "$1" == "$WIFI_INTERFACE" && "$2" == "up" ]]; then
  log_message "$LOG_FILE" "Event :: Cancel Delayed start (Wifi Up)"
  AP_START_DELAY_AFTER_DISCONNECT="$AP_START_DELAY_AFTER_DISCONNECT" bash "$MODULE_DIR/delayed_start.sh" cancel &
elif [[ "$1" == "$WIFI_INTERFACE" && "$2" == "down" ]]; then
  log_message "$LOG_FILE" "Event :: Start AP delayed in $AP_START_DELAY_AFTER_DISCONNECT minutes (Wifi Down)"
  AP_START_DELAY_AFTER_DISCONNECT="$AP_START_DELAY_AFTER_DISCONNECT" bash "$MODULE_DIR/delayed_start.sh" &
fi
