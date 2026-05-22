import paramiko

host = '129.121.84.30'
user = 'root'
password = '2027January!'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, username=user, password=password, timeout=30)

commands = [
    'apt-get update -qq',
    'DEBIAN_FRONTEND=noninteractive apt-get install -y unzip python3 python3-venv python3-pip nginx',
    'id ubuntu >/dev/null 2>&1 || adduser --disabled-password --gecos "" ubuntu',
    'usermod -aG www-data ubuntu',
    'cd /var/www/web_server && unzip -o web_server_vps_20260331_125456.zip',
    'cd /var/www/web_server && python3 -m venv .venv',
    'cd /var/www/web_server && .venv/bin/pip install --upgrade pip -q',
    'cd /var/www/web_server && .venv/bin/pip install -r requirements.txt gunicorn -q',
    'cp /var/www/web_server/deploy/vps/web_server.service /etc/systemd/system/web_server.service',
    'cp /var/www/web_server/deploy/vps/nginx_web_server.conf /etc/nginx/sites-available/web_server',
    'ln -sf /etc/nginx/sites-available/web_server /etc/nginx/sites-enabled/web_server',
    'rm -f /etc/nginx/sites-enabled/default',
    'systemctl daemon-reload',
    'systemctl enable --now web_server',
    'nginx -t',
    'systemctl reload nginx',
    'systemctl status web_server --no-pager -l | head -30',
    'curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000',
]

for cmd in commands:
    print(f'\n>>> {cmd}')
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=180)
    out = stdout.read().decode().strip()
    err = stderr.read().decode().strip()
    if out:
        print(out)
    if err:
        print('ERR:', err)

ssh.close()
print('\nDeployment complete.')
