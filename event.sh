#!/bin/bash

source "load_config.sh"

if [[ "$1" == "bt" ]]; then
  echo "Bluetooth Event"
  LOCALE="${config[host]}" CONNECT_TEXT="${translations[bt_connect_text]}" bash ./bt/event.sh "${@:2}"
elif [[ "$1" == "wifi" ]]; then
  echo "Wifi Event"
else
  echo "Unknown Event"
fi