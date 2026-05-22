from server import app, db, User, Post

def reset_database():
    with app.app_context():
        # 1. Wipe everything
        db.drop_all()
        db.create_all()
        print("Database cleared and recreated.")

        # 2. Create your Admin User (Mike)
        admin = User(
            username='Mike', 
            password='password123', # Change this to your preferred password
            pin=1234,               # Change this to your preferred pin
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit() # Commit so we have an ID for the post
        print(f"Admin user '{admin.username}' created.")

        # 3. Create your 'Hello World' Post
        hello_post = Post(
            title="Hello World",
            content="This is my first official post. The database is back online!",
            author=admin # This uses the 'backref' we set up earlier
        )
        db.session.add(hello_post)
        db.session.commit()
        print("Hello World post published.")

if __name__ == "__main__":
    reset_database()
    print("\nSystem Ready! Login at http://127.0.0.1:5000/login")