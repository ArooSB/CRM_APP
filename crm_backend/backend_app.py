from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from crm_backend.config import Config
from crm_backend.db import db

# Initialize other extensions
migrate = Migrate()
jwt = JWTManager()

def create_app():
    """
    Create and configure the Flask application.

    This function initializes the Flask application, sets up the configuration,
    and initializes various extensions such as the database, migrations, and JWT.

    It performs the following steps:
    1. Initializes the Flask application instance.
    2. Loads the configuration from the specified configuration object.
    3. Initializes the database extension with the app.
    4. Initializes the migration extension with the app and database.
    5. Initializes the JWT extension with the app.
    6. Registers blueprints to organize application routes.

    Returns:
        Flask: The configured Flask application instance ready for use.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from crm_backend.routes import register_blueprints
    register_blueprints(app)

    return app

if __name__ == "__main__":
    app = create_app()
    try:
        app.run(debug=True, port=5004)
    except Exception as e:
        print(f"Error starting the application: {str(e)}")
