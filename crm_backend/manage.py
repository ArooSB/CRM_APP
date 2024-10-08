from crm_backend import app, db
from crm_backend.models import Worker

@app.cli.command('create_db')
def create_db():
    db.create_all()
    print("Database created!")

@app.cli.command('drop_db')
def drop_db():
    db.drop_all()
    print("Database dropped!")

@app.cli.command('seed_db')
def seed_db():
    admin = Worker(username='admin', role='admin')
    admin.set_password('admin_password')
    db.session.add(admin)
    db.session.commit()
    print("Database seeded with admin user.")
