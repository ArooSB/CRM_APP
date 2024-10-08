from crm_backend.backend_app import create_app, db
from crm_backend.models import Worker
from sqlalchemy import text

app = create_app()


@app.cli.command('check_db')
def check_db():
    """Check database connection."""
    try:
        with app.app_context():
            db.session.execute(text('SELECT 1'))  # Wrap the SQL expression in text()
        print("Database connection successful!")
    except Exception as e:
        print(f"Error connecting to database: {str(e)}")

@app.cli.command('create_db')
def create_db():
    """Create the database."""
    try:
        with app.app_context():
            db.create_all()
            print("Database created successfully!")
            print("Created tables:", db.metadata.tables.keys())  # This will show the created tables
    except Exception as e:
        print(f"Error creating database: {str(e)}")

@app.cli.command('drop_db')
def drop_db():
    """Drop the database."""
    try:
        with app.app_context():
            db.drop_all()  # Drop all tables
        print("Database dropped!")
    except Exception as e:
        print(f"Error dropping database: {str(e)}")

@app.cli.command('seed_db')
def seed_db():
    """Seed the database with initial data."""
    try:
        with app.app_context():
            # Check if the table exists
            if 'workers' not in db.metadata.tables:
                print("Error: 'workers' table does not exist. Please run 'create_db' first.")
                return

            admin = Worker.query.filter_by(email='admin@example.com').first()
            if not admin:
                admin = Worker(name='admin', email='admin@example.com', position='admin')
                admin.set_password('admin_password')
                db.session.add(admin)
                db.session.commit()
                print("Database seeded with admin user.")
            else:
                print("Admin user already exists.")
    except Exception as e:
        print(f"Error seeding database: {e}")


@app.cli.command('reset_db')
def reset_db():
    """Reset the database (drop and create)."""
    drop_db()  # Drop the database
    create_db()  # Create the database and tables
    seed_db()  # Seed the database with initial data
    print("Database has been reset and seeded with initial data.")

@app.cli.command('list_users')
def list_users():
    """List all users in the database."""
    try:
        with app.app_context():
            users = Worker.query.all()
            if users:
                print("List of users:")
                for user in users:
                    print(f"ID: {user.id}, Name: {user.name}, Email: {user.email}, Position: {user.position}")
            else:
                print("No users found.")
    except Exception as e:
        print(f"Error listing users: {str(e)}")

if __name__ == "__main__":
    app.run()  # Run the app if this script is executed directly
