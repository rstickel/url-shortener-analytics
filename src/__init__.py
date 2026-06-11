import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

# Initialize extensions outside of create_app
db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()


def create_app(config_name='default'):
    """Factory function to create the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    # Load configuration from config.py based on config_name
    from src.config import config_by_name
    app.config.from_object(config_by_name[config_name])

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    # Register blueprints
    from src.views import main_bp
    app.register_blueprint(main_bp)

    # Basic error handlers
    @app.errorhandler(404)
    def page_not_found(error):
        return '<h1>404 Not Found</h1><p>The page you requested could not be found.</p>', 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return '<h1>500 Internal Server Error</h1><p>An unexpected error occurred.</p>', 500

    return app
