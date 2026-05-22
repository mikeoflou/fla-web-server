
import os
print(f"DEBUG: I am running in: {os.getcwd()}")
print(f"DEBUG: I see these files/folders here: {os.listdir('.')}")
from fabric import Connection


# --- CONNECTION SETTINGS ---
host = "127.0.0.1"
user = "root"  # If this fails, change to "ubuntu"
key_path = r"C:\desktop\churchNewsletter\id_rsa"
key_pass = "2027May!"
remote_base = "/var/www/churchNewsletter/"

# ==========================================
# --- WHAT TO UPLOAD TODAY ---
# ==========================================

# 1. SPECIFIC FILES
# Add individual files you want to sync right now.

files_to_sync = [
    ('main.py', 'main.py'),
    ('requirements.txt', 'requirements.txt')
]

    # You can also add a single image here if you don't want to push a whole folder:


# 2. ENTIRE FOLDERS
# Add specific folders you want to sync. 
# To skip syncing folders, just leave this empty like this: folders_to_sync = []
folders_to_sync = [
    
    
    # Use the '#' symbol to temporarily disable a folder without deleting the line:
    # 'static/images/YouthMinistry', 
]

# ==========================================


def get_folder_sync_tuples(folder_path):
    """Scans a local folder and generates upload tuples."""
    sync_list = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            local_path = os.path.join(root, file)
            remote_path = local_path.replace("\\", "/")
            sync_list.append((local_path, remote_path))
    return sync_list

# Combine the specific files and the specific folders into one master list
image_tuples = []
for folder in folders_to_sync:
    if os.path.exists(folder):
        # 'extend' adds all the items from the folder scan into our image_tuples list
        image_tuples.extend(get_folder_sync_tuples(folder))
    else:
        print(f"Warning: The folder '{folder}' was not found locally.")

all_uploads = files_to_sync + image_tuples
    
def deploy():
    conn = Connection(
        host=host,
        user=user,
        connect_kwargs={
            "key_filename": key_path,
            "passphrase": key_pass,
        }
    )

    try:
        print(f"Connecting to {host} via Fabric...")
        
        # Ensure we actually have things to upload
        if not all_uploads:
            print("No files or folders specified for upload today. Skipping sync.")
        else:
            for local, remote in all_uploads:
                if os.path.exists(local):
                    print(f"Pushing {local}...")
                    remote_full_path = os.path.join(remote_base, remote).replace('\\', '/')
                    remote_dir = os.path.dirname(remote_full_path)
                    
                    conn.run(f"mkdir -p {remote_dir}")
                    conn.put(local, remote_full_path)
                else:
                    print(f"Skipping {local} - File not found locally.")

        print("\n--- RESTARTING SERVICES ---")
        conn.sudo("systemctl restart ehbcnewsletter", warn=True)
        conn.sudo("systemctl restart nginx", warn=True)
        
        print("\nDeployment Successful!")

    except Exception as e:
        print(f"Deployment failed: {e}")

if __name__ == "__main__":
    deploy()