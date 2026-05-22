# Bluehost VPS Migration Steps

## 1) Build deploy package on Windows

From project root:

```powershell
powershell -ExecutionPolicy Bypass -File .\deploy\vps\package_for_vps.ps1
```

This creates `web_server_vps_YYYYMMDD_HHMMSS.zip` and excludes local virtualenv/system folders.

## 2) Upload and extract on VPS

```bash
mkdir -p /var/www/web_server
cd /var/www/web_server
unzip /path/to/web_server_vps_YYYYMMDD_HHMMSS.zip
```

## 3) Install runtime dependencies

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip nginx
cd /var/www/web_server
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn
```

## 4) Configure systemd service

1. Edit `deploy/vps/web_server.service` placeholders:
   - `YOUR_LINUX_USER`
   - `REPLACE_WITH_LONG_RANDOM_SECRET`
2. Install service:

```bash
sudo cp /var/www/web_server/deploy/vps/web_server.service /etc/systemd/system/web_server.service
sudo systemctl daemon-reload
sudo systemctl enable web_server
sudo systemctl restart web_server
sudo systemctl status web_server --no-pager
```

## 5) Configure Nginx

1. Edit `deploy/vps/nginx_web_server.conf` placeholders:
   - `YOUR_DOMAIN`
2. Install config:

```bash
sudo cp /var/www/web_server/deploy/vps/nginx_web_server.conf /etc/nginx/sites-available/web_server
sudo ln -sf /etc/nginx/sites-available/web_server /etc/nginx/sites-enabled/web_server
sudo nginx -t
sudo systemctl reload nginx
```

## 6) Point DNS to VPS IP

Set your domain A records to `129.121.84.30`.

## 7) Enable HTTPS

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d YOUR_DOMAIN -d www.YOUR_DOMAIN
```

## 8) Future app updates

### Recommended: one-command publish from Windows

From `C:\desktop\web_Server`, run:

```powershell
powershell -ExecutionPolicy Bypass -File .\deploy\vps\publish_to_vps.ps1 -User YOUR_VPS_USERNAME
```

This now uses **fast deploy mode** by default and skips the heavy uploaded-media folders (`static/images/gallery` and `static/images/events`) so routine updates do not stall on a huge upload.

It also now **preserves live editable site data** by default, so files like `events_data.json`, `announcements_data.json`, `users_data.json`, and other JSON content files on the server are not overwritten during routine deploys.

If you need a full media sync too, run:

```powershell
powershell -ExecutionPolicy Bypass -File .\deploy\vps\publish_to_vps.ps1 -User YOUR_VPS_USERNAME -IncludeUploads
```

If you intentionally want to replace the live JSON content with the copies from this PC, use:

```powershell
powershell -ExecutionPolicy Bypass -File .\deploy\vps\publish_to_vps.ps1 -User YOUR_VPS_USERNAME -IncludeContentData
```

Or simply double-click:

```text
deploy\vps\publish_to_vps.bat
```

This will:
- build the deploy zip
- upload it to the VPS
- extract it into `/var/www/web_server`
- run the remote update script automatically

### Manual fallback

If you ever upload changed files manually to `/var/www/web_server`, then run:

```bash
cd /var/www/web_server
bash deploy/vps/deploy_update.sh
```
