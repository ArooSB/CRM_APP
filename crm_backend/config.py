import os

class Config:
    """Base configuration class for the application.

    This class contains the base settings for the application, including database,
    JWT, logging, and general application settings. Subclasses can inherit from
    this class to customize settings for different environments.
    """

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///crm.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'my-secret-key')
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = os.getenv('PORT', '5002')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'app.log')
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')


class DevelopmentConfig(Config):
    """Configuration settings for the development environment.

    Inherits from the base configuration and enables debug mode.
    It also specifies the database URI for the development database.
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL', 'sqlite:///dev_crm.db')


class TestingConfig(Config):
    """Configuration settings for the testing environment.

    Inherits from the base configuration and enables testing mode.
    It specifies the database URI for the testing database.
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL', 'sqlite:///test_crm.db')


class ProductionConfig(Config):
    """Configuration settings for the production environment.

    Inherits from the base configuration and disables debug mode.
    It specifies the database URI for the production database.
    """
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///prod_crm.db')
    DEBUG = False


config_map = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}


def get_config():
    """Retrieve the appropriate configuration class based on the environment variable.

    This function checks the FLASK_ENV environment variable to determine which
    configuration class to use. If the environment variable is not set,
    it defaults to the development configuration.

    Returns:
        Config: An instance of the selected configuration class.
    """
    env = os.getenv('FLASK_ENV', 'development')
    return config_map.get(env, DevelopmentConfig)()
