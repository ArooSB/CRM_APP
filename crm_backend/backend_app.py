
from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from crm_backend.config import Config
from crm_backend.db import db  # Import db from db.py


# Initialize other extensions
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)  # Initialize db
    migrate.init_app(app, db)  # Initialize migrations
    jwt.init_app(app)  # Initialize JWT

    # Register blueprints for routes
    from crm_backend.routes import register_blueprints
    register_blueprints(app)

    return app

if __name__ == "__main__":
    app = create_app()
    try:
        app.run(debug=True, port=5004)
    except Exception as e:
        print(f"Error starting the application: {str(e)}")
