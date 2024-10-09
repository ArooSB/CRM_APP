from flask import Flask
from flask_migrate import Migrate, upgrade
from sqlalchemy import text
from crm_backend.backend_app import create_app
from crm_backend.db import *
from crm_backend.models import *
from sqlalchemy import inspect

# Initialize the app and migration
app = create_app()
migrate = Migrate(app, db)

# Flask CLI command to check database connection
@app.cli.command('check_db')
def check_db():
    """Check if the database connection is working."""
    try:
        with app.app_context():
            # Perform a simple query to test the connection
            db.session.execute(text('SELECT 1'))
        print("Database connection successful!")
    except Exception as e:
        print(f"Error connecting to the database: {str(e)}")

# Flask CLI command to create the database
@app.cli.command('create_db')
def create_db():
    """Create the database and all necessary tables."""
    try:
        with app.app_context():
            db.create_all()  # Create all tables based on models
            print("Database created successfully!")
            print("Created tables:", db.metadata.tables.keys())  # Display created tables
    except Exception as e:
        print(f"Error creating database: {str(e)}")

# Flask CLI command to drop all tables in the database
@app.cli.command('drop_db')
def drop_db():
    """Drop all tables in the database."""
    try:
        with app.app_context():
            db.drop_all()  # Drop all tables in the database
        print("Database dropped successfully!")
    except Exception as e:
        print(f"Error dropping database: {str(e)}")



@app.cli.command('seed_db')
def seed_db():
    """Seed the database with an initial admin user."""
    try:
        with app.app_context():
            # Use `inspect` to check if the workers table exists
            inspector = inspect(db.engine)
            if not inspector.has_table('workers'):
                print("Error: 'workers' table does not exist. Please run 'create_db' first.")
                return

            # Check if an admin user already exists
            admin = Worker.query.filter_by(email='admin@example.com').first()
            if not admin:
                # Create an admin user if it doesn't exist
                admin = Worker(first_name='Admin', last_name='User', email='admin@example.com', position='admin')
                admin.set_password('admin_password')  # Set password for admin user
                db.session.add(admin)
                db.session.commit()
                print("Admin user seeded into the database.")
            else:
                print("Admin user already exists.")
    except Exception as e:
        print(f"Error seeding database: {str(e)}")


# Flask CLI command to reset the database (drop, create, and seed)
@app.cli.command('reset_db')
def reset_db():
    """Reset the database by dropping, creating, and seeding it."""
    drop_db()  # Drop all tables
    create_db()  # Create all tables
    seed_db()  # Seed the database with initial data
    print("Database has been reset and seeded with initial data.")

# Flask CLI command to list all users
@app.cli.command('list_users')
def list_users():
    """List all users in the database."""
    try:
        with app.app_context():
            users = Worker.query.all()
            if users:
                print("List of users:")
                for user in users:
                    print(f"ID: {user.id}, Name: {user.first_name} {user.last_name}, Email: {user.email}, Position: {user.position}")
            else:
                print("No users found.")
    except Exception as e:
        print(f"Error listing users: {str(e)}")

# Flask CLI command to upgrade the database using migrations
@app.cli.command('db_upgrade')
def upgrade_db():
    """Apply migrations to upgrade the database."""
    try:
        with app.app_context():
            upgrade()  # Perform the database upgrade
        print("Database upgraded successfully!")
    except Exception as e:
        print(f"Error upgrading database: {str(e)}")

# Main entry point to run the application
if __name__ == "__main__":
    app = create_app()  # Initialize the application
    try:
        app.run(debug=True, port=5003)  # Run the app on port 5003
    except Exception as e:
        print(f"Error starting the application: {str(e)}")
