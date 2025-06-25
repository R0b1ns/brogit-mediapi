#!/bin/bash

# bt-auto-remove.sh
# Automatically remove failed Bluetooth pairings on auth errors
# Logs to systemd journal and /var/log/bt-auto-remove.log

LOG_TAG="bt-auto-remove"
LOG_FILE="/var/log/bt-auto-remove.log"

log() {
    logger --tag "$LOG_TAG" "$1"
    echo "$(date '+%Y-%m-%d %H:%M:%S') $1" >> "$LOG_FILE"
}

# Ensure log file exists with correct permissions
touch "$LOG_FILE"
chmod 644 "$LOG_FILE"

# Check for bluetoothctl
if ! command -v bluetoothctl >/dev/null; then
    log "bluetoothctl not found. Exiting."
    exit 1
fi

log "Started Bluetooth auth failure watcher."

btmon | while read -r line; do
    if echo "$line" | grep -qE 'status.*(0x05|0x0e)'; then
        MAC=$(echo "$line" | grep -oE '([0-9A-F]{2}:){5}[0-9A-F]{2}')
        if [ -n "$MAC" ]; then
            log "Detected pairing/auth failure for $MAC. Removing..."
            echo -e "remove $MAC\nquit" | bluetoothctl >/dev/null 2>&1
            log "Removed $MAC via bluetoothctl."
        fi
    fi
done
