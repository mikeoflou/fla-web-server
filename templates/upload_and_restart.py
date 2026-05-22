import paramiko
import os

host = '129.121.84.30'
user = 'root'
password = r'2027April!'

# Local and Remote paths
local_file = r'C:\desktop\web_Server\templates\login.html'
remote_file = '/var/www/web_server/templates/login.html'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh.connect(host, username=user, password=password)
    
    # 1. Use SFTP via Paramiko to upload the file
    sftp = ssh.open_sftp()
    print(f"Uploading {os.path.basename(local_file)}...")
    sftp.put(local_file, remote_file)
    sftp.close()
    
    # 2. Restart the service
    print("Restarting the EHBC service...")
    ssh.exec_command("systemctl restart ehbc")
    
    print("\nSUCCESS! The 'Note' box should be gone now.")
    print("Go to ehbcnewsletterjeff.org/login and press Ctrl + F5.")

except Exception as e:
    print(f"Error: {e}")
finally:
    ssh.close()