#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

PROJECT_RELATIVE_ROOT="../"
PROJECT_ROOT_PATH="$(cd "$SCRIPT_DIR/$PROJECT_RELATIVE_ROOT" && pwd)"

WEBAPP_ROOT_PATH="$SCRIPT_DIR"

# Install and deploy app
source "$WEBAPP_ROOT_PATH/deploy.sh"

source "$PROJECT_ROOT_PATH/load_config.sh"

WEBAPP_NAME="${config[project_name]}_webapp"
PROJECT_USER="${config[project_user]}"
APP_NAME="app"
HOST="${config[host]}"
PORT="${config[port]}"

echo "Run ..."
source "$WEBAPP_ROOT_PATH/.venv/bin/activate"
# python3 "$SCRIPT_DIR/app.py"
# Instead of direct execution we use gunicorn
gunicorn $APP_NAME:$APP_NAME -b $HOST:$PORT