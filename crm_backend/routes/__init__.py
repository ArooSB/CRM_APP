
from flask import Blueprint

# Define blueprints for each route
workers_bp = Blueprint('workers', __name__)
customers_bp = Blueprint('customers', __name__)
sales_leads_bp = Blueprint('sales_leads', __name__)
interactions_bp = Blueprint('interactions', __name__)
support_tickets_bp = Blueprint('support_tickets', __name__)
analytics_bp = Blueprint('analytics', __name__)

def register_blueprints(app):
    app.register_blueprint(workers_bp)
    app.register_blueprint(customers_bp)
    app.register_blueprint(sales_leads_bp)
    app.register_blueprint(interactions_bp)
    app.register_blueprint(support_tickets_bp)
    app.register_blueprint(analytics_bp)
