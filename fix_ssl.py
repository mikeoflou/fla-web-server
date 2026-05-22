from fabric import Connection

# --- CONNECTION SETTINGS ---
host = "129.121.84.30"
user = "root"  
key_path = r"C:\desktop\churchNewsletter\id_rsa"
key_pass = "2027May!"

def fix_ssl():
    conn = Connection(
        host=host,
        user=user,
        connect_kwargs={
            "key_filename": key_path,
            "passphrase": key_pass,
        }
    )

    try:
        print("Connecting to server to fix SSL...")
        
        # 1. Update package list
        print("Updating package list...")
        conn.sudo("apt-get update")
        
        # 2. Install Certbot and Nginx plugin
        print("Installing Certbot...")
        conn.sudo("apt-get install -y certbot python3-certbot-nginx")
        
        # 3. Request the certificate 
        # (Using --register-unsafely-without-email to bypass the interactive email prompt)
        print("Generating SSL Certificate for ehbcnewsletterjeff.org...")
        cert_command = (
            "certbot --nginx -d ehbcnewsletterjeff.org -d www.ehbcnewsletterjeff.org "
            "--non-interactive --agree-tos --register-unsafely-without-email"
        )
        conn.sudo(cert_command)
        
        # 4. Restart Nginx to apply changes
        print("Restarting Nginx...")
        conn.sudo("systemctl restart nginx")
        
        print("\nSuccess! The SSL certificate is installed.")
        print("Cloudflare should now be able to securely connect to your VPS.")

    except Exception as e:
        print(f"Failed to fix SSL: {e}")

if __name__ == "__main__":
    fix_ssl()