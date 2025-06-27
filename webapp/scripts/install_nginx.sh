#!/bin/bash

# brogit nginx setup script
# Author: r0b1ns

set -e

DEFAULT_CONF="/etc/nginx/sites-available/default"
BACKUP_CONF="${DEFAULT_CONF}.bak"

echo "Installing nginx..."
sudo apt update
sudo apt install -y nginx

# Enable snakeoil certs if not present
if [[ ! -f /etc/ssl/certs/ssl-cert-snakeoil.pem || ! -f /etc/ssl/private/ssl-cert-snakeoil.key ]]; then
  echo "Generating self-signed snakeoil certificates..."
  sudo apt install -y ssl-cert
fi

# Backup existing default config if needed
if [[ ! -f "$BACKUP_CONF" ]]; then
  echo "Backing up existing nginx default config..."
  sudo cp "$DEFAULT_CONF" "$BACKUP_CONF"
fi

# Write new default config
echo "Writing nginx default site config..."
sudo tee "$DEFAULT_CONF" > /dev/null << 'EOF'
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

echo "Testing and reloading nginx..."
sudo nginx -t
sudo systemctl reload nginx

echo "nginx setup complete. Service reachable at https://localhost/"
