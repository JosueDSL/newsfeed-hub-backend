# Import the configuration classes from the config module
from config import (
    DevelopmentConfig,
    DevelopmentDockerConfig,
    # ProductionConfig,          # Another config class examples, just for common usage reference:
    # QAConfig
)

# Import main Flask class and necessary extensions
from flask import Flask

# Import the database configuration
from database import init_db, create_tables

# Import the extensions for the app
from application.extensions import jwt, migrate

# Import the CORS module
from flask_cors import CORS

# Import logging
import logging

# Import the models to create the tables
from application.models import User, Feed, Topic, Resource



def create_app():

    # Create an instance of the Flask application
    app = Flask(__name__)


    """
        NOTE: Change the configuration class to match the desired environment.
        Options:
        - DevelopmentConfig: For local development
        - DevelopmentDockerConfig: For Docker development

        Example:
        app.config.from_object(DevelopmentConfig)  # Use this for local development
        app.config.from_object(DevelopmentDockerConfig)  # Use this for Docker development
    """

    # Load the configuration from the config.py file
    app.config.from_object(DevelopmentConfig)
    # print(app.config)

    # Initialize extensions

    # Initialize the database with the newly created app
    init_db(app)
    with app.app_context():
        create_tables(app)

    # Initialize the migration extension
    # Import the db object from the application module
    from database import db

    migrate.init_app(app, db)


    # Initialize objects of the extensions
    jwt.init_app(app)

    # Configure CORS to allow requests from any origin
    CORS(app, supports_credentials=True, origins=["http://front-end-url-if-apply", "http://localhost:5000"], allow_headers=["Content-Type", "Authorization", "X-CSRF-TOKEN", "Set-Cookie"], expose_headers=["Content-Type", "Authorization", "X-CSRF-TOKEN", "Set-Cookie"])


    # Import the blueprints
    from .blueprints import auth_bp, user_bp, feeds_bp

    # Register the blueprints with url prefixes
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(feeds_bp, url_prefix='/feeds')



    # # Import the function here to avoid circular import
    # from application.services.database_initial_population_service import seed_all_tables

    # # Run the function once initially
    # seed_all_tables(app)


    # Configure logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        handlers=[
                            logging.FileHandler('app.log'),
                            logging.StreamHandler()
                        ])
    app.logger = logging.getLogger(__name__)


    return app



