#!/bin/bash

# brogit nginx setup script (idempotent)
# Author: r0b1ns

set -e

DEFAULT_CONF="/etc/nginx/sites-available/default"
BACKUP_CONF="${DEFAULT_CONF}.bak"
CERT="/etc/ssl/certs/ssl-cert-snakeoil.pem"
KEY="/etc/ssl/private/ssl-cert-snakeoil.key"

install_package_if_missing() {
  if ! dpkg -s "$1" >/dev/null 2>&1; then
    echo "Installing $1..."
    sudo apt-get install -y "$1"
  fi
}

echo "Updating package index..."
sudo apt-get update -y

# Install nginx and ssl-cert if missing
install_package_if_missing nginx
install_package_if_missing ssl-cert

# Backup default config once
if [[ -f "$DEFAULT_CONF" && ! -f "$BACKUP_CONF" ]]; then
  echo "Creating backup of existing nginx default config..."
  sudo cp "$DEFAULT_CONF" "$BACKUP_CONF"
fi

# Desired config content
read -r -d '' NEW_CONF <<'EOF'
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl default_server;
    listen [::]:443 ssl default_server;

    ssl_certificate     /etc/ssl/certs/ssl-cert-snakeoil.pem;
    ssl_certificate_key /etc/ssl/private/ssl-cert-snakeoil.key;

    location / {
        proxy_pass https://127.0.0.1:8443;
        proxy_ssl_verify off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
    }
}
EOF

# Only write config if changed
CURRENT_HASH=$(sudo sha256sum "$DEFAULT_CONF" 2>/dev/null | awk '{print $1}' || true)
NEW_HASH=$(echo "$NEW_CONF" | sha256sum | awk '{print $1}')

if [[ "$CURRENT_HASH" != "$NEW_HASH" ]]; then
  echo "Updating nginx default config..."
  echo "$NEW_CONF" | sudo tee "$DEFAULT_CONF" > /dev/null
  sudo nginx -t && sudo systemctl reload nginx
else
  echo "nginx default config is up to date. No changes made."
fi

echo "nginx setup complete. Service reachable at https://localhost/"
