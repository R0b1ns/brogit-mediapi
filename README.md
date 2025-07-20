# brogit-mediapi
Wireless Audio Receiver (DLNA, Airplay, Bluetooth), SteamPlay, Auto USB-Networkshare - Functionality bundle

# Access Point

## Captive portal Mode
- Unverschlüsseltes Netzwerk
- Captive portal
- Eingabe des PIN's

- Wenn Gerät hochfährt und keine Verbindung zu eth0 und keine WLAN verbindung hat, wird der AP gestartet
- Wenn das Gerät die WLAN Verbindung verliert und keine eth0 Verbindung besteht, wird ebenfalls der AP gestartet.

## AP Mode
- Wenn ein AP in der Webapp konfiguriert wurde, startet dieser wenn das Gerät hoch fährt.

# Webapp

Default password is: 112358


# Service Info
Add Service info on webapp
sudo service --status-all

# Getting started

## Prerequisites

For Orange Pi (Armbian) following package is also required:
(Missing arm-linux-gnueabihf-gcc)

```
sudo apt install -y gcc-arm-linux* g++-arm-linux*
sudo apt install python3-dev
sudo apt install build-essential libffi-dev
```

## Install

Clone and install this project

```
cd /opt/
git clone https://github.com/R0b1ns/brogit-mediapi
cd brogit-mediapi
git checkout <branch>
./install.sh
```

# Errors

## 2. Self Signed Certificate does not work like expected

Long loading times. Deactivated for now

## 4. Verify_user is not secure.

Develop auth_server via socket

## Feature: Generic script for a task queue.

So tasks can not be triggert twice at the same time

## Bug: Efficiency: Enable WiFi Power Management

Move commented script in shairport-sync/install.sh to AP install

# Debug and Logging

```
journalctl -u brogit-cast-webapp.service  -f
```