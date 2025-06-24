#!/bin/bash
set -e

# brogit (c) 2025
# Author: r0b1ns

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd "$SCRIPT_DIR/respositories"

# NQPTP
cd nqptp
git pull
autoreconf -fi
./configure --with-systemd-startup
make
make install

cd "$SCRIPT_DIR/respositories"

# ALAC
cd alac
git pull
autoreconf -fi
./configure
make
make install

cd "$SCRIPT_DIR/respositories"

# Shairport-sync
cd shairport-sync
git pull
autoreconf -fi
./configure --sysconfdir=/etc --with-libdaemon --with-piddir=/opt/shairport-sync/ --with-soxr --with-apple-alac --with-metadata --with-mqtt-client --with-dbus-interface --with-alsa --with-ssl=openssl --with-systemd --with-avahi --with-airplay-2
make
make install

systemctl restart nqptp
systemctl restart alac
systemctl restart shairport-sync