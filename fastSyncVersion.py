import paramiko
import os

# --- CONFIGURATION ---
hostname = '129.121.84.30'
username = 'root'
password = '2027March!' 
local_path = r'C:\desktop\churchNewsletter'
remote_path = '/var/www/web_server'

# ONLY upload these folders and files
REQUIRED_FOLDERS = ['static', 'templates', 'data']
REQUIRED_FILES = ['app.py', 'requirements.txt'] 

def sync_files():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, username=username, password=password, timeout=30)
        sftp = client.open_sftp()

        print(f"Starting CLEAN sync to {remote_path}...")

        for root, dirs, files in os.walk(local_path):
            # Calculate relative path
            rel_root = os.path.relpath(root, local_path)
            
            # Only enter directories we want
            if rel_root != "." and not any(rel_root.startswith(f) for f in REQUIRED_FOLDERS):
                continue

            for file in files:
                # Check if it's a file we want
                is_required_file = file in REQUIRED_FILES
                is_in_required_dir = any(rel_root.startswith(f) for f in REQUIRED_FOLDERS)

                if is_required_file or is_in_required_dir:
                    local_file = os.path.join(root, file)
                    rel_path = os.path.relpath(local_file, local_path).replace('\\', '/')
                    remote_file = os.path.join(remote_path, rel_path).replace('\\', '/')

                    # Ensure remote directory exists
                    remote_dir = os.path.dirname(remote_file)
                    try:
                        sftp.stat(remote_dir)
                    except FileNotFoundError:
                        current_dir = ""
                        for part in remote_dir.split('/'):
                            if part:
                                current_dir += "/" + part
                                try: sftp.mkdir(current_dir)
                                except: pass

                    print(f"Uploading: {rel_path}")
                    sftp.put(local_file, remote_file)

        sftp.close()

        # Finalize permissions and restart
        print("Finalizing...")
        client.exec_command(f"chown -R www-data:www-data {remote_path}")
        client.exec_command("systemctl restart ehbcnewsletter.service")
        
        print("✅ Clean sync complete!")
        client.close()

    except Exception as e:
        print(f"❌ Sync failed: {e}")

if __name__ == "__main__":
    sync_files()