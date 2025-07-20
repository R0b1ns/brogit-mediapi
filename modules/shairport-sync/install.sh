#!/bin/bash

# brogit (c) 2025
# Author: r0b1ns

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

UPDATE_FILE_PATH="$SCRIPT_DIR/update.sh"

sudo apt update

# Shairport sync https://github.com/mikebrady/shairport-sync/blob/master/BUILD.md
sudo apt install --no-install-recommends build-essential git autoconf automake libtool \
    libpopt-dev libconfig-dev libasound2-dev avahi-daemon libavahi-client-dev libssl-dev libsoxr-dev \
    libplist-dev libsodium-dev libavutil-dev libavcodec-dev libavformat-dev uuid-dev libgcrypt-dev xxd \
    libdaemon-dev libglib2.0-dev libmosquitto-dev libtool -yy

cd $SCRIPT_DIR

# Create and enter repositories directory
mkdir -p repositories && cd repositories

# NQPTP and ALAC is required for Airplay2
git clone https://github.com/mikebrady/nqptp
git clone https://github.com/mikebrady/alac.git

git clone https://github.com/mikebrady/shairport-sync.git

# Execute Update
chmod +x "$UPDATE_FILE_PATH"
"$UPDATE_FILE_PATH"

## Adjust config
SHAIRPORT_SYNC_CONFIG_FILE="/etc/shairport-sync.conf"
ALLOW_LINE='    allow_session_interruption = "yes";'

# Prüfen, ob bereits eine nicht-kommentierte allow_session_interruption-Zeile existiert
if ! grep -q '^[[:space:]]*allow_session_interruption[[:space:]]*=' "$SHAIRPORT_SYNC_CONFIG_FILE"; then
  # Innerhalb des sessioncontrol-Blocks einfügen, vor der schließenden };
  sed -i "/^[[:space:]]*sessioncontrol[[:space:]]*=/,/^[[:space:]]*};/ {
    /^[[:space:]]*};/ i\\
$ALLOW_LINE
  }" "$SHAIRPORT_SYNC_CONFIG_FILE"
fi

# Restart
systemctl restart nqptp
systemctl restart shairport-sync

# TODO: Move that to ap (wifi) ctl
# WiFi Power Management off (Instant but not after reboot)
# iwconfig wlan0 power off

# NetworkManager (For future connection, also after reboot) (2=disabled, 3=enabled)
# TODO: This command creates an error, cause nmcli is maybe not installed
# sudo nmcli connection modify preconfigured wifi.powersave 2