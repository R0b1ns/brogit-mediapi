#!/bin/bash

source "load_config.sh"

echo "Host: ${config[host]}"

if [[ "$1" == "bt" ]]; then
  echo "Bluetooth Event"
  LOCALE="test" bash ./bt/event.sh
elif [[ "$1" == "wifi" ]]; then
  echo "Wifi Event"
else
  echo "Unknown Event"
fi