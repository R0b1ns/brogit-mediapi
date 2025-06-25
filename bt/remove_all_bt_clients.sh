#!/bin/bash

# Get list of paired Bluetooth devices
devices=$(bluetoothctl devices | awk '{print $2}')

if [ -z "$devices" ]; then
  echo "No devices found."
  exit 0
fi

echo "Removing all paired devices..."

for dev in $devices; do
  echo "Removing device $dev"
  bluetoothctl remove "$dev"
done

echo "All devices have been removed."
