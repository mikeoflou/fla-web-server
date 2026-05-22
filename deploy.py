import paramiko
import os

# CONFIGURE THESE VALUES
HOST = 'your.bluehost.server.com'  # e.g., box123.bluehost.com
USERNAME = 'your_ftp_username'
PASSWORD = 'your_ftp_password'
LOCAL_PATH = os.path.abspath('.')  # Local project root
REMOTE_PATH = '/home/yourcpanelusername/public_html'  # Remote web root

# Only upload users_data.json
FILES_TO_UPLOAD = ['users_data.json']

def upload_file(sftp, local_file, remote_file):
    sftp.put(local_file, remote_file)
    print(f"Uploaded {local_file} -> {remote_file}")

def main():
    transport = paramiko.Transport((HOST, 22))
    transport.connect(username=USERNAME, password=PASSWORD)
    sftp = paramiko.SFTPClient.from_transport(transport)
    try:
        for filename in FILES_TO_UPLOAD:
            local_file = os.path.join(LOCAL_PATH, filename)
            remote_file = os.path.join(REMOTE_PATH, filename)
            upload_file(sftp, local_file, remote_file)
    finally:
        sftp.close()
        transport.close()
        print("Done.")

if __name__ == '__main__':
    main()
