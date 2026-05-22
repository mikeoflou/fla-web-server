#!/usr/bin/env bash
set -euo pipefail

APP_DIR="/var/www/web_server"
SERVICE_NAME="web_server"
SUDO=""

if [[ ! -d "$APP_DIR" ]]; then
  echo "Error: $APP_DIR does not exist"
  exit 1
fi

if [[ "$(id -u)" -ne 0 ]]; then
  if ! sudo -n true 2>/dev/null; then
    echo "Error: deployment needs sudo access. Re-run as root or allow this user to use sudo." >&2
    exit 1
  fi
  SUDO="sudo"
fi

cd "$APP_DIR"

echo "Deploying from $APP_DIR ..."

SERVICE_USER="$($SUDO systemctl show -p User --value "$SERVICE_NAME" 2>/dev/null || true)"
SERVICE_GROUP="$($SUDO systemctl show -p Group --value "$SERVICE_NAME" 2>/dev/null || true)"

if [[ -z "$SERVICE_USER" ]]; then
  SERVICE_USER="ubuntu"
fi

if [[ -z "$SERVICE_GROUP" ]]; then
  SERVICE_GROUP="www-data"
fi

# Ensure the live app can write JSON content and uploaded images after deploys.
$SUDO chown -R "$SERVICE_USER:$SERVICE_GROUP" "$APP_DIR"
$SUDO find "$APP_DIR" -type d -exec chmod 755 {} +
$SUDO find "$APP_DIR" -type f -name "*.json" -exec chmod 664 {} +

if [[ -d "$APP_DIR/static/images" ]]; then
  $SUDO find "$APP_DIR/static/images" -type d -exec chmod 775 {} +
  $SUDO find "$APP_DIR/static/images" -type f -exec chmod 664 {} +
fi

if [[ -f "$APP_DIR/deploy/vps/deploy_update.sh" ]]; then
  $SUDO chmod 755 "$APP_DIR/deploy/vps/deploy_update.sh"
fi

if [[ ! -d ".venv" ]]; then
  echo "Creating virtual environment ..."
  python3 -m venv .venv
fi

source .venv/bin/activate
echo "Installing Python dependencies ..."
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn

echo "Restarting $SERVICE_NAME ..."
$SUDO systemctl daemon-reload
$SUDO systemctl restart "$SERVICE_NAME"
$SUDO systemctl status "$SERVICE_NAME" --no-pager

echo "Reloading nginx ..."
$SUDO nginx -t
$SUDO systemctl reload nginx

echo "Deploy update completed."
