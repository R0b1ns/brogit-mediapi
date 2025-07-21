#!/bin/bash

# brogit nginx setup script (idempotent)
# Author: r0b1ns

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

source "$SCRIPT_DIR/../.env"

# Determine scheme based on NGINX_PROXY_PASS_SSL
if [[ "$NGINX_PROXY_PASS_SSL" == "true" || "$NGINX_PROXY_PASS_SSL" == "True" ]]; then
  SCHEME="https"
else
  SCHEME="http"
fi

NGINX_PROXY_PASS_PORT="${NGINX_PROXY_PASS_PORT:-8443}"
PROXY_PASS_URL="${PROXY_PASS_URL:-$SCHEME://127.0.0.1:$NGINX_PROXY_PASS_PORT}"

DEFAULT_CONF="/etc/nginx/sites-available/default"
BACKUP_CONF="${DEFAULT_CONF}.bak"
NGINX_CERT="/etc/ssl/certs/ssl-cert-snakeoil.pem"
NGINX_KEY="/etc/ssl/private/ssl-cert-snakeoil.key"

install_package_if_missing() {
  if ! dpkg -s "$1" >/dev/null 2>&1; then
    echo "Installing $1..."
    sudo apt-get install -y "$1"
  else
    echo "Skip installing. $1 already exists"
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
else
  echo "Backup of original 'default' config file already exists!"
fi

if [[ "$SCHEME" == "https" ]]; then
  PROXY_SSL_VERIFY="proxy_ssl_verify off;"
else
  PROXY_SSL_VERIFY=""
fi

# Build new config with dynamic proxy_pass
NEW_CONF=$(cat <<EOF
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    return 301 https://\$host\$request_uri;
}

server {
    listen 443 ssl default_server;
    listen [::]:443 ssl default_server;

    ssl_certificate     $NGINX_CERT;
    ssl_certificate_key $NGINX_KEY;

    location / {
        proxy_pass $PROXY_PASS_URL;
        $PROXY_SSL_VERIFY
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;

        proxy_connect_timeout 60s;
        proxy_send_timeout    60s;
        proxy_read_timeout    60s;
        send_timeout          60s;

        # Only when big json data is consumed  e.g. yield
        # proxy_buffering off;
    }
}
EOF
)

echo "$NEW_CONF"

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

echo "nginx setup complete. Service reachable at $SCHEME://localhost:$NGINX_PROXY_PASS_PORT/"
