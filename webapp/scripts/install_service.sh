#!/bin/bash

# brogit (c) 2025
# Author: r0b1ns

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

SERVICE_NAME="brogitCast WebApp Service"
SERVICE_PATH="/etc/systemd/system/brogit-cast-webapp.service"
SERVICE_UNIT_NAME=$(basename "$SERVICE_PATH" .service)

echo "$SERVICE_UNIT_NAME"
BACKUP_PATH="${SERVICE_PATH}.bak"
TEMP_PATH="$(mktemp)"
trap 'rm -f "$TEMP_PATH"' EXIT

# Backup existing service
#if [[ ! -f "$BACKUP_PATH" ]]; then
#  sudo cp "$SERVICE_PATH" "$BACKUP_PATH" 2>/dev/null || true
#  echo "Backup created: $BACKUP_PATH"
#fi

# Generate service file
cat << EOF > "$TEMP_PATH"
[Unit]
Description=$SERVICE_NAME
After=network.target sound.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=$PROJECT_ROOT
Environment="PYTHONUNBUFFERED=1"
ExecStartPre=$PROJECT_ROOT/deploy.sh

ExecStart=$PROJECT_ROOT/.venv/bin/python $PROJECT_ROOT/app.py
Restart=always
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Apply service file if changed
if ! cmp -s "$TEMP_PATH" "$SERVICE_PATH"; then
  echo "Updating $SERVICE_UNIT_NAME"
  sudo cp "$TEMP_PATH" "$SERVICE_PATH"
  sudo systemctl daemon-reload
  sudo systemctl enable "$SERVICE_UNIT_NAME"
  sudo systemctl restart "$SERVICE_UNIT_NAME"
else
  echo "$SERVICE_UNIT_NAME unchanged"
fi

rm "$TEMP_PATH"