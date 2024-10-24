#!/bin/bash

AUDIO_DEVICE="hci0"

sudo rm /etc/systemd/system/bt-agent@.service
sudo rm /etc/udev/rules.d/99-bluetooth-connect.rules

sudo systemctl disable bt-agent@${AUDIO_DEVICE}.service
sudo systemctl disable bluealsa
sudo systemctl disable bluetooth
sudo systemctl daemon-reload

cp /etc/bluetooth/main.conf.bak /etc/bluetooth/main.conf
