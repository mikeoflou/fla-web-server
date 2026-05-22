import paramiko
import os
from datetime import datetime

# --- Configuration ---
host = '129.121.84.30'
user = 'root'
password = r'2027April!'
local_root = r'c:/desktop/churchNewsletter'
remote_root = '/var/www/churchNewsletter'
log_file_path = r'c:/desktop/churchNewsletter/publish_log.txt't

# --- Connection Setup ---
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh.connect(host, username=user, password=password)
    sftp = ssh.open_sftp()
    
    print("🚀 Starting Master Sync to Eastern Heights Server...")

    for root, dirs, files in os.walk(local_root):
        # Strictly ignore system, virtual env, and IDE folders
        ignored_folders = ['venv', '.vscode', '__pycache__', 'Include', 'Lib', 'Scripts', '.git', 'python-lyrics-transcriber-main']
        if any(x in root for x in ignored_folders):
            continue
            
        for file in files:
            # Skip local backups, ff*, agentic*, music videos .mp4, and the script itself
            if file.endswith('.zip') or file.endswith('.mp4') or file.startswith('ff') or file.startswith('agentic') or file == 'sync_all.py' or file == 'publish_log.txt' or (file.endswith('.jpg') and not any(keep in file for keep in ['church_exterior.jpg', 'welcome.jpg', 'SeniorBibleStudy.jpg', '2026AfternoonTea.png'])):
                continue
                
            local_path = os.path.join(root, file)
            # Create the matching path for the Linux server
            relative_path = os.path.relpath(local_path, local_root).replace('\\', '/')
            remote_path = f"{remote_root}/{relative_path}"
            
            # Ensure the remote directory exists before uploading
            remote_dir = os.path.dirname(remote_path)
            try:
                sftp.mkdir(remote_dir)
            except IOError:
                pass # Directory already exists

            print(f"Uploading: {relative_path}")
            sftp.put(local_path, remote_path)

    sftp.close()
    
    print("\n♻️ Restarting EHBC Service...")
    ssh.exec_command("systemctl restart ehbc")
    
    # --- Update Local Log ---
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file_path, "a") as log:
        log.write(f"Successful Publish: {now}\n")
        
    print(f"✅ All changes are live at https://ehbcnewsletterjeff.org/login")
    print(f"Logged at: {now}")

except Exception as e:
    print(f"❌ Error during sync: {e}")
finally:
    ssh.close()