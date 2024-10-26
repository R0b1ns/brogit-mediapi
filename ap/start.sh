#!/bin/bash

# brogit (c) 2024
# Author: r0b1ns

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

PROJECT_RELATIVE_ROOT="../"
PROJECT_ROOT_PATH="$(cd "$SCRIPT_DIR/$PROJECT_RELATIVE_ROOT" && pwd)"

source "$PROJECT_ROOT_PATH/load_config.sh"

WIFI_INTERFACE="${config[wifi_interface]}"
AP_CON_NAME="${config[ap_con_name]}"
AP_HOST="${config[ap_host]}"
WEBAPP_PORT="${config[port]}"
AP_SSID="${config[ap_ssid]}"
AP_SSID_USE_HOSTNAME="${config[ap_ssid_use_hostname]}"

if [ "$(universal_true "$AP_SSID_USE_HOSTNAME")" == "true" ]; then
  # Overwrite SSID
  AP_SSID="$(hostname)"
fi

# Prevent cancel skript to not end up in a non working state
trap ctrl_c INT
ctrl_c () {
  echo -n;
}

echo "Info: Enable captive portal. Redirect all traffic to: $AP_Host"
sudo bash -c 'echo "address=/#/'$AP_HOST'" > /etc/NetworkManager/dnsmasq-shared.d/redirect.conf'

# We want to start cleaned, so we remove leftovers if they exist
nmcli con delete "AccessPoint" > /dev/null 2>&1

echo "Info: Create Access Point=$AP_CON_NAME with SSID=$AP_SSID"
nmcli con add type wifi mode ap con-name "$AP_CON_NAME" ssid "$AP_SSID" ipv4.method shared ipv4.address $AP_HOST/24 autoconnect no

# Clear firewall
sudo iptables -F
sudo iptables -t nat -F

# If WEBAPP_PORT is not running on port 80, redirect the traffic
if [ $WEBAPP_PORT -ne 80 ]
then
	echo "Info: Redirect all inbound traffic on port 80 to webapp $AP_HOST:$WEBAPP_PORT"
	sudo iptables -t nat -I PREROUTING -p tcp --dport 80 -j DNAT --to-destination $AP_HOST:$WEBAPP_PORT
fi

echo "Info: Enable AccessPoint"
nmcli con up "AccessPoint"