#!/bin/bash

# brogit (c) 2025
# Author: r0b1ns

systemctl disable shairport-sync
systemctl stop shairport-sync

BIN_PATH="$(which shairport-sync 2>/dev/null)"

if [ -z "$BIN_PATH" ]; then
  echo "shairport-sync not found."
  exit 0
fi

echo "Found at: $BIN_PATH"

# Remove binary
sudo rm -f "$BIN_PATH"

echo "Removed."

# WiFi Power Management on (Instant but not after reboot)
# iwconfig wlan0 power on

# NetworkManager (For future connection, also after reboot) (2=disabled, 3=enabled)
# sudo nmcli connection modify preconfigured wifi.powersave 3