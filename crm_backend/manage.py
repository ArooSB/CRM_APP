from flask_migrate import Migrate, upgrade
from sqlalchemy import text
from crm_backend.backend_app import create_app
from crm_backend.db import db
from crm_backend.models import Worker
from sqlalchemy import inspect

# Initialize the app and migration
app = create_app()
migrate = Migrate(app, db)

@app.cli.command('check_db')
def check_db():
    """Check if the database connection is functioning properly.

    This command executes a simple query to ensure that the database
    connection is active. If successful, it prints a confirmation message;
    otherwise, it prints an error message indicating the issue.
    """
    try:
        with app.app_context():
            db.session.execute(text('SELECT 1'))
        print("Database connection successful!")
    except Exception as e:
        print(f"Error connecting to the database: {str(e)}")

@app.cli.command('create_db')
def create_db():
    """Create the database and all necessary tables.

    This command initializes the database and creates all tables defined
    in the models. Upon success, it prints a success message along with
    the names of the created tables.
    """
    try:
        with app.app_context():
            db.create_all()
            print("Database created successfully!")
            print("Created tables:", db.metadata.tables.keys())
    except Exception as e:
        print(f"Error creating database: {str(e)}")

@app.cli.command('drop_db')
def drop_db():
    """Drop all tables in the database.

    This command removes all tables from the database. Upon success,
    it prints a message confirming the operation.
    """
    try:
        with app.app_context():
            db.drop_all()
        print("Database dropped successfully!")
    except Exception as e:
        print(f"Error dropping database: {str(e)}")

@app.cli.command('seed_db')
def seed_db():
    """Seed the database with an initial admin user.

    This command checks if the 'workers' table exists and seeds the
    database with an initial admin user if none exists. If the admin
    user already exists, it prints a message indicating so.
    """
    try:
        with app.app_context():
            inspector = inspect(db.engine)
            if not inspector.has_table('workers'):
                print("Error: 'workers' table does not exist. Please run 'create_db' first.")
                return

            admin = Worker.query.filter_by(email='admin@example.com').first()
            if not admin:
                admin = Worker(first_name='Admin', last_name='User', email='admin@example.com', position='admin')
                admin.set_password('admin_password')
                db.session.add(admin)
                db.session.commit()
                print("Admin user seeded into the database.")
            else:
                print("Admin user already exists.")
    except Exception as e:
        print(f"Error seeding database: {str(e)}")

@app.cli.command('reset_db')
def reset_db():
    """Reset the database by dropping, creating, and seeding it.

    This command performs a full reset of the database by dropping all
    tables, creating them again, and seeding the database with initial
    data, including an admin user.
    """
    drop_db()
    create_db()
    seed_db()
    print("Database has been reset and seeded with initial data.")

@app.cli.command('list_users')
def list_users():
    """List all users in the database.

    This command retrieves and prints a list of all users in the
    'workers' table, displaying their ID, name, email, and position.
    If no users are found, it prints an appropriate message.
    """
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

@app.cli.command('db_upgrade')
def upgrade_db():
    """Apply migrations to upgrade the database.

    This command runs database migrations to apply any pending changes.
    Upon success, it prints a confirmation message.
    """
    try:
        with app.app_context():
            upgrade()
        print("Database upgraded successfully!")
    except Exception as e:
        print(f"Error upgrading database: {str(e)}")

if __name__ == "__main__":
    app = create_app()
    try:
        app.run(debug=True, port=5003)
    except Exception as e:
        print(f"Error starting the application: {str(e)}")
