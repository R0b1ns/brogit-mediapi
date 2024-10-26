#!/bin/bash

source "load_config.sh"

echo "${config[locale]}"
echo "${translations[bt_connect_text]}"

if [[ "$1" == "bt" ]]; then
  echo "Bluetooth Event"
  LOCALE="${config[locale]}" CONNECT_TEXT="${translations[bt_connect_text]}" CONFIG=$config bash ./bt/event.sh "${@:2}"
elif [[ "$1" == "wifi" ]]; then
  echo "Wifi Event"
else
  echo "Unknown Event"
fi