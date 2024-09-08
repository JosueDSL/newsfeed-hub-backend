# Description: This file initializes the database with the provided app or the current app. It also creates all tables if they don't exist.

# Import the required modules
from flask_sqlalchemy import SQLAlchemy
from flask import current_app
from flask_migrate import Migrate

# Initialize the SQLAlchemy object
db = SQLAlchemy()

# Function to initialize the database with the provided app or the current app
def init_db(app=None):
    # If the app is not provided, use the current app
    if app is None:
        app = current_app

    # Initialize the database with the app
    db.init_app(app)

# Create all tables if they don't exist
def create_tables(app):
    with app.app_context():
        db.create_all()