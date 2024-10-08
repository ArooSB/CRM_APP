from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from crm_backend.config import Config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    """Create and configure the Flask application."""
    # Initialize the Flask application
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Register blueprints
    from crm_backend.routes import register_blueprints
    register_blueprints(app)

    return app

# Main entry point for the application
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5002)
