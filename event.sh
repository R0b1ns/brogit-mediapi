#!/bin/bash

source "load_config.sh"

mkdir -p "${config[log_dir]}"
LOG_FILE="${config[log_dir]}/event.log"

echo "$@" >> LOG_FILE

if [[ "$1" == "bt" ]]; then
  echo "Bluetooth Event"
  LOCALE="${config[locale]}" CONNECT_TEXT="${translations[bt_connect_text]}" ERROR_DEVICES_EMPTY="${translations[error_devices_empty]}" bash ./bt/event.sh "${@:2}"
elif [[ "$1" == "wifi" ]]; then
  echo "Wifi Event"
  bash ./ap/event.sh "${@:2}"
else
  echo "Unknown Event"
fi