import os
from server import app, db

# 1. Get the absolute path to the instance folder
basedir = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(basedir, 'instance')

# 2. Create the folder if it doesn't exist
if not os.path.exists(instance_path):
    os.makedirs(instance_path)
    print(f"Created folder: {instance_path}")

# 3. Build the database
with app.app_context():
    # This deletes old tables and creates new ones with the PIN column
    db.drop_all()
    db.create_all()
    print("------------------------------------------")
    print("SUCCESS: Database created with PIN column!")
    print(f"Location: {os.path.join(instance_path, 'database.db')}")
    print("------------------------------------------")