#!/bin/bash
# Script to allow www-data to run the auto_apt_update.sh script with sudo without password

SUDOERS_FILE="/etc/sudoers.d/www-data-system_update"

echo "www-data ALL=(ALL) NOPASSWD: /usr/local/bin/auto_apt_update.sh" | sudo tee $SUDOERS_FILE
sudo chmod 440 $SUDOERS_FILE
