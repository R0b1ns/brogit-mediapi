#!/bin/bash

# brogit (c) 2024
# Author: r0b1ns

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

PROJECT_RELATIVE_ROOT="../"
PROJECT_ROOT_PATH="$(cd "$SCRIPT_DIR/$PROJECT_RELATIVE_ROOT" && pwd)"

source "$PROJECT_ROOT_PATH/helper.sh"
source "$PROJECT_ROOT_PATH/load_config.sh"

MODULE_NAME="${config[project_name]}_ap"
PROJECT_USER="${config[project_user]}"
WIFI_INTERFACE="${config[wifi_interface]}"

LOG_DIR="${config[log_dir]}/${config[project_name]}"
LOG_FILE=$(create_log_with_rotation "$LOG_DIR" "$MODULE_NAME")

AP_CON_NAME="${config[ap_con_name]}"

log_message "$LOG_FILE" "Stop :: Info: Disable Access Point=$AP_CON_NAME"
nmcli con down "$AP_CON_NAME"

sudo iptables -t nat -F

log_message "$LOG_FILE" "Stop :: Info: Remove captive portal redirection"
sudo rm -f /etc/NetworkManager/dnsmasq-shared.d/redirect.conf

log_message "$LOG_FILE" "Stop :: Info: Delete Access Point=$AP_CON_NAME"
nmcli con delete "$AP_CON_NAME"