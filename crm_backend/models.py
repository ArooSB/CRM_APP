from crm_backend import db
from werkzeug.security import generate_password_hash, check_password_hash

class Customer(db.Model):
    __tablename__ = 'customers'
    __table_args__ = {'extend_existing': True}  # Allow redefining the table

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    company = db.Column(db.String(100))
    address = db.Column(db.String(200))

    # Establish relationships to related entities (optional but useful)
    sales_leads = db.relationship('SalesLead', backref='customer', lazy=True)
    interactions = db.relationship('Interaction', backref='customer', lazy=True)
    support_tickets = db.relationship('SupportTicket', backref='customer', lazy=True)


class Worker(db.Model):
    __tablename__ = 'workers'
    __table_args__ = {'extend_existing': True}  # Allow redefining the table

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    position = db.Column(db.String(100))
    password_hash = db.Column(db.String(128))  # Field to store hashed password

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class SalesLead(db.Model):
    __tablename__ = 'sales_leads'
    __table_args__ = {'extend_existing': True}  # Allow redefining the table

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    status = db.Column(db.String(50))


class Interaction(db.Model):
    __tablename__ = 'interactions'
    __table_args__ = {'extend_existing': True}  # Allow redefining the table

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    notes = db.Column(db.Text)


class SupportTicket(db.Model):
    __tablename__ = 'support_tickets'
    __table_args__ = {'extend_existing': True}  # Allow redefining the table

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50))


class Analytics(db.Model):
    __tablename__ = 'analytics'
    __table_args__ = {'extend_existing': True}  # Allow redefining the table

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Text)
