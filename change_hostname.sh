#!/bin/bash

mac_address=$(ip link show | awk '/ether/ {print $2; exit}' | sed 's/://g' | tail -c 6)
new_hostname="bMediaPi-$mac_address"

sudo hostnamectl set-hostname "$new_hostname"

sudo sed -i.bak "s/127.0.1.1.*/127.0.1.1 $new_hostname/g" /etc/hosts