from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from crm_backend.config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

from crm_backend.routes import workers, customers, sales_leads, interactions, support_tickets, analytics
app.register_blueprint(workers.bp)
app.register_blueprint(customers.bp)
app.register_blueprint(sales_leads.bp)
app.register_blueprint(interactions.bp)
app.register_blueprint(support_tickets.bp)
app.register_blueprint(analytics.bp)

if __name__ == "__main__":
    app.run(debug=True)
