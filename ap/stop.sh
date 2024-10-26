#!/bin/bash

# brogit (c) 2024
# Author: r0b1ns

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

source "$SCRIPT_DIR/load_config.sh"

AP_CON_NAME="${config[ap_con_name]}"

echo "Info: Disable Access Point=$AP_CON_NAME"
nmcli con down "$AP_CON_NAME"

sudo iptables -t nat -F

echo "Info: Remove captive portal redirection"
sudo rm -f /etc/NetworkManager/dnsmasq-shared.d/redirect.conf

echo "Info: Delete Access Point=$AP_CON_NAME"
nmcli con delete "$AP_CON_NAME"