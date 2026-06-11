import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration class."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'a_default_secret_key_if_not_set_in_env')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Default to SQLite for development, can be overridden by DATABASE_URL
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///instance/app.db')


class DevelopmentConfig(Config):
    """Development specific configuration."""
    DEBUG = True


class TestingConfig(Config):
    """Testing specific configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL', 'sqlite:///:memory:')
    WTF_CSRF_ENABLED = False  # Disable CSRF during testing for easier form submission


class ProductionConfig(Config):
    """Production specific configuration."""
    DEBUG = False
    # In production, DATABASE_URL should always be set securely
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
